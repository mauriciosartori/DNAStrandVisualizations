from manim import *
from util import *

# Single Strand animation
# manim -pql sceneSingleTwo.py DNAStrand


class DNAStrand(MovingCameraScene):
    def construct(self):
        # Show intro animation
        self.create_intro()
        Text.set_default(color=WHITE)

        config.tex_template = TexTemplate()
        input_strand = get_input_strand('dnaParenDotEncoded_1.txt')
        circle_factor = 0.2
        pairs = VGroup()
        characters, string = parse_dot_parens_plus(input_strand)

        n_parenthesis = characters[0][1]

        for parenthesis in range(n_parenthesis):
            dot1 = Dot(color=RED, radius=0.2)
            dot2 = dot1.copy().set_color(ORANGE).next_to(dot1, DOWN, buff=1)
            line = Line(dot1.get_center(), dot2.get_center(), color=WHITE, stroke_width=3.5).set_z_index(-1)
            pairs.add(VGroup(dot1, line, dot2))
        pairs.arrange(RIGHT, buff=0.5)

        line_top = Line(pairs[0][0].get_center(), pairs[-1][0].get_center(), stroke_width=3.5, color=WHITE).set_z_index(
            -1)
        line_bottom = Line(pairs[0][-1].get_center(), pairs[-1][-1].get_center(), stroke_width=3.5,
                           color=WHITE).set_z_index(-1).reverse_points()

        circle = Circle.from_three_points(pairs[-1][0].get_center(), pairs[-1][-1].get_center(),
                                          pairs[-1].get_center() + LEFT * circle_factor).rotate(PI)
        center = circle.get_center()
        radius = circle.radius
        circle = Difference(circle,
                            Rectangle(color=RED, height=pairs.height, width=5, fill_opacity=1).next_to(pairs[-1][1],
                                                                                                       LEFT,
                                                                                                       buff=0)).reverse_points()
        circle.set_color(WHITE).set_stroke(width=3.45).set_z_index(-5)
        rec = SurroundingRectangle(pairs[-1][1], color=BLACK, buff=0.005).set_z_index(-2).set_fill(BLACK, 1)

        VGroup(line_bottom, line_top).shift(RIGHT * 0.022).stretch(1.01, 1)
        pairs.shift(RIGHT * 0.022)

        circle_dots = VGroup()
        n_dots = characters[1][1]

        for k in range(n_dots):
            dot = dot1.copy().move_to(center + radius * np.cos(1.5 * np.pi * k / n_dots) * RIGHT + radius * np.sin(
                1.5 * np.pi * k / n_dots) * UP)
            dot.set_color(BLUE)
            circle_dots.add(dot)
        circle_dots.rotate(-1.5 * np.pi * (n_dots - 1) / (2 * n_dots), about_point=center)

        VGroup(pairs, line_top, line_bottom, circle, circle_dots, rec).center()

        ax = Axes(
            x_range=(-config.frame_width / 2, config.frame_width / 2),
            y_range=(-config.frame_height / 2, config.frame_height / 2),
            x_length=config.frame_width,
            y_length=config.frame_height,
        )

        x1, y1 = line_top.get_start()[:2]
        x2, y2 = line_top.get_end()[:2]

        x12, y12 = line_bottom.get_end()[:2]
        x22, y22 = line_bottom.get_start()[:2]

        A = 0.2

        sin_func_top = ax.plot(lambda x: A * np.sin((x - x2) * len(pairs)) + y1, x_range=(x1, x2), color=WHITE)
        sin_func_bottom = ax.plot(lambda x: A * np.sin((x - x22) * len(pairs)) + y22, x_range=(x1, x2),
                                  color=WHITE).reverse_points()
        sin_func_bottom.rotate(PI / 8, about_point=sin_func_bottom.get_start())

        strand = Text("Strand").to_corner(UL, buff=0.5).set_color(WHITE)
        string_text = Text(string).next_to(strand, buff=0.25)

        # Write strand title
        self.add(rec)
        self.play(Write(VGroup(strand, string_text)), run_time=2.3)
        self.wait(0.5)

        # Play Sin + circle + Sin
        self.play(Create(VGroup(rec, sin_func_top, circle, sin_func_bottom)), run_time=3)
        self.wait(0.7)

        # Replace and animate strand title for dots
        self.play(FadeOut(string_text), run_time=0.8)
        self.wait(0.5)

        # Draw dots on circle
        self.play(LaggedStart(*[AnimationGroup(
            FadeIn(dot, string_text[n_parenthesis + n])) for n, dot in enumerate(circle_dots[::-1])],
                              lag_ratio=0.4,
                              run_time=n_dots / 2.5
                              ))
        self.wait(0.5)

        # Replace AND play Sin by lines
        self.play(AnimationGroup(
            ReplacementTransform(sin_func_top, line_top),
            ReplacementTransform(sin_func_bottom, line_bottom)
        ), run_time=1.55)

        # Play dots on lines
        self.play(LaggedStart(
            *[LaggedStart(FadeIn(pair[0], VGroup(string_text[n], string_text[-1-n])), Create(pair[1]), FadeIn(pair[2]), lag_ratio=0.35)
                for n, pair in enumerate(pairs[::-1])],
            lag_ratio=0.4,
            run_time=len(pairs) / 1.7
        ))
        self.wait()

    def create_intro(self):
        center_text = Text('DNA Strand Visualization').center()
        self.play(Create(center_text))
        self.wait(1)
        self.remove(center_text)
        func = lambda pos: (pos[0] * UR + pos[1] * LEFT) - pos
        stream_lines = StreamLines(
            func,
            color=WHITE,
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            stroke_width=3,
            virtual_time=1,  # use shorter lines
            max_anchors_per_line=5,  # better performance with fewer anchors
        )
        self.play(stream_lines.create())  # uses virtual_time as run_time
        self.wait()

        # Zoom animation
        self.create_zoom_effect(1)
        self.clear()
        self.play(Restore(self.camera.frame))

    def create_zoom_effect(self, radius):
        circle = Circle(color=BLACK, radius=radius)
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.set(width=circle.width * 2).move_to(circle))
        self.wait(0.3)
