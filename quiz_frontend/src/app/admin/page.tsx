"use client"
import React, { useState, useEffect, FormEvent } from 'react'
import { Category } from '@/types/quizType'
import { cookie_deleter, cookie_getter } from "@/lib/cookie";
import SetQuestion from './adminComponents/SetQuestion';
import { verifyAdmin, getCategories, deleteTokenFromDB, addCategory } from './adminComponents/adminApiActions';
import { useRouter } from 'next/navigation';
import Loader from '@/components/layout/Loader';

const AdminPage = () => {
    const router = useRouter();
    const [categories, setCategories] = useState<Category[]>([]);
    const [loading, setLoading] = useState(true);
    const [categoryInput, setCategoryInput] = useState<string>("");
    const [categoryMarks, setCategoryMarks] = useState<number>(50);
    const [categoryDetails, setCategoryDetails] = useState<string>("");
    const [error, setError] = useState<string>();
    const [resMessage, setResMessage] = useState<string>();
    const adminToken = cookie_getter("admin_token");
    const admin_token_id = localStorage.getItem("admin_token_id");

    useEffect(() => {
        const admin_verification = async () => {
            // "use server"
            if (adminToken && admin_token_id) {
                const response = await verifyAdmin(adminToken);
                if (!response.ok) {
                    router.push("/admin/adminLogin");
                };
                const categories = await getCategories();
                if (categories) setCategories(categories);
                setLoading(false);

            } else if (admin_token_id) {
                await deleteTokenFromDB(Number(admin_token_id));
                router.push("/admin/adminLogin");
            } else {
                router.push("/admin/adminLogin");
            };
        };
        admin_verification();
    }, []);

    const setCategory = async (f: FormEvent) => {
        f.preventDefault();
        if (adminToken) {
            const response = await addCategory(categoryInput, categoryDetails, categoryMarks, adminToken);
            const categories = await response.json();
            if (!response.ok) {
                setResMessage("");
                setError(categories.message);
            } else {
                setCategories(categories);
                setResMessage("Category added successfully!");
                setCategoryInput("");
                setCategoryDetails("");
                setError("");
            };
        };
    };

    if (loading) return <div className='h-screen flex justify-center items-center'>
        <Loader/>
        </div>
    return (
        <main>
            <div className='w-full h-44 flex justify-center items-center'>
                <h2 className='text-center text-4xl md:text-6xl font-heading font-bold bg-gradient-to-r from-white via-slate-100 to-slate-400 bg-clip-text text-transparent'>Welcome to Dashboard</h2>
            </div>
            <section className='m-6 mb-16 p-4 rounded-md  bg-gradient-to-b from-slate-800 via-slate-400 to-slate-300'>
                <h1 className='text-center text-3xl md:text-4xl text-white font-heading font-bold'>
                    Add Category
                </h1>
                <div>
                    <form onSubmit={setCategory} className=''>
                        <label htmlFor="category" className="block mb-2 mt-3 font-heading text-xl text-slate-200">Category</label>
                        <input className='rounded-lg ms-2 px-3 py-2' required={true} minLength={2} maxLength={30} type="text" placeholder='Python' value={categoryInput} onChange={(input) => setCategoryInput(input.target.value)
                        } />
                        <label htmlFor="categoryMarks" className="block mb-2 mt-3 font-heading text-xl text-slate-200">Category Marks</label>
                        <input className='rounded-lg ms-2 px-3 py-2' required={true} minLength={2} maxLength={30} type="text" placeholder='Python' value={categoryMarks} onChange={(input) => setCategoryMarks(Number(input.target.value))
                        } />
                        <label htmlFor="categoryDetails" className="block mb-2 mt-3 font-heading text-xl text-slate-200">Category Description</label>
                        <textarea id="categoryDetails" value={categoryDetails} rows={4} className="block ms-2 p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 max-h-36" placeholder="Write your thoughts here..." onChange={(event) => setCategoryDetails(event.target.value)}></textarea>

                        <button className='rounded-lg m-2 p-2 bg-slate-900 hover:bg-slate-800 text-white shrink-0' type='submit'>Add Category</button>
                    </form>
                    <p className='text-lg m-2 font-bold text-red-800'>{error ? error : ""}</p>
                    <p className='text-xl m-2 text-[#009A00] font-heading font-medium'>{resMessage ? resMessage : ""}</p>
                </div>
            </section>
            <div className='h-0.5 bg-gradient-to-r from-[#000000] via-gray-600 to-[#000000'/>
            <section className="mt-16">
                <SetQuestion categories={categories} />
            </section>
        </main>
    );
};

export default AdminPage;