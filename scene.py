from manim import *


# manim -pql scene.py DNAStrand

def get_input_strand(file_name):
    file = open("./assets/" + file_name, "r")
    return file.read()


class DNAStrand(Scene):

    def construct(self):
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

        dots = list()
        for element in input_strand:
            print(element)
            dot = Dot([initial_x, 0, 0]).scale(1.4)
            initial_x = initial_x + 1
            dots.append(dot)
            self.add(dot)

        self.remove(dots[-1])
        self.wait(0.5)
