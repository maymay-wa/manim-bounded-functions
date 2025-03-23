from manim import *

class DifferenceOfSquares(Scene):
    def construct(self):
        ##############################
        # Title & Introduction
        ##############################
        title = Text("Exploring the Difference of Squares", font_size=48)
        self.play(FadeIn(title, shift=UP, run_time=2))
        self.wait()
        self.play(FadeOut(title, shift=DOWN, run_time=1.5))
        self.wait(0.5)

        # Introduce the two problems
        prob1 = MathTex(r"101^2 - 100^2").scale(1.3)
        prob2 = MathTex(r"25^2 - 20^2").scale(1.3)
        
        prob1.move_to(UP*0.5)
        self.play(Write(prob1))
        self.wait(2)
        
        # Transform the first problem into the second
        self.play(Transform(prob1, prob2, run_time=2))
        self.wait(2)
        self.play(FadeOut(prob1, run_time=1.5))
        self.wait(0.5)

        #################################
        # PART 1: Algebraic Approach
        #################################
        alg_title = Text("Algebraic Approach", font_size=36)
        alg_title.to_edge(UP)

        self.play(FadeIn(alg_title, shift=RIGHT))
        self.wait(1)

        # Show the specific example for 101^2 - 100^2
        eq1 = MathTex(
            r"101^2", r"=", r"(100+1)^2", r"=", r"100^2", r"+", r"2\cdot 100", r"+", r"1"
        )
        eq1.scale(0.8)
        eq1.next_to(alg_title, DOWN, buff=0.5)
        self.play(Write(eq1))
        self.wait(3)

        # Subtract 100^2 from both sides:
        eq2 = MathTex(r"101^2 - 100^2", r"=", r"2\cdot 100", r"+", r"1")
        eq2.scale(0.8)
        eq2.next_to(eq1, DOWN, buff=0.6)

        # Transform part of eq1 into eq2 to emphasize the subtraction
        self.play(
            TransformFromCopy(eq1[0], eq2[0]),  # 101^2
            TransformFromCopy(eq1[1], eq2[1]),  # =
            TransformFromCopy(eq1[5], eq2[2]),  # 2*100
            TransformFromCopy(eq1[7], eq2[4]),  # + 1
            run_time=2
        )
        # Insert the plus sign (index 3) from eq2 by hand:
        self.play(Write(eq2[3]))
        self.wait(2)

        # Show the general result
        general_eq = MathTex(r"(x+1)^2 - x^2 = 2x + 1")
        general_eq.scale(0.8)
        general_eq.next_to(eq2, DOWN, buff=0.6)
        self.play(Write(general_eq))
        self.wait(3)

        # Fade out everything from Part 1
        self.play(
            FadeOut(alg_title, shift=LEFT),
            FadeOut(eq1, shift=LEFT),
            FadeOut(eq2, shift=LEFT),
            FadeOut(general_eq, shift=LEFT)
        )
        self.wait(0.5)

        #################################
        # PART 2: Geometric Interpretation
        #################################
        geo_title = Text("Geometric Interpretation", font_size=36).to_edge(UP)
        self.play(FadeIn(geo_title, shift=UP))
        self.wait(1)

        # Create a 4x4 grid of small squares (like graph paper)
        square_size = 0.6
        grid4 = VGroup(*[Square(side_length=square_size, color=BLUE) for _ in range(16)])
        grid4.arrange_in_grid(rows=4, buff=0)
        grid4.center()

        grid4_label = MathTex("4\\times 4").next_to(grid4, DOWN)

        # Animate creation of the 4x4 grid in a lagged style
        self.play(
            LaggedStartMap(
                Create, grid4,
                run_time=3,
                lag_ratio=0.05
            )
        )
        self.play(Write(grid4_label))
        self.wait()

        # Indicate that the grid contains 16 squares.
        sixteen_text = Text("16 squares", font_size=24)
        sixteen_text.next_to(grid4, UP)
        self.play(FadeIn(sixteen_text, shift=UP, run_time=1))
        self.wait(1)
        self.play(FadeOut(sixteen_text, shift=UP, run_time=1))

        # Add 4 squares along the bottom of the 4x4 grid.
        bottom_row = VGroup(*[Square(side_length=square_size, color=GREEN) for _ in range(4)])
        bottom_row.arrange(RIGHT, buff=0)
        bottom_row.next_to(grid4, DOWN, aligned_edge=LEFT, buff=0)
        self.play(LaggedStartMap(Create, bottom_row, lag_ratio=0.1))
        self.wait(1)

        # Add 4 squares along the right side of the 4x4 grid.
        right_col = VGroup(*[Square(side_length=square_size, color=GREEN) for _ in range(4)])
        right_col.arrange(DOWN, buff=0)
        right_col.next_to(grid4, RIGHT, aligned_edge=UP, buff=0)
        self.play(LaggedStartMap(Create, right_col, lag_ratio=0.1))
        self.wait()

        # At this point: 16 + 4 + 4 = 24 squares.
        addition_text = MathTex(r"16 + 4 + 4 = 24")
        addition_text.next_to(grid4, UP, buff=1)
        self.play(Write(addition_text, run_time=2))
        self.wait()
        self.play(FadeOut(addition_text))

        # Add the final square to complete the 5x5 grid.
        last_square = Square(side_length=square_size, color=RED)
        last_square.next_to(bottom_row, RIGHT, buff=0)
        last_square.align_to(right_col, DOWN)
        self.play(Create(last_square))
        self.wait(1)

        # Group everything to represent the complete 5x5 grid.
        grid5 = VGroup(grid4, bottom_row, right_col, last_square)
        complete_label = MathTex("5\\times 5").next_to(grid5, DOWN)
        self.play(Write(complete_label))
        self.wait(1)

        # Optionally, show the total count: 16 + 4 + 4 + 1 = 25.
        total_text = MathTex("16 + 4 + 4 + 1 = 25").next_to(complete_label, DOWN)
        self.play(Write(total_text, run_time=2))
        self.wait()

        # Fade out geometry
        self.play(
            FadeOut(geo_title, shift=UP),
            FadeOut(grid5, shift=LEFT),
            FadeOut(grid4_label),
            FadeOut(complete_label),
            FadeOut(total_text)
        )
        self.wait(0.5)

        #################################
        # PART 3: Calculus Perspective
        #################################
        calc_title = Text("Calculus Perspective", font_size=36)
        calc_title.to_edge(UP)
        self.play(FadeIn(calc_title, shift=UP))
        self.wait(1)

        # Show the function and its derivative.
        func_text = MathTex(r"f(x)=x^2")
        deriv_text = MathTex(r"f'(x)=2x")

        func_text.to_edge(UP, buff=1)
        deriv_text.next_to(func_text, DOWN, buff=0.5)

        self.play(Write(func_text), Write(deriv_text))
        self.wait()

        # Demonstrate the finite difference approximation:
        approx_text = MathTex(r"101^2-100^2=2\cdot100+1=201")
        approx_text.next_to(deriv_text, DOWN, buff=1)
        self.play(Write(approx_text))
        self.wait(1)

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
        axes.shift(DOWN*1.5)
        graph = axes.plot(lambda x: x**2, color=BLUE)

        self.play(Create(axes), run_time=2)
        self.play(Create(graph), run_time=3)
        self.wait(1)

        # Mark two points on the curve (at x = 4.1 and x = 4.9).
        p1 = axes.coords_to_point(4.1, 4.1**2)
        p2 = axes.coords_to_point(4.9, 4.9**2)
        dot1 = Dot(p1, color=RED)
        dot2 = Dot(p2, color=RED)
        self.play(
            FadeIn(dot1, scale=0.7),
            FadeIn(dot2, scale=0.7),
            run_time=1.5
        )
        self.wait(1)

        # Draw the secant line between these points.
        secant = Line(p1, p2, color=GREEN)
        self.play(Create(secant), run_time=2)
        self.wait(1)

        # Annotate the slope of the secant.
        slope_calc = MathTex(r"\frac{4.9^2-4.1^2}{4.9-4.1}\approx 4.5")
        slope_calc.to_edge(RIGHT, buff=1)
        self.play(Write(slope_calc), run_time=2)
        self.wait(2)

        # Fade out the calculus part
        self.play(
            FadeOut(calc_title, shift=UP),
            FadeOut(func_text),
            FadeOut(deriv_text),
            FadeOut(approx_text),
            FadeOut(slope_text),
            FadeOut(axes),
            FadeOut(graph),
            FadeOut(dot1),
            FadeOut(dot2),
            FadeOut(secant),
            FadeOut(slope_calc),
        )
        self.wait(0.5)

        ##############################
        # Conclusion
        ##############################
        # Create the conclusion text
        conclusion = Text("Algebra, Geometry, and Calculus all reveal the beauty of math!", font_size=36)
        conclusion.to_edge(DOWN)

        # Algebra symbol: re-create the general equation
        algebra_symbol = MathTex(r"(x+1)^2 - x^2 = 2x+1").scale(0.7)

        # Geometry symbol: a small grid of squares
        square_size = 0.3
        grid = VGroup(*[Square(side_length=square_size, color=BLUE) for _ in range(9)])
        grid.arrange_in_grid(rows=3, buff=0.1)
        geometry_symbol = grid

        # Calculus symbol: small axes with graph, two dots, and a secant line
        axes_small = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 25, 5],
            x_length=3,
            y_length=3,
            tips=False,
        )
        graph = axes_small.plot(lambda x: x**2, color=BLUE)
        # Mark two points and draw a secant line
        p1 = axes_small.coords_to_point(2, 2**2)
        p2 = axes_small.coords_to_point(3, 3**2)
        dot1 = Dot(p1, color=RED).scale(0.7)
        dot2 = Dot(p2, color=RED).scale(0.7)
        secant = Line(p1, p2, color=GREEN)
        calculus_symbol = VGroup(axes_small, graph, dot1, dot2, secant)

        # Arrange the symbols horizontally at the top of the screen
        symbols = VGroup(algebra_symbol, geometry_symbol, calculus_symbol).arrange(RIGHT, buff=1)
        symbols.to_edge(UP)

        # Animate the symbols and conclusion text
        self.play(FadeIn(symbols, shift=DOWN, run_time=2))
        self.play(FadeIn(conclusion, shift=UP, run_time=2))
        self.wait(3)
        self.play(
            FadeOut(conclusion, shift=DOWN, run_time=2),
            FadeOut(symbols, shift=UP, run_time=2)
        )