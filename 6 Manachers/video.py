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
    txt = Text(letter, font_size=140, color=text_color, weight=BOLD, font="ScrambleMixed")
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
    Helper for syncing voiceovers with animations. Ensures animations are not empty.
    """
    # Convert single animation to a list
    if animation_or_animations is None:
        animations_list = []  # No animations
    elif isinstance(animation_or_animations, list):
        animations_list = animation_or_animations
    else:
        animations_list = [animation_or_animations]

    if INCLUDE_NARRATION and text:
        with scene.voiceover(text=text) as tracker:
            if animations_list:
                if run_time is None:
                    scene.play(*animations_list, run_time=tracker.duration)
                else:
                    scene.play(*animations_list, run_time=run_time)
    else:
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
            #service = AzureService(voice=NARRATOR_VOICE)
        else:
            service = GTTSService(lang="en", tld="com")

        if INCLUDE_NARRATION:
            self.set_speech_service(service)

        #
        # (A) FIVE-PART ROADMAP
        #
        # Background animation
        grid = NumberPlane().fade(0.8)
        self.play(DrawBorderThenFill(grid), run_time=3)
        self.wait(0.1)
        # Title text
        title = Text("Manimator", font_size=72, gradient=(BLUE, PURPLE))
        title.shift(UP * 0.5)
        # Animations
        self.play(DrawBorderThenFill(title), run_time=2.5)
        self.play(FadeOut(grid), run_time = 1)
        self.wait(0.5)
        # Reverse Animation
        self.play(Uncreate(title), run_time=1)  # Erase outline
        self.wait(0.5)

        roadmap_title = Text("Longest Palindromic Substring", font_size=40).to_edge(UP)
        part_labels = VGroup(
            Text("Part 1: Problem Explanation", font_size=28),
            Text("Part 2: n^3 and n^2 Solutions", font_size=28),
            Text("Part 3: Manacher’s Key Insight", font_size=28),
            Text("Part 4: Python Implementation", font_size=28),
            Text("Part 5: Performance Demo", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT).move_to(ORIGIN)

        # Highlight Part 1
        part_labels[0].set_color(BLUE)

        voiceover_or_play(
            self,
            [Write(roadmap_title), FadeIn(part_labels)],
            text=(
                "Welcome to our five-part series on the findinf the Longest Palindromic Substring. "
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
                "This question is popular for interviews from companies like Google or Microsoft"
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
            Text("A Palindromic Substring is a section of a word", font_size=30),
            Text("that reads the same forwards and backwards.", font_size=30)
        ).arrange(DOWN, center=True).move_to(DOWN)
        voiceover_or_play(
            self,
            FadeIn(definition_lines),
            text=(
                "First, let's clarify what we mean by a palindrome: "
                "Its a word that reads the same forwards and backwards."
                "For example Racecar, Tacocat, Abba"
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
                "Now, consider this 9-character string. It actually contains several palindromic substrings"
                "of various sizes."
            )
        )
        self.wait(1)

        # Show multiple palindromes
        # 1) "abcba" (0..4)
        pal_abcba_rect = SurroundingRectangle(VGroup(*tiles[0:5]), buff=0.02, color=YELLOW)
        pal_abcba_text = Text("abcba", font_size=34, color=YELLOW).next_to(tiles, DOWN*2)
        voiceover_or_play(
            self,
            [Create(pal_abcba_rect), FadeIn(pal_abcba_text)],
            text="One palindrome here is 'abcba'—the same forwards and backwards."
        )
        self.wait(1)
        self.play(FadeOut(pal_abcba_rect), FadeOut(pal_abcba_text))

        # # 2) "bacab" (3..7)
        # highlight_color = LOGO_BLUE  # Define a highlight color for the letters

        # # Create a copy of the tiles for "bacab" with the new color
        # highlighted_tiles = VGroup()
        # for i in range(3, 8):  # indices 3 to 7 (inclusive)
        #     letter = tiles[i][2]  # Access the Text object within each tile
        #     highlighted_letter = Text(letter.text, font_size=140, color=highlight_color, font="ScrambleMixed", weight=BOLD)
        #     highlighted_letter.move_to(letter.get_center())  # Position it exactly where the original letter is
        #     highlighted_tiles.add(highlighted_letter)

        # pal_abcba_text = Text("bacab", font_size=34, color=YELLOW).next_to(tiles, DOWN*2)

        # # Replace the original letters with the highlighted ones
        # voiceover_or_play(
        #     self,
        #     [FadeOut(VGroup(*[tiles[i][2] for i in range(3, 8)])), FadeIn(highlighted_tiles), FadeIn(pal_abcba_text)],
        #     text="We also find 'bacab' in the middle. It overlaps with the previous ones."
        # )
        # self.wait(2)

        # 2) "bacab" (3..7)
        pal_bacab_rect = SurroundingRectangle(VGroup(*tiles[3:8]), buff=0.02, color=ORANGE)
        pal_bacab_text = Text("bacab", font_size=34, color=ORANGE).next_to(tiles, DOWN*2)
        voiceover_or_play(
            self,
            [Create(pal_bacab_rect), FadeIn(pal_bacab_text)],
            text=(
                "We also find 'bacab' in the middle. It overlaps with the previous ones."
            )
        )
        self.wait(1)
        self.play(FadeOut(pal_bacab_rect), FadeOut(pal_bacab_text))

        # # Restore the original letters
        # voiceover_or_play(
        #     self,
        #     [FadeOut(pal_abcba_text), FadeIn(VGroup(*[tiles[i][2] for i in range(3, 8)]))],
        #     text=""
        # )
        self.wait(1)

        # 3) "bb" (7..8)
        pal_bb_rect = SurroundingRectangle(VGroup(*tiles[7:9]), buff=0.02, color=RED)
        pal_bb_text = Text("bb", font_size=34, color=RED).next_to(tiles, DOWN*2)
        voiceover_or_play(
            self,
            [Create(pal_bb_rect), FadeIn(pal_bb_text)],
            text="And of course, two identical letters 'bb' form the simplest palindrome."
        )
        self.wait(1)

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
                "The way a computer does it is really the same as how you’d do it in your head."
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
            text="Take a smaller word 'abcba'. We're going to call the action we take an expansion."
        )
        self.wait(1)

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
            text="We start in the middle and then we will compare letters as we go."
        )
        self.wait(1)

        # Move arrows outward
        voiceover_or_play(
            self,
            [center_arrow_left.animate.move_to(short_tiles[1].get_center() + DOWN*1),
             center_arrow_right.animate.move_to(short_tiles[3].get_center() + DOWN*1)],
            text="Then expand outward..."
        )
        self.wait(1)

        # Move arrows outward
        voiceover_or_play(
            self,
            [center_arrow_left.animate.move_to(short_tiles[0].get_center() + DOWN*1),
             center_arrow_right.animate.move_to(short_tiles[4].get_center() + DOWN*1)],
            text="and continue until the word is over or letters don't match"
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
                "Finally, let's talk about performance. Some methods are slower, and some are faster. "
            )
        )
        self.wait(1)

        # Add a heading for the section
        complexity_heading = Text("Time Complexity Comparison for a 50 letter word", font_size=32, color=BLUE).to_edge(UP)

        # Define the bullet points with improved formatting
        bullet_points = VGroup(
            Text("1. Obvious Solution: ~125,000 expansions", font_size=26, color=RED).scale(0.9),
            Text("2. Expand by letter: ~2,500 expansions", font_size=26, color=ORANGE).scale(0.9),
            Text("3. Manacher’s Algorithm: ~50 expansions", font_size=26, color=GREEN).scale(0.9)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(complexity_heading, DOWN, buff=1)

        # Fade in the heading first
        voiceover_or_play(
            self,
            FadeIn(complexity_heading),
            text="Let’s compare the time complexity of three approaches to finding the longest palindromic substring."
        )
        self.wait(1)

        # Fade in bullet points one by one
        bullet_texts = [
            "A naive O(n^3) solution might do around 125,000 expansions for a 50-character string.",
            "An O(n^2) approach reduces the work significantly to about 2,500 expansions.",
            "And finally Manacher’s Algorithm, which solves the problem with only 50 or so expansions."
        ]

        for bullet, text in zip(bullet_points, bullet_texts):
            voiceover_or_play(
                self,
                FadeIn(bullet),
                text=text
            )
            self.wait(1)

        # Wait after the last bullet point
        self.wait(1)

        #
        # (F) PERSONAL NOTE WRAP-UP
        #
        personal_note = VGroup(
            Text("It's a puzzle so simple a child could solve it,", font_size=24),
            Text("yet so ingenious few would ever think of the optimal solution ", font_size=24)
        ).arrange(DOWN, center=True).to_edge(DOWN, buff=1.5)

        voiceover_or_play(
            self,
            Write(personal_note),
            text=(
                "What drew me to this problem is its childlike simplicity—anyone can check a palindrome "
                "Yet, there's a brilliant method discovered by Manacher in 1975"
                "It's a wonderful example of how a seemingly simple puzzle can inspire deep and elegant solutions."
            )
        )
        self.wait(2)

        voiceover_or_play(
            self,
            None,
            text=(
                "Thank you for watching! In the next video, we'll look at the naive and expand-around-center methods "
                "before we unlock Manacher’s Algorithm."
            )
        )
        self.wait(2)

        # Fade out everything
        self.play(
            FadeOut(personal_note),
            FadeOut(bullet_points)
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
            #service = AzureService(voice=NARRATOR_VOICE)
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
        part_labels[1].set_color(BLUE)

        voiceover_or_play(
            self,
            [Write(roadmap_title), FadeIn(part_labels)],
            text=(
                "Welcome back! Here’s our five-part roadmap again. We've already covered Part 1. "
                "Now, let's head into Part 2: the naive O of n cubed solution, and the O of n squared approach."
            )
        )
        self.wait(1)

        # Zoom in or fade out others
        keep_part2 = part_labels[1]
        others = [part_labels[i] for i in [0,2,3,4]]
        voiceover_or_play(
            self,
            [FadeOut(roadmap_title)] + [FadeOut(lbl) for lbl in others],
            text="So let's focus on those approaches now"
        )
        self.play(keep_part2.animate.to_edge(UP))
        self.wait(1)

        #
        # (B) TITLE
        #
        main_title = Text("The Naive Approach", font_size=30).next_to(keep_part2, DOWN, buff=1)
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

        bullet_points_naive = VGroup(
            Text("1. Generate all substrings → O(n^2)", font_size=24),
            Text("2. Check each one → O(n)", font_size=24),
            Text("Overall → O(n^3)", font_size=24, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(main_title, DOWN, buff=1.5)

        voiceover_or_play(
            self,
            FadeIn(bullet_points_naive),
            text=(
                "First up, the naive approach, where we create all possible substrings"
                "then for each one, we check if its a palindrome"
            )
        )
        self.wait(1)
        self.play(FadeOut(bullet_points_naive))
        self.wait(1)

        #
        # (D) NAIVE DEMO
        #
        sample_str = "babcd"
        # Show scrabble tiles for "babad"
        tiles = VGroup()
        for i, ch in enumerate(sample_str):
            tile = create_tile(ch, tile_width=0.9)
            tile.move_to(RIGHT * i)
            tiles.add(tile)

        tiles.shift(DOWN*0.5 + LEFT*(len(sample_str)-1)*0.5)

        voiceover_or_play(
            self,
            Write(tiles),
            text="Let’s see it in action with the word 'babcd'."
        )
        self.wait(1)

        # Sliding window rectangle
        sliding_window = SurroundingRectangle(tiles[0], buff=0.05, color=YELLOW)
        self.play(Create(sliding_window))

        # Fast motion sliding window logic
        num_tiles = len(tiles)
        for start in range(num_tiles):
            for end in range(start + 1, num_tiles + 1):
                # Update the sliding window position
                window_tiles = VGroup(*tiles[start:end])
                new_window = SurroundingRectangle(window_tiles, buff=0.05, color=YELLOW)
                # Dynamically adjust the height of the sliding window rectangle
                self.play(Transform(sliding_window, new_window), run_time=0.3)

        # Final fade out
        self.play(FadeOut(sliding_window, tiles, main_title))

        # Substrings data in 3 columns
        substrings_columns = [
            ["b", "ba", "bab", "babc", "babcd"],
            ["a", "ab", "abc", "abcd", ''],
            ["b", "bc", "bcd", '', ''],
            ["c", "cd", '', '', ''], 
            ["d", '', '', '', '']
        ]

        # Create the table
        table = Table(
            substrings_columns
        ).move_to(DOWN)

        # Style the table
        table.get_horizontal_lines().set_color(BLUE)
        table.get_vertical_lines().set_color(BLUE)

        # Add the table to the scene
        voiceover_or_play(
            self,
            self.play(Create(table)),
            text="Here is a table showing every word inside of the word babcd, you can tell that there are half of n^2 squared options since they create the area of a triangle"
        )
        self.wait(1)

        # Highlight a cell (row 1, column 1)
        palCells = [table.get_cell((1, 1)), table.get_cell((2, 1)), table.get_cell((4, 1)),
                    table.get_cell((5, 1)), table.get_cell((3, 1)), table.get_cell((1, 3))]
        for cell in palCells:
            cell.set_stroke(width=0)
        # Add the table to the scene
        voiceover_or_play(
            self,
            self.play([cell.animate.set_fill(GREEN, opacity=0.5) for cell in palCells]),
            text="Now we will mark every word that is a palindrome and check for the longest one"
        )

        palCells2 = palCells[:-1]

        voiceover_or_play(
            self,
            self.play([FadeOut(cell) for cell in palCells2]),
            text="Which would clearly be bab in this case"
        )
        
        self.wait(1)

        self.play(FadeOut(palCells[-1]))
        
        palCells = [table.get_cell((2, 3)), table.get_cell((1, 5))]

        voiceover_or_play(
            self,
            self.play([cell.animate.set_fill(YELLOW, opacity=0.5) for cell in palCells]),
            text="Something to notice is that this algorithm does redundant work."
        )
        self.wait(1)

        voiceover_or_play(
            self,
            None,
            text="For instance it would check both abc, and babcd even though we already knew it wasn't a palindrome from abc"
        )
        self.wait(1)

        voiceover_or_play(
            self,
            self.play([FadeOut(cell) for cell in palCells]),
            text="The heart of algorithm development is taking into account redundant steps like this, and our next algorithm will do exactly that"
        )

        self.play(FadeOut(table))

        self.wait(1)

        #
        # (E) EXPAND AROUND CENTER (O(n^2))
        #
        expand_label = Text("Expand Around Center", font_size=28, color=WHITE).next_to(keep_part2, DOWN, buff=1)
        self.play(Write(main_title))
        self.play(ReplacementTransform(main_title, expand_label))
        bullet_points_expand = VGroup(
            Text("1. Only check a letter as a center once", font_size=24, color=BLUE),
            Text("2. Stop on mismatch to save time", font_size=24, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(expand_label, DOWN, buff=1.5)

        voiceover_or_play(
            self,
            FadeIn(bullet_points_expand),
            text=(
                "Now a more efficient approach: Expand Around Center. "
                "We treat each letter as a possible center, "
                "then we expand outward while letters match. "
                "If we see a mismatch, we stop immediately."
            )
        )
        self.wait(3)

        self.play(FadeOut(bullet_points_expand))
        
        # We'll re-highlight the same row
        tiles = VGroup()
        tile_width=0.9
        for i, ch in enumerate(sample_str):
            tile = create_tile(ch, tile_width=0.9)
            tile.move_to(RIGHT * i)
            tiles.add(tile)
        tiles.shift(DOWN*1.5 + LEFT*(len(sample_str)-1)*0.5)
        self.play(Write(tiles))

        # We’ll demonstrate expansions for each letter-center:
        for center_index in range(len(sample_str)):
            # 1) Highlight the center tile
            center_rect = SurroundingRectangle(tiles[center_index], buff=0, color=GREEN)
            self.play(Create(center_rect))
            arrow_left = Arrow(
                    start=tiles[center_index].get_top() + UP,
                    end=tiles[center_index].get_top(),
                    buff=0,
                    color=GREEN
                )
            arrow_right = Arrow(
                    start=tiles[center_index].get_top() + UP,
                    end=tiles[center_index].get_top(),
                    buff=0,
                    color=GREEN
                )
            self.play(GrowArrow(arrow_left), GrowArrow(arrow_right))
            left_idx = center_index
            right_idx = center_index
            while True:
                self.wait(0.1)
                if left_idx >= 0 and right_idx < len(sample_str) and sample_str[left_idx] == sample_str[right_idx]:
                    self.play(
                        arrow_left.animate.shift(LEFT),
                        arrow_right.animate.shift(RIGHT)
                    )
                else:
                    if left_idx < 0 or right_idx == len(sample_str):
                        if left_idx < 0:
                            self.play(arrow_left.animate.set_color(RED))
                        if right_idx == len(sample_str):
                            self.play(arrow_right.animate.set_color(RED))
                    elif sample_str[left_idx] != sample_str[right_idx]:
                        self.play(arrow_left.animate.set_color(RED), arrow_right.animate.set_color(RED))
                    # Fade out these red arrows
                    self.play(FadeOut(arrow_left), FadeOut(arrow_right))
                    break
                # Move one step outward
                left_idx -= 1
                right_idx += 1

            # Cleanup the center rectangle after we finish expanding this center
            self.play(FadeOut(center_rect))


        self.wait(1)
        self.play(FadeOut(tiles))
        self.wait()        

        voiceover_or_play(
            self,
            None,
            text=(
                "By halting expansions the moment we see a mismatch, "
                "we avoid re-checking all those inner letters, dropping complexity to O(n^2)."
            )
        )
        self.wait(1)

        #
        # (F) WRAP-UP
        #
        wrapup_text = Text(
            "Algorithms are all about leveraging information we know, so we don't repeat any work",
            font_size=24,
            color=BLUE
        )

        voiceover_or_play(
            self,
            Write(wrapup_text),
            text=(
                "So there you have it: the naive method is easy but slow at O(n^3), "
                "while expanding around the center is more clever, at O(n^2). "
                "Next time, we'll see how we can do even better with an algorithm that runs in linear time"
                "Manacher’s algorithm!"
            )
        )
        self.wait(1)

        # Cleanup
        self.play(FadeOut(wrapup_text), FadeOut(main_title), FadeOut(keep_part2))
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
        title = Text("Part 3: Manacher’s Genius", font_size=36).to_edge(UP)
        voiceover_or_play(
            self,
            Write(title),
            text=(
                "Welcome to Part 3 of our Longest Palindromic Substring series. "
                "Here, we'll delve into Manacher’s Algorithm step by step, "
                "revealing how we achieve linear time by leveraging informatioin we have already seen."
            )
        )
        self.wait(1)

        sample_str =  'aaaaaaaaaaa'

        # Scrabble tiles
        tiles = VGroup()
        for i, ch in enumerate(sample_str):
            tile = create_tile(ch, tile_width=0.9)
            tile.move_to(RIGHT * i)
            tiles.add(tile)
        tiles.shift(DOWN*0.5 + LEFT*(len(sample_str)-1)*0.5)

        # Create the counter text
        counter = 0  # Initial value
        counter_text = Text(f"Expansion Count: {counter}", font_size=45).next_to(tiles, DOWN * 2.5)
        self.add(counter_text)  # Display the counter initially

        voiceover_or_play(
            self,
            Write(tiles),
            text="Let's start with a tricky string of letters aaaaaaaaaaa."
        )
        self.wait(1)
        
        

        # shortRunTime = 0.15
        # runTime = 0.25
        # longRunTime = 0.65
        # # We’ll demonstrate expansions for each letter-center:
        # for center_index in range(len(sample_str)):
        #     # 1) Highlight the center tile
        #     center_rect = SurroundingRectangle(tiles[center_index], buff=0, color=GREEN)
        #     self.play(Create(center_rect), run_time = shortRunTime)
        #     arrow_left = Arrow(
        #             start=tiles[center_index].get_top() + UP,
        #             end=tiles[center_index].get_top(),
        #             buff=0,
        #             color=GREEN
        #         )
        #     arrow_right = Arrow(
        #             start=tiles[center_index].get_top() + UP,
        #             end=tiles[center_index].get_top(),
        #             buff=0,
        #             color=GREEN
        #         )
        #     self.play(GrowArrow(arrow_left), GrowArrow(arrow_right), run_time = shortRunTime)
        #     left_idx = center_index
        #     right_idx = center_index
        #     notFirstFlag = False
        #     while True:
        #         if notFirstFlag:
        #             counter += 1
        #         notFirstFlag = True
        #         new_counter_text = Text(f"Expansion Count: {counter}", font_size=45).next_to(tiles, DOWN * 2.5)
        #         self.play(counter_text.animate.become(new_counter_text), run_time=shortRunTime)
        #         if left_idx >= 0 and right_idx < len(sample_str) and sample_str[left_idx] == sample_str[right_idx]:
        #             self.play(
        #                 arrow_left.animate.shift(LEFT),
        #                 arrow_right.animate.shift(RIGHT),
        #                 run_time = runTime
        #             )
        #         else:
        #             if left_idx < 0 or right_idx == len(sample_str):
        #                 if left_idx < 0:
        #                     self.play(arrow_left.animate.set_color(RED), run_time = runTime)
        #                 if right_idx == len(sample_str):
        #                     self.play(arrow_right.animate.set_color(RED), run_time = runTime)
        #             elif sample_str[left_idx] != sample_str[right_idx]:
        #                 self.play(arrow_left.animate.set_color(RED), arrow_right.animate.set_color(RED), duration = longRunTime)
        #             # Fade out these red arrows
        #             self.play(FadeOut(arrow_left), FadeOut(arrow_right), run_time = longRunTime)
        #             break
        #         # Move one step outward
        #         left_idx -= 1
        #         right_idx += 1

        #     # Cleanup the center rectangle after we finish expanding this center
        #     self.play(FadeOut(center_rect), run_time = shortRunTime)

        self.play(FadeOut(counter_text))

        # 2) Define "fourth letter" (1-based) → index 3 in 0-based
        center_index = 3   # 'b' at index 3 in "abcbac" (which is the 4th letter)

        # 3) "Third expansion" means radius=2
        expansion_radius = 3
        left_start  = center_index - expansion_radius  # 3 - 2 = 1
        right_end   = center_index + expansion_radius  # 3 + 2 = 5

        # Safety check to avoid going out of range
        if left_start < 0 or right_end >= len(sample_str):
            print("String too short for a 3rd expansion at index 3!")
            return

        # 4) Highlight the center tile just for clarity
        center_rect = SurroundingRectangle(tiles[center_index], color=GREEN, buff=0)
        self.play(Create(center_rect))
        self.wait(0.5)
        
        # 5) Create curly braces under the “left half” and “right half” of this expansion
        left_half  = tiles[left_start : center_index]    # indices [1..2]
        right_half = tiles[center_index+1 : right_end+1] # indices [4..5]

        # Create the braces
        brace_left  = Brace(left_half, direction=UP, buff=0.2)
        brace_right = Brace(right_half, direction=UP, buff=0.2)

        # Optionally add labels under each brace
        label_left = brace_left.get_text("Left Half")
        label_right = brace_right.get_text("Right Half")

        # Animate them in sequentially
        self.play(Write(brace_left), run_time=2)
        self.play(FadeIn(label_left), run_time=2)
        self.play(Write(brace_right), run_time=2)
        self.play(FadeIn(label_right), run_time=2)
        self.wait(1)

        



        # shortRunTime = 0.15
        # runTime = 0.25
        # longRunTime = 0.65
        # # Create the counter text
        # counter = 0  # Initial value
        # new_counter_text = Text(f"Expansion Count: {counter}", font_size=45).next_to(tiles, DOWN * 2.5)
        # self.play(counter_text.animate.become(new_counter_text), run_time=shortRunTime)
        # self.add(counter_text)  # Display the counter initially
        # n = len(sample_str)
        # # We'll keep track of the "center" (C) and the "right boundary" (R)
        # C = 0
        # R = 0
        # p = [0]*n
        # # We'll animate expansions for each center i in the transformed string
        # line_height = 1.2  # Slightly larger than tile height
        # right_bound_line = Line(
        #     tiles[0].get_center() + UP*(line_height/2) + LEFT * 0.5,
        #     tiles[0].get_center() + DOWN*(line_height/2) + LEFT * 0.5,
        #     color=RED,
        #     stroke_width=6
        # )
        # self.add(right_bound_line)
        # for i in range(n):
        #     # ------------------------------------------------------------------
        #     # 1) Mirror logic: mirror = 2*C - i
        #     #    If i < R, we know part of palindrome from mirror's expansions
        #     # ------------------------------------------------------------------
        #     mirror = 2*C - i
        #     if i < R:
        #         # We'll "pretend" to skip expansions by setting p[i] = min(...)
        #         # but only do partial expansions if needed.
        #         p[i] = min(R - i, p[mirror])
        #     # ------------------------------------------------------------------
        #     # 2) Actual expansions around i: expand if chars match
        #     # ------------------------------------------------------------------
        #     # We'll show expansions visually using arrows around the "center" tile
        #     center_rect = SurroundingRectangle(tiles[i], buff=0, color=GREEN)
        #     self.play(Create(center_rect), run_time=0.3)
        #     arrow_left = Arrow(
        #             start=tiles[i - p[i]].get_top() + UP,
        #             end=tiles[i - p[i]].get_top(),
        #             buff=0,
        #             color=GREEN
        #         )
        #     arrow_right = Arrow(
        #             start=tiles[i + p[i]].get_top() + UP,
        #             end=tiles[i + p[i]].get_top(),
        #             buff=0,
        #             color=GREEN
        #         )
        #     self.play(GrowArrow(arrow_left), GrowArrow(arrow_right), run_time=0.4)

        #     # Try expanding further
        #     while (i - p[i] - 1 >= 0 and i + p[i] + 1 < n 
        #            and sample_str[i - p[i] - 1] == sample_str[i + p[i] + 1]):
        #         counter += 1
        #         new_counter_text = Text(f"Expansion Count: {counter}", font_size=45).next_to(tiles, DOWN * 2.5)
        #         self.play(counter_text.animate.become(new_counter_text), run_time=shortRunTime)
        #         p[i] += 1
        #         # Animate arrows moving left/right
        #         self.play(
        #             arrow_left.animate.shift(LEFT),
        #             arrow_right.animate.shift(RIGHT),
        #             run_time=0.3
        #         )

        #     # ------------------------------------------------------------------
        #     # 3) Update center (C) and right boundary (R) if we expanded beyond R
        #     # ------------------------------------------------------------------
        #     if i + p[i] > R:
        #         C = i
        #         R = i + p[i]
        #         new_pos = tiles[R].get_center() + RIGHT * 0.5 if R < n else tiles[n-1].get_center() + RIGHT * 0.5
        #         self.play(
        #             right_bound_line.animate.move_to(
        #                 [new_pos[0], right_bound_line.get_center()[1], 0]
        #             ),
        #             run_time=0.4
        #         )

        #     # Fade out the center rect and arrows
        #     self.play(
        #         FadeOut(center_rect),
        #         FadeOut(arrow_left),
        #         FadeOut(arrow_right),
        #         run_time=runTime
        #     )

        # # Finally, we highlight the maximum palindrome found
        # # (In a real Manacher’s, we use max in p[] to find it. Here, we show just a message.)
        # max_len = max(p)  # the radius in the transformed string
        # max_center = p.index(max_len)

        # # Convert center, radius → original indices if you want
        # # (Skipping the full math for brevity: it’s basically (center - radius)//2 in the raw string.)
        # highlight_start = max_center - max_len
        # highlight_end = max_center + max_len
        # # We'll highlight those tiles
        # highlight_rect = SurroundingRectangle(
        #     VGroup(*tiles[highlight_start:highlight_end+1]),
        #     buff=0.1,
        #     color=GREEN
        # )
        # highlight_label = Text("Longest Palindrome Found", font_size=24, color=GREEN)
        # highlight_label.next_to(highlight_rect, DOWN)

        # self.play(Create(highlight_rect), FadeIn(highlight_label), run_time=longRunTime)
        # self.wait(2)

        # self.play(FadeOut(tiles), FadeOut(title), run_time = runT)
        # self.wait()


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