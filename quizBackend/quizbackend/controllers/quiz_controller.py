from sqlmodel import Session, select, func

from quizbackend.models.user_model import User
from quizbackend.models.quiz_model import CategoryMarks, CategoryQuizDetails, Question, Category
from quizbackend.utils.apierrors import NotFoundException


# ================================================================================================================================
def get_categories(session: Session):
    """
    Retrieve all categories from the database.

    Args:
        session (Session): Database session.

    Returns:
        List[Category]: List of all categories.
    """
    # Execute a query to fetch all quiz categories
    all_categories = session.exec(select(Category)).all()
    return all_categories


# ================================================================================================================================
def get_quiz(user_id: int, category_name: str, session: Session):
    """
    Retrieve a quiz for a specific user and category from the database.

    Args:
        user_id (int): The ID of the user for whom the quiz is being retrieved.
        category_name (str): The name of the category for the quiz.
        session (Session): Database session.

    Returns:
        dict: A dictionary containing details of the quiz, including remaining questions, questions, and choices.
    Raises:
        NotFoundException: If the category or quiz details are not found in the database.
    """
    # Retrieve category details
    categoryDetails = session.exec((select(CategoryQuizDetails).join(Category)
                                    .where(Category.category_name == category_name)
                                    .where(CategoryQuizDetails.user_id == user_id))).one()
    print(categoryDetails)
    # Raise NotFoundException if category details are not found
    if not categoryDetails:
        raise NotFoundException("Category")
    # Select random questions from the category
    random_selecting_lang = select(Question).where(Question.category_id ==
                                                   categoryDetails.category_id).order_by(func.random()).limit(categoryDetails.remaining_questions)
    questions = session.exec(random_selecting_lang).all()
    choices = []
    # Retrieve choices for each question
    for question in questions:
        choice = question.choices
        choices.append(choice)

    return {
        "remaining_questions": categoryDetails.remaining_questions,
        "questions": questions,
        "choices": choices
    }



# ================================================================================================================================
def isAvailableQuiz(category_name: str, session: Session):
    """
    Check if a quiz is available for a specific category.

    Args:
        category_name (str): The name of the category for which quiz availability is checked.
        session (Session): Database session.

    Returns:
        bool: True if a quiz is available, False otherwise.
    Raises:
        NotFoundException: If the quiz is not found for the given category.
    """
    # Retrieve quiz for the category
    quiz = session.exec(select(Question).join(Category).where(
        Category.category_name == category_name)).all()
    # Raise NotFoundException if quiz is not found
    if quiz is None:
        raise NotFoundException("Quiz")
    # Check if number of questions is greater than 9
    if len(quiz) > 9:
        return True
    return False


# ================================================================================================================================
def getQuizDetails(user_id: int, category_name: str, session: Session):
    """
    Get quiz details for a user and a specific category.

    Args:
        user_id (int): The ID of the user.
        category_name (str): The name of the category.
        session (Session): Database session.

    Returns:
        Union[str, dict]: Quiz details if available, otherwise a message indicating quiz unavailability.
    Raises:
        NotFoundException: If the category is not found.
    """
    # Check if quiz is available for the category
    is_available = isAvailableQuiz(category_name, session)
    if not is_available:
        return f"Quiz is not available for {category_name}"

    # Retrieve category details
    category = session.exec(select(Category).where(
        Category.category_name == category_name)).one()
    if not category:
        raise NotFoundException("Category")

    # Retrieve category quiz details for the user
    category_details = session.exec((select(CategoryQuizDetails, CategoryMarks)
                                     .where(CategoryMarks.category_id == category.category_id)
                                     .where(CategoryQuizDetails.category_id == category.category_id)
                                     .where(CategoryQuizDetails.user_id == user_id)))

    # Process category details
    for categoryDetails, categoryMarks in category_details:
        if categoryDetails:
            details = categoryDetails.model_dump()
            # Check if user has attempted the quiz
            if categoryDetails.remaining_questions < 10:
                details.update({
                    "category_marks": categoryMarks.marks
                })
                return {
                    "isAttempt": True,
                    "quizDetails": details
                }
            return {
                "isAttempt": False,
                "quizDetails": f"You have never attempted {category.category_name} questions"
            }

    # Add category details for the user if not present
    category_details_table = CategoryQuizDetails(
        user_id=user_id, category_id=category.category_id, obtaining_marks=0)
    session.add(category_details_table)
    session.commit()
    return {
        "isAttempt": False,
        "quizDetails": f"You have never attempted {category.category_name} questions"
    }



