import React from 'react';
import {Button, Grid, Typography} from "@material-ui/core";
import 'react-toastify/dist/ReactToastify.css';
import './Styles/login.css'
import './Styles/scrollBar.css';
function Register(
    {
        handleChangeUsername,
        handleChangePassword,
        handleRegister
    }
) {
    document.title = "Register";
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
                            onClick={handleRegister}
                        >SING UP</Button>
                    </Grid>
                </Grid>
            </div>
        </div>
    );
}
export default Register;