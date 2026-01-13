package com.gomoku;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class GomokuGUI extends JFrame {
    private static final int CELL_SIZE = 40;
    private static final int MARGIN = 30;
    private static final int STONE_SIZE = 30;

    private Game game;
    private BoardPanel boardPanel;
    private JLabel statusLabel;
    private JButton resetButton;

    public GomokuGUI() {
        game = new Game();

        setTitle("五子棋游戏");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        // 创建顶部面板
        JPanel topPanel = new JPanel();
        statusLabel = new JLabel("当前玩家: " + game.getCurrentPlayer().getName() + " (" + game.getCurrentPlayer().getStoneColor() + ")");
        statusLabel.setFont(new Font("微软雅黑", Font.BOLD, 16));
        topPanel.add(statusLabel);
        add(topPanel, BorderLayout.NORTH);

        // 创建棋盘面板
        boardPanel = new BoardPanel();
        add(boardPanel, BorderLayout.CENTER);

        // 创建底部面板
        JPanel bottomPanel = new JPanel();
        resetButton = new JButton("重新开始");
        resetButton.setFont(new Font("微软雅黑", Font.PLAIN, 14));
        resetButton.addActionListener(e -> resetGame());
        bottomPanel.add(resetButton);
        add(bottomPanel, BorderLayout.SOUTH);

        pack();
        setLocationRelativeTo(null);
        setResizable(false);
    }

    private void resetGame() {
        game.reset();
        updateStatus();
        boardPanel.repaint();
    }

    private void updateStatus() {
        if (game.isGameOver()) {
            if (game.isDraw()) {
                statusLabel.setText("游戏结束 - 平局！");
            } else {
                statusLabel.setText("游戏结束 - " + game.getWinner().getName() + " (" + game.getWinner().getStoneColor() + ") 获胜！");
            }
        } else {
            statusLabel.setText("当前玩家: " + game.getCurrentPlayer().getName() + " (" + game.getCurrentPlayer().getStoneColor() + ")");
        }
    }

    class BoardPanel extends JPanel {
        public BoardPanel() {
            int size = game.getBoard().getSize() * CELL_SIZE + 2 * MARGIN;
            setPreferredSize(new Dimension(size, size));
            setBackground(new Color(220, 179, 92));

            addMouseListener(new MouseAdapter() {
                @Override
                public void mouseClicked(MouseEvent e) {
                    if (game.isGameOver()) {
                        return;
                    }

                    int x = e.getX();
                    int y = e.getY();

                    // 计算点击位置对应的棋盘坐标
                    int col = Math.round((float)(x - MARGIN) / CELL_SIZE);
                    int row = Math.round((float)(y - MARGIN) / CELL_SIZE);

                    if (row >= 0 && row < game.getBoard().getSize() &&
                        col >= 0 && col < game.getBoard().getSize()) {

                        if (game.makeMove(row, col)) {
                            repaint();
                            updateStatus();

                            if (game.isGameOver()) {
                                Timer timer = new Timer(500, evt -> {
                                    if (game.getWinner() != null) {
                                        JOptionPane.showMessageDialog(
                                            GomokuGUI.this,
                                            game.getWinner().getName() + " (" + game.getWinner().getStoneColor() + ") 获胜！",
                                            "游戏结束",
                                            JOptionPane.INFORMATION_MESSAGE
                                        );
                                    } else {
                                        JOptionPane.showMessageDialog(
                                            GomokuGUI.this,
                                            "平局！",
                                            "游戏结束",
                                            JOptionPane.INFORMATION_MESSAGE
                                        );
                                    }
                                });
                                timer.setRepeats(false);
                                timer.start();
                            }
                        }
                    }
                }
            });
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            Graphics2D g2d = (Graphics2D) g;
            g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

            // 绘制棋盘网格
            g2d.setColor(Color.BLACK);
            g2d.setStroke(new BasicStroke(1));

            int boardSize = game.getBoard().getSize();
            for (int i = 0; i < boardSize; i++) {
                // 画横线
                g2d.drawLine(MARGIN, MARGIN + i * CELL_SIZE,
                           MARGIN + (boardSize - 1) * CELL_SIZE, MARGIN + i * CELL_SIZE);
                // 画竖线
                g2d.drawLine(MARGIN + i * CELL_SIZE, MARGIN,
                           MARGIN + i * CELL_SIZE, MARGIN + (boardSize - 1) * CELL_SIZE);
            }

            // 绘制星位
            int[] starPoints = {3, 7, 11};
            g2d.setColor(Color.BLACK);
            for (int i : starPoints) {
                for (int j : starPoints) {
                    g2d.fillOval(MARGIN + j * CELL_SIZE - 4, MARGIN + i * CELL_SIZE - 4, 8, 8);
                }
            }

            // 绘制棋子
            for (int i = 0; i < boardSize; i++) {
                for (int j = 0; j < boardSize; j++) {
                    int stone = game.getBoard().getStone(i, j);
                    if (stone != Board.getEmptyStone()) {
                        int x = MARGIN + j * CELL_SIZE - STONE_SIZE / 2;
                        int y = MARGIN + i * CELL_SIZE - STONE_SIZE / 2;

                        if (stone == Board.getBlackStone()) {
                            g2d.setColor(Color.BLACK);
                        } else {
                            g2d.setColor(Color.WHITE);
                        }

                        g2d.fillOval(x, y, STONE_SIZE, STONE_SIZE);
                        g2d.setColor(Color.BLACK);
                        g2d.setStroke(new BasicStroke(1));
                        g2d.drawOval(x, y, STONE_SIZE, STONE_SIZE);
                    }
                }
            }
        }
    }
}
