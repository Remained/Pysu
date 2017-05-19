#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Imports
import os
import sys
import settings_parse
import pygame
import create_stage
import arrow_object


# Constants
NAME = "Pysu!"
VERSION = "0.01-ALPHA"
SCROLL_SPEED = 29
# Game arrows
arrows = []
arrow_1 = arrow_object.arrowObject(192, 192, 0, 1, 0)
arrow_2 = arrow_object.arrowObject(92, 192, 234, 1, 0)
arrow_3 = arrow_object.arrowObject(448, 192, 0, 1, 0)
arrows.append(arrow_1)
arrows.append(arrow_2)
arrows.append(arrow_3)

# Directories of files
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
beatmaps = os.path.abspath(os.path.join(os.path.dirname(__file__), 'beatmaps'))

# Create dir if doesn't exist (used to generate default settings)
if not os.path.isdir(basedir):
    os.mkdir(basedir)


def draw_arrows(arrows):
    arrow_images = []
    for arrow in arrows:
        image_dir = arrow_object.arrow_skin(arrow.get_column())
        arrow_image = pygame.image.load(image_dir)
        arrow_images.append(arrow_image)
    return arrow_images


# Load normal key images and create image list
def loadKeyImages():
    image = []
    infoObject = pygame.display.Info()
    for i in xrange(4):
        file = create_stage.key_image_file(i)
        key_image = pygame.image.load(file)
        image.append(key_image)
    return image


# Main game init and loop
def main():
    # Get settings from file
    settings = settings_parse.parse(basedir)

    # Get keys from settings
    KEYS = [int(key) for key in settings['keys'].split(",")]

    # Init pygame module
    pygame.init()

    # Set game clock
    clock = pygame.time.Clock()

    # Set game display (determine fullscreen mode according to settings)
    infoObject = pygame.display.Info()
    if bool(int(settings["fullscreen"])):
        os.environ['SDL_VIDEO_WINDOW_POS'] = '1'
        game_display = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.NOFRAME)
    else:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (infoObject.current_w/4,10)
        game_display = pygame.display.set_mode((int(settings["width"]),int(settings["height"])), pygame.NOFRAME)
    pygame.display.set_caption(NAME + " - " + VERSION)
    infoObject = pygame.display.Info()
    i = 0
    # Game run loop
    while 1:
        # Get key images list
        keyImages = loadKeyImages()
        arrow_images = draw_arrows(arrows)

        original_height, original_width, ratio = 0, 0, 0
        # Check if players wants to leave game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Set repeat interval to 60 milliseconds
        pygame.key.set_repeat(60)

        # Get pressed keys and check if keys determined in settings were pressed
        for key in KEYS:
            if pygame.key.get_pressed()[key] == 1:
                # Change image to pressed button
                file = create_stage.keypressed_image_file(KEYS.index(key))
                keyImages[KEYS.index(key)] = pygame.image.load(file)

        # Draw images of keys
        for i, image in enumerate(keyImages):
            original_width, original_height = image.get_size()
            ratio = float(infoObject.current_h) / original_height
            image = pygame.transform.smoothscale(image, (int(ratio * original_width), int(ratio * original_height)))
            game_display.blit(image, (infoObject.current_w / 2 - original_width * ratio * 4 / 2 + i * original_width * ratio, -50))

        print arrow_images
        for i, arrow in enumerate(arrow_images):
            width, height = arrow.get_size()
            arrow = pygame.transform.smoothscale(arrow, (int(width * ratio * 0.8), int(height * ratio * 0.8)))
            game_display.blit(arrow, (5 + infoObject.current_w / 2 - original_width * 2 + original_width * ratio * (arrows[i].get_column() - 1), 595 - 192 * arrows[i].get_time() / 1000.0 * SCROLL_SPEED + pygame.time.get_ticks() / 1000.0 * SCROLL_SPEED * 592.0 / 192))

        # Update game and tick game
        print pygame.time.get_ticks()
        pygame.display.update()
        pygame.display.flip()
        clock.tick(144)

# Call main
main()

