Here is the complete English translation of the `README.md`, tailored for your `README_en.md` file.

---

# Parakeet-TDT GUI - Intelligent Video/Audio Subtitle Generator

<p align="center">
  <a href="./README.md">简体中文</a>
  <a href="./README_ko.md">한국어</a>
  <a href="./README_ja.md">日本語</a>
</p>

This project is a modern GUI tool based on the **NVIDIA NeMo** framework, encapsulating the powerful **Parakeet-TDT** series ASR (Automatic Speech Recognition) models. It automatically recognizes speech in video or audio files and generates **SRT subtitle files** with precise timestamps.

Refactored with a modular design, this project supports a **multi-language interface**, **batch file processing**, and **multi-model switching**, aiming to provide users with the most convenient localized subtitle generation experience.

## ✨ Core Features

*   **Multi-language Interface**: Built-in Internationalization (I18n) support. Switch between **Chinese / English / Japanese / Korean** with one click.
*   **Multi-format Output**: Supports generating various subtitle and text formats:
    *   `SRT`: The most widely used standard movie subtitle format.
    *   `VTT`: Web video (HTML5) standard subtitle format.
    *   `ASS`: Advanced subtitle format supporting styles, effects, and positioning (optimized for HD resolution).
    *   `LRC`: Synchronized lyric format for music players.
    *   `TXT / JSON`: Plain text or structured data, convenient for post-processing, archiving, or API integration.
*   **Universal Media Processing**: Unified entry for all media types. Supports direct uploading of **MP4, MKV, AVI, MP3, WAV, FLAC**, and almost all common formats.
*   **Batch Transcription**: Supports uploading multiple files at once with automatic queue processing for high efficiency.
*   **Multi-Model Support**:
    *   `nvidia/parakeet-tdt-0.6b-v2`: Balanced performance, excellent for English.
    *   `nvidia/parakeet-tdt_ctc-110m`: Lightweight model with extremely fast inference speed.
    *   `nvidia/parakeet-tdt-0.6b-v3`: Stronger multilingual capabilities (supports 20+ European languages).
    *   `nvidia/parakeet-tdt_ctc-0.6b-ja`: "Japanese model, supports Japanese transcription."
*   **Flexible Deployment**:
    *   **Cloud Loading**: Download and load the latest models directly from NVIDIA NGC.
    *   **Local Loading**: Supports loading existing local `.nemo` model files to avoid repeated downloads.
*   **Smart Hardware Acceleration**: Automatically detects NVIDIA GPU (CUDA) and prioritizes GPU acceleration; automatically falls back to CPU if no GPU is found.
*   **Configuration Persistence**: Automatically saves your last used model, chunk settings, and language preferences.

## 🛠 Requirements

*   **Python**: 3.10 or higher (3.12 recommended).
*   **FFmpeg**: **Must be installed separately** and configured in the system environment variables (used for media format conversion and audio extraction).
*   **NVIDIA GPU**: (Highly Recommended) An NVIDIA graphics card with 4GB+ VRAM and CUDA drivers installed.

## 🚀 Installation Guide (Windows)

### Method 1: Using Batch Script (Recommended for Beginners)

1.  **Clone/Download** this project to your local machine.
2.  Double-click to run **`install_dependencies.bat`**.
    *   The script will automatically create a Python virtual environment.
    *   It will automatically install the required dependencies.
3.  Once installation is complete, double-click **`launcher.bat`** to start the program.

> **Note**: If you need GPU acceleration, it is recommended to refer to "Method 2" to manually install PyTorch to ensure the CUDA version matches your system.

