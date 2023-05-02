import React from 'react';
import {ToastContainer} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './login.css'

function Register(
    {
        handleChangeUsername,
        handleChangePassword,
        handleRegister
    }
) {
    return(
        <div className="container">
            <h1 className="title">Register</h1>
            <div className="form">
                <div className="form-group">
                    <label htmlFor="username">Username</label>
                    <input
                        type="text"
                        id="username"
                        placeholder="Enter username"
                        onChange={(e) => handleChangeUsername(e.target.value)}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password</label>
                    <input
                        type="password"
                        id="password"
                        placeholder="Enter password"
                        onChange={(e) => handleChangePassword(e.target.value)}
                    />
                </div>
                <button className="btn" onClick={handleRegister}>Register</button>
            </div>
        </div>
    )
}

export default Register;