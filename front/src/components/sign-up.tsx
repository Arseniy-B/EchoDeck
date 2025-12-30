import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import React from "react"

import { Separator } from "@/components/ui/separator"
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form"
import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
} from "@/components/ui/input-group"
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import { HelpCircle, InfoIcon } from "lucide-react"
import type { UserCreate, PasswordUserLogin } from "@/services/schemas/auth"
import { sendUserData, confirmRegisterEmail, loginByPassword } from "@/services/api/auth"
import { toast } from "sonner"
import { Toaster } from "@/components/ui/sonner"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import {
  InputOTP,
  InputOTPGroup,
  InputOTPSeparator,
  InputOTPSlot,
} from "@/components/ui/input-otp"
import { useNavigate } from 'react-router-dom';


const LoginSchema = z.object({
  email: z.email(),
  password: z.string().min(3).max(50)
})


export default function SignUp(){
  const navigate = useNavigate();
  const [open, setOpen] = React.useState(false);
  const [userCreate, setUserCreate] = React.useState<UserCreate>({email: "", password: ""});
  const [otpValue, setOtpValue] = React.useState('');
  const [isOtpError, setOtpError] = React.useState<boolean>(false);

  const form = useForm<z.infer<typeof LoginSchema>>({
    resolver: zodResolver(LoginSchema),
    defaultValues: {
      email: "",
      password: "",
    }
  })

  React.useEffect(() => {
    if (otpValue.length == 6){
      const confirmEmail = {email: userCreate.email, otp: otpValue}
      confirmRegisterEmail({userLogin: confirmEmail})
      .then(() => {
        const userLogin = {email: userCreate.email, password: userCreate.password}
        loginByPassword({userLogin: userLogin}) 
        .then(() => {
          navigate("/")
        })
      })
      .catch(err => {
        setOtpError(true);
        if (err.response){
          console.log(err.response.status);
        }
      })
    }
  }, [otpValue])

  async function onSubmit(values: z.infer<typeof LoginSchema>) {
    const user: UserCreate = {email: values.email, password: values.password};
    setUserCreate(user);
    toast.promise(() => sendUserData({user}), {
      loading: "sending an email notification",
      success: "OTP has been sent to your email.",
      error: "Error, OTP was not sent"
    })
    setUserCreate(user);
    setOpen(true);
  }

  return (
    <div className="max-w-[500px]">
      <Toaster position="top-right" />
      <h1 className="scroll-m-20 text-center text-4xl font-extrabold tracking-tight text-balance">
        Create your account
      </h1> 
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormControl>
                  <InputGroup>
                    <InputGroupInput placeholder="Your email address" {...field}/>
                    <InputGroupAddon align="inline-end">
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <InputGroupButton
                            variant="ghost"
                            aria-label="Help"
                            size="icon-xs"
                          >
                            <HelpCircle />
                          </InputGroupButton>
                        </TooltipTrigger>
                        <TooltipContent>
                          <p>We&apos;ll use this to send you notifications</p>
                        </TooltipContent>
                      </Tooltip>
                    </InputGroupAddon>
                  </InputGroup>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="password"
            render={({ field }) => (
              <FormItem>
                <FormControl>
                  <InputGroup>
                    <InputGroupInput placeholder="Enter password" type="password" {...field}/>
                    <InputGroupAddon align="inline-end">
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <InputGroupButton
                            variant="ghost"
                            aria-label="Info"
                            size="icon-xs"
                          >
                            <InfoIcon />
                          </InputGroupButton>
                        </TooltipTrigger>
                        <TooltipContent>
                          <p>Password must be at least 8 characters</p>
                        </TooltipContent>
                      </Tooltip>
                    </InputGroupAddon>
                  </InputGroup>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <Separator/>
          <Button type="submit">Submit</Button>
          <Dialog open={open} onOpenChange={setOpen}>
            <DialogContent className="sm:max-w-md">
              <div className="flex flex-col items-center space-y-6 py-4">
                <DialogHeader>
                  <DialogTitle>Enter the confirmation code</DialogTitle>
                </DialogHeader>
                <Separator/>
                <InputOTP 
                  maxLength={6}
                  value={otpValue}
                  onChange={(value) => setOtpValue(value)}
                >
                  <InputOTPGroup>
                    <InputOTPSlot index={0} className={isOtpError ? "border-red-500 ring-red-500" : ""}/>
                    <InputOTPSlot index={1} className={isOtpError ? "border-red-500 ring-red-500" : ""}/>
                    <InputOTPSlot index={2} className={isOtpError ? "border-red-500 ring-red-500" : ""}/>
                  </InputOTPGroup>
                  <InputOTPSeparator />
                  <InputOTPGroup>
                    <InputOTPSlot index={3} className={isOtpError ? "border-red-500 ring-red-500" : ""}/>
                    <InputOTPSlot index={4} className={isOtpError ? "border-red-500 ring-red-500" : ""}/>
                    <InputOTPSlot index={5} className={isOtpError ? "border-red-500 ring-red-500" : ""}/>
                  </InputOTPGroup>
                </InputOTP>         
              </div>
            </DialogContent>
          </Dialog>
        </form>
      </Form>
    </div>
  )}
