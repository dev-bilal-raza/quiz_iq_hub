import React from 'react'

const Circle = ({ userPercentage }: { userPercentage: number }) => {

    const circumference = 50 * 2 * Math.PI;

    return (
        <div>
            <div className='flex justify-start'>
                <div className="flex items-center justify-center overflow-hidden  rounded-full">
                    <svg className="w-32 h-32 transform translate-x-1 translate-y-1" aria-hidden="true">
                        <circle
                            className="text-[#B0CCDD]"
                            strokeWidth="10"
                            stroke="currentColor"
                            fill="transparent"
                            r="50"
                            cx="60"
                            cy="60"
                        />
                        <circle
                            className="text-blue-600"
                            strokeWidth="10"
                            strokeDasharray={circumference}
                            strokeDashoffset={userPercentage ? circumference - userPercentage / 100 * circumference : circumference - 0 / 100 * circumference}
                            strokeLinecap="round"
                            stroke="currentColor"
                            fill="transparent"
                            r="50"
                            cx="60"
                            cy="60" />
                    </svg>
                    <span className="absolute text-2xl text-zinc-300" x-text="`${percent}%`">{userPercentage > 0 ? userPercentage : 0}%</span>
                </div>
            </div>
        </div>
    )
}

export default Circle