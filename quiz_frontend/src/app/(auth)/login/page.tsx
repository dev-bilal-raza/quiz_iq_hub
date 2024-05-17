"use client";
import { cookie_setter } from "@/lib/cookie";
import React, { useState } from "react";
import { Label } from "@/components/ui/Label";
import { Input } from "@/components/ui/Input";
import { cn } from "@/lib/utils";
import Image from "next/image";
import logo from "../../../../public/logo.png"
import { SubmitHandler, useForm } from "react-hook-form";
import Link from "next/link";
import { useAppDispatch } from "@/app/redux/hooks";
import { fetchUser } from "@/app/redux/features/user/userApi";
import { useRouter } from "next/navigation";

interface Form {
    userFirstName: string,
    userLastName: string,
    userEmail: string,
    userPassword: string,
}


export default function Login() {
    const { register, handleSubmit } = useForm<Form>();
    const dispatch = useAppDispatch();
    const router = useRouter();
    const [error, setError] = useState();
    const signUser: SubmitHandler<Form> = async (data: Form) => {
        const response = await fetch("/api/login",
            {
                method: 'POST',
                headers: {
                    "content-type": "application/json"
                },
                body: JSON.stringify({
                    "user_email": data.userEmail,
                    "user_password": data.userPassword
                })
            }
        );
        const auth_message = await response.json();
        if (!response.ok) {
            setError(auth_message.message)
        } else {

            // const addAccessToken = cookie_setter("access_token", userData.access_token.token, userData.access_token.expires_in,
            //     {
            //         secure: true,
            //         sameSite: "strict"
            //     });
        
            // const addRefreshToken = cookie_setter("refresh_token", userData.refresh_token.token, userData.refresh_token.expires_in, {
            //     secure: true,
            //     // httpOnly: true,

            //     sameSite: "strict"
            // });
            console.log(auth_message);

            dispatch(fetchUser());
            router.push("/")

            // console.log("Token", userData.refresh_token.token);
            // console.log("Token", userData.access_token.token);
            // console.log("Data from response", userData);
            // console.log("Data from filled form", data);
            // console.log("Token from cookie", getCookie("access_token"));
        }
    }
    return (
        <main className="bg-gradient-to-b from-[#083755] via-black to-black lg:bg-gradient-to-bl lg:from-[#042c44] lg:via-black lg:to-black h-screen flex items-center justify-center">
            <div className="flex justify-center items-stretch w-11/12 md:rounded-2xl  lg:shadow-[rgba(0,_0,_0,_0.4)_0px_30px_90px]">
                <div className="w-3/4 rounded-l-2xl lg:bg-gradient-to-br from-black from-10% via-[#083755] to-black to-85% justify-center lg:flex hidden">
                    <Image src={logo} alt="QuizIQHUB" className="object-cover" />
                </div>
                <div className="max-w-md w-full  mx-auto rounded-none text-white md:rounded-r-2xl p-4 md:p-8 shadow-input bg-[#000000]">
                    <h4 className="text-center m-2 text-red-500">{error ? error : ""}</h4>
                    <h2 className="font-bold text-xl text-center text-neutral-200">
                        Welcome to QuizIQHub
                    </h2>
                    <p className="text-sm max-w-sm mt-2 text-neutral-300">
                        Learning from QuizIQHub is one of your best choices.
                    </p>
                    <form className="my-8" onSubmit={handleSubmit(signUser)} >
                        <LabelInputContainer className="mb-4">
                            <Label htmlFor="email">Email Address</Label>
                            <Input id="email" placeholder="projectbcoding@bc.com" type="email" {...register("userEmail", {
                                required: true,
                                validate: (value) => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(value) ||
                                    "Email address must be a valid address",
                            })} />
                        </LabelInputContainer>
                        <LabelInputContainer className="mb-4">
                            <Label htmlFor="password">Password</Label>
                            <Input id="password" placeholder="••••••••" type="password" {...register("userPassword", { required: true })} />
                        </LabelInputContainer>

                        <button
                            className="bg-gradient-to-br relative group/btn from-zinc-900 to-zinc-900 bg-zinc-800 w-full text-white rounded-md h-10 font-medium shadow-[0px_1px_0px_0px_var(--zinc-800)_inset,0px_-1px_0px_0px_var(--zinc-800)_inset]"
                            type="submit"
                        >
                            Sign in &rarr;
                            <BottomGradient />
                        </button>

                        <div className="bg-gradient-to-r from-transparent via-neutral-700 to-transparent my-8 h-[1px] w-full" />
                        <div className="flex flex-col space-y-4">
                            <p className="text-sm max-w-sm mt-2 text-center text-neutral-300">
                                Don't have an account?
                            </p>
                            <Link href={"/register"}>
                                <button
                                    className="bg-gradient-to-br relative group/btn from-zinc-900 to-zinc-900 bg-zinc-800 w-full text-white rounded-md h-10 font-medium shadow-[0px_1px_0px_0px_var(--zinc-800)_inset,0px_-1px_0px_0px_var(--zinc-800)_inset]"
                                    type="submit"
                                >
                                    Sign up &rarr;
                                    <BottomGradient />
                                </button>
                            </Link>
                        </div>
                    </form>
                </div>
            </div>
        </main>
    );
}

const BottomGradient = () => {
    return (
        <>
            <span className="group-hover/btn:opacity-100 block transition duration-500 opacity-0 absolute h-px w-full -bottom-px inset-x-0 bg-gradient-to-r from-transparent via-cyan-500 to-transparent" />
            <span className="group-hover/btn:opacity-100 blur-sm block transition duration-500 opacity-0 absolute h-px w-1/2 mx-auto -bottom-px inset-x-10 bg-gradient-to-r from-transparent via-indigo-500 to-transparent" />
        </>
    );
};

const LabelInputContainer = ({
    children,
    className,
}: {
    children: React.ReactNode;
    className?: string;
}) => {
    return (
        <div className={cn("flex flex-col space-y-2 w-full", className)}>
            {children}
        </div>
    );
};
