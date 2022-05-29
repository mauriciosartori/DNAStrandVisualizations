from manim import *
from util import *

# Double Strand animation
# manim -pql sceneDouble.py DoubleStrand


class DoubleStrand(Scene):
    def construct(self):
        # Intro animation
        self.create_intro()

        # Initial animation - Strands interaction
        axis = Axes()
        a = ValueTracker(-1 * PI)
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

    def create_intro(self):
        center_text = Text('DNA Strand Visualization').center()
        self.play(Create(center_text))
        self.wait(1)
        self.remove(center_text)
        center_text = Text('DNA strands interact with each other without any specific order').move_to(1*UP).scale(0.7)
        self.play(Create(center_text))
        self.wait(2)
        self.remove(center_text)
        func_1 = lambda pos: np.sin(pos[0] / 2) * UR + np.cos(pos[1] / 2) * LEFT
        func_2 = lambda pos: np.sin(pos[0] / 2) * UR + np.cos(pos[1] / 2) * RIGHT
        stream_lines_1 = StreamLines(
            func_1, stroke_width=3, max_anchors_per_line=5, virtual_time=1, color=BLUE
        )
        stream_lines_2 = StreamLines(
            func_2, stroke_width=3, max_anchors_per_line=5, virtual_time=1, color=RED
        )
        self.add(stream_lines_1, stream_lines_2)
        stream_lines_1.start_animation(warm_up=False, flow_speed=1.5, time_width=0.5)
        stream_lines_2.start_animation(warm_up=False, flow_speed=1.5, time_width=0.5)
        self.wait(3)
        self.play(stream_lines_1.end_animation(), stream_lines_2.end_animation())
        self.clear()
