@echo off
chcp 65001 > nul
echo 正在启动五子棋游戏...

:: 检查bin目录是否存在
if not exist bin (
    echo 错误：未找到编译文件，请先运行 compile.bat
    pause
    exit /b 1
)

:: 运行游戏
java -cp bin com.gomoku.Main

if %errorlevel% neq 0 (
    echo 运行失败，请检查错误信息
    pause
    exit /b 1
)
