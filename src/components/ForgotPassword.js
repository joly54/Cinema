import React, {useEffect, useState} from 'react';
import {useNavigate} from "react-router-dom";
import { Button, Grid, Typography } from "@material-ui/core";
import { forgotPasswordConfirm, ResetPassword } from "../utils/Api";
import './Styles/scrollBar.css';
import './Styles/ForgotPassword.css';
import LoadingBar from "./Progress.js";

function ForgotPassword({handleToastErr, handleToastSuc}) {

    const [loading, setLoading] = useState(false);

    useEffect(() => {
        window.scrollTo(0, 0)
    }, [])
    const md5 = require('md5');
    document.title = "Forgot Password";
    const [showConfirmationCode, setShowConfirmationCode] = useState(false);
    const [isUsernameDisabled, setIsUsernameDisabled] = useState(false);
    const [isButtonClicked, setIsButtonClicked] = useState(false);
    const [username, setUsername] = useState('');
    const [code, setCode]=useState('')
    const [password, setPassword]=useState('')
    const navigate = useNavigate();
    const handleSendCode = () => {
        if (username !== '') {
            setLoading(true)
            forgotPasswordConfirm(username)
                .then(response => {
                    setLoading(false)
                    if (response.ok) {
                        handleToastSuc("Please check your email for the code");
                        setShowConfirmationCode(true);
                        setIsUsernameDisabled(true);
                        setIsButtonClicked(true);
                    } else {
                        response.json().then(data => {
                            const errorMessage = data.message || "An error occurred";
                            handleToastErr(errorMessage);
                        });
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    handleToastErr("An error occurred");
                });
        } else {
            handleToastErr("Please enter a username");
        }
    };
    const handleChangeUsername = (value) => {
        setUsername(value);
    };
    const handleGetCode = (valueCode)=>{
        setCode(valueCode);
    };
    const handleGetNewPassword = (valuePass)=>{
        setPassword(valuePass);
    };
    const [confirmPassword, setConfirmPassword] = useState('');
    const handleGetConfirmPassword = (value) => {
        setConfirmPassword(value);
    };
    const handleResetPassword = () => {
        if (password === '') {
            handleToastErr("Please enter a password");
        }if (password !== confirmPassword) {
            handleToastErr("Check that the password is entered correctly")
        }else {
            setLoading(true)
            ResetPassword(username, code, md5(md5(password)))
                .then(response=>{
                    setLoading(false)
                    if(response.ok){
                        handleToastSuc("Password reset");
                        navigate('/login');
                    }else {
                        response.json().then(data => {
                            const errorMessage = data.message || "An error occurred";
                            handleToastErr(errorMessage);
                        });
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    handleToastErr(error);
                });
        }
    };
    return (
        <div className="div-container">
            <div className="container">
                <Grid
                    lg={4}
                    md={8}
                    sm={10}
                    xs={12}
                    container
                    direction="row"
                    justify="center"
                    alignItems="center"
                    className="form"
                >
                    <Grid item className="loginTitle">
                        <Typography variant="h4" style={{ fontFamily: "Montserrat" }}>Forgot Password</Typography>
                    </Grid>
                    <Grid item xs={12} className={`loginInput ${isButtonClicked ? 'darken' : ''}`}>
                        <input
                            style={{
                                fontFamily: "Montserrat" }}
                            type="text"
                            placeholder="Username"
                            onChange={(e) => handleChangeUsername(e.target.value)}
                            disabled={isUsernameDisabled}
                        ></input>
                    </Grid>
                    {showConfirmationCode && (
                        <Grid item xs={12} >
                            <Grid className="loginInput">
                                <input
                                    style={{ fontFamily: "Montserrat" }}
                                    type="text"
                                    placeholder="Confirmation Code"
                                    onChange={(e) => handleGetCode(e.target.value)}
                                ></input>
                            </Grid>
                            <Grid className="loginInput">
                                <input
                                    style={{ fontFamily: "Montserrat" }}
                                    type="password"
                                    placeholder="Enter New Password"
                                    onChange={(e) => handleGetNewPassword(e.target.value)}
                                ></input>
                            </Grid>
                            <Grid className="loginInput">
                                <input
                                    style={{ fontFamily: "Montserrat" }}
                                    type="password"
                                    placeholder="Repeat New Password"
                                    onChange={(e) => handleGetConfirmPassword(e.target.value)}
                                ></input>
                            </Grid>
                        </Grid>
                    )}
                    {isButtonClicked ? (
                        <Button
                            style={{ fontFamily: "Montserrat" }}
                            className="btn"
                            onClick={handleResetPassword}
                            disabled={loading}
                        >
                            {
                                loading ? (
                                    <LoadingBar/>
                                ) : null
                            }
                            Reset Password
                        </Button>
                    ) : (
                        <Button
                            style={{ fontFamily: "Montserrat" }}
                            className="btn"
                            onClick={handleSendCode}
                            disabled={loading}
                        >
                            {
                                loading ? (
                                    <LoadingBar/>
                                ) : null
                            }
                            Send Code
                        </Button>
                    )}
                </Grid>
            </div>
        </div>
    );
}
export default ForgotPassword;