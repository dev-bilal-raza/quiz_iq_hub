"use client";
import Image from "next/image";
import React from "react";
import { CardContainer, CardBody, CardItem } from "../ui/3dCard";
import heroImage from "../../../public/laptopImage.png"
import Button from "./Button";
import { BackgroundBeams } from "../ui/BackgroundBeams";
import { useAppSelector } from "@/app/redux/hooks";
import Link from "next/link";
export function HeroSection() {
    const status = useAppSelector(state => state.user.status);
    return (
        <main className="relative">
            <BackgroundBeams />
            <section className="flex p-20 items-center md:justify-between justify-center gap-5 relative z-30  rounded">
                <div className="flex flex-col gap-10  items-center border-white text-center w-full lg:w-3/5 text-white ">
                    <h1 className="lg:text-5xl text-4xl shadow-[4.0px_8.0px_8.0px_rgba(0,0,0,0.38)] bg-gradient-to-r from-slate-50 to-blue-400 bg-clip-text text-transparent font-heading font-bold">
                        Welcome to the QuizIQHub
                    </h1>
                    <p className="text-lg lg-text-xl font-para leading-relaxed">
                        <span className="font-semibold"><q> Knowledge is a treasure, but practice is the key to it.</q></span> – Unlock the vault of wisdom with each question you answer!
                    </p>
                    <Link href={status?"/quiz":"/login"}>
                    <Button ButtonType="button" isDeleted={false} classnames={"w-24 "}>
                        {status?"Quiz": "Sign in"}
                    </Button>
                    </Link>
                </div>
                <div className="py-20 w-5/12 lg:block hidden">
                    <CardContainer className="inter-var ">
                        <CardBody className=" ">
                            <CardItem translateZ="100" className="w-full mt-4">
                                <Image
                                    src={heroImage}
                                    height="1000"
                                    width="1000"
                                    className="h-100 w-full object-cover rounded-xl group-hover/card:shadow-xl"
                                    alt="thumbnail"
                                />
                            </CardItem>
                        </CardBody>
                    </CardContainer>
                </div>
            </section>
        </main>

    );
}
