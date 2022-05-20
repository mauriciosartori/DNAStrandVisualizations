from manim import *
import math


# manim -pql scene.py DNAStrand

def get_input_strand(file_name):
    file = open("./assets/" + file_name, "r")
    return file.read()


class DNAStrand(Scene):

    def construct(self):
        # Initial animation 1 (strand)
        input_strand = get_input_strand('dnaParenDot_1.txt')
        initial_x = 0 - (len(input_strand) / 2)
        final_x = initial_x + (len(input_strand) - 1)
        line = Arrow([initial_x, 0, 0], [final_x, 0, 0], buff=0).set_color(ORANGE)
        title_text = Text('DNA Strand').to_edge(UL)
        strand_text = Text(input_strand).next_to(title_text, DOWN)
        self.play(Write(title_text), Write(strand_text))
        frame_box = SurroundingRectangle(strand_text, buff=0.1)
        self.play(
            Create(frame_box),
        )
        self.wait()
        self.play(Create(line))
        # Add dots to animation 1
        dots = list()
        input_strand = input_strand.translate(str.maketrans('', '', ' \n\t\r'))
        for element in input_strand:
            print(element)
            dot = Dot([initial_x, 0, 0]).scale(1.4)
            initial_x = initial_x + 1
            dots.append(dot)
            strand_char = Text(element).next_to(dot, UP)
            self.add(dot)
            self.play(Create(strand_char))

        self.wait()

        # Clear the screen
        self.clear()

        # Animation 2 (mfe structure)
        self.add(title_text, strand_text, frame_box)
        number_parenthesis = input_strand.count('(')
        # Build structure
        path = VMobject()
        dot = Dot()
        path.set_points_as_corners([dot.get_center(), dot.get_center()])

        def update_path(path):
            previous_path = path.copy()
            previous_path.add_points_as_corners([dot.get_center()])
            path.become(previous_path)

        path.add_updater(update_path)
        self.add(path, dot)
        for i in range(number_parenthesis):
            new_dot = Dot([i, 0, 0])
            self.add(new_dot)
            self.play(dot.animate.shift(RIGHT))
        dot1 = Dot([number_parenthesis, 0, 0])
        self.add(dot1)
        self.play(dot.animate.shift(DOWN))
        dot2 = Dot([number_parenthesis, -1, 0])
        self.add(dot2)
        for i in reversed(range(number_parenthesis)):
            self.play(dot.animate.shift(LEFT))
            new_dot = Dot([i, -1, 0])
            self.add(new_dot)
        # Add arrow at the end
        arrow = Arrow([0, -1, 0], [-2, -1, 0], buff=0, max_stroke_width_to_length_ratio=1.7)
        self.play(Create(arrow))
        self.wait()
        # Add the connection lines
        for i in range(number_parenthesis):
            if i % 2 == 0:
                self.play(dot.animate.shift(UP))
            else:
                self.play(dot.animate.shift(DOWN))
            self.play(dot.animate.shift(RIGHT))
        #Draw circle
        self.wait()
        angle = math.radians(-300)
        arc = Arc(arc_center=[4.9, -0.5, 0], radius=1, angle=angle)
        self.add(arc)
        self.play(Rotate(arc, angle=PI*.85, rate_func=linear))
        self.wait()

