import React from "react";
import { StickyScroll } from "../ui/StickyScroll";
import Image from "next/image";
import { TracingBeam } from "../ui/TracingBeam";
import typescriptCourse from "../../../public/typescriptCourseImage.png"
import nextJSCourse from "../../../public/nextJsCourseImage.png"
import PythonCourse from "../../../public/pythonCourseImage.png"
import AICourse from "../../../public/aiCourse.png"
import Link from "next/link";

const content = [
    {
        title: "Typescript Course",
        description:
            "TypeScript is a statically typed superset of JavaScript that enhances your code with additional features like type checking, interfaces, and better tooling. It’s widely used in modern web development to build robust and maintainable applications.",
        content: (
            <div className="h-full w-full text-white">
                <Image
                    src={typescriptCourse}
                    width={100}
                    height={100}
                    className="h-full w-full object-cover"
                    alt="linear board demo"
                />
            </div>
        ),
    },
    {
        title: "Next-JS Course",
        description:
            "Next.js is a powerful React framework for building server-rendered and statically generated web applications. It simplifies routing, optimizes performance, and provides a delightful developer",
        content: (
            <div className="h-full w-full text-white">
                <Image
                    src={nextJSCourse}
                    width={100}
                    height={100}
                    className="h-full w-full object-cover"
                    alt="linear board demo"
                />
            </div>
        ),
    },
    {
        title: "Python Course",
        description:
            "Python is a versatile and beginner-friendly programming language. It’s used for web development, data analysis, machine learning, and more. Learning Python opens up a world of possibilities!",
        content: (
            <Link href={"https://www.youtube.com/playlist?list=PL0vKVrkG4hWrEujmnC7v2mSiaXMV_Tfu0"} target="_blank">
                <div className="h-full w-full text-white">
                    <Image
                        src={PythonCourse}
                        width={100}
                        height={100}
                        className="h-full w-full object-cover"
                        alt="linear board demo"
                    />
                </div>
            </Link>
        ),
    },
    {
        title: "Gen-AI Course",
        description:
            "General AI, often referred to as AGI (Artificial General Intelligence), aims to create machines that can perform any intellectual task that a human can. It’s an exciting field with immense potential.",
        content: (
            <div className="h-full w-full text-white">
                <Image
                    src={AICourse}
                    width={100}
                    height={100}
                    className="h-full w-full object-cover"
                    alt="linear board demo"
                />
            </div>
        ),
    },
];
export function Courses() {
    return (
        <div className="bg-[#0F172A]">
                <h1 className="text-5xl font-heading text-center p-6 text-gray-200 font-bold">Our Couses</h1>
            <div className="h-0.5 bg-gradient-to-r from-[#0F172A] via-gray-500 to-[#0F172A]
            m-1"/>
            <TracingBeam>
                <StickyScroll content={content} />
            </TracingBeam>
        </div>
    );
}
