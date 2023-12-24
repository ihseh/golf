from operator import iand
from re import L
from tkinter import CENTER
import arcade
import arcade.gui
import math
# import numpy as np

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
BIKE_SCALE = 0.5
WHEEL_RADIUS = BIKE_SCALE * 75
GROUND = 200

class Bike():
    def __init__(self):
        self.x = 600
        self.y = 500
        self.sprite = arcade.Sprite("sprites/player.png", center_x = self.x, center_y = self.y, scale = BIKE_SCALE)
        self.backWheel = Wheel("back",self.x,self.y)
        self.frontWheel = Wheel("front",self.x,self.y)

class Wheel():
    def __init__(self,type, bikeX, bikeY):
        if type == "front":
            self.x = bikeX + BIKE_SCALE * 165
            self.y = bikeY - BIKE_SCALE * 165
        elif type == "back":
            self.x = bikeX - BIKE_SCALE * 165
            self.y = bikeY - BIKE_SCALE * 165
        self.bikeCenterX = bikeX
        self.bikeCenterY = bikeY

    def touchingRamp(self, ramp): #currently, ramp is an integer representing ground level
        # for i in np.arange(0, 2*math.pi):
        for i in range(0, int(2*math.pi)):
            xCoord = WHEEL_RADIUS * math.cos(i) + self.x
            yCoord = WHEEL_RADIUS * math.sin(i) + self.y
            # print(xCoord,yCoord)
            if yCoord < GROUND:
                return True
        return False

    
class Ramp():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width
        self.height

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)
        self.bike = Bike()
        self.spinLeft = False
        self.spinRight = False
        self.yVel = 0
        self.inAir = True

    def on_draw(self):
        arcade.start_render()
        self.clear()
        arcade.draw_rectangle_filled(center_x = SCREEN_WIDTH/2,center_y = GROUND/2, width = SCREEN_WIDTH, height = GROUND, color = (100,200,50) )#draw ground
        #draw bike
        self.bike.sprite.center_x = self.bike.x
        self.bike.sprite.center_y = self.bike.y
        self.bike.sprite.draw()
        #draw wheel hitboxes
        arcade.draw_circle_filled(center_x = self.bike.backWheel.x, center_y = self.bike.backWheel.y, radius = WHEEL_RADIUS, color = (0,0,255,150))
        arcade.draw_circle_filled(center_x = self.bike.frontWheel.x, center_y = self.bike.frontWheel.y, radius = WHEEL_RADIUS, color = (0,0,255,150))


    def on_update(self, delta_time):        
        #spin bike
        if self.spinLeft:
            self.moveBike(0,0,5)
        elif self.spinRight:
            self.moveBike(0,0,-5)
        #GRAVITY
        #move by yVel if inAir
        if self.inAir:
            self.moveBike(0,self.yVel,0)
            self.yVel -= .1
        #check if touching ramp
        backWheelTouch = self.bike.backWheel.touchingRamp(200)
        frontWheelTouch = self.bike.frontWheel.touchingRamp(200)
        #update inAir if needed
        if backWheelTouch or frontWheelTouch:
            self.inAir = False  
            # print('TOUCH!')

    def moveBike(self, x, y, rot):
        #move bike
        self.bike.x += x
        self.bike.y += y
        self.bike.sprite.angle += rot
        #move wheels
        self.bike.frontWheel.x = self.bike.x + math.sqrt(((BIKE_SCALE*165)**2) *2) * math.cos(math.radians(self.bike.sprite.angle)-math.pi/4)
        self.bike.frontWheel.y = self.bike.y + math.sqrt(((BIKE_SCALE*165)**2) *2) * math.sin(math.radians(self.bike.sprite.angle)-math.pi/4)
        self.bike.backWheel.x = self.bike.x + math.sqrt(((BIKE_SCALE*165)**2) *2) * math.sin(math.radians(self.bike.sprite.angle)-math.pi/4)
        self.bike.backWheel.y = self.bike.y - math.sqrt(((BIKE_SCALE*165)**2) *2) * math.cos(math.radians(self.bike.sprite.angle)-math.pi/4)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
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