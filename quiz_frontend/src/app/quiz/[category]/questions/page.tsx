import Header from '@/components/layout/Header'
import QuestionPage from '@/components/pages/QuestionPage';

const page = ({ params }: { params: { category: string } }) => {
    console.log(params.category);
    let category = params.category;

    // for (const str of params.category) {
    //     console.log(str);

    //     if (str == "%" || str == "2" || str == "0") {
    //         console.log("hello");

    //         category += "  "
    //     } else {
    //         category += str
    //     }
    // }
    // const titlecategory = category.charAt(0).toUpperCase() + category.slice(1);

    return (
        // header
        <main className='h-screen'>
            <Header />
            <QuestionPage category={category} />
        </main>
    )
}

export default page