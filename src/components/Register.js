import React, {useEffect} from 'react';
import {Button, Grid, Typography} from "@material-ui/core";
import 'react-toastify/dist/ReactToastify.css';
import './Styles/login.css'
import './Styles/scrollBar.css';
import {Link, useNavigate} from "react-router-dom";
import LoadingBar from "./Progress.js";

function Register(
    {
        handleChangeUsername,
        handleChangePassword,
        handleRegister,
        isLogin,
        isLoading,
    }
) {
    document.title = "Register";
    const navigate = useNavigate();
    useEffect(() => {
        if (isLogin) {
            navigate("/profile");
        }
    }, [isLogin, navigate]);
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
                        <Typography variant="h4" style={{fontFamily: "Montserrat"}}>SING UP</Typography>
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
                            onClick={handleRegister}
                            disabled={isLoading}
                        >
                            {
                                isLoading ? <LoadingBar/> : null
                            }
                            SING UP</Button>
                    </Grid>
                    <Link to={"/login"} style={{textDecoration: "none",
                        paddingLeft: "10px"
                    }}>
                        <Typography
                            className={"text-btn"}
                            style={{fontFamily: "Montserrat"}}
                        >Already have account?</Typography></Link>
                </Grid>
            </div>
        </div>
    );
}
export default Register;