const local = false
export const baseurl = local ? 'http://127.0.0.1:5000/' : "https://vincinemaapi.pythonanywhere.com/"
export const login = (username, password) => {
    const json = JSON.stringify({username: username, password: password})
    return fetch(`${baseurl}/login`, {
            credentials: 'include',
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            },
            body: json
        }
    )
}

export const isAuthenticated = () => {
    return fetch(`${baseurl}/isUserAuthenticated`, {credentials: 'include'})
}

export const logout = () => {
    return fetch(`${baseurl}/logout_us`, {credentials: 'include'})
}


export const register = (username, password) => {
    const json = JSON.stringify({username: username, password: password})
    return fetch(`${baseurl}/register?username=${username}&password=${password}`,
        {
            credentials: 'include',
            method: 'POST',
            body: json})
}
export const forgotPasswordConfirm = (username) => {
    return fetch(`${baseurl}/forgot-password?username=${username}`, {method: 'POST'})
}

export const ResetPassword = (username, code, password) => {
    return fetch(`${baseurl}/reset-password?username=${username}&secret_code=${code}&password=${password}`, {method: 'POST'})
}
export const userInfo = () => {
    return fetch(`${baseurl}/userinfo`,
        {
            credentials: 'include',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            },
        }
    )
}

export const get_history = () => {
    return fetch(`${baseurl}/history`, {credentials: 'include'})
}
export const get_navbar = () => {
    return fetch(`${baseurl}/getnav`, {credentials: 'include'})
}

export const schedule = () => {
    return fetch(`${baseurl}/schedule`)
}

export const getSessionInfo = (ses_id) => {
    return fetch(`${baseurl}/getSession?ses_id=${ses_id}`)
}
export const getFilms = () => {
    return fetch(`${baseurl}/getFilms`)
}
export const getSessions = (film_id) => {
    return fetch(`${baseurl}/getSessions?film_id=${film_id}`)
}
export const buyTicket = (ses, seats) => {
    const json = JSON.stringify({seats: seats})
    return fetch(`${baseurl}/buyTikets?sessions_id=${ses}`, {
        credentials: 'include',
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json'
        },
        body: json
    })
}

export const confirmPayment = (payment_id) => {
    return fetch(`${baseurl}/confirmPayment?payment_id=${payment_id}`)
}