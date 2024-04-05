import sys
import pygame

pygame.init()
pygame.display.set_caption("Conway's game of life")
img = pygame.image.load("Glider.png")
pygame.display.set_icon(img)

width, height = 1024, 768
cell_size = 5
dead_color = 'light gray'
living_color = 'black'
master_list: list[list[list[bool | int]]] = [
    [
        [False, 0] for _ in range(height // cell_size)
    ] for _ in range(width // cell_size)
]
living_cells = []

screen = pygame.display.set_mode((width, height))
screen.fill(dead_color)
pygame.display.update()


def level_set_up():
    global master_list, living_cells
    master_list = []
    living_cells = []
    for i in range(width // cell_size):
        master_list.append([])
        for _ in range(height // cell_size):
            master_list[i].append([False, 0])


def main():
    global master_list, cell_size
    demonstration_mode = False
    interval_time = 50
    key = None
    while True:
        for event in pygame.event.get():
            # ends the display
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    life_death()
                # "c" will reset the screen
                elif event.key == pygame.K_c:
                    level_set_up()
                elif event.key == pygame.K_d:
                    demonstration_mode = not demonstration_mode
                # up arrow increases cell size
                elif event.key == pygame.K_UP:
                    cell_size += 1
                    level_set_up()
                # down arrow decreases cell size
                elif event.key == pygame.K_DOWN:
                    if cell_size > 1:
                        cell_size -= 1
                    level_set_up()
            # create and kill living tiles
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    key = 1
                elif event.button == 3:  # right click
                    key = 3
                elif event.button == 4:  # mouse wheel down
                    if interval_time > 25:
                        interval_time -= 5
                elif event.button == 5:  # mouse wheel up
                    interval_time += 5
            elif event.type == pygame.MOUSEBUTTONUP:
                key = None
        if key in [1, 3]:
            inputs(key)
        # fills screen white so if a tile is killed it will update and turn white
        screen.fill(dead_color)
        pygame.draw.circle(screen, 'dark gray', [width / 2, height / 2], cell_size / 3)
        # draws all living tiles
        for x in range(len(master_list)):
            for y in range(len(master_list[x])):
                if master_list[x][y][0]:
                    pygame.draw.rect(screen, living_color, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))
                # Demonstration (will cause significant slow down)
                if demonstration_mode and master_list[x][y][1]:
                    text = pygame.font.SysFont('arial', int(cell_size / 2)).render(str(master_list[x][y][1]), True, 'white')
                    screen.blit(text, text.get_rect(center=((x+.5) * cell_size, (y + .5) * cell_size)))
        # updates the screen
        pygame.display.flip()
        pygame.key.set_repeat(250, interval_time)


def inputs(key):
    x, y = pygame.mouse.get_pos()
    x //= cell_size
    y //= cell_size
    # updates the main list
    if key == 1:
        t1, t2 = False, True
    else:  # right
        t1, t2 = True, False
    try:
        if master_list[x][y][0] is t1:
            master_list[x][y][0] = t2
            around_l = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1),
                        (x, y + 1), (x + 1, y + 1)]  # all cells around
            for _ in range(len(around_l)):
                around_l[_] = wrap_around(around_l[_])
            if t2:
                living_cells.append((x, y))
                for i in around_l:
                    master_list[i[0]][i[1]][1] += 1
                    living_cells.append(tuple(i))
            else:
                living_cells.remove((x, y))
                for i in around_l:
                    master_list[i[0]][i[1]][1] -= 1
                    living_cells.remove(tuple(i))
    except IndexError:
        pass


def life_death():
    add, sub = [], []
    for x, y in set(living_cells):  # check all the alive cells
        if master_list[x][y][0]:  # the cell is alive and needs to die
            if master_list[x][y][1] not in [2, 3]:
                sub.append([x, y])
        elif master_list[x][y][1] == 3:  # the cell is dead so now check its neighbors
            add.append([x, y])
    change_loop(sub, False)
    change_loop(add, True)


def change_loop(to_change, add):
    for x, y in to_change:
        master_list[x][y][0] = add
        around_l = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1),
                    (x, y + 1), (x + 1, y + 1)]  # all cells around
        for _ in range(len(around_l)):
            around_l[_] = wrap_around(around_l[_])
        if add:
            living_cells.append((x, y))
            for i in around_l:
                living_cells.append(tuple(i))
                master_list[i[0]][i[1]][1] += 1
        else:
            living_cells.remove((x, y))
            for i in around_l:
                living_cells.remove(tuple(i))
                master_list[i[0]][i[1]][1] -= 1


def wrap_around(pos):
    x, y = pos
    if 0 > x:
        x = width // cell_size - 1
    if x >= width // cell_size:
        x = 0
    if 0 > y:
        y = height // cell_size - 1
    if y >= height // cell_size:
        y = 0
    return [x, y]


if __name__ == '__main__':
    main()
