from manim import *
from util import *

# Double Strand animation
# manim -pql sceneDouble.py DoubleStrand


class DoubleStrand(MovingCameraScene):
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
        strand_1 = always_redraw(lambda: axis.plot(lambda x: np.sin(x + a.get_value()) + np.sin(x) + 1).set_color(RED))
        #f(x) = cos(x + a + cos(x))
        strand_2 = always_redraw(lambda: axis.plot(lambda x: np.cos(x + a.get_value()) + np.cos(x) - 1).set_color(BLUE))
        self.play(Create(VGroup(strand_1, strand_2)))
        self.wait()
        #Value of "a" becomes (5 * PI & - 5 * PI)
        self.play(a.animate.set_value(5 * PI), run_time=10)
        self.wait()

        # Create bounds
        pairs = VGroup()
        for i in range(elements[0].count('(')):
            dot1 = Dot(color=PURPLE, radius=0.2)
            dot2 = dot1.copy().set_color(PURPLE).next_to(dot1, DOWN, buff=1)
            line = Line(dot1.get_center(), dot2.get_center(), color=WHITE, stroke_width=3.5).set_z_index(-1)
            pairs.add(VGroup(dot1, line, dot2))
        pairs.arrange(RIGHT, buff=2.0)
        self.play(Create(pairs, run_time=2))
        self.wait(2)
        self.create_zoom_effect(2)
        self.wait(.5)
        self.remove(pairs)

        # Final animation - Create double helix
        helix_1 = axis.plot(lambda x: np.sin(x + PI), x_range=(-16, 16)).set_color(RED)
        helix_2 = axis.plot(lambda x: np.sin(x), x_range=(-16, 16)).set_color(BLUE)
        lines = VGroup()
        for i in np.arange(-7 * PI, 7 * PI, PI/6):
            if np.isclose(i % PI, 0):
                continue
            line = Line(axis.i2gp(i, helix_1), axis.i2gp(i, helix_2), color=WHITE).set_z_index(-10)
            dots = [Dot(i, DEFAULT_DOT_RADIUS, color=PURPLE).set_z_index(10) for i in line.get_start_and_end()]
            lines.add(VGroup(line, *dots))
        self.play(ReplacementTransform(strand_1, helix_1), ReplacementTransform(strand_2, helix_2))
        self.add(lines)
        self.wait()
        self.play(self.camera.frame.animate.shift(LEFT*9), run_time=7)
        self.wait()

    def create_intro(self):
        center_text = Text('DNA Strand Visualization').center()
        self.play(Create(center_text))
        self.wait(1)
        self.remove(center_text)
        center_text = Text('DNA strands interact with each other without any specific order.\n\nWhen two complementary domains react, they can combine.').move_to(1*UP).scale(0.7)
        self.play(Write(center_text))
        self.wait(3)
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
        # Zoom animation
        self.create_zoom_effect(1)
        self.play(stream_lines_1.end_animation(), stream_lines_2.end_animation())
        self.play(Restore(self.camera.frame))
        self.clear()

    def create_zoom_effect(self, radius):
        circle = Circle(color=BLACK, radius=radius)
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.set(width=circle.width*2).move_to(circle))
        self.wait(0.3)
