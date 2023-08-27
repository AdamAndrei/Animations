from manim import *


def getPointsOnCircle(circle: Circle, n) -> list[np.ndarray]:
    angles = [k * (360 / n) for k in range(n)]
    return [circle.point_at_angle(angle * DEGREES) for angle in angles]


def getDotsOnCircle(n, label_dots: bool, circle: Circle) -> VGroup:
    return VGroup(*getDotsOnCircleL(n, label_dots, circle))


def getDotsOnCircleL(n, label_dots: bool, circle: Circle) -> list:
    points: list[np.ndarray] = getPointsOnCircle(circle, n)
    objects = []
    for i in range(n):
        p = points[i]
        if label_dots:
            objects.append(LabeledDot(Tex("{}".format(i), color=WHITE), color=RED).scale(0.4).move_to(p))
        else:
            objects.append(Dot(color=RED, stroke_width=1).scale(0.4).move_to(p))

    return objects


def getSegmentsOnCircleL(n, circle: Circle, colour: str = PURPLE, width: float = 4.0) -> list:
    points: list[np.ndarray] = getPointsOnCircle(circle, n)
    objects = []
    for i in range(n):
        p1 = points[i]
        second_index = (2 * i) % n
        p2 = points[second_index]
        segment = Line(p1, p2, stroke_width=width, stroke_color=colour)
        objects.append(segment)

    return objects


def getSegmentsOnCircle(n, circle: Circle, colour: str = PURPLE) -> VGroup:
    return VGroup(*getSegmentsOnCircleL(n, circle, colour))


def getImage(n, circle: Circle, colour: str = PURPLE) -> VGroup:
    d = VGroup(*[])
    if n < 50:
        d.add(getDotsOnCircle(n, True, circle))
    else:
        d.add(getDotsOnCircle(n, False, circle))
    d.add(getSegmentsOnCircle(n, circle, colour))

    return d


class WithSegments(Scene):

    def construct(self):
        self.a()
        circle = Circle(radius=3, color=DARK_BLUE, stroke_width=8)
        self.b(10, circle)
        self.c(circle)

    def a(self):
        s = 0.5
        m1 = Text("Mathematics has the magic of taking simple \"things\", \"complicating\" them \n \t\t\t\t\t\t\t and"
                  " then revealing it's hidden beauty.").to_edge(UP).scale(s)
        m2 = Text("Let's take for example the 2 times multiplication table").next_to(m1, .5 * DOWN).scale(s)
        t1 = MathTex("2 \\times 0 = 0").next_to(m2, 2 * DOWN).scale(s)
        t2 = MathTex("2 \\times 1 = 2").next_to(t1, DOWN).scale(s)
        t3 = MathTex("2 \\times 2 = 4").next_to(t2, DOWN).scale(s)
        t4 = MathTex("2 \\times 3 = 6").next_to(t3, DOWN).scale(s)
        t5 = MathTex("2 \\times 4 = 8").next_to(t4, DOWN).scale(s)
        t6 = MathTex("2 \\times 5 = 10").next_to(t5, DOWN).scale(s)
        t7 = MathTex("2 \\times 6 = 12").next_to(t6, DOWN).scale(s)
        t8 = MathTex("2 \\times 7 = 14").next_to(t7, DOWN).scale(s)
        t9 = MathTex("2 \\times 8 = 16").next_to(t8, DOWN).scale(s)
        t10 = MathTex("2 \\times 9 = 18").next_to(t9, DOWN).scale(s)

        self.play(Create(m1), run_time=4)
        self.wait(.5)
        self.play(Create(m2), run_time=2)
        self.play(Create(t1), Create(t2), Create(t3), Create(t4), Create(t5), Create(t6),
                  Create(t7), Create(t8), Create(t9), Create(t10), run_time=3)

        self.wait(1)
        self.clear()

    def b(self, n, circle: Circle):
        doc: VGroup = getDotsOnCircle(n, True, circle)
        soc: VGroup = getSegmentsOnCircle(n, circle)
        cd: VGroup = VGroup(*[circle]).add(doc.copy())

        tu = Text("Let's take a circle and put some equally distanced points on it").scale(0.5).to_edge(UP)

        self.play(Write(tu), run_time=3)
        self.play(Create(cd), run_time=4)
        self.wait()

        td = Text("Now unite each point with its double, if it surpasses the maximum number, go around the circle") \
            .scale(0.4).to_edge(DOWN)

        self.play(Write(td), run_time=2)

        goes = Text("goes to").scale(0.5).move_to(5 * RIGHT)
        nu = Text("0").scale(0.5).next_to(goes, UP)
        nd = Text("0").scale(0.5).next_to(goes, DOWN)
        s0 = soc[0]
        self.play(FadeIn(nu), FadeIn(goes), FadeIn(nd), Create(s0), run_time=1)

        for i in range(1, n):
            nu1 = Text("{}".format(i)).scale(0.5).next_to(goes, UP)
            nd1 = Text("{}".format((2 * i) % n)).scale(0.5).next_to(goes, DOWN)
            si = soc[i]
            self.play(ReplacementTransform(nu, nu1), ReplacementTransform(nd, nd1), ReplacementTransform(s0, si),
                      run_time=1)
            nu = nu1
            nd = nd1
            s0 = si
            self.wait(.5)

        self.wait(1)
        self.clear()

    def c(self, circle: Circle):
        t1 = Text("Now let's see what happens if we put all these together and increase the number of points") \
            .scale(0.3).to_edge(UP)
        self.play(Write(t1), run_time=1)
        self.wait(1.5)
        self.play(Unwrite(t1), run_time=1)

        self.play(FadeIn(circle), run_time=2)

        start = 10
        ds = getDotsOnCircle(start, True, circle)
        objects = getSegmentsOnCircleL(start, circle)
        animations = [Create(o) for o in objects]
        self.play(Create(ds))
        self.play(*animations, run_time=2)

        v1: VGroup = getImage(10, circle)
        l1 = Tex("{}".format(10), color=TEAL).to_edge(UP)
        self.play(Create(v1), Create(l1), run_time=1)
        self.remove(ds)
        self.remove(*objects)

        for k in range(start + 1, start + 91):
            v2: VGroup = getImage(k, circle)
            l2 = Tex("{}".format(k), color=TEAL).to_edge(UP)
            self.play(ReplacementTransform(v1, v2), ReplacementTransform(l1, l2), run_time=0.2)
            v1 = v2
            l1 = l2

        self.wait(1)

        final = 500
        self.play(Uncreate(v1), ReplacementTransform(l1, Tex("{}".format(final), color=TEAL).to_edge(UP)), run_time=2)
        self.wait(0.2)
        df = getDotsOnCircle(final, False, circle)
        objects1 = getSegmentsOnCircleL(final, circle, YELLOW, 1)
        animations1 = [Create(o) for o in objects1]
        self.play(Create(df))
        self.play(*animations1, run_time=3)
        self.wait(2)
