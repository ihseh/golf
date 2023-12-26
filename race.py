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

FRICTION = 0

class Bike():
    def __init__(self):
        self.x = 600
        self.y = 650
        self.sprite = arcade.Sprite("sprites/player.png", center_x = self.x, center_y = self.y, scale = BIKE_SCALE)
        self.backWheel = Wheel("back",self.x,self.y)
        self.frontWheel = Wheel("front",self.x,self.y)
        self.headX = self.x + BIKE_SCALE * 50
        self.headY = self.y + BIKE_SCALE * 140

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
            if yCoord < ramp:
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

        #BIKE INSTANCE
        self.bike = Bike()
        #INPUT VARIABLES
        self.spinLeft = False
        self.spinRight = False
        #PHYSICS VARIABLES
        self.yVel = 0
        self.inAir = True
        self.flat = False

    def on_draw(self):
        arcade.start_render()
        self.clear()
        arcade.draw_rectangle_filled(center_x = SCREEN_WIDTH/2,center_y = GROUND/2, width = SCREEN_WIDTH, height = GROUND, color = (100,200,50) )#draw ground
        #draw bike
        self.bike.sprite.center_x = self.bike.x
        self.bike.sprite.center_y = self.bike.y
        self.bike.sprite.draw()
        #draw wheel hitboxes
        arcade.draw_circle_filled(center_x = self.bike.backWheel.x, center_y = self.bike.backWheel.y, radius = WHEEL_RADIUS, color = (220,220,220,150))
        arcade.draw_circle_filled(center_x = self.bike.frontWheel.x, center_y = self.bike.frontWheel.y, radius = WHEEL_RADIUS, color = (220,220,220,150))
        #draw head hitbox
        arcade.draw_circle_filled(center_x = self.bike.headX, center_y = self.bike.headY, radius = BIKE_SCALE * 95, color = (220,220,220,150))

    def on_update(self, delta_time):
        #spin bike
        if self.spinLeft:
            self.moveBike(0,0,5)
        elif self.spinRight:
            self.moveBike(0,0,-5)
        
        #PHYSICS

        #Gravity: move by yVel if inAir
        if self.inAir:
            self.moveBike(0,self.yVel,0)
            self.yVel -= .2
            # self.yVel = self.yVel * 1.1 #also an option

        #check if touching ramp
        backWheelTouch = self.bike.backWheel.touchingRamp(200)
        frontWheelTouch = self.bike.frontWheel.touchingRamp(200)
        #update inAir if needed
        if backWheelTouch or frontWheelTouch:
            self.inAir = False
        #update flat
        if backWheelTouch and frontWheelTouch:
            self.flat = True

    
    def moveBike(self, dx, dy, dRot):
        #move bike
        self.bike.x += dx
        self.bike.y += dy
        self.bike.sprite.angle += dRot

        #update wheels
        self.bike.frontWheel.x = self.bike.x + math.sqrt(((BIKE_SCALE*165)**2) *2) * math.cos(math.radians(self.bike.sprite.angle)-math.pi/4)
        self.bike.frontWheel.y = self.bike.y + math.sqrt(((BIKE_SCALE*165)**2) *2) * math.sin(math.radians(self.bike.sprite.angle)-math.pi/4)
        self.bike.backWheel.x = self.bike.x + math.sqrt(((BIKE_SCALE*165)**2) *2) * math.sin(math.radians(self.bike.sprite.angle)-math.pi/4)
        self.bike.backWheel.y = self.bike.y - math.sqrt(((BIKE_SCALE*165)**2) *2) * math.cos(math.radians(self.bike.sprite.angle)-math.pi/4)
        #update head
        self.bike.headX = self.bike.x + math.sqrt(((BIKE_SCALE*50)**2) + ((BIKE_SCALE*140)**2) ) * math.cos(math.radians(self.bike.sprite.angle)+math.pi/2.6)
        self.bike.headY = self.bike.y + math.sqrt(((BIKE_SCALE*50)**2) + ((BIKE_SCALE*140)**2) ) * math.sin(math.radians(self.bike.sprite.angle)+math.pi/2.6)

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