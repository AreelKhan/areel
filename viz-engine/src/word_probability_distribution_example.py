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
LLM_THINKING_TIME = 0.25
INPUT_TRANSFORM_TIME = 0.8
SCENE_UPSHIFT = 0.6
LABEL_BOTTOM_OFFSET = 0.9

INITIAL_PROMPT_TEXT = "Question: How does a car work?"
INITIAL_ANSWER_TEXT = "Answer:"

# Top-1 at each step corresponds to the first entry
TOKEN_DISTRIBUTIONS = [
    [("A", 0.43), ("The", 0.18), ("It", 0.12), ("In", 0.07)],
    [("car", 0.51), ("vehicle", 0.20), ("engine", 0.12), ("automobile", 0.06)],
    [("works", 0.48), ("operates", 0.23), ("runs", 0.18), ("functions", 0.08)],
    [("by", 0.39), ("through", 0.26), ("using", 0.18), ("with", 0.10)],
]


class TokenProbabilityDistributionExample(Scene):
    def construct(self):
        # LLM box
        llm_box = RoundedRectangle(width=2.5, height=1.5, corner_radius=0.2, stroke_width=6)
        llm_label = Text("LLM", font_size=35)
        llm = VGroup(llm_box, llm_label)
        self.add(llm)
        llm.shift(UP * SCENE_UPSHIFT)

        # Input on the left
        prompt = Text(INITIAL_PROMPT_TEXT, font_size=FONT_SIZE)
        answer = Text(INITIAL_ANSWER_TEXT, font_size=FONT_SIZE)
        answer.next_to(prompt, DOWN)
        answer.align_to(prompt, LEFT)
        input_text = VGroup(prompt, answer)
        input_text.move_to(llm.get_center() + (-4.5, 0, 0))
        self.play(Write(input_text), run_time=1)

        current_response_text = INITIAL_ANSWER_TEXT
        for index, distribution in enumerate(TOKEN_DISTRIBUTIONS):
            moving_copy = input_text.copy()
            self.add(moving_copy)

            if index == 0:
                label_input = Text("Your question goes into the LLM", font_size=EXPLANATION_FONT_SIZE)
            else:
                label_input = Text(
                    "Your question + LLM's predictions go back into the LLM",
                    font_size=EXPLANATION_FONT_SIZE - 4,
                )
            label_input.to_edge(DOWN)
            label_input.shift(UP * LABEL_BOTTOM_OFFSET)
            self.play(FadeIn(label_input), run_time=EXPLANATION_FADE_TIME)
            self.play(
                Transform(
                    moving_copy,
                    llm,
                    replace_mobject_with_target_in_scene=False,
                ),
                run_time=INPUT_TRANSFORM_TIME,
            )
            self.play(FadeOut(label_input), run_time=EXPLANATION_FADE_TIME)

            # LLM thinking
            label_thinking = Text("The LLM \"thinks\"", font_size=EXPLANATION_FONT_SIZE)
            label_thinking.to_edge(DOWN)
            label_thinking.shift(UP * LABEL_BOTTOM_OFFSET)
            self.play(FadeIn(label_thinking), run_time=EXPLANATION_FADE_TIME)
            self.play(FadeToColor(moving_copy, BLUE), run_time=LLM_THINKING_TIME)
            self.play(FadeToColor(moving_copy, WHITE), run_time=LLM_THINKING_TIME)
            self.play(FadeToColor(moving_copy, BLUE), run_time=LLM_THINKING_TIME)
            self.play(FadeToColor(moving_copy, WHITE), run_time=LLM_THINKING_TIME)
            self.play(FadeOut(label_thinking), run_time=EXPLANATION_FADE_TIME)

            # Distribution on the left
            label_predict = Text(
                "The LLM returns probabilities for next words",
                font_size=EXPLANATION_FONT_SIZE,
            )
            label_predict.to_edge(DOWN)
            label_predict.shift(UP * LABEL_BOTTOM_OFFSET)

            lines = []
            for rank, (word, prob) in enumerate(distribution, start=1):
                line_text = f"{rank}. {word}  ({prob*100:.1f}%)"
                color = BLUE if rank == 1 else WHITE
                line = Text(line_text, font_size=FONT_SIZE, color=color)
                lines.append(line)
            distribution_group = VGroup(*lines)
            for i in range(1, len(lines)):
                lines[i].next_to(lines[i - 1], DOWN, aligned_edge=LEFT)

            distribution_group.move_to(llm.get_center() + (4.8, 0, 0))
            ellipsis = Text("⋮", font_size=int(FONT_SIZE * 1.8), color=WHITE, weight="BOLD")
            ellipsis.set_opacity(0.95)
            ellipsis.next_to(distribution_group, DOWN)
            full_distribution = VGroup(distribution_group, ellipsis)

            self.play(FadeIn(label_predict), run_time=EXPLANATION_FADE_TIME)
            self.play(
                Transform(
                    moving_copy,
                    full_distribution,
                    replace_mobject_with_target_in_scene=False,
                    path_arc=0.5,
                ),
                run_time=TRANSFORM_TIME,
            )
            self.play(FadeOut(label_predict), run_time=EXPLANATION_FADE_TIME)

            # Pick top-1 and fade out lower rankings
            top_word, _ = distribution[0]

            token_at_input = Text(top_word, font_size=FONT_SIZE)
            token_at_input.next_to(answer, RIGHT)
            token_at_input.align_to(answer, DOWN)

            label_pick = Text("Pick the most likely next word", font_size=EXPLANATION_FONT_SIZE)
            label_pick.to_edge(DOWN)
            label_pick.shift(UP * LABEL_BOTTOM_OFFSET)
            self.play(FadeIn(label_pick), run_time=EXPLANATION_FADE_TIME)

            top_ranking = lines[0].copy()
            self.play(
                Transform(
                    top_ranking,
                    token_at_input,
                    replace_mobject_with_target_in_scene=False,
                    path_arc=-0.6,
                ),
                run_time=TRANSFORM_TIME,
            )
            self.play(FadeOut(full_distribution), run_time=EXPLANATION_FADE_TIME)
            self.play(FadeOut(moving_copy), run_time=EXPLANATION_FADE_TIME)
            self.play(FadeOut(label_pick), run_time=EXPLANATION_FADE_TIME)

            new_response_text = current_response_text + " " + token_at_input.text
            new_response = Text(new_response_text, font_size=FONT_SIZE)
            new_response.next_to(prompt, DOWN)
            new_response.align_to(prompt, LEFT)
            self.remove(top_ranking)
            answer.become(new_response)

            input_text = VGroup(prompt, answer)
            current_response_text = new_response_text

        self.play(FadeOut(llm), FadeOut(input_text), run_time=EXPLANATION_FADE_TIME)
        outro = Text("And so on…", font_size=40, color=WHITE)
        self.play(Write(outro), run_time=EXPLANATION_FADE_TIME)
        self.wait(1)


