from manim import *
from util import *

# Single Strand animation
# manim -pql sceneSingleTwo.py DNAStrand


class DNAStrand(Scene):
    def construct(self):
        config.tex_template = TexTemplate()
        input_strand = get_input_strand('dnaParenDotEncoded_1.txt')
        circle_factor = 0.2
        pairs = VGroup()
        characters, string = parse_dot_parens_plus(input_strand)
        strand = Text(string).to_corner(UL, buff=0.5).set_color(WHITE)

        for parenthesis in range(characters[0][1]):
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
        rec = SurroundingRectangle(pairs[-1][1], color=BLACK, buff=0.005).set_z_index(-2).set_fill(WHITE, 1)

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

        self.add(rec)
        self.play(Write(strand), run_time=2.3)
        self.wait(0.5)

        self.play(Create(VGroup(rec, sin_func_top, circle, sin_func_bottom)), run_time=3)
        self.wait(0.7)
        self.play(AnimationGroup(
            ReplacementTransform(sin_func_top, line_top),
            ReplacementTransform(sin_func_bottom, line_bottom)
        ), run_time=1.5)
        self.play(LaggedStart(
            *[FadeIn(dot) for dot in circle_dots[::-1]],
            lag_ratio=0.4,
            run_time=n_dots / 2.5
        ))
        self.wait(0.5)
        self.play(LaggedStart(
            *[LaggedStart(FadeIn(pair[0]), Create(pair[1]), FadeIn(pair[2]), lag_ratio=0.35) for pair in pairs[::-1]],
            lag_ratio=0.4,
            run_time=len(pairs) / 1.7
        ))
        self.wait()
