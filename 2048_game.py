from ion import keydown, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_BACKSPACE, KEY_OK
from kandinsky import draw_string, fill_rect
from random import choice, random
from time import sleep

class Screen: palette = {"Background" : (255,255,255), "PrimaryColor" : (0,0,0), "PrimaryText" : (0,200,200), "SecondaryText" : (255,255,255)}

class Cube:
    style = {2:(204,238,255), 4:(102,170,178), 8:(51,136,140), 16:(0,102,102), 32:(85,153,68), 64:(142,187,45), 128:(179,210,30), 256:(255,255,0), 512:(255,127,0), 1024:(255,64,0), 2048:(255,0,0)}
    def __init__(self, x, y, nbr=2): self.x, self.y, self.nbr = x, y, nbr

    def draw(self, pos_x, pos_y, taille, espace):
        fill_rect(pos_x+self.x*(taille+espace),pos_y+self.y*(taille+espace),taille, taille, Cube.style[self.nbr])
        draw_string(str(self.nbr),pos_x+self.x*(taille+espace)+2,pos_y+self.y*(taille+espace) + int(taille/2)-8,"black", Cube.style[self.nbr])

class Matrice:
    def __init__(self, N=4): self.N, self.score = N, 0 ; self.cubes = [[Cube(x, y, 2 if random() <= 0.85 else 4) for y in range(self.N)] for x in range(self.N)]
    def __getitem__(self, ij): return self.cubes[ij]
    def __len__(self): return self.N * self.N - sum([ligne.count(None) for ligne in self.cubes])
    def __iter__(self): return (self[x][y] for y in range(self.N) for x in range(self.N))

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
            if m != 0 and not check: self.score += cube.nbr*2 if self[cube.x][cube.y-m] != None else 0
            if m != 0: new_cube = Cube(cube.x, cube.y-m, cube.nbr*2 if self[cube.x][cube.y-m] != None else cube.nbr)
            else: new_cube = cube ; change = True
            if not check: self[cube.x][cube.y] = None ; self[cube.x][cube.y-m] = new_cube
        elif ind == "DOWN":
            if m != 0 and not check: self.score += cube.nbr*2 if self[cube.x][cube.y+m] != None else 0
            if m != 0: new_cube = Cube(cube.x, cube.y+m, cube.nbr*2 if self[cube.x][cube.y+m] != None else cube.nbr)
            else: new_cube = cube ; change = True
            if not check: self[cube.x][cube.y] = None ; self[cube.x][cube.y+m] = new_cube
        elif ind == "LEFT":
            if m != 0 and not check: self.score += cube.nbr*2 if self[cube.x-m][cube.y] != None else 0
            if m != 0: new_cube = Cube(cube.x-m, cube.y, cube.nbr*2 if self[cube.x-m][cube.y] != None else cube.nbr)
            else: new_cube = cube ; change = True
            if not check: self[cube.x][cube.y] = None ; self[cube.x-m][cube.y] = new_cube
        elif ind == "RIGHT":
            if m != 0 and not check: self.score += cube.nbr*2 if self[cube.x+m][cube.y] != None else 0
            if m != 0: new_cube = Cube(cube.x+m, cube.y, cube.nbr*2 if self[cube.x+m][cube.y] != None else cube.nbr)
            else: new_cube = cube ; change = True
            if not check: self[cube.x][cube.y] = None ; self[cube.x+m][cube.y] = new_cube
        return change

    def move_cubes(self, ind):
        if ind == "UP" or ind == "LEFT":
            for cube in self: self.move_cube(cube, ind) if cube != None else None
        elif ind == "DOWN" or ind == "RIGHT":
            for x in range(self.N-1, -1, -1):
                for y in range(self.N-1, -1, -1): self.move_cube(self[x][y], ind) if self[x][y] != None else None

    def draw_cubes(self, pos_x, pos_y, taille, espace):
        fill_rect(pos_x, pos_y, self.N*(taille+espace)-espace, self.N*(taille+espace)-espace, Screen.palette["Background"])
        for cube in self: cube.draw(pos_x, pos_y, taille, espace) if cube != None else None

    def getNoneAndReplace(self):
        if len(self) != self.N*self.N: new_cube = choice([Cube(x,y,2 if random() <= 0.85 else 4) for y in range(self.N) for x in range(self.N) if self[x][y] is None]) ; self[new_cube.x][new_cube.y] = new_cube

    def check(self):
        if 2048 in [cube.nbr for cube in self if cube != None]: return "WIN"
        elif sum([sum([1 for ind in ["UP", "DOWN", "LEFT", "RIGHT"] if self.move_cube(cube, ind, True)]) for cube in self if cube != None]) / 4 == self.N * self.N: return "LOSE"

