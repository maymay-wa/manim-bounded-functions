from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService
from manim_voiceover.services.gtts import GTTSService
import numpy as np

# Flags for narration and styles
INCLUDE_NARRATION = True
FANCY_NARRATION = True
NARRATOR_VOICE = "en-US-SteffanNeural"

class FibonacciExplainer(VoiceoverScene):
    def construct(self):
        # Setup Voiceover Service
        if FANCY_NARRATION:
            service = AzureService(voice=NARRATOR_VOICE)
        else:
            service = GTTSService(lang="en", tld="com")

        if INCLUDE_NARRATION:
            self.set_speech_service(service)

        # Intro Section
        self.show_introduction()

        # Fibonacci Definition (before bunny problem)
        self.define_fibonacci()

        # Bunny Problem Section
        self.bunny_problem()

        # Climbing Stairs Section
        self.climbing_stairs()

        # Recursion vs DP Section
        self.recursion_vs_dp()

        # Golden Ratio Section
        self.golden_ratio_section()

        # Efficiency and Conclusion
        self.efficiency_conclusion()

    def voiceover_or_play(self, animation, text=""):
        if INCLUDE_NARRATION:
            with self.voiceover(text=text) as tracker:
                if animation is not None:
                    self.play(animation, run_time=tracker.duration)
        else:
            if animation is not None:
                self.play(animation)

    def show_introduction(self):
        # Show main title
        title = Text("The Fibonacci Sequence", font_size=48)
        subtitle = Text("Leonardo of Pisa (Fibonacci), 1170–1250", font_size=36)
        intro_text = (
            "In the early 13th century, Leonardo of Pisa, known as Fibonacci, "
            "introduced Europe to a simple yet powerful sequence in his book 'Liber Abaci'."
        )
        intro_subtext = (
            "This sequence, although studied earlier in India, gained widespread recognition in Europe "
            "thanks to his work."
        )

        self.voiceover_or_play(Write(title), text=intro_text)
        self.wait(2)
        self.voiceover_or_play(Transform(title, subtitle), text=intro_subtext)
        self.wait(2)
        self.play(FadeOut(subtitle))
        self.wait(1)

    def define_fibonacci(self):
        # Introduce Fibonacci sequence definition before showing rabbits
        define_text = Text("Defining the Fibonacci Sequence", font_size=36)
        self.voiceover_or_play(FadeIn(define_text), text=(
            "The Fibonacci sequence starts with 1 and 1, "
            "and each new term after that is the sum of the previous two terms."
        ))
        self.wait(2)
        self.play(FadeOut(define_text))

        fib_seq = MathTex("1,\,1,\,2,\,3,\,5,\,8,\,13,\dots").scale(1.2)
        self.voiceover_or_play(Write(fib_seq), text=(
            "So it begins: one, one, then two, three, five, eight, thirteen, and so on. "
            "This pattern emerges in many unexpected places."
        ))
        self.wait(3)
        self.play(fib_seq.animate.to_edge(UP))
        self.wait(1)

    def bunny_problem(self):
        # Introduce the bunny problem slowly
        bunny_title = Text("The Rabbit Problem", font_size=36).to_edge(UP)
        intro_bunny_text = (
            "A classic example: how quickly do rabbits breed under idealized conditions? "
            "Imagine starting with a single pair of newborn rabbits."
        )
        self.voiceover_or_play(FadeIn(bunny_title), text=intro_bunny_text)
        self.wait(2)

        # Timeline
        line = Line(4*LEFT, 4*RIGHT)
        months_desc = "Let's track their population month by month."
        self.voiceover_or_play(Create(line), text=months_desc)
        self.wait(1)

        month_marks = VGroup()
        for i in range(6):
            tick = Line(UP*0.1, DOWN*0.1).move_to(line.point_from_proportion(i/6))
            month_label = Text(str(i)).scale(0.6).next_to(tick, DOWN)
            month_marks.add(VGroup(tick, month_label))

        for mark in month_marks:
            self.play(Create(mark[0]), FadeIn(mark[1]), run_time=0.5)

        self.wait(1)

        # Show rabbit counts step-by-step, pausing in between
        fib_vals = [1,1,2,3,5,8]
        rabbits_groups = VGroup()
        for i, val in enumerate(fib_vals):
            # Represent rabbits as small dots
            rabbit_group = VGroup(*[Circle(radius=0.1, fill_opacity=1, color=WHITE).shift(UP*(0.2*j)) for j in range(val)])
            pos = line.point_from_proportion(i/6) + UP*1
            rabbit_group.move_to(pos)
            rabbits_groups.add(rabbit_group)

        bunny_expl_text = (
            "At month 0, we have just 1 pair. "
            "At month 1, still 1 pair. "
            "By month 2, the original pair reproduces, giving us 2 pairs in total. "
            "At month 3, we now have 3 pairs, and so on."
        )
        # Show first month slowly
        self.voiceover_or_play(FadeIn(rabbits_groups[0]), text=bunny_expl_text)
        self.wait(2)
        for i in range(1, 6):
            self.play(FadeIn(rabbits_groups[i]))
            self.wait(1)
            if i >= 2:
                arrow_prev = Arrow(line.point_from_proportion((i-1)/6)+UP*0.5,
                                   line.point_from_proportion(i/6)+UP*0.5,
                                   buff=0.1, stroke_width=2, color=YELLOW)
                arrow_prev2 = Arrow(line.point_from_proportion((i-2)/6)+UP*0.3,
                                    line.point_from_proportion(i/6)+UP*0.3,
                                    buff=0.1, stroke_width=2, color=YELLOW)
                self.play(Create(arrow_prev), Create(arrow_prev2))
                self.wait(1)
                self.play(FadeOut(arrow_prev), FadeOut(arrow_prev2))

        final_desc = (
            "This matches our definition: each month's count is the sum of the previous two. "
            "This is exactly how Fibonacci numbers are formed."
        )
        self.voiceover_or_play(None, text=final_desc)
        self.wait(2)

        self.play(FadeOut(rabbits_groups), FadeOut(line), FadeOut(month_marks), FadeOut(bunny_title))
        self.wait(1)

    def climbing_stairs(self):
        # Transition and give viewer a break before new concept
        self.wait(1)
        stairs_title = Text("Climbing Stairs Problem", font_size=36).to_edge(UP)
        intro_stairs_text = (
            "The same logic applies to other scenarios. Consider a staircase problem: "
            "How many ways can you climb an n-step staircase if you take either 1 or 2 steps at a time?"
        )
        self.voiceover_or_play(FadeIn(stairs_title), text=intro_stairs_text)
        self.wait(2)

        stair_count = 5
        stair_width = 0.5
        stair_height = 0.3
        stairs = VGroup()
        for i in range(stair_count):
            rect = Rectangle(width=stair_width, height=stair_height).shift(RIGHT*i*stair_width + UP*i*stair_height)
            stairs.add(rect)
        stairs.move_to(ORIGIN + DOWN*1 + LEFT*1)

        self.voiceover_or_play(Create(stairs), text=(
            "For 1 step, there's only 1 way. For 2 steps, there are 2 ways. "
            "For 3 steps, think: you can come from step 1 or step 2, so that's 3 ways in total."
        ))
        self.wait(2)

        ways = [1,2,3,5,8]
        ways_labels = VGroup()
        for i,w in enumerate(ways):
            label = Tex(str(w)).scale(0.7).next_to(stairs[i], UP)
            ways_labels.add(label)

        # Show ways one by one
        self.play(Write(ways_labels[0]))
        self.wait(1)
        self.play(Write(ways_labels[1]))
        self.wait(1)
        for i in range(2,5):
            self.play(Write(ways_labels[i]))
            self.wait(1)
            # Show arrows for dependencies
            if i >= 2:
                arr1 = Arrow(ways_labels[i-1].get_bottom(), ways_labels[i].get_top(), buff=0.1, color=YELLOW)
                arr2 = Arrow(ways_labels[i-2].get_bottom(), ways_labels[i].get_top(), buff=0.1, color=YELLOW)
                self.play(Create(arr1), Create(arr2))
                self.wait(1)
                self.play(FadeOut(arr1), FadeOut(arr2))
                self.wait(1)

        recap_text = "Again, we get the Fibonacci pattern: each count is the sum of the previous two."
        self.voiceover_or_play(None, text=recap_text)
        self.wait(2)

        # Clear the screen before next topic
        self.play(FadeOut(ways_labels), FadeOut(stairs), FadeOut(stairs_title))
        self.wait(1)

    def recursion_vs_dp(self):
        # Introduce recursion vs DP
        recursion_title = Text("Naive Recursion vs Dynamic Programming", font_size=36).to_edge(UP)
        intro_recursion_text = (
            "Computing large Fibonacci numbers using a naive recursive definition leads to a lot of repeated work. "
            "Let's illustrate this for F_5."
        )
        self.voiceover_or_play(FadeIn(recursion_title), text=intro_recursion_text)
        self.wait(2)

        # Recursion tree
        f5 = MathTex("F_{5}")
        f4 = MathTex("F_{4}").next_to(f5, LEFT+DOWN)
        f3 = MathTex("F_{3}").next_to(f5, RIGHT+DOWN)
        f3_l = MathTex("F_{3}").next_to(f4, LEFT+DOWN)
        f2_l = MathTex("F_{2}").next_to(f4, RIGHT+DOWN)
        f2_ll = MathTex("F_{2}").next_to(f3_l, LEFT+DOWN)
        f1_ll = MathTex("F_{1}").next_to(f3_l, RIGHT+DOWN)
        f1_lr = MathTex("F_{1}").next_to(f2_l, LEFT+DOWN)
        f0_lr = MathTex("F_{0}").next_to(f2_l, RIGHT+DOWN)
        recursion_group = VGroup(f5,f4,f3,f3_l,f2_l,f2_ll,f1_ll,f1_lr,f0_lr).scale(0.7).move_to(LEFT*3+UP*1)

        self.play(FadeIn(f5))
        self.play(FadeIn(f4),FadeIn(f3))
        self.play(FadeIn(f3_l),FadeIn(f2_l))
        self.play(FadeIn(f2_ll),FadeIn(f1_ll),FadeIn(f1_lr),FadeIn(f0_lr))
        self.wait(1)

        arrow_pairs = [(f5,f4),(f5,f3),(f4,f3_l),(f4,f2_l),(f3_l,f2_ll),(f3_l,f1_ll),(f2_l,f1_lr),(f2_l,f0_lr)]
        arrs = VGroup(*[Arrow(p1.get_bottom(), p2.get_top(), buff=0.1, color=BLUE) for p1,p2 in arrow_pairs])
        self.play(*[Create(a) for a in arrs])
        self.wait(2)

        highlight_text = (
            "Notice how some values, like F_2 and F_3, appear multiple times, causing exponential redundancy."
        )
        self.voiceover_or_play(None, text=highlight_text)
        self.wait(2)

        repeat_circle = Circle(color=RED)
        repeat_circle.surround(f2_ll)
        repeat_circle.scale(1.2)
        self.play(Create(repeat_circle))
        self.wait(1)
        self.play(FadeOut(repeat_circle))
        self.wait(1)

        dp_title = Text("Dynamic Programming", font_size=36).to_edge(UP).shift(RIGHT*3)
        dp_intro_text = (
            "With Dynamic Programming, we store previously computed values to avoid repetition, "
            "reducing complexity dramatically."
        )
        self.play(Write(dp_title))
        self.voiceover_or_play(None, text=dp_intro_text)
        self.wait(2)

        dp_values = [1,1,2,3,5]
        dp_boxes = VGroup()
        for i,v in enumerate(dp_values):
            box = Square(side_length=0.5).shift(RIGHT*(i*0.7+3) + DOWN*1)
            val = Tex(str(v)).scale(0.7).move_to(box)
            dp_boxes.add(VGroup(box,val))

        self.voiceover_or_play(None, text="Start with the base cases: F_0 and F_1.")
        self.play(Create(dp_boxes[0][0]), Write(dp_boxes[0][1]))
        self.wait(1)
        self.play(Create(dp_boxes[1][0]), Write(dp_boxes[1][1]))
        self.wait(1)

        for i in range(2,5):
            self.play(Create(dp_boxes[i][0]), Write(dp_boxes[i][1]))
            self.wait(1)
            arr1 = Arrow(dp_boxes[i-1][0].get_top(), dp_boxes[i][0].get_bottom(), buff=0.1, color=YELLOW)
            arr2 = Arrow(dp_boxes[i-2][0].get_top(), dp_boxes[i][0].get_bottom(), buff=0.1, color=YELLOW)
            self.play(Create(arr1), Create(arr2))
            self.wait(1)
            self.play(FadeOut(arr1), FadeOut(arr2))
            self.wait(1)

        self.play(FadeOut(recursion_title), FadeOut(dp_title), FadeOut(recursion_group), FadeOut(arrs), FadeOut(dp_boxes))
        self.wait(2)

    def golden_ratio_section(self):
        gold_title = Text("The Golden Ratio", font_size=36).to_edge(UP)
        intro_gold_text = (
            "As we take the ratio of consecutive Fibonacci numbers, we approach a special number: the golden ratio, approximately 1.618."
        )
        self.voiceover_or_play(FadeIn(gold_title), text=intro_gold_text)
        self.wait(2)

        ratio_calc = MathTex(r"\frac{F_{14}}{F_{13}} = \frac{377}{233} \approx 1.618").move_to(UP*1)
        self.play(Write(ratio_calc))
        self.wait(1)
        self.voiceover_or_play(None, text=(
            "This number appears in art, architecture, and nature. "
            "It’s also close to the factor for converting mph to kph, making a handy mental approximation."
        ))
        self.wait(2)

        note = Text("1 mph ≈ 1.609 kph; Golden Ratio ≈ 1.618", font_size=24)
        note.next_to(ratio_calc, DOWN*2)
        self.play(FadeIn(note))
        self.wait(2)

        golden_rect = Rectangle(width=2, height=2/1.618, color=YELLOW).next_to(ratio_calc, RIGHT, buff=1)
        self.play(Create(golden_rect))
        self.wait(2)
        self.play(FadeOut(gold_title), FadeOut(ratio_calc), FadeOut(note), FadeOut(golden_rect))
        self.wait(1)

    def efficiency_conclusion(self):
        comp_title = Text("Efficiency Comparison", font_size=36).to_edge(UP)
        intro_comp_text = (
            "Naive recursion grows roughly as 2^N, exploding in complexity. "
            "Dynamic programming grows only linearly with N, making it vastly more efficient."
        )
        self.voiceover_or_play(FadeIn(comp_title), text=intro_comp_text)
        self.wait(2)

        exp_text = Text("Naive: ~2^N operations", font_size=24).move_to(LEFT*3)
        lin_text = Text("DP: ~N operations", font_size=24).move_to(RIGHT*3)
        self.play(Write(exp_text), Write(lin_text))
        self.wait(2)
        self.play(FadeOut(exp_text), FadeOut(lin_text), FadeOut(comp_title))
        self.wait(1)

        conclusion = Text("Fibonacci: Patterns, Efficiency, and Beauty", font_size=30)
        concluding_text = (
            "From simple rabbits to advanced computations and the elegant golden ratio, "
            "the Fibonacci sequence teaches us about patterns, efficiency, and hidden connections. "
            "Thanks for watching!"
        )
        self.voiceover_or_play(FadeIn(conclusion), text=concluding_text)
        self.wait(3)
        self.play(FadeOut(conclusion))
        self.wait(2)