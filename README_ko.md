# Parakeet-TDT GUI - 지능형 동영상/오디오 자막 생성 도구

<p align="center">
  <a href="./README_en.md">English</a> | 
  <a href="./README.md">简体中文</a> |
  <a href="./README_ja.md">日本語</a>
</p>

이 프로젝트는 **NVIDIA NeMo** 프레임워크를 기반으로 하는 현대적인 GUI 도구로, 강력한 **Parakeet-TDT** 시리즈 ASR (자동 음성 인식) 모델을 탑재하고 있습니다. 동영상 또는 오디오 파일의 음성을 자동으로 인식하여 정밀한 타임스탬프가 포함된 **SRT 자막 파일**을 생성합니다.

모듈식 설계로 완전히 리팩토링되었으며, **다국어 인터페이스**, **일괄 파일 처리** 및 **다중 모델 전환**을 지원하여 사용자에게 가장 편리한 로컬 자막 생성 경험을 제공하는 것을 목표로 합니다.

## ✨ 핵심 기능

*   **다국어 인터페이스**: 국제화(I18n)를 지원하여 **중국어 / 영어 / 일본어 / 한국어** 인터페이스를 원클릭으로 전환할 수 있습니다.
*   **만능 미디어 처리**: 동영상과 오디오 업로드를 구분할 필요가 없습니다. **MP4, MKV, AVI, MP3, WAV, FLAC** 등 거의 모든 일반적인 형식의 직접 업로드를 지원합니다.
*   **일괄 전사 (Batch Transcription)**: 여러 파일을 한 번에 업로드하고 대기열에 넣어 자동으로 순차 처리할 수 있어 효율적입니다.
*   **다중 모델 지원**:
    *   `nvidia/parakeet-tdt-0.6b-v2`: 종합적인 성능이 우수하며 영어에 강합니다.
    *   `nvidia/parakeet-tdt_ctc-110m`: 경량 모델로 추론 속도가 매우 빠릅니다.
    *   `nvidia/parakeet-tdt-0.6b-v3`: 더 강력한 다국어 지원 (유럽어 등 20개 이상의 언어 지원).
*   **유연한 배포**: 
    *   **클라우드 로드**: NVIDIA NGC에서 최신 모델을 원클릭으로 다운로드하여 로드합니다.
    *   **로컬 로드**: 기존에 보유한 `.nemo` 모델 파일 로드를 지원하여 중복 다운로드를 방지합니다.
*   **스마트 하드웨어 가속**: NVIDIA GPU (CUDA)를 자동으로 감지하여 GPU 가속을 우선 사용하며, GPU가 없을 경우 자동으로 CPU 실행으로 전환됩니다.
*   **설정 기억**: 마지막으로 사용한 모델, 청크 설정 및 언어 기본 설정을 자동으로 저장합니다.

## 🛠 환경 요구 사항

*   **Python**: 3.10 이상 (3.12 권장).
*   **FFmpeg**: **반드시 별도로 설치**하고 시스템 환경 변수(PATH)에 구성해야 합니다 (미디어 형식 변환 및 오디오 추출에 사용).
*   **NVIDIA GPU**: (강력 권장) 4GB 이상의 VRAM을 탑재한 NVIDIA 그래픽 카드 및 CUDA 드라이버 설치 필요.

## 🚀 설치 가이드 (Windows)

### 방법 1: 배치 스크립트 사용 (초보자 추천)

1.  이 저장소를 로컬에 **복제(Clone)/다운로드**합니다.
2.  **`install_dependencies.bat`** 파일을 더블 클릭하여 실행합니다.
    *   스크립트가 자동으로 Python 가상 환경을 생성합니다.
    *   필요한 의존성 라이브러리를 자동으로 설치합니다.
3.  설치가 완료되면 **`launcher.bat`** 파일을 더블 클릭하여 프로그램을 시작합니다.

> **주의**: GPU 가속이 필요한 경우, "방법 2"를 참조하여 PyTorch를 수동으로 설치하고 CUDA 버전을 일치시키는 것을 권장합니다.

### 방법 2: 수동 명령줄 설치 (권장)

1.  **저장소 복제:**
    ```bash
    git clone https://github.com/NINIYOYYO/parakeet-tdt-0.6b-v2-SRT-GUI.git
    cd parakeet-tdt-0.6b-v2-SRT-GUI
    ```

2.  **가상 환경 생성 및 활성화:**
    ```bash
    python -m venv .venv
    # Windows:
    .\.venv\Scripts\activate
    # Linux/Mac:
    source .venv/bin/activate
    ```

