
from interfaces import ISrtGenerator


class SrtService(ISrtGenerator):
    """
    生成 SRT 字幕文件内容的服务。
    """
       

    def _format_srt_time(self, seconds) -> str:
        """
        将秒数格式化为 SRT 时间格式 (HH:MM:SS,mmm)。
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds * 1000) % 1000)
        return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"



    def generate_srt_content(self, segment_timestamps: list) -> str:
        """
        根据时间戳列表生成 SRT 格式的字幕内容。
        ARGS:
            segment_timestamps: 包含 {'start': float, 'end': float, 'segment': str} 的列表。
        RETURNS:
            SRT 格式的字符串。
        """
        srt_content = ""
        for i, stamp in enumerate(segment_timestamps):
            subtitle_number = i + 1
            start_time_srt = self._format_srt_time(stamp["start"])
            end_time_srt = self._format_srt_time(stamp["end"])
            segment_text = stamp["segment"]
            srt_block = f"{subtitle_number}\n{start_time_srt} --> {end_time_srt}\n{segment_text}\n\n"
            srt_content += srt_block
        return srt_content
