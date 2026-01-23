import torch
import nemo.collections.asr as nemo_asr
from pydub import AudioSegment
import tempfile
import os
from utils.logger import logger
from interfaces import IASRService
from utils.exceptions import ModelLoadError
from core.post_processors import DefaultSegmentStrategy, JapaneseCharStrategy


class ASRService(IASRService):
    """封装所有与 NeMo ASR 模型相关的操作。"""

    def __init__(self) -> None:
        self.model = None
        self.device  = torch.device("cuda" if torch.cuda.is_available() else "cpu")

          # 当前使用的处理策略，默认为普通策略
        self.processor_strategy = DefaultSegmentStrategy()
        logger.info(f"ASRservice 初始化，使用设备: {self.device}")


    @property
    def is_model_loaded(self) -> bool:
        """检查 ASR 模型是否已加载。"""
        return self.model is not None
    
    def _update_strategy(self, model_name: str):
        """
        【工厂方法逻辑】：根据模型名称决定使用哪个策略。
        这是整个设计模式的核心切换点。
        """
        name_lower = model_name.lower()
        
        if "ja" in name_lower or "japanese" in name_lower:
            logger.info(f"模型 '{model_name}' 被识别为日语模型，切换至 [日语字符重组策略]。")
            self.processor_strategy = JapaneseCharStrategy()
        else:
            logger.info(f"模型 '{model_name}' 被识别为通用模型，切换至 [默认段落策略]。")
            self.processor_strategy = DefaultSegmentStrategy()


    def load_model_from_ngc(self, model_name: str) -> str:
        """从 NVIDIA NGC 加载预训练模型。"""
        try:
            self.model = nemo_asr.models.ASRModel.from_pretrained(
                model_name=model_name, map_location=self.device
            )
            # 加载成功后，更新策略
            self._update_strategy(model_name)
            return f"云端模型 '{model_name}' 加载成功。"
        except Exception as e:
            self.model = None
            return f"从NGC加载云端模型 '{model_name}' 失败: {e}"
        
    def load_model_from_local(self, model_path: str) -> str:
        """从本地 .nemo 文件加载模型。"""
        actual_path = model_path.strip()
        if not os.path.exists(actual_path) or not actual_path.endswith(".nemo"):
            return f"错误：指定的本地模型路径无效: {actual_path}"
        
        logger.info(f"尝试从本地路径加载模型: {actual_path}...")
        try:
            self.model = nemo_asr.models.ASRModel.restore_from(
                restore_path=actual_path, map_location=self.device
            )
            model_name = os.path.basename(actual_path)
              # 加载成功后，更新策略
            self._update_strategy(model_name)
            return f"本地模型 '{model_name}' 加载成功。"
        except Exception as e:
            self.model = None
            raise ModelLoadError(f"从本地路径加载模型失败: {e}") from e
        
    
    


    def transcribe_audio_in_chunks(self, audio_path: str, chunk_length_ms: int) -> list:
        """
        将音频文件分块转录并返回带有全局时间戳的段列表。
        ARGS:
            audio_path: 音频文件路径 (假设为 WAV)。
            chunk_length_ms: 每块的长度（毫秒）。
        RETURNS:
            包含 {'start': float, 'end': float, 'segment': str} 的列表。

        """
        if not self.is_model_loaded:
            logger.error("错误: ASR 模型未加载，无法进行转录。")
            return []
        

        if not audio_path or not os.path.exists(audio_path):
            logger.error(f"错误: 音频文件路径 '{audio_path}' 无效或文件不存在。")
            return []

        logger.info(f"正在加载音频文件 '{audio_path}' 进行分块处理...")
        try:
            audio = AudioSegment.from_wav(audio_path)  # 假设已预处理为 WAV
            audio = audio.set_frame_rate(16000).set_channels(1)  # 确保格式
        except Exception as e:
            logger.info(f"加载或处理音频文件 '{audio_path}' 时发生错误 (pydub): {e}")
            return []

        audio_duration_ms = len(audio)
        logger.info(f"音频总时长: {audio_duration_ms / 1000:.2f} 秒")
        all_results = []

        for i in range(0, audio_duration_ms, chunk_length_ms):
            start_time_ms = i
            end_time_ms = min(i + chunk_length_ms, audio_duration_ms)
            chunk = audio[start_time_ms:end_time_ms]

            temp_chunk_file_path = ""  # 在 try 块外部定义
            try:
                with tempfile.NamedTemporaryFile(
                    suffix=".wav", delete=False
                ) as temp_chunk_file:
                    temp_chunk_file_path = temp_chunk_file.name
                chunk.export(temp_chunk_file_path, format="wav")
                logger.info(
                    f"处理音频块: {start_time_ms / 1000:.2f}s - {end_time_ms / 1000:.2f}s"
                )

                chunk_output_list = self.model.transcribe(
                    [temp_chunk_file_path], batch_size=1, timestamps=True, return_hypotheses=True
                )
        
                chunk_global_start_offset_sec = start_time_ms / 1000.0

                new_segments = self.processor_strategy.process(
                    chunk_output_list, chunk_global_start_offset_sec
                )
                
                if new_segments:
                    all_results.extend(new_segments)

            except Exception as e:
                logger.info(f"转录音频块 '{temp_chunk_file_path}' 时发生错误: {e}")
                import traceback

                traceback.print_exc()
            finally:
                if temp_chunk_file_path and os.path.exists(temp_chunk_file_path):
                    try:
                        os.remove(temp_chunk_file_path)
                    except OSError as e_os:
                        logger.error(
                            f"删除临时音频文件 '{temp_chunk_file_path}' 时发生OS错误: {e_os}"
                        )

        all_results.sort(key=lambda x: x["start"])
        return all_results
