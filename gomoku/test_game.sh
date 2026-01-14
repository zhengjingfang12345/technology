#!/bin/bash

# 测试控制台五子棋游戏
echo "测试控制台五子棋游戏..."
echo ""

# 模拟游戏输入
echo "7 7
7 8
8 7
8 8
9 7
9 8
10 7
10 8
11 7
q" | java -cp bin com.gomoku.MainConsole
