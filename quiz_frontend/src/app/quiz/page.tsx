"use client"
import React, { useState } from 'react'
import { useEffect } from 'react'
import { Category } from '@/types/quizType';
import Link from 'next/link';
import { CardBody, CardContainer, CardItem } from '@/components/ui/3dCard';
import Header from '@/components/layout/Header';
import Loader from '@/components/layout/Loader';

const page = () => {
  const [categories, setCategories] = useState<Category[]>([])
  const [isError, setError] = useState<string>();
  const [isLoading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const getCategories = async () => {
      const response = await fetch("http://localhost:8000/api/getQuizCategories"
      );
      const data = await response.json();
      if (!response.ok) {
        console.log(data);
        setError("You are not authorized to Quiz.");
        setCategories([]);
      };
      setCategories(data);
      setLoading(false);
      data.map((category: any) => {
        // console.log(category.category_description.);
      })
    };
    getCategories();
  }, []);
  if (isError) return <h1>{isError}</h1>

  return (
    <main className='w-full h-screen bg-black'>
      <Header />
      <section className='h-36 flex w-11/12 mx-auto justify-center items-center '>
        <h1 className='text-white md:text-5xl text-xl font-heading border-b'>
          Available Topics for Quiz
        </h1>
      </section>
      {/* flex flex-wrap gap-10 max-w-7xl mx-auto mt-3 */}
      {isLoading ?
        <div className='w-full flex justify-center items-center'>
          <Loader />
        </div> :
        <section className='flex flex-wrap gap-10 max-w-6xl mx-auto p-4'>
          {categories.map((category) => (
            <Link key={category.category_id} href={`/quiz/${category.category_name}`}>
              <CardContainer className="inter-var">
                <CardBody className="">
                  <CardItem translateZ="100" className="w-full mt-4">
                    <div className='flex gap-4 flex-col justify-center items-center text-white border rounded-lg w-56 h-44 p-3 shadow-[0px_0px_15px_5px_#072C45]'>
                      <h3 className='text-center font-heading text-xl md:text-2xl '>{category.category_name.charAt(0).toUpperCase() + category.category_name.slice(1)}</h3>
                      <p className='text-center font-para'>{category.category_description.split(".")[0]}...</p>
                    </div>
                  </CardItem>
                </CardBody>
              </CardContainer>
            </Link>
          ))}
        </section>
      }
    </main>
  );
};
// text-white border rounded-lg w-56 h-44 p-3 shadow-[0px_0px_15px_5px_#072C45]
export default page;