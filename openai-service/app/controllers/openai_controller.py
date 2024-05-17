import json
from typing import Any, Callable
from sqlmodel import select, Session

from app.models.quiz_model import Category
from app.utils.apierrors import InvalidInputException
from app.utils.openai_helper import client, generate_quiz_messages, functions, ChatCompletionMessageParam
from app.controllers import db_controller

def generate_question(category: int, session: Session):
    db_category = session.exec(select(Category).where(
        Category.category_id == category)).one_or_none()

    if db_category is None:
        raise InvalidInputException("Category")
    generate_quiz_messages.append(
        {
            "role": "user",
            "content": f"Generate a MCQ in {db_category.category_name}"
        }
    )
    openAi_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=generate_quiz_messages
    )
    print(openAi_response)
    return openAi_response.choices[0].message.content


def openai_conversation(prompt: str):
    messages: Any = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        tools=functions,
        tool_choice="auto"
    )
    response_message = response.choices[0].message
    print("================ Response from Chat Gpt after calling first function ===================")
    print(response_message)
    tool_calls = response_message.tool_calls
    if tool_calls:
        available_functions: dict[str, Callable] = {
            "get_user_details": db_controller.get_user_details,
            "get_total_points": db_controller.get_total_points,
            "get_specific_category_details": db_controller.get_specific_category_details,
            "get_all_categories_details": db_controller.get_all_categories_details
        } 
        
        for tool_call in tool_calls:
                
            function_name = tool_call.function.name
            function_to_call: Callable = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            messages.append(response_message)
            messages.append(
                {
                    "tool_call_is": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(function_response)
                }
            )
        second_response = client.chat.completions.create(
                model= "gpt-3.5-turbo-0125",
                messages=messages
            )
        return second_response.choices[0].message.content
    else:
        return response_message.content