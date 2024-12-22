from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService

INCLUDE_NARRATION = True
FANCY_NARRATION = True
NARRATOR_VOICE = "en-US-SteffanNeural"

class FibonacciRecursionVsDP(VoiceoverScene):
    def construct(self):
        if FANCY_NARRATION:
            service = AzureService(voice=NARRATOR_VOICE)
        else:
            service = None
        if INCLUDE_NARRATION and service:
            self.set_speech_service(service)

        title = Text("Recursion vs Dynamic Programming", font_size=36).to_edge(UP)
        intro = (
            "Naive recursion for Fibonacci numbers recalculates the same values many times, leading to exponential complexity."
        )
        self.voiceover_or_play(FadeIn(title), text=intro)
        self.wait(2)

        # Show a small recursion tree for F_5 for brevity
        f5 = MathTex("F_{5}")
        f4 = MathTex("F_{4}").next_to(f5, LEFT+DOWN)
        f3 = MathTex("F_{3}").next_to(f5, RIGHT+DOWN)
        self.play(FadeIn(f5), FadeIn(f4), FadeIn(f3))
        self.wait(1)

        explanation = "Notice how to compute F_5, we need F_4 and F_3, and each of those need more calls, repeating calculations."
        self.voiceover_or_play(None, text=explanation)
        self.wait(2)

        # Highlight repetition if desired
        repeat_text = "Dynamic Programming solves this by storing previously computed results."
        self.voiceover_or_play(None, text=repeat_text)
        self.wait(2)

        # Show DP array
        dp_vals = [1,1,2,3,5]
        dp_boxes = VGroup()
        for i,v in enumerate(dp_vals):
            box = Square(0.4).shift(RIGHT*i*0.5+DOWN*1)
            val = Tex(str(v)).scale(0.7).move_to(box)
            dp_boxes.add(VGroup(box,val))

        dp_title = Text("Dynamic Programming", font_size=24).next_to(dp_boxes, UP)
        self.play(FadeIn(dp_title))
        for pair in dp_boxes:
            self.play(Create(pair[0]), Write(pair[1]))
            self.wait(0.5)

        recap = "With DP, each Fibonacci value is computed once, reducing complexity from exponential to linear."
        self.voiceover_or_play(None, text=recap)
        self.wait(2)

        self.play(FadeOut(dp_boxes), FadeOut(dp_title), FadeOut(f5), FadeOut(f4), FadeOut(f3), FadeOut(title))
        self.wait(1)