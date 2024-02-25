import pygame
from pygame_phyics import util
from pygame_phyics.manger import Manger
from pygame_phyics.objects.gameobject import GameObject


class TileMap(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, tiles, sheet_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.tiles = tiles
        self.sheet = Manger.tile_sheet[sheet_name]
        self.sheet_name = sheet_name
        self.size = self.sheet.size
        self.canvas = self.sheet.surfaces

    def set_tile(self, xy, value):
        match xy:
            case n if n[0] >= 0 and n[1] >= 0:
                y = self.tiles[0][n[1]]
                if y != None:
                    y[n[0]] = value
                else:
                    y = [][n[0]] = value
            case n if n[0] < 0 and n[1] >= 0:
                y = self.tiles[0][n[1]]
                if y != None:
                    y[-n[0]] = value
                else:
                    y = [][-n[0]] = value
            case n if n[0] < 0 and n[1] < 0:
                y = self.tiles[0][-n[1]]
                if y != None:
                    y[-n[0]] = value
                else:
                    y = [][n[0]] = value
            case n if n[0] >= 0 and n[1] < 0:
                y = self.tiles[0][-n[1]]
                if y != None:
                    y[n[0]] = value
                else:
                    y = [][n[0]] = value
        
    def get_tile(self, xy):
        try:
            match xy:
                case n if n[0] >= 0 and n[1] >= 0:
                    return self.tiles[0][n[1] - 1][n[0]]
                case n if n[0] < 0 and n[1] >= 0:
                    return self.tiles[1][n[1] - 1][-n[0] - 1]
                case n if n[0] < 0 and n[1] < 0:
                    return self.tiles[2][-n[1]][-n[0] - 1]
                case n if n[0] >= 0 and n[1] < 0:
                    return self.tiles[3][-n[1]][n[0]]
        except:
            return None
    
    def render(self, surface, camera):
        HALF_WIDTH = Manger.WIDTH / (self.size * 2)
        HALF_HEIGHT = Manger.HEIGHT / (self.size * 2)
        tile_camera = camera.location.world_position.div_float(self.size)
        xrange = int(tile_camera.x - HALF_WIDTH), int(tile_camera.x + HALF_WIDTH) + 1
        yrange = int(tile_camera.y - HALF_HEIGHT), int(tile_camera.y + HALF_HEIGHT) + 1
        pygame.draw.circle(surface, (255, 255, 255), (500, 400), 5)
        for y in range(*yrange):
            for x in range(*xrange):
                tile_n = self.get_tile((x, y))
                if tile_n != None:
                    image = self.canvas[tile_n]
                    cx = (HALF_WIDTH + x) * self.size - camera.location.world_position.x
                    cy = (HALF_HEIGHT - y) * self.size + camera.location.world_position.y
                    surface.blit(image, (cx, cy))