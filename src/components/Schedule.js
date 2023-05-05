import React, { useState, useEffect } from 'react';
import './Schedule.css'
import {Grid, Card, CardActionArea, CardMedia, CardContent, Typography, Button} from '@material-ui/core';
import * as api from '../utils/Api'

function CinemaSchedule() {
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
    schedule.map((item) => {
        console.log(item);
    })
    return (
        schedule.map((day) => (
            <>
                <h2
                style={{ textAlign: "center",
                    fontSize: "2rem",
                    fontWeight: "bold",
                    margin: "2rem 0",
                    color: "#ff8c00"
                }}
                >{day["date"]}</h2>
                <Grid container spacing={4}>
                    {day["sessions"].map((scheduleItem) => (
                        <Grid item xs={12} md={6} lg={3} key={scheduleItem}>
                            <Card>
                                <CardActionArea>
                                    <CardMedia
                                        component="img"
                                        image={"https://img.youtube.com/vi/" + scheduleItem["trailer"].split('v=')[1] + "/maxresdefault.jpg"}
                                        title="Card image"
                                        style={{ maxHeight: '200px' }}
                                    />
                                    <CardContent className="card-content">
                                        <Typography gutterBottom variant="h5" component="h2" className="card-title">
                                            {scheduleItem["title"]}
                                        </Typography>
                                        <Typography variant="body2" color="textSecondary" component="p">
                                            {scheduleItem["description"]}
                                        </Typography>
                                        <Button variant="contained" color="primary" href="/"
                                                style={{ backgroundColor: "#ff8c00",
                                                    color: "#fff",
                                                    padding: "0.5rem 1rem",
                                                    border: "none",
                                                    borderRadius: "0.3rem",
                                                    cursor: "pointer",
                                                    transition: "background-color 0.2s ease-in-out" }}>
                                            Buy ticket for {scheduleItem["price"]}UAH
                                        </Button>

                                    </CardContent>
                                </CardActionArea>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            </>
        ))
    );

}

export default CinemaSchedule;
