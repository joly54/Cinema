import React, { useState, useEffect } from 'react';
import './Styles/Payment.css'
import {Grid, Card, CardActionArea, CardMedia, CardContent, Typography, Button} from '@material-ui/core';
import * as api from '../utils/Api'
import './Styles/scrollBar.css';
import BackToTopButton from "./BackToTopButton";

function Payment (){
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
                    className="card-form"
                >
                    <Grid item className="paymentTitle">
                        <Typography variant="h4" style={{fontFamily: "Montserrat"}}>PAYMENT</Typography>
                    </Grid>
                    <Grid item xs={12} className="numberInput">
                        <Typography variant="h6" style={{fontFamily: "Montserrat"}}>Card number:</Typography>
                        <input
                            style={{fontFamily: "Montserrat"}}
                            type="text"
                            placeholder="XXXX-XXXX-XXXX-XXXX"
                        ></input>

                    </Grid>

                    <Grid container  className="gridContainer" >

                        <Grid item xs={3} className="privateInput">
                            <Typography className="" variant="h6" style={{fontFamily: "Montserrat"}}>Date:</Typography>
                            <input
                                style={{fontFamily: "Montserrat"}}
                                type="text"
                                placeholder="XX/XX"
                            ></input>
                        </Grid>
                        <Grid item xs={2} className="privateInput">
                            <Typography className="" variant="h6" style={{fontFamily: "Montserrat"}}>CVV:</Typography>
                            <input
                                style={{fontFamily: "Montserrat"}}
                                type="password"
                                placeholder="XXX"
                            ></input>
                        </Grid>
                    </Grid>

                    <Grid item xs={12} className="payButton">
                        <Button
                            style={{fontFamily: "Montserrat"}}
                            className="btn"
                        >PAY</Button>
                    </Grid>
                </Grid>
            </div>
        </div>
    );
}

export default Payment
