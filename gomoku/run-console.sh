#!/bin/bash

echo "启动控制台五子棋游戏..."

# 设置UTF-8编码
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

# 检查bin目录是否存在
if [ ! -d "bin" ]; then
    echo "错误：未找到编译文件，请先运行 ./compile.sh"
    exit 1
fi

# 运行控制台版本游戏
java -Dfile.encoding=UTF-8 -cp bin com.gomoku.MainConsole

if [ $? -ne 0 ]; then
    echo "运行失败，请检查错误信息"
    exit 1
fi
