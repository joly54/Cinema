import React, {useEffect, useState} from "react";
import * as api from "../utils/Api";
import {Grid, Typography} from "@material-ui/core";
import {useNavigate} from "react-router-dom";
import "./Styles/pay_history.css";

function PayHistory({
                        setPayData,
                        moneyFormat,
                    }) {
    document.title = "Pay history";

    const navigate = useNavigate();

    const [data, setData] = useState([]);

    useEffect(() => {
        api.get_history()
            .then((res) => {
                if (res.ok) {
                    res.json().then((data) => {
                        setData(data);
                    });
                } else {
                    res.json().then((errorData) => {
                        console.error(errorData);
                        // Handle the error appropriately
                    });
                }
            })
            .catch((error) => {
                console.error(error);
                // Handle the error appropriately
            });
    }, []);

    return (
        <div
            style={{
                padding: "1rem",
                minHeight: "100vh",
                display: "flex",
                justifyContent: "center",
            }}
        >
            <div style={{width: "80%"}}>
                <Grid container spacing={3}>
                    <Grid item xs={12}>
                        <Typography variant="h3" component="h4" gutterBottom
                                    style={{
                                        textAlign: "center",
                                        marginBottom: "1rem",
                                        fontFamily: "Montserrat",
                                        color: "#fff",
                                    }}
                        >
                            Pay history
                        </Typography>
                    </Grid>
                    {data.map((item) => (
                        <Grid
                            item
                            key={item.id}
                            xs={6}
                            sm={6}
                            md={6}
                            lg={12}
                            container
                            direction="row"
                            justifyContent="center"
                            alignItems="baseline"
                            >
                            <div
                                {...(!item.confirmed ? {
                                    onClick: () => {
                                        setPayData({
                                            pay_id: item.id,
                                            pay_amount: item.amount,
                                            pay_title: item.title,
                                            pay_time: item.time,
                                            pay_date: item.date,
                                            pay_seats: item.seats.join(", "),
                                        });
                                        navigate("/payment");
                                    }
                                } : {})}
                                className={item.confirmed ? "confirmed" : "not_confirmed"}
                                style={{
                                    backgroundColor: item.confirmed ? "rgb(220 252 231)" : "rgb(254 205 211)",
                                    padding: "1rem",
                                    width: "60%",

                                    borderRadius: "0.5rem",
                                }}
                            >
                                <Grid container direction="row" justifyContent="space-between" alignItems="baseline">
                                    <h5>{item.title}</h5>
                                    <h5>{moneyFormat(item.amount)} UAH</h5>
                                </Grid>
                                <Grid container direction="row" justifyContent="space-between" alignItems="baseline">
                                    <p>{item.seats.length === 1 ? "Seat: " : "Seats: "}{item.seats.join(", ")}</p>
                                    <p>{item.date} {item.time}</p>
                                </Grid>
                                {item.confirmed ? null : <p style={{color: "red"}}>Not confirmed</p>}
                            </div>
                        </Grid>
                    ))}
                </Grid>
            </div>
        </div>
    );
}

export default PayHistory;
