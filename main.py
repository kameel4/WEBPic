import os
import sys

import pygame
import requests


def get_coords(json):
    try:
        n = \
            json['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData'][
                'boundedBy'][
                'Envelope']['lowerCorner']
    except Exception:
        n = json["response"]['GeoObjectCollection']['featureMember'][0]['GeoObject']['boundedBy']['Envelope'][
            "lowerCorner"]
    ns = ''
    for i in n:
        if i != ' ':
            ns += i
        else:
            ns += ','
    ms = ''
    try:
        m = \
            json['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData'][
                'boundedBy'][
                'Envelope']['upperCorner']
    except Exception:
        m = json["response"]['GeoObjectCollection']['featureMember'][0]['GeoObject']['boundedBy']['Envelope'][
            "upperCorner"]
    for i in m:
        if i != ' ':
            ms += i
        else:
            ms += ','
    coords = f'{ns}~{ms}'
    return coords


def get_pic(mp="map"):
    global map_file, scale, longitude, latitude
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={longitude},{latitude}&spn={scale},{scale}&l={mp}"
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
    global scale, longitude, latitude, k, finded, textochek, my_map
    if not finded:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
            if scale >= 6:
                scale -= 6
                get_pic(my_map)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
            if scale <= 60:
                scale += 6
                get_pic(my_map)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if latitude <= 70:
                latitude += k
                get_pic(my_map)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if latitude >= -77:
                latitude -= k
                get_pic(my_map)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if longitude <= 167:
                longitude += k
                get_pic(my_map)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if longitude >= -167:
                longitude -= k
                get_pic(my_map)
    else:
        if textochek != '':
            toponym_to_find = textochek
        else:
            toponym_to_find = "Australia"

        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json",
            "l": my_map
        }

        response = requests.get(geocoder_api_server, params=geocoder_params)

        if not response:
            print("Ты сам понял, что написал, нетъ?")
            return None

        json_responses = response.json()
        toponym = json_responses["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        longitude, latitude = float(toponym_longitude), float(toponym_lattitude)

        delta = "0.005"
        scale = 0.05

        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": ",".join([delta, delta]),
            "l": my_map,
            "bbox": get_coords(json_responses),
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)

        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)

        finded = False


if __name__ == '__main__':
    map_file = "map.png"
    scale = 43
    longitude = 136
    latitude = -25.5
    k = scale / 4
    get_pic()
    pygame.init()
    pygame.display.set_caption('map')
    size = width, height = 600, 475
    screen = pygame.display.set_mode(size)
    textochek = ''
    color = "grey"
    change_list = [pygame.K_PAGEDOWN, pygame.K_PAGEUP, pygame.K_UP, pygame.K_DOWN,
                   pygame.K_RIGHT, pygame.K_LEFT]
    finded = False
    my_map = "map"

    running = True

    while running:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in change_list:
                    change_coords(event)
                else:
                    if color == "white":
                        if event.key != pygame.K_BACKSPACE:
                            textochek += event.unicode
                        else:
                            textochek = textochek[:-1]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] <= 460 and event.pos[1] <= 25:
                    if color == "grey":
                        color = "white"
                    else:
                        color = "grey"
                elif event.pos[0] <= 532 and event.pos[1] <= 25:
                    finded = True
                    change_coords(event)
                elif event.pos[0] > 532 and event.pos[1] <= 25:
                    if my_map == "map":
                        my_map = "sat"
                    # elif my_map == "sat":
                    #     my_map = "sat,scl"
                    else:
                        my_map = "map"
                    finded = True
                    change_coords(event)

        if color == "grey":
            pygame.draw.rect(screen, (204, 204, 204), (0, 0, 460, 30))
        else:
            pygame.draw.rect(screen, (244, 244, 244), (0, 0, 460, 30))
        pygame.draw.rect(screen, (163, 198, 192), (460, 0, 2, 30))
        pygame.draw.rect(screen, (104, 139, 176), (462, 0, 68, 30))
        pygame.draw.rect(screen, (163, 198, 192), (530, 0, 2, 30))
        pygame.draw.rect(screen, (104, 139, 176), (532, 0, 68, 30))

        font = pygame.font.Font("19889.ttf", 20)
        text = font.render(
            "Find", True, (255, 255, 255))
        place = text.get_rect(
            center=(496, 15))
        screen.blit(text, place)

        font = pygame.font.Font("19889.ttf", 20)
        text = font.render(
            "Map", True, (255, 255, 255))
        place = text.get_rect(
            center=(566, 15))
        screen.blit(text, place)

        input_font = pygame.font.SysFont(None, 16)
        input_text = font.render(
            textochek, True, (5, 5, 5))
        place = text.get_rect(
            center=(20, 15))
        screen.blit(input_text, place)

        screen.blit(pygame.image.load(map_file), (0, 25))
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()
    os.remove(map_file)

# bad comment
