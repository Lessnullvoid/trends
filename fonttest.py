# -*- coding: utf-8 -*-

import pygame, sys


unistr = u"サトノダイヤモンド"
pygame.font.init()
srf = pygame.display.set_mode((640,480))
f = pygame.font.Font("BloggerSans.ttf",20)
srf.blit(f.render(unistr,True,(255,50,50)),(0,0))
pygame.display.flip()

while True:
    srf.blit(f.render(unistr,True,(255,255,255)),(0,0))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
