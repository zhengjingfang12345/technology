# 五子棋游戏（Gomoku Game）

这是一个使用Java和Swing实现的五子棋游戏，支持双人对战。

## 功能特点

- 15x15标准棋盘
- 图形化界面
- 支持黑白双方对战
- 自动检测胜负
- 支持重新开始游戏
- 平局检测

## 项目结构

```
gomoku/
├── src/
│   └── com/
│       └── gomoku/
│           ├── Board.java       # 棋盘类
│           ├── Player.java      # 玩家类
│           ├── Game.java        # 游戏逻辑类
│           ├── GomokuGUI.java   # 图形界面类
│           └── Main.java        # 主程序入口
├── README.md
├── compile.sh                   # Linux/Mac编译脚本
├── run.sh                       # Linux/Mac运行脚本
├── compile.bat                  # Windows编译脚本
└── run.bat                      # Windows运行脚本
```

## 编译和运行

### Linux/Mac系统

1. 编译：
```bash
cd gomoku
chmod +x compile.sh run.sh
./compile.sh
```

2. 运行：
```bash
./run.sh
```

或者手动编译和运行：
```bash
# 编译
javac -d bin -encoding UTF-8 src/com/gomoku/*.java

# 运行
java -cp bin com.gomoku.Main
```

### Windows系统

1. 编译：
```cmd
cd gomoku
compile.bat
```

2. 运行：
```cmd
run.bat
```

或者手动编译和运行：
```cmd
# 编译
javac -d bin -encoding UTF-8 src\com\gomoku\*.java

# 运行
java -cp bin com.gomoku.Main
```

## 游戏规则

1. 黑棋先行，白棋后手
2. 双方轮流在棋盘上落子
3. 最先在横、竖、斜任意方向形成连续五子的一方获胜
4. 棋盘下满且无人获胜则为平局

## 操作说明

- 鼠标点击棋盘交叉点落子
- 点击"重新开始"按钮开始新游戏
- 游戏结束时会弹出提示框显示结果

## 系统要求

- Java JDK 8或更高版本
- 支持图形界面的操作系统

## 类说明

### Board.java
管理棋盘状态，包括：
- 棋盘初始化和重置
- 落子有效性检查
- 胜负判断（检查横、竖、斜四个方向）

### Player.java
表示游戏玩家，存储玩家名称和棋子颜色。

### Game.java
管理游戏流程，包括：
- 玩家切换
- 落子处理
- 游戏状态判断

### GomokuGUI.java
图形用户界面，包括：
- 棋盘绘制
- 棋子绘制
- 鼠标事件处理
- 游戏状态显示

### Main.java
程序入口，启动图形界面。

## 作者

五子棋游戏 - Java实现

## 许可证

MIT License
