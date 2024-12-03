from manim import *
import numpy as np

class ColorChangingShape(Scene):
    def __init__(self):
        super().__init__()
        self.colors = [PURE_RED, ORANGE, YELLOW, PURE_GREEN, BLUE, "#A020F0"]
        self.directions = [
                        RIGHT * 5, 
                        RIGHT * 5, 
                        DOWN * 4, 
                        LEFT * 5,
                        LEFT * 5
                    ]
        self.old_shapes = []
        self.shape_tracker = 0
        self.color_tracker = 0
        self.shape_types = self.initialize_shapes()

    def initialize_shapes(self):
        """Initialize the shapes with consistent properties."""
        shapes = [
            RegularPolygon(3),  # Triangle
            RegularPolygon(4).rotate(PI / 4),  # Square
            RegularPolygon(5),  # Pentagon
            RegularPolygon(6),  # Hexagon
            RegularPolygon(7),  # Septagon
            Circle(),  # Circle
        ]
        for shape in shapes:
            shape.set_stroke(WHITE)
        return shapes

    def update_color_tracker(self):
        """Cycle through the color list."""
        self.color_tracker = (self.color_tracker + 1) % len(self.colors)

    def animate_shape(self, shape, shift_direction):
        """Animate the shape's movement and color change."""
        self.update_color_tracker()
        self.play(
            shape.animate.shift(shift_direction)
                 .set_fill(self.colors[self.color_tracker])
        )

    def change_shape(self, current_shape):
        """Transform the current shape into the next shape."""
        self.shape_tracker = (self.shape_tracker + 1) % len(self.shape_types)
        new_shape = self.shape_types[self.shape_tracker].copy()
        new_shape.set_fill(self.colors[self.color_tracker], opacity=0.8)
        new_shape.move_to(current_shape.get_center())
        self.play(Transform(current_shape, new_shape))
        self.old_shapes.append(current_shape)
        return new_shape

    def construct(self):
        """Construct the scene."""
        # Create the initial shape
        shape = self.shape_types[0].copy()
        self.add_sound("Zeta.mp3")
        shape.set_fill(self.colors[self.color_tracker], opacity=0.8)
        shape.move_to(UP * 2 + LEFT * (config.frame_x_radius - 2))
        shape2 = shape.copy()

        text = "A Rainbow of all shapes and sizes"
        speech_text = Text(text, font_size=40)
        speech_text.move_to(ORIGIN)  # Position text above the circle
        self.play(Write(speech_text))  # Animate the text appearing
        self.wait(1.5)

        # Animate the text with color cycling
        colors = [PURE_RED, ORANGE, YELLOW, PURE_GREEN, BLUE, "#A020F0"]
        for i in range(len(speech_text)):
            color = colors[i % (len(colors))]
            self.play(speech_text[i].animate.set_color(color), run_time=0.3)

        self.play(FadeOut(speech_text))
        self.add(shape)
        self.add(shape2)
        self.old_shapes.append(shape2)

        # Animate the shape's transformations
        for direction in self.directions:
            self.animate_shape(shape, direction)
            shape = self.change_shape(shape)

        self.wait(1)
        
        for old_shape in self.old_shapes:
            self.play(Transform(old_shape, shape))
            self.remove(old_shape)
        
        self.play(shape.animate.shift(UP * 2, RIGHT * 5))

        # Create the building
        building = Rectangle(height=4, width=2.3, color=GRAY)
        building.set_fill(GRAY, opacity=0.5)
        building.move_to(LEFT * 5.2 + DOWN)  # Place building on the left

        # Create the ground
        ground = Line(LEFT * 7, RIGHT * 7, color=GREEN, stroke_width = 7)
        ground.move_to(DOWN * 3)

        # Create the circle (jumper)
        circle = Circle(radius=0.3, color=BLUE)
        circle.set_fill(BLUE, opacity=0.8)
        circle.move_to(building.get_top() + UP * 0.3 + LEFT * 0.4)  # Place on top of the building

        # Add a tree to the grass
        tree_trunk = Rectangle(height=1, width=0.2, color=DARK_BROWN)
        tree_trunk.set_fill(DARK_BROWN, opacity=1)
        tree_trunk.move_to(DOWN * 2.5)

        tree_leaves = Triangle(color=PURE_GREEN)
        tree_leaves.set_fill(PURE_GREEN, opacity=1)
        tree_leaves.scale(0.7)
        tree_leaves.move_to(tree_trunk.get_top() + UP * 0.4)

        tree = VGroup(tree_trunk, tree_leaves)

        # Create the pillow
        pillow = RoundedRectangle(
            width=1, height=0.2, corner_radius=0.2, color=WHITE, fill_opacity = 0.8
        )
        pillow.move_to(RIGHT * 4 + DOWN * 2.8)  # Place it at the landing spot


        # Add objects to the scene
        self.play(Transform(shape, circle))
        speech_text = Text("A Story of a Brave Ball", font_size=40)
        speech_text.move_to(ORIGIN)  # Position text above the circle
        self.play(Write(speech_text))  # Animate the text appearing
        self.wait(3)
        self.play(FadeOut(speech_text))
        self.add(circle)
        self.remove(shape)
        self.play(Create(building))
        self.play(Create(ground))
        self.play(Create(tree))

        # Add speech bubble text
        speech_text = Text("I'm scared to jump!", font_size=24)
        speech_text.next_to(circle, UP * 1.5 + RIGHT)  # Position text above the circle
        self.play(Write(speech_text))  # Animate the text appearing
        self.play(speech_text.animate.scale(3), run_time = 0.2)
        self.play(speech_text.animate.scale(0.3), run_time = 0.2)
        self.play(speech_text.animate.scale(3), run_time = 0.2)
        self.play(speech_text.animate.scale(0.3), run_time = 0.2)
        self.play(speech_text.animate.scale(3), run_time = 0.2)
        self.play(speech_text.animate.scale(1.5), run_time = 0.2)
        self.play(FadeOut(speech_text))

        self.play(circle.animate.shift(RIGHT*1.2))
        # Add speech bubble text
        speech_text = Text("EEP!", font_size=24)
        speech_text.next_to(circle, UP * 1.5 + RIGHT)  # Position text above the circle
        self.play(Write(speech_text))  # Animate the text appearing
        self.play(speech_text.animate.shift(LEFT * 1).scale(3), run_time=0.2)
        self.play(speech_text.animate.shift(RIGHT * 1).scale(0.3), run_time=0.2)
        self.play(speech_text.animate.shift(LEFT * 1).scale(3), run_time=0.2)
        self.play(speech_text.animate.shift(RIGHT * 1).scale(0.3), run_time=0.2)
        self.play(FadeOut(speech_text))

        speech_text = Text("Wait! I see a pillow!", font_size=24)
        speech_text.next_to(circle, UP * 1.5 + RIGHT)  # Position text above the circle
        self.play(Write(speech_text))  # Animate the text appearing
        self.play(FadeOut(speech_text))
        self.play(Create(pillow))


        self.play(circle.animate.shift(LEFT*1.2))


        

        # Add speech bubble text for explanation
        explanation_text = Tex(
            r"The path of my jump follows a parabolic equation:", font_size=28
        )
        explanation_text.next_to(circle, UP * 1.5 + RIGHT)
        equation_text = MathTex(
            r"y = ax^2 + bx + c", font_size=45
        ).next_to(explanation_text, DOWN)
        
        # Animate the speech and equation
        self.play(Write(explanation_text))
        self.play(Write(equation_text))
        self.wait(1)
        self.play(FadeOut(explanation_text))
        self.play(FadeOut(equation_text))

        # Add speech bubble text
        speech_text = Text("Okay if I do this just right and do the math I can land on the pillow!", font_size=30)
        self.wait(1.5)
        speech_text.next_to(circle, UP * 1.5 + RIGHT)  # Position text above the circle
        self.play(Write(speech_text))  # Animate the text appearing
        self.wait(2)
        self.play(FadeOut(speech_text))

        # Define the jump path function
        def jump_path(t):
            # Starting position
            start_x = building.get_top()[0] - 0.4
            start_y = building.get_top()[1] + 0.3

            # Landing position
            end_x = 4
            end_y = -2.4

            # Calculate the trajectory parameters
            peak_x = (start_x + end_x) / 2
            peak_y = max(start_y, end_y) + 4  # Adjust as needed

            # Solve for a, b, c
            coefficients = np.linalg.solve(
                [
                    [start_x**2, start_x, 1],
                    [peak_x**2, peak_x, 1],
                    [end_x**2, end_x, 1],
                ],
                [start_y, peak_y, end_y]
            )
            a, b, c = coefficients

            # Parametric equations
            x = start_x + (end_x - start_x) * t
            y = a * x**2 + b * x + c
            return np.array([x, y, 0])

        # Create the path
        jump_curve = ParametricFunction(jump_path, t_range=[0, 1], color=YELLOW)

        # Animate the jump
        self.play(MoveAlongPath(circle, jump_curve, rate_func=smooth))

        # Simulate a bounce when it hits the ground
        self.play(circle.animate.scale(1.5).shift(UP * 0.5), run_time=0.2)
        self.play(circle.animate.scale(0.6).shift(DOWN * 0.5), run_time=0.2)
        self.play(circle.animate.scale(1.5).shift(UP * 0.5), run_time=0.2)
        self.play(circle.animate.scale(0.6).shift(DOWN * 0.5), run_time=0.2)
        self.play(circle.animate.scale(1.0))

        # Add speech bubble text
        speech_text = Text("I made it!", font_size=24)
        speech_text.next_to(circle, UP * 1.5 + RIGHT)  # Position text above the circle
        self.play(Write(speech_text))  # Animate the text appearing
        self.wait(1)
        self.play(FadeOut(speech_text))

        # End scene with the circle rolling away
        self.play(circle.animate.shift(RIGHT * 5))

        self.play(Uncreate(building))
        self.play(Uncreate(tree))
        self.play(Uncreate(pillow))
        self.play(Uncreate(circle))
        self.play(Uncreate(ground))