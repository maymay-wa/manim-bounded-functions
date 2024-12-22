from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService

INCLUDE_NARRATION = True
FANCY_NARRATION = True
NARRATOR_VOICE = "en-US-SteffanNeural"

class FibonacciIntroBunny(VoiceoverScene):
    def construct(self):
        # Setup Voiceover
        if FANCY_NARRATION:
            service = AzureService(voice=NARRATOR_VOICE)
        else:
            service = None
        if INCLUDE_NARRATION and service:
            self.set_speech_service(service)

        # Introduction: Fibonacci and what we'll cover
        title = Text("The Fibonacci Sequence", font_size=48)
        intro_text = (
            "The Fibonacci sequence is a simple pattern of numbers that reveals deep mathematical beauty. "
            "Starting with 1 and 1, each term is the sum of the previous two, forming a sequence: 1, 1, 2, 3, 5, 8, 13, ..."
        )
        self.voiceover_or_play(Write(title), text=intro_text)
        self.wait(2)
        self.play(FadeOut(title))
        self.wait(1)

        definition = Text("We will see how Fibonacci helps solve real problems and shows hidden beauty.", font_size=30)
        plan_text = (
            "In this first part, we'll see a classic problem about bunny reproduction. "
            "In upcoming videos, we'll apply Fibonacci logic to climbing stairs, discuss efficient computation, "
            "and explore the golden ratio, connecting mathematics and nature."
        )
        self.voiceover_or_play(FadeIn(definition), text=plan_text)
        self.wait(3)
        self.play(FadeOut(definition))
        self.wait(1)

        # Bunny problem
        bunny_title = Text("The Bunny Problem", font_size=36).to_edge(UP)
        self.voiceover_or_play(FadeIn(bunny_title), text=(
            "Imagine starting with a single pair of newborn rabbits. Each month, each mature pair produces a new pair. "
            "How many pairs will we have after several months?"
        ))
        self.wait(2)

        line = Line(4*LEFT,4*RIGHT)
        self.voiceover_or_play(Create(line), text="Let's track their population month by month.")
        self.wait(1)

        month_marks = VGroup()
        for i in range(6):
            tick = Line(UP*0.1, DOWN*0.1).move_to(line.point_from_proportion(i/6))
            month_label = Text(str(i)).scale(0.6).next_to(tick, DOWN)
            month_marks.add(VGroup(tick, month_label))
        for mark in month_marks:
            self.play(Create(mark[0]), FadeIn(mark[1]), run_time=0.3)
        self.wait(1)

        fib_vals = [1,1,2,3,5,8]
        rabbits_groups = VGroup()
        for i,val in enumerate(fib_vals):
            group = VGroup(*[Dot(radius=0.1) for _ in range(val)]).arrange(UP, buff=0.15)
            group.move_to(line.point_from_proportion(i/6)+UP*1)
            rabbits_groups.add(group)

        explanation = (
            "Month 0: 1 pair. Month 1: still 1 pair. Month 2: 2 pairs. Month 3: 3 pairs. "
            "Each month's total is the sum of the previous two, exactly like Fibonacci numbers."
        )
        self.voiceover_or_play(FadeIn(rabbits_groups[0]), text=explanation)
        self.wait(1)
        for i in range(1,6):
            self.play(FadeIn(rabbits_groups[i]))
            self.wait(0.5)

        recap = "This simple rabbit puzzle gave birth to the Fibonacci sequence concept."
        self.voiceover_or_play(None, text=recap)
        self.wait(2)

        self.play(
            FadeOut(rabbits_groups),
            FadeOut(line),
            FadeOut(month_marks),
            FadeOut(bunny_title)
        )
        self.wait(1)