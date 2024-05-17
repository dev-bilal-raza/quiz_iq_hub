import React from 'react'

const Avatar = ({ user_name, width, height, fillMode }:
    {
        user_name: string, width: number, height: number, fillMode: string
    }) => {
    return (
        <div>
            <div className='flex justify-center items-center m-5'>
                <svg xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink" width={`${width}px`} height={`${height}px`} viewBox="0 0 64 64" version="1.1"><circle fill={fillMode} cx="32" width="90" height="90" cy="32" r="32" /><text x="50%" y="50%" style={{ "color": "#222", "lineHeight": 1, "fontFamily": "-apple-system, BlinkMacSystemFont" }} alignmentBaseline="middle" textAnchor="middle" fontSize="28" fontWeight="400" dy=".1em" dominantBaseline="middle" fill="#222">{user_name.split(" ").map((name: string) => name.charAt(0).toUpperCase())}</text>
                </svg>
            </div>
        </div>
    )
}

export default Avatar