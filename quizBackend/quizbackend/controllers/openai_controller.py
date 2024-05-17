from quizbackend.utils.openai_client import client
from sqlmodel import select, Session
from quizbackend.models.quiz_model import Category
from quizbackend.utils.apierrors import InvalidInputException


def generate_question(category: int, session: Session):
    db_category = session.exec(select(Category).where(
        Category.category_id == category)).one_or_none()

    if db_category is None:
        raise InvalidInputException("Category")

    openAi_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You will generate a mcq with four choices in json format. Each choice will have its own status that will show its true or false answer in boolean."
            },
            {
                "role": "user",
                "content": f"Generate a MCQ in {db_category.category_name}"
            }
        ]
    )
    print(openAi_response)
    return openAi_response.choices[0].message.content
