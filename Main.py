import sys

from tkinter import messagebox

import pygame

from chessman import *


class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((750, 600))
        self.screen.fill((190, 190, 190))
        self.Black = (0, 0, 0)
        self.chessman_list = []
        self.init_chessman()

    @staticmethod
    def posconvert(x, y):
        return [x * 60 + 30, y * 60]
        
    def draw_able_pos(self, chessman):
        for pos in chessman.able_pos(self.chessman_list):
            pygame.draw.circle(self.screen, (0, 0, 255), [pos[0] * 60 + 60, pos[1] * 60 + 30], 10, 10)
            pygame.draw.circle(self.screen, (0, 255, 0), [chessman.x * 60 + 60, chessman.y * 60 + 30], 30, 3)

    def drawchessboard(self):
        self.screen.fill((190, 190, 190))
        x = 120
        y = 30
        for i in range(10):
            pygame.draw.aaline(self.screen, self.Black, [60, y], [540, y], 1)
            y += 60
        for i in range(7):
            pygame.draw.aaline(self.screen, self.Black, [x, 30], [x, 270], 1)
            pygame.draw.aaline(self.screen, self.Black, [x, 330], [x, 570], 1)
            x += 60
        pygame.draw.aaline(self.screen, self.Black, [60, 30], [60, 570], 1)
        pygame.draw.aaline(self.screen, self.Black, [540, 30], [540, 570], 1)
        pygame.draw.aaline(self.screen, self.Black, [240, 30], [360, 150], 1)
        pygame.draw.aaline(self.screen, self.Black, [360, 30], [240, 150], 1)
        pygame.draw.aaline(self.screen, self.Black, [240, 450], [360, 570], 1)
        pygame.draw.aaline(self.screen, self.Black, [360, 450], [240, 570], 1)
        for x in range(9):
            for y in range(10):
                chessman = self.chessman_list[x][y]
                if chessman != 0:
                    self.screen.blit(chessman.image, self.posconvert(chessman.x, chessman.y))

    def init_chessman(self):
        self.chessman_list = []
        for x in range(9):
            self.chessman_list.append([])
            for y in range(10):
                self.chessman_list[x].append(0)
        list0 = [(9, -1, "Red", 0), (0, 1, "Black", 1)]
        for y1, m, player, p in list0:
            y2 = y1 + 2 * m
            y3 = y1 + 3 * m
            list1 = [(3, Guard.Guard, "image/" + player + "/Guard.png"),
                     (2, Bishop.Bishop, "image/" + player + "/Bishop.png"),
                     (1, Knight.Knight, "image/" + player + "/Knight.png"),
                     (0, Rook.Rook, "image/" + player + "/Rook.png")]

            self.chessman_list[4][y1] = King.King(4, y1, p, "image/" + player + "/King.png")
            self.chessman_list[1][y2] = Cannon.Cannon(1, y2, p, "image/" + player + "/Cannon.png")
            self.chessman_list[7][y2] = Cannon.Cannon(7, y2, p, "image/" + player + "/Cannon.png")
            for x, chessman, image_path in list1:
                self.chessman_list[x][y1] = chessman(x, y1, p, image_path)
                self.chessman_list[8 - x][y1] = chessman(8 - x, y1, p, image_path)
            for x in range(0, 10, 2):
                self.chessman_list[x][y3] = Pawn.Pawn(x, y3, p, "image/" + player + "/Pawn.png")

    @staticmethod
    def get_king(player, chessman_list):
        for l in chessman_list:
            for chessman in l:
                if isinstance(chessman, King.King) and chessman.player == player:
                    return chessman

    def check(self, player, chessman_list):
        attacked_pos = []
        for l in chessman_list:
            for chessman in l:
                if chessman != 0 and chessman.player == 1 - player:
                    for pos in chessman.able_pos(chessman_list):
                        attacked_pos.append(pos)
        king1 = self.get_king(player, chessman_list)
        king2 = self.get_king(1 - player, chessman_list)
        if [king1.x, king1.y] in attacked_pos:
            return True
        elif king1.x == king2.x:
            for y in range(self.get_king(1, chessman_list).y + 1, self.get_king(0, chessman_list).y):
                if chessman_list[self.get_king(0, chessman_list).x][y] != 0:
                    return False
            return True
        else:
            return False

    def is_over(self, player, chessman_list):
        l0 = []
        for l1 in chessman_list:
            for chessman in l1:
                if chessman != 0 and chessman.player == player:
                    l2 = [chessman]
                    for pos in chessman.able_pos(chessman_list):
                        l2.append(pos)
                    l0.append(l2)
        for x in l0:
            rx = x[0].x
            ry = x[0].y
            for i in range(1, len(x)):
                pos = x[i]
                chessman_list[rx][ry] = 0
                y = chessman_list[pos[0]][pos[1]]
                x[0].x = pos[0]
                x[0].y = pos[1]
                chessman_list[pos[0]][pos[1]] = x[0]
                if not self.check(player, chessman_list):
                    x[0].x = rx
                    x[0].y = ry
                    chessman_list[pos[0]][pos[1]] = y
                    chessman_list[rx][ry] = x[0]
                    return False
                x[0].x = rx
                x[0].y = ry
                chessman_list[pos[0]][pos[1]] = y
                chessman_list[rx][ry] = x[0]
        return True

    def start_game(self):
        self.drawchessboard()
        ischoose = False
        player = 0
        cx = cy = -1
        while True:
            if player == 0:
                self.screen.blit(pygame.image.load("image/Red/King.png"), [590, 250])
            else:
                self.screen.blit(pygame.image.load("image/Black/King.png"), [590, 250])
            for event in pygame.event.get():
                if not self.is_over(player, self.chessman_list):
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = event.pos
                        x = (mx - 30) // 60
                        y = my // 60
                        if 0 <= x <= 8 and 0 <= y <= 9:
                            if not ischoose:
                                cx = x
                                cy = y
                                chessman = self.chessman_list[x][y]
                                if chessman != 0:
                                    if chessman.player == player:
                                        self.drawchessboard()
                                        self.draw_able_pos(chessman)
                                        ischoose = True
                            else:
                                chessman = self.chessman_list[x][y]
                                if x == cx and y == cy:
                                    self.drawchessboard()
                                    ischoose = False
                                elif chessman != 0 and chessman.player == self.chessman_list[cx][cy].player:
                                    cx = x
                                    cy = y
                                    self.drawchessboard()
                                    self.draw_able_pos(chessman)
                                else:
                                    chessman0 = self.chessman_list[cx][cy]
                                    chessman1 = self.chessman_list[x][y]
                                    if [x, y] in self.chessman_list[cx][cy].able_pos(self.chessman_list):
                                        self.chessman_list[x][y] = chessman0
                                        chessman0.x = x
                                        chessman0.y = y
                                        self.chessman_list[cx][cy] = 0
                                        if self.check(player, self.chessman_list):
                                            self.chessman_list[x][y] = chessman1
                                            chessman0.x = cx
                                            chessman0.y = cy
                                            self.chessman_list[cx][cy] = chessman0
                                            messagebox.askokcancel("提示：", "移动将会送将！")
                                        else:
                                            self.drawchessboard()
                                            ischoose = False
                                            player = 1 - player
                else:
                    if player == 0:
                        a = messagebox.askokcancel("黑胜", "是否重新开始游戏？")
                        if a:
                            self.init_chessman()
                            self.drawchessboard()
                            ischoose = False
                            player = 0
                            cx = cy = -1
                        else:
                            pygame.quit()
                            sys.exit()
                    else:
                        a = messagebox.askokcancel("红胜", "是否重新开始游戏？")
                        if a:
                            self.init_chessman()
                            self.drawchessboard()
                            ischoose = False
                            player = 0
                            cx = cy = -1
                        else:
                            pygame.quit()
                            sys.exit()
            pygame.display.flip()


if __name__ == "__main__":
    Main().start_game()
