export const baseurl = "https://vincinemaApi.pythonanywhere.com";

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
export const schedule = () => {
    return fetch(`${baseurl}/schedule`)
}
export const checktoken = (username, token) => {
    return fetch(`${baseurl}/checkToken?username=${username}&token=${token}`)
}
export const getSessionInfo = (ses_id) => {
    return fetch(`${baseurl}/getSession?ses_id=${ses_id}`)
}
export const buyTicket = (ses, username, token, seats) => {
    return fetch(`${baseurl}/buyTikets?sessions_id=${ses}`, {method: 'POST', headers: {
        username: username,
        token: token,
        seats: "[" + seats + "]"
        }})
}

export const getFilms = () => {
    return fetch(`${baseurl}/getFilms`)
}

export const forgotPasswordConfirm = (username) => {
    return fetch(`${baseurl}/forgot-password?username=${username}`, {method: 'POST'})
}