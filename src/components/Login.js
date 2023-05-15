import React from 'react';
import {Link, useNavigate} from "react-router-dom";
import { Button, Grid, Typography } from "@material-ui/core";
import './Styles/login.css';
function Login({
                   handleChangeUsername,
                   handleChangePassword,
                   handleLogin,
               }) {
    document.title = "Login";
    const navigate = useNavigate();
    return (
        <div className="container"
             style={{
                 height: "100vh",
             }}
        >
            <div
                style={{
                    width: "100%",
                }}
            >
                <Grid
                    xl={4}
                    lg={5}
                    md={5}
                    sm={9}
                    xs={12}
                    container
                    direction="row"
                    justify="center"
                    alignItems="center"
                    className="form"
                >
                    <Grid item className="loginTitle">
                        <Typography variant="h4" style={{fontFamily: "Montserrat"}}>LOGIN</Typography>
                    </Grid>
                    <Grid item xs={12} className="loginInput">
                        <input
                            style={{fontFamily: "Montserrat"}}
                            type="text"
                            placeholder="Username"
                            onChange={(e) => handleChangeUsername(e.target.value)}
                        ></input>
                    </Grid>
                    <Grid item xs={12} className="loginInput">
                        <input
                            style={{fontFamily: "Montserrat"}}
                            type="password"
                            placeholder="Password"
                            onChange={(e) => handleChangePassword(e.target.value)}
                        >
                        </input>
                    </Grid>
                    <Grid item xs={12} className="loginButton">
                        <Button
                            style={{fontFamily: "Montserrat"}}
                            className="btn"
                            onClick={handleLogin}
                        >Log in</Button>
                        <Grid
                            spacing={2}
                            container
                            direction="row"
                            justify="center"
                            alignItems="center"
                        >
                            <Link to={"/forgotPassword"} style={{textDecoration: "none"}}>
                                <Typography
                                    className={"text-btn"}
                                    style={{fontFamily: "Montserrat"}}
                                >Forgot Password?</Typography></Link>
                            <Link to={"/register"} style={{textDecoration: "none",
                            paddingLeft: "10px"
                            }}>
                                <Typography
                                    className={"text-btn"}
                                    style={{fontFamily: "Montserrat"}}
                                >Register</Typography></Link>
                        </Grid>
                    </Grid>
                </Grid>
            </div>
        </div>
    );
}
export default Login;