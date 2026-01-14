#!/bin/bash

# 五子棋控制台版演示
# 演示一局完整的游戏

echo "=== 五子棋控制台版演示 ==="
echo ""
echo "模拟一局游戏，黑棋将获胜..."
echo ""

# 模拟游戏输入：黑棋在第7列形成五连
cat <<'EOF' | java -Dfile.encoding=UTF-8 -cp bin com.gomoku.MainConsole
7 7
7 8
8 7
8 8
9 7
9 8
10 7
10 8
11 7
n
EOF

echo ""
echo "=== 演示结束 ==="
