from sqlmodel import select

from app.models.quiz_model import Category, CategoryQuizDetails
from app.models.user_model import User
from app.config.database import DB_SESSION

def get_user_details(user_id: int, user_name: str | None, session: DB_SESSION):
    if user_name:
        query = select(User).where(User.user_id == user_id).where(
            User.user_name == user_name)
        if query:
            user = session.exec(query).one_or_none()
            if user:
                return {
                    "user_name": user.user_name,
                    "user_email":  user.user_email,
                    "total_points": user.total_points
                }
            return "User does not exist"
        return "I can just provide your details"
    else:
        query = select(User).where(User.user_id == user_id)
        if query:
            user = session.exec(query).one_or_none()
            if user:
                return {
                    "user_name": user.user_name,
                    "user_email":  user.user_email,
                    "total_points": user.total_points
                }
            return "User does not exist"
        return "User does not exist"


def get_total_points(user_id: int, user_name: str | None, session: DB_SESSION):
    user_details = get_user_details(user_id, user_name, session)
    if type(user_details) is dict:
        user_details.pop("user_email")
        return user_details
    return user_details


def get_specific_category_details(user_id, user_name: str | None, category_name: str, session: DB_SESSION):
    user_details = get_user_details(user_id, user_name, session)
    if type(user_details) is dict:
        category = session.exec(select(Category).where(
            Category.category_name == category_name)).one_or_none()
        if category:
            query = select(CategoryQuizDetails).join(Category).where(CategoryQuizDetails.user_id == user_id).where(
                CategoryQuizDetails.category_id == category.category_id)
            category_details = session.exec(query).one_or_none()
            if category_details:
                return {
                    "user_name": user_name,
                    "category_name": category_name,
                    "obtaining_marks": category_details.obtaining_marks,
                    "total_marks": category_details.percentage,
                    "rank": category_details.rank,
                    "is_finished": category_details.is_finished,
                    "remaining_questions": category_details.remaining_questions
                }
            return f"You haven't taken the {category_name.title()} exam yet."
        return f"We haven't provided you with the {category_name.title()} exam yet"
    return user_details


def get_all_categories_details(user_id: int, user_name: str | None, session: DB_SESSION):
    user_details = get_user_details(user_id, user_name, session)
    if type(user_details) is dict:
        all_categories_details = session.exec(select(CategoryQuizDetails).where(
            CategoryQuizDetails.user_id == user_id)).all()
        if all_categories_details:
            return all_categories_details
        return f"You haven't taken the any type of exam yet."
    return user_details
