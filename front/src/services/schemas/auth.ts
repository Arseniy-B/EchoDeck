export type UserCreate = {
  email: string
  password: string
}

export type EmailUserLogin = {
  email: string
  otp: string
}

export type PasswordUserLogin = {
  email: string
  password: string
}
