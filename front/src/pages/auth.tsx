import { Separator } from "@/components/ui/separator";
import { Routes, Route } from "react-router-dom";
import SignIn from "../components/sign-in";
import SignUp from "../components/sign-up";
import { Card } from "@/components/ui/card";


export default function Auth(){
  return (
    <>
      <Separator className="absolute ml-[10vw]" orientation="vertical"/>
      <Separator className="absolute right-0 mr-[10vw]" orientation="vertical"/>
      <div className="h-[100vh] content-center">
        <Separator />
        <div className="px-[10vw] m-auto">
          <Card className="m-5 p-[10%] bg-gradient-to-r from-card">
            <Routes>
              <Route path="/sign_in" element={<SignIn/>}/>
              <Route path="/sign_up" element={<SignUp/>}/>
            </Routes>
          </Card>
        </div>
        <Separator />
      </div>
    </>
  )
}

