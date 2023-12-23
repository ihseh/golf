import arcade
import arcade.gui

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 1000
GROUND = SCREEN_HEIGHT/3

class Golfer():
    pass 

class Ball():
    def __init__(self):
        self.x = 75
        self.y = GROUND + 600
        self.start = True
        
class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)
        self.ball = Ball()
        self.xVel = 0
        self.yVel = 0
        self.launchAngle = 0
        self.inAir = True
    
    def on_draw(self):
        arcade.start_render()
        self.clear()
        arcade.draw_rectangle_filled(center_x = SCREEN_WIDTH/2, center_y = GROUND/2, width = SCREEN_WIDTH, height = GROUND, color = (102,205,0))
        arcade.draw_circle_filled(center_x = self.ball.x, center_y = self.ball.y, radius = 10, color = (255,255,255))
        

    def on_update(self, delta_time):
        self.moveBall()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
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
        
        


        

window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT)

def main():
    gameView = GameView()
    window.show_view(gameView)
    arcade.run()

main()