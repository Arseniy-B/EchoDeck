import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"

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
import type { UserCreate } from "@/services/schemas/auth"
import { sendUserData } from "@/services/api/auth"
import { toast } from "sonner"
import { Toaster } from "@/components/ui/sonner"


const LoginSchema = z.object({
  email: z.email(),
  password: z.string().min(3).max(50)
})


export default function SignUp(){
  const form = useForm<z.infer<typeof LoginSchema>>({
    resolver: zodResolver(LoginSchema),
    defaultValues: {
      email: "",
      password: "",
    }
  })

  async function onSubmit(values: z.infer<typeof LoginSchema>) {
    const user: UserCreate = {email: values.email, password: values.password};
    toast.promise(() => sendUserData({user}), {
      loading: "sending an email notification",
      success: "OTP has been sent to your email.",
      error: "Error, OTP was not sent"
    })
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
        </form>
      </Form>
    </div>
  )}
