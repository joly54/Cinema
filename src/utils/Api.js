import {baseurl} from "../components/Profile";

export const login = (username, password) => {
    return fetch(`${baseurl}/login?username=${username}&password=${password}`, {method: 'POST'})
}
export const checkToken = (username, token) => {
    return fetch(`${baseurl}/checkToken?username=${username}&token=${token}`)
}
export const userInfo = (username, token) => {
    return fetch(`${baseurl}/userinfo?username=${username}&token=${token}`)
}

export const register = (username, password) => {
    return fetch(`${baseurl}/register?username=${username}&password=${password}`, {method: 'POST'})
}

export const forgotPassword = (username) => {
    return fetch(`${baseurl}/forgot-password?username=${username}`, {method: 'POST'})
}
export const schedule = () => {
    return fetch(`${baseurl}/schedule`)
}
export const checktoken = (username, token) => {
    return fetch(`${baseurl}/checkToken?username=${username}&token=${token}`)
}