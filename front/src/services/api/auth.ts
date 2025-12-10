import axios from "axios";
import { backendAddress } from "@/config";
import type { UserCreate } from "@/services/schemas/auth";


export async function sendUserData({user}: { user:UserCreate }){
  return axios.post(backendAddress + "/auth/sign_up/send_data", {
    email: user.email,
    password: user.password,
  })
}

