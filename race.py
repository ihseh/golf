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
BIKE_SCALE = .5
WHEEL_RADIUS = BIKE_SCALE * 75
HEAD_RADIUS = BIKE_SCALE * 95
GROUND = 200
GRAVITY = .2
X_ACCELERATION_RATE = .8
ANGULAR_ROTATION_RATE = .4
FRICTION = 0

class Box():
    def __init__(self, centerX = None, centerY = None, width = None, height = None, bottomLeftX = None, bottomRightX = None, bottomY = None):
        self.height = height
        if centerX and centerY: #instantiate using centerX, centerY, width, height
            self.centerX = centerX
            self.centerY = centerY
            self.width = width
            self.top = self.centerY + self.height/2
            self.bottom = self.centerY - self.height/2
            self.left = self.centerX - self.width/2
            self.right = self.centerX + self.width/2
        elif bottomLeftX: #instantiate using bottomLeftX, bottomRightX, height, bottomY
            self.width = bottomRightX -bottomLeftX
            self.left = bottomLeftX
            self.right = bottomRightX
            self.top = bottomY + height
            self.bottom = bottomY
            self.centerX = self.left + self.width/2
            self.centerY = self.bottom + self.height/2
        elif width: #instantiate using centerX, bottomY, height, width
            self.width = width
            self.bottom = bottomY
            self.top = self.bottom + height
            self.centerX = centerX
            self.centerY = self.bottom + height/2
            self.left = self.centerX - self.width/2
            self.right = self.centerX + self.width/2

