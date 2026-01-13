package com.gomoku;

public class Player {
    private String name;
    private int stone;

    public Player(String name, int stone) {
        this.name = name;
        this.stone = stone;
    }

    public String getName() {
        return name;
    }

    public int getStone() {
        return stone;
    }

    public String getStoneColor() {
        if (stone == Board.getBlackStone()) {
            return "黑棋";
        } else if (stone == Board.getWhiteStone()) {
            return "白棋";
        } else {
            return "未知";
        }
    }
}
