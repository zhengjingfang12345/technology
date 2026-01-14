package com.gomoku;

public class Game {
    private Board board;
    private Player player1;
    private Player player2;
    private Player currentPlayer;
    private boolean gameOver;
    private Player winner;

    public Game() {
        board = new Board();
        player1 = new Player("玩家1", Board.getBlackStone());
        player2 = new Player("玩家2", Board.getWhiteStone());
        currentPlayer = player1;
        gameOver = false;
        winner = null;
    }

    public boolean makeMove(int row, int col) {
        if (gameOver) {
            return false;
        }

        if (board.placeStone(row, col, currentPlayer.getStone())) {
            if (board.checkWin(row, col, currentPlayer.getStone())) {
                gameOver = true;
                winner = currentPlayer;
            } else if (board.isFull()) {
                gameOver = true;
                winner = null;  // 平局
            } else {
                switchPlayer();
            }
            return true;
        }
        return false;
    }

    private void switchPlayer() {
        currentPlayer = (currentPlayer == player1) ? player2 : player1;
    }

    public void reset() {
        board.reset();
        currentPlayer = player1;
        gameOver = false;
        winner = null;
    }

    public Board getBoard() {
        return board;
    }

    public Player getCurrentPlayer() {
        return currentPlayer;
    }

    public boolean isGameOver() {
        return gameOver;
    }

    public Player getWinner() {
        return winner;
    }

    public boolean isDraw() {
        return gameOver && winner == null;
    }
}
