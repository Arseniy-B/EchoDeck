import { Routes, Route } from "react-router-dom";
import DecksList from "@/components/decks-list";
import Deck from "@/components/deck";


function NotFound(){
  return (
    <>Not found</>
  )
}


function DeckMenu() {
  return (
    <div className="w-[100vw] h-[100vh]">
      <Routes>
        <Route path="/" element={<DecksList />} />
        <Route path="/:deckId" element={<Deck/>} />
        <Route path="*" element={<NotFound/>} />
      </Routes>
    </div>
  )
}

export default DeckMenu
