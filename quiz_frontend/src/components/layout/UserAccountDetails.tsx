"use client"
import React, { useState } from 'react'
import { useAppDispatch } from '@/app/redux/hooks';
import { cookie_getter } from '@/lib/cookie';
import Loader from './Loader';
import { updateUserFn } from '@/app/redux/features/user/userSlice';

const UserAccountDetails = ({ user_id, user_name, user_email }: {
    user_id: number,
    user_name: string,
    user_email: string
}) => {
    const access_token = cookie_getter("access_token");
    const dispatch = useAppDispatch();
    const [name, setName] = useState(user_name);
    const [isLoading, setLoading] = useState(false);
    const [email, setEmail] = useState(user_email);
    const [nameDisabled, setNamedisabled] = useState(true);
    const [emailDisabled, setEmaildisabled] = useState(true);

    const updateUser = async () => {
        setLoading(true);
        console.log(access_token);
        const response = await fetch("/api/update_user", {
            method: "POST",
            headers: {
                "Authorization": "Bearer " + access_token,
                "content-type": "application/json"
            },
            body: JSON.stringify({
                "user_id": user_id,
                "user_name": name,
                "user_email": email,
            })
        })
        console.log(await response.json());
        dispatch(updateUserFn({
            user_email: email,
            user_name: name
        }));
        setLoading(false)
    }
    return (
        <div>
            {
                isLoading ?
                    <div className='m-2'>
                        <Loader />
                    </div>
                    :
                    <div className='flex flex-col gap-5 m-5'>
                        <div className='border-2 border-gray-300 rounded-md p-3'>
                            <div className='flex justify-end'>
                                <button onClick={() => { setNamedisabled(!nameDisabled) }}>✏️</button>
                            </div>
                            <div className='m-1.5 flex flex-col gap-2'>
                                <input value={name} disabled={nameDisabled} type="text" className={`'font-para ${nameDisabled ? "cursor-not-allowed bg-transparent" : "p-1.5 rounded-lg"} w-full '`}
                                    onChange={(e) => setName(e.target.value)} />
                                {!nameDisabled ? <button className='p-2 px-4 bg-gradient-to-tr from-sky-500 to-gray-900 text-white font-para rounded-lg ' onClick={() => {
                                    updateUser()
                                    setNamedisabled(!nameDisabled)
                                }}>
                                    Save
                                </button> : ""}
                            </div>
                        </div>
                        <div className='border-2 border-gray-300 rounded-md p-3'>
                            <div className='flex justify-end'>
                                <button onClick={() => {
                                    setEmaildisabled(!emailDisabled)
                                }}>✏️</button>
                            </div>
                            <div className='m-1.5 flex flex-col gap-2'>
                                <input value={email} disabled={emailDisabled} type="text" className={`'m-1.5 font-para ${emailDisabled ? "cursor-not-allowed bg-transparent" : "p-1.5 rounded-lg"} w-full '`} onChange={(e) => setEmail(e.target.value)} />
                                {!emailDisabled ? <button className='p-2 px-4 bg-gradient-to-tr from-sky-500 to-gray-900 text-white font-para rounded-lg ' onClick={() => {
                                    updateUser();
                                    setEmaildisabled(!emailDisabled)
                                }}>
                                    Save
                                </button> : ""}
                            </div>
                        </div>
                    </div>
            }
        </div>
    )
}

export default UserAccountDetails