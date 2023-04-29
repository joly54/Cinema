import {baseurl} from "../components/Profile";
import {toast} from "react-toastify";

export const login = (username, password) => {
    return fetch(`${baseurl}login?username=${username}&password=${password}`, {method: 'POST'})
}