from manim import *


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
        for element in input_strand:
            print(element)
            dot = Dot([initial_x, 0, 0]).scale(1.4)
            initial_x = initial_x + 1
            dots.append(dot)
            self.add(dot)

        self.remove(dots[-1])
        self.wait(1)

        # Clear the screen
        self.clear()

        # Animation 2 (mfe structure)
        self.add(title_text, strand_text, frame_box)

        path = VMobject()
        dot = Dot()
        path.set_points_as_corners([dot.get_center(), dot.get_center()])
        def update_path(path):
            previous_path = path.copy()
            previous_path.add_points_as_corners([dot.get_center()])
            path.become(previous_path)
        path.add_updater(update_path)
        self.add(path, dot)
        for i in range(3):
            auxDot = Dot([i, 0, 0])
            self.add(auxDot)
            self.play(dot.animate.shift(RIGHT))

        # self.play(Rotating(dot, radians=PI, about_point=DOWN, run_time=2))
        # self.wait()

        dot1 = Dot([3, 0, 0])
        self.add(dot1)
        self.play(dot.animate.shift(DOWN))
        dot2 = Dot([3, -1, 0])
        self.add(dot2)

        for i in reversed(range(3)):
            self.play(dot.animate.shift(LEFT))
            auxDot = Dot([i, -1, 0])
            self.add(auxDot)

        arrow = Arrow([0, -1, 0], [-2, -1, 0], buff=0, max_stroke_width_to_length_ratio=1.7)
        self.play(Create(arrow))

        self.wait()
