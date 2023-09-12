import pygame as pg
import json

LEVEL_ID = 4
IMPLEMENTED_LEVELS = [1, 2, 3, 4]

from utils import SCALE

COLORS = [
    "white",
    "red",
    "green",
    "blue",
    "yellow",
    "orange",
    "purple",
    "pink",
    "brown",
    "cyan",
]


pg.init()
screen = pg.display.set_mode((int(350 * SCALE), int(450 * SCALE)))
font = pg.font.Font("assets/fonts/Comfortaa.ttf", 20)
bfont = pg.font.Font("assets/fonts/Comfortaa.ttf", 40)


def load_tiles(level_id):
    data = json.load(open("Gamedata/Levels/level" + str(level_id) + ".json"))
    tiles = [Tile(x, y) for x in range(7) for y in range(9)]

    for tile in tiles:
        if [tile.x, tile.y] in data["wallPositions"]:
            tile.txt = "W"
            tile.value = REFERENCES["W"](tile.x, tile.y)
        elif [tile.x, tile.y] in data["pitPositions"]:
            tile.txt = "P"
            tile.value = REFERENCES["P"](tile.x, tile.y)
        elif [tile.x, tile.y] == data["playerStartPosition"]:
            tile.txt = "O"
            tile.value = REFERENCES["O"](tile.x, tile.y)
        for enemy in data["enemies"]:
            enemy = data["enemies"][enemy]
            enemy_positions = enemy["positions"]

            if enemy_positions[0] == [tile.x, tile.y]:
                tile.txt = "E" if enemy["type"] == "glider" else "AE"
                tile.value = REFERENCES[tile.txt](tile.x, tile.y, enemy_positions)

    return tiles


def debug(txt):
    screen.blit(font.render(txt, True, "white", "black"), (0, 0))


def encode_into(filename, tiles):
    data = {
        "levelId": 1,
        "playerStartPosition": [3, 0],
        "pitPositions": [],
        "wallPositions": [],
        "enemies": {},
    }

    for tile in tiles:
        if tile.txt == "W":
            data["wallPositions"].append([tile.value.x, tile.value.y])
        elif tile.txt == "P":
            data["pitPositions"].append([tile.value.x, tile.value.y])
        elif tile.txt == "O":
            data["playerStartPosition"] = [tile.value.x, tile.value.y]
        elif tile.txt == "E":
            data["enemies"]["enemy" + str(len(data["enemies"]) + 1)] = {
                "type": "glider",
                "positions": tile.value.positions,
            }
        elif tile.txt == "AE":
            data["enemies"]["enemy" + str(len(data["enemies"]) + 1)] = {
                "type": "glider-advanced",
                "positions": tile.value.positions,
            }

    json.dump(data, open("Gamedata/Levels/" + filename, "w"), indent=4)


class WallTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class PitTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class EnemyTile:
    def __init__(self, x, y, positions):
        self.x = x
        self.y = y
        self.positions = positions
        self.color = COLORS.pop()
        print(positions)


class PlayerTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class GoalTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class AdvancedEnemyTile:
    def __init__(self, x, y, positions):
        self.x = x
        self.y = y
        self.positions = positions


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.txt = ""
        self.rect = pg.Rect(
            10 + self.x * 40 * SCALE, 70 + self.y * 40 * SCALE, 40 * SCALE, 40 * SCALE
        )
        self.value = None

    def update(self):
        hover = True if self.rect.collidepoint(pg.mouse.get_pos()) else False
        if hover:
            pg.draw.rect(screen, "#222222", self.rect)
        if self.txt != "":
            label = bfont.render(self.txt, True, "white")
            labelrect = label.get_rect(center=self.rect.center)
            screen.blit(label, labelrect)
        pg.draw.rect(screen, "white", self.rect, 1)
        if self.txt == "E" or self.txt == "AE":
            enemy_paths.append([self.value.positions, self.value.color])

    def check_click(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            global currently_selected
            if mode == "enemy" or mode == "advanced_enemy":
                if [self.x, self.y] not in positions:
                    positions.append([self.x, self.y])
            elif currently_selected != None:
                if str(currently_selected) == "O":
                    for tile in TILES:
                        if tile.txt == "O":
                            tile.txt = ""
                            tile.value = None
                if self.txt == str(currently_selected):
                    self.txt = ""
                    self.value = None
                else:
                    self.txt = str(currently_selected)
                    self.value = REFERENCES[currently_selected.txt](self.x, self.y)


class TileSelector:
    def __init__(self, x, y, txt):
        self.x = x
        self.y = y
        self.txt = txt
        self.rect = pg.Rect(
            30 + self.x * 40 * SCALE, 70 + self.y * 45 * SCALE, 40 * SCALE, 40 * SCALE
        )

    def __str__(self):
        return self.txt

    def update(self):
        hover = True if self.rect.collidepoint(pg.mouse.get_pos()) else False
        if hover:
            pg.draw.rect(screen, "#222222", self.rect)
        pg.draw.rect(screen, "red", self.rect, 1)

        label = bfont.render(self.txt, True, "red")
        labelrect = label.get_rect(center=self.rect.center)
        screen.blit(label, labelrect)

    def check_click(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            global currently_selected, mode, enemy_paths
            currently_selected = self
            if self.txt == "E" or self.txt == "AE":
                if mode == "edit":
                    mode = "enemy" if self.txt == "E" else "advanced_enemy"
                elif (mode == "enemy" or mode == "advanced_enemy") and any(positions):
                    x, y = positions[-1]
                    for tile in TILES:
                        if tile.x == x and tile.y == y:
                            found_tile = tile
                            break

                    found_tile.txt = str(currently_selected)
                    found_tile.value = REFERENCES["E" if mode == "enemy" else "AE"](
                        x, y, positions.copy()
                    )
                    positions.clear()
                    mode = "edit"
                    currently_selected = None
                else:
                    mode = "edit"
                    currently_selected = None


TILE_TYPES = ["W", "P", "O", "E", "AE", "G"]
REFERENCES = {
    "W": WallTile,
    "P": PitTile,
    "O": PlayerTile,
    "E": EnemyTile,
    "AE": AdvancedEnemyTile,
    "G": GoalTile,
}
TILES = (
    [Tile(x, y) for x in range(7) for y in range(9)]
    if LEVEL_ID not in IMPLEMENTED_LEVELS
    else load_tiles(LEVEL_ID)
)
TILE_SELECTORS = [
    TileSelector(7, y, txt)
    for y, txt in enumerate(TILE_TYPES)
    if txt not in ["AE", "G"]
]

currently_selected = None

mode = "edit"
positions = []
enemy_paths = []

while True:
    enemy_paths = []
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.MOUSEBUTTONDOWN:
            for tile in TILES + TILE_SELECTORS:
                tile.check_click()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s:
                print("Saving...")
                encode_into("level" + str(LEVEL_ID) + ".json", TILES)
            if event.key == pg.K_ESCAPE:
                mode = "edit"
    screen.fill("black")
    for tile in TILES + TILE_SELECTORS:
        tile.update()

    for path, color in enemy_paths:
        pg.draw.lines(
            screen,
            color,
            False,
            [
                (x * 40 * SCALE + 10 + SCALE * 20, y * 40 * SCALE + 70 + SCALE * 20)
                for x, y in path
            ],
            2,
        )

    debug(
        f"Currently selected: {currently_selected} | Mode: {mode} | Positions: {str(positions)}"
    )

    pg.display.flip()
