import React, {useEffect} from 'react';
import {Link, useNavigate} from "react-router-dom";
import {Button, Grid, Typography} from "@material-ui/core";
import './Styles/login.css';
import LoadingBar from "./Progress.js";


function Login({
                   handleChangeUsername,
                   handleChangePassword,
                   handleLogin,
                   isLoggedIn,
                   Isloading
               }) {
    useEffect(() => {
        window.scrollTo(0, 0)
    }, [])
    document.title = "Login";
    const navigate = useNavigate();
    useEffect(() => {
        if (isLoggedIn) {
            navigate("/profile");
        }
    }, [isLoggedIn, navigate]);
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
                            placeholder="Email"
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
                            disabled={Isloading}
                        >
                            {
                                Isloading ? <LoadingBar/> : null
                            }
                            Log in</Button>
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
                            <Link to={"/register"} style={{
                                textDecoration: "none",
                                paddingLeft: "10px"
                            }}>
                                <Typography
                                    className={"text-btn"}
                                    style={{fontFamily: "Montserrat"}}
                                >Dont have account?</Typography></Link>
                        </Grid>
                    </Grid>
                </Grid>
            </div>
        </div>
    );
}

export default Login;