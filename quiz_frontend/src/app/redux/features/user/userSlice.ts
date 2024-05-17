import { createSlice } from "@reduxjs/toolkit";
import { fetchUser } from "./userApi";

interface UserInterface {
    payload:{
        user_name: string
        user_email: string
    },
    type: string
}

const initialState = {
    status: false,
    user: {
        user_email: "",
        total_points: 0,
        user_id: 0,
        user_name: "",
    },
    isLoading: true,
    isError: ""
};

const userSlice = createSlice(
    {
        name: "user",
        initialState,
        reducers: {
            updateUserFn: (state, action: UserInterface) => {
                state.user.user_name = action.payload.user_name
                state.user.user_email = action.payload.user_email;
            },
            logout: (state) => {
                state.user = {
                    user_email: "",
                    total_points: 0,
                    user_id: 0,
                    user_name: "",
                },
                    state.status = false;
                state.isLoading = false;
            }
        },
        extraReducers: (builder) => {

            builder.addCase(fetchUser.pending, (state) => {
                state.isLoading = true
            })
            builder.addCase(fetchUser.fulfilled, (state, action) => {
                state.user = action.payload;
                state.status = true;
                state.isLoading = false;
            });
            builder.addCase(fetchUser.rejected, (state, action: any) => {
                state.user = {
                    user_email: "",
                    total_points: 0,
                    user_id: 0,
                    user_name: "",
                };
                state.status = false;
                state.isLoading = false;
                state.isError = action.message;
                console.log(action.payload);
            });
        }
    }
);

export const { logout, updateUserFn } = userSlice.actions;
export default userSlice.reducer;