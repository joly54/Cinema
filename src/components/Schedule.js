import React, { useState, useEffect } from 'react';
import './Styles/Schedule.css'
import {Grid, Card, CardActionArea, CardMedia, CardContent, Typography, Button} from '@material-ui/core';
import * as api from '../utils/Api'
import './Styles/scrollBar.css';
import BackToTopButton from "./BackToTopButton";

function CinemaSchedule({
                            handleFilm
                        }) {
    const [schedule, setSchedule] = useState([])
    useEffect(() => {
        api.schedule()
            .then((res) => {
                res.json().then(data => {
                    console.log(data);
                    if (res.ok) {
                        console.log(data);
                        setSchedule(data)
                    } else {
                        console.log(data);
                    }
                })
                    .catch(error => {
                        console.error(error);
                    });
            })
    },[])
    return (
        schedule.map((day) => (
            <div key={day.date}
                 className={"schedule"}
                 style={{
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        justifyContent: "center",
                        maxWidth: "100%",
                 }}
            >
                <BackToTopButton />
                <h2
                >
                    {day.date}
                </h2>

                <Grid
                    container
                    spacing={4}
                    style={{
                        display: "flex",
                        justifyContent: "left",
                        //padding: "0.1rem",
                        maxWidth: "100%",
                    }}
                >
                    {day.sessions.map((scheduleItem) => (
                        <Grid item xs={12} sm={6} md={6} lg={3} key={scheduleItem.id}>
                            <Card
                                className="card"
                                style={{
                                    transition: "all 0.3s ease-in-out",
                                    borderRadius: "12px",
                                    boxShadow: "1px 5px 15px 10px rgba(0,0,0,0.5)",
                                    display: "flex",
                                    flexDirection: "column",
                                    justifyContent: "space-between",
                                    height: "100%",
                                }}
                            >
                                <CardActionArea
                                    style={{
                                        display: "flex",
                                        flexDirection: "column",
                                        justifyContent: "space-between",
                                        height: "100%",
                                    }}
                                >
                                    <CardMedia
                                        component="img"
                                        image={scheduleItem.poster}
                                        title="Card image"
                                        style={{
                                            height: "200px",
                                            objectFit: "cover",
                                            objectPosition: "top",
                                            borderRadius: "12px 12px 0 0",
                                        }}
                                    />
                                    <CardContent className="card-content">
                                        <Typography
                                            gutterBottom
                                            variant="h5"
                                            component="h2"
                                            className="card-title"
                                            color="textSecondary"
                                        >
                                            {scheduleItem.title + " " + scheduleItem.time}
                                        </Typography>
                                        <Typography
                                            variant="body2"
                                            color="textSecondary"
                                            component="p"
                                            style={{
                                                height: "100px",
                                                overflow: "hidden",
                                                textOverflow: "ellipsis",
                                            }}
                                        >
                                            {scheduleItem.description}
                                        </Typography>
                                    </CardContent>
                                </CardActionArea>
                                <Button
                                    className={scheduleItem.seats.length === 0 ? "btn soldOut" : "btn"}
                                    variant="contained"
                                    disableElevation
                                    color="primary"
                                    onClick={() => handleFilm(scheduleItem.session_id)}
                                    disabled={scheduleItem.seats.length === 0}
                                    style={{
                                        width: "100%",
                                        borderRadius: "0 0 12px 12px",
                                       // objectPosition: "bottom",
                                    }}
                                >
                                    <Typography
                                        variant="body2"
                                        component="p"
                                        className={`BuyTicket ${scheduleItem.seats.length === 0 ? "soldOut" : ""}`}
                                    >
                                        {scheduleItem.seats.length === 0 ? "Sold out" : `Buy ticket ${scheduleItem.price} UAH`}
                                    </Typography>
                                </Button>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            </div>
        ))
    );


}

export default CinemaSchedule;