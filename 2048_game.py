from ion import keydown, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_BACKSPACE, KEY_OK
from kandinsky import draw_string, fill_rect
from random import choice, random
from time import sleep

class Screen: palette = {"Background" : (255, 255, 255), "PrimaryColor" : (0, 0, 0), "PrimaryText" : (0, 200, 200), "SecondaryText" : (255, 255, 255)}

class Cube:
    style = {2:"grey", 4:"cyan", 8:"blue", 16:"purple", 32:"pink", 64:"magenta", 128:"red", 256:"orange", 512:"yellow", 1024:"green", 2048:"brown"}
    def __init__(self, x, y, nbr=2): self.x, self.y, self.nbr = x, y, nbr

    def draw(self, pos_x, pos_y, taille, espace):
        fill_rect(pos_x+self.x*(taille+espace),pos_y+self.y*(taille+espace),taille, taille, Cube.style[self.nbr])
        draw_string(str(self.nbr),pos_x+self.x*(taille+espace)+2,pos_y+self.y*(taille+espace) + int(taille/2)-8,"black", Cube.style[self.nbr])

class Matrice:
    def __init__(self, N=4): self.N = N ; self.cubes = [[Cube(x, y, 2 if random() <= 0.85 else 4) for y in range(self.N)] for x in range(self.N)]

    def __getitem__(self, ij): return self.cubes[ij]

    def __len__(self): 
        n = 0
        for x in range(self.N):
            for y in range(self.N): n = n + 1 if self[x][y] != None else n + 0
        return n

    def __iter__(self): iterator = [] ; liste = [[iterator.append(self[x][y]) for y in range(self.N)] for x in range(self.N)] ; del liste ; return iter(iterator)

    def getNumberMove(self, cube, ind):
        if ind == "UP":
            m = cube.y
            if cube.y != 0:
                while True:
                    m -= 1
                    if self[cube.x][m] != None: 
                        if self[cube.x][m].nbr != cube.nbr: m += 1
                        break
                    elif m == 0: break
            return cube.y - m
        elif ind == "DOWN":
            m = cube.y
            if cube.y + 1 != self.N:
                while True:
                    m += 1
                    if self[cube.x][m] != None:
                        if self[cube.x][m].nbr != cube.nbr: m -= 1
                        break
                    elif m + 1 == self.N: break
            return abs(cube.y - m)
        elif ind == "LEFT":
            m = cube.x
            if cube.x != 0:
                while True:
                    m -= 1
                    if self[m][cube.y] != None:
                        if self[m][cube.y].nbr != cube.nbr: m += 1
                        break
                    elif m == 0: break
            return cube.x - m
        elif ind == "RIGHT":
            m = cube.x
            if cube.x + 1 != self.N:
                while True:
                    m += 1
                    if self[m][cube.y] != None:
                        if self[m][cube.y].nbr != cube.nbr: m -= 1
                        break
                    elif m + 1 == self.N: break
            return abs(cube.x - m)

    def move_cube(self, cube, ind, check=False):
        m, change = self.getNumberMove(cube, ind), False
        if ind == "UP":
            if m != 0: new_cube = Cube(cube.x, cube.y-m, cube.nbr*2 if self[cube.x][cube.y-m] != None else cube.nbr)
            else: new_cube = cube ; change = True
            if not check: self[cube.x][cube.y] = None ; self[cube.x][cube.y-m] = new_cube            
        elif ind == "DOWN":
            if m != 0: new_cube = Cube(cube.x, cube.y+m, cube.nbr*2 if self[cube.x][cube.y+m] != None else cube.nbr)
            else: new_cube = cube ; change = True
            if not check: self[cube.x][cube.y] = None ; self[cube.x][cube.y+m] = new_cube
        elif ind == "LEFT":
            if m != 0: new_cube = Cube(cube.x-m, cube.y, cube.nbr*2 if self[cube.x-m][cube.y] != None else cube.nbr)
            else: new_cube = cube ; change = True
            if not check: self[cube.x][cube.y] = None ; self[cube.x-m][cube.y] = new_cube
        elif ind == "RIGHT":
            if m != 0: new_cube = Cube(cube.x+m, cube.y, cube.nbr*2 if self[cube.x+m][cube.y] != None else cube.nbr)
            else: new_cube = cube ; change = True
            if not check: self[cube.x][cube.y] = None ; self[cube.x+m][cube.y] = new_cube
        return change

    def move_cubes(self, ind):
        if ind == "UP" or ind == "LEFT":
            for cube in self:
                if cube != None: self.move_cube(cube, ind)
        elif ind == "DOWN" or ind == "RIGHT":
            for x in range(self.N-1, -1, -1):
                for y in range(self.N-1, -1, -1):
                    if self[x][y] != None: self.move_cube(self[x][y], ind)

    def draw_cubes(self, pos_x, pos_y, taille, espace):
        fill_rect(pos_x, pos_y, self.N*(taille+espace)-espace, self.N*(taille+espace)-espace, Screen.palette["Background"])
        for cube in self:
            if cube != None: cube.draw(pos_x, pos_y, taille, espace)

    def getNoneAndReplace(self):
        if len(self) != self.N*self.N:
            nones = [] ; liste = [[nones.append(Cube(x,y,2 if random() <= 0.85 else 4)) for y in range(self.N) if self[x][y] is None] for x in range(self.N)]
            new_cube = choice(nones) ; self[new_cube.x][new_cube.y] = new_cube ; del nones, liste

    def check(self):
        n = 0
        for cube in self:
            if cube != None:
                for ind in ["UP", "DOWN", "LEFT", "RIGHT"]:
                    if self.move_cube(cube, ind, True): n += 1
        cube_2048 = False
        for cube in self: 
            if cube != None:
                if cube.nbr == 2048: cube_2048 = True
        if cube_2048: return "WIN"
        if n / 4 == self.N * self.N: return "LOSE"

