from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
from manim_voiceover.services.azure import AzureService
from manim_voiceover.services.recorder import RecorderService
import numpy as np  # For mathematical functions like np.sin

# Flag to include or exclude narration
INCLUDE_NARRATION = 1  # Set to True to include narratio
FANCY_NARRATION = 1
NARRARATOR_VOICE = "en-US-SteffanNeural"
INTRO = 1
DRAW_SIN = True

class BoundedFunctionsWithNarration(VoiceoverScene):
    def construct(self):            
        # Initialize the gTTS voiceover service if narration is included
        if FANCY_NARRATION:
            service = RecorderService()
            #service = AzureService(voice=NARRARATOR_VOICE)
        else:
            service = GTTSService(lang="en", tld="com")
            
        if INCLUDE_NARRATION:
            self.set_speech_service(service)
            self.add_sound("Zeta.mp3", gain=-23)

        if INTRO:
            # --- Introduction ---
            self.wait(2)
            intro_text = "My math proffessor would go on and on about bounded functions."
            self.voiceover_or_play(None, text=intro_text)
            intro_text = "What Even is a Bounded Function?"
            intro_text2 = "But What Even is a Bounded Function?"
            title = Text(intro_text, font_size=50, color=BLUE)
            self.voiceover_or_play(Write(title), text=intro_text2)
            self.wait(1)
            self.play(Uncreate(title))

        def voiceover_or_play(self, animation, text=""):
            """
            Helper method to conditionally include voiceover and synchronize it with animations.
            If INCLUDE_NARRATION is True, it uses voiceover; otherwise, it plays the animation normally.
            """
            if INCLUDE_NARRATION:
                with self.voiceover(text=text) as tracker:
                    if animation is not None:
                        self.play(animation, run_time=tracker.duration)
            elif animation is not None:
                self.play(animation)

        

            intro_description = "In this video, we are going to figure out what it means for a function to be bounded."
            intro_description2 = "and how to determine if a tricky one is bounded or not."
            #intro_description3 = "Tracking the behavior of a function as it grows is a vital and basics of investigating a function."
            intro_description3 = "An introduction to investigating functions"
            title = Text(intro_description3, font_size=50)
            self.voiceover_or_play(Write(title), text=intro_description)
            self.wait(1)
            self.voiceover_or_play(None, text=intro_description2)
            #self.wait(1)
            #self.voiceover_or_play(None, text=intro_description3)
            self.play(Uncreate(title))

        if DRAW_SIN:
            # --- Section 1: What Is a Bounded Function? ---
            heading_text = "Here's an example that sums it up perfectly:"
            heading = Text(heading_text, font_size=40).to_edge(UP)
            self.voiceover_or_play(Write(heading), text=heading_text)
            
            # Create axes and scale them to fit within the screen
            axes = Axes(
                x_range=[-6, 6, 2],  # x-axis range
                y_range=[-2.8, 2.8, 1],    # y-axis range
                axis_config={"include_tip": False}
              )  # Scale the axes and shift them down
            
            # Create axes and scale them to fit within the screen
            axes_full_size = Axes(
                x_range=[-6, 6, 2],  # x-axis range
                y_range=[-3, 2.9, 1],    # y-axis range
                axis_config={"include_tip": False}
            ).add_coordinates()  # Scale the axes and shift them down

            # Plot sine function
            sine_curve = axes.plot(np.sin, color=BLUE, x_range=[-6, 6])
            sine_label = MathTex("f(x) = \\sin(x)", color=BLUE).next_to(axes, DOWN * 1.5)

            sine_description = "Here is a sine function, classically used to model waves."
            self.voiceover_or_play(
                Succession(
                    Create(axes),
                    Create(sine_curve),
                    Write(sine_label)
                ),
                text=sine_description
            )

        bound_description =  "Basically for a function to be bounded, it must stop growing at some point."
        bound_description2 = "in simple terms this means that a horizontal line exists with no part of the function above it for an upper bound, or below it for a lower bound."

        self.voiceover_or_play(None, text=bound_description)
        self.wait(1)
        self.voiceover_or_play(None, text=bound_description2)

        # Create horizontal dashed lines for the upper and lower bounds
        badBound = DashedLine(
            start=axes.c2p(-6, 0.5), 
            end=axes.c2p(6, 0.5),    
            color=RED
        )

        bad_example = 'Lets give an example of what is not a bound line.'
        self.voiceover_or_play(Create(badBound), text=bad_example)
        self.wait(1)

        bad_bound_description = (
            "if I were to draw a horizontal line at y equals half, "
            "the sine function would both cross that line and have values below and above the line."
        )

        # Create a red label "Invalid Line"
        invalid_label = Tex("Invalid Bound", color=RED).next_to(badBound, UP * 2).shift(LEFT * 1.7)

        self.voiceover_or_play(Write(invalid_label), text=bad_bound_description)
        self.wait(2)

        self.play(Unwrite(invalid_label))

        good_bound = 'An example of a valid upper bound would be y equals 2'
        upper_bound = DashedLine(
            start=axes.c2p(-6, 2),  # Start at the left edge of the axes at y = 1
            end=axes.c2p(6, 2),     # End at the right edge of the axes at y = 1
            color=RED
        )
        upper_bound2 = DashedLine(
            start=axes.c2p(-6, 2),  # Start at the left edge of the axes at y = 1
            end=axes.c2p(6, 2),     # End at the right edge of the axes at y = 1
            color=YELLOW
        )
        # Create a red label "Invalid Line"
        valid_label = Tex("Valid Upper Bound", color=YELLOW).next_to(badBound, UP * 2).shift(LEFT * 1.8)
        self.voiceover_or_play(
            Succession(
                Transform(badBound, upper_bound), 
                Transform(badBound, upper_bound2),
                Write(valid_label)
            ),
            text=good_bound
            )
        self.remove(upper_bound, upper_bound2)
        self.play(Unwrite(valid_label))

        good_bound_description = "In this example there would never be a value for f of x that's greater than y equals 2."
        good_bound_description2 = "Something interesting to note is it doesn't have to be as low as possible to be considered a legitimate upper bound to the function."
        self.voiceover_or_play(None, text=good_bound_description)
        self.wait(1)
        self.voiceover_or_play(None, text=good_bound_description2)

        bestUpperBound = 'Of course the closest fitting upper bound would be y equals 1'
        # Create horizontal dashed lines for the upper and lower bounds
        best_upper_bound = DashedLine(
            start=axes.c2p(-6, 1),  # Start at the left edge of the axes at y = 1
            end=axes.c2p(6, 1),     # End at the right edge of the axes at y = 1
            color=YELLOW
        )
        best_upper_bound_green = DashedLine(
            start=axes.c2p(-6, 1),  # Start at the left edge of the axes at y = 1
            end=axes.c2p(6, 1),     # End at the right edge of the axes at y = 1
            color=PURE_GREEN
        )
        valid_label = Tex("Best Fitting Upper Bound", color=PURE_GREEN).next_to(best_upper_bound_green, UP * 2).shift(LEFT * 2)
        self.voiceover_or_play(Transform(badBound, best_upper_bound), text=bestUpperBound)
        self.play(Transform(badBound, best_upper_bound_green))
        self.remove(best_upper_bound, best_upper_bound_green)
        bestLowerBound = 'and the best fitting lower bound would be y equals negative 1'
        bad_lower_bound = DashedLine(
            start=axes.c2p(-6, -2.5),  # Start at the left edge of the axes at y = -1
            end=axes.c2p(6, -2.5),     # End at the right edge of the axes at y = -1
            color=YELLOW
        )
        lower_bound = DashedLine(
            start=axes.c2p(-6, -1),  # Start at the left edge of the axes at y = -1
            end=axes.c2p(6, -1),     # End at the right edge of the axes at y = -1
            color=YELLOW
        )
        lower_bound_green = DashedLine(
            start=axes.c2p(-6, -1),  # Start at the left edge of the axes at y = -1
            end=axes.c2p(6, -1),     # End at the right edge of the axes at y = -1
            color=PURE_GREEN
        )
        self.voiceover_or_play(
            Succession(
                Transform(bad_lower_bound, lower_bound),
                Transform(bad_lower_bound, lower_bound_green),
                Write(valid_label)
            ),
            text=bestLowerBound)
        self.remove(lower_bound_green, lower_bound)
        self.play(Unwrite(valid_label))

        #sine_label = MathTex("f(x) = \\sin(x)", color=BLUE).next_to(axes, DOWN * 1.5)
        bound_text = MathTex(r"-1 \leq \sin(x) \leq 1", color=BLUE).next_to(axes, DOWN * 1.5)
        bound_description = "One would say the function is bounded between negative one and one."
        self.voiceover_or_play(
            Succession(
                Transform(sine_label, bound_text), 
                Indicate(sine_label)
            ),
            text=bound_description)
        self.remove(bound_text)
        self.wait(2)

        # Prepare linear function
        linear_curve = axes.plot(lambda x: x/2, color=BLUE, x_range=[-6, 6])
        linear_label = MathTex("f(x) = x", color=BLUE).next_to(axes, DOWN)

        # Transition from sine to linear function
        transform_text = "Now, let's see an example of a functions with no bounds."
        # Animate transformation
        self.voiceover_or_play(
            Succession(
                Uncreate(heading),
                Uncreate(badBound),
                Uncreate(bad_lower_bound),
                Transform(axes, axes_full_size),
                Transform(sine_curve, linear_curve),
                Transform(sine_label, linear_label)
            ),
            text=transform_text
        )
        self.remove(linear_label)

        badBound = DashedLine(
            start=axes.c2p(-6, 1), 
            end=axes.c2p(6, 1),    
            color=RED
        )
        badBound2 = DashedLine(
            start=axes.c2p(-6, -2), 
            end=axes.c2p(6, -2),    
            color=RED
        )
        badBound3 = DashedLine(
            start=axes.c2p(-6, 2.5), 
            end=axes.c2p(6, 2.5),    
            color=RED
        )

        unbounded_description = "In this case it's clear that any horizontal line we chose would be crossed by the function, and have an infinite number of points above and below the bound"
        self.voiceover_or_play(
            Succession(
                Create(badBound),
                Transform(badBound, badBound2),
                Transform(badBound, badBound3)
            ),
            text=unbounded_description
        )
        self.remove(badBound2, badBound3)
        self.play(Uncreate(badBound))
        self.wait(1)

        # Clean up before next section
        self.play(
            Succession(
                Uncreate(sine_label),
                Uncreate(linear_curve),
                Uncreate(sine_curve),
                Uncreate(axes)
            )
        )

        # --- Section 2: Bounds, Maximum, and Supremum ---
        max_description = "Let's define some helpful terms to choose where the closest fitting boundary should go."
        max_description2 = 'To do this we will use the maximum and the supremum.'
        self.voiceover_or_play(None, text=max_description)
        new_heading_text = "Maximum vs Supremum"
        new_heading = Text(new_heading_text, font_size=40)
        self.voiceover_or_play(
            Create(new_heading),
            text=max_description2
        )

        max_description2 = "what even is the difference between the two? they both sound like the highest point of a function."
        self.voiceover_or_play(Uncreate(new_heading), text=max_description2)

        # Plot bounded parabola
        parabola_axes = Axes(
            x_range=[-3, 3, 1], y_range=[-1, 5, 1],
            axis_config={"include_tip": False}
        ).add_coordinates()

        parabola_curve = parabola_axes.plot(lambda x: -x**2 + 4, color=BLUE, x_range=[-2, 2])
        parabola_label = MathTex("f(x) = -x^2 + 4", color=BLUE).next_to(parabola_axes, DOWN)

        parabola_description = "Let's give a parabola as an example."
        self.voiceover_or_play(
            Succession(
                Create(parabola_axes),
                Write(parabola_label),
                Create(parabola_curve)
            ),
            text=parabola_description
        )
        self.wait(1)

        # Highlight maximum
        max_point = Dot(parabola_axes.c2p(0, 4), color=RED)
        max_label = MathTex("\\text{Maximum} = 4", color=RED).next_to(max_point, UP + RIGHT)

        max_description = "The maximum point of the parabola is at y equals four."
        self.voiceover_or_play(
            Succession(
                Create(max_point),
                Write(max_label)
            ),
            text=max_description
        )
        self.wait(1)

        supremum_label = MathTex("\\text{Supremum} = 4", color=RED).next_to(max_point, UP + RIGHT)
        max_description = "In a case where there is a defined maximum then that point is also called the supremum."
        self.voiceover_or_play(
                Transform(max_label, supremum_label), text=max_description)
        self.wait(1)
        self.remove(supremum_label)

        # Highlighting the supremum on the plot with a green line
        supremum_line = DashedLine(
            start=parabola_axes.c2p(-3, 4),    # Start at the left-most point of the plot
            end=parabola_axes.c2p(3, 4),       # End at the right-most point of the plot
            color=GREEN                     # Green line to represent the supremum
        )

        # Add the supremum line and label to the scene
        supremum_description4 = "Here, the closes fitting upper bound is clearly the same as the maximum."
        self.voiceover_or_play(
            Create(supremum_line), 
            text=supremum_description4
        )
        self.wait(2)

        supremum_description = "But cases do exist where the numbers converge on a maximum point without ever quite reaching it."
        self.voiceover_or_play(
            Succession(
                Uncreate(supremum_line),
                Uncreate(max_label),
                Uncreate(max_point)
                ),
            text=supremum_description
        )
        self.wait(1)

        # Plot bounded limit
        limit_axes = Axes(
            x_range=[-1, 50, 5], y_range=[-1, 5, 1],
            axis_config={"include_tip": False}
        ).add_coordinates()

        limit_curve = limit_axes.plot(lambda x: -1/x + 4 if x != 0 else 0, color=BLUE, x_range=[0.18, 50])
        limit_label = MathTex(r"f : \mathbb{R}^+ \to \mathbb{R}, \quad f(x) = -\frac{1}{x} + 4", color=WHITE).to_edge(UP)

        supremum_description2 = 'For example, in the given function it clearly stops growing at y equals four.'
        self.voiceover_or_play(
            Succession(
                Uncreate(parabola_curve),
                Uncreate(parabola_label),
                FadeOut(parabola_axes),
                FadeIn(limit_axes),
                Create(limit_curve),
                Create(limit_label)
                ),
            text=supremum_description2
        )
        self.wait(1)

        supremum_description3 = (
            "But at the same time, this function has no maximum ."
        )
        self.voiceover_or_play(None, text=supremum_description3)

        closer_description = "If we take an x of 45, the value of y gets close to four, "
        example_point1 = Dot(limit_axes.c2p(45, -1/45 + 4), color=YELLOW)
        example_label1 = MathTex("f(45) \\approx 3.99", color=YELLOW).next_to(example_point1, LEFT + DOWN)
        self.voiceover_or_play(
            Succession(
                Create(example_point1),
                Write(example_label1)
            ),
            text = closer_description
        )
        self.wait(1)

        closer_description = "But for 46, y gets even closer to 4 "
        example_point2 = Dot(limit_axes.c2p(46, -1/46 + 4), color=GREEN)
        example_label2 = MathTex("f(46) \\approx 3.999", color=GREEN).next_to(example_point2, LEFT + DOWN * 3.5)
        self.voiceover_or_play(
            Succession(
                Create(example_point2),
                Write(example_label2)
            ),
            text=closer_description
        )
        self.wait(1)

        general_description = (
            "This is true For any value of x we choose, that's why this function has no maximum"
        )
        self.voiceover_or_play(
            Succession(
                Uncreate(example_label1),
                Uncreate(example_label2),
                Uncreate(example_point1),
                Uncreate(example_point2)
            ),
            text=general_description
        )
        self.wait(1)

        # Highlighting the supremum on the plot
        supremum_line = DashedLine(
            start=limit_axes.c2p(0, 4),  # Start at the left-most point of the plot
            end=limit_axes.c2p(50, 4),   # End at the right-most point of the plot
            color=GREEN
        )
        supremum_label = MathTex(r"\text{Supremum} = 4", color=GREEN).next_to(supremum_line, DOWN)

        supremum_description4 = (
            "In the simplest of terms, the supremum is the highest value that the function approaches."
        )
        self.voiceover_or_play(
            Succession(
                Create(supremum_line),
                Write(supremum_label)
            ),
            text=supremum_description4
        )
        self.wait(1)

        # Clean up and transition
        self.play(
            Succession(
                Uncreate(supremum_line),
                Uncreate(supremum_label),
                Uncreate(limit_label),
                Uncreate(limit_curve),
                Uncreate(limit_axes)
            )
        )

        bye = "Thank you for watching! I hope this video helped clear up some of the confusion around bounded functions, maxima, and suprema. If you found it helpful, feel free to like, share, and subscribe for more insights into mathematical concepts. See you in the next one!"
        self.voiceover_or_play(None, text=bye)
        self.wait(2)

