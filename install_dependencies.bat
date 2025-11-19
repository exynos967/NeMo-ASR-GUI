@echo off
REM 切换代码页到 UTF-8 以支持多语言显示
chcp 65001 >nul

setlocal enabledelayedexpansion

:LANGUAGE_SELECT
cls
echo ========================================================
echo Please select your language / 请选择语言 / 言語を選択 / 언어 선택
echo ========================================================
echo 1. 简体中文 (Chinese)
echo 2. English
echo 3. 日本語 (Japanese)
echo 4. 한국어 (Korean)
echo ========================================================
set /p lang_choice="Input [1-4]: "

if "%lang_choice%"=="1" goto LANG_CN
if "%lang_choice%"=="2" goto LANG_EN
if "%lang_choice%"=="3" goto LANG_JA
if "%lang_choice%"=="4" goto LANG_KO
goto LANGUAGE_SELECT

REM ========================================================
REM 定义语言变量 (Define Language Variables)
REM ========================================================

:LANG_CN
set "MSG_START=开始环境配置和依赖安装..."
set "MSG_NO_PYTHON=错误：未找到 Python。请先安装 Python 3.12.2 或更高版本并添加到 PATH。"
set "MSG_DL_LINK=下载地址: https://www.python.org/downloads/"
set "MSG_PY_FOUND=Python 已检测到。"
set "MSG_CREATE_VENV=正在创建虚拟环境 .venv..."
set "MSG_VENV_FAIL=错误：创建虚拟环境失败。"
set "MSG_VENV_SUCCESS=虚拟环境 .venv 创建成功。"
set "MSG_VENV_ACT=虚拟环境已激活。"
set "MSG_MIRROR_TITLE=请选择软件包下载源 (中国大陆建议选 1 或 2):"
set "MSG_MIRROR_1=1. 国内镜像 (清华大学 - Tsinghua)"
set "MSG_MIRROR_2=2. 国内镜像 (阿里云 - Aliyun)"
set "MSG_MIRROR_3=3. 官方默认源 (Official/Global)"
set "MSG_MIRROR_SEL_MSG=已选择镜像源："
set "MSG_INSTALL_ASK=是否安装依赖 (requirements.txt)? (y/n): "
set "MSG_INSTALLING=正在安装依赖..."
set "MSG_INSTALL_FAIL=错误：安装依赖失败。"
set "MSG_INSTALL_DONE=依赖安装成功。"
set "MSG_FFMPEG_TITLE=重要提示：FFmpeg 安装 (必需)"
set "MSG_FFMPEG_BODY1=本项目需要 FFmpeg。"
set "MSG_FFMPEG_BODY2=请确保下载 FFmpeg 并将 'bin' 目录添加到系统 PATH。"
set "MSG_FFMPEG_CHECK=检查方法：新建终端输入 'ffmpeg -version'"
set "MSG_ALL_DONE=所有流程已完成。"
set "MSG_NEXT_STEP=下一步：双击 'launcher.bat' 启动。"
goto MAIN_LOGIC

:LANG_EN
set "MSG_START=Starting environment setup and installation..."
set "MSG_NO_PYTHON=Error: Python not found. Please install Python 3.12.2+ and add to PATH."
set "MSG_DL_LINK=Download: https://www.python.org/downloads/"
set "MSG_PY_FOUND=Python detected."
set "MSG_CREATE_VENV=Creating virtual environment .venv..."
set "MSG_VENV_FAIL=Error: Failed to create virtual environment."
set "MSG_VENV_SUCCESS=Virtual environment .venv created."
set "MSG_VENV_ACT=Virtual environment activated."
set "MSG_MIRROR_TITLE=Select PIP Mirror Source:"
set "MSG_MIRROR_1=1. China Mirror (Tsinghua)"
set "MSG_MIRROR_2=2. China Mirror (Aliyun)"
set "MSG_MIRROR_3=3. Official Source (Global)"
set "MSG_MIRROR_SEL_MSG=Selected Source:"
set "MSG_INSTALL_ASK=Install dependencies (requirements.txt)? (y/n): "
set "MSG_INSTALLING=Installing dependencies..."
set "MSG_INSTALL_FAIL=Error: Failed to install dependencies."
set "MSG_INSTALL_DONE=Dependencies installed successfully."
set "MSG_FFMPEG_TITLE=IMPORTANT: FFmpeg Installation (Required)"
set "MSG_FFMPEG_BODY1=This project requires FFmpeg."
set "MSG_FFMPEG_BODY2=Please download FFmpeg and add the 'bin' folder to your system PATH."
set "MSG_FFMPEG_CHECK=To check: Open new cmd and type 'ffmpeg -version'"
set "MSG_ALL_DONE=Setup completed."
set "MSG_NEXT_STEP=Next: Double-click 'launcher.bat' to start."
goto MAIN_LOGIC

