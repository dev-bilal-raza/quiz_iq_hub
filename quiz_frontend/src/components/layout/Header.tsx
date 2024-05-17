"use client"
import Link from 'next/link'
import React, { useState } from 'react'
import Image from 'next/image'
import logo from "../../../public/logo.png"
import { useAppSelector } from '@/app/redux/hooks'
import { GiHamburgerMenu } from "react-icons/gi";
import { RxCross2 } from "react-icons/rx";
import Avatar from './Avatar'

const Header = () => {
    // const status = useSelector((state: RootState) => state.user.status);
    const [hamburgerNav, setHamburgerNav] = useState(false);
    const state = useAppSelector((state) => state.user);
    const status = useAppSelector((state) => state.user.status);
    const user: any = state.user;
    console.log(state.status);

    // status(state => state.user.status)
    const navItems = [
        {
            id: 1,
            link: "Home",
            path: "/",
            status: true
        },
        {
            id: 2,
            link: "Our Courses",
            path: "/courses",
            status: true
        },
        {
            id: 3,
            link: "Quiz",
            path: "/quiz",
            status: status
        },
        {
            id: 4,
            link: "Login",
            path: "/login",
            status: !status
        },
        {
            id: 5,
            link: "Signup",
            path: "/register",
            status: !status
        },
    ];
    return (
        <main className='w-full flex justify-center bg-gradient-to-tr from-black/25 via-slate-950 to-sky-950 sticky top-0 z-50'>
            <header className=' text-white  w-11/12 z-40'>
                <div className='flex justify-between items-center'>
                    <Link className='flex flex-col justify-center items-center ' href={"/"}>
                        <Image className='' height={50} width={70} src={logo} alt='Quiz App' />
                        <h3 className='font-serif tracking-widest mb-0.5'>
                            QuizIQHub
                        </h3>
                    </Link>
                    <div>
                        <nav className='md:block hidden'>
                            <ul className='flex gap-4 text-xl font-heading items-center font-extralight'>
                                {navItems.map((item) => (
                                    item.status ? <Link key={item.id} href={item.path}>{item.link}</Link> : null
                                ))}
                                {status ?
                                    <Link href={"/accounts"}>
                                        {/* <svg xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink" width="64px" height="50px" viewBox="0 0 64 64" version="1.1"><circle fill="#CDD9EF" cx="32" width="50" height="50" cy="32" r="32" /><text x="50%" y="50%" style={{ "color": "#222", "lineHeight": 1, "fontFamily": "-apple-system, BlinkMacSystemFont" }} alignmentBaseline="middle" textAnchor="middle" fontSize="28" fontWeight="400" dy=".1em" dominantBaseline="middle" fill="#222">{user && user.user_name.split(" ").map((name: string) => name.charAt(0).toUpperCase())}</text>
                                        </svg> */}
                                        <Avatar user_name={user.user_name} height={50} width={64} fillMode='#CDD9EF' />
                                    </Link>
                                    : null}
                            </ul>
                        </nav>
                        <div className='md:hidden block'>
                            {hamburgerNav ?

                                <div className='cursor-pointer' onClick={() => setHamburgerNav(!hamburgerNav)}>
                                    <RxCross2 className='text-white text-4xl' />
                                </div>
                                :
                                <div className='cursor-pointer' onClick={() => setHamburgerNav(!hamburgerNav)}>
                                    <GiHamburgerMenu className='text-white text-4xl' />
                                </div>
                            }
                        </div>
                    </div>
                </div>
                <div>
                    {
                        <ul className='flex gap-4 text-xl font-heading items-center font-extralight'>
                            {hamburgerNav ?
                                <div className='w-full flex flex-col items-center justify-center gap-2 m-2'>
                                    {status ?
                                        <Link href={"/accounts"}>
                                            <svg xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink" width="64px" height="50px" viewBox="0 0 64 64" version="1.1"><circle fill="#CDD9EF " cx="32" width="50" height="50" cy="32" r="32" /><text x="50%" y="50%" style={{ "color": "#222", "lineHeight": 1, "fontFamily": "-apple-system, BlinkMacSystemFont" }} alignmentBaseline="middle" textAnchor="middle" fontSize="28" fontWeight="400" dy=".1em" dominantBaseline="middle" fill="#222">{user && user.user_name.split(" ").map((name: string) => name.charAt(0).toUpperCase())}</text>
                                            </svg>
                                        </Link>
                                        : null}
                                    {navItems.map((item) => (
                                        item.status ? <Link key={item.id} href={item.path}>{item.link}</Link> : null
                                    ))}
                                </div> : ""}
                        </ul>
                    }
                </div>
            </header>
        </main >
    )
}

export default Header