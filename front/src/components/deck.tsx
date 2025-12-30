import {useParams} from "react-router-dom";

function Deck(){
  const {deckId} = useParams<{deckId: string}>();
  return (
    <>Deck id</>
  )
};

export default Deck
