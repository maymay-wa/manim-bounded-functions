from manim import *

class DifferenceOfSquares(Scene):
    def construct(self):
        ##############################
        # Title & Introduction
        ##############################
        # Introduce the two problems
        #narraration: The other day I was doing school work with my friend when I came across this problem:
        prob1 = MathTex(r"101^2 - 100^2").scale(1.5)
        # I asked him, not really expecting and answer and without looking up from his page he said "201"
        prob2 = MathTex(r"101^2 - 100^2 = 201").scale(1.5)
        self.play(Write(prob1))
        self.wait(2)
        # I put it in my calculator and sure enough:
        self.play(Transform(prob1, prob2))
        self.wait(2)
        #narraration: In this video we're going to explore how a prblem that seems impossible to do on the fly
        #can be broken down into smaller steps
        prob3 = MathTex(r"5^2 - 4^2 = 25 - 16 = 9").scale(1.5)
        # lets use ony of my favorite techniques and play with the problem with smaller numbers and see how it behaves
        self.play(Transform(prob1, prob3))
        self.wait(2)
        self.play(FadeOut(prob1))
        self.wait(0.5)
        #################################
        # PART 1: Algebraic Approach
        #################################
        alg_title = Text("Level 1 - The Algebraic Approach", font_size=36)
        self.play(Write(alg_title))
        self.wait(1)
        self.play(Unwrite(alg_title))

        # Show the specific example for 101^2 - 100^2
        eq1p1 = MathTex(
            r"5", r"=", r"4+1"
        )
        # Right-align both expressions
        self.play(Write(eq1p1))
        self.wait(3)
        eq1p2 = MathTex(
            r"5^2", 
            r"=", r"(4 + 1)^2"
        )
        self.play(Transform(eq1p1, eq1p2))
        eq1p3 = MathTex(
            r"5^2", r"=", r"(4 + 1)^2",  r"=", r"4^2 + 4\cdot 2 + 1"
        )
        self.play(Transform(eq1p1, eq1p3))

        eq1p4 = MathTex(r"5^2 - 4^2 = 4^2 + 4\cdot 2 + 1 = 2\cdot 100 + 1")
        self.play(Transform(eq1p1, eq1p4))
        self.wait(3)

        eq1p5 = MathTex(r"4\cdot 2 + 1")
        self.play(Transform(eq1p1, eq1p4))
        self.wait(3)

        # Show the general result
        general_eq = MathTex(r"(x+1)^2 - x^2 = 2x + 1")
        general_eq.next_to(eq1p5, DOWN, buff=1)
        self.play(Write(general_eq))
        self.wait(3)

        self.play(*[FadeOut(mob) for mob in [eq1p1, general_eq]])
        self.wait(0.5)
