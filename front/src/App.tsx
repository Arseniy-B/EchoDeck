import { BrowserRouter, Routes, Route } from "react-router-dom";
import Auth from "./pages/auth";
import Home from "./pages/home";
import ThemeProvider from "@/components/theme-provider";


function App() {
  return (
    <div className="w-[100vw] h-[100vh]">
      <ThemeProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/*" element={<Home />} />
            <Route path="/auth/*" element={<Auth/>} />
          </Routes>
        </BrowserRouter>
      </ThemeProvider>
    </div>
  )
}

export default App
