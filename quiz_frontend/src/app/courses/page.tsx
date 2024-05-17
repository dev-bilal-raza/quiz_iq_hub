import React from 'react'
import { Courses } from '@/components/layout/Courses'
import Header from '@/components/layout/Header'

const page = () => {
    return (
        <main>
            <div>
                <Header />
            </div>
            <section>
                <Courses />
            </section>

        </main>
    )
}

export default page