class Kicker():
    def __init__(self, centerX = None, centerY = None, width = None, height = None, reversed: bool = None, bottomY = None, bottomLeftX = None, bottomRightX = None):
        if centerX and centerY: # instantiate using centerX, centerY, width, height
            self.centerX = centerX
            self.centerY = centerY
            self.width = width
            self.height = height
        elif bottomLeftX: #instantiate using bottomLeftX, bottomRightX, height, bottomY
            self.height = height
            self.width = bottomRightX - bottomLeftX
            self.bottom = bottomY
            self.centerX = bottomLeftX + self.width/2
            self.centerY = self.bottom + self.height/2
        elif width: #instantiate using centerX, bottomY, height, width
            self.height = height
            self.width = width
            self.bottom = bottomY
            self.centerX = centerX
            self.centerY = bottomY + self.height/2
        self.slope = self.height/self.width

        if reversed: #flip ramp around
            pass

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
            self.crashed = True
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

    def touchingGround(self, ground):
        minY = 1000
        for i in np.arange(0, 2*math.pi):
        # for i in range(0, int(2*math.pi)):
            # xCoord = WHEEL_RADIUS * math.cos(i) + self.x
            yCoord = WHEEL_RADIUS * math.sin(i) + self.y
            if yCoord < minY:
                minY = yCoord
        if minY <= ground + 2:
            return ground - minY
        else:
            return None
        
    def touchingBox(self, box):
        for i in np.arange(0,2*math.pi):
            xCoord = WHEEL_RADIUS * math.cos(i) + self.x
            yCoord = WHEEL_RADIUS * math.sin(i) + self.y
            if (xCoord <= box.centerX and xCoord >= box.left) or (xCoord >= box.centerX and xCoord <= box.right):
                if (yCoord <= box.centerY and yCoord >= box.bottom) or (yCoord >= box.centerY and yCoord <= box.top):
                    return (box.right - xCoord,box.top-yCoord)
        return False

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)
        #BIKE INSTANCE
        self.bike = Bike()
        self.wheels = [self.bike.frontWheel,self.bike.backWheel]
        #RAMPS
        self.boxes = []
        self.boxes.append(Box(width = 100, height=50, bottomY=200, centerX = 150))
        self.kickers = []
        # self.kickers.append(Kicker(centerX = 800, height = 200, width = 100, bottomY = 200))
        #INPUT VARIABLES
        self.spinLeft = False
        self.spinRight = False
        self.moveLeft = False
        self.moveRight = False
        #PHYSICS VARIABLES
        self.yVel = 0
        self.xVel = 0
        self.angVel = 0
        self.state = "inAir" #inAir, oneWheelTouch, flat, crashed

    def on_update(self, delta_time):
        #check if touching ramp and update variables
        backWheelTouch = self.bike.backWheel.touchingGround(200)
        frontWheelTouch = self.bike.frontWheel.touchingGround(200)
        #spin bike from user input
        self.setAngVel()
        self.moveBike(0,0,self.angVel)
        #move bike in x from user input
        if backWheelTouch is not None:
            self.setXVel()
            self.moveBike(self.xVel,0,0)
        #move bike to surface
        self.moveToSurface(backWheelTouch,frontWheelTouch)
        #set bike state
        self.setState(frontWheelTouch,backWheelTouch)
        #apply forces due to gravity and contact with ground
        self.doPhysics(backWheelTouch,frontWheelTouch)
        #toggle command line output for debugging
        # self.printData(backWheelTouch,frontWheelTouch)
        #check collision with box
        self.boxCollisionX()
        
    def boxCollisionX(self):
        for box in self.boxes:
                backWheelTouchingBox = self.bike.backWheel.touchingBox(box)
                if backWheelTouchingBox:
                    self.xVel = 0
                    self.moveLeft = False
                    self.moveRight = False
                    self.moveBike(backWheelTouchingBox[0],0,0)

    def moveToSurface(self,backWheelTouch,frontWheelTouch):
        if backWheelTouch is not None:
            self.moveBike(0,backWheelTouch,0)
        elif frontWheelTouch is not None: #elif so bike doesn't move twice if it lands flat
            self.moveBike(0,frontWheelTouch,0)

    def setState(self, backWheelTouch, frontWheelTouch):
        if self.bike.crash(200):
            self.state = "crashed"
        else:
            if backWheelTouch is not None and frontWheelTouch is not None: #both wheels on ground
                self.state = "flat"
            elif backWheelTouch is not None or frontWheelTouch is not None: #one wheel on ground
                self.state = "oneWheelTouch"
            else: #no wheels on ground - bike is in air
                self.state = "inAir"

    def doPhysics(self, backWheelTouch, frontWheelTouch):
        #in air 
        if self.state == "inAir":
            self.moveBike(0,self.yVel,0)
            self.yVel -= GRAVITY
        #touching ground with one wheel
        if self.state == "oneWheelTouch": #only one wheel is on the ground, still in freefall
            if not (self.spinLeft or self.spinRight): #if user is not applying rotational force. THIS IS BUGGY
                if backWheelTouch is not None: #wheel on the ground is the back wheel. 
                    if self.bike.x >= self.bike.backWheel.x: #if bike is leaning more forward than back
                        self.moveBike(0,self.yVel,0)
                        while(self.bike.backWheel.touchingGround(199)):
                            self.moveBike(0,0,-.1)
                        self.yVel -= GRAVITY
                    elif self.bike.x < self.bike.backWheel.x: #if bike is leaning more back than forward
                        self.moveBike(0,self.yVel,0)
                        while(self.bike.backWheel.touchingGround(199)):
                            self.moveBike(0,0,.1)
                        self.yVel -= GRAVITY
                if frontWheelTouch is not None: #wheel on the ground is the front wheel
                    if self.bike.x <= self.bike.frontWheel.x: #if bike is leaning more back than forward
                        self.moveBike(0,self.yVel,0)
                        while(self.bike.frontWheel.touchingGround(199)):
                            self.moveBike(0,0,.1)
                        self.yVel -= GRAVITY
                    elif self.bike.x > self.bike.frontWheel.x: #if bike is leaning more forward than back
                        self.moveBike(0,self.yVel,0)
                        while(self.bike.frontWheel.touchingGround(199)):
                            self.moveBike(0,0,-.1)
                        self.yVel -= GRAVITY
        #flat
        if self.state == "flat":
            self.yVel = 0
        #crashed
        if self.state == "crashed":
            self.yVel = 0

    def moveBike(self, dx, dy, dRot):
        # print("moveBike called with dx = " + str(dx) + ", dy = " + str(dy) + ", dRot = " + str(dRot))
        #move bike by delta x
        self.bike.x += dx
        #move bike by delta y, ensuring that center never passes below center y coordinate when flat
        if self.bike.y + dy < (GROUND + WHEEL_RADIUS + (BIKE_SCALE * 165)) and self.bike.sprite.angle < 45 and self.bike.sprite.angle > -45:
            self.bike.y = (GROUND + WHEEL_RADIUS + (BIKE_SCALE * 165))
        elif not self.bike.crash(200):
            self.bike.y += dy
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

    def setAngVel(self):
        #subtract excess angle
        self.subtractExcessAngle()
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

    def putBikeInAir(self):
        self.bike.y = 800
        self.bike.sprite.angle = 0
        self.yVel = 0
        self.state = "inAir"

    def subtractExcessAngle(self):
        if self.bike.sprite.angle > 360:
            self.bike.sprite.angle -= 360
        elif self.bike.sprite.angle < -360:
            self.bike.sprite.angle += 360

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

    def on_draw(self):
        arcade.start_render()
        self.clear()
        #draw ground
        arcade.draw_rectangle_filled(center_x = SCREEN_WIDTH/2,center_y = GROUND/2, width = SCREEN_WIDTH, height = GROUND, color = (100,200,50) )
        #draw bike
        self.bike.sprite.center_x = self.bike.x
        self.bike.sprite.center_y = self.bike.y
        self.bike.sprite.draw()
        #draw wheel hitboxes
        arcade.draw_circle_filled(center_x = self.bike.backWheel.x, center_y = self.bike.backWheel.y, radius = WHEEL_RADIUS, color = (220,220,220,150))
        arcade.draw_circle_filled(center_x = self.bike.frontWheel.x, center_y = self.bike.frontWheel.y, radius = WHEEL_RADIUS, color = (220,220,220,150))
        #draw head hitbox
        arcade.draw_circle_filled(center_x = self.bike.headX, center_y = self.bike.headY, radius = HEAD_RADIUS, color = (220,220,220,150))
        #draw dot in center
        arcade.draw_circle_filled(center_x = self.bike.x, center_y = self.bike.y, radius = 10, color = (0,0,255))
        #draw ramps
        for box in self.boxes:
            arcade.draw_rectangle_filled(center_x = box.centerX, center_y = box.centerY, width = box.width, height = box.height, color = (0,0,255))
        for kicker in self.kickers:
            arcade.draw_triangle_filled(kicker.centerX - kicker.width/2, kicker.centerY - kicker.height/2, kicker.centerX + kicker.width/2, kicker.centerY - kicker.height/2, kicker.centerX + kicker.width/2, kicker.centerY + kicker.height/2, (0,0,255))

    def printData(self, backWheelTouch, frontWheelTouch):
        print("backWheelTouch: " + str(backWheelTouch))
        print("frontWheelTouch: " + str(frontWheelTouch))
        print("state: " + str(self.state))
        print("bike.y: " + str(self.bike.y))
        print("yVel: " + str(self.yVel))
        print("angle: " + str(self.bike.sprite.angle))

window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT)

def main():
    gameView = GameView()
    window.show_view(gameView)
    arcade.run()

main()