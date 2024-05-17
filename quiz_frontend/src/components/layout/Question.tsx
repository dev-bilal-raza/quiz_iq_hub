import { Questions } from '@/types/quizType'
import React from 'react'

const Question = ({ questions, quizNumber }: {
    questions: Questions[],
    quizNumber: number
}) => {
    return (
        <div className='w-full md:w-2/4 rounded-xl bg-gradient-to-r from-purple-700 via-[#082B44] to-blue-500 p-3 mt-8'>
            <div className='bg-black w-full h-80 flex justify-center items-center p-5'>
                <h4 className='font-heading text-2xl text-center sm:text-3xl tracking-wide'>
                    {questions[quizNumber] && questions[quizNumber].question.endsWith("?") ? questions[quizNumber].question : questions[quizNumber] && questions[quizNumber].question + "?"}
                </h4>
            </div>
        </div>
    )
}

export default Question