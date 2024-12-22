from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
from manim_voiceover.services.azure import AzureService
from manim_voiceover.services.recorder import RecorderService
import numpy as np  # For any mathematical functions if needed

# Flags and configuration
INCLUDE_NARRATION = False
FANCY_NARRATION = True
NARRARATOR_VOICE = "en-US-SteffanNeural"

class CacheIndexingExplanation(VoiceoverScene):
    def construct(self):
        # Set up voiceover service
        if FANCY_NARRATION:
            # Using the RecorderService for now; can switch to AzureService once ready
            service = RecorderService()
            # service = AzureService(voice=NARRARATOR_VOICE)
        else:
            service = GTTSService(lang="en", tld="com")

        if INCLUDE_NARRATION:
            self.set_speech_service(service)

        # Helper method to handle voiceover and animation sync
        def voiceover_or_play(animation, text=""):
            if INCLUDE_NARRATION and text:
                with self.voiceover(text=text) as tracker:
                    if animation is not None:
                        self.play(animation, run_time=tracker.duration)
            elif animation is not None:
                self.play(animation)

        # --- Scene 1 (0:00 - 0:15): Context and Introduction ---
        # Show a large memory line
        memory_line = Line(LEFT*5, RIGHT*5).set_stroke(width=2)
        memory_squares = VGroup(*[Square(side_length=0.2).move_to(
            memory_line.point_from_proportion(i/40)).shift(UP*0.3) 
            for i in range(41)])
        memory_squares.set_color(GRAY)

        voiceover_or_play(Create(memory_line), text="Your computer’s main memory is huge...")
        self.add(memory_squares)
        self.wait(0.5)
        voiceover_or_play(None, text="...and finding data could be slow if we had to fetch directly from it every time.")

        # Show a simplified cache structure off to the side
        cache_box = Rectangle(width=2, height=2).to_corner(UR).set_color(YELLOW)
        voiceover_or_play(Create(cache_box), text="To speed things up, we use a smaller, faster cache.")
        self.wait(0.5)

        # --- Scene 2 (0:15 - 0:30): Accessing a Single Memory Address ---
        # Highlight a single memory cell
        chosen_cell = memory_squares[20].copy().set_color(BLUE)
        voiceover_or_play(Indicate(chosen_cell), text="Suppose we want the data at this specific memory address.")
        self.wait(0.5)

        # Represent the address as a binary string
        address_str = "10110110010111001000110101100010"  # Just an example 32-bit address
        address_text = Text(address_str, font_size=24).next_to(memory_line, DOWN)
        voiceover_or_play(Write(address_text), text="The address is a binary number, something like this...")
        self.wait(0.5)

        # --- Scene 3 (0:30 - 1:00): Decomposing the Address ---
        # Split the address into parts: Tag (e.g., first 20 bits), Index (e.g., next 8 bits), Offset (e.g., last 4 bits)
        # For illustration, let's say:
        # Tag = first 20 bits, Index = next 8 bits, Offset = last 4 bits
        tag_bits = address_str[:20]
        index_bits = address_str[20:28]
        offset_bits = address_str[28:]

        # Color them differently and show brackets
        tag_mob = Text(tag_bits, font_size=24, color=BLUE)
        index_mob = Text(index_bits, font_size=24, color=ORANGE)
        offset_mob = Text(offset_bits, font_size=24, color=GREEN)

        # Arrange them in a line
        address_group = VGroup(tag_mob, index_mob, offset_mob).arrange(RIGHT, buff=0.1).move_to(address_text.get_center())

        voiceover_or_play(Transform(address_text, address_group),
                          text="This binary address is typically divided into parts: a tag, an index, and a block offset.")

        # Label them
        tag_label = Text("Tag", font_size=24, color=BLUE).next_to(tag_mob, UP)
        index_label = Text("Index", font_size=24, color=ORANGE).next_to(index_mob, UP)
        offset_label = Text("Offset", font_size=24, color=GREEN).next_to(offset_mob, UP)
        self.play(FadeIn(tag_label), FadeIn(index_label), FadeIn(offset_label))
        self.wait(0.5)

        voiceover_or_play(None, text="The index bits point us to which 'set' in the cache to look into...")

        # --- Scene 4 (1:00 - 1:30): Introducing the Cache Structure ---
        # Create a small grid representing cache sets.
        # For simplicity, show 8 sets (rows) and 2 ways (columns)
        num_sets = 8
        ways = 2
        cache_sets = VGroup()
        for i in range(num_sets):
            row = VGroup(*[Rectangle(width=0.6, height=0.4).set_stroke(width=1) for _ in range(ways)])
            row.arrange(RIGHT, buff=0.1)
            cache_sets.add(row)
        cache_sets.arrange(DOWN, buff=0.1).next_to(cache_box, DOWN, buff=0.5)

        voiceover_or_play(Create(cache_sets), text="The cache is organized into sets, each able to hold a few memory blocks.")

        # Highlight the chosen set based on index bits (just pick one row)
        chosen_index = int(index_bits, 2) % num_sets  # For demonstration
        chosen_set = cache_sets[chosen_index]
        self.play(Indicate(chosen_set), run_time=2)
        voiceover_or_play(None, text="The index bits act like a small address pointing directly to one set out of many.")

        # --- Scene 5 (1:30 - 2:00): Using the Index Bits Like a 'Bucket Number' ---
        # Conceptualize sets as buckets
        bucket_label = Text("Set = Bucket", font_size=24).next_to(cache_sets, RIGHT, buff=1)
        voiceover_or_play(Write(bucket_label), text="These index bits are like a hash function output, leading us straight to the right 'bucket' without searching everywhere.")

        # --- Scene 6 (2:00 - 2:30): Matching the Tag ---
        # Inside the chosen set, show tag fields
        tag_fields = VGroup(
            Text("Tag?", font_size=20, color=BLUE),
            Text("Tag?", font_size=20, color=BLUE)
        ).arrange(DOWN, buff=0.2).move_to(chosen_set.get_center())
        self.play(FadeIn(tag_fields))

        voiceover_or_play(None, text="Once we find the correct set, we compare the tag stored in each line with the tag in our address...")

        # Simulate a match on the first line
        self.play(tag_fields[0].animate.set_color(GREEN))
        voiceover_or_play(None, text="If one matches, we’ve found the correct block in the cache.")

        # --- Scene 7 (2:30 - 2:45): Connecting to a Hash Map Analogy ---
        # Show a small hash map analogy
        hashmap_box = Rectangle(width=2, height=1).to_corner(DR).set_color(PURPLE)
        hashmap_label = Text("Hash Map Buckets", font_size=20, color=PURPLE).next_to(hashmap_box, UP)
        self.play(Create(hashmap_box), Write(hashmap_label))

        voiceover_or_play(None, text="This is just like how a hash map works: the index bits are the hash, selecting a bucket, and the tag is like the key.")

        # --- Scene 8 (2:45 - 3:00): Wrapping Up ---
        # Pan out to show everything
        self.play(
            FadeOut(hashmap_box),
            FadeOut(hashmap_label),
            run_time=1
        )
        voiceover_or_play(None, text="By quickly narrowing down where to look, your CPU’s cache makes memory access faster. It’s a well-structured, hashmap-like lookup!")

        # Final hold
        self.wait(2)