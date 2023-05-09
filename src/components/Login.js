import React from 'react';
import './Styles/login.css';
import {useNavigate} from "react-router-dom";
import './Styles/scrollBar.css';
import {Button, Grid, Typography} from "@material-ui/core";
function Login(
    {
        handleChangeUsername,
        handleChangePassword,
        handleLogin,
    }
) {
    const navigate = useNavigate();
    return (
        <div
        className="container"
        >
            <Grid
                style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                }}
                lg={4}
                md={5}
                xs={12}
            className="form"
            >
            <Grid
                container
                direction="row"
                justify="center"
                alignItems="center"
                className="loginContainer">
                <Grid
                    item

                    className="loginTitle"
                style={{
                    fontFamily: "Montserrat",
                }}
                >
                    <h1>LOGIN</h1>
                </Grid>
                <Grid item xs={12} className="loginInput">
                    <input
                        type="text"
                        placeholder="Username"
                        onChange={(e) => handleChangeUsername(e.target.value)}
                    ></input>
                </Grid>
                <Grid item xs={12} className="loginInput">
                    <input
                        type="password"
                        placeholder="Password"
                        onChange={(e) => handleChangePassword(e.target.value)}
                    >
                    </input>
                </Grid>
                <Grid item xs={12} className="loginButton">
                    <Button
                        className="btn"
                            onClick={handleLogin}
                        style={{
                            fontFamily: "Montserrat",
                        }}
                    >Log in</Button>
                    <Typography
                        className="text-btn"
                        onClick={() => navigate("/forgotPassword")}
                        style={{
                            fontFamily: "Montserrat",
                        }}
                    >Forgot Password?</Typography>
                </Grid>

            </Grid>
        </Grid>
        </div>
    );
}

export default Login;
