"use client";
import React from "react";
import { AnimatedTooltip } from "../ui/AnimatedTooltip";
import ahsaanAvatar from "../../../public/ahsaanAvatar.jpg"
import sirQasimAvatar from "../../../public/sirQasimAvatar.png"
import sirZiaAvatar from "../../../public/sirZiaAvatar.png"
import sirOkashaAvatar from "../../../public/sirOkashaAvatar.png"
import sirHamzaAvatar from "../../../public/sirHamzaAvatar.jpeg"
import mustafaAvatar from "../../../public/mustafaAvatar.jpeg"
import hammadAvatar from "../../../public/hammadAvatar.jpeg"
import bilalAvatar from "../../../public/bilalAvatar.png"
import Container from "./Container";
const people = [
    {
        id: 1,
        name: "Zia Khan",
        designation: "AI Engineer",
        image: sirZiaAvatar,
    },
    {
        id: 2,
        name: "Muhammad Qasim",
        designation: "AI Engineer",
        image: sirQasimAvatar,
    },
    {
        id: 3,
        name: "Hamza Syed",
        designation: "Jamstack Developer",
        image: sirHamzaAvatar
    },
    {
        id: 4,
        name: "Okasha Tantoli",
        designation: "Jamstack Developer",
        image: sirOkashaAvatar,
    },
    {
        id: 5,
        name: "Mustafa Zuberi",
        designation: "Web Developer",
        image: mustafaAvatar,
    },
    {
        id: 6,
        name: "Ahsaan Abbasi",
        designation: "Jamstack Developer",
        image: ahsaanAvatar,
    },
    {
        id: 7,
        name: "Hammad",
        designation: "Jamstack Developer",
        image: hammadAvatar,
    },
    {
        id: 8,
        name: "Bilal Raza",
        designation: "Web Developer",
        image: bilalAvatar,
    },
];

export function Teachers() {
    return (
        <main>
            <section className="pt-20">
                <h1 className="text-center text-5xl font-bold font-heading bg-gradient-to-r from-slate-900 to-gray-600 bg-clip-text text-transparent">
                    Our Valueble Teachers
                </h1>
                <div className="flex md:flex-row flex-col md:items-center  md:justify-between gap-6 m-14">
                    <div className="w-full md:w-3/6 md:order-first order-last  ">
                        <p className="font-para leading-relaxed md:text-start text-center">
                            Our teaching faculty comprises a team of highly skilled professionals, each bringing unique expertise to our educational platform. <strong>Sir Zia</strong> and <strong>Sir Qasim</strong>, both <em>AI Engineers</em>, instill a passion for innovation and problem-solving in students through their deep understanding of artificial intelligence. <strong>Sir Hamza</strong> and <strong>Sir Okasha</strong>, adept <em>Jamstack Developers</em>, empower students to build fast and secure web applications, utilizing the latest Jamstack technologies. <strong>Sir Mustafa</strong>, <strong>Sir Ahsaan</strong>, <strong>Sir Hammad</strong>, and <strong>Sir Bilal</strong>, our seasoned <em>Web Developers</em>, provide comprehensive instruction in frontend and backend development, equipping students with the tools and knowledge needed to thrive in the dynamic field of web development. Together, our dedicated faculty fosters a collaborative learning environment where students can explore, innovate, and succeed.
                        </p>
                    </div>
                    <div className="flex flex-col w-full md:w-1/2 items-center">
                        <div className="flex flex-row items-center justify-center mb-10 w-full">
                            <AnimatedTooltip items={people} />
                        </div>
                        <blockquote cite="https://www.teachthought.com/pedagogy/great-best-quotes-about-teaching/" className="text-center font-semibold font-para">
                            A good teacher is like a candle – it consumes itself to light the way for others
                        </blockquote>
                    </div>
                </div>
            </section>
        </main>
    );
}
