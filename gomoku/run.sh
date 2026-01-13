#!/bin/bash

echo "正在启动五子棋游戏..."

# 检查bin目录是否存在
if [ ! -d "bin" ]; then
    echo "错误：未找到编译文件，请先运行 ./compile.sh"
    exit 1
fi

# 运行游戏
java -cp bin com.gomoku.Main

if [ $? -ne 0 ]; then
    echo "运行失败，请检查错误信息"
    exit 1
fi
