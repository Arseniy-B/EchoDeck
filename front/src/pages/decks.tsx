import { Routes, Route } from "react-router-dom";
import DecksList from "@/components/decks-list";
import Deck from "@/components/deck";
import { Separator } from "@/components/ui/separator";

function NotFound(){
  return (
    <>Not found</>
  )
}


function DeckMenu() {
  return (
    <>
      <Separator className="fixed ml-[10vw]" orientation="vertical"/>
      <Separator className="fixed right-0 mr-[10vw]" orientation="vertical"/>
      <div className="pt-10">
        <Separator/>
        <Routes>
          <Route path="/" element={<DecksList />} />
          <Route path="/:deckId" element={<Deck/>} />
          <Route path="*" element={<NotFound/>} />
        </Routes>
      </div>
    </>
  )
}

export default DeckMenu
