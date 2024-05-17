import React from 'react'

const Container = ({children}: {children: React.ReactNode}) => {
  return (
    <div className='w-6xl mx-auto'>
        {children}
    </div>
  )
}

export default Container