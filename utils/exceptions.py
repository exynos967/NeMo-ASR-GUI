

class BaseAppException(Exception):
    """应用程序所有自定义异常的基类。"""
    pass


class ModelLoadError(BaseAppException):
    """模型加载失败时引发的异常。"""
    pass


class AudioProcessingError(BaseAppException):
    """当音频提取或转换失败时引发。"""
    pass

class TranscriptionError(BaseAppException):
    """当转录过程失败时引发。"""
    pass

class SubtitleGenerationError(BaseAppException):
    """当SRT内容生成失败时引发。"""
    pass