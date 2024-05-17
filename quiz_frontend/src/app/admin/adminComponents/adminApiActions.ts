import { QuestionForm } from "@/types/quizType";
import { cookie_getter } from "@/lib/cookie";
import router from "next/router";

export async function verifyAdmin(admin_token: string) {
    const response = await fetch("http://localhost:8000/api/verifyAdmin", {
        headers: {
            "Authorization": "Bearer " + admin_token
        }
    })
    console.log(await response.json());
    return response;
}

export async function deleteTokenFromDB(admin_token_id: number) {
    const response = await fetch(`http://localhost:8000/api/deleteToken?token_id=${admin_token_id}`,
        {
            method: "DELETE"
        }
    )
        .then((res) => res.json());
    localStorage.removeItem("admin_token_id")
    console.log(response);
}

export async function getCategories() {
    const categories = await fetch("http://localhost:8000/api/getQuizCategories").then((res) => res.json());
    return categories;
}

export async function addCategory(categoryInput: string, categoryDetails: string, category_marks: number, adminToken: string) {
    const response = await fetch("http://localhost:8000/api/addCategory", {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "Authorization": "Bearer " + adminToken
        },
        body: JSON.stringify(
            {
                "category": categoryInput,
                "category_description": categoryDetails,
                "category_marks": category_marks
            }
        )
    });
    return response;
}

export async function addQuestion(admin_token: string, data: QuestionForm) {
    const response = await fetch("http://localhost:8000/api/addQuiz",
        {
            method: "POST",
            headers: {
                "content-type": "application/json",
                "Authorization": "Bearer " + admin_token
            },
            body: JSON.stringify(data)
        }
    )
    return response
}


export const admin_verification = async () => {
    const adminToken = cookie_getter("admin_token");
    const admin_token_id = 6

    if (adminToken && admin_token_id) {
        const response = await verifyAdmin(adminToken);
        if (!response.ok) {
            return false
        };
        return true
        // const categories = await getCategories();
        // if (categories) setCategories(categories);
        // setLoading(false);

    } else if (admin_token_id) {
        await deleteTokenFromDB(Number(admin_token_id));
        return false
    } else {
        return false
    };
};

export const generate_question = async (category: number) => {
    const response = await fetch(`/api/generate_mcqs?category=${category}`)
    if (response.ok) return await  response.json()
        
}