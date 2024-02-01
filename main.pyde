# FIREBOY AND WATERGIRL BY NISA SHAHID(NS5376) AND KRISTINA SISIAKOVA(KS6261)
# CS-UH 1001 Section 001: Final Group Project 


add_library('minim')
import os

path = os.getcwd()
RESOLUTION_W = 800
RESOLUTION_H = 600
GROUND = 580
player = Minim(this)

#create the stationary platforms
class Platform:
    
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
    def display(self):
        fill(30,30,30)
        stroke(30,30,30)
        rect(self.x, self.y,self.w,self.h)
        
#create the moving platforms
class MovingPlatform:
    
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vx = 3
        
        if self.x <= 270: 
            self.x_lim_left = x - 1
            self.x_lim_right = 270 
        elif self.x >= 420:  
            self.x_lim_left = 420 - 1
            self.x_lim_right = RESOLUTION_W - 110
            
    #get the platforms to move in between defined points    
    def update(self):
        
        if self.x >= self.x_lim_right:
            self.vx *= - 1
        elif self.x <= self.x_lim_left:
            self.vx *= - 1
            
        self.x += self.vx
    
    def display(self):
        self.update()
        fill(30,30,30)
        stroke(30,30,30)
        rect(self.x, self.y, self.w, self.h)
        
