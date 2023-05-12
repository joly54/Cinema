import React, { useState } from 'react';
import './Styles/scrollBar.css';
import './Styles/ForgotPassword.css';
import { Button, Grid, Typography } from "@material-ui/core";

function ForgotPassword({ ResetPassword, handleChangeUsername }) {
    const [showConfirmationCode, setShowConfirmationCode] = useState(false);
    const [confirmationCode, setConfirmationCode] = useState('');
    const [isUsernameDisabled, setIsUsernameDisabled] = useState(false);
    const [isButtonClicked, setIsButtonClicked] = useState(false);

    const handleResetPassword = () => {
        ResetPassword();
        setShowConfirmationCode(true);
        setIsUsernameDisabled(true);
        setIsButtonClicked(true);
    };

    const handleConfirmationCodeChange = (e) => {
        setConfirmationCode(e.target.value);
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
                        style={{ fontFamily: "Montserrat" }}
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
                            >
                            </input>
                        </Grid>
                        <Grid className="loginInput">
                            <input
                                style={{ fontFamily: "Montserrat" }}
                                type="text"
                                placeholder="Repeat New Password"
                            >
                            </input>
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
