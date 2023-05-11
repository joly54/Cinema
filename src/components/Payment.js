import React from 'react';
import './Styles/Payment.css'
import {Button, Grid, Typography} from '@material-ui/core';

import './Styles/scrollBar.css';

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
                            maxLength="19"
                            onKeyUp={(event) => {
                                const input = event.target;
                                const inputValue = input.value.replace(/\D/g, '');
                                let maskedValue = '';
                                for (let i = 0; i < inputValue.length && i < 16; i++) {
                                    if (i % 4 === 0 && i > 0) {
                                        maskedValue += ' ';
                                    }
                                    maskedValue += inputValue.charAt(i);
                                }
                                input.value = maskedValue;
                            }}
                        ></input>
                    </Grid>

                    <Grid container className="gridContainer">

                        <Grid item xs={3} className="privateInput">
                            <Typography className="" variant="h6" style={{fontFamily: "Montserrat"}}>Date:</Typography>
                            <input
                                style={{fontFamily: "Montserrat"}}
                                type="text"
                                placeholder="XX/XX"
                                maxLength="5"
                                onKeyUp={(event) => {
                                    const input = event.target;
                                    const inputValue = input.value.replace(/\D/g, '');
                                    let maskedValue = '';
                                    for (let i = 0; i < inputValue.length && i < 4; i++) {
                                        if (i === 2) {
                                            maskedValue += '/';
                                        }
                                        maskedValue += inputValue.charAt(i);
                                    }
                                    input.value = maskedValue;
                                }}
                            ></input>

                        </Grid>
                        <Grid item xs={2} className="privateInput">
                            <Typography className="" variant="h6" style={{fontFamily: "Montserrat"}}>CVV:</Typography>
                            <input
                                maxLength={3}
                                style={{fontFamily: "Montserrat"}}
                                type="text"
                                placeholder="XXX"
                                onKeyUp={(event) => {
                                    const input = event.target;
                                    const inputValue = input.value.replace(/\D/g, '');
                                    input.value = inputValue;
                                }}
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
