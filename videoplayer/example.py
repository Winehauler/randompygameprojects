import sys
import os
import pygame
from pygame.locals import *

from VideoPlayer import VideoPlayer



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('need path to video as argument')
        sys.exit()

    resolution = (900, 600)
    video_filename = os.path.abspath(sys.argv[1])

    # init pygame
    pygame.init()
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption('VideoPlayer example')

    # create 2 videoplayers
    videoplayer = VideoPlayer(video_filename, shape=(200,200), keep_ratio=True)
    videoplayer.set_crop((0,0), (100, 100))
    videoplayer2 = VideoPlayer(video_filename, shape=None)
    start_pos = videoplayer2.num_frames // 3
    videoplayer2.get_frame(start_pos-1)

    running = True
    while running:

        # handle events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == 27:  # esc
                    running = False

        # get next frames from videoplayers and blit them on the screen
        frame = videoplayer.get_frame()
        if frame:
            screen.blit(frame, (0,0))

        frame = videoplayer2.get_frame()
        if frame:
            screen.blit(frame, (200, 20))
            
        pygame.display.flip()
    pygame.quit()
    
    
