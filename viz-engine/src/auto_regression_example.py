from manim import (
    Scene,
    Text,
    Transform,
    RoundedRectangle,
    VGroup,
    config,
    Write,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    FadeIn,
    FadeOut,
    FadeToColor,
    WHITE,
    BLUE,
)

FONT_SIZE = 25
EXPLANATION_FONT_SIZE = 26

TRANSFORM_TIME = 1.6
EXPLANATION_FADE_TIME = 0.35
LLM_THINKING_TIME = 0.5
SCENE_UPSHIFT = 0.6
LABEL_BOTTOM_OFFSET = 0.9

INITIAL_PROMPT_TEXT = "Question: How does a car work?"
INITIAL_RESPONSE_TEXT = "Answer: "
RESPONSE_TEXTS = ["A ", "car ", "works ", "by ", "using ", "an ", "engine "]


class AutoRegressionExample(Scene):
    def construct(self):
        
        # define LLM box
        llm_box = RoundedRectangle(width=2.5, height=1.5, corner_radius=0.2, stroke_width=6)
        llm_label = Text("LLM", font_size=35)
        llm = VGroup(llm_box, llm_label)
        llm.to_edge(UP, buff=config.frame_height * 0.2)
        self.add(llm)
        llm.shift(UP * SCENE_UPSHIFT)

        # define text objects
        prompt = Text(INITIAL_PROMPT_TEXT, font_size=FONT_SIZE)
        response = Text(INITIAL_RESPONSE_TEXT, font_size=FONT_SIZE)
        response.next_to(prompt, DOWN)
        response.align_to(prompt, LEFT)
        input_text = VGroup(prompt, response)
        input_text.move_to(llm.get_center() + (-4, -3, 0))
        self.play(Write(input_text), run_time=0.5)
        
        current_response_text = INITIAL_RESPONSE_TEXT
        for index, token_text in enumerate(RESPONSE_TEXTS):
            moving_copy = input_text.copy()
            self.add(moving_copy)
            if index == 0:
                label_input = Text("Your question goes into the LLM", font_size=EXPLANATION_FONT_SIZE)
            else:
                label_input = Text("Your question + LLM's predictions go back into the LLM", font_size=EXPLANATION_FONT_SIZE - 4)
            label_input.to_edge(DOWN)
            label_input.shift(UP * LABEL_BOTTOM_OFFSET)
            self.play(FadeIn(label_input), run_time=EXPLANATION_FADE_TIME)
            self.play(
                Transform(
                    moving_copy,
                    llm,
                    replace_mobject_with_target_in_scene=False,
                ),
                run_time=TRANSFORM_TIME+0.3,
            )
            self.play(FadeOut(label_input), run_time=EXPLANATION_FADE_TIME)
            # LLM "thinking" pulse
            label_thinking = Text("The LLM \"thinks\"", font_size=EXPLANATION_FONT_SIZE)
            label_thinking.to_edge(DOWN)
            label_thinking.shift(UP * LABEL_BOTTOM_OFFSET)
            self.play(FadeIn(label_thinking), run_time=EXPLANATION_FADE_TIME)
            self.play(FadeToColor(moving_copy, BLUE), run_time=LLM_THINKING_TIME)
            self.play(FadeToColor(moving_copy, WHITE), run_time=LLM_THINKING_TIME)
            self.play(FadeToColor(moving_copy, BLUE), run_time=LLM_THINKING_TIME)
            self.play(FadeToColor(moving_copy, WHITE), run_time=LLM_THINKING_TIME)
            self.play(FadeOut(label_thinking), run_time=EXPLANATION_FADE_TIME)
            
            token = Text(token_text, font_size=FONT_SIZE, color=BLUE)
            token.move_to(llm.get_center() + (4, -3, 0))
            label_predict = Text("The LLM predicts the next word", font_size=EXPLANATION_FONT_SIZE)
            label_predict.to_edge(DOWN)
            label_predict.shift(UP * LABEL_BOTTOM_OFFSET)
            self.play(FadeIn(label_predict), run_time=EXPLANATION_FADE_TIME)
            self.play(
                Transform(
                    moving_copy,
                    token,
                    replace_mobject_with_target_in_scene=False,
                    path_arc=0.5,
                ),
                run_time=TRANSFORM_TIME,
            )
            self.play(FadeOut(label_predict), run_time=EXPLANATION_FADE_TIME)

            token_at_input = Text(token_text, font_size=FONT_SIZE, color=BLUE)
            token_at_input.next_to(response, RIGHT, buff=0.08)
            token_at_input.align_to(response, DOWN)
            label_append = Text("The predicted word gets added to the sentence", font_size=EXPLANATION_FONT_SIZE)
            label_append.to_edge(DOWN)
            label_append.shift(UP * LABEL_BOTTOM_OFFSET)
            self.play(FadeIn(label_append), run_time=EXPLANATION_FADE_TIME)
            self.play(
                Transform(
                    moving_copy,
                    token_at_input,
                    replace_mobject_with_target_in_scene=False,
                    path_arc=-0.6,
                ),
                run_time=TRANSFORM_TIME,
            )
            self.play(FadeOut(label_append), run_time=EXPLANATION_FADE_TIME)
            
            new_response_text = current_response_text + token_text
            new_response = Text(new_response_text, font_size=FONT_SIZE)
            new_response.next_to(prompt, DOWN)
            new_response.align_to(prompt, LEFT)

            response.become(new_response)
            self.play(FadeOut(moving_copy), run_time=EXPLANATION_FADE_TIME)
            input_text = VGroup(prompt, response)
            current_response_text = new_response_text


        # Fade out all scene elements
        self.play(FadeOut(llm), FadeOut(input_text), run_time=EXPLANATION_FADE_TIME)
        # Centered outro title
        outro = Text("And so on…", font_size=40, color=WHITE)
        self.play(Write(outro), run_time=EXPLANATION_FADE_TIME)
        self.wait(1)
