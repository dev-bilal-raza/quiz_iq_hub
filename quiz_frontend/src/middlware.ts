import { NextRequest, NextResponse } from "next/server";

export const middleware = async (req: NextRequest) => {

    const cookies = req.cookies.get("refresh_token")?.value ? req.cookies.get("refresh_token")?.value : req.cookies.get("access_token")?.value ? req.cookies.get("refresh_token")?.value : null;

    const url = req.url;

    if ((url.startsWith("/login") && cookies) || url.startsWith("/register")) {

    }

}