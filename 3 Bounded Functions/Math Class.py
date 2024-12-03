from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
from manim_voiceover.services.azure import AzureService
import numpy as np  # For mathematical functions like np.sin

# Flag to include or exclude narration
INCLUDE_NARRATION = 0  # Set to True to include narratio
FANCY_NARRATION = INCLUDE_NARRATION
NARRARATOR_VOICE = "en-US-SteffanNeural"
INTRO = 1
DRAW_SIN = True

class BoundedFunctionsWithNarration(VoiceoverScene):
    def construct(self):            
        # Initialize the gTTS voiceover service if narration is included
        if FANCY_NARRATION:
            service = AzureService(voice=NARRARATOR_VOICE)
        else:
            service = GTTSService(lang="en", tld="com")
        if INCLUDE_NARRATION:
            self.set_speech_service(service)
            self.add_sound("Zeta.mp3", gain=-12)

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
            self.play(FadeOut(title))

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
            self.play(FadeOut(title))

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
        self.voiceover_or_play(None, text=bad_bound_description)
        self.wait(2)

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
        self.voiceover_or_play(
            Succession(
                Transform(badBound, upper_bound), 
                Transform(badBound, upper_bound2),
            ),
            text=good_bound
            )
        self.remove(upper_bound, upper_bound2)

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
                Transform(bad_lower_bound, lower_bound_green)
            ),
            text=bestLowerBound)
        self.remove(lower_bound_green, lower_bound)

        #sine_label = MathTex("f(x) = \\sin(x)", color=BLUE).next_to(axes, DOWN * 1.5)
        bound_text = MathTex(r"-1 \leq \sin(x) \leq 1", color=BLUE).next_to(axes, DOWN * 1.5)
        bound_description = "One would say the function is bounded between negative one and one."
        self.voiceover_or_play(Transform(sine_label, bound_text), text=bound_description)
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
                FadeOut(heading),
                FadeOut(badBound),
                FadeOut(bad_lower_bound),
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
        self.remove(badBound, badBound2, badBound3)
        self.wait(1)

        # Clean up before next section
        self.play(
            Succession(
                FadeOut(linear_curve),
                FadeOut(sine_curve),
                FadeOut(axes)
            )
        )

        # --- Section 2: Bounds, Maximum, and Supremum ---
        new_heading_text = "Bounds, Maximum, and Supremum"
        new_heading = Text(new_heading_text, font_size=40).to_edge(UP)
        self.voiceover_or_play(
            ReplacementTransform(heading, new_heading),
            text=new_heading_text
        )

        # Plot bounded parabola
        parabola_description = "This parabola is bounded with a maximum value at four."
        parabola_axes = Axes(
            x_range=[-3, 3, 1], y_range=[-1, 5, 1],
            axis_config={"include_tip": False}
        ).add_coordinates()
        parabola_curve = parabola_axes.plot(lambda x: -x**2 + 4, color=BLUE, x_range=[-2, 2])
        parabola_label = MathTex("f(x) = -x^2 + 4", color=BLUE).next_to(parabola_axes, DOWN)

        self.voiceover_or_play(
            AnimationGroup(
                Create(parabola_axes),
                Create(parabola_curve),
                Write(parabola_label),
                lag_ratio=0.1
            ),
            text=parabola_description
        )

        # Highlight maximum
        max_point = Dot(parabola_axes.c2p(0, 4), color=RED)
        max_label = MathTex("\\text{Maximum: } 4", color=RED).next_to(max_point, UP)

        max_description = "The maximum point of the parabola is at y equals four."
        self.voiceover_or_play(
            AnimationGroup(
                Create(max_point),
                Write(max_label),
                lag_ratio=0.1
            ),
            text=max_description
        )
        self.wait(1)

        # Continue with further scenes as needed

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