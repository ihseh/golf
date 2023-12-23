import arcade
import arcade.gui

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 1000
GROUND = SCREEN_HEIGHT/3
FLAG_HEIGHT = 150

class Golfer():
    pass 

class Ball():
    def __init__(self):
        self.x = 75
        self.y = GROUND + 600
        self.start = True
        print("1")
        
class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        # sky
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)
        self.ball = Ball()
        self.xVel = 0
        self.yVel = 0
        self.launchAngle = 0
        self.inAir = True
    
    def on_draw(self):
        arcade.start_render()
        self.clear()
        # ground
        arcade.draw_rectangle_filled(center_x = SCREEN_WIDTH/2, center_y = GROUND/2, width = SCREEN_WIDTH, height = GROUND, color = (102,205,0))
        # golf ball
        arcade.draw_circle_filled(center_x = self.ball.x, center_y = self.ball.y, radius = 10, color = (255,255,255))
        # pole
        arcade.draw_rectangle_filled(center_x = 1000, center_y = GROUND + FLAG_HEIGHT/2, width = 2, height = FLAG_HEIGHT, color = (255,255,255))
        # flag
        arcade.draw_triangle_filled(x1 = 1000, y1 = GROUND + FLAG_HEIGHT, x2 = 1050, y2 = GROUND + FLAG_HEIGHT - 25, x3 = 1000, y3 = GROUND + FLAG_HEIGHT - 50, color = (255,0,0))


        

    def on_update(self, delta_time):
        self.moveBall()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            if self.inAir is True:
                pass
            else:
                self.stroke()

    def stroke(self):
        launchAngle = 45
        self.xVel = 10
        self.yVel = 25
        self.inAir = True
        self.ball.start = False


    def moveBall(self):
        # movement of ball in air
        if self.inAir:
            self.yVel -=1

        if self.ball.y + self.yVel < GROUND:
            self.ball.y = GROUND + 6 
            self.yVel = 0
            self.inAir = False
        else:
            self.ball.y += self.yVel

        self.ball.x += self.xVel

        # movement of ball on ground
        if not self.ball.start and self.ball.y == GROUND + 6:
            if self.xVel > 0: 
                self.xVel -= 0.5
            else:
                self.xVel = 0
        # ball movement if it hits flag
        if self.ball.x >= 1000 and self.ball.y in range(0, 1000):
            # self.xVel = 0
            # self.yVel -= 1
            print("hi")

        
        


        

window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT)

def main():
    gameView = GameView()
    window.show_view(gameView)
    arcade.run()

main()