'''
        #################################
        # PART 2: Geometric Interpretation
        #################################
        geo_title = Text("Geometric Interpretation", font_size=36)
        self.play(Write(geo_title))
        self.wait(1)
        self.play(Unwrite(geo_title))

        # Create a 4x4 grid of small squares (like graph paper)
        square_size = 0.7
        grid4 = VGroup(*[Square(side_length=square_size, color=BLUE) for _ in range(16)])
        grid4.arrange_in_grid(rows=4, buff=0)
        grid4.center()
        grid4_label = MathTex("4\\times 4").next_to(grid4, DOWN)
        self.play(Create(grid4), Write(grid4_label))
        self.wait(1)

        # Indicate that the grid contains 16 squares.
        sixteen_text = Text("16 squares", font_size=24)
        sixteen_text.next_to(grid4, UP)
        self.play(Write(sixteen_text))
        self.wait(1)
        self.play(FadeOut(sixteen_text))

        # Add 4 squares along the bottom of the 4x4 grid.
        bottom_row = VGroup(*[Square(side_length=square_size, color=GREEN) for _ in range(4)])
        bottom_row.arrange(RIGHT, buff=0)
        bottom_row.next_to(grid4, DOWN, aligned_edge=LEFT, buff=0)
        self.play(Create(bottom_row))
        self.wait(1)

        # Add 4 squares along the right side of the 4x4 grid.
        right_col = VGroup(*[Square(side_length=square_size, color=GREEN) for _ in range(4)])
        right_col.arrange(DOWN, buff=0)
        right_col.next_to(grid4, RIGHT, aligned_edge=UP, buff=0)  # Changed TOP to UP
        self.play(Create(right_col))
        self.wait(1)

        # At this point: 16 + 4 + 4 = 24 squares.
        addition_text = MathTex(r"16 + 4 + 4 = 24").next_to(grid4, UP, buff=1)
        self.play(Write(addition_text))
        self.wait(2)
        self.play(FadeOut(addition_text))

        # Add the final square to complete the 5x5 grid.
        last_square = Square(side_length=square_size, color=RED)
        last_square.next_to(bottom_row, RIGHT, buff=0)
        last_square.align_to(right_col, DOWN)
        self.play(Create(last_square))
        self.wait(2)

        # Group everything to represent the complete 5x5 grid.
        grid5 = VGroup(grid4, bottom_row, right_col, last_square)
        complete_label = MathTex("5\\times 5").next_to(grid5, DOWN)
        self.play(Write(complete_label))
        self.wait(2)

        # Optionally, show the total count: 16 + 4 + 4 + 1 = 25.
        total_text = MathTex("16 + 4 + 4 + 1 = 25").next_to(complete_label, DOWN)
        self.play(Write(total_text))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in [geo_title, grid5, grid4_label, complete_label, total_text]])
        self.wait(0.5)

        #################################
        # PART 3: Calculus Perspective
        #################################
        calc_title = Text("Calculus Perspective", font_size=36)
        self.play(Write(calc_title))
        self.wait(1)

        # Show the function and its derivative.
        func_text = MathTex(r"f(x)=x^2")
        func_text.to_edge(UP)
        deriv_text = MathTex(r"f'(x)=2x")
        deriv_text.next_to(func_text, DOWN)
        self.play(Write(func_text), Write(deriv_text))
        self.wait(2)

        # Demonstrate the finite difference approximation:
        approx_text = MathTex(r"101^2-100^2=2\cdot100+1=201")
        approx_text.next_to(deriv_text, DOWN, buff=1)
        self.play(Write(approx_text))
        self.wait(2)

        # Now, compare with a different example:
        slope_text = MathTex(r"\text{Average slope between }4\text{ and }5 = 4.5")
        slope_text.next_to(approx_text, DOWN, buff=1)
        self.play(Write(slope_text))
        self.wait(2)

        # Draw an axes and plot f(x)=x^2.
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 100, 10],
            x_length=6,
            y_length=6,
            tips=False,
        )
        axes.to_edge(DOWN)
        graph = axes.plot(lambda x: x**2, color=BLUE)
        self.play(Create(axes), Create(graph))
        self.wait(1)

        # Mark two points on the curve (at x = 4.1 and x = 4.9).
        p1 = axes.coords_to_point(4.1, 4.1**2)
        p2 = axes.coords_to_point(4.9, 4.9**2)
        dot1 = Dot(p1, color=RED)
        dot2 = Dot(p2, color=RED)
        self.play(FadeIn(dot1), FadeIn(dot2))
        self.wait(1)

        # Draw the secant line between these points.
        secant = Line(p1, p2, color=GREEN)
        self.play(Create(secant))
        self.wait(2)

        # Annotate the slope of the secant.
        slope_calc = MathTex(r"\frac{4.9^2-4.1^2}{4.9-4.1}\approx 4.5")
        slope_calc.to_edge(RIGHT)
        self.play(Write(slope_calc))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in [
            calc_title, func_text, deriv_text, approx_text, slope_text,
            axes, graph, dot1, dot2, secant, slope_calc
        ]])
        self.wait(0.5)

        ##############################
        # Conclusion
        ##############################
        conclusion = Text("Algebra, Geometry, and Calculus all reveal the beauty of math!", font_size=36)
        self.play(Write(conclusion))
        self.wait(3)
        self.play(FadeOut(conclusion))'
        '''