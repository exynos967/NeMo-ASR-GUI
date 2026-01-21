# Parakeet-TDT GUI - 智能视频/音频字幕生成工具

<p align="center">
  <a href="./README_en.md">English</a>
  <a href="./README_ko.md">한국어</a> 
  <a href="./README_ja.md">日本語</a>

</p>

本项目是一个基于 **NVIDIA NeMo** 框架的现代化 GUI 工具，封装了强大的 **Parakeet-TDT** 系列 ASR (自动语音识别) 模型。它能够自动识别视频或音频文件中的语音，并生成带精确时间戳的 **SRT 字幕文件**。

本项目采用模块化设计，支持**多语言界面**、**批量文件处理**以及**多种模型切换**，旨在为用户提供最便捷的本地化字幕生成体验。

## ✨ 核心功能

*   **多语言界面**: 内置国际化支持，支持一键切换 **中文 / English / 日本語 / 한국어** 界面。
*   **多格式输出**: 支持生成多种字幕/文本格式：
    *   `SRT`: 标准电影字幕格式。
    *   `VTT`: 网页视频标准格式。
    *   `ASS`: 支持高级样式和定位的字幕格式（已优化高清分辨率适配）。
    *   `LRC`: 歌词同步格式。
    *   `TXT / JSON`: 方便后续数据处理和存档。
*   **全能媒体处理**: 不再区分视频或音频入口，支持直接上传 **MP4, MKV, AVI, MP3, WAV, FLAC** 等几乎所有常见格式。
*   **批量转录**: 支持一次性上传多个文件，排队自动处理，高效便捷。
*   **多模型支持**:
    *   `nvidia/parakeet-tdt-0.6b-v2`: 综合能力强，支持英语。
    *   `nvidia/parakeet-tdt_ctc-110m`: 轻量级模型，推理速度极快。
    *   `nvidia/parakeet-tdt-0.6b-v3`: 更强的多语言支持（支持欧语系等20+种语言）。
    *   ` "nvidia/parakeet-tdt_ctc-0.6b-ja`: "日语模型，支持日语转录"
*   **灵活部署**: 
    *   **云端加载**: 一键从 NVIDIA NGC 下载并加载最新模型。
    *   **本地加载**: 支持加载本地已有的 `.nemo` 模型文件，无需重复下载。
*   **智能硬件加速**: 自动检测 NVIDIA GPU (CUDA)，优先使用 GPU 加速；若无 GPU 则自动回退至 CPU 运行。
*   **配置记忆**: 自动保存您上次使用的模型、分块设置和语言偏好。

## 🛠 环境要求

*   **Python**: 3.10 或更高版本 (推荐 3.12)。
*   **FFmpeg**: **必须单独安装**并配置到系统环境变量中（用于媒体格式转换和音频提取）。
*   **NVIDIA GPU**: (强烈推荐) 拥有 4GB 以上显存的 NVIDIA 显卡，并安装好 CUDA 驱动。

## 🚀 安装指南 (Windows)

### 方法一：使用批处理脚本 (小白推荐)

1.  **克隆/下载本项目**到本地。
2.  双击运行 **`install_dependencies.bat`**。
    *   脚本会自动创建 Python 虚拟环境。
    *   自动安装所需的依赖库。
3.  安装完成后，双击 **`launcher.bat`** 即可启动程序。

> **注意**: 如果你需要 GPU 加速，建议参考“方法二”手动安装 PyTorch，以确保 CUDA 版本匹配。

### 方法二：手动命令行安装 (推荐)

1.  **克隆仓库:**
    ```bash
    git clone https://github.com/NINIYOYYO/NeMo-ASR-GUI.git
    cd NeMo-ASR-GUI.git
    ```

2.  **创建并激活虚拟环境:**
    ```bash
    python -m venv .venv
    # Windows:
    .\.venv\Scripts\activate
    # Linux/Mac:
    source .venv/bin/activate
    ```



