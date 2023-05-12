import React, { useState } from 'react';
import './Styles/scrollBar.css';
import './Styles/ForgotPassword.css';
import { Button, Grid, Typography } from "@material-ui/core";
import { toast } from "react-toastify";
import { forgotPasswordConfirm } from "../utils/Api";

function ForgotPassword({}) {
    const [showConfirmationCode, setShowConfirmationCode] = useState(false);
    const [confirmationCode, setConfirmationCode] = useState('');
    const [isUsernameDisabled, setIsUsernameDisabled] = useState(false);
    const [isButtonClicked, setIsButtonClicked] = useState(false);
    const [username, setUsername] = useState('');

    const handleResetPassword = () => {
        if (username !== '') {
            forgotPasswordConfirm(username)
                .then(response => {
                    if (response.ok) {
                        toast.success("Please check your email for the code", {
                            position: "top-center",
                            autoClose: 5000,
                            hideProgressBar: false,
                            closeOnClick: true,
                            pauseOnHover: false,
                            draggable: true
                        });
                        setShowConfirmationCode(true);
                        setIsUsernameDisabled(true);
                        setIsButtonClicked(true);
                    } else {
                        toast.error("Invalid email address", {
                            position: "top-center",
                            autoClose: 5000,
                            hideProgressBar: false,
                            closeOnClick: true,
                            pauseOnHover: false,
                            draggable: true
                        });
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    toast.error("An error occurred", {
                        position: "top-center",
                        autoClose: 5000,
                        hideProgressBar: false,
                        closeOnClick: true,
                        pauseOnHover: false,
                        draggable: true
                    });
                });
        } else {
            toast.error("Please enter a username", {
                position: "top-center",
                autoClose: 5000,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: false,
                draggable: true
            });
        }
    };

    const handleConfirmationCodeChange = (e) => {
        setConfirmationCode(e.target.value);
    };

    const handleChangeUsername = (value) => {
        setUsername(value);
        console.log(username);
    };
    return (
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
                                value={confirmationCode}
                                onChange={handleConfirmationCodeChange}
                            ></input>
                        </Grid>
                        <Grid className="loginInput">
                            <input
                                style={{ fontFamily: "Montserrat" }}
                                type="text"
                                placeholder="Enter New Password"
                            ></input>
                        </Grid>
                        <Grid className="loginInput">
                            <input
                                style={{ fontFamily: "Montserrat" }}
                                type="text"
                                placeholder="Repeat New Password"
                            ></input>
                        </Grid>
                    </Grid>
                )}
                <Button
                    style={{ fontFamily: "Montserrat" }}
                    className="btn"
                    onClick={handleResetPassword}
                >
                    Reset Password
                </Button>
            </Grid>
        </div>
    );
}

export default ForgotPassword;

