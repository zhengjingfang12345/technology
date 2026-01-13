package com.gomoku;

public class Board {
    private static final int SIZE = 15;
    private int[][] board;
    private static final int EMPTY = 0;
    private static final int BLACK = 1;
    private static final int WHITE = 2;

    public Board() {
        board = new int[SIZE][SIZE];
        reset();
    }

    public void reset() {
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                board[i][j] = EMPTY;
            }
        }
    }

    public boolean isValidMove(int row, int col) {
        if (row < 0 || row >= SIZE || col < 0 || col >= SIZE) {
            return false;
        }
        return board[row][col] == EMPTY;
    }

    public boolean placeStone(int row, int col, int player) {
        if (!isValidMove(row, col)) {
            return false;
        }
        board[row][col] = player;
        return true;
    }

    public int getStone(int row, int col) {
        if (row < 0 || row >= SIZE || col < 0 || col >= SIZE) {
            return -1;
        }
        return board[row][col];
    }

    public boolean checkWin(int row, int col, int player) {
        return checkDirection(row, col, player, 1, 0) ||  // 水平
               checkDirection(row, col, player, 0, 1) ||  // 垂直
               checkDirection(row, col, player, 1, 1) ||  // 对角线 \
               checkDirection(row, col, player, 1, -1);   // 对角线 /
    }

    private boolean checkDirection(int row, int col, int player, int dRow, int dCol) {
        int count = 1;

        // 正向检查
        count += countStones(row, col, player, dRow, dCol);

        // 反向检查
        count += countStones(row, col, player, -dRow, -dCol);

        return count >= 5;
    }

    private int countStones(int row, int col, int player, int dRow, int dCol) {
        int count = 0;
        int r = row + dRow;
        int c = col + dCol;

        while (r >= 0 && r < SIZE && c >= 0 && c < SIZE && board[r][c] == player) {
            count++;
            r += dRow;
            c += dCol;
        }

        return count;
    }

    public boolean isFull() {
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                if (board[i][j] == EMPTY) {
                    return false;
                }
            }
        }
        return true;
    }

    public int getSize() {
        return SIZE;
    }

    public static int getBlackStone() {
        return BLACK;
    }

    public static int getWhiteStone() {
        return WHITE;
    }

    public static int getEmptyStone() {
        return EMPTY;
    }
}
