export interface Category {
    category_id: number,
    category_name: string,
    category_description: string
}
export interface FormType {
    userFirstName: string,
    userLastName: string,
    userEmail: string,
    userPassword: string
}

export interface Questions {
    question_id: number,
    category_id: number,
    question: string
}
export type Choices = [
    {
        choice_status: boolean,
        question_id: number,
        choice: string,
        choice_id: number
    },
]

export interface QuestionForm {
    question: string,
    category_id: number,
    choice1: {
        choice: string,
        status: boolean
    },
    choice2: {
        choice: string,
        status: boolean
    },
    choice3: {
        choice: string,
        status: boolean
    },
    choice4: {
        choice: string,
        status: boolean
    }
}
export interface Options {
    httpOnly?: boolean,
    secure?: boolean,
    sameSite?: "lax" | "strict" | "none"
}

export interface AttemptQuizType {
    user_id: number,
    category_id: number,
    quiz_numbers: number,
    isFinished: boolean
}

export interface GetQuizDetailsForm {
    user_id: number,
    category_name: string
}

export interface QuizDetails {
    category_id: number,
    category_marks: number,
    id: number,
    is_finished: boolean,
    obtaining_marks: number,
    remaining_questions: number,
    percentage: number,
    rank: string,
    user_id: number,
}
interface allCategoryDetails {
    category_name: string,
    isAttempt: boolean
}
export interface CategoriesDetails {
    allCategoryDetails: allCategoryDetails[],
}