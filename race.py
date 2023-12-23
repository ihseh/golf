import arcade
import arcade.gui

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 1000

class Player():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.sprite = arcade.Sprite("sprites/player.png", center_x = 300, center_y = 300, scale = .3)
        self.backWheel = Wheel()
        self.frontWheel = Wheel()

class Wheel():
    def __init__(self, x, y, type):
        # self.sprite = arcade.Sprite()
        pass

    def isOnRamp(self):
        pass

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)
        self.player = Player()

    def on_draw(self):
        arcade.start_render()
        self.clear()
        self.player.sprite.draw()

    
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