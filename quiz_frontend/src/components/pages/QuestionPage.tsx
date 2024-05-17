"use client"
import React, { useEffect, useState } from 'react'
import { Choices, Questions } from '@/types/quizType'
import { useAppSelector, useAppDispatch } from '@/app/redux/hooks';
import { useRouter } from 'next/navigation';
import Button from '../layout/Button';
import { fetchUser } from '@/app/redux/features/user/userApi';
import { attemptQuiz } from '../../api-actions/quizApiActions';
import Loader from '../layout/Loader';
import Question from '../layout/Question';
import { get_quiz } from '../../api-actions/quizApiActions';


const QuestionPage = ({ category }: {
    category: string,
}) => {
    const [isAttempt, setIsAttempt] = useState(false);
    const [isCorrect, setIsCorrect] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const [quizNumber, setQuizNumber] = useState(0);
    const [questions, setQuestions] = useState<Questions[]>([]);
    const [choices, setChoices] = useState<Choices[]>([]);
    const dispatch = useAppDispatch();
    const router = useRouter();
    const user: any = useAppSelector(state => state.user.user);

    useEffect(() => {
        const getQuiz = async (category: string, user_id: number) => {
            const data = await get_quiz(category, user_id)
            setQuestions(data.questions);
            setChoices(data.choices);
            setIsLoading(false);
        };
        getQuiz(category, user.user_id)
    }, [])

    const quiz_attempt = async (isFinished: boolean) => {

        const res = await attemptQuiz({
            category_id: questions[quizNumber].category_id,
            user_id: user?.user_id,
            quiz_numbers: isCorrect ? 5 : 0,
            isFinished
        });
        if (isFinished) {
            dispatch(fetchUser())
            router.push(`/quiz/${category}`);
        };
        console.log(await res.json());

        setIsAttempt(false);
        // setIsCorrect(false);
        console.log(quizNumber);
        setQuizNumber(quizNumber + 1);
    };
    return (
        <main>
            {isLoading ? (
                <div className='flex justify-center items-center'>
                    <Loader />
                </div>
            )
                :
                (
                    <div className='flex md:flex-row flex-col gap-5 justify-between max-w-6xl mx-auto text-white m-12 mt-16 p-5'>
                        <Question questions={questions} quizNumber={quizNumber} />
                        <section className='w-full md:w-1/3'>
                            <ul className='flex h-full flex-col items-center justify-center gap-5'>
                                {isAttempt ? (
                                    <div className='flex flex-col gap-3'>
                                        {isCorrect ?
                                            <h2 className='text-green-600 font-heading text-3xl'>
                                                Correct Answer 🎉
                                            </h2> :
                                            <h2 className='text-red-400 font-heading text-3xl'>
                                                Wrong Answer 😞
                                            </h2>
                                        }
                                        {quizNumber < questions.length - 1 ?
                                            <Button isDeleted={false} ButtonType='button' onClick={() => {
                                                quiz_attempt(false)
                                            }}>Next Question</Button>
                                            :
                                            <Button isDeleted={false} ButtonType='button' onClick={() => {
                                                quiz_attempt(true)
                                            }}>Finish Question</Button>
                                        }
                                    </div>
                                ) :
                                    choices[quizNumber] && choices[quizNumber].map((item, index) => (
                                        <li className=" w-full hover:cursor-pointer p-1.5 rounded-xl bg-gradient-to-r from-gray-600 to-slate-900 hover:bg-gradient-to-r hover:from-purple-700 hover:via-blue-500 hover:to-[#082B44]" onClick={() => {
                                            setIsAttempt(true);
                                            setIsCorrect(item.choice_status);
                                        }}>
                                            <div className='flex p-2 gap-3 items-center bg-black w-full'>
                                                <h2 className='font-heading text-xl'>{index + 1}</h2>
                                                <h4 className='font-para'>{item.choice}</h4>
                                            </div>
                                        </li>
                                    ))}
                            </ul>
                        </section>
                    </div>
                )
            }
        </main>
    )
}

export default QuestionPage;