class Curseur:
    def __init__(self, *args, default=""): self.args, self.sens, self.default = args, "R", default
    def __next__(self): self.N += 1 if self.sens == "R" else -1 ; self.check() ; self.curs = self.args[self.N] ; return self.curs
    def __iter__(self): self.curs, self.N = self.default, self.args.index(self.default) if self.default != ""  else -1 ; return self
    def check(self):
        if self.N > len(self.args)-1: self.N = 0
        elif self.N < 0: self.N = len(self.args)-1

class GUI:
    nbr_cubes, speed, color_mode = 4, 0.2, "light"
    @staticmethod
    def clean(): fill_rect(0, 0, 320, 222, Screen.palette["Background"])
    class Menu:
        @staticmethod
        def draw():
            def draw_curseur(curseur):
                if curseur == "start":
                    draw_string("  settings        ", 92, 130, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
                    draw_string("  graphics        ", 92, 160, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
                    draw_string(">  start  <", 105, 100, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
                elif curseur == "settings":
                    draw_string("  start        ", 105, 100, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
                    draw_string("  graphics        ", 92, 160, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
                    draw_string(">  settings  <", 92, 130, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
                elif curseur == "graphics":
                    draw_string("  start        ", 105, 100, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
                    draw_string("  settings        ", 92, 130, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
                    draw_string(">  graphics  <", 92, 160, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            GUI.clean() ; GUI.Menu.C = iter(Curseur("start", "settings", "graphics"))
            draw_string("Game 2048", 105, 50, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            draw_string("  start  ", 105, 100, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            draw_string("  settings  ", 92, 130, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            draw_string("  graphics  ", 92, 160, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            while True:
                if keydown(KEY_UP): GUI.Menu.C.sens = "L" ; next(GUI.Menu.C) ; draw_curseur(GUI.Menu.C.curs) ; sleep(0.15)
                if keydown(KEY_DOWN): GUI.Menu.C.sens = "R" ; next(GUI.Menu.C) ; draw_curseur(GUI.Menu.C.curs) ; sleep(0.15)
                if keydown(KEY_OK) and GUI.Menu.C.curs == "start": game = GUI.Game(GUI.nbr_cubes) ; game.draw() ; break
                if keydown(KEY_OK) and GUI.Menu.C.curs == "settings": GUI.Setting.draw() ; break
                if keydown(KEY_OK) and GUI.Menu.C.curs == "graphics": GUI.Graph.draw() ; break
    class Game:
        def __init__(self, N=4): self.matrice = Matrice(N)# ; self.matrice[0][0] = Cube(0,0,2048)

        def draw(self, pos_x=100, pos_y=23, taille=48, espace=1):
            def check():
                if self.matrice.check() == "WIN": draw_string("You Win", 162, 2, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
                elif self.matrice.check() == "LOSE": draw_string("Game Over", 152, 2, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            def update(ind): self.matrice.move_cubes(ind) ; self.matrice.getNoneAndReplace() ; self.matrice.draw_cubes(pos_x, pos_y, taille, espace) ; sleep(GUI.speed) ; draw_string(str(self.matrice.score),8,80,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
            GUI.clean()
            draw_string("Score :",14,50,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
            draw_string(str(self.matrice.score),8,80,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
            fill_rect(pos_x-2, pos_y-2, self.matrice.N*(taille+espace)+3,self.matrice.N*(taille+espace)+3, Screen.palette["PrimaryColor"])
            fill_rect(pos_x-1, pos_y-1, self.matrice.N*(taille+espace)+1,self.matrice.N*(taille+espace)+1, Screen.palette["Background"])
            self.matrice.draw_cubes(pos_x, pos_y, taille, espace)
            while True:
                if keydown(KEY_UP): check() ; update("UP")
                if keydown(KEY_DOWN): check() ; update("DOWN")
                if keydown(KEY_LEFT): check() ; update("LEFT")
                if keydown(KEY_RIGHT): check() ; update("RIGHT")
                if keydown(KEY_BACKSPACE): GUI.Graph.list_score.append(self.matrice.score) ; GUI.Menu.draw() ; break
    class Setting:
        @staticmethod
        def draw():
            def draw_curseur(curseur):
                if curseur == "speed":
                    draw_string(">  "+str(GUI.speed)+"  <    ", 200, 80, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
                    draw_string("    "+GUI.color_mode+"        ", 180, 110, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
                elif curseur == "color mode":
                    draw_string("   "+str(GUI.speed)+"       ", 200, 80, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
                    draw_string(">   "+GUI.color_mode+"   <    ", 180, 110, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            def change_color(mode):
                if mode == "light": Screen.palette["Background"] = (255,255,255) ; Screen.palette["PrimaryText"] = (0,200,200) ;Screen.palette["SecondaryText"] = (255,255,255) ; Screen.palette["PrimaryColor"] = (0,0,0)
                elif mode == "dark": Screen.palette["Background"] = (80,80,100) ; Screen.palette["PrimaryText"] = (255,255,255) ; Screen.palette["SecondaryText"] = (80,80,100) ; Screen.palette["PrimaryColor"] = (255,255,255)
            GUI.clean() ; GUI.Setting.C = iter(Curseur("speed", "color mode")) ; GUI.Setting.C_speed = iter(Curseur(0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1, default=GUI.speed)) ; GUI.Setting.C_color_mode = iter(Curseur("light", "dark", default=GUI.color_mode))
            draw_string("Settings", 110, 30, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            draw_string("speed", 25, 80, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            draw_string("color mode", 25, 110, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            draw_string("   "+str(GUI.speed)+"       ", 200, 80, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            draw_string("    "+GUI.color_mode+"        ", 180, 110, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            while True:
                if GUI.Setting.C.curs == "speed" and keydown(KEY_RIGHT): GUI.Setting.C_speed.sens = "R" ; next(GUI.Setting.C_speed) ; GUI.speed = GUI.Setting.C_speed.curs ; draw_curseur(GUI.Setting.C.curs) ; sleep(0.15)
                if GUI.Setting.C.curs == "speed" and keydown(KEY_LEFT): GUI.Setting.C_speed.sens = "L" ; next(GUI.Setting.C_speed) ; GUI.speed = GUI.Setting.C_speed.curs ; draw_curseur(GUI.Setting.C.curs) ; sleep(0.15)
                if GUI.Setting.C.curs == "color mode" and keydown(KEY_RIGHT): GUI.Setting.C_color_mode.sens = "R" ; next(GUI.Setting.C_color_mode) ; GUI.color_mode = GUI.Setting.C_color_mode.curs ; draw_curseur(GUI.Setting.C.curs) ; sleep(0.15)
                if GUI.Setting.C.curs == "color mode" and keydown(KEY_LEFT): GUI.Setting.C_color_mode.sens = "L" ; next(GUI.Setting.C_color_mode) ; GUI.color_mode = GUI.Setting.C_color_mode.curs ; draw_curseur(GUI.Setting.C.curs) ; sleep(0.15)
                if keydown(KEY_UP): GUI.Setting.C.sens = "L" ; next(GUI.Setting.C) ; draw_curseur(GUI.Setting.C.curs) ; sleep(0.15)
                if keydown(KEY_DOWN): GUI.Setting.C.sens = "R" ; next(GUI.Setting.C) ; draw_curseur(GUI.Setting.C.curs) ; sleep(0.15)
                if keydown(KEY_BACKSPACE): change_color(GUI.color_mode) ; GUI.clean() ; GUI.Menu.draw() ; break
    class Graph:
        list_score = [0]
        @staticmethod
        def draw():
            GUI.clean()
            draw_string("Graphics", 120, 20, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            draw_string("Maximum Score : "+str(max(GUI.Graph.list_score)), 15, 200, Screen.palette["PrimaryText"], Screen.palette["SecondaryText"])
            fill_rect(10,0,1,222,Screen.palette["PrimaryColor"]);fill_rect(0,196,320,1,Screen.palette["PrimaryColor"])
            for n, bar in enumerate(GUI.Graph.list_score): fill_rect(10+n*(3+2),195,3,round(-bar/103),Screen.palette["PrimaryColor"])
            while True:
                if keydown(KEY_BACKSPACE): GUI.Menu.draw() ; break
    @staticmethod
    def main(): GUI.Menu.draw()

GUI.main()