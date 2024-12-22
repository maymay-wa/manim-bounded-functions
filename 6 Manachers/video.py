from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
from manim_voiceover.services.azure import AzureService
from manim_voiceover.services.recorder import RecorderService

# For mathematical operations if you need them (e.g., random, etc.)
import numpy as np

# -------- Configuration Flags -------- #
INCLUDE_NARRATION = False      # Toggle to True/False for including voiceover
FANCY_NARRATION = False        # If True, use AzureService or RecorderService
NARRATOR_VOICE = "en-US-SteffanNeural"


# ----------------------------------------- #
# Helper to create a "scrabble tile" style
# ----------------------------------------- #
def create_tile(
    letter, 
    tile_color="#F9EAC2", 
    text_color=BLACK, 
    tile_width=1.0, 
    tile_height=1.0
):
    """
    Creates a single "Scrabble-style" tile with:
      - A warm background color
      - Rounded corners
      - A soft drop shadow
      - A bold letter in the center
    """
    # Slightly offset shadow for a simple drop-shadow effect
    shadow = RoundedRectangle(
        width=tile_width,
        height=tile_height,
        corner_radius=0.2,
        fill_color=BLACK,
        fill_opacity=0.2,
        stroke_width=0
    )
    shadow.shift(DOWN*0.06 + RIGHT*0.06)

    # Main tile with a darker stroke for a friendly outline
    tile_base = RoundedRectangle(
        width=tile_width,
        height=tile_height,
        corner_radius=0.2,
        fill_color=tile_color,
        fill_opacity=1,
        stroke_width=2,
        stroke_color=BLACK
    )

    # Letter text (bold & slightly bigger for a Scrabble look)
    txt = Text(letter, font_size=40, color=text_color, weight=BOLD)
    txt.move_to(tile_base.get_center())

    group = VGroup(shadow, tile_base, txt)
    return group

# def create_tile(letter, tile_color="#DAD2C1", text_color=BLACK, tile_width=0.8, tile_height=0.9):
#     """
#     Creates a single "tile" shaped like a scrabble piece or alphabet block.
#     - letter: the character to display
#     - tile_color: background color
#     - text_color: color of the letter
#     - tile_width/tile_height: dimensions of the tile
#     Returns a VGroup with the tile and the centered letter.
#     """
#     tile = RoundedRectangle(
#         width=tile_width, 
#         height=tile_height, 
#         corner_radius=0.15, 
#         fill_color=tile_color, 
#         fill_opacity=1
#     )
#     txt = Text(letter, font_size=30, color=text_color)
#     group = VGroup(tile, txt)
#     txt.move_to(tile.get_center())
#     return group

# ---------------------------------- #
#  Helper: voiceover_or_play function
# ---------------------------------- #
def voiceover_or_play(scene, animation_or_animations, text="", run_time=None):
    """
    Helper to handle voiceover + animation sync. 
    - 'scene' is the current VoiceoverScene instance
    - 'animation_or_animations' can be a single Animation or list of them
    - 'text' is the narration text (optional)
    - 'run_time' if you want to override the default run time
    """
    if animation_or_animations is None:
        animations_list = []
    elif isinstance(animation_or_animations, list):
        animations_list = animation_or_animations
    else:
        animations_list = [animation_or_animations]

    if INCLUDE_NARRATION and text:
        with scene.voiceover(text=text) as tracker:
            # If run_time not specified, we match the voiceover duration
            if run_time is None:
                scene.play(*animations_list, run_time=tracker.duration)
            else:
                scene.play(*animations_list, run_time=run_time)
    else:
        # No narration, just play the animations
        if animations_list:
            if run_time:
                scene.play(*animations_list, run_time=run_time)
            else:
                scene.play(*animations_list)