# ================================================================================================================================
def attempt_quiz(session: Session, user_id: int, category_id: int, quiz_numbers: int, isFinished: bool):
    """
    Attempt a quiz for a specific user and category.

    Args:
        session (Session): Database session.
        user_id (int): The ID of the user.
        category_id (int): The ID of the category.
        quiz_numbers (int): Number of quiz questions attempted.
        isFinished (bool): Indicates if the quiz is finished.

    Returns:
        str: A message indicating the result of the quiz attempt.
    """
    # Select category details for the user
    select_category = (select(CategoryQuizDetails, CategoryMarks)
                       .where(CategoryMarks.category_id == category_id)
                       .where(CategoryQuizDetails.category_id == category_id)
                       .where(CategoryQuizDetails.user_id == user_id))
    category_details = session.exec(select_category)

    # Process category details
    for categoryDetails, categoryMarks in category_details:
        if categoryDetails:
            if not categoryDetails.is_finished:
                # Update quiz details for the user
                categoryDetails.obtaining_marks += quiz_numbers
                categoryDetails.remaining_questions -= 1
                categoryDetails.percentage = int(
                    (categoryDetails.obtaining_marks/categoryMarks.marks) * 100)
                # Check if the quiz is finished
                if isFinished:
                    categoryDetails.is_finished = True
                    # Determine user's rank based on obtained marks
                    if categoryDetails.obtaining_marks < 20:
                        categoryDetails.rank = "Poor"
                    elif categoryDetails.obtaining_marks < 30:
                        categoryDetails.rank = "Better"
                    elif categoryDetails.obtaining_marks < 40:
                        categoryDetails.rank = "Good"
                    else:
                        categoryDetails.rank = "Excellent"
                    session.commit()
                    session.refresh(categoryDetails)
                    # Update user's total points
                    user = session.exec(select(User).where(
                        User.user_id == user_id)).one()
                    user.total_points += categoryDetails.obtaining_marks
                    session.commit()
                    return f"You have attempted {category_id} category quiz"
                session.commit()
                return f"Your Quiz details for {category_id} category has been updated successfully"
            return f"You can't attempt {category_id} category quiz, because you have already attempted"
    else:
        # Add quiz details for the user if not present
        quiz_details_table = CategoryQuizDetails(category_id=category_id,
                                                 user_id=user_id, total_numbers=quiz_numbers)
        session.add(quiz_details_table)
        session.commit()
    return f"Your Quiz details for {category_id} category has been added to the database"


# ================================================================================================================================
def delete_quiz(user_id: int, category_id: int, session: Session):
    """
    Delete a quiz for a specific user and category.

    Args:
        user_id (int): The ID of the user.
        category_id (int): The ID of the category.
        session (Session): Database session.

    Returns:
        str: A message indicating the result of the quiz deletion.
    """
    # Fetch quiz details for the user and category
    quiz_details = session.exec(select(User, CategoryQuizDetails)
                                .where(User.user_id == user_id)
                                .where(CategoryQuizDetails.category_id == category_id)
                                .where(CategoryQuizDetails.user_id == user_id))
    # Process quiz details
    for user, category in quiz_details:
        if user and category:
            # Update user's total points and delete quiz details
            user.total_points -= category.obtaining_marks
            session.delete(category)
            session.commit()
            return f"Quiz has been deleted."
        else:
            raise NotFoundException("User and Category")


# ================================================================================================================================
def get_categories_details(user_id: int, session: Session):
    """
    Get details of categories attempted by a user.

    Args:
        user_id (int): The ID of the user.
        session (Session): Database session.

    Returns:
        dict: Details of categories attempted by the user and total marks across all categories.
    """
    details = []
    all_category_marks = 0
    categories = session.exec(select(Category))
    for category in categories:
        # Query database to check if user attempted the category
        category_details = session.exec(select(CategoryQuizDetails)
                                        .where(CategoryQuizDetails.user_id == user_id)
                                        .where(CategoryQuizDetails.category_id == category.category_id)).first()

        if category_details:
            if category_details.is_finished:
                # If the category is attempted and finished, retrieve its marks
                category_marks = session.exec(select(CategoryMarks).where(
                    CategoryMarks.category_id == category.category_id)).one()
                details.append({
                    "category_name": category.category_name,
                    "isAttempt": True})
                all_category_marks += category_marks.marks
            else:
                # If attempted but not finished
                details.append({
                    "category_name": category.category_name,
                    "isAttempt": False})
        else:
            # If category not attempted
            details.append({
                "category_name": category.category_name,
                "isAttempt": False})
    return {
        "allCategoryDetails": details,
        "allCategoryMarks": all_category_marks
    }
