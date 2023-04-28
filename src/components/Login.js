import React, { useState } from 'react';
import './login.css';
import {baseurl} from './Profile';
import { useNavigate } from 'react-router-dom';

function Login() {
    useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    function hendleLogin() {
        const options = {method: 'POST'};
        fetch(`${baseurl}login?username=${username}&password=${password}`, options)
            .then(response => {
                if (response.status === 200) {
                    response.json().then(data => {
                            localStorage.setItem('token', data.token);
                            localStorage.setItem('validDue', data.validDue);
                            document.location.href = '/profile';
                        }
                    )
                } else {
                    alert("Wrong username or password")
                }
            })
            .catch(err => console.error(err));
    }

    return (
        <div className="container">
            <h1 className="title">Login</h1>
            <div className="form">
                <div className="form-group">
                    <label htmlFor="username">Username</label>
                    <input
                        type="text"
                        id="username"
                        placeholder="Enter username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password</label>
                    <input
                        type="password"
                        id="password"
                        placeholder="Enter password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <button className="btn" onClick={hendleLogin}>Log in</button>
            </div>
        </div>
    );
    }

export default Login;