class GUI:
    nbr_cubes = 4
    speed = 0.2
    color_mode = "light"
    @staticmethod
    def clean(): fill_rect(0, 0, 320, 222, Screen.palette["Background"])
    class Menu:
        @staticmethod
        def draw():
            def draw_curseur(curseur):
                if curseur == "start":
                    draw_string("  settings        ", 92, 130, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
                    draw_string(">  start  <", 105, 100, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
                elif curseur == "settings":
                    draw_string("  start        ", 105, 100, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
                    draw_string(">  settings  <", 92, 130, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            GUI.clean()
            draw_string("Game 2048", 105, 50, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            draw_string("  start  ", 105, 100, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            draw_string("  settings  ", 92, 130, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            curseur = "start"
            while True:
                if keydown(KEY_UP) or keydown(KEY_DOWN): curseur = "settings" if curseur == "start" else "start" ; draw_curseur(curseur) ; sleep(0.2)
                if keydown(KEY_OK) and curseur == "start": game = GUI.Game(GUI.nbr_cubes) ; game.draw() ; break
                if keydown(KEY_OK) and curseur == "settings": GUI.Setting.draw() ; break
    class Game:
        def __init__(self, N=4): self.matrice = Matrice(N)# ; self.matrice[0][0] = Cube(0,0,2048)
        def draw(self, pos_x=65, pos_y=23, taille=48, espace=1):
            def check():
                if self.matrice.check() == "WIN": draw_string("You Win", 130, 2, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
                elif self.matrice.check() == "LOSE": draw_string("Game Over", 120, 2, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            def update(ind): self.matrice.move_cubes(ind) ; self.matrice.getNoneAndReplace() ; self.matrice.draw_cubes(pos_x, pos_y, taille, espace) ; sleep(GUI.speed)
            GUI.clean()
            fill_rect(pos_x-2, pos_y-2, self.matrice.N*(taille+espace)+3,self.matrice.N*(taille+espace)+3, Screen.palette["PrimaryColor"])
            fill_rect(pos_x-1, pos_y-1, self.matrice.N*(taille+espace)+1,self.matrice.N*(taille+espace)+1, Screen.palette["Background"])
            self.matrice.draw_cubes(pos_x, pos_y, taille, espace)
            while True:
                if keydown(KEY_UP): check() ; update("UP")
                if keydown(KEY_DOWN): check() ; update("DOWN")
                if keydown(KEY_LEFT): check() ; update("LEFT")
                if keydown(KEY_RIGHT): check() ; update("RIGHT")
                if keydown(KEY_BACKSPACE): GUI.Menu.draw() ; break
    class Setting:
        @staticmethod
        def draw():
            def draw_speed(v,curs): draw_string("   "+str(round(v, 2))+"   " if not curs else ">  "+str(round(v, 2))+"  <", 200, 80, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            def draw_color_mode(mode,curs): draw_string("    "+mode+"    " if not curs else ">  "+mode+"  <  ", 190, 110, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            def change_color(mode):
                if mode == "light": Screen.palette["Background"] = (255,255,255) ; Screen.palette["PrimaryText"] = (0,200,200) ;Screen.palette["SecondaryText"] = (255,255,255) ; Screen.palette["PrimaryColor"] = (0,0,0)
                elif mode == "dark": Screen.palette["Background"] = (80,80,100) ; Screen.palette["PrimaryText"] = (255,255,255) ; Screen.palette["SecondaryText"] = (80,80,100) ; Screen.palette["PrimaryColor"] = (255,255,255)
            GUI.clean()
            draw_string("Settings", 110, 30, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            draw_string("speed", 25, 80, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            draw_string("color mode", 25, 110, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            curseur  = "speed"
            draw_speed(GUI.speed, True) ; draw_color_mode(GUI.color_mode, False)
            while True:
                if curseur == "speed" and keydown(KEY_RIGHT) and round(GUI.speed, 2) != 1: GUI.speed += 0.1 ; draw_speed(GUI.speed, True) ; sleep(0.15)
                if curseur == "speed" and keydown(KEY_LEFT) and round(GUI.speed, 2) != 0: GUI.speed -= 0.1 ; draw_speed(GUI.speed, True) ; sleep(0.15)
                if curseur == "color mode" and keydown(KEY_RIGHT): GUI.color_mode = "light" if GUI.color_mode == "dark" else "dark" ; draw_color_mode(GUI.color_mode,True) ; sleep(0.15)
                if curseur == "color mode" and keydown(KEY_LEFT): GUI.color_mode = "light" if GUI.color_mode == "dark" else "dark" ; draw_color_mode(GUI.color_mode,True) ; sleep(0.15)
                if keydown(KEY_UP) or keydown(KEY_DOWN): curseur = "color mode" if curseur == "speed" else "speed" ; sleep(0.15) ; draw_speed(GUI.speed, True if curseur == "speed" else False) ; draw_color_mode(GUI.color_mode, True if curseur == "color mode" else False)
                if keydown(KEY_BACKSPACE): change_color(GUI.color_mode) ; GUI.clean() ; GUI.Menu.draw() ; break
    @staticmethod
    def main(): GUI.Menu.draw()

GUI.main()