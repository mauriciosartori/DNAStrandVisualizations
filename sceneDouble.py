from manim import *

# Double Strand animation
# manim -pql sceneDouble.py DoubleStrand

def get_input_strand(file_name):
    file = open("./assets/" + file_name, "r")
    return file.read()


class DoubleStrand(Scene):
    def construct(self):
        axis = Axes()
        a = ValueTracker(-1 * PI)

        # Initial animation - Strands interaction
        input_strand = get_input_strand('dnaParenDot_2.txt')
        input_strand = input_strand.translate(str.maketrans('', '', ' \n\t\r'))
        elements = input_strand.split("+")
        print(elements)

        #f(x) = sin(x + a + sin(x))
        strand_1 = always_redraw(lambda : axis.plot(lambda x : np.sin(x + a.get_value()) + np.sin(x) + 1).set_color(RED))
        #f(x) = cos(x + a + cos(x))
        strand_2 = always_redraw(lambda : axis.plot(lambda x : np.cos(x + a.get_value()) + np.cos(x) - 1).set_color(BLUE))
        self.play(Create(VGroup(strand_1, strand_2)))
        self.wait()
        #Value of "a" becomes (5 * PI & - 5 * PI)
        self.play(a.animate.set_value(5 * PI), run_time=10)
        self.wait()
        self.play(a.animate.set_value(-5 * PI), run_time=10)
        self.wait()

        # Final animation - Create double helix
        helix_1 = axis.plot(lambda x : np.sin(x)).set_color(RED)
        helix_2 = axis.plot(lambda x : np.sin(x+PI)).set_color(BLUE)
        self.play(ReplacementTransform(strand_1, helix_1), ReplacementTransform(strand_2, helix_2))
        self.wait()
