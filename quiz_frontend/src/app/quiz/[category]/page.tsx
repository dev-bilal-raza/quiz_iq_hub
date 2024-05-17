"use client"
import React, { use, useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { isQuizAvailable, getQuizDetails, deleteQuiz } from '@/api-actions/quizApiActions'
import { useAppSelector} from '@/app/redux/hooks'
import Header from '@/components/layout/Header'
import Loader from '@/components/layout/Loader'
import Button from '@/components/layout/Button'
import { QuizDetails } from '@/types/quizType'

const page = ({ params }: { params: { category: string } }) => {
    const router = useRouter();
    const user: any = useAppSelector(state => state.user.user);
    const [quizDetails, setQuizDetails] = useState<QuizDetails | null>();
    const [isAvailable, setIsAvailable] = useState(true);
    const [loader, setLoader] = useState(true);
    const [error, setError] = useState("");
    const [startQuizPopup, setStartQuizPopup] = useState(false);
    console.log(params.category);
    let category = "";

    for (const str of params.category) {
        console.log(str);

        if (str == "%" || str == "2" || str == "0") {
            console.log("hello");

            category += "  "
        } else {
            category += str
        }
    }
    const titlecategory = category.charAt(0).toUpperCase() + category.slice(1);

    useEffect(() => {
        //2) TODO: If quiz is avilable then, you have to fetch a deatils of quiz for this category 
        const get_quiz_details = async () => {
            //1) TODO: here you will need to c heck that the quiz is available for this category or not
            const response = await isQuizAvailable(category);
            const is_quiz_available = await response.json();
            if (response.ok) {
                if (is_quiz_available) {
                    const response = await getQuizDetails({ category_name: category, user_id: user.user_id });
                    if (response.ok) {
                        const quiz_details = await response.json();
                        if (!quiz_details.isAttempt) {
                            console.log(quiz_details);
                            setStartQuizPopup(true);
                            setQuizDetails(null)
                            setLoader(false);
                        } else {
                            console.log(quiz_details);
                            setQuizDetails(quiz_details.quizDetails);
                            setStartQuizPopup(false);
                            setLoader(false);
                        };
                    };
                } else {
                    setQuizDetails(null)
                    setIsAvailable(false);
                    setLoader(false);
                }
            } else {
                setError(is_quiz_available.message);
                setLoader(false);
            };
        };
        get_quiz_details();
    }, []);

    return (
        // header
        <main className='h-screen'>
            <Header />
            {loader ?
                <div className='w-full flex justify-center mt-16'>
                    <Loader />
                </div>
                : !isAvailable ?
                    <div className='w-full mt-16 flex justify-center'>
                        <h2 className='text-2xl md:text-4xl font-bold font-heading text-slate-400 text-center'>{titlecategory} Quiz is not available yet 😔</h2>
                    </div>
                    : startQuizPopup ?
                        <div className='backdrop-blur-sm absolute z-50 top-0 bottom-0 left-0 right-0 flex justify-center items-center '>
                            <div className='flex flex-col gap-7 border-2 border-black rounded-lg sm:w-1/3  p-4 bg-[#65798b] '>
                                <div className='w-full flex justify-end'>
                                    <button className='text-2xl' onClick={() => router.push(`/quiz/`)}>✖</button>
                                </div>
                                <h3 className='w-full font-heading text-xl md:text-2xl text-black font-bold'>
                                    Do you want to start {titlecategory} Quiz?
                                </h3>
                                <div className='w-full flex justify-center gap-2'>
                                    <Button ButtonType='button' isDeleted={false} onClick={() => router.push(`/quiz/${category}/questions/`)}>
                                        Yes
                                    </Button>
                                </div>
                            </div>
                        </div>
                        :
                        <section className='m-4 md:m-0 text-white flex flex-col justify-center items-center gap-3 pt-10'>
                            <h1 className='text-center font-heading md:text-4xl text-2xl font-bold'>{user.user_name.split(" ")[0].charAt(0).toUpperCase() + user.user_name.split(" ")[0].slice(1)}'s {titlecategory} Quiz Details</h1>
                            <div className='w-full md:w-2/4 m-4 flex flex-col rounded-md bg-gradient-to-tr from-slate-600 via-slate-700 to-[#041327] justify-center items-center gap-3 p-8'>
                                <div className='w-full border border-gray-800 rounded-md p-2 flex gap-3 items-center justify-between'>
                                    <h2 className='text-lg font-para'>Quiz Category</h2>
                                    <h2 className='font-para text-lg'>{titlecategory}</h2>
                                </div>
                                <div className='w-full border border-gray-800 rounded-md p-2 flex gap-3 items-center justify-between'>
                                    <h2 className='text-lg font-para'>Is finished ?</h2>
                                    <h2 className='font-para text-lg'>{quizDetails?.is_finished ? "✔️" : "❌"}</h2>
                                </div>
                                <div className='w-full border border-gray-800 rounded-md p-2 flex gap-3 items-center justify-between'>
                                    <h2 className='text-lg font-para'>Remaining Questions</h2>
                                    <h2 className='text-lg'>{quizDetails?.remaining_questions}</h2>
                                </div>
                                <div className='w-full border border-gray-800 rounded-md p-2 flex gap-3 items-center justify-between'>
                                    <h2 className='text-lg font-para'>Score</h2>
                                    <h2 className='text-lg'>{quizDetails?.category_marks}/{quizDetails?.obtaining_marks}</h2>
                                </div>
                                <div className='w-full border border-gray-800 rounded-md p-2 flex gap-3 items-center justify-between'>
                                    <h2 className='text-lg font-para'>Percentage</h2>
                                    {
                                        quizDetails?.percentage ?
                                            <div className='flex flex-col items-end'>
                                                <h3 className='text-lg'>{quizDetails?.percentage}%</h3>
                                                <div className='w-48 h-2 rounded-full bg-gray-500'>
                                                    <div className={`h-full rounded-full bg-green-500 ${quizDetails?.percentage <= 30 ? "w-1/5 bg-red-500" : quizDetails?.percentage <= 50 ? "w-2/5" : quizDetails?.percentage <= 70 ? "w-4/6" : quizDetails?.percentage <= 90 ? "w-11/12" : "w-full"} `} />
                                                </div>
                                            </div>
                                            : 0
                                    }
                                </div>
                                <div className='w-full border border-gray-800 rounded-md p-2 flex gap-3 items-center justify-between'>
                                    <h2 className='text-lg font-para'>Rank</h2>
                                    <h2 className='text-lg'>{quizDetails?.rank ? quizDetails.rank : "--"}</h2>
                                </div>
                                <div className='w-full flex justify-center'>
                                    {
                                        quizDetails?.is_finished ?
                                            <Button ButtonType='button' isDeleted={true} onClick={() => {
                                                deleteQuiz(quizDetails.user_id, quizDetails.category_id);
                                                // dispatch(fetchUser())
                                                router.push("/quiz")
                                            }
                                            }>Delete Quiz</Button>
                                            :
                                            <Button ButtonType='button' isDeleted={false} onClick={() => router.push(`/quiz/${category}/questions/`)}>Attempt Questions</Button>
                                    }
                                </div>
                            </div>
                        </section>
            }
        </main>
    )
}

export default page