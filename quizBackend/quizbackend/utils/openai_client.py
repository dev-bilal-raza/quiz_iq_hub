from openai import OpenAI
from quizbackend.settings import OPEN_AI_KEY

client = OpenAI(api_key=OPEN_AI_KEY)