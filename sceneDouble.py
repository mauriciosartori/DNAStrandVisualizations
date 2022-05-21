from manim import *

# Demo of using the manim library.
# https://docs.manim.community/en/stable/tutorials/quickstart.html#overview
# manim -pql scene.py SquareAndCircle

def get_input_strand(file_name):
    file = open("./assets/" + file_name, "r")
    return file.read()


class DoubleStrand(Scene):
    def construct(self):
        axis = Axes()
        a = ValueTracker(-1 * PI)

        # Initial animation 1 (strand)
        input_strand = get_input_strand('dnaParenDot_2.txt')
        input_strand = input_strand.translate(str.maketrans('', '', ' \n\t\r'))
        elements = input_strand.split("+")
        print(elements)

        #f(x) = sin(x + a + sin(x))
        s1 = always_redraw(lambda : axis.plot(lambda x : np.sin(x + a.get_value()) + np.sin(x)).set_color(GREEN))
        self.play(Create(VGroup(s1)))
        self.wait()
        #Value of "a" becomes (5 * PI)
        self.play(a.animate.set_value(5 * PI), run_time=10)
        self.wait()
