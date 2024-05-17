"use client"
import React, { useEffect, useState} from 'react'
import { usePathname } from 'next/navigation'
import { useRouter } from 'next/navigation'
import { cookie_getter, cookie_setter } from '@/lib/cookie'
import { useAppDispatch, useAppSelector } from '@/app/redux/hooks'
import { fetchUser } from '@/app/redux/features/user/userApi'
import { logout } from '@/app/redux/features/user/userSlice'
import Loader from '@/components/layout/Loader'

const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const dispatch = useAppDispatch();
    const isLoading = useAppSelector(state => state.user.isLoading);
    // const [isLoading, setIsLoading] = useState(true);
    // dispatch(fetchUser())
    const pathName = usePathname();
    const router = useRouter();
    const access_token = cookie_getter("access_token");
    const refresh_token = cookie_getter("refresh_token");

    useEffect(() => {
        const verifyUser = async () => {
            if (access_token && refresh_token) {
                console.log(access_token);
                // TODO: dispatch login func from redux 
                dispatch(fetchUser());
                // setIsLoading(false)
                
            } else if (refresh_token) {
                const response = await fetch("/api/getToken", {
                    headers: {
                        "Authorization": "Bearer " + refresh_token
                    }
                });
                if (!response.ok) {
                    dispatch(logout());
                    // setIsLoading(false)
                };
                const { access_token, expires_in } = await response.json();
                cookie_setter("access_token", access_token, expires_in, { secure: true });
                dispatch(fetchUser());
                // setIsLoading(false)
            } else {
                dispatch(logout());
                // setIsLoading(false)
                //TODO: logout from backend and redux
            };
        };
        verifyUser();
        console.log("after function called in useEffect");
    }, [])
    // const status = useAppSelector(state => state.user.status);
    // console.log(status, "User status from auth");

    // if ((pathName === "/quiz" && !status) || (pathName === "/accounts" && !status)) {
    //     router.push("/login");
    // } else if ((pathName === "/login" || pathName === "/register") && status) {
    //     router.push("/");
    // };
    return (
        <div>
            {isLoading ?
                <div className='flex justify-center items-center w-full h-screen '>
                    <Loader />
                </div>
                :
                children
            }
        </div>
    )
}
export default AuthProvider