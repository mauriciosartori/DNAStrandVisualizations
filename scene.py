from manim import *

# Demo of using the manim library.
# https://docs.manim.community/en/stable/tutorials/quickstart.html#overview

class MovingGroupToDestination(Scene):
    def construct(self):
        group = VGroup(Dot(LEFT), Dot(ORIGIN), Dot(RIGHT, color=RED), Dot(2 * RIGHT)).scale(1.4)
        dest = Dot([4, 3, 0], color=YELLOW)
        self.add(group, dest)
        self.play(group.animate.shift(dest.get_center() - group[2].get_center()))
        self.wait(0.5)

class SquareAndCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency

        square = Square()  # create a square
        square.set_fill(BLUE, opacity=0.5)  # set the color and transparency

        square.next_to(circle, RIGHT, buff=0.5)  # set the position
        self.play(Create(circle), Create(square))  # show the shapes on screen
