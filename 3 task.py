import os
import sys

import pygame
import requests


def change_coords():
    global longitude, latitude

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


if __name__ == '__main__':
    map_file = "map.png"
    scale = 0.1
    k = scale / 50
    longitude, latitude = 54.721045726797506, 55.94144523201517
    change_coords()
    pygame.init()
    pygame.display.set_caption('map')
    size = width, height = 600, 450
    screen = pygame.display.set_mode(size)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
                if scale >= 5:
                    scale -= 6
                    change_coords()
                elif 0.2 < scale < 5:
                    scale -= 0.1
                    change_coords()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
                if 10 > scale <= 50:
                    scale += 6
                    change_coords()
                elif scale <= 10:
                    scale += 0.1
                    change_coords()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if -180 <= longitude <= 180:
                    longitude -= k
                    change_coords()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if -180 <= longitude <= 180:
                    longitude += k
                    change_coords()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if -90 <= latitude <= 90:
                    latitude += k
                    change_coords()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if -90 <= latitude <= 90:
                    latitude -= k
                    change_coords()

        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()
    os.remove(map_file)