#parent class for the players
class Player:
    
    def __init__(self, x, y, r, img, img_w, img_h, slices):
        self.x = x
        self.y = y
        self.r = r
        self.ground = GROUND
        self.vx = 0
        self.vy = 0
        self.img = loadImage(path + "/images/" + img)
        self.img_w = img_w
        self.img_h = img_h
        self.slices = slices
        self.slice = 0
        self.dir = RIGHT
        self.win = False
        self.eat_sound = player.loadFile(path + "/sounds/sd_0.mp3")
        self.jump_sound = player.loadFile(path + "/sounds/jump_01.mp3")
        self.puddle_sound = player.loadFile(path + "/sounds/puddle_sound.mp3")
        
    #get the players to move downwards towards the ground if they do not encounter a platform    
     
    def gravity(self):
        if self.y +self.r <= self.ground:
            self.vy += 0.5
            if self.y + self.r + self.vy > self.ground:
                self.vy = self.ground - (self.y+self.r)
        else:
            self.vy = 0
        
            
        for platform in game.platforms:
            if self.y + self. r <= platform.y and self.x >= platform.x and self.x <= platform.x + platform.w:
                self.ground = platform.y
                return

            else:
                self.ground = GROUND
                
        for platform in game.moving_platforms:
            if self.y + self.r <= platform.y and self.x >= platform.x and self.x <= platform.x + platform.w :
                print("w")
                self.ground = platform.y - 23
                #self.x = platform.x
            else:
                self.ground = GROUND
                return
    
    #make the player move after calculating coordinates       
     
    def update(self):
        # self.gravity()
        self.x += self.vx
        self.y += self.vy
        self.gravity()

                            
                    
    #calculate distance between a player and a diamond            
    def distance(self, other):
        if isinstance(other, Diamond):
            return (((self.x + self.img_w/2) - other.x)**2 + ((self.y - self.img_h/2) - other.y)**2)**0.5
        
    #display player image according to its movement and direction using image slicing and cropping
    def display(self):
        self.update()
        if self.dir == RIGHT:
            image(self.img, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
        elif self.dir == LEFT:
            image(self.img, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w, self.img_h, (self.slice + 1) * self.img_w, 0, self.slice * self.img_w, self.img_h)

#one of the players
class Fireboy(Player):
    
    def __init__(self, x, y, r):
        Player.__init__(self, x, y, r, "fireboy_sprite.png", 32, 45, 6)
        self.key_handler = {LEFT:False, RIGHT:False, UP:False}
        self.alive = True
        self.dir = LEFT
        self.score = 0
    
    # define the way the fireboy moves according to keyboard input    
    def update(self):
        self.gravity()
        
        if self.key_handler[LEFT] == True:
            self.vx = -5
            self.dir = LEFT
        elif self.key_handler[RIGHT] == True:
            self.vx = 5
            self.dir = RIGHT
        else:
            self.vx = 0
        
        if self.key_handler[UP] == True and self.y + self.r == self.ground:
            self.jump_sound.rewind()
            self.jump_sound.play()
            self.vy = - 10

        self.x += self.vx
        self.y += self.vy
        
        if frameCount % 5 == 0 and self.vx != 0 and self.vy == 0:
            self.slice = (self.slice + 1) % self.slices
        elif self.vx == 0:
            self.slice = 3
            
        # screen boundary and the middle separator limits
        if self.x - self.r <= 0:
            self.x = self.r
        if self.x + self.r > 800:
            self.x = 800 - self.r
        if self.x < 380:
            if self.x + self.r > 380 and self.y <= 390:
                self.x = 380 - self.r
        if self.x > 420:
            if self.x - self.r <= 420 and self.y <= 390 :
                self.x = 420 + self.r
        
        #check if player collides with diamond
        for diamond in game.red_diamonds:
            if self.distance(diamond) <= self.img_w:
                self.eat_sound.rewind()
                self.eat_sound.play()
                game.red_diamonds.remove(diamond)
                self.score += 1
    #check if player steps on a puddle that kills it
    def puddle_collide(self):
        for puddle in game.green_puddles:
            if self.x <= puddle.x+puddle.w:
                if self.x >= puddle.x:
                    if self.y + self.img_h == puddle.y + 23:
                        self.alive = False
                        break
        for puddle in game.blue_puddles:
            if self.x <= puddle.x+puddle.w:
                if self.x >= puddle.x:
                    if self.y + self.img_h == puddle.y + 23:
                        self.alive = False
                        break
   #check if plahyer reaches their door
    def check_win(self):
        for door in game.doors:
            if self.x <= door.x + door.w:
                if self.x >= door.x:
                    if self.y >= door.y:
                        if self.y <= door.y + door.h:
                            if door.type == "red":
                                self.win = True
                                break
    
    # call to check player demise and win
    def check(self):
        self.puddle_collide()
        self.check_win()
        if self.alive == False:
            self.puddle_sound.play()
            
#class for watergirl
class Watergirl(Player):
    def __init__(self, x, y, r):
        Player.__init__(self, x, y, r, "watergirl_sprite.png", 41, 45, 5)
        self.key_handler = {LEFT:False, RIGHT:False, UP:False}
        self.alive = True
        self.score = 0

    def update(self):
        self.gravity()
        
        if self.key_handler[LEFT] == True:
            self.vx = - 5
            self.dir = LEFT
        elif self.key_handler[RIGHT] == True:
            self.vx = 5
            self.dir = RIGHT
        else:
            self.vx = 0
        
        if self.key_handler[UP] == True and self.y + self.r == self.ground:
            self.jump_sound.rewind()
            self.jump_sound.play()
            self.vy = -10

        self.x += self.vx
        self.y += self.vy
        
        if frameCount % 5 == 0 and self.vx != 0 and self.vy == 0:
            self.slice = (self.slice + 1) % self.slices
        elif self.vx == 0:
            self.slice = 3
        
        # screen boundary and middle separator limits
        if self.x - self.r <= 0:
            self.x = self.r
        if self.x + self.r > 800:
            self.x = 800 - self.r
        if self.x > 420:
            if self.x - self.r <= 420 and self.y <= 390 :
                self.x = 420 + self.r
        if self.x < 380:
            if self.x + self.r > 380 and self.y <= 390:
                self.x = 380 - self.r
                
        for diamond in game.blue_diamonds:
            if self.distance(diamond) <= self.img_w:
                self.eat_sound.rewind()
                self.eat_sound.play()
                game.blue_diamonds.remove(diamond)
                self.score += 1
            
    def puddle_collide(self):
        for puddle in game.green_puddles:
            if self.x <= puddle.x+puddle.w:
                if self.x >= puddle.x:
                    if self.y + self.img_h == puddle.y + 23:
                        self.alive = False
                        return
        for puddle in game.red_puddles:
            if self.x <= puddle.x+puddle.w:
                if self.x >= puddle.x:
                    if self.y + self.img_h == puddle.y + 23:
                        self.alive = False
                        return
    def check_win(self):
        for door in game.doors:
            if self.x <= door.x + door.w:
                if self.x >= door.x:
                    if self.y >= door.y:
                        if self.y <= door.y + door.h:
                            if door.type == "blue":
                                self.win = True
                                break
                        
    def check(self):
        self.puddle_collide()
        self.check_win()
        if self.alive == False:
            self.puddle_sound.play()
        
#display dimaonds according to color
class Diamond:
    
    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.c = c
        self.img_red = loadImage(path + "/images/" + "diamond_1.png")
        self.img_blue= loadImage(path + "/images/" + "diamond_2.png")
    
    def display(self):
        if self.c == "red":
            image(self.img_red, self.x - 20, self.y)
        elif self.c == "blue":
            image(self.img_blue, self.x - 40, self.y)

# display puddle according to color
class Puddle:
    def __init__(self, x, y, w, h, type):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.type = type
        
    def display(self):
        if self.type == "green":
            fill(0,125,0)
            stroke(0,125,0)
            rect(self.x, self.y,self.w,self.h)
        elif self.type == "red":
            fill(255,69,0)
            stroke(255,69,0)
            rect(self.x, self.y,self.w,self.h)
        elif self.type == "blue":
            fill(135,206,250)
            stroke(135,206,250)
            rect(self.x, self.y,self.w,self.h)

#display door according to color
class Door:
    def __init__(self, x, y, w, h, type):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.type = type
    
    def display(self):
        if self.type == "red":
            fill(255,69,0)
            stroke(0, 0, 0)
            rect(self.x, self.y, self.w, self.h)
        elif self.type == "blue":
            fill(135,206,250)
            stroke(0, 0, 0)
            rect(self.x, self.y, self.w, self.h)

# main class            
class Game:
    
    def __init__(self):
        self.w = RESOLUTION_W
        self.h = RESOLUTION_H
        self.ground= GROUND
        self.fireboy = Fireboy(350, 0, 22)
        self.watergirl =  Watergirl(450, 0, 22)
        self.start_up = True
        self.bg_sound = player.loadFile(path+ "/sounds/background_sound.mp3")
        self.start_img = loadImage(path + "/images/background2.png")
        
        # background
        self.bg_image = loadImage(path + "/images/background.png")
        
        # doors
        self.doors = []
        self.doors.append(Door(320, 20, 50, 60, "blue"))
        self.doors.append(Door(430, 20, 50, 60, "red"))                 
        
        # diamonds
        self.red_diamonds = []
        self.blue_diamonds = []
        self.red_diamonds.append(Diamond(40, 60, "red"))
        self.blue_diamonds.append(Diamond(40, 470, "blue"))
        self.red_diamonds.append(Diamond(330, 270, "red"))
        self.blue_diamonds.append(Diamond(760, 60, "blue"))
        self.red_diamonds.append(Diamond(760, 470, "red"))
        self.blue_diamonds.append(Diamond(480, 275, "blue"))
        

        # plaforms and puddles
        self.platforms = []
        self.green_puddles = []
        self.red_puddles = []
        self.blue_puddles =[]
        self.moving_platforms =[]
        
        self.green_puddles.append(Puddle(0, 580, 800, 20,"green")) # big puddle on the bottom
        self.platforms.append(Platform(230, 80, 150, 30)) # 1. platform left
        self.platforms.append(Platform(420, 80, 150, 30)) # 1. platform right
        self.platforms.append(Platform(0, 150, 160, 30)) # 2. platform left - with the puddle on top
        self.red_puddles.append(Puddle(0, 150, 80, 10,"red")) 
        self.platforms.append(Platform(650, 150, 160, 30)) # 2. platform right - with the puddle on top
        self.blue_puddles.append(Puddle(720, 150, 80, 10,"blue")) 
        self.platforms.append(Platform(230, 220, 80, 30)) # 3. platform left
        self.platforms.append(Platform(490, 220, 80, 30)) # 3. platform right
        self.platforms.append(Platform(110, 290, 80, 30)) # 4. platform left
        self.platforms.append(Platform(610, 290, 80, 30)) # 4. platform right
        self.platforms.append(Platform(0, 420, 110, 30)) # 5. platform left
        self.platforms.append(Platform(690, 420, 110, 30)) # 5. platform right
        self.platforms.append(Platform(230, 360, 160, 30)) # 6. platform left - with the puddle on top
        self.blue_puddles.append(Puddle(300, 360, 80, 10,"blue")) # puddle on top of the 6. platform left
        self.platforms.append(Platform(420, 360, 160, 30)) # 6. platform right - with the puddle on top
        self.red_puddles.append(Puddle(420, 360, 80, 10,"red")) # puddle on top of the 6. platform right
        
        self.platforms.append(Platform(380, 0, 40, 390)) # big separator in the middle
        self.platforms.append(Platform(380, 520, 40, 100)) # small separator in the middle


        self.moving_platforms.append(MovingPlatform(0, 520, 110, 30)) # moving platform left 
        self.moving_platforms.append(MovingPlatform(420, 520, 110, 30)) # moving platform right
    
    #function to display main menu with instructions
    def display_start_screen(self):
        image(self.start_img,0,0)
        
        # instructions
        fill(220, 220, 220)
        stroke(0,0,0)
        rect(140, 470, 520, 120)
        strokeWeight(3)
        
        fill(0, 0, 0)
        textSize(12)
        text("Fireboy and Watergirl compete against each other in a race to their corresponding door", 147, 490)
        text(" -blue door for the Watergirl, red door for the Fireboy. During the race, they must avoid", 143, 508)
        text("green puddles which kill them. In addition each player must avoid the puddles of the ", 147, 526)
        text("opposite color. If one player dies, the other player automatically wins.",147,544)
        text("They collect diamonds to increase their score - Watergirl collects the blue diamonds", 147, 562)
        text("and Fireboy the red ones. If both players survive, the player with a higher score wins.", 147, 580)
        
        fill(220, 220, 220)
        stroke(0,0,0)
        rect(10, 10, 300, 70)
        strokeWeight(3)
        fill(0, 0, 0)
        textSize(15)
        text("MOVEMENT OF PLAYERS", 15,30)
        text("FIREBOY: LEFT, RIGHT, UP ARROW KEYS", 15, 45)
        text("WATERGIRL: a, d, w KEYS", 15, 60)
        fill(220, 220, 220)
        stroke(0,0,0)
        rect(580, 10,200,70)
        strokeWeight(3)
        fill(0, 0, 0)
        textSize(15)
        text("Press 'f' for background ", 590,30)
        text("music and 'v' to turn it", 590,50)
        text("off.", 590, 70)
    
                     
        # play button
        fill(220, 220, 220)
        rect(343, 245, 100, 47)
        strokeWeight(3)
        
        fill(0, 0, 0)
        textSize(28)
        text("Play", 365, 280)
        # print(mouseX, mouseY)
        
        #if mouse presses play button game starts
        if mouseX>=343 and mouseX<=443 and mouseY>=245 and mouseY<=292:
            if mousePressed:
                self.start_up = False

                
    def display(self):
        
        # check if players die
        self.fireboy.check()
        self.watergirl.check()
        if self.fireboy.win == True and self.watergirl.win == True:
            if self.fireboy.score >= self.watergirl.win:
                #display the score and who won
                image(self.start_img,0,0)
                fill(255,127,80)
                stroke(0,0,0)
                rect(250, 200, 300, 120)
                strokeWeight(3)
                fill(0, 0, 0)
                textSize(16)
                text("Fireboy wins as his score is greater!", 261, 221)
                text("Fireboy: " + str(game.fireboy.score), 355, 265)
                text("Watergirl: " + str(game.watergirl.score), 350, 243)
                text("Click to play again", 325,287)
                return
            elif self.watergirl.score >= self.fireboy.score:
                image(self.start_img,0,0)
                fill(135,206,250)
                stroke(0,0,0)
                rect(250, 200, 300, 120)
                strokeWeight(3)
                fill(0, 0, 0)
                textSize(16)
                text("Watergirl wins as her score is greater!", 261, 221)
                text("Watergirl: " + str(game.watergirl.score), 350, 243)
                text("Fireboy: " + str(game.fireboy.score), 355, 265)
                text("Click to play again", 325, 287)
                return
            elif self.fireboy.score == self.watergirl.score:
                image(self.start_img,0,0)
                fill(135,206,250)
                stroke(0,0,0)
                rect(300, 200, 200, 100)
                strokeWeight(3)
                fill(0, 0, 0)
                textSize(16)
                text("It is a Tie!", 340, 221)
                text("Watergirl: " + str(game.watergirl.score), 350, 243)
                text("Fireboy: " + str(game.fireboy.score), 355, 265)
                text("Click to play again", 325, 287)
                return
        elif self.fireboy.alive == False or self.watergirl.win == True:
            image(self.start_img,0,0)
            fill(135,206,250)
            stroke(0,0,0)
            rect(300, 200, 200, 100)
            strokeWeight(3)
            fill(0, 0, 0)
            textSize(16)
            text("Watergirl wins!", 340, 221)
            text("Watergirl: " + str(game.watergirl.score), 350, 243)
            text("Fireboy: " + str(game.fireboy.score), 355, 265)
            text("Click to play again", 325, 287)
            return
        elif self.fireboy.win == True or self.watergirl.alive == False:
            image(self.start_img,0,0)
            fill(255,127,80)
            stroke(0,0,0)
            rect(300, 200, 200, 100)
            strokeWeight(3)
            fill(0, 0, 0)
            textSize(16)
            text("Fireboy wins!", 345, 221)
            text("Fireboy: " + str(game.fireboy.score), 355, 265)
            text("Watergirl: " + str(game.watergirl.score), 350, 243)
            text("Click to play again", 325, 287)
            return
       
        
        # display background
        image(self.bg_image, 0, 0, RESOLUTION_W, RESOLUTION_H)

        # display doors
        for door in self.doors:
            door.display()
    
        # display platforms and puddles
        for platform in self.platforms:
            platform.display()
        for platform in self.moving_platforms:
            platform.display()
        for puddle in self.green_puddles:
            puddle.display()
        for puddle in self.blue_puddles:
            puddle.display()
        for puddle in self.red_puddles:
            puddle.display()
        # display diamonds
        for diamond in self.red_diamonds:
            diamond.display()
        for diamond in self.blue_diamonds:
            diamond.display()
        #display score on left and right corners
        fill(220, 220, 220)
        textSize(20)
        text("Fireboy: " + str(game.fireboy.score), 10, 20)
        fill(220, 220, 220)
        textSize(20)
        text("Watergirl: " + str(game.watergirl.score), 680, 20)
        
        # display players
        self.fireboy.display()
        self.watergirl.display()

game = Game()

def setup():
    size(RESOLUTION_W, RESOLUTION_H)
    background(255,255,255)

def draw():
    if  game.start_up == True:
        game.display_start_screen()
    elif game.start_up == False:
        game.display()

def keyPressed():
    #background music
    if key == "f":
        game.bg_sound.loop()
    if key == "v":
        game.bg_sound.pause()
    # FireBoy
    if keyCode == LEFT:
        game.fireboy.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.fireboy.key_handler[RIGHT] = True
    elif keyCode == UP:
        game.fireboy.key_handler[UP] = True
        
    # WaterGirl
    if key == 'a':
        game.watergirl.key_handler[LEFT] = True
    elif key == 'd':
        game.watergirl.key_handler[RIGHT] = True
    elif key == 'w':
        game.watergirl.key_handler[UP] = True

def keyReleased():
    # FireBoy
    if keyCode == LEFT:
        game.fireboy.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.fireboy.key_handler[RIGHT] = False
    elif keyCode == UP:
        game.fireboy.key_handler[UP] = False
        
    # WaterGirl
    if key == 'a':
        game.watergirl.key_handler[LEFT] = False
    elif key == 'd':
        game.watergirl.key_handler[RIGHT] = False
    elif key == 'w':
        game.watergirl.key_handler[UP] = False

def mouseClicked():
    #restart game once it ends
    global game
    if game.fireboy.alive == False or game.watergirl.alive == False:
        game = Game()
        
    if game.fireboy.win == True or game.watergirl.win == True:
        game = Game()
    


    
        
