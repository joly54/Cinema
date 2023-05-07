import React from 'react';
import './Styles/login.css';
import './Styles/scrollBar.css';
function ForgotPassword(
    {
        ResetPassword,
        handleChangeUsername
    }
){
    return(
        <div className="container">
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
                <button className="btn" onClick={ResetPassword}>Reset password</button>
            </div>
        </div>
    )
}

export default ForgotPassword;