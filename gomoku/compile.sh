#!/bin/bash

echo "正在编译五子棋游戏..."

# 创建bin目录
mkdir -p bin

# 编译所有Java文件
javac -d bin -encoding UTF-8 src/com/gomoku/*.java

if [ $? -eq 0 ]; then
    echo "编译成功！"
    echo "运行 ./run.sh 来启动游戏"
else
    echo "编译失败，请检查错误信息"
    exit 1
fi
