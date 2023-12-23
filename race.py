import arcade
import arcade.gui
import math

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 900
BIKE_SCALE = 0.5


class Bike():
    def __init__(self):
        self.x = 600
        self.y = 500
        self.sprite = arcade.Sprite("sprites/player.png", center_x = self.x, center_y = self.y, scale = BIKE_SCALE)
        self.backWheel = Wheel("back",self.x,self.y)
        self.frontWheel = Wheel("front",self.x,self.y)

class Wheel():
    def __init__(self,type, bikeX, bikeY):
        # self.sprite = arcade.Sprite()
        if type == "front":
            self.x = bikeX + BIKE_SCALE * 165
            self.y = bikeY - BIKE_SCALE * 165
        elif type == "back":
            self.x = bikeX - BIKE_SCALE * 165
            self.y = bikeY - BIKE_SCALE * 165

        

    def isOnRamp(self):
        pass

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)
        self.bike = Bike()
        self.spinLeft = False
        self.spinRight = False

    def on_draw(self):
        arcade.start_render()
        self.clear()
        self.bike.sprite.draw() #draw bike
        #draw wheels
        backX = self.bike.x + math.sqrt(((BIKE_SCALE*165)**2) *2) * math.sin(math.radians(self.bike.sprite.angle)-math.pi/4)
        backY = self.bike.y - math.sqrt(((BIKE_SCALE*165)**2) *2) * math.cos(math.radians(self.bike.sprite.angle)-math.pi/4)
        frontX = self.bike.x + math.sqrt(((BIKE_SCALE*165)**2) *2) * math.cos(math.radians(self.bike.sprite.angle)-math.pi/4)
        frontY = self.bike.y + math.sqrt(((BIKE_SCALE*165)**2) *2) * math.sin(math.radians(self.bike.sprite.angle)-math.pi/4)
        arcade.draw_circle_filled(center_x = backX, center_y = backY, radius = BIKE_SCALE * 75, color = (0,0,255,150)) #back wheel hitbox
        arcade.draw_circle_filled(center_x = frontX, center_y = frontY, radius = BIKE_SCALE * 75, color = (0,0,255,150)) #front wheel hitbox
    
    def on_update(self, delta_time):
        if self.spinLeft:
            self.bike.sprite.angle -= 5
        elif self.spinRight:
            self.bike.sprite.angle += 5

        

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.LEFT:
            self.spinLeft = True
        if key == arcade.key.RIGHT:
            self.spinRight = True
    
    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.LEFT:
            self.spinLeft = False
        if key == arcade.key.RIGHT:
            self.spinRight = False



window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT)

def main():
    gameView = GameView()
    window.show_view(gameView)
    arcade.run()

main()