:LANG_JA
set "MSG_START=環境設定と依存関係のインストールを開始します..."
set "MSG_NO_PYTHON=エラー：Pythonが見つかりません。Python 3.12.2以上をインストールしてください。"
set "MSG_DL_LINK=ダウンロード: https://www.python.org/downloads/"
set "MSG_PY_FOUND=Pythonが検出されました。"
set "MSG_CREATE_VENV=仮想環境 .venv を作成中..."
set "MSG_VENV_FAIL=エラー：仮想環境の作成に失敗しました。"
set "MSG_VENV_SUCCESS=仮想環境 .venv の作成に成功しました。"
set "MSG_VENV_ACT=仮想環境がアクティブ化されました。"
set "MSG_MIRROR_TITLE=PIPミラーソースを選択してください:"
set "MSG_MIRROR_1=1. 中国ミラー (清華大学)"
set "MSG_MIRROR_2=2. 中国ミラー (Aliyun)"
set "MSG_MIRROR_3=3. 公式ソース (Global)"
set "MSG_MIRROR_SEL_MSG=選択されたソース："
set "MSG_INSTALL_ASK=依存関係をインストールしますか？ (y/n): "
set "MSG_INSTALLING=インストール中..."
set "MSG_INSTALL_FAIL=エラー：インストールに失敗しました。"
set "MSG_INSTALL_DONE=インストールが完了しました。"
set "MSG_FFMPEG_TITLE=重要：FFmpegのインストール（必須）"
set "MSG_FFMPEG_BODY1=このプロジェクトにはFFmpegが必要です。"
set "MSG_FFMPEG_BODY2=FFmpegをダウンロードし、'bin'フォルダをシステムPATHに追加してください。"
set "MSG_FFMPEG_CHECK=確認：新しいCMDを開き 'ffmpeg -version' と入力"
set "MSG_ALL_DONE=すべての処理が完了しました。"
set "MSG_NEXT_STEP=次へ：'launcher.bat' をダブルクリックして起動します。"
goto MAIN_LOGIC

:LANG_KO
set "MSG_START=환경 설정 및 의존성 설치를 시작합니다..."
set "MSG_NO_PYTHON=오류: Python을 찾을 수 없습니다. Python 3.12.2 이상을 설치하고 PATH에 추가하십시오."
set "MSG_DL_LINK=다운로드: https://www.python.org/downloads/"
set "MSG_PY_FOUND=Python이 감지되었습니다."
set "MSG_CREATE_VENV=가상 환경 .venv 생성 중..."
set "MSG_VENV_FAIL=오류: 가상 환경 생성 실패."
set "MSG_VENV_SUCCESS=가상 환경 .venv 생성 성공."
set "MSG_VENV_ACT=가상 환경이 활성화되었습니다."
set "MSG_MIRROR_TITLE=PIP 미러 소스를 선택하십시오:"
set "MSG_MIRROR_1=1. 중국 미러 (칭화대)"
set "MSG_MIRROR_2=2. 중국 미러 (알리윤)"
set "MSG_MIRROR_3=3. 공식 소스 (글로벌)"
set "MSG_MIRROR_SEL_MSG=선택된 소스:"
set "MSG_INSTALL_ASK=의존성을 설치하시겠습니까? (y/n): "
set "MSG_INSTALLING=설치 중..."
set "MSG_INSTALL_FAIL=오류: 설치 실패."
set "MSG_INSTALL_DONE=설치 완료."
set "MSG_FFMPEG_TITLE=중요: FFmpeg 설치 (필수)"
set "MSG_FFMPEG_BODY1=이 프로젝트에는 FFmpeg가 필요합니다."
set "MSG_FFMPEG_BODY2=FFmpeg를 다운로드하고 'bin' 폴더를 시스템 PATH에 추가하십시오."
set "MSG_FFMPEG_CHECK=확인: 새 CMD를 열고 'ffmpeg -version' 입력"
set "MSG_ALL_DONE=설정이 완료되었습니다."
set "MSG_NEXT_STEP=다음: 'launcher.bat'를 더블 클릭하여 시작하십시오."
goto MAIN_LOGIC


REM ========================================================
REM 主逻辑 (Main Logic)
REM ========================================================

:MAIN_LOGIC
echo.
echo %MSG_START%

REM 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %MSG_NO_PYTHON%
    echo %MSG_DL_LINK%
    pause
    exit /b
)
echo %MSG_PY_FOUND%

REM 检查/创建虚拟环境
if not exist .\.venv\Scripts\activate.bat (
    echo %MSG_CREATE_VENV%
    python -m venv .venv
    if !errorlevel! neq 0 (
        echo %MSG_VENV_FAIL%
        pause
        exit /b
    )
    echo %MSG_VENV_SUCCESS%
)

REM 激活虚拟环境
call .\.venv\Scripts\activate.bat
echo %MSG_VENV_ACT%

REM 显示 PyTorch 信息 (使用子程序处理长文本)
call :SHOW_TORCH_INFO_%lang_choice%

REM 选择 PIP 源
echo.
echo ===============================================================================
echo %MSG_MIRROR_TITLE%
echo ===============================================================================
echo %MSG_MIRROR_1%
echo %MSG_MIRROR_2%
echo %MSG_MIRROR_3%
echo ===============================================================================
set /p source_choice="Select (1, 2, 3) [Default 3]: "

