import axios from "axios";
import { backendAddress } from "@/config";
import type { UserCreate, EmailUserLogin, PasswordUserLogin } from "@/services/schemas/auth";


const ACCESS_STORAGE_KEY = "accessToken";
const ACCESS_HEADER_KEY = "authorization";

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
    withCredentials: true,
    ...userLogin
  })
  .then((res) => {
    localStorage.setItem(ACCESS_STORAGE_KEY, res.headers[ACCESS_HEADER_KEY]);
  })
}


async function refreshToken(){
  return axios.get("/auth/token", {withCredentials: true});
}

async function authorizedRequest({method, url, data}: {method: string, url: string, data?: any | null}){
  const requestData = {method: method, url: url, ...(data !== null && data !== undefined ? { data } : {})};
  const accessToken = localStorage.getItem(ACCESS_STORAGE_KEY);
  return axios({
    headers: {
      ACCESS_HEADER_KEY: accessToken
    },
    ...requestData
  }).catch(err => {
    if (err.response && err.response.status == 401){
      refreshToken().then(res => {
        const newAccess = res.headers[ACCESS_HEADER_KEY]
        localStorage.setItem(ACCESS_STORAGE_KEY, newAccess);
        
        return axios({
          headers: {ACCESS_HEADER_KEY: newAccess},
          ...requestData
        })
      })
    }
    throw err;
  })
}

export async function getDecks(){
  return authorizedRequest({method: "get", url: backendAddress + "/deck/"})
}
