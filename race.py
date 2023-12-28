from operator import iand
from re import L
from tkinter import CENTER, YView
from turtle import back, backward
import arcade
import arcade.gui
import math
import numpy as np

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
BIKE_SCALE = 0.4
WHEEL_RADIUS = BIKE_SCALE * 75
HEAD_RADIUS = BIKE_SCALE * 95
GROUND = 200
GRAVITY = .2
X_ACCELERATION_RATE = .8
ANGULAR_ROTATION_RATE = .4

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

    def crash(self, ramp):
        minY = 1000
        for i in np.arange(0, 2*math.pi):
            xCoord = self.headX + HEAD_RADIUS * math.cos(i)
            yCoord = self.headY + HEAD_RADIUS * math.sin(i)
            if yCoord < minY:
                minY = yCoord
        if minY <= ramp:
            return True
        else:
            return False



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
        minY = 1000
        for i in np.arange(0, 2*math.pi):
        # for i in range(0, int(2*math.pi)):
            xCoord = WHEEL_RADIUS * math.cos(i) + self.x
            yCoord = WHEEL_RADIUS * math.sin(i) + self.y
            if yCoord < minY:
                minY = yCoord
        if minY <= ramp + 2:
            return ramp - minY
        else:
            return None

    
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
        self.moveLeft = False
        self.moveRight = False
        #PHYSICS VARIABLES
        self.yVel = 0
        self.xVel = 0
        self.angVel = 0
        self.inAir = True
        self.onGround = False
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
        arcade.draw_circle_filled(center_x = self.bike.headX, center_y = self.bike.headY, radius = HEAD_RADIUS, color = (220,220,220,150))

    def on_update(self, delta_time):
        #spin bike from user input
        self.setAngVel()
        self.moveBike(0,0,self.angVel)
        #move bike in x from user input 
        self.setXVel()
        self.moveBike(self.xVel,0,0)
        #check if touching ramp and update variables
        backWheelTouch = self.bike.backWheel.touchingRamp(200)
        frontWheelTouch = self.bike.frontWheel.touchingRamp(200)
        #move bike to surface
        if backWheelTouch:
            self.moveBike(0,backWheelTouch,0)
        elif frontWheelTouch: #elif to bike doesn't move twice if it lands flat
            self.moveBike(0,frontWheelTouch,0)
        #update inAir and onGround
        if backWheelTouch or frontWheelTouch:
            self.inAir = False
            self.onGround = True
        #update flat
        if backWheelTouch and frontWheelTouch:
            self.flat = True
            self.yVel = 0
        #MOVE BIKE
        #If in air
        if self.inAir:
            self.moveBike(0,self.yVel,0)
            self.yVel -= GRAVITY
        #if on ground
        if self.onGround == True and self.flat == False: #only one wheel is on the ground
            if backWheelTouch: #wheel on the ground is the back wheel. 
                if self.bike.x >= self.bike.backWheel.x: #if bike is leaning more forward than back
                    self.moveBike(0,self.yVel,0)
                    while(self.bike.backWheel.touchingRamp(199)):
                        self.moveBike(0,0,-.1)
                    self.yVel -= GRAVITY
                elif self.bike.x < self.bike.backWheel.x: #if bike is leaning more back than forward
                    self.moveBike(0,self.yVel,0)
                    while(self.bike.backWheel.touchingRamp(199)):
                        self.moveBike(0,0,.1)
                    self.yVel -= GRAVITY
            if frontWheelTouch: #wheel on the ground is the front wheel
                if self.bike.x <= self.bike.frontWheel.x: #if bike is leaning more back than forward
                    self.moveBike(0,self.yVel,0)
                    while(self.bike.frontWheel.touchingRamp(199)):
                        self.moveBike(0,0,.1)
                    self.yVel -= GRAVITY
                elif self.bike.x > self.bike.frontWheel.x: #if bike is leaning more forward than back
                    self.moveBike(0,self.yVel,0)
                    while(self.bike.frontWheel.touchingRamp(199)):
                        self.moveBike(0,0,-.1)
                    self.yVel -= GRAVITY

        # print("back = " + str(backWheelTouch))
        # print("front = " + str(frontWheelTouch))
        # print("flat = " + str(self.flat))
        # print("yVel = " + str(self.yVel))
        # print("inAir = " + str(self.inAir))
        # print("self.bike.y = " + str(self.bike.y))

    def moveBike(self, dx, dy, dRot):
        # print("moveBike called with dx = " + str(dx) + ", dy = " + str(dy) + ", dRot = " + str(dRot))
        #move bike by delta x
        self.bike.x += dx
        #move bike by delta y, ensuring that center never passes below center y coordinate when flat
        if self.bike.y + dy < 736.919320599735375 * BIKE_SCALE and self.bike.sprite.angle < 45 and self.bike.sprite.angle > -45:
            self.bike.y = 736.919320599735375 * BIKE_SCALE #THIS NUMBER DOESN'T WORK FOR DIFFERENT VALUES OF BIKE SCALE
        elif not self.bike.crash(200):
            self.bike.y += dy #TODO: yVel keeps decreasing if bike crashes
        #rotate bike
        self.bike.sprite.angle += dRot

        #update wheels
        self.bike.frontWheel.x = self.bike.x + math.sqrt(((BIKE_SCALE*165)**2) *2) * math.cos(math.radians(self.bike.sprite.angle)-math.pi/4)
        self.bike.frontWheel.y = self.bike.y + math.sqrt(((BIKE_SCALE*165)**2) *2) * math.sin(math.radians(self.bike.sprite.angle)-math.pi/4)
        self.bike.backWheel.x = self.bike.x + math.sqrt(((BIKE_SCALE*165)**2) *2) * math.sin(math.radians(self.bike.sprite.angle)-math.pi/4)
        self.bike.backWheel.y = self.bike.y - math.sqrt(((BIKE_SCALE*165)**2) *2) * math.cos(math.radians(self.bike.sprite.angle)-math.pi/4)
        #update head
        self.bike.headX = self.bike.x + math.sqrt(((BIKE_SCALE*50)**2) + ((BIKE_SCALE*140)**2) ) * math.cos(math.radians(self.bike.sprite.angle)+math.pi/2.6)
        self.bike.headY = self.bike.y + math.sqrt(((BIKE_SCALE*50)**2) + ((BIKE_SCALE*140)**2) ) * math.sin(math.radians(self.bike.sprite.angle)+math.pi/2.6)

    def putBikeInAir(self):
        self.bike.y = 800
        self.bike.sprite.angle = 0
        self.yVel = 0
        self.onGround = False
        self.flat = False
        self.inAir = True

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        if key == arcade.key.LEFT:
            self.spinLeft = True
        if key == arcade.key.RIGHT:
            self.spinRight = True
        if key == arcade.key.SPACE:
            self.putBikeInAir()
        if key == arcade.key.D:
            self.moveRight = True
        if key == arcade.key.A:
            self.moveLeft = True
    
    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.LEFT:
            self.spinLeft = False
        if key == arcade.key.RIGHT:
            self.spinRight = False
        if key == arcade.key.D:
            self.moveRight = False
        if key == arcade.key.A:
            self.moveLeft = False

    def setAngVel(self):
        if self.spinLeft: #spin left
            self.angVel += ANGULAR_ROTATION_RATE
        elif self.angVel > 0:
            if self.angVel - ANGULAR_ROTATION_RATE > 0:
                self.angVel -= ANGULAR_ROTATION_RATE
            else:
                self.angVel = 0
        if self.spinRight: #spin right
            self.angVel -= ANGULAR_ROTATION_RATE
        elif self.angVel < 0:
            if self.angVel + ANGULAR_ROTATION_RATE < 0:
                self.angVel += ANGULAR_ROTATION_RATE
            else:
                self.angVel = 0
    
    def setXVel(self):
        if self.moveLeft: #move left
            self.xVel -= X_ACCELERATION_RATE
        elif self.xVel < 0:
            if self.xVel + X_ACCELERATION_RATE < 0:
                self.xVel += X_ACCELERATION_RATE
            else:
                self.xVel = 0
        if self.moveRight: #move right
            self.xVel += X_ACCELERATION_RATE
        elif self.xVel > 0:
            if self.xVel - X_ACCELERATION_RATE > 0:
                self.xVel -= X_ACCELERATION_RATE
            else:
                self.xVel = 0

window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT)

def main():
    gameView = GameView()
    window.show_view(gameView)
    arcade.run()

main()