set "PIP_ARGS="
if "%source_choice%"=="1" (
    set "PIP_ARGS=-i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn"
    echo %MSG_MIRROR_SEL_MSG% Tsinghua
) else if "%source_choice%"=="2" (
    set "PIP_ARGS=-i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com"
    echo %MSG_MIRROR_SEL_MSG% Aliyun
) else (
    echo %MSG_MIRROR_SEL_MSG% Official
)
echo.

REM 安装依赖
set /p choice="%MSG_INSTALL_ASK%"
if /i "%choice%"=="y" (
    echo %MSG_INSTALLING%
    pip install %PIP_ARGS% -r requirements.txt
    if !errorlevel! neq 0 (
        echo %MSG_INSTALL_FAIL%
        pause
        exit /b
    )
    echo %MSG_INSTALL_DONE%
) else (
    REM 用户选择不安装依赖，直接退出或继续
    REM 此处逻辑是如果不安装就退出，保持原样
    pause
    exit /b
)

echo.
echo ===============================================================================
echo %MSG_FFMPEG_TITLE%
echo ===============================================================================
echo %MSG_FFMPEG_BODY1%
echo %MSG_FFMPEG_BODY2%
echo %MSG_FFMPEG_CHECK%
echo ===============================================================================
echo.
echo %MSG_ALL_DONE%
echo %MSG_NEXT_STEP%
echo.
pause
exit /b

REM ========================================================
REM PyTorch 信息显示子程序 (Subroutines for Long Text)
REM ========================================================

:SHOW_TORCH_INFO_1
echo.
echo ===============================================================================
echo 关于 PyTorch 安装 (重要！)：
echo ===============================================================================
echo 如果您有 NVIDIA GPU 并希望使用 CUDA 加速，强烈建议您：
echo   1. 访问 PyTorch 官网 (https://pytorch.org/get-started/locally/)
echo   2. 获取适合您 CUDA 版本的 PyTorch 安装命令。
echo   3. 在【新的命令行窗口中先激活此虚拟环境(.venv\Scripts\activate)】，
echo      然后【手动执行】该 PyTorch 安装命令。
echo   4. 手动安装 PyTorch GPU 版本【之后】，再回到【此窗口】按 'n' 跳过自动安装。
echo.
echo 如果您不确定、只想使用 CPU，或者已手动安装 GPU 版 PyTorch，
echo 脚本可以尝试安装一个通用的 PyTorch (通常是CPU版)，或者直接安装 requirements.txt。
echo ===============================================================================
goto :EOF

:SHOW_TORCH_INFO_2
echo.
echo ===============================================================================
echo About PyTorch Installation (IMPORTANT!):
echo ===============================================================================
echo If you have an NVIDIA GPU and want CUDA acceleration, it is recommended to:
echo   1. Visit https://pytorch.org/get-started/locally/
echo   2. Get the install command matching your CUDA version.
echo   3. Open a NEW terminal, Activate the venv (.venv\Scripts\activate),
echo      and MANUALLY RUN the PyTorch install command.
echo   4. AFTER manually installing the GPU version, come back here and
echo      install other dependencies.
echo.
echo If you only need CPU mode, you can proceed with the automatic install below.
echo ===============================================================================
goto :EOF

:SHOW_TORCH_INFO_3
echo.
echo ===============================================================================
echo PyTorchのインストールについて (重要！):
echo ===============================================================================
echo NVIDIA GPUを使用してCUDA高速化を行いたい場合、以下を強く推奨します：
echo   1. PyTorch公式サイト (https://pytorch.org/get-started/locally/) にアクセス。
echo   2. お使いのCUDAバージョンに合ったインストールコマンドを取得。
echo   3. 【新しいターミナルでこの仮想環境をアクティブ化 (.venv\Scripts\activate)】し、
echo      そのコマンドを【手動で実行】してください。
echo   4. 手動インストール【後】に、このウィンドウに戻ってください。
echo.
echo CPUのみを使用する場合、またはGPU版を既にインストール済みの場合は、
echo そのまま続行してください。
echo ===============================================================================
goto :EOF

:SHOW_TORCH_INFO_4
echo.
echo ===============================================================================
echo PyTorch 설치에 관하여 (중요!):
echo ===============================================================================
echo NVIDIA GPU를 사용하여 CUDA 가속을 원하시는 경우, 다음을 강력히 권장합니다:
echo   1. PyTorch 공식 웹사이트 (https://pytorch.org/get-started/locally/) 방문.
echo   2. 사용 중인 CUDA 버전에 맞는 설치 명령어를 확인.
echo   3. [새 터미널 창에서 가상 환경을 활성화(.venv\Scripts\activate)] 한 후,
echo      해당 명령어를 [수동으로 실행]하십시오.
echo   4. GPU 버전을 수동으로 설치한 [후], 다시 이 창으로 돌아오십시오.
echo.
echo CPU만 사용하거나 이미 GPU 버전을 설치한 경우 아래에서 계속 진행하십시오.
echo ===============================================================================
goto :EOF