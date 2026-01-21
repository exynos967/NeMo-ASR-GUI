
import os
import time
from pathlib import Path
from interfaces import IASRService
from interfaces import ITranscriptionController, IAudioService, ISubtitleGenerator
from utils.exceptions import TranscriptionError
from utils.logger import logger 


class TranscriptionController(ITranscriptionController):
    """
    一个专门处理转录相关 UI 事件的控制器。
    """

    def __init__(self, app_services: IASRService, audio_service: IAudioService, subtitle_generator: ISubtitleGenerator) -> None:
       
        self.app_services = app_services
        self.audio_service = audio_service
        self.subtitle_generator = subtitle_generator
        
        self.subtitles_folder_path = Path(__file__).resolve().parent.parent / "subtitles"

    
    def process_media(self, media_file_objs: list, chunk_length_s: int, output_formats: list):
        """处理上传的视频/音频文件，生成 SRT 字幕文件。
        ARGS:
            media_file_objs: Gradio 上传的视频/音频文件对象列表。
            chunk_length_s: 音频分块长度（秒）。
            outpu_formats: 输出字幕格式列表 (e.g., ['srt', 'vtt'])
        YIELDS:
            状态消息 (str), 输出 SRT 文件路径列表 (list), SRT 内容预览 (str)。
        """

        if not self.app_services.is_model_loaded:
            yield "错误：ASR 模型未加载。请先加载模型。", None, ""
            return

        if media_file_objs is None:
            yield "请上传至少一个视频文件。", None, ""
            return
        
        if not output_formats:
            output_formats = ['srt']

        output_files_all = []
        total_files = len(media_file_objs)
        start_time_total = time.time()

        for i, media_file_obj in enumerate(media_file_objs):
            input_media_path = media_file_obj  # Gradio Video 对象具有 .name 属性表示路径
            file_name = os.path.basename(input_media_path)

            logger.info(f"开始处理视频/音频文件， 当前: {i+1}/{total_files}, 文件名: {file_name}")
            yield f"状态：正在处理文件, 当前：{i+1}/{total_files}, 文件名：{file_name} ...", None, ""

            extracted_audio_path = None
            output_path_for_download = None  # 用于 Gradio File 组件

            try:
                yield f"状态：正在提取 {file_name} 的音频...", None, ""
                extracted_audio_path = self.audio_service.extract_audio_from_video(input_media_path)
                if not extracted_audio_path:
                    yield "错误：音频提取失败。请检查视频文件或ffmpeg安装。", None, ""
                    return

                chunk_length_ms = chunk_length_s * 1000
                yield f"状态：正在转录音频 (分块大小: {chunk_length_s}秒)...", None, ""
                segment_timestamps = self.app_services.transcribe_audio_in_chunks(
                    extracted_audio_path, chunk_length_ms
                )

                if not segment_timestamps:
                    yield f"警告：转录文件 {file_name} 未生成有效的时间戳。正在跳过此文件。", None, ""
                    continue


                base_name = os.path.basename(input_media_path).rsplit(".", 1)[0]

                yield f"状态：正在生成字幕文件 ({', '.join(output_formats)})...", None, ""

                generated_content_preview = "" # 用于在UI预览，默认只预览第一个格式

                if not os.path.exists(self.subtitles_folder_path):
                    os.makedirs(self.subtitles_folder_path, exist_ok=True)
                for fmt in output_formats:
                    try:
                        content = self.subtitle_generator.generate_content(segment_timestamps, fmt)
                        output_path_for_download = os.path.join(self.subtitles_folder_path,  f"{base_name}.{fmt}")
                        with open(output_path_for_download, "w", encoding="utf-8") as subtitle_file:
                            subtitle_file.write(content)
                        output_files_all.append(output_path_for_download)

                        # 仅预览 SRT 或第一个格式
                        if fmt == "srt" or generated_content_preview == "":
                            generated_content_preview = content
                    except Exception as e:
                        logger.error(f"生成 {fmt} 格式失败: {e}")
                    logger.info(f"字幕文件位于: {output_path_for_download}")

            except Exception as e:
                logger.error(f"处理文件 {file_name} 时发生未知错误: {e}")
                import traceback
                traceback.print_exc()
                yield f"错误：处理文件 {file_name} 时发生未知错误: {e}。正在跳过此文件。", None, ""
                continue
            finally:
                if extracted_audio_path and os.path.exists(extracted_audio_path):
                    try:
                        os.remove(extracted_audio_path)
                    except OSError as e_clean:
                        logger.warning(f"无法删除临时音频文件 {extracted_audio_path}: {e_clean}")
   
            elapsed_time_total = time.time() - start_time_total
            status_message = f"处理完成。总耗时 {elapsed_time_total:.2f} 秒。生成{len(output_files_all)} 个字幕文件。"
            logger.info(status_message)
            yield status_message, output_files_all, generated_content_preview
    



    