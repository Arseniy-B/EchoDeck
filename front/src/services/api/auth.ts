import axios from "axios";
import { backendAddress } from "@/config";
import type { UserCreate, EmailUserLogin, PasswordUserLogin } from "@/services/schemas/auth";


export async function sendUserData({user}: { user:UserCreate }){
  return axios.post(backendAddress + "/auth/sign_up/send_data", {
    ...user
  })
}

export async function confirmRegisterEmail({userLogin}: {userLogin: EmailUserLogin}){
  return axios.post(backendAddress + "/auth/sign_up/confirm_email", {
    ...userLogin
  })
}

export async function loginByPassword({userLogin}: {userLogin: PasswordUserLogin}){
  return axios.post(backendAddress + "/auth/sign_in/password", {
    ...userLogin
  })
}