3.  **PyTorch 설치 (중요 단계):**
    GPU 가속을 활성화하려면 **반드시** [PyTorch 공식 웹사이트](https://pytorch.org/get-started/locally/)에서 사용 중인 CUDA 버전에 해당하는 설치 명령어를 확인하십시오.
    *예시 (CUDA 12.1 환경):*
    ```bash
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    ```

4.  **기타 프로젝트 의존성 설치:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **FFmpeg 설치:**
    *   **Windows**: FFmpeg 사전 컴파일된 패키지를 다운로드하여 압축을 풀고, `bin` 폴더 경로를 시스템의 `Path` 환경 변수에 추가합니다.
    *   터미널을 열고 `ffmpeg -version`을 입력하여 출력이 나오면 설치가 성공한 것입니다.

6.  **프로그램 시작:**
    ```bash
    python main.py
    ```

## 📖 사용 튜토리얼

프로그램이 시작되면 브라우저가 자동으로 `http://127.0.0.1:7860`을 엽니다.

### 1. 초기 설정 및 언어
*   인터페이스 상단에 언어 전환 메뉴가 있습니다. 익숙한 언어(예: "한국어")를 선택하십시오.
*   프로그램은 선택 사항을 자동으로 기억합니다.

### 2. ASR 모델 로드
전사(Transcription) 기능을 사용하기 전에 먼저 모델을 로드해야 합니다.

*   **클라우드 모델 (최초 사용 시 권장)**:
    1.  "클라우드 모델 이름" 드롭다운에서 모델을 선택합니다 (예: `nvidia/parakeet-tdt-0.6b-v2`).
    2.  **"클라우드 모델 로드 (Load Cloud Model)"** 버튼을 클릭합니다.
    3.  *주의: 처음 로드할 때 약 1-2GB의 모델 파일을 다운로드하므로 잠시 기다려 주십시오.*

*   **로컬 모델**:
    1.  이미 `.nemo` 파일을 가지고 있는 경우, "로컬 모델 경로" 입력란에 파일의 절대 경로를 입력합니다.
    *예: C:\Users\models\parakeet-tdt-0.6b-v2.nemo*
    2.  **"로컬 모델 로드 (Load Local Model)"** 버튼을 클릭합니다.

### 3. 자막 생성
1.  **"자막 생성 (Transcription)"** 탭으로 전환합니다.
2.  파일 업로드 영역을 클릭하여 하나 또는 **여러 개**의 **동영상** 또는 **오디오** 파일을 선택합니다.
3.  (선택 사항) **오디오 분할 길이 (Chunk Length)** 슬라이더를 조정합니다.
    *   *권장 값: 60-180초. 청크가 길수록 문맥 연결이 자연스럽지만, 더 많은 VRAM을 요구합니다.*
4.  **"생성 시작 / Submit"** 버튼을 클릭합니다.
5.  오른쪽/하단에 현재 처리 중인 파일 이름과 진행 상황이 실시간으로 표시됩니다.
6.  처리가 완료되면 다음을 수행할 수 있습니다.
    *   링크를 클릭하여 생성된 `.srt` 파일을 다운로드합니다.
    *   아래 텍스트 상자에서 자막 내용을 직접 미리 봅니다.

## 📂 프로젝트 구조

```text
.
├── main.py                  # 프로그램 진입점
├── application.py           # 애플리케이션 핵심 조립 및 서비스 조정
├── app_ui.py                # Gradio UI 구축 로직
├── config.json              # 사용자 구성 파일 (자동 생성됨)
├── controllers/             # [MVC] 컨트롤러 계층: 비즈니스 로직 처리
│   ├── model_controller.py
│   └── transcription_controller.py
├── core/                    # 핵심 기능 계층
│   ├── asr_service.py       # NeMo 모델 로드 및 추론
│   ├── audio_processor.py   # FFmpeg 오디오 추출 및 처리
│   └── srt_generator.py     # SRT 형식 생성
├── interfaces/              # 추상 인터페이스 정의
├── utils/                   # 유틸리티
│   ├── config_manager.py    # 구성 읽기/쓰기
│   ├── logger.py            # 로그 시스템
│   └── translator.py        # 국제화 번역 관리
└── locales/                 # 다국어 번역 파일 (zh.json, ko.json...)
```

## 인터페이스 스크린샷 (Screenshot)
![Interface](./README.assets/1.png)

## ⚠️ 자주 묻는 질문 (FAQ)

**Q: "모델 로드"를 클릭한 후 화면이 멈췄습니다.**
A: 클라우드 모델을 처음 로드할 때 백그라운드에서 대용량 파일을 다운로드하고 있습니다. 터미널(명령줄) 창을 확인하면 자세한 다운로드 진행률 표시줄이 나타납니다.

**Q: `FileNotFoundError: [WinError 2] 지정된 파일을 찾을 수 없습니다` 오류가 발생합니다.**
A: 이는 일반적으로 **FFmpeg**가 설치되지 않았거나 설치 후 시스템 환경 변수 PATH에 추가되지 않았기 때문입니다.

**Q: GPU가 있는데 프로그램이 CPU에서 실행된다고 표시됩니다.**
A: PyTorch가 CUDA 버전으로 설치되었는지 확인하십시오. 터미널에 `python`을 입력하고 `import torch; print(torch.cuda.is_available())`을 실행하십시오. `False`가 출력되면 GPU 버전의 PyTorch를 다시 설치하십시오.

**Q: 비디오 메모리 부족 (OOM)이 발생합니다.**
A: 1. "오디오 분할 길이 (Chunk Length)"를 줄여보십시오. 2. 파라미터 수가 더 적은 모델(예: `ctc-110m`)을 선택해 보십시오.

## 🤝 기여

이 프로젝트를 개선하기 위한 Issue 또는 Pull Request 제출을 환영합니다!

---