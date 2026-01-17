from abc import ABC, abstractmethod
from utils.logger import logger

class ITranscriptionStrategy(ABC):
    """
    转录后处理策略接口。
    规定了所有处理器都必须实现 process 方法。
    """
    @abstractmethod
    def process(self, chunk_output_list, chunk_offset_sec: float) -> list:
        """
        处理模型输出的原始数据，返回标准化的字幕段落列表。
        Args:
            chunk_output_list: NeMo 模型 transcribe 方法的返回结果
            chunk_offset_sec: 当前音频块的起始时间偏移量（秒）
        Returns:
            list: [{'start': float, 'end': float, 'segment': str}, ...]
        """
        pass

class DefaultSegmentStrategy(ITranscriptionStrategy):
    """
    【策略 A】: 默认段落处理策略。
    适用于英语等 segment 输出准确的模型。
    直接读取 timestamp['segment']。
    """
    def process(self, chunk_output_list, chunk_offset_sec: float) -> list:
        segments = []
        
        # 安全检查
        if not chunk_output_list or not hasattr(chunk_output_list[0], "timestamp") or not chunk_output_list[0].timestamp:
            return []

        # 直接提取 segment
        if "segment" in chunk_output_list[0].timestamp:
            current_chunk_segments = chunk_output_list[0].timestamp["segment"]
            for segment_data in current_chunk_segments:
                local_start = segment_data["start"]
                local_end = segment_data["end"]
                # 优先取 segment，没有则取 text
                text = segment_data.get("segment", segment_data.get("text", ""))

                global_start = local_start + chunk_offset_sec
                global_end = local_end + chunk_offset_sec

                if global_end < global_start:
                    global_end = global_start + 0.05

                segments.append({
                    "start": global_start,
                    "end": global_end,
                    "segment": text
                })
        
        return segments

class JapaneseCharStrategy(ITranscriptionStrategy):
    """
    【策略 B】: 日语字符级重组策略 (V3 算法)。
    适用于 Parakeet 日语 TDT 模型。
    读取 timestamp['char'] 并智能重组。
    """
    def process(self, chunk_output_list, chunk_offset_sec: float) -> list:
        char_timestamps = []

        # 安全检查
        if not chunk_output_list or not hasattr(chunk_output_list[0], "timestamp") or not chunk_output_list[0].timestamp:
            return []

        # 1. 提取所有 Char 并转换为全局时间
        if "char" in chunk_output_list[0].timestamp:
            current_chunk_chars = chunk_output_list[0].timestamp["char"]
            for char_data in current_chunk_chars:
                char_c = char_data.get('char')
                if isinstance(char_c, list):
                    char_c = "".join(char_c)
                
                char_timestamps.append({
                    "char": char_c,
                    "start": char_data["start"] + chunk_offset_sec,
                    "end": char_data["end"] + chunk_offset_sec
                })
        
        # 2. 调用智能重组算法
        return self._group_chars_into_segments(char_timestamps)

    def _group_chars_into_segments(
        self, char_timestamps: list, max_duration: float = 8.0, soft_limit_chars: int = 20, hard_limit_chars: int = 40
    ) -> list:
        """V3 智能断句核心算法"""
        if not char_timestamps:
            return []

        segments = []
        current_segment_chars = []
        current_segment_start = None

        strong_endings = {'。', '！', '？', '!', '?', '…', '.', '\n'}
        weak_pauses = {'、', '，', ',', ' ', '　'}
        SILENCE_THRESHOLD = 0.45

        for i, char_data in enumerate(char_timestamps):
            char_text = char_data['char']
            char_start = char_data['start']
            char_end = char_data['end']

            if not char_text:
                continue

            if current_segment_start is None:
                current_segment_start = char_start

            current_segment_chars.append(char_text)

            should_break = False
            is_last_char = (i == len(char_timestamps) - 1)

            time_gap = 0.0
            if not is_last_char:
                next_char_start = char_timestamps[i + 1]['start']
                time_gap = next_char_start - char_end

            current_text_len = len(current_segment_chars)
            current_duration = char_end - current_segment_start

            if char_text in strong_endings:
                should_break = True
            elif time_gap > SILENCE_THRESHOLD:
                should_break = True
            elif current_text_len >= hard_limit_chars:
                should_break = True
            elif current_text_len >= soft_limit_chars and char_text in weak_pauses:
                should_break = True
            elif current_duration >= max_duration:
                if not is_last_char and char_timestamps[i + 1]['char'] not in strong_endings:
                    should_break = True

            if should_break or is_last_char:
                segment_text = "".join(current_segment_chars).strip()
                if segment_text and not all(c in weak_pauses or c in strong_endings for c in segment_text):
                    final_end = char_end
                    if (final_end - current_segment_start) < 0.5:
                        final_end = max(final_end, current_segment_start + 0.5)
                    
                    if not is_last_char and final_end > char_timestamps[i+1]['start']:
                         final_end = char_timestamps[i+1]['start'] - 0.01

                    segments.append({
                        'start': current_segment_start,
                        'end': final_end,
                        'segment': segment_text
                    })

                current_segment_chars = []
                current_segment_start = None

        return segments