### Method 2: Manual Command Line Installation (Recommended)

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/NINIYOYYO/NeMo-ASR-GUI.git
    cd NeMo-ASR-GUI.git
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    python -m venv .venv
    # Windows:
    .\.venv\Scripts\activate
    # Linux/Mac:
    source .venv/bin/activate
    ```

3.  **Install PyTorch (Crucial Step):**
    If you wish to use NVIDIA GPU acceleration (Highly Recommended), **you must install a PyTorch version compatible with your CUDA environment before installing other dependencies.**
    *   Press `Win+R`, type `cmd`, and press Enter.
    *   Type `nvidia-smi` and press Enter to check your **CUDA Version**.
    *   Visit the [PyTorch Get Started Page](https://pytorch.org/get-started/locally/).
    *   Select your OS, Package Manager (pip), and the Compute Platform matching your CUDA version (e.g., CUDA 11.8, CUDA 12.1).
    *   *Example command for CUDA 12.1:*
        ```bash
        pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
        ```
    *If you skip this step, `nemo_toolkit` might default to a CPU-only version of PyTorch.*

4.  **Install Project Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Install FFmpeg:**
    *   **Windows**: Download a pre-compiled FFmpeg build, unzip it, and add the `bin` folder path to your system's `Path` environment variable.
    *   Open a terminal and type `ffmpeg -version`. If version information is output, the installation is successful.

6.  **Run the Program:**
    ```bash
    python main.py
    ```

## 📖 Usage Tutorial

After the program starts, your browser will automatically open `http://127.0.0.1:7860`.

### 1. Initial Setup & Language
*   A language switching menu is available at the top of the interface. Select your preferred language (e.g., "English").
*   The program will remember your choice.

### 2. Load ASR Model
You must load a model before using the transcription features.

*   **Cloud Model (Recommended for first-time use)**:
    1.  Select a model from the "Cloud Model Name" dropdown (e.g., `nvidia/parakeet-tdt-0.6b-v2`).
    2.  Click the **"Load Cloud Model"** button.
    3.  *Note: First-time loading involves downloading a 1-2GB model file. Please wait patiently.*

*   **Local Model**:
    1.  If you already have a `.nemo` file, enter the absolute path in the "Local Model Path" input box.
    *Example: `C:\Users\models\parakeet-tdt-0.6b-v2.nemo`*
    2.  Click the **"Load Local Model"** button.

### 3. Generate Subtitles
1.  Switch to the **"Transcription"** tab.
2.  Click the upload area and select one or **multiple** video or audio files.
3.  (Optional) Adjust the **Chunk Length** slider.
    *   *Recommended: 60-180 seconds. Longer chunks provide better context but require more VRAM.*
4.  Click the **"Submit"** button.
5.  The right/bottom side will display the current file name and processing progress in real-time.
6.  Once completed, you can:
    *   Click the link to download the generated `.srt` file.
    *   Preview the subtitle content directly in the text box below.

## 📂 Project Structure

```text
.
├── main.py                  # Program entry point
├── application.py           # Core application assembly and service coordination
├── app_ui.py                # Gradio UI construction logic
├── config.json              # User configuration (Auto-generated)
├── controllers/             # [MVC] Controller Layer: Handles business logic
│   ├── model_controller.py
│   └── transcription_controller.py
├── core/                    # Core Functionality Layer
│   ├── asr_service.py       # NeMo model loading and inference
│   ├── audio_processor.py   # FFmpeg audio extraction and processing
│   └── srt_generator.py     # SRT format generation
├── interfaces/              # Abstract interface definitions
├── utils/                   # Utilities
│   ├── config_manager.py    # Configuration I/O
│   ├── logger.py            # Logging system
│   └── translator.py        # I18n translation management
└── locales/                 # Multi-language translation files (zh.json, en.json...)
```

## Screenshot
![Interface](./README.assets/1.png)

## ⚠️ FAQ

**Q: The interface freezes after clicking "Load Model"?**
A: When loading a cloud model for the first time, it downloads a large file in the background. Please check the terminal (command line) window for a detailed download progress bar.

**Q: Error `FileNotFoundError: [WinError 2] The system cannot find the file specified`?**
A: This usually means **FFmpeg** is not installed or its path is not added to the system environment variable `Path`.

**Q: The program says it's running on CPU, but I have a GPU?**
A: Please check if your PyTorch is the CUDA version. Enter `python` in the terminal, then type `import torch; print(torch.cuda.is_available())`. If it outputs `False`, please reinstall the GPU version of PyTorch.

**Q: Out of Memory (OOM)?**
A: 1. Try reducing the "Chunk Length" slider. 2. Try selecting a model with fewer parameters (e.g., `ctc-110m`).

## 🤝 Contribution

Issues and Pull Requests are welcome to improve this project!
