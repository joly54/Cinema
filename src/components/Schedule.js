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
            <div key={day.date}>
                <BackToTopButton />
                    <h2
                        style={{
                            textAlign: "center",
                        }}
                    >{day["date"]}</h2>

                    <Grid container spacing={4}
                          style={{
                              padding: "0 2rem",
                              alignContent: "center",
                              maxWidth: "100%",
                          }}
                    >
                        {day["sessions"].map((scheduleItem) => (
                            <Grid item xs={12} md={6} lg={3} key={scheduleItem.id}>
                                <Card
                                    style={{
                                        height: "100%",
                                        display: "flex",
                                        flexDirection: "column",
                                        justifyContent: "space-between",
                                    }}
                                >
                                    <CardActionArea>
                                        <CardMedia
                                            component="img"
                                            image={"https://img.youtube.com/vi/" + scheduleItem["trailer"].split('v=')[1] + "/maxresdefault.jpg"}
                                            title="Card image"
                                            style={{ maxHeight: '200px' }}
                                        />
                                        <CardContent className="card-content">
                                            <Typography gutterBottom variant="h5" component="h2" className="card-title" color = "textSecondary">
                                                {scheduleItem["title"] + " " + scheduleItem["time"]}
                                            </Typography>
                                            <Typography variant="body2" color="textSecondary" component="p">
                                                {scheduleItem["description"]}
                                            </Typography>
                                            <br></br>
                                            <Button
                                                className="btn"
                                                variant="contained"
                                                disableElevation
                                                color="primary"
                                                onClick={() => handleFilm(scheduleItem["session_id"])}
                                                disabled={scheduleItem["seats"].length === 0}
                                            >
                                                <Typography variant="body2" component="p" className="BuyTicket">
                                                    {scheduleItem["seats"].length === 0 ? "Sold out" : `Buy ticket ${scheduleItem["price"]} UAH`}
                                                </Typography>
                                            </Button>


                                        </CardContent>
                                    </CardActionArea>
                                </Card>
                            </Grid>
                        ))}
                    </Grid>

            </div>
        ))
    );
}

export default CinemaSchedule;