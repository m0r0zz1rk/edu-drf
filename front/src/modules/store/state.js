import {getCookie} from "@/commons/cookie";

const state = {
  cokoToken: getCookie('cokoToken') || '',
  cokoRole: getCookie('cokoRole') || '',
  authStatus: ''
}

export default state