# ---------------------------------- #
#   PART 1: Problem Explanation
# ---------------------------------- #
class LPSPart1ProblemExplanation(VoiceoverScene):
    def construct(self):
        """
        This scene:
          1) Shows a 5-part roadmap,
          2) Defines palindromic substring,
          3) Demonstrates a 9-letter example with multiple palindromes using scrabble-style tiles,
          4) Illustrates the ends-inward vs. center-outward checking method,
          5) Compares O(n^3), O(n^2), O(n) with n=50,
          6) Wraps up with a personal note on the problem’s childlike simplicity vs. advanced solutions.
        """

        # 1) Set up voiceover service
        if FANCY_NARRATION:
            # RecorderService for custom voice track, or switch to AzureService for TTS
            service = RecorderService()
            # service = AzureService(voice=NARRATOR_VOICE)
        else:
            service = GTTSService(lang="en", tld="com")

        if INCLUDE_NARRATION:
            self.set_speech_service(service)

        #
        # (A) FIVE-PART ROADMAP
        #
        roadmap_title = Text("Longest Palindromic Substring", font_size=40).to_edge(UP)
        part_labels = VGroup(
            Text("Part 1: Problem Explanation", font_size=28),
            Text("Part 2: n^3 and n^2 Solutions", font_size=28),
            Text("Part 3: Manacher’s Key Insight", font_size=28),
            Text("Part 4: Python Implementation", font_size=28),
            Text("Part 5: Performance Demo", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT).move_to(ORIGIN)

        # Highlight Part 1
        part_labels[0].set_color(YELLOW)

        voiceover_or_play(
            self,
            [Write(roadmap_title), FadeIn(part_labels)],
            text=(
                "Welcome to our five-part series on the Longest Palindromic Substring problem. "
                "Here's our roadmap for the upcoming videos."
            )
        )
        self.wait(3)

        # Keep Part 1 on screen, fade out others
        voiceover_or_play(
            self,
            [FadeOut(roadmap_title)] + [FadeOut(lbl) for lbl in part_labels[1:]],
            text=(
                "In this first video, we’ll explore the problem itself and see some examples."
                "This is a popular question for interviews from companies like Google and Microsoft"
            )

        )
        self.play(part_labels[0].animate.to_edge(UP))
        self.wait(1)

        #
        # (B) TITLE & DEFINITION
        #
        title_text = Text(
            "Longest Palindromic Substring – Introduction", 
            font_size=36
        ).next_to(part_labels[0], DOWN, buff=0.5)
        voiceover_or_play(
            self,
            Write(title_text),
            text="Let’s dive right in!"
        )
        self.wait(1)

        definition_lines = VGroup(
            Text("A Palindromic Substring is a substring", font_size=30),
            Text("that reads the same forwards and backwards.", font_size=30)
        ).arrange(DOWN, center=True).move_to(DOWN)
        voiceover_or_play(
            self,
            FadeIn(definition_lines),
            text=(
                "First, let's clarify what we mean by a palindromic substring: "
                "It reads the same forwards and backwards."
            )
        )
        self.wait(2)
        # Fade out the definition_lines
        self.play(FadeOut(definition_lines))
        self.wait(1)

        

        # Create scrabble-style tiles for each letter (just bigger/friendlier)
        tiles = VGroup()
        tile_width = 1.0  # Slightly larger than the original 0.8
        example_str = "abcbacabb"
        for i, ch in enumerate(example_str):
            tile_group = create_tile(ch, tile_width=tile_width, tile_height=1.0)
            tile_group.move_to(RIGHT * (i * (tile_width + 0.1)))
            tiles.add(tile_group)

        tiles.move_to(DOWN * 1.5)
        voiceover_or_play(
            self,
            Create(tiles),
            text=(
                  "Now, consider this 9-character string. It actually contains several palindromic substrings "
                 "of various sizes."
                 "We'll lay it out as fun alphabet tiles, one character per piece."
            )
        )
        self.wait(1.5)

        # Show multiple palindromes
        # 1) "abcba" (0..4)
        pal_abcba_rect = SurroundingRectangle(VGroup(*tiles[0:5]), buff=0.1, color=YELLOW)
        pal_abcba_text = Text("abcba", font_size=34, color=YELLOW).next_to(tiles, DOWN*2)
        voiceover_or_play(
            self,
            [Create(pal_abcba_rect), FadeIn(pal_abcba_text)],
            text="One palindrome here is 'abcba'—the same forwards and backwards."
        )
        self.wait(2)
        self.play(FadeOut(pal_abcba_rect), FadeOut(pal_abcba_text))

        # 2) "bcba" (1..4)
        pal_bcba_rect = SurroundingRectangle(VGroup(*tiles[1:5]), buff=0.1, color=GREEN)
        pal_bcba_text = Text("bcba", font_size=34, color=GREEN).next_to(tiles, DOWN*2)
        voiceover_or_play(
            self,
            [Create(pal_bcba_rect), FadeIn(pal_bcba_text)],
            text="Inside it, there's also a shorter one, 'bcba'."
        )
        self.wait(2)
        self.play(FadeOut(pal_bcba_rect), FadeOut(pal_bcba_text))

        # 3) "bacab" (3..7)
        pal_bacab_rect = SurroundingRectangle(VGroup(*tiles[3:8]), buff=0.1, color=ORANGE)
        pal_bacab_text = Text("bacab", font_size=34, color=ORANGE).next_to(tiles, DOWN*2)
        voiceover_or_play(
            self,
            [Create(pal_bacab_rect), FadeIn(pal_bacab_text)],
            text=(
                "We also find 'bacab' in the middle. It overlaps with the previous ones."
            )
        )
        self.wait(2)
        self.play(FadeOut(pal_bacab_rect), FadeOut(pal_bacab_text))

        # 4) "bb" (7..8)
        pal_bb_rect = SurroundingRectangle(VGroup(*tiles[7:9]), buff=0.1, color=RED)
        pal_bb_text = Text("bb", font_size=34, color=RED).next_to(tiles, DOWN*2)
        voiceover_or_play(
            self,
            [Create(pal_bb_rect), FadeIn(pal_bb_text)],
            text="And of course, two identical letters 'bb' form the simplest palindrome."
        )
        self.wait(2)

        self.play(FadeOut(pal_bb_rect), FadeOut(pal_bb_text), FadeOut(tiles))
        self.wait(1)

        #
        # (D) DEMO: Checking from Ends or Center
        #
        checking_title = Text("How do we check for a palindrome?", font_size=32).to_edge(UP, buff=2.5)
        voiceover_or_play(
            self,
            Write(checking_title),
            text=(
                "So how do we actually check if a substring is palindromic? "
                "It’s very much like how you’d do it in your head."
            )
        )
        self.wait(1)

        # We'll use a short example, e.g. "abcba"
        short_str = "abcba"
        short_tiles = VGroup()
        for i, ch in enumerate(short_str):
            tile_group = create_tile(ch, tile_width=1.0, tile_height=1.0)
            tile_group.move_to(RIGHT * (i * 1.1))
            short_tiles.add(tile_group)

        short_tiles.move_to(DOWN*1)

        voiceover_or_play(
            self,
            Create(short_tiles),
            text="Take a smaller substring 'abcba'."
        )
        self.wait(1)

        # (D1) Ends Inward Approach
        arrow_left = Arrow(start=UP*0.5, end=DOWN*0.3, buff=0, color=YELLOW)
        arrow_left.move_to(short_tiles[0].get_center() + UP*1)
        arrow_right = Arrow(start=UP*0.5, end=DOWN*0.3, buff=0, color=YELLOW)
        arrow_right.move_to(short_tiles[4].get_center() + UP*1)

        voiceover_or_play(
            self,
            [GrowArrow(arrow_left), GrowArrow(arrow_right)],
            text="One way: compare the first and last letters. If they match, move inward."
        )
        self.wait(1)

        # Move arrows inward
        voiceover_or_play(
            self,
            [arrow_left.animate.move_to(short_tiles[1].get_center() + UP*1),
             arrow_right.animate.move_to(short_tiles[3].get_center() + UP*1)],
            text="Then compare the next pair inside..."
        )
        self.wait(1)

        # Move arrows inward again
        voiceover_or_play(
            self,
            [arrow_right.animate.move_to(short_tiles[2].get_center() + UP*1),
             arrow_left.animate.move_to(short_tiles[2].get_center() + UP*1),
            ],
            text="...until you reach the center, confirming they're all matches."
        )
        self.wait(1)

        # (D2) Center Outward Approach
        self.play(FadeOut(arrow_left), FadeOut(arrow_right))
        center_arrow_left = Arrow(start=DOWN*0.5, end=UP*0.3, buff=0, color=GREEN)
        center_arrow_right = Arrow(start=DOWN*0.5, end=UP*0.3, buff=0, color=GREEN)
        center_arrow_left.move_to(short_tiles[2].get_center() + DOWN*1)
        center_arrow_right.move_to(short_tiles[2].get_center() + DOWN*1)
        voiceover_or_play(
            self,
            [
            GrowArrow(center_arrow_left),
            GrowArrow(center_arrow_right)
            ],
            text="Alternatively, start in the middle and compare letters expanding outward step by step."
        )
        self.wait(2)

        # Move arrows outward
        voiceover_or_play(
            self,
            [center_arrow_left.animate.move_to(short_tiles[1].get_center() + DOWN*1),
             center_arrow_right.animate.move_to(short_tiles[3].get_center() + DOWN*1)],
            text="Then compare the next pair inside..."
        )
        self.wait(1)

        # Move arrows outward
        voiceover_or_play(
            self,
            [center_arrow_left.animate.move_to(short_tiles[0].get_center() + DOWN*1),
             center_arrow_right.animate.move_to(short_tiles[4].get_center() + DOWN*1)],
            text="Then compare the next pair inside..."
        )
        self.wait(1)

        self.play(FadeOut(center_arrow_right), FadeOut(center_arrow_left), FadeOut(short_tiles), FadeOut(checking_title))
        self.wait(1)

        
        self.play(FadeOut(title_text), FadeOut(part_labels[0]))
        self.wait(1)

        #
        # (E) COMPLEXITY WRAP-UP
        #
        voiceover_or_play(
            self,
            None,
            text=(
                "Finally, let's talk about performance. Some methods are slower, some faster. "
                "It matters for bigger strings."
            )
        )
        self.wait(1)

        # Add a heading for the section
        complexity_heading = Text("Time Complexity Comparison for a 50 letter word", font_size=32, color=BLUE).to_edge(UP)

        # Define the bullet points with improved formatting
        bullet_points = VGroup(
            Text("1. Naive: O(n^3) → that’s ~125,000 expansions", font_size=26, color=RED).scale(0.9),
            Text("2. Center Expand: O(n^2) ~2,500 expansions", font_size=26, color=ORANGE).scale(0.9),
            Text("3. Manacher’s: O(n) → ~50 expansions", font_size=26, color=GREEN).scale(0.9)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(complexity_heading, DOWN, buff=1)

        # Fade in the heading first
        voiceover_or_play(
            self,
            FadeIn(complexity_heading),
            text="Let’s compare the time complexity of three approaches to finding the longest palindromic substring."
        )
        self.wait(2)

        # Fade in bullet points one by one
        bullet_texts = [
            "A naive O(n^3) solution might do around 125,000 checks for a 50-character string.",
            "An O(n^2) approach reduces the work significantly to about 2,500 checks.",
            "A linear-time solution, like Manacher’s Algorithm, does only around 50 expansions."
        ]

        for bullet, text in zip(bullet_points, bullet_texts):
            voiceover_or_play(
                self,
                FadeIn(bullet),
                text=text
            )
            self.wait(2)

        # Wait after the last bullet point
        self.wait(2)

        #
        # (F) PERSONAL NOTE WRAP-UP
        #
        personal_note = VGroup(
            Text("It's a puzzle so simple a child could solve it,", font_size=24),
            Text("yet so ingenious we only cracked the best solution in 1975", font_size=24)
        ).arrange(DOWN, center=True).to_edge(DOWN, buff=1.5)

        voiceover_or_play(
            self,
            Write(personal_note),
            text=(
                "What drew me to this problem is its childlike simplicity—anyone can check a palindrome "
                "by looking from the ends inward. Yet, there's a brilliant method discovered by Manacher—"
                "so clever that we name the algorithm after him. "
                "It's a wonderful example of how a seemingly simple puzzle can inspire deep and elegant solutions."
            )
        )
        self.wait(5)

        final_text = Text(
            "Next time: n^3 and n^2 solutions, then Manacher’s O(n) approach!",
            font_size=26, color=YELLOW
        ).to_edge(UP)
        voiceover_or_play(
            self,
            FadeIn(final_text),
            text=(
                "Thank you for watching! In the next video, we'll look at the naive and expand-around-center methods "
                "and see why they're slower, before we unlock Manacher’s Algorithm."
            )
        )
        self.wait(4)

        # Fade out everything
        self.play(
            FadeOut(final_text),
            FadeOut(personal_note),
            FadeOut(bullet_points),
            FadeOut(definition_lines),
            FadeOut(title_text),
            FadeOut(part_labels[0])
        )
        self.wait(1)



# ---------------------------------- #
#   PART 2: n^3 and n^2 Solutions
# ---------------------------------- #
class LPSPart2NaiveExpandSolutions(VoiceoverScene):
    def construct(self):
        """
        A refined Part 2 scene:
          1) Quick 5-part roadmap review, focusing on Part 2.
          2) Demonstration of naive O(n^3) method with a simple example,
             showing substring generation and palindrome checks step by step.
          3) Demonstration of expand-around-center O(n^2) approach more clearly,
             with fewer shapes and an emphasis on 'stopping early' to save time.
          4) Wrap-up that teases Manacher’s O(n) in Part 3.
          5) Less visual clutter, more engaging, friendlier tone.
        """
        # 1) Set up voiceover service
        if FANCY_NARRATION:
            service = RecorderService()
            # or switch to AzureService(voice=NARRATOR_VOICE)
        else:
            service = GTTSService(lang="en", tld="com")

        if INCLUDE_NARRATION:
            self.set_speech_service(service)

        #
        # (A) ROADMAP REVIEW
        #
        roadmap_title = Text("Longest Palindromic Substring – Roadmap", font_size=36).to_edge(UP)
        part_labels = VGroup(
            Text("Part 1: Problem Explanation", font_size=24),
            Text("Part 2: O(n^3) & O(n^2) Solutions", font_size=24),
            Text("Part 3: Manacher’s Key Insight (O(n))", font_size=24),
            Text("Part 4: Python Implementation", font_size=24),
            Text("Part 5: Performance Demo", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT).move_to(ORIGIN)

        # Highlight Part 2
        part_labels[1].set_color(YELLOW)

        voiceover_or_play(
            self,
            [Write(roadmap_title), FadeIn(part_labels)],
            text=(
                "Welcome back! Here’s our five-part roadmap again. We've already covered Part 1. "
                "Now, let's head into Part 2: the naive O of n cubed solution, and the O of n squared approach."
            )
        )
        self.wait(3)

        # Zoom in or fade out others
        keep_part2 = part_labels[1]
        others = [part_labels[i] for i in [0,2,3,4]]
        voiceover_or_play(
            self,
            [FadeOut(roadmap_title)] + [FadeOut(lbl) for lbl in others],
            text="So let's focus on that second approach right now!"
        )
        self.play(keep_part2.animate.to_edge(UP))
        self.wait(1)

        #
        # (B) TITLE
        #
        main_title = Text("Naive O(n^3) & Expand Around Center O(n^2)", font_size=30).next_to(keep_part2, DOWN)
        voiceover_or_play(
            self,
            Write(main_title),
            text=(
                "In this video, we'll compare two methods. "
                "First, the naive method—nice and simple, but oh so slow. "
                "Then, we'll see a smarter approach that cuts down the runtime."
            )
        )
        self.wait(2)

        #
        # (C) NAIVE O(n^3) – EXPLANATION
        #
        naive_label = Text("Naive O(n^3) Approach", font_size=28, color=RED).to_corner(UL)
        self.play(FadeIn(naive_label))

        bullet_points_naive = VGroup(
            Text("1. Generate all substrings → O(n^2)", font_size=24),
            Text("2. Check each substring → O(n)", font_size=24),
            Text("Overall → O(n^3)", font_size=24, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(naive_label, DOWN, buff=0.5)

        voiceover_or_play(
            self,
            FadeIn(bullet_points_naive),
            text=(
                "First up, the naive approach. We create all possible substrings—about n squared many—"
                "then for each one, we do a palindrome check in O(n). Multiply them together, and we get n cubed."
            )
        )
        self.wait(3)

        #
        # (D) NAIVE DEMO
        #
        sample_str = "babad"
        example_text = Text(f"Example: '{sample_str}'", font_size=28, color=YELLOW).to_edge(LEFT)
        voiceover_or_play(
            self,
            FadeIn(example_text),
            text="Let’s see it in action with the string 'babad'."
        )
        self.wait(1)

        # Show scrabble tiles for "babad"
        tiles_babad = VGroup()
        for i, ch in enumerate(sample_str):
            tile = create_tile(ch, tile_width=0.9)
            tile.move_to(RIGHT * i)
            tiles_babad.add(tile)

        tiles_babad.shift(DOWN*1.5 + LEFT*(len(sample_str)-1)*0.5)

        voiceover_or_play(
            self,
            Create(tiles_babad),
            text="We'll lay out the letters horizontally."
        )
        self.wait(2)

        # Substring generation highlight
        highlight_sub = SurroundingRectangle(VGroup(tiles_babad[0], tiles_babad[1]), buff=0.1, color=BLUE)
        voiceover_or_play(
            self,
            Create(highlight_sub),
            text="First, we pick a start and end index—like indices 0 to 1—for substring 'ba'."
        )
        self.wait(1)

        highlight_sub_2 = SurroundingRectangle(VGroup(tiles_babad[0], tiles_babad[1], tiles_babad[2]), buff=0.1, color=GREEN)
        self.play(ReplacementTransform(highlight_sub, highlight_sub_2))
        voiceover_or_play(
            self,
            None,
            text="Then 0..2 for 'bab'. We keep doing this for all possible pairs of start and end indices."
        )
        self.wait(2)

        self.play(FadeOut(highlight_sub_2))

        # Checking a substring for palindrome
        check_label = Text("Check Substring in O(n)", font_size=24, color=RED).to_edge(UP, buff=1)
        self.play(FadeIn(check_label))

        highlight_bab = SurroundingRectangle(VGroup(tiles_babad[0], tiles_babad[1], tiles_babad[2]), buff=0.1, color=GREEN)
        arrow_left = Arrow(UP*0.3, DOWN*0.3, buff=0, color=YELLOW).move_to(tiles_babad[0].get_center() + UP*0.6)
        arrow_right = Arrow(UP*0.3, DOWN*0.3, buff=0, color=YELLOW).move_to(tiles_babad[2].get_center() + UP*0.6)

        voiceover_or_play(
            self,
            [Create(highlight_bab), GrowArrow(arrow_left), GrowArrow(arrow_right)],
            text="Take substring 'bab'. We check from the ends inward. If mismatch, it's not a palindrome. If all match, we succeed."
        )
        self.wait(2)

        self.play(FadeOut(arrow_left), FadeOut(arrow_right), FadeOut(highlight_bab))

        voiceover_or_play(
            self,
            None,
            text="Do that for every substring. It’s straightforward but definitely O(n^3)."
        )
        self.wait(2)

        self.play(FadeOut(check_label))

        #
        # (E) EXPAND AROUND CENTER (O(n^2))
        #
        expand_label = Text("Expand Around Center (O(n^2))", font_size=28, color=GREEN).to_corner(UL)
        self.play(ReplacementTransform(naive_label, expand_label))
        bullet_points_expand = VGroup(
            Text("1. For each index (and gap) as 'center'", font_size=24),
            Text("2. Expand outward while letters match", font_size=24),
            Text("Stop on mismatch → saves time", font_size=24, color=BLUE),
            Text("Overall → O(n^2)", font_size=24, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(expand_label, DOWN, buff=0.5)

        voiceover_or_play(
            self,
            FadeIn(bullet_points_expand),
            text=(
                "Now a more efficient approach: Expand Around Center. "
                "We treat each character—and each gap between characters—as a possible center, "
                "then expand outward while letters match. "
                "If we see a mismatch, we stop immediately."
            )
        )
        self.wait(3)

        # Reuse "babad"
        expand_title_demo = Text("Again, 'babad'", font_size=24, color=YELLOW).to_edge(LEFT)
        self.play(FadeIn(expand_title_demo))

        # We'll re-highlight the same row
        # (We'll just use the same tiles_babad; if it's not on screen, re-create it.)
        if tiles_babad not in self.mobjects:
            # If it was removed, re-create
            tiles_babad = VGroup()
            for i, ch in enumerate(sample_str):
                tile = create_tile(ch, tile_width=0.9)
                tile.move_to(RIGHT * i)
                tiles_babad.add(tile)
            tiles_babad.shift(DOWN*1.5 + LEFT*(len(sample_str)-1)*0.5)
            self.play(Create(tiles_babad))

        # Example: center at index 2
        center_rect = SurroundingRectangle(tiles_babad[2], buff=0.1, color=GREEN)
        arrow_left_c = Arrow(UP*0.3, DOWN*0.3, buff=0, color=YELLOW).move_to(tiles_babad[1].get_center() + UP*0.6)
        arrow_right_c = Arrow(UP*0.3, DOWN*0.3, buff=0, color=YELLOW).move_to(tiles_babad[3].get_center() + UP*0.6)

        voiceover_or_play(
            self,
            [Create(center_rect), GrowArrow(arrow_left_c), GrowArrow(arrow_right_c)],
            text=(
                "Pick index 2 (the middle 'b'). Check one step left and one step right. "
                "If they match, expand further; if they don’t, you stop."
            )
        )
        self.wait(3)

        self.play(FadeOut(arrow_left_c), FadeOut(arrow_right_c), FadeOut(center_rect))

        voiceover_or_play(
            self,
            None,
            text=(
                "By halting expansions the moment we see a mismatch, "
                "we avoid re-checking all those inner letters, dropping complexity to O(n^2)."
            )
        )
        self.wait(3)

        self.play(FadeOut(tiles_babad), FadeOut(expand_title_demo), FadeOut(bullet_points_expand))
        self.wait(1)

        #
        # (F) WRAP-UP
        #
        wrapup_text = Text(
            "Naive: O(n^3) vs. Expand Around Center: O(n^2). Next: an O(n) approach!",
            font_size=24,
            color=YELLOW
        ).to_edge(DOWN)

        voiceover_or_play(
            self,
            Write(wrapup_text),
            text=(
                "So there you have it: the naive method is easy but slow at O(n^3), "
                "while expanding around the center is more clever, at O(n^2). "
                "Next time, we'll see if we can do even better with an O(n) algorithm—Manacher’s!"
            )
        )
        self.wait(3)

        # Cleanup
        self.play(FadeOut(wrapup_text), FadeOut(main_title), FadeOut(keep_part2), FadeOut(example_text))
        self.wait(1)


# ---------------------------------- #
#   PART 3: Manacher’s Key Insight
# ---------------------------------- #
class LPSPart3ManacherMirror(VoiceoverScene):
    def construct(self):
        """
        In this longer, step-by-step Part 3 animation:
          1) Transform a small string "aba" → "*a*b*a*"
          2) Show p array below each tile
          3) Illustrate expansions at each index i
          4) Demonstrate skipping expansions using mirror = 2*C - i
          5) Emphasize how the algorithm remains O(n) overall
        """

        # 1) Voiceover configuration
        if FANCY_NARRATION:
            service = RecorderService()
            # or: service = AzureService(voice=NARRATOR_VOICE)
        else:
            service = GTTSService(lang="en", tld="com")

        if INCLUDE_NARRATION:
            self.set_speech_service(service)

        #
        # (A) PART 3 TITLE
        #
        title = Text("Part 3: Manacher’s Key Insight", font_size=36).to_edge(UP)
        voiceover_or_play(
            self,
            Write(title),
            text=(
                "Welcome to Part 3 of our Longest Palindromic Substring series. "
                "Here, we'll delve into Manacher’s Algorithm step by step, "
                "revealing how we achieve linear time with mirror indices."
            )
        )
        self.wait(3)

        #
        # (B) TRANSFORM THE STRING
        #
        transform_label = Text("Transforming 'aba' → '*a*b*a*'", font_size=28, color=BLUE).to_edge(LEFT)
        voiceover_or_play(
            self,
            FadeIn(transform_label),
            text=(
                "First, we insert '*' between every character (and at the ends) to unify odd and even palindromes. "
                "So 'aba' becomes '*a*b*a*'."
            )
        )
        self.wait(3)

        # Original vs transformed text
        original_str = "aba"
        transformed_str = "*a*b*a*"
        ex_original = Text(f"Original: {original_str}", font_size=24).move_to(UP*0.5 + LEFT*3)
        ex_trans = Text(f"Transformed: {transformed_str}", font_size=24, color=YELLOW).next_to(ex_original, DOWN, buff=0.3)

        voiceover_or_play(
            self,
            [FadeIn(ex_original), FadeIn(ex_trans)],
            text="Let’s lay it out visually as scrabble tiles."
        )
        self.wait(2)

        # Scrabble tiles
        tile_row = VGroup()
        for i, ch in enumerate(transformed_str):
            tile = create_tile(ch)
            tile.move_to(RIGHT * i * 1.1)
            tile_row.add(tile)
        tile_row.shift(DOWN*1.5 + LEFT*(len(transformed_str)-1)*0.55)

        voiceover_or_play(
            self,
            Create(tile_row),
            text="Each character in the transformed string, including '*', has its own tile."
        )
        self.wait(3)

        #
        # (C) DEFINING p[i], CENTER, RIGHT
        #
        define_label = Text("Define p[i], center (C), right (R)", font_size=28, color=BLUE).to_edge(LEFT)
        voiceover_or_play(
            self,
            FadeIn(define_label),
            text=(
                "We'll maintain an array p[i], storing the palindrome radius at each index i. "
                "C and R track the rightmost palindrome we’ve found so far: "
                "C is its center, and R is the boundary index."
            )
        )
        self.wait(3)

        # p bars
        p_bars = VGroup()
        for i in range(len(transformed_str)):
            bar = Rectangle(
                width=0.3, 
                height=0.01, 
                fill_color=GREEN, 
                fill_opacity=1, 
                stroke_width=1
            )
            bar.move_to(tile_row[i].get_center() + DOWN*1.5)
            p_bars.add(bar)

        voiceover_or_play(
            self,
            Create(p_bars),
            text="Below each tile, these green bars represent p[i]. We'll adjust their height as expansions happen."
        )
        self.wait(3)

        #
        # (D) INDEX i=0
        #
        i0_marker = Arrow(UP, DOWN, color=YELLOW).move_to(tile_row[0].get_center() + UP*0.6)
        voiceover_or_play(
            self,
            GrowArrow(i0_marker),
            text=(
                "At i=0 (the first '*'), there's nothing to expand around. p[0] remains 0. "
                "Center C=0, Right R=0 for now."
            )
        )
        self.wait(2)
        self.play(FadeOut(i0_marker))

        #
        # (E) INDEX i=1 => 'a'
        #
        i1_marker = Arrow(UP, DOWN, color=YELLOW).move_to(tile_row[1].get_center() + UP*0.6)
        voiceover_or_play(
            self,
            GrowArrow(i1_marker),
            text=(
                "Now at i=1 (the 'a'), we try to expand outwards. "
                "Check T[0] = '*', T[2] = '*', they match!"
            )
        )
        self.wait(2)

        self.play(p_bars[1].animate.stretch_to_fit_height(0.6, about_edge=DOWN))  # p[1]=1
        voiceover_or_play(
            self,
            None,
            text="So p[1]=1. Next expansion step would check T[-1], T[3], out of range on left. We stop."
        )
        self.wait(2)

        # Update C,R since i+p[i]=1+1=2 > R=0
        c_marker = Arrow(DOWN, UP, color=RED).move_to(tile_row[1].get_center() + DOWN*1.0)
        r_marker = Arrow(DOWN, UP, color=GREEN).move_to(tile_row[2].get_center() + DOWN*1.0)
        voiceover_or_play(
            self,
            [GrowArrow(c_marker), GrowArrow(r_marker)],
            text="We set center = 1, right = 2 now."
        )
        self.wait(2)
        self.play(FadeOut(i1_marker))

        #
        # (F) INDEX i=2 => '*'
        #
        i2_marker = Arrow(UP, DOWN, color=YELLOW).move_to(tile_row[2].get_center() + UP*0.6)
        voiceover_or_play(
            self,
            GrowArrow(i2_marker),
            text=(
                "At i=2 ('*'), i < R? (2<2?) It's equal, so no mirror logic. "
                "Try expanding T[1] vs T[3] => 'a' vs 'b' mismatch => p[2]=0."
            )
        )
        self.wait(2)
        self.play(FadeOut(i2_marker))

        #
        # (G) INDEX i=3 => 'b'
        #
        i3_marker = Arrow(UP, DOWN, color=YELLOW).move_to(tile_row[3].get_center() + UP*0.6)
        voiceover_or_play(
            self,
            GrowArrow(i3_marker),
            text=(
                "At i=3 ('b'), i=3 > R=2 => no mirror logic. "
                "We expand: T[2]='*', T[4]='a', mismatch => p[3]=0. No update to C,R."
            )
        )
        self.wait(2)
        self.play(FadeOut(i3_marker), FadeOut(c_marker), FadeOut(r_marker))

        #
        # (H) Suppose we find a bigger palindrome at i=4 => '*'
        #
        i4_marker = Arrow(UP, DOWN, color=YELLOW).move_to(tile_row[4].get_center() + UP*0.6)
        voiceover_or_play(
            self,
            GrowArrow(i4_marker),
            text=(
                "At i=4 ('*'), let's see if expansions succeed: T[3]='b', T[5]='b', match => p[4]=1. "
                "Then T[2]='*', T[6]='*', match => p[4]=2. Then T[1]='a', T[7]? Out of range or mismatch, stop."
            )
        )
        self.wait(2)
        self.play(p_bars[4].animate.stretch_to_fit_height(1.2, about_edge=DOWN))  # p[4]=2
        voiceover_or_play(
            self,
            None,
            text="So p[4]=2. i+p[i] = 4+2=6, bigger than old R=2 => update C=4, R=6."
        )
        self.wait(2)

        c_marker_2 = Arrow(DOWN, UP, color=RED).move_to(tile_row[4].get_center() + DOWN*1.0)
        r_marker_2 = Arrow(DOWN, UP, color=GREEN).move_to(tile_row[6].get_center() + DOWN*1.0)
        voiceover_or_play(
            self,
            [GrowArrow(c_marker_2), GrowArrow(r_marker_2)],
            text="Center is 4, Right is 6."
        )
        self.wait(2)
        self.play(FadeOut(i4_marker))

        #
        # (I) Mirror usage at i=5
        #
        i5_marker = Arrow(UP, DOWN, color=YELLOW).move_to(tile_row[5].get_center() + UP*0.6)
        voiceover_or_play(
            self,
            GrowArrow(i5_marker),
            text=(
                "Now at i=5. Since i=5 < R=6, we find mirror = 2*C - i = 2*4 - 5=3. "
                "We start p[5] = min( p[mirror], R - i )."
            )
        )
        self.wait(2)

        mirror_arrow = Arrow(UP, DOWN, color=BLUE).move_to(tile_row[3].get_center() + UP*1.2)
        voiceover_or_play(
            self,
            GrowArrow(mirror_arrow),
            text="The mirror is index 3. p[3]=0. R-i=6-5=1 => p[5] starts at min(0,1)=0."
        )
        self.wait(2)

        # Attempt expansions
        voiceover_or_play(
            self,
            None,
            text="But we can still expand if T[4]= '*' and T[6]= '*' match => p[5]=1."
        )
        self.play(p_bars[5].animate.stretch_to_fit_height(0.6, about_edge=DOWN))
        self.wait(2)

        self.play(FadeOut(i5_marker), FadeOut(mirror_arrow))

        #
        # (J) Final Summation
        #
        summary_text = Text("We skip expansions using p[mirror]. That’s Manacher’s O(n) trick!", font_size=28, color=YELLOW).to_edge(UP)
        voiceover_or_play(
            self,
            Write(summary_text),
            text=(
                "By leveraging p[mirror], we avoid re-checking inner characters over and over. "
                "This single pass across the transformed string is O(n) in total."
            )
        )
        self.wait(3)

        # Final text
        end_note = Text("Next: Coding Manacher’s in Part 4. Thanks for watching!", font_size=26, color=GREEN).to_edge(DOWN)
        voiceover_or_play(
            self,
            FadeIn(end_note),
            text=(
                "In the next video, we’ll write the actual Python code for Manacher’s. See you there!"
            )
        )
        self.wait(3)

        # Fade everything out
        self.play(
            FadeOut(summary_text),
            FadeOut(end_note),
            FadeOut(tile_row),
            FadeOut(p_bars),
            FadeOut(transform_label),
            FadeOut(define_label),
            FadeOut(c_marker_2),
            FadeOut(r_marker_2),
            FadeOut(ex_original),
            FadeOut(ex_trans),
            FadeOut(title)
        )
        self.wait(1)


# ---------------------------------- #
#   PART 4: Writing the Python Code
# ---------------------------------- #
class LPSPart4PythonCode(VoiceoverScene):
    def construct(self):
        # 1) Voiceover service
        if FANCY_NARRATION:
            service = RecorderService()
            # service = AzureService(voice=NARRATOR_VOICE)
        else:
            service = GTTSService(lang="en", tld="com")

        if INCLUDE_NARRATION:
            self.set_speech_service(service)

        # Title
        title_text = Text("Manacher’s Algorithm – Python Implementation", font_size=32).to_edge(UP)
        voiceover_or_play(self, Write(title_text),
                          text="Now let’s see how to code Manacher’s in Python step by step.")

        self.wait(1)

        # Present the code in chunks
        code_lines = [
            "def longestPalindrome(s: str) -> str:",
            "    # 1. Transform the string with delimiters",
            "    T = '|' + '|'.join(s) + '|'",
            "    n = len(T)",
            "    p = [0]*n  # p[i] = radius of palindrome around center i in T",
            "    center = 0",
            "    right = 0",
            "",
            "    # 2. Main loop",
            "    for i in range(n):",
            "        mirror = 2*center - i",
            "        if i < right:",
            "            p[i] = min(right - i, p[mirror])",
            "",
            "        # Expand around i",
            "        while (i - p[i] - 1 >= 0 and i + p[i] + 1 < n",
            "               and T[i - p[i] - 1] == T[i + p[i] + 1]):",
            "            p[i] += 1",
            "",
            "        # Update center and right if expanded past right",
            "        if i + p[i] > right:",
            "            center = i",
            "            right = i + p[i]",
            "",
            "    # 3. Find max palindrome",
            "    max_len = max(p)",
            "    max_center = p.index(max_len)",
            "",
            "    # 4. Convert back to original indices",
            "    start = (max_center - max_len)//2",
            "    return s[start : start + max_len]"
        ]

        # We'll display them line by line as we narrate
        code_text_group = VGroup(*[CodeLine(line, font_size=20) for line in code_lines]).arrange(DOWN, aligned_edge=LEFT)
        code_box = Rectangle(width=10, height=8, color=WHITE).move_to(ORIGIN)
        code_box.set_opacity(0.1).scale(1.1)

        self.add(code_box)
        self.add(code_text_group)
        code_text_group.shift(UP*0.5)

        voiceover_or_play(self, None,
                          text="Let’s look at the essential steps inside this function.")

        self.wait(1)

        # Animate highlighting different regions
        highlight_rect = Rectangle(width=9, height=0.6, color=YELLOW).set_opacity(0.3)

        # Transform steps
        step_descriptions = [
            "Step 1: We transform the string with '|'.",
            "Step 2: We maintain p[i], center, and right, and iterate through the transformed string.",
            "We compute a mirror index, and initialize p[i] based on p[mirror].",
            "Then we try to expand further if characters on both sides match.",
            "Finally, we update center and right if our new palindrome extends beyond the old boundary.",
            "After finishing, we find the maximum palindrome length in p, convert back to the original string, and return it."
        ]
        highlight_indices = [0, 7, 11, 14, 18, 24]

        for i, desc in enumerate(step_descriptions):
            # Move highlight rect to the line region
            highlight_rect.move_to(code_text_group[highlight_indices[i]].get_center())
            voiceover_or_play(self, Create(highlight_rect), text=desc)
            self.wait(2)

        # Wrap up
        voiceover_or_play(self, None,
                          text="That’s the full Python code for Manacher’s Algorithm. It runs in O(n) time, a remarkable improvement over the simpler methods.")
        self.wait(2)


# ---------------------------------- #
#   PART 5: Performance Demonstration
# ---------------------------------- #
class LPSPart5PerformanceTest(VoiceoverScene):
    def construct(self):
        # 1) Voiceover service
        if FANCY_NARRATION:
            service = RecorderService()
            # service = AzureService(voice=NARRATOR_VOICE)
        else:
            service = GTTSService(lang="en", tld="com")

        if INCLUDE_NARRATION:
            self.set_speech_service(service)

        # Title
        title_text = Text("Performance Demo on Worst-Case String", font_size=32).to_edge(UP)
        voiceover_or_play(self, Write(title_text),
                          text="Finally, let's demonstrate Manacher’s speed on a worst-case input: a string of all identical characters.")

        self.wait(1)

        # Example string
        worstcase_str = "a" * 15  # shorter for illustration
        example_text = Text(f"Example: 15 'a' characters: {worstcase_str}", font_size=28)
        example_text.move_to(UP*1)
        voiceover_or_play(self, FadeIn(example_text),
                          text="For demonstration, here's a 15-character string of all 'a's. In practice, we might do 1 million characters, but let's keep it short here.")

        self.wait(2)

        # Show naive O(n^2) or O(n^3) meltdown
        meltdown_label = Text("Naive solutions can degrade severely here...", font_size=28, color=RED).shift(DOWN*1)
        voiceover_or_play(self, FadeIn(meltdown_label),
                          text="Naive or even O(n^2) solutions can become very slow. A million characters would be nearly impossible to handle quickly.")
        self.wait(2)

        # Show Manacher’s text
        manacher_label = Text("Manacher’s handles it in O(n)", font_size=28, color=GREEN).next_to(meltdown_label, DOWN)
        voiceover_or_play(self, FadeIn(manacher_label),
                          text="But Manacher’s remains linear, completing in a blink, even for millions of characters.")

        self.wait(2)

        # Final summary
        summary_group = VGroup(
            Text("Conclusion", font_size=36, color=YELLOW),
            Text("Manacher’s Algorithm is O(n).", font_size=28),
            Text("Works even on tough cases like 'aaaaaaaaaaa....'", font_size=28),
            Text("Thank you for watching!", font_size=28, color=BLUE)
        ).arrange(DOWN, buff=0.6).move_to(ORIGIN)

        voiceover_or_play(self, FadeIn(summary_group[0]),
                          text="That brings us to the conclusion of our series on the Longest Palindromic Substring.")
        self.wait(1)
        voiceover_or_play(self, FadeIn(summary_group[1]),
                          text="Manacher’s algorithm offers an elegant O(n) solution...")
        self.wait(1)
        voiceover_or_play(self, FadeIn(summary_group[2]),
                          text="...even on strings that cause slower methods to stall.")
        self.wait(1)
        voiceover_or_play(self, FadeIn(summary_group[3]),
                          text="Thank you for joining us. Happy coding!")
        self.wait(3)


# ------------------------
#   Utility: CodeLine
# ------------------------
# A helper class to display code lines nicely. 
# (This is optional; you can also just use Text.)
class CodeLine(Text):
    CONFIG = {
        "t2c": {
            # You can add syntax highlighting here if you want, e.g.:
            # "def": BLUE,
            # "return": GREEN,
        },
        "font": "Consolas"
    }

    def __init__(self, text, **kwargs):
        Text.__init__(self, text, **kwargs)