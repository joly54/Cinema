import {baseurl} from "../components/Profile";

export const login = (username, password) => {
    return fetch(`${baseurl}login?username=${username}&password=${password}`, {method: 'POST'})
}
export const checkToken = (username, token) => {
    return fetch(`${baseurl}checkToken?username=${username}&token=${token}`)
}
export const userInfo = (username, token) => {
    return fetch(`${baseurl}userinfo?username=${username}&token=${token}`)
}