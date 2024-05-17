import React from 'react'

const Button = ({ children, ButtonType, isDeleted, classnames, onClick }: {
    children: React.ReactNode,
    ButtonType: "submit" | "reset" | "button",
    isDeleted: boolean,
    classnames?: any,
    onClick?: () => void
}) => {
    return (
        <button className={` ${!isDeleted ? "bg-gradient-to-tr from-sky-900 hover:from-sky-800 via-blue-900 hover:via-blue-800 to-violet-500 hover:to-violet-400" : " bg-red-500   hover:bg-red-400"} p-2 px-5 rounded-md transition ease-in-out duration-300 hover:-translate-y-1 hover:scale-110 text-white  ${classnames}`} type={ButtonType} onClick={onClick}>
            {children}
        </button>
    )
}

export default Button