package com.gomoku;

import java.util.Scanner;

public class ConsoleGomoku {
    private Game game;
    private Scanner scanner;

    public ConsoleGomoku() {
        game = new Game();
        scanner = new Scanner(System.in);
    }

    public void start() {
        System.out.println("=================================");
        System.out.println("    欢迎来到五子棋游戏！");
        System.out.println("=================================");
        System.out.println();

        printInstructions();

        while (true) {
            printBoard();
            System.out.println();

            if (game.isGameOver()) {
                if (game.isDraw()) {
                    System.out.println("游戏结束 - 平局！");
                } else {
                    System.out.println("🎉 游戏结束 - " + game.getWinner().getName() +
                                     " (" + game.getWinner().getStoneColor() + ") 获胜！");
                }
                System.out.println();
                System.out.print("是否再来一局？(y/n): ");
                String answer = scanner.nextLine().trim().toLowerCase();
                if (answer.equals("y") || answer.equals("yes")) {
                    game.reset();
                    System.out.println("\n开始新游戏！\n");
                    continue;
                } else {
                    System.out.println("感谢游玩！再见！");
                    break;
                }
            }

            System.out.println("当前玩家: " + game.getCurrentPlayer().getName() +
                             " (" + game.getCurrentPlayer().getStoneColor() + ")");
            System.out.print("请输入坐标 (格式: 行 列，如 '7 7')，或输入 'q' 退出: ");

            String input = scanner.nextLine().trim();

            if (input.equalsIgnoreCase("q") || input.equalsIgnoreCase("quit")) {
                System.out.println("感谢游玩！再见！");
                break;
            }

            if (input.equalsIgnoreCase("help") || input.equalsIgnoreCase("h")) {
                printInstructions();
                continue;
            }

            try {
                String[] parts = input.split("\\s+");
                if (parts.length != 2) {
                    System.out.println("❌ 输入格式错误！请输入两个数字，用空格分隔。");
                    continue;
                }

                int row = Integer.parseInt(parts[0]);
                int col = Integer.parseInt(parts[1]);

                if (game.makeMove(row, col)) {
                    System.out.println("✓ 落子成功！\n");
                } else {
                    System.out.println("❌ 无效的落子位置！请选择空白位置。");
                }
            } catch (NumberFormatException e) {
                System.out.println("❌ 输入格式错误！请输入数字。");
            }
        }

        scanner.close();
    }

    private void printBoard() {
        Board board = game.getBoard();
        int size = board.getSize();

        System.out.println("   " + generateColumnHeaders(size));
        System.out.println("   " + generateSeparatorLine(size));

        for (int i = 0; i < size; i++) {
            System.out.printf("%2d │", i);
            for (int j = 0; j < size; j++) {
                int stone = board.getStone(i, j);
                String symbol;
                if (stone == Board.getBlackStone()) {
                    symbol = "●";  // 黑棋
                } else if (stone == Board.getWhiteStone()) {
                    symbol = "○";  // 白棋
                } else {
                    symbol = "·";  // 空位
                }
                System.out.print(symbol);
                if (j < size - 1) {
                    System.out.print(" ");
                }
            }
            System.out.println(" │");
        }

        System.out.println("   " + generateSeparatorLine(size));
    }

    private String generateColumnHeaders(int size) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < size; i++) {
            sb.append(String.format("%d", i));
            if (i < 10 && i < size - 1) {
                sb.append(" ");
            } else if (i >= 10 && i < size - 1) {
                sb.append("");
            }
        }
        return sb.toString();
    }

    private String generateSeparatorLine(int size) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < size * 2 - 1; i++) {
            sb.append("─");
        }
        return sb.toString();
    }

    private void printInstructions() {
        System.out.println("游戏规则：");
        System.out.println("1. 黑棋（●）先行，白棋（○）后手");
        System.out.println("2. 双方轮流在棋盘上落子");
        System.out.println("3. 最先在横、竖、斜任意方向形成连续五子的一方获胜");
        System.out.println("4. 棋盘坐标从 0 到 14");
        System.out.println();
        System.out.println("操作说明：");
        System.out.println("- 输入 '行 列' 来落子，例如 '7 7' 表示在第7行第7列落子");
        System.out.println("- 输入 'q' 或 'quit' 退出游戏");
        System.out.println("- 输入 'help' 或 'h' 查看帮助");
        System.out.println();
    }
}
