import os
import sys

import pygame
import requests


def get_pic(k):
    global map_file, scale, longitude, latitude

    scale += k
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={longitude},{latitude}&spn={scale},{scale}&l=map"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


def change_coords(x, y):
    global scale, map_file, longitude, latitude
    new_x, new_y = longitude + x, latitude + y
    if (new_x <= 180 and new_x >= -180) and \
            (new_y <= 70 and new_y >= -80):
        longitude += x
        latitude += y

    map_request = f"http://static-maps.yandex.ru/1.x/?ll={longitude},{latitude}&spn={scale},{scale}&l=map"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    print(longitude, latitude)


if __name__ == '__main__':
    map_file = "map.png"
    scale = 43
    longitude = 136
    latitude = -25

    get_pic(0)
    pygame.init()
    pygame.display.set_caption('map')
    size = width, height = 600, 450
    screen = pygame.display.set_mode(size)

    running = True

    while running:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
                if scale >= 6:
                    get_pic(-6)
                    print('-6')
            if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
                if scale <= 80:
                    get_pic(6)
                    print('+6')

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                change_coords(0, 6)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                change_coords(0, -6)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                change_coords(6, 0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                change_coords(-6, 0)

        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()
    os.remove(map_file)