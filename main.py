import os
import sys

import pygame
import requests

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Mario')
    size = width, height = 600, 450
    screen = pygame.display.set_mode(size)
    scale = 43

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


clock = pygame.time.Clock()
running = True

while running:
    screen.blit(pygame.image.load(map_file), (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            os.remove(map_file)
            plus_spn()
    pygame.display.flip()
    clock.tick(60)
