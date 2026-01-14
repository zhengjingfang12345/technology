@echo off
chcp 65001 > nul
echo 正在编译五子棋游戏...

:: 创建bin目录
if not exist bin mkdir bin

:: 编译所有Java文件
javac -d bin -encoding UTF-8 src\com\gomoku\*.java

if %errorlevel% equ 0 (
    echo 编译成功！
    echo 运行 run.bat 来启动游戏
) else (
    echo 编译失败，请检查错误信息
    pause
    exit /b 1
)
pause
