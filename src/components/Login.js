import React from 'react';
import './login.css';
import {ToastContainer} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function Login(
    {
        handleChangeUsername,
        handleChangePassword,
        handleLogin,
    }
) {

    return (
        <div className="container">
            <ToastContainer />
            <h1 className="title">Login</h1>
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
                <button className="btn" onClick={handleLogin}>Log in</button>
            </div>
        </div>
    );
}

export default Login;
