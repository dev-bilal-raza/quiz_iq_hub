import { Options } from "../types/quizType"
import { getCookie, setCookie, deleteCookie } from "cookies-next"

export const cookie_getter = (cookie_key: string) => {
    const cookie = getCookie(cookie_key)
    return cookie
}

export const cookie_setter = (cookie_key: string, cookie_value: string, expires_in: number, options?: Options) => {
    const expirationTime = new Date();
    expirationTime.setSeconds(expirationTime.getSeconds() + expires_in)
    setCookie(cookie_key, cookie_value, {
        expires: expirationTime,
        ...options
    })
    return "Cookie has been added successfully"
}

export const cookie_deleter = (cookie_key: string) => {
    deleteCookie(cookie_key)
    return "Cookie has been removed successfully"
}