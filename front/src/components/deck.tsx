import {useParams} from "react-router-dom";
import { Card } from "@/components/ui/card";


function Deck(){
  const {deckId} = useParams<{deckId: string}>();
  return (
    <>
      deck
    </>
  )
};

export default Deck
