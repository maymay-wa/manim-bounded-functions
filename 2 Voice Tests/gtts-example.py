from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class GoogleCloudTTSExample(VoiceoverScene):
    def construct(self):
        # Set up the Google Cloud TTS service with your desired voice
        self.set_speech_service(GTTSService(lang="en", tld="com"))
        
        circle = Circle()
        square = Square().shift(2 * RIGHT)

        # Add voiceover and animations
        with self.voiceover(text="This circle is drawn as I speak.") as tracker:
            self.play(Create(circle), run_time=tracker.duration)

        with self.voiceover(text="Let's shift it to the left 2 units.") as tracker:
            self.play(circle.animate.shift(2 * LEFT), run_time=tracker.duration)

        with self.voiceover(text="Now, let's transform it into a square.") as tracker:
            self.play(Transform(circle, square), run_time=tracker.duration)

        with self.voiceover(text="Thank you for watching."):
            self.play(Uncreate(circle))

        self.wait()