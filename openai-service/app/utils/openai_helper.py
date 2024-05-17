from typing import Any, Iterable
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolParam
from app.config.settings import OPEN_AI_KEY

client = OpenAI(api_key=OPEN_AI_KEY)

generate_quiz_messages: list[ChatCompletionMessageParam] = [
    {
        "role": "system",
        "content": "You will generate a mcq with four choices in json format. Each choice will have its own status that will show its true or false answer in boolean."
    },
]

functions: Iterable[ChatCompletionToolParam] = [
    {
        "type": "function",
        "function": {
                "name": "get_user_details",
                "description": "retrieve user details based on a given username, if user name is null then we will find user details from user id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "int",
                        },
                        "user_name": {
                            "type": "string",
                            "description": "The name of the student, e.g. 'Bilal' or 'Baber' etc"
                        }
                    },
                    "required": ["user_id"],
                },

        },
    },
    {
        "type": "function",
        "function": {
                "name": "get_total_points",
                "description": "Retrieve the cumulative points from all topic exams for a specified user. If the function returns -1, it signifies that no user matching the provided username was found.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "int",
                        },
                        "user_name": {
                            "type": "string",
                            "description": "The user name, e.g. 'Bilal' or 'Baber' etc"
                        }
                    },
                    "required": ["user_id"],
                },
        },
    },
    {
        "type": "function",
        "function": {
                "name": "get_specific_category_details",
                "description": "Create a function that retrieves the details of a specific topic exam for a given username. If the function returns -1, it signifies that no user matching the provided username was found.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string"
                        },
                        "user_name": {
                            "type": "string",
                            "description": "The student name, e.g. 'Bilal' or 'Baber' etc"
                        },
                        "category": {
                            "type": "string",
                            "description": "The topic of exam, e.g. 'Python' or 'Typescript' etc"
                        },
                    },
                    "required": ["user_id", "category"],
                },
        },
    },
    {
        "type": "function",
        "function": {
                "name": "get_all_categories_details",
                "description": "Create a function that retrieves the details of all topics exams for a given username. If the function returns -1, it signifies that no user matching the provided username was found.",
                 "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string"
                        },
                        "user_name": {
                            "type": "string",
                            "description": "The student name, e.g. 'Bilal' or 'Baber' etc"
                        }
                    },
                    "required": ["user_id"],
                },
        },
    }
]
