@echo off
echo 开始环境配置和依赖安装...

REM 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
echo 错误：未找到 Python。请先安装 Python 3.12.2 或更高版本 并将其添加到 PATH。
echo 您可以从 https://www.python.org/downloads/ 下载。
pause
exit /b
)
echo Python 已检测到。


REM 检查虚拟环境是否存在
if not exist .\.venv\Scripts\activate.bat (
	REM 创建虚拟环境
	echo 正在创建虚拟环境 .venv...
	python -m venv .venv
	if %errorlevel% neq 0 (
	echo 错误：创建虚拟环境失败。
	pause
	exit /b
	)
	echo 虚拟环境 .venv 创建成功。
)

REM 激活虚拟环境
call .\.venv\Scripts\activate.bat
echo 虚拟环境已激活。

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
echo 脚本可以尝试安装一个通用的 PyTorch (通常是CPU版)，或者跳过。
echo ===============================================================================
echo.

REM --- [新增] 选择软件包下载源 ---
echo ===============================================================================
echo 请选择软件包的下载源：
echo (如果您在中国大陆，选择国内镜像可以大幅提升下载速度)
echo ===============================================================================
echo 1. 国内镜像 (清华大学)
echo 2. 国内镜像 (阿里云)
echo 3. 官方默认源 (海外用户)
echo ===============================================================================
set /p source_choice="请输入您的选项 (1, 2 或 3，默认为 3): "

set "PIP_ARGS="
if "%source_choice%"=="1" (
    set "PIP_ARGS=-i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn"
    echo 已选择使用【清华大学】镜像源。
) else if "%source_choice%"=="2" (
    set "PIP_ARGS=-i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com"
    echo 已选择使用【阿里云】镜像源。
) else (
    echo 已选择或默认使用【官方默认源】。
)
echo.
REM --- [新增] 结束 ---


set /p choice="是否安装torch (cpu版本) 及其依赖？(y/n): "
if /i "%choice%"=="y" (
	echo 正在安装torch及其依赖...
	
	REM 使用上面选择的 PIP_ARGS 变量
	pip install %PIP_ARGS% -r requirements.txt

	if %errorlevel% neq 0 (
		echo 错误：安装依赖失败。
		pause
		exit /b
	)
	echo 依赖安装成功。
) else (
		pause
		exit /b
)
 

echo requirements依赖安装完成。

echo.
echo ===============================================================================
echo 重要提示：FFmpeg 安装 (必需)
echo ===============================================================================
echo 本项目运行需要 FFmpeg。
echo 请确保您已从 https://ffmpeg.org/download.html (推荐 gyan.dev 构建)
echo 下载 FFmpeg，并将其中的 'bin' 目录路径添加到系统的 PATH 环境变量中。
echo.
echo 如何检查FFmpeg是否配置成功：
echo   打开一个新的命令行窗口，输入 'ffmpeg -version'，如果显示版本信息则表示成功。
echo ===============================================================================
echo.
echo 所有依赖项的安装流程已执行完毕。
echo.
echo 下一步：
echo   1. 如果您尚未配置 FFmpeg，请立即配置。
echo   2. 配置完成后，您可以双击运行 'launcher.bat' 来启动应用程序。
echo.
pause
exit /bs