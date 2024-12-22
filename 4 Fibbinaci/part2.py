from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService

INCLUDE_NARRATION = True
FANCY_NARRATION = True
NARRATOR_VOICE = "en-US-SteffanNeural"

class FibonacciStairsCode(VoiceoverScene):
    def construct(self):
        if FANCY_NARRATION:
            service = AzureService(voice=NARRATOR_VOICE)
        else:
            service = None
        if INCLUDE_NARRATION and service:
            self.set_speech_service(service)

        title = Text("Climbing Stairs Problem", font_size=36).to_edge(UP)
        intro_text = (
            "Consider a staircase: if you can climb either 1 or 2 steps at a time, how many ways to reach the top of an n-step staircase?"
        )
        self.voiceover_or_play(FadeIn(title), text=intro_text)
        self.wait(2)

        stair_count = 5
        stairs = VGroup()
        for i in range(stair_count):
            step = Square(0.3).shift(RIGHT*i*0.4+UP*i*0.4)
            stairs.add(step)
        stairs.move_to(DOWN*1.5+LEFT*1.5)

        ways_explanation = (
            "For 1 step: 1 way. For 2 steps: 2 ways. For 3 steps: 3 ways. "
            "This pattern repeats the Fibonacci logic: ways(n) = ways(n-1) + ways(n-2)."
        )
        self.voiceover_or_play(Create(stairs), text=ways_explanation)
        self.wait(2)

        ways = [1,2,3,5,8]
        ways_labels = VGroup()
        for i,w in enumerate(ways):
            lbl = Tex(str(w)).next_to(stairs[i], UP)
            ways_labels.add(lbl)
        for lbl in ways_labels:
            self.play(Write(lbl))
            self.wait(0.5)

        # Show a Python code snippet as text
        code_text = (
            "def climb_stairs(n):\n"
            "    if n <= 2:\n"
            "        return n\n"
            "    dp = [0]*(n+1)\n"
            "    dp[1], dp[2] = 1, 2\n"
            "    for i in range(3, n+1):\n"
            "        dp[i] = dp[i-1] + dp[i-2]\n"
            "    return dp[n]"
        )

        code_mob = Text(code_text, font="Courier", font_size=24).to_edge(RIGHT)
        self.voiceover_or_play(FadeIn(code_mob), text=(
            "Here's how you'd implement it in Python. This uses dynamic programming to compute the number of ways efficiently."
        ))
        self.wait(4)

        recap = "Just like rabbits, the staircase problem leads us back to the Fibonacci pattern."
        self.voiceover_or_play(None, text=recap)
        self.wait(2)

        self.play(FadeOut(ways_labels), FadeOut(stairs), FadeOut(code_mob), FadeOut(title))
        self.wait(1)