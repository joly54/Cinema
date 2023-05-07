import React from "react";
import {useNavigate} from "react-router-dom";
import { useState, useEffect } from "react";
import * as api from "../utils/Api";
import {Card, Grid, Typography} from "@material-ui/core";
import "./Styles/TiktetPage.css";
import './Styles/scrollBar.css';
import BackToTopButton from "./BackToTopButton";

function FilmPage(ses_id){
    const navigate = useNavigate();
    const [sessionInfo, setSessionInfo] = useState([]);
    const [aviSeats, setAviSeats] = useState([]);
    const [selected, setSelected] = useState([]);
    useEffect(() => {
        api.getSessionInfo(ses_id["ses_id"])
            .then(res => {
                if (res.ok) {
                    res.json().then(data => {
                        console.log(data);
                        setSessionInfo(data);
                        setAviSeats(data["seats"])
                        console.log(aviSeats[0])
                    });
                } else {
                    res.json().then(data => {
                        console.error(data);
                        //alert(data.message);
                        navigate("/");
                    });
                }
            })
            .catch(error => {
                console.error(error);
                alert("Failed to fetch session info.");
            });
    }, []);
    Array.from({ length: 49 }, (_, i) => i + 1);

    function setSelect(id){
        if(document.getElementById(id).classList.contains("occupied"))
            return;
        document.getElementById(id).classList.toggle("selected");
        const items = selected;
        if(document.getElementById(id).classList.contains("selected"))
            items.push(id);
        else
            items.splice(items.indexOf(id), 1);
        setSelected(items)
        document.getElementById("selected").innerHTML = "Selected: " + selected;

        console.log(selected);
    }
    return (
        <div>
            <BackToTopButton />
            {sessionInfo && sessionInfo["trailer"] ? (
                <Grid>
                    <Card class = "CenterDataFilm">
                        <h1>{sessionInfo["title"]}</h1>
                        <h2>{sessionInfo["description"]}</h2>
                        <h3>{sessionInfo["date"]}</h3>
                        <h3>{sessionInfo["time"]}</h3>
                        <h3>Prise: {sessionInfo["price"]} uah</h3>
                    </Card>
                    <Card class="CenterIframe">
                        <iframe
                            width="560"
                            height="315"
                            src={`https://www.youtube.com/embed/${sessionInfo["trailer"].split("v=")[1]}`}
                            title="YouTube video player"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                            allowFullScreen
                        ></iframe>
                    </Card>
                    <br/>
                    <div id="selected"></div>
                    <div className="Seats">
                        <Grid container spacing={1}
                        style={
                            {
                                maxWidth: "100%",
                            }
                        }
                        >
                            {[...Array(7)].map((_, row) => (
                                <Grid key={row} item xs={12} container justifyContent="center">
                                    {[...Array(7)].map((_, col) => (
                                        <div id={(row * 7) + col + 1} className={
                                            ( aviSeats.includes((row * 7) + col + 1) ? "aviable" : "occupied") + " square"
                                        } onClick={()=>{
                                            setSelect((row * 7) + col + 1);}
                                        }>
                                            <Typography
                                                variant="body1"
                                                style={{
                                                    color: "white",
                                                    textAlign: "center",
                                                    fontWeight: "bold",
                                                    display: "flex",
                                                    alignItems: "center", // Центрирование по вертикали
                                                    height: "100%", // Задайте высоту для Typography
                                                    justifyContent: "center"
                                                }}
                                            >
                                                {(row * 7) + col + 1}
                                            </Typography>
                                        </div>
                                    ))}
                                </Grid>
                            ))}
                        </Grid>

                    </div>
                </Grid>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );

}

export default FilmPage;