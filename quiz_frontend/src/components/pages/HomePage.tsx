import React from 'react'
import Header from '../layout/Header'
import { HeroSection } from '../layout/HeroSection'
import { Teachers } from '../layout/Teachers'
import CurlyBackground from '../ui/CurlyBackground'
import { Courses } from '../layout/Courses'
import Footer from '../layout/Footer'

const HomePage = () => {
    return (
        <div>
            <Header />
            <HeroSection />
            <div className="z-30 relative bg-gradient-to-r from-slate-50 to-gray-400">
                <Teachers />
                <CurlyBackground />
            </div>
            <Courses />
            {/* <footer>
                <Footer />
            </footer> */}
        </div>
    )
}

export default HomePage