from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import numpy as np  # For mathematical functions like np.sin

# Flag to include or exclude narration
# Flag to include or exclude narration
INCLUDE_NARRATION = 0  # Set to True to include narratio
FANCY_NARRATION = INCLUDE_NARRATION
NARRARATOR_VOICE = "en-US-SteffanNeural"
INTRO = 1
DRAW_SIN = True

class BoundedFunctionsWithNarration(VoiceoverScene):
    def construct(self):
        # --- Section 2: Bounds, Maximum, and Supremum ---
        new_heading_text = "Bounds, Maximum, and Supremum"
        new_heading = Text(new_heading_text, font_size=40).to_edge(UP)
        service = GTTSService(lang="en", tld="com")
        if INCLUDE_NARRATION:
            self.set_speech_service(service)
        self.voiceover_or_play(
            Create(new_heading),
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