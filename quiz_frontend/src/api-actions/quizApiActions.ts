
import { AttemptQuizType, GetQuizDetailsForm } from "@/types/quizType"

export const logoutUser = async (user_id: number) => {
    const response = await fetch(`/api/logout?user_id=${user_id}`,
        {
            method: "DELETE"
        })
    return response
}


export const attemptQuiz = async (quiz_details: AttemptQuizType) => {
    const response = await fetch("/api/attemptQuiz",
        {
            method: "POST",
            headers: {
                "content-type": "application/json"
            },
            body: JSON.stringify(quiz_details)
        }
    )
    return response
}

export const isQuizAvailable = async (category_name: string) => {
    const response = await fetch(`http://localhost:8000/api/isAvailableQuiz?category_name=${category_name}`,
    );
    return response;
};

export const getQuiz = async (user_id: number, category: string) => {
    const response = await fetch(`/api/getQuiz?user_id=${user_id}&category_name=${category}`)
    return response;
}

export const getQuizDetails = async (getDetails: GetQuizDetailsForm) => {
    const response = await fetch(`http://localhost:8000/api/getCategoryQuizDetails?user_id=${getDetails.user_id}&category_name=${getDetails.category_name}`,
    );
    return response;
};

export const deleteQuiz = async (user_id: number, category_id: number) => {
    const response = await fetch(`http://localhost:8000/api/deleteQuiz?user_id=${user_id}&category_id=${category_id}`,
        {
            method: 'DELETE',
        }
    );
    return response;
}

export const getAllCategoriesDetails = async (user_id: number,) => {
    const response = await fetch(`http://localhost:8000/api/getAllCategoryDetails?user_id=${user_id}`,
    );
    return response;
};
export const get_quiz = async (category: string, user_id: number) => {
    const response = await fetch(`http://localhost:8000/api/getQuiz?user_id=${user_id}&category_name=${category}`);
    const data = await response.json();
    if (response.ok) {
        return { questions: data.questions, choices: data.choices }
    };
    throw new Error("Quiz not found")
};
