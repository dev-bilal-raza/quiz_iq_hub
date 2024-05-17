import { createAsyncThunk } from "@reduxjs/toolkit";
import { getCookie } from "cookies-next";

export const fetchUser = createAsyncThunk("fetchUser", async () => {

    const token = getCookie("access_token");
    const response = await fetch("http://localhost:8000/api/getUser", {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    return response.json();

});