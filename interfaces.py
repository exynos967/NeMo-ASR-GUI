from abc import ABC, abstractmethod



class IASRService(ABC):
    """
    封装所有与 NeMo ASR 模型相关的操作。
    """
    @property
    @abstractmethod
    def is_model_loaded(self) -> bool:
        """检查 ASR 模型是否已加载。"""
        ...


    @abstractmethod
    def load_model_from_ngc(self, model_name: str) -> str:
        """从 NVIDIA NGC 加载预训练模型。"""
        ...

    @abstractmethod
    def load_model_from_local(self, model_path: str) -> str:
        """从本地 .nemo 文件加载模型。"""
        ...

    @abstractmethod
    def transcribe_audio_in_chunks(self, audio_path: str, chunk_length_ms: int) -> list:
        """
        将音频文件分块转录并返回带有全局时间戳的段列表。
        ARGS:
            audio_path: 音频文件路径 (假设为 WAV)。
            chunk_length_ms: 每块的长度（毫秒）。
        RETURNS:
            包含 {'start': float, 'end': float, 'segment': str} 的列表。

        """
        ...
    

    


class IConfigManager(ABC):
    """
    定义配置管理器的接口，封装配置的加载、保存和访问功能。
    """

    @abstractmethod
    def get_config_all(self) -> dict:
        """
        获取所有配置项。
        返回包含所有配置项的字典。
        """
        ...

    @abstractmethod
    def save_config(self, local_model_path: str, chunk_length: int, cloud_model_name: str = None):
        """将当前配置保存到 config.json。"""
        ...

    @abstractmethod
    def get_config_value(self, key: str):
        """获取配置中的特定值。"""
        ...
    
    
    
class ISubtitleGenerator(ABC):
    """
    字幕生成服务接口。
    支持多种格式转换逻辑
    """
    @abstractmethod
    def generate_content(self, segment_timestamps: list, format_type: str) -> str:
        """
        根据时间戳列表生成指定格式的字幕内容。
        ARGS:
            segment_timestamps: 包含 {'start': float, 'end': float, 'segment': str} 的列表。
            format_type: 格式类型 (e.g., 'srt', 'vtt', 'txt', 'json')
        RETURNS:
            SRT 格式的字符串。
        """
        ...


class IAudioService(ABC):
    """
    定义音频处理服务的接口，封装音频相关的核心服务。
    """

    @abstractmethod
    def extract_audio_from_video(self, input_media_path: str) -> str:
        """
        使用 ffmpeg 从视频文件中提取音频并转换为 WAV 格式。
        返回提取的音频文件路径，或在失败时返回 None。
        """
        ...
    

class IModelController(ABC):
    """
    一个专门处理模型相关 UI 事件的控制器

    """
    @abstractmethod
    def handle_load_local_click(self, path_from_input_box, chunk_val_from_slider, selected_cloud_model):
        """处理“加载本地模型”按钮点击事件。"""
        ...

    @abstractmethod
    def handle_load_cloud_click(self, chunk_val_from_slider, selected_cloud_model):
        """处理“加载云端模型”按钮点击事件。"""
        ...

class ITranscriptionController(ABC):
    """
    一个专门处理转录相关 UI 事件的控制器。
    """
    @abstractmethod
    def process_media(self, media_file_objs: list, chunk_length_s: int, output_formats: list):
        """处理上传的视频/音频文件，生成 SRT 字幕文件。
        ARGS:
            media_file_objs: Gradio 上传的视频/音频文件对象列表。
            chunk_length_s: 音频分块长度（秒）。
            outpu_formats: 输出字幕格式列表 (e.g., ['srt', 'vtt'])
        YIELDS:
            状态消息 (str), 输出 SRT 文件路径列表 (list), SRT 内容预览 (str)。
        """
    ...

    



class IApplication(ABC):
    """
    定义应用程序的接口，封装核心服务和配置管理器。
    """

    @property
    @abstractmethod
    def asr_service(self) -> IASRService:
        """获取 ASR 服务实例。"""
        ...

    @property
    @abstractmethod
    def config_manager(self) -> IConfigManager:
        """获取配置管理器实例。"""
        ...

    @property
    @abstractmethod
    def audio_service(self) -> IAudioService:
        """获取音频处理服务实例。"""
        ...

    @property
    @abstractmethod
    def subtitle_generator(self) -> ISubtitleGenerator:
        """获取字幕生成服务实例。"""
        ...
        
    @property
    @abstractmethod
    def model_controller(self) -> IModelController:
        """获取模型控制器实例。"""
        ...

    @property
    @abstractmethod
    def transcription_controller(self) -> ITranscriptionController:
        """获取转录控制器实例。"""
        ...