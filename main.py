import arcade
import arcade.gui

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

class Golfer():
    pass

class Ball():
    pass

class GameView(arcade.View):

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)

    
    def on_draw(self):
        pass
    

    def on_update(self, delta_time):
        pass


    def on_key_press(self, key, key_modifiers):
        pass


window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT)

def main():
    gameView = GameView()
    window.show_view(gameView)
    arcade.run()

main()