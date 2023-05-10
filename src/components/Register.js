import React from 'react';
import 'react-toastify/dist/ReactToastify.css';
import './Styles/login.css'
import './Styles/scrollBar.css';
import {Button, Grid, Typography} from "@material-ui/core";
function Register(
    {
        handleChangeUsername,
        handleChangePassword,
        handleRegister
    }
) {
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
                className="form">
                <Grid item className="loginTitle">
                    <Typography variant="h4" style={{fontFamily: "Montserrat"}}>REGISTER</Typography>
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
                    >Register</Button>
                </Grid>
            </Grid>
        </div>
    );
}

export default Register;