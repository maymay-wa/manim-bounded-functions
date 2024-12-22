from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService

INCLUDE_NARRATION = True
FANCY_NARRATION = True
NARRATOR_VOICE = "en-US-SteffanNeural"

class FibonacciGoldenRatio(VoiceoverScene):
    def construct(self):
        if FANCY_NARRATION:
            service = AzureService(voice=NARRATOR_VOICE)
        else:
            service = None
        if INCLUDE_NARRATION and service:
            self.set_speech_service(service)

        title = Text("The Golden Ratio", font_size=36).to_edge(UP)
        self.voiceover_or_play(FadeIn(title), text=(
            "As the Fibonacci numbers grow, the ratio of successive terms approaches the golden ratio, about 1.618."
        ))
        self.wait(2)

        ratio = MathTex(r"\frac{F_{14}}{F_{13}} \approx 1.618").move_to(UP*1)
        self.play(Write(ratio))
        self.wait(1)
        explain = (
            "This magical number appears in art, architecture, and nature. "
            "Interestingly, 1.618 is close to 1.609, the factor to convert mph to kph."
        )
        self.voiceover_or_play(None, text=explain)
        self.wait(2)

        note = Text("1 mph ≈ 1.609 kph; Golden Ratio ≈ 1.618", font_size=24).next_to(ratio, DOWN*2)
        self.play(FadeIn(note))
        self.wait(2)

        # Optionally show a golden rectangle
        golden_rect = Rectangle(width=2, height=2/1.618, color=YELLOW).next_to(ratio, RIGHT, buff=1)
        self.play(Create(golden_rect))
        self.wait(2)

        final = "From a simple sequence to real-world applications and natural aesthetics, Fibonacci teaches us about interconnectedness."
        self.voiceover_or_play(None, text=final)
        self.wait(3)

        self.play(FadeOut(title), FadeOut(ratio), FadeOut(note), FadeOut(golden_rect))
        self.wait(1)