import pygame
import random
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui.ui', self)
        self.but.clicked.connect(self.cl)

    def cl(self):
        self.close()
        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    if app.exec_():
        f = 1
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = True
        pygame.draw.circle(screen, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (random.randint(1, 500), random.randint(1, 500)), random.randint(1, 100), 2)
        pygame.display.flip()
        clock.tick(4)