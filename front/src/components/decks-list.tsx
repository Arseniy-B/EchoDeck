import { Card, CardTitle, CardHeader } from "@/components/ui/card";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import {getDecks} from "@/services/api/deck";
import {type Deck} from "@/services/schemas/deck";
import React from "react";


function DecksList(){
  const [decks, setDecks] = React.useState<Deck[]>([]);


  React.useEffect(() => {
    getDecks().then((res) => {
      console.log(res.data);
      setDecks(res.data);
    })
  }, [])
  
  return (
    <div className="p-[15%] grid grid-cols-[repeat(auto-fit,minmax(300px,1fr))] gap-6">
      {decks.map(deck => 
        <Card className="dark:hover:bg-input/50 hover:text-accent-foreground">
          <CardHeader><CardTitle>{deck.title}</CardTitle></CardHeader>
        </Card>
      )}
    </div>
  )
}

export default DecksList;
