import { configureStore } from "@reduxjs/toolkit";
import userReducer from "./features/user/userSlice"
// import categoryReducer from "./features/quizCategory/quizCategorySlice"

export const store = configureStore(
    {
        reducer: {
            user: userReducer,
            // category: categoryReducer
        }
    }
)

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;