3.  **安装 PyTorch (重要：GPU 用户请特别注意!):**
    如果你希望使用 NVIDIA GPU 进行加速处理 (强烈推荐)，**请务必在安装其他依赖项之前，先手动安装一个与你的 CUDA 环境兼容的 PyTorch 版本。**
    *   输入Win+R键打开windows系统的运行窗口输入CMD进入终端输入
    ```bash
    nvidia-smi
    ```
    并且回车来检查你的 CUDA Version:
    *   访问 [PyTorch 官网安装指引页面](https://pytorch.org/get-started/locally/)。
    *   根据你的操作系统、包管理器 (推荐 `pip`)、计算平台 (例如 CUDA 11.8, CUDA 12.1) 和 Python 版本选择正确的安装命令。
    *   例如，如果使用 `pip` 且你的系统有 CUDA 12.1 环境，可以运行：
        ```bash
        pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
        ```
    如果跳过此步骤，或者你的系统没有 NVIDIA GPU，后续安装的 `nemo_toolkit` 可能会默认安装仅支持 CPU 的 PyTorch 版本。

4.  **安装项目其他依赖:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **安装 FFmpeg:**
    *   **Windows**: 下载 FFmpeg 预编译包，解压并将 `bin` 文件夹路径添加到系统的 `Path` 环境变量中。
    *   打开终端输入 `ffmpeg -version`，如果有输出则说明安装成功。

6.  **启动程序:**
    ```bash
    python main.py
    ```

## 📖 使用教程

程序启动后，浏览器会自动打开 `http://127.0.0.1:7860`。

### 1. 初始设置与语言
*   界面顶部提供了语言切换菜单，选择你熟悉的语言（如“中文”）。
*   程序会自动记住你的选择。

### 2. 加载 ASR 模型
在使用转录功能前，必须先加载模型。

*   **云端模型 (推荐首次使用)**:
    1.  在“云端模型名称”下拉框中选择模型（例如 `nvidia/parakeet-tdt-0.6b-v2`）。
    2.  点击 **“加载云端模型”** 按钮。
    3.  *注意：首次加载需要下载约 1-2GB 的模型文件，请耐心等待。*

*   **本地模型**:
    1.  如果你已有 `.nemo` 文件，在“本地模型路径”输入框中填入文件的绝对路径。
    *例如 C:\Users\models--nvidia--parakeet-tdt-0.6b-v2\snapshots\30c5e6f557f6ba26e5819a9ed2e86f670186b43f\parakeet-tdt-0.6b-v2.nemo*
    2.  点击 **“加载本地模型”** 按钮。

### 3. 生成字幕
1.  切换到 **“字幕生成 (Transcription)”** 标签页。
2.  点击文件上传区域，选择一个或多个 **视频** 或 **音频** 文件。
3.  (可选) 调整 **音频分块长度** 滑块。
    *   *建议值：60-180秒。分块越长，上下文越连贯，但对显存要求越高。*
4.  点击 **“开始生成 / Submit”** 按钮。
5.  右侧/下方会实时显示当前处理的文件名和进度。
6.  处理完成后，你可以：
    *   点击链接下载生成的 `.srt` 文件。
    *   在下方文本框直接预览字幕内容。

## 📂 项目结构说明

```text
.
├── main.py                  # 程序入口
├── application.py           # 应用核心组装与服务协调
├── app_ui.py                # Gradio 界面构建逻辑
├── config.json              # 用户配置文件 (自动生成)
├── controllers/             # [MVC] 控制器层：处理业务逻辑
│   ├── model_controller.py
│   └── transcription_controller.py
├── core/                    # 核心功能层
│   ├── asr_service.py       # NeMo 模型加载与推理
│   ├── audio_processor.py   # FFmpeg 音频提取与处理
│   └── srt_generator.py     # SRT 格式生成
├── interfaces/              # 抽象接口定义
├── utils/                   # 工具库
│   ├── config_manager.py    # 配置读写
│   ├── logger.py            # 日志系统
│   └── translator.py        # 国际化翻译管理
└── locales/                 # 多语言翻译文件 (zh.json, en.json...)
```
## 界面展示
![界面展示](./README.assets/1.png)

## ⚠️ 常见问题 (FAQ)

**Q: 点击“加载模型”后界面卡住不动了？**
A: 首次加载云端模型时正在后台下载大文件。请查看终端（命令行）窗口，那里会有详细的下载进度条。

**Q: 报错 `FileNotFoundError: [WinError 2] 系统找不到指定的文件`？**
A: 这通常是因为没有安装 **FFmpeg** 或者安装后没有将其加入到系统环境变量 PATH 中。

**Q: 程序提示在 CPU 上运行，但我有显卡？**
A: 请检查你的 PyTorch 是否安装了 CUDA 版本。在终端输入 `python` 进入交互模式，输入 `import torch; print(torch.cuda.is_available())`，如果输出 `False`，请重新安装 GPU 版 PyTorch。

**Q: 显存不足 (OOM) 怎么办？**
A: 1. 尝试减小“音频分块长度”。 2. 尝试选择参数量更小的模型（如 `ctc-110m`）。

## 🤝 贡献

欢迎提交 Issue 或 Pull Request 来改进本项目！
