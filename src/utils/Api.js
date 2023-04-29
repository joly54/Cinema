import {baseurl} from "../components/Profile";
import {toast} from "react-toastify";

export const login = (username, password) => {
    fetch(`${baseurl}login?username=${username}&password=${password}`, {method: 'POST'})
        .then(response => {
            if (response.status === 200) {
                response.json().then(data => {
                        localStorage.setItem('token', data['token']);
                        localStorage.setItem('validDue', data['validDue']);
                        localStorage.setItem('username', username);
                        return response;
                    }
                )
            } else {
                toast.error("Wrong username or password");
            }
        })
        .catch(err => console.error(err));
    //wait response
    return new Promise(resolve => {
        setTimeout(() => {
            resolve();
        }, 0);
    });
}