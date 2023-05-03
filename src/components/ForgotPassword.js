import React from 'react';
import './login.css';

function ForgotPassword(
    {
        handleChangeUsername
    }
){
    return(
        <div>
            <h1 className="title">Forgot Password</h1>
            <div className="form">
                <div className="form-group">
                    <label htmlFor="username">Username</label>
                    <input
                        type="text"
                        id="username"
                        placeholder="Enter username"
                        onChange={(e) => handleChangeUsername(e.target.value)}
                    />
                    <label htmlFor="code">Code from Email</label>
                    <input
                        type="text"
                        id="code"
                        placeholder="Enter code from email"
                        disabled={true}
                    />
                </div>
                <button className="btn" onClick={''}>Reset password</button>
            </div>
        </div>
    )
}

export default ForgotPassword;