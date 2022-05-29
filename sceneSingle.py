import math

from manim import *


# manim -pql scene.py DNAStrand
# ((((...))))
def get_input_strand(file_name):
    file = open("./assets/" + file_name, "r")
    return file.read()


class DNAStrand(Scene):
    def construct(self):
        # Common params
        input_strand_text = get_input_strand('dnaParenDot_1.txt')
        initial_x = 0 - (len(input_strand_text) / 2)
        title_text = Text('DNA Single Strand').to_edge(UL)
        strand_manim_text = Text(input_strand_text).next_to(title_text, DOWN)
        frame_box = SurroundingRectangle(strand_manim_text, buff=0.1)

        # Show animation title
        self.animate_strand_pattern_and_title(title_text, input_strand_text, frame_box)

    # I am NOT calling this method now
    def dna_shape(self, input_strand, title_text, strand_text, frame_box):
        # Animate arrow
        self.draw_arrow(input_strand, initial_x)

        # Draw dots over arrow
        self.draw_dots_over_arrow(input_strand, initial_x)

        # Clear the screen
        self.clear()

        # Draw animation two
        self.animation_two(input_strand, title_text, strand_text, frame_box)

    def animate_strand_pattern_and_title(self, title_text, input_strand_text, frame_box):
        temp_strand_text = '.' * (len(input_strand_text) - 1)
        temp_strand_text_manim = Text(temp_strand_text).next_to(title_text, DOWN)
        self.animate_title_and_box(title_text, frame_box)

        # Animate one time with only dots
        self.play(Write(temp_strand_text_manim))
        self.wait(2)
        self.remove(temp_strand_text_manim)

        # Start frame animations getting length of stand and set up indexes
        stand_text_len = len(input_strand_text)
        start_index = 0
        end_index = stand_text_len - 2

        # Create list to modify it
        text_list = list(temp_strand_text)
        for x in range(stand_text_len):
            if start_index >= (end_index - 2): break

            text_list[start_index] = input_strand_text[start_index]
            text_list[end_index] = input_strand_text[end_index]
            updated_strand_text = "".join(text_list)

            scene_temp_strand_text_manim = Text(updated_strand_text).next_to(title_text, DOWN)
            start_index += 1
            end_index -= 1

            self.play(Write(scene_temp_strand_text_manim))
            self.wait(2)
            self.remove(scene_temp_strand_text_manim)

    def animate_strand_text(self, strand_text_manim):
        self.play(Write(strand_text_manim))
        self.wait()

    def animate_title_and_box(self, title_text, frame_box):
        self.play(Write(title_text))
        self.play(
            Create(frame_box),
        )
        self.wait()

    def draw_arrow(self, input_strand, initial_x):

        final_x = initial_x + (len(input_strand) - 1)
        line = Arrow([initial_x, 0, 0], [final_x, 0, 0], buff=0).set_color(ORANGE)
        self.play(Create(line))

    def draw_dots_over_arrow(self, input_strand, initial_x):
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

    def animation_two(self, input_strand, title_text, strand_text, frame_box):
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
        # Draw circle
        self.wait()
        angle = math.radians(-300)
        arc = Arc(arc_center=[4.9, -0.5, 0], radius=1, angle=angle)
        self.add(arc)
        self.play(Rotate(arc, angle=PI * .85, rate_func=linear))
        self.wait()
