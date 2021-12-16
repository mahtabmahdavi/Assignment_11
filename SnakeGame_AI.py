import random
import math
import arcade


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500


class Snake(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 16
        self.height = 16
        self.color = arcade.color.GREEN
        self.change_x = 0
        self.change_y = 0
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.score = 0
        self.speed = 4
        self.body = []


    def move(self):
        self.body.append([self.center_x, self.center_y])

        if len(self.body) > self.score:
            self.body.pop(0)
        
        if self.change_x > 0:
            self.center_x += self.speed
        elif self.change_x < 0:
            self.center_x -= self.speed

        if self.change_y > 0:
            self.center_y += self.speed
        elif self.change_y < 0:
            self.center_y -= self.speed


    def eat(self, food):
        if food == "apple":
            self.score += 1
        elif food == "pear":
            self.score += 2
        elif food == "poop":
            self.score -= 1


    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.color)

        for i in range(len(self.body)):
            arcade.draw_rectangle_filled(self.body[i][0], self.body[i][1], self.width, self.height, self.color)



class Apple(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 16
        self.height = 16
        self.image = arcade.load_texture("apple.png")
        
        self.snake = Snake()
        temp_x = random.randint(0, SCREEN_WIDTH)
        temp_y = random.randint(0, SCREEN_HEIGHT)
        if not any ([temp_x, temp_y] for part in self.snake.body):
            self.center_x = temp_x
            self.center_y = temp_y


    def draw(self):
        arcade.draw_texture_rectangle(self.center_x, self.center_y, 30, 30, self.image)



class Pear(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 16
        self.height = 16
        self.image = arcade.load_texture("pear.png")

        self.apple = Apple()
        temp_x = random.randint(0, SCREEN_WIDTH)
        temp_y = random.randint(0, SCREEN_HEIGHT)
        if temp_x != self.apple.center_x or temp_y != self.apple.center_y:
            self.center_x = temp_x
            self.center_y = temp_y


    def draw(self):
        arcade.draw_texture_rectangle(self.center_x, self.center_y, 30, 30, self.image)



class Poop(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 16
        self.height = 16
        self.image = arcade.load_texture("poop.png")

        self.pear = Pear()
        temp_x = random.randint(0, SCREEN_WIDTH)
        temp_y = random.randint(0, SCREEN_HEIGHT)
        if temp_x != self.pear.center_x or temp_y != self.pear.center_y:
            self.center_x = temp_x
            self.center_y = temp_y


    def draw(self):
        arcade.draw_texture_rectangle(self.center_x, self.center_y, 30, 30, self.image)



class Game(arcade.Window):
    def __init__(self):
        super().__init__(width = SCREEN_WIDTH, height = SCREEN_HEIGHT, title = "Snake Game")
        arcade.set_background_color(arcade.color.SAND)
        self.snake = Snake()
        self.apple = Apple()
        self.pear = Pear()
        self.poop = Poop()


    def on_draw(self):
        arcade.start_render()

        if self.snake.score < 0 or  self.snake.center_x < 0 or self.snake.center_x > SCREEN_WIDTH or self.snake.center_y < 0 or self.snake.center_y > SCREEN_HEIGHT:
            arcade.draw_text("Game Over!", (SCREEN_WIDTH // 4) - 40, SCREEN_HEIGHT // 2, arcade.color.RED, width = 400, font_size = 40, align = "left")
        else:
            self.snake.draw()
            self.apple.draw()
            self.pear.draw()
            self.poop.draw()
            arcade.draw_text(f"Scores: {self.snake.score}", 5, SCREEN_HEIGHT - 20, arcade.color.BLACK, width = 100, font_size = 15, align = "left")
        

    def on_update(self, delta_time: float):
        self.auto_find()

        if arcade.check_for_collision(self.snake, self.apple):
            self.snake.eat("apple")
            self.apple = Apple()
        elif arcade.check_for_collision(self.snake, self.pear):
            self.snake.eat("pear")
            self.pear = Pear()
        elif arcade.check_for_collision(self.snake, self.poop):
            self.snake.eat("poop")
            self.poop = Poop()


    def auto_find(self):
        distance_apple = math.sqrt((self.snake.center_x - self.apple.center_x) ** 2 + (self.snake.center_y - self.apple.center_y) ** 2)
        distance_pear = math.sqrt((self.snake.center_x - self.pear.center_x) ** 2 + (self.snake.center_y - self.pear.center_y) ** 2)
        goal_x = 0
        goal_y = 0

        if distance_apple < distance_pear:
            goal_x = self.apple.center_x
            goal_y = self.apple.center_y
        else:
            goal_x = self.pear.center_x
            goal_y = self.pear.center_y

        go_right = True
        go_left = True
        go_up = True
        go_down = True

        if self.snake.center_x < self.poop.center_x and self.snake.center_y == self.poop.center_y:
            go_right = False
        if self.snake.center_x > self.poop.center_x and self.snake.center_y == self.poop.center_y:
            go_left = False
        if self.snake.center_x == self.poop.center_x and self.snake.center_y < self.poop.center_y:
            go_up = False
        if self.snake.center_x == self.poop.center_x and self.snake.center_y > self.poop.center_y:
            go_down = False

        if go_right and self.snake.center_x < goal_x:
            self.snake.change_x = 1
            self.snake.change_y = 0
            self.snake.move()
        elif go_left and self.snake.center_x > goal_x:
            self.snake.change_x = -1
            self.snake.change_y = 0
            self.snake.move()
        elif go_up and self.snake.center_y < goal_y:
            self.snake.change_x = 0
            self.snake.change_y = 1
            self.snake.move()
        elif go_down and self.snake.center_y > goal_y:
            self.snake.change_x = 0
            self.snake.change_y = -1
            self.snake.move()
    


my_game = Game()
arcade.run()