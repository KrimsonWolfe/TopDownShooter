import arcade
import math

"Top Down Shooter"

"""

TODO:
Sprite Movement
Bullet Shooting
Targets to shoot
Add barrel and barrel rotations
"""

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Topdown"
BULLET_SPEED = 10
PLAYER_MOVEMENT_SPEED = 2.5
TANK_SCALING = 1
TARGET_SCALING = 0.5
SPEED_BONUS = 3
SPEED_BOOST_TIME = 5
TANK_HEALTH = 3
BULLET_UPGRADE_TIME = 10


class Game(arcade.Window):
    """ The Game Class """

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Sprite list
        # self.wall_list = None
        self.bullet_list = None
        self.player_list = None
        self.target_list = None
        self.speed_power_up_list = None
        self.health_power_up_list = None
        self.bullet_upgrade_list = None

        # Player Stuffs
        self.player_sprite = None
        self.barrel_sprite = None
        self.speed_sprite = None
        self.health_sprite = None
        self.bullet_upgrade_sprite = None

        # Background
        # self.background = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Power up
        self.speed_active = False
        self.power_up_timer = 0
        self.upgrade_active = False

    def setup(self):
        """ Fill out the things we initialized """

        # Sprite list
        # self.wall_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.target_list = arcade.SpriteList()
        self.speed_power_up_list = arcade.SpriteList()
        self.health_power_up_list = arcade.SpriteList()
        self.bullet_upgrade_list = arcade.SpriteList()
        # Set up the player sprites
        self.player_sprite = Player("topdowntanks\\PNG\\Tanks\\tankGreen_outline.png", TANK_SCALING)
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 300

        # Setting up the barrel sprite
        self.barrel_sprite = arcade.Sprite("topdowntanks\\PNG\\Tanks\\barrelGreenExtended.png")
        self.barrel_sprite.position = self.player_sprite.position

        # Setting up the sprite
        self.speed_sprite = arcade.Sprite("shooting-gallery-pack\\PNG\\Objects\\shot_blue_large.png")
        self.speed_sprite.center_x = 600
        self.speed_sprite.center_y = 100

        self.health_sprite = arcade.Sprite("shooting-gallery-pack\\PNG\\Objects\\shot_yellow_large.png")
        self.health_sprite.center_x = 200
        self.health_sprite.center_y = 100

        self.bullet_upgrade_sprite = arcade.Sprite("topdowntanks\\PNG\\Bullets\\bulletRed_outline.png")
        self.bullet_upgrade_sprite.center_x = 400
        self.bullet_upgrade_sprite.center_y = 100

        x_start = 100
        for _ in range(7):
            duck = arcade.Sprite("shooting-gallery-pack\\PNG\\Objects\\duck_target_yellow.png", TARGET_SCALING)

            duck.center_x = x_start
            duck.center_y = 400
            self.target_list.append(duck)
            x_start += 100
        self.player_list.append(self.player_sprite)
        self.player_list.append(self.barrel_sprite)
        self.speed_power_up_list.append(self.speed_sprite)
        self.health_power_up_list.append(self.health_sprite)
        self.bullet_upgrade_list.append(self.bullet_upgrade_sprite)
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        # arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        self.bullet_list.draw()
        self.player_list.draw()
        # self.wall_list.draw()
        self.target_list.draw()
        self.speed_power_up_list.draw()
        self.health_power_up_list.draw()
        self.bullet_upgrade_list.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Create Bullet
        bullet = arcade.Sprite("topdowntanks\\PNG\\Bullets\\bulletGreen_outline.png")
        if self.upgrade_active:
            bullet = arcade.Sprite("topdowntanks\\PNG\\Bullets\\bulletRed_outline.png")

        # Position the bullet at the player's current location
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        # Get the mouse angle
        dest_x = x
        dest_y = y

        # SOH CAH TOA angle stuff
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Move the Bullet facing its destination
        bullet.angle = math.degrees(angle) - 90

        # Changes the Bullet Velocity
        bullet.change_x = math.cos(angle) * BULLET_SPEED
        bullet.change_y = math.sin(angle) * BULLET_SPEED

        # Append the Bullets to the list
        self.bullet_list.append(bullet)

    def on_key_press(self, key, modifiers):
        # Movement when key is pressed
        if key in [arcade.key.UP, arcade.key.W]:
            self.up_pressed = True
        elif key in [arcade.key.DOWN, arcade.key.S]:
            self.down_pressed = True
        elif key in [arcade.key.LEFT, arcade.key.A]:
            self.left_pressed = True
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        # Stops movement when key is released
        if key in [arcade.key.UP, arcade.key.W]:
            self.up_pressed = False
        elif key in [arcade.key.DOWN, arcade.key.S]:
            self.down_pressed = False
        elif key in [arcade.key.LEFT, arcade.key.A]:
            self.left_pressed = False
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.right_pressed = False

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        barrel = self.barrel_sprite

        # Get mouse angle
        dest_x = x
        dest_y = y

        # SOH CAH TOA things
        x_diff = dest_x - self.barrel_sprite.center_x
        y_diff = dest_y - self.barrel_sprite.center_y
        angle = math.atan2(y_diff, x_diff)

        # Changes bullet angle
        barrel.angle = math.degrees(angle) - 90

    def bullet_logic(self):
        for bullet in self.bullet_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.target_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.kill()

            # For every coin we hit, add to the score and remove the coin
            for target in hit_list:
                target.kill()

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > self.width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
                bullet.kill()

    def power_up_logic(self, delta_time):
        speed_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.speed_power_up_list)

        for power_up in speed_hit_list:
            power_up.kill()

        global PLAYER_MOVEMENT_SPEED
        global SPEED_BONUS

        if len(speed_hit_list) > 0:
            self.speed_active = True
            PLAYER_MOVEMENT_SPEED = PLAYER_MOVEMENT_SPEED * SPEED_BONUS

        if self.speed_active:
            self.power_up_timer += delta_time
            if self.power_up_timer > SPEED_BOOST_TIME:
                self.speed_active = False
                PLAYER_MOVEMENT_SPEED = PLAYER_MOVEMENT_SPEED / SPEED_BONUS
                self.power_up_timer = 0

        health_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.health_power_up_list)

        for power_up in health_hit_list:
            power_up.kill()

        global TANK_HEALTH

        if len(health_hit_list) > 0:
            TANK_HEALTH = TANK_HEALTH + 1
            if TANK_HEALTH > 3:
                TANK_HEALTH = 3

        bullet_upgrade_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.bullet_upgrade_list)

        for power_up in bullet_upgrade_hit_list:
            power_up.kill()

        if len(bullet_upgrade_hit_list) > 0:
            self.upgrade_active = True

        if self.upgrade_active:
            self.power_up_timer += delta_time
            if self.power_up_timer > BULLET_UPGRADE_TIME:
                self.upgrade_active = False
                self.power_up_timer = 0

    def on_update(self, delta_time: float):

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        self.barrel_sprite.change_x = 0
        self.barrel_sprite.change_y = 0
        self.player_sprite.change_angle = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED * math.sin(self.player_sprite.radians + math.pi / 2)
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED * math.cos(self.player_sprite.radians + math.pi / 2)
            # self.barrel_sprite.change_y = PLAYER_MOVEMENT_SPEED * math.sin(self.player_sprite.radians + math.pi/2)
            # self.barrel_sprite.change_x = PLAYER_MOVEMENT_SPEED * math.cos(self.player_sprite.radians + math.pi/2)
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED * math.sin(self.player_sprite.radians + math.pi / 2)
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED * math.cos(self.player_sprite.radians + math.pi / 2)
            # self.barrel_sprite.change_y = -PLAYER_MOVEMENT_SPEED * math.sin(self.player_sprite.radians + math.pi/2)
            # self.barrel_sprite.change_x = -PLAYER_MOVEMENT_SPEED * math.cos(self.player_sprite.radians + math.pi/2)

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_angle = 3
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_angle = -3

        self.barrel_sprite.position = self.player_sprite.position

        self.bullet_logic()
        self.power_up_logic(delta_time)

        # Update the player and bullet lists
        self.player_list.update()
        self.bullet_list.update()


class Player(arcade.Sprite):
    def __init__(self, *args):
        super().__init__(*args)
        self.fuel = 100

    def update(self):

        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += self.change_angle

        # Stops from moving off of the screen
        if self.left < 5:
            self.left = 5
        elif self.right > SCREEN_WIDTH - 5:
            self.right = SCREEN_WIDTH - 5

        if self.bottom < 5:
            self.bottom = 5
        elif self.top > SCREEN_HEIGHT - 5:
            self.top = SCREEN_HEIGHT - 5


def main():
    window = Game()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
