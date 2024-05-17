import React from 'react'
import Image from 'next/image'
import logo from "../../../public/logo.png"
import { FaFacebook, FaGithub, FaLinkedin, FaYoutube } from "react-icons/fa";
import Link from 'next/link';

const Footer = () => {
  return (
    <footer className='text-white p-8'>
      <div className='flex sm:flex-row flex-col gap-4 items-center'>
        <div className='w-11/12 flex flex-col gap-3 sm:border-r  border-gray-500 p-4'>
          <Link href={"/"}>
            <Image className='w-20' src={logo} alt='QuizIQHub' />
          </Link>
          <p className='font-para font-extralight tracking-wide'>
            Our mission is to empower every aspiring coder with the confidence and skills needed to succeed. Through our comprehensive programming courses, we offer valuable learning resources tailored to students of all levels. Additionally, our MCQ-based exams provide a practical assessment framework, allowing students to gauge their understanding and progress effectively. Our goal is not only to impart knowledge but also to foster self-recognition and growth, enabling students to realize their full potential in the dynamic world of coding and programming.
          </p>
        </div>
        <div className=' flex gap-4'>
          <ul className='flex sm:flex-col flex-row gap-3'>
            <li>
              <Link href={"http://facebook.com"}>
                <FaGithub className='text-2xl hover:text-slate-500' />
              </Link>
            </li>
            <li>
              <Link href={"http://facebook.com"}>
                <FaLinkedin className='text-2xl hover:text-blue-400' />
              </Link>
            </li>
            <li>
              <Link href={"http://facebook.com"}>
                <FaYoutube className='text-2xl hover:text-red-400' />
              </Link>
            </li>
            <li>
              <Link href={"http://facebook.com"}>
                <FaFacebook className='text-2xl hover:text-blue-400' />
              </Link>
            </li>
          </ul>
        </div>
        <div></div>
      </div>
      <div className='h-0.5 bg-gradient-to-r from-black via-slate-900 to-black m-4' />
      <div className='font-para flex justify-center p-2'>
        <p>© 2024 QuizIQHub - All right reserved</p>
      </div>
    </footer>
  )
}

export default Footer