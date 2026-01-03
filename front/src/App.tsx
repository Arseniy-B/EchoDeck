import { BrowserRouter, Routes, Route } from "react-router-dom";
import Auth from "./pages/auth";
import Home from "./pages/home";
import DeckMenu from "./pages/decks";
import ThemeProvider from "@/components/theme-provider";


function App() {
  return (
      <ThemeProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/home/*" element={<Home />} />
            <Route path="/auth/*" element={<Auth/>} />
            <Route path="/*" element={<DeckMenu />} />
          </Routes>
        </BrowserRouter>
      </ThemeProvider>
  )
}

export default App
