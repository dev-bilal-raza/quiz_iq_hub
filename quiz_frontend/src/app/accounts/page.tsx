"use client"
import React, { useEffect, useState } from 'react'
import Image from 'next/image'
import logo from "../../../public/logo.png"
import { useAppSelector } from '../redux/hooks'
import { getAllCategoriesDetails } from '@/api-actions/quizApiActions'
import { useRouter } from 'next/navigation'
import { CategoriesDetails } from '@/types/quizType'
import Loader from '@/components/layout/Loader'
import Link from 'next/link'
import Logout from '@/app/(auth)/logout/Logout'
import Circle from '@/components/layout/Circle'
import Avatar from '@/components/layout/Avatar'
import UserAccountDetails from '@/components/layout/UserAccountDetails'

const page = () => {
    const router = useRouter();
    const [quizCategoryDetails, setQuizCategoryDetails] = useState<CategoriesDetails>();
    const [isLoading, setLoading] = useState(true);
    const [userPercentage, setUserPercentage] = useState<number>(0);
    const user: any = useAppSelector(state => state.user.user);
    const status: any = useAppSelector(state => state.user.status);
    useEffect(() => {
        if (status) {
            const getCategoryDetails = async () => {
                const response = await getAllCategoriesDetails(user.user_id);
                if (response.ok) {
                    const details = await response.json();
                    setQuizCategoryDetails(details);
                    setUserPercentage(user.total_points / details.allCategoryMarks * 100)
                    setLoading(false);
                    console.log(details);
                };
            };
            getCategoryDetails();
            console.log(userPercentage);
            console.log(quizCategoryDetails);
        } else {
            router.push("/login");
        };
    }, []);
    return (
        <main className='text-black'>
            <section className='bg-gradient-to-tr from-black via-slate-950 to-sky-950 pb-2'>
                <div className='flex flex-col  justify-center items-center'>
                    <Link href={"/"}>
                        <Image className='' height={50} width={70} src={logo} alt='Quiz App' />
                    </Link>
                </div>
            </section>
            {isLoading ? (
                <div className='flex justify-center items-center mt-8 h-96'>
                    <Loader />
                </div>
            ) :
                (
                    <section className='bg-white m-4 rounded-xl p-12 pt-5 pb-20 bg-gradient-to-b from-[#072840] from-0% via-sky-100 via-100% to-[#072840] to-100%'>
                        <div className='font-para flex sm:flex-row flex-col gap-4 text-gray-300 items-center justify-between m-7'>
                            <h2>
                                QuizIQHub Account
                            </h2>
                            <Logout user_id={user?.user_id} />
                        </div>
                        <div className='max-w-7xl h-0.5 bg-gradient-to-r from-[#37556A] from-10% via-gray-300 to-[#37556A] to-85% mx-auto' />
                        <div>
                            <section>
                                <div className='flex lg:flex-row flex-col'>
                                    <div className='w-full lg:w-1/5 lg:border-r-2 border-[#AFCBDD]'>
                                        {user ? <Avatar user_name={user.user_name} height={100} width={100}
                                            fillMode='#B0CCDD' /> : ""}
                                        <UserAccountDetails user_id={user?.user_id} user_email={user?.user_email} user_name={user?.user_name} />
                                    </div>
                                    <div className='w-full lg:w-2/3'>
                                        <div className='flex justify-center items-center p-3 m-3'>
                                            <h2 className='font-heading text-4xl font-bold'>Quiz Details</h2>
                                        </div>
                                        <div className='flex justify-center items-center'>
                                            <div className='flex justify-between p-3 gap-5 items-center border-2 border-zinc-300 rounded-xl'>
                                                <h2 className='font-heading text-2xl font-semibold'>
                                                    Total Points
                                                </h2>
                                                <Circle userPercentage={userPercentage} />
                                            </div>
                                        </div>
                                        <div className='flex flex-wrap gap-8 p-4 mt-4'>
                                            {quizCategoryDetails && quizCategoryDetails?.allCategoryDetails.map((item) => (
                                                <Link href={`/quiz/${item.category_name}`} key={item.category_name}>
                                                    <div className='flex justify-between gap-5 items-center p-6 border-2 rounded-2xl hover:bg-slate-100 border-gray-300'>
                                                        <h2 className='font-para text-lg '>
                                                            {item.category_name.charAt(0).toUpperCase() + item.category_name.slice(1)}
                                                        </h2>
                                                        <p>
                                                            {item.isAttempt ? "✔" : "✖"}
                                                        </p>
                                                    </div>
                                                </Link>
                                            ))}
                                        </div>
                                        <div>
                                        </div>
                                    </div>
                                </div>
                            </section>
                        </div>
                    </section>
                )
            }
        </main>
    )
}

export default page