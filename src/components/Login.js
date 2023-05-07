import React from 'react';
import './Styles/login.css';
import {useNavigate} from "react-router-dom";

function Login(
    {
        handleChangeUsername,
        handleChangePassword,
        handleLogin,
    }
) {
    const navigate = useNavigate();
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
                <div className="row">
                    <button className="btn" onClick={handleLogin}>Log in</button>
                    <p className="text-btn" onClick={() =>{
                       navigate('/forgot-password')
                    }
                    }>
                        Forgot password?
                    </p>
                </div>
            </div>
        </div>
    );
}

export default Login;
