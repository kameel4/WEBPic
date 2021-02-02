import os
import sys

import pygame
import requests


def get_pic():
    global map_file, scale
    map_request = f"http://static-maps.yandex.ru/1.x/?ll=136.274000,-25.596000&spn={scale},{scale}&l=map"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


def plus_spn():
    global scale, map_file
    if scale <= 50:
        scale += 3
    map_request = f"http://static-maps.yandex.ru/1.x/?ll=136.274000,-25.596000&spn={scale},{scale}&l=map"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


if __name__ == '__main__':
    map_file = "map.png"
    scale = 43
    get_pic()
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
                    scale -= 6
                    get_pic()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
                plus_spn()

        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()
    os.remove(map_file)