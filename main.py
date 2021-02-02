import os
import sys

import pygame
import requests


def get_pic():
    global map_file, scale, longitude, latitude
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


def change_coords(event):
    global scale, longitude, latitude, k
    if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
        if scale >= 6:
            scale -= 6
            get_pic()
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
        if scale <= 60:
            scale += 6
            get_pic()
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
        if latitude <= 70:
            latitude += k
            get_pic()
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
        if latitude >= -77:
            latitude -= k
            get_pic()
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
        if longitude <= 167:
            longitude += k
            get_pic()
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
        if longitude >= -167:
            longitude -= k
            get_pic()


if __name__ == '__main__':
    map_file = "map.png"
    scale = 43
    longitude = 136
    latitude = -25.5
    k = scale / 4
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
            if event.type == pygame.KEYDOWN:
                change_coords(event)

        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()
    os.remove(map_file)

# bad comment
