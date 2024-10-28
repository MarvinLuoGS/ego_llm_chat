from otree.api import *
from openai import OpenAI
import os

doc = """
This app send the input to the GPT or other LLM to get the scores.
"""

def get_scores(client, article):
    # get the scores from the LLM
    stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": f"给下面的这首诗评分，内容在【】中，评分范围1-10分，只报告分数数字：【{article}】"}],
    )
    score = stream.choices[0].message.content
    return score

class C(BaseConstants):
    NAME_IN_URL = 'send_input'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    article = models.LongStringField(label="Article")
    score = models.StringField(label="Score")



# PAGES
class Input_article(Page):
    form_fields = ["article"]
    form_model = "player"

    @staticmethod
    def before_next_page(player, timeout_happened):
        api_key = os.environ.get("OPENAI_API_KEY")
        base_url = os.environ.get("OPENAI_BASE_URL")
        client = OpenAI(api_key=api_key, base_url=base_url)
        player.score = get_scores(client, player.article)

class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Input_article,Results]
