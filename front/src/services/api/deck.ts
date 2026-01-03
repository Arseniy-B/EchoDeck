import {authorizedRequest} from "@/services/api/auth";
import { backendAddress } from "@/config";


export async function getDecks(){
  return authorizedRequest({method: "get", url: backendAddress + "/deck/"})
}
