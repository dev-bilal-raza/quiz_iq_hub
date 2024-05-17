import React, { useState } from 'react'
import { useForm, SubmitHandler } from 'react-hook-form';
import { QuestionForm } from '@/types/quizType';
import { Category } from '@/types/quizType';
import { cookie_getter } from '@/lib/cookie';
import { addQuestion, generate_question } from './adminApiActions';


const SetQuestion = ({ categories }: {
  categories: Category[]
}) => {
  const [category, setCategory] = useState(0);
  const [error, setError] = useState<string>();
  const [resMessage, setResMessage] = useState<string>();
  const { register, handleSubmit, reset } = useForm<QuestionForm>();
  const admin_token = cookie_getter("admin_token");

  const generateQuestion = async () => {
    console.log(category);
    if (category === 0) {
      setError("Please select a category");
    } else {
      setError("");
      const data = await generate_question(category);
      console.log(data);
      console.log(data["choices"][0]["option"]);
      
      data.choices.map((choice: any)=>{

      })

      reset({
        question: data.question,
        choice1: {
          choice: data["choices"][0]["option"],
          status: data["choice"][0]["status"]
        },
        choice2: {
          choice: data["choices"][1]["option"],
          status: data["choice"][1]["status"]
        },
        choice3: {
          choice: data["choices"][2]["option"],
          status: data["choice"][2]["status"]
        },
        choice4: {
          choice: data["choices"][3]["option"],
          status: data["choice"][3]["status"]
        }
      })
    }
  }
  const setQuestion: SubmitHandler<QuestionForm> = async (data: QuestionForm) => {
    setResMessage("")
    if (data.choice1.status || data.choice2.status || data.choice3.status || data.choice4.status) {
      reset({
        question: "",
        choice1: {
          choice: "",
          status: false
        },
        choice2: {
          choice: "",
          status: false
        },
        choice3: {
          choice: "",
          status: false
        },
        choice4: {
          choice: "",
          status: false
        }
      })
      if (admin_token) {
        const response = await addQuestion(admin_token, data)
        const message = await response.json()
        if (!response.ok) {
          setError(message.message)
          setResMessage("")
        } else {
          setResMessage(message)
          setError("")
        }
        console.log(message);
      }
    } else {
      setError("Please select correct answer from checkbox")
    }
  }

  return (
    <div className='rounded-md items-center flex flex-col gap-5 m-6 p-5 bg-gradient-to-b from-slate-800 via-slate-400 to-slate-300'>
      <h2 className='text-3xl md:text-4xl text-white font-heading font-bold'>
        Add Question
      </h2>
      <form onSubmit={handleSubmit(setQuestion)} className='w-full border p-3 rounded-lg'>
        <div className='flex sm:flex-row flex-col w-full gap-3'>
          <div className='w-full sm:w-6/12'>
            <label htmlFor="categories" className=' mb-2 font-medium text-white'> Question </label>
            <input className='bg-gray-50 border m-2  border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5' placeholder='What is Typescript?' type="text" {...register("question", { required: true })} />
            <label htmlFor="categories" className=' mb-2 font-medium text-white'>Choice 01</label>
            <input className='bg-gray-50 border m-2  border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5' placeholder='A programming language developed by Microsoft.' type="text" {...register("choice1.choice", { required: true })} />
            <label htmlFor="categories" className=' mb-2 font-medium text-gray-900'>Choice 02</label>
            <input className='bg-gray-50 border m-2 border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5' placeholder='A Compiler language.' type="text" {...register("choice2.choice", { required: true })} />
            <label htmlFor="categories" className=' mb-2 font-medium text-gray-900'>Choice 03</label>
            <input className='bg-gray-50 border m-2  border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5' placeholder='Adds static types to JavaScript' type="text" {...register("choice3.choice", { required: true })} />
            <label htmlFor="categories" className=' mb-2 font-medium text-gray-900'>Choice 04</label>
            <input className='bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full m-2 p-2.5' placeholder='A superset of JavaScript.' type="text" {...register("choice4.choice", { required: true })} />
          </div>

          <div className='w-full sm:w-6/12 flex flex-col items-center'>
            <div className='w-full'>

              <label htmlFor="categories" className='font-medium text-white'> Select Category</label>
              <select id="" className='bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full m-2 p-2.5' {...register("category_id")} onChange={(e) => setCategory(Number(e.target.value))}>
                {categories.map((category) => (
                  <option value={category.category_id} key={category.category_id}>
                    {category.category_name}
                  </option>
                ))}
              </select>
            </div>
            <div className='w-full'>
              <h3 className="font-medium text-white">Choose Correct Answer</h3>
              <ul className="m-2 items-center w-full text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-lg lg:flex">
                <li className="w-full border-b border-gray-200 sm:border-b-0 sm:border-r">
                  <div className="flex items-center ps-3">
                    <input id='choice01' type="checkbox" className="w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500" {...register("choice1.status")} />
                    <label htmlFor="choice01" className="w-full py-2.5 ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">Choice 01</label>
                  </div>
                </li>
                <li className="w-full border-b border-gray-200 sm:border-b-0 sm:border-r">
                  <div className="flex items-center ps-3">
                    <input id="choice2" type="checkbox" className="w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500" {...register("choice2.status")} />
                    <label htmlFor="choice2" className="w-full py-2.5 ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">Choice 02</label>
                  </div>
                </li>
                <li className="w-full border-b border-gray-200 sm:border-b-0 sm:border-r">
                  <div className="flex items-center ps-3">
                    <input id="choice3" type="checkbox" className="w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500" {...register("choice3.status")} />
                    <label htmlFor="choice3" className="w-full py-2.5 ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">Choice 03</label>
                  </div>
                </li>
                <li className="w-full border-b border-gray-200 sm:border-b-0">
                  <div className="flex items-center ps-3">
                    <input id="choice4" type="checkbox" className="w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500" {...register("choice4.status")} />
                    <label htmlFor="choice4" className="w-full py-2.5 ms-2 text-sm font-medium text-gray-900">Choice 04</label>
                  </div>
                </li>
              </ul>
              <button type='button' className='m-2 p-2 px-6 text-white bg-slate-900 hover:bg-slate-800 rounded-lg'
                onClick={generateQuestion} >
                Generate via AI
              </button>
            </div>
          </div>
        </div>
        <div className='flex flex-col justify-center items-center'>
          <button className='rounded-lg p-2.5 mx-auto bg-slate-900 hover:bg-slate-800 text-white shrink-0' type='submit'>Add Question</button>
          <p className='text-lg font-semibold text-red-600'>{error ? error : ""}</p>
          <p className='text-lg font-semibold text-green-400'>{resMessage ? resMessage : ""}</p>
        </div>
      </form>
    </div>
  )
};

export default SetQuestion