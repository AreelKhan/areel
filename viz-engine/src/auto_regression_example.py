from manim import (
    Scene,
    Text,
    Transform,
    Rectangle,
    VGroup,
    config,
    Write,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    FadeOut,
    FadeToColor,
    WHITE,
    BLUE,
)

FONT_SIZE = 25

class AutoRegressionExample(Scene):
    def construct(self):
        
        # define LLM box
        llm_box = Rectangle(width=2.5, height=1.5)
        llm_label = Text("LLM", font_size=35)
        llm = VGroup(llm_box, llm_label)
        llm.to_edge(UP, buff=config.frame_height * 0.2)
        self.add(llm)

        # define text constants
        INITIAL_PROMPT_TEXT = "Question: How does a car work?"
        INITIAL_RESPONSE_TEXT = "Answer: "
        RESPONSE_TEXTS = ["A ", "car ", "works ", "by ", "converting ", "gas ", "into ", "mechanical"]

        # define text objects
        prompt = Text(INITIAL_PROMPT_TEXT, font_size=FONT_SIZE)
        response = Text(INITIAL_RESPONSE_TEXT, font_size=FONT_SIZE)
        response.next_to(prompt, DOWN)
        response.align_to(prompt, LEFT)
        input_text = VGroup(prompt, response)
        input_text.move_to(llm.get_center() + (-4, -3, 0))
        self.play(Write(input_text), run_time=1)
        
        current_response_text = INITIAL_RESPONSE_TEXT
        for token_text in RESPONSE_TEXTS:
            moving_copy = input_text.copy()
            self.add(moving_copy)
            self.play(
                Transform(
                    moving_copy,
                    llm,
                    replace_mobject_with_target_in_scene=False,
                ),
                run_time=0.6,
            )
            # LLM "thinking" pulse
            self.play(FadeToColor(moving_copy, BLUE), run_time=0.4)
            self.play(FadeToColor(moving_copy, WHITE), run_time=0.4)
            self.play(FadeToColor(moving_copy, BLUE), run_time=0.4)
            self.play(FadeToColor(moving_copy, WHITE), run_time=0.4)
            
            token = Text(token_text, font_size=FONT_SIZE, color=BLUE)
            token.move_to(llm.get_center() + (4, -3, 0))
            self.play(
                Transform(
                    moving_copy,
                    token,
                    replace_mobject_with_target_in_scene=False,
                    path_arc=0.5,
                ),
                run_time=0.6,
            )

            token_at_input = Text(token_text, font_size=FONT_SIZE, color=BLUE)
            token_at_input.next_to(response, RIGHT, buff=0.08)
            token_at_input.align_to(response, DOWN)
            self.play(
                Transform(
                    moving_copy,
                    token_at_input,
                    replace_mobject_with_target_in_scene=False,
                    path_arc=-0.6,
                ),
                run_time=0.5,
            )
            
            new_response_text = current_response_text + token_text
            new_response = Text(new_response_text, font_size=FONT_SIZE)
            new_response.next_to(prompt, DOWN)
            new_response.align_to(prompt, LEFT)

            response.become(new_response)
            self.play(FadeOut(moving_copy), run_time=0.25)
            input_text = VGroup(prompt, response)
            current_response_text = new_response_text


        # Fade out all scene elements
        self.play(FadeOut(llm), FadeOut(input_text), run_time=0.6)
        # Centered outro title
        outro = Text("And so on…", font_size=40, color=WHITE)
        self.play(Write(outro), run_time=0.6)
        self.wait(0.8)