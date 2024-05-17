"use client";
import React, { useState } from "react";
import { Label } from "@/components/ui/Label";
import { Input } from "@/components/ui/Input";
import { cn } from "@/lib/utils";
import { SubmitHandler, useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import { cookie_setter } from "@/lib/cookie";

interface AdminForm {
    adminEmail: string,
    adminPassword: string,
}

export default function Adminlogin() {
    const router = useRouter();
    const [error, setError] = useState();
    const { register, handleSubmit } = useForm<AdminForm>()
    const signUser: SubmitHandler<AdminForm> = async (data: AdminForm) => {
        // "use server"
        console.log(data);

        const response = await fetch("http://localhost:8000/api/adminLogin",
            {
                method: 'POST',
                headers: {
                    "content-type": "application/json"
                },
                body: JSON.stringify({
                    "admin_email": data.adminEmail,
                    "admin_password": data.adminPassword
                })
            }
        );
        const res_data = await response.json();
        if (!response.ok) {
            console.log("hello");
            setError(res_data.message);
        } else {
            const { admin_token, admin_token_id, expiry_time } = res_data;
            // console.log("Token", adminToken);
            // console.log("Response", response);
            console.log("Data form login function", admin_token);
            console.log("Data form login function", admin_token_id);

            localStorage.setItem("admin_token_id", admin_token_id)

            cookie_setter("admin_token", admin_token, expiry_time, {
                secure: true,
                sameSite: "strict"
            });
            router.push("/admin")
        };
    };
    return (
        <main className="bg-gradient-to-b from-[#083755] via-black to-black lg:bg-gradient-to-bl lg:from-[#042c44] lg:via-black lg:to-black h-screen flex items-center justify-center">
            <div className="flex justify-center items-stretch w-11/12 md:rounded-2xl  ">
                {/* <div className="w-3/4 rounded-l-2xl lg:bg-gradient-to-br from-black from-10% via-[#083755] to-black to-85% justify-center lg:flex hidden">
                    <Image src={logo} alt="QuizIQHUB" className="object-cover" />
                </div> */}
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
                            <Input id="email" placeholder="adminbcoding@bc.com" type="email" {...register("adminEmail", {
                                required: true,
                                validate: (value) => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(value) ||
                                    "Email address must be a valid address",
                            })} />
                        </LabelInputContainer>
                        <LabelInputContainer className="mb-4">
                            <Label htmlFor="password">Password</Label>
                            <Input id="password" placeholder="••••••••" type="password" {...register("adminPassword", { required: true })} />
                        </LabelInputContainer>

                        <button
                            className="bg-gradient-to-br relative group/btn from-zinc-900 to-zinc-900 bg-zinc-800 w-full text-white rounded-md h-10 font-medium shadow-[0px_1px_0px_0px_var(--zinc-800)_inset,0px_-1px_0px_0px_var(--zinc-800)_inset]"
                            type="submit"
                        >
                            Verify admin &rarr;
                            <BottomGradient />
                        </button>
                        <div className="bg-gradient-to-r from-transparent via-neutral-700 to-transparent my-8 h-[1px] w-full" />
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
