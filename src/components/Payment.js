import React, {useEffect} from 'react';
import {toast} from "react-toastify";
import {Button, Grid, Typography} from '@material-ui/core';
import * as api from "../utils/Api"
import './Styles/Payment.css'
import './Styles/scrollBar.css';
import {useNavigate} from "react-router-dom";
import LoadingBar from "./Progress.js";


function Payment ({data, moneyFormat}){
    useEffect(() => {
        window.scrollTo(0, 0)
    }, [])
    document.title = "Payment";
    const navigate = useNavigate();
    const [isLoading, setIsLoading] = React.useState(false);

    if(data["pay_id"] === undefined){
        navigate("/");
        return
    }
    function confirmPayment() {
        setIsLoading(true);
        if(
            document.getElementById("cardNumber").value.length !== 19 ||
            document.getElementById("cardDate").value.length !== 5 ||
            document.getElementById("cardCVV").value.length !== 3
        ){
            //reqest focus
            toast.error("Invalid card data", {
                position: "top-center",
                autoClose: 5000,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: false,
                pauseOnFocusLoss: false,
                theme: "colored",
                draggable: true
            });
            document.getElementById("cardNumber").focus();
            setIsLoading(false);
            return
        }
        api.confirmPayment(data["pay_id"])
            .then(res => {
                setIsLoading(false);
                if (res.ok) {
                    res.json().then(data => {
                        toast.success("You successfully bought tickets!",{
                            position: "top-center",
                            autoClose: 5000,
                            hideProgressBar: false,
                            closeOnClick: true,
                            pauseOnHover: false,
                            pauseOnFocusLoss: false,
                            theme: "colored",
                            draggable: true
                        });
                        navigate("/profile");
                    });
                }
                else {
                    res.json().then(data => {
                        toast.success(data["message"],{
                            position: "top-center",
                            autoClose: 5000,
                            hideProgressBar: false,
                            closeOnClick: true,
                            pauseOnHover: false,
                            pauseOnFocusLoss: false,
                            theme: "colored",
                            draggable: true
                        });
                    });
                }
            })
            .catch(error => {
                console.error(error);
                toast.error("Failed to confirm payment", {
                    position: "top-center",
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: false,
                    pauseOnFocusLoss: false,
                    theme: "colored",
                    draggable: true
                });
            });
    }
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
                        <Grid
                            spacing={12}
                        className="paymentInfo"
                        style={{
                            fontFamily: "Montserrat",
                            marginBottom: "20px",
                            width: "100%",
                            fontWeight: "bold",
                        }}
                        container
                        >
                            <Typography className="payInfo" variant="h6">Film tittle: {data["pay_title"]};</Typography>
                            <Typography className="payInfo" variant="h6">Date: {data["pay_date"]};</Typography>
                            <Typography className="payInfo" variant="h6">Time: {data["pay_time"]};</Typography>
                            <Typography className="payInfo" variant="h6">Seats: {data["pay_seats"]};</Typography>
                            <Typography className="payInfo" variant="h6">Price: {moneyFormat(data["pay_amount"])}UAH</Typography>
                        </Grid>
                        <Typography variant="h6" style={{fontFamily: "Montserrat"}}>Card number:</Typography>
                        <input
                            style={{fontFamily: "Montserrat"}}
                            id={"cardNumber"}
                            type="text"
                            placeholder="XXXX-XXXX-XXXX-XXXX"
                            maxLength="19"
                            onChange={(event) => {
                                console.log("123")
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
                                id={"cardDate"}
                                placeholder="XX/XX"
                                maxLength="5"
                                onChange={(event) => {
                                    console.log("123")
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
                                id="cardCVV"
                                maxLength={3}
                                style={{ fontFamily: "Montserrat" }}
                                type="text"
                                placeholder="XXX"
                                onKeyUp={(event) => {
                                    let modifiedValue = event.target.value;
                                    switch (modifiedValue.length) {
                                        case 0:
                                            break;
                                        case 1:
                                            modifiedValue = "*";
                                            break;
                                        case 2:
                                            modifiedValue = "**";
                                            break;
                                        case 3:
                                            modifiedValue = "***";
                                            break;
                                        default:
                                            break;
                                    }
                                    event.target.value = modifiedValue;
                                }}
                            />


                        </Grid>
                    </Grid>
                    <Grid item xs={12} className="payButton">
                        <Button onClick = {confirmPayment}
                            style={{fontFamily: "Montserrat"}}
                            className="btn"
                                disabled={isLoading}
                        >
                            {isLoading ? <LoadingBar/> : null}
                            PAY</Button>
                    </Grid>
                </Grid>
            </div>
        </div>
    );
}
export default Payment