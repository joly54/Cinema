import React, {useEffect} from "react";
import {toast, ToastContainer} from "react-toastify";
import {Grid, Typography} from "@material-ui/core";
import BackToTopButton from "./BackToTopButton";
import * as api from "../utils/Api";
import "./Styles/FIlmInfo.css"
import {Link} from "react-router-dom";

function FilmsInfo() {
    useEffect(() => {
        window.scrollTo(0, 0)
    }, [])
    const film_id = window.location.href.split("/")[window.location.href.split("/").length - 1];
    const [data, setData] = React.useState(null);
    const [sessions, setSessions] = React.useState(null);
    useEffect(() => {
        api.getSessions(film_id)
            .then(res => {
                if (res.ok) {
                    res.json().then(data => {
                        setData(data);
                        setSessions(data["sessions"]);
                        document.title = data["title"];
                    });
                } else {
                    res.json().then(data => {
                        console.error(data);
                        toast.error(data["message"]);
                    });
                }
            });
    }, [film_id]);
    return (
        <div
            style={{
                marginLeft: "8px",
                height: "100%",
                justifyContent: "center",
                alignItems: "center",
            }}
        >
            <ToastContainer/>
            <BackToTopButton/>
            {data && data["trailer"] ? <div>
                <Grid container spacing={2}
                      style={{
                          maxWidth: "100%",
                          display: "flex",
                          justifyContent: "center",
                          alignItems: "center",
                          marginTop: "20px"
                      }}
                >
                    <Grid item xs={12} md={6}
                    >
                        <Typography
                            className="FilmInfo"
                            style={{fontFamily: "Montserrat", textDecoration: 'none'}}
                            variant="h4"
                        >
                            {data["title"]}
                        </Typography>
                        <Typography
                            style={{fontFamily: "Montserrat", textDecoration: 'none'}}
                            variant="h6"
                            className="FilmInfo">
                            {data["sessions"].length + " available sessions"}
                        </Typography>
                        <br></br>
                        <Typography
                            mt={2}
                            className="FilmInfo"
                            variant="h6"
                            style={{textDecoration: 'none'}}
                        >
                            {data["description"]}
                        </Typography>
                    </Grid>
                    <Grid item xs={12} md={6}
                          style={{
                              display: "flex",
                              justifyContent: "center",
                              alignItems: "center",
                          }}
                    >
                        <iframe
                            style={{borderRadius: "10px", marginTop: "1rem"}}
                            title="Movie trailer"
                            width="500"
                            height="315"
                            src={`https://www.youtube.com/embed/${data["trailer"].split("v=")[1]}?autoplay=1&mute=1`}
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                            allowFullScreen/>
                    </Grid>
                    <Grid
                        style={{
                            maxWidth: "100%",
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            marginTop: "15px",
                            marginBottom: "15px",
                        }}
                    >
                        <img

                            className={"film-poster"}
                            src={data["poster"]}
                            alt="poster"></img>
                    </Grid>
                    <Grid container xs={12} md={6} lg={8}
                          style={
                              {
                                  display: "flex",
                                  justifyContent: "center",
                                  alignItems: "center",
                                  padding: "10px",
                                  borderRadius: "10px",
                                  boxShadow: "0px 3px 10px rgba(0, 0, 0, 0.1)",
                                  marginBottom: "10px",
                              }
                          }
                    >
                        {sessions.map((session, index) => (
                            session["seats"].length > 0 ?
                                <Link to={`/sessionInfo/${session["id"]}`}
                                      style={{
                                          textDecoration: "none",
                                          color: "black",
                                      }}
                                >
                                    <Grid
                                        key={index}
                                        item
                                        spacing={2}
                                        className={"session"}
                                        style={{
                                            marginBottom: "10px",
                                            marginRight: "10px",
                                            textDecoration: "none",
                                        }}
                                    >
                                        <Typography
                                            style={{
                                                fontFamily: "Montserrat",
                                                fontWeight: "bold",
                                                marginBottom: "5px",
                                            }}
                                            variant="h6"
                                        >
                                            {session["date"]}
                                        </Typography>
                                        <Typography
                                            style={{fontFamily: "Montserrat", marginBottom: "5px"}}
                                            variant="h6"
                                        >
                                            {session["time"]}
                                        </Typography>
                                        <Typography
                                            style={{fontFamily: "Montserrat"}}
                                            variant="h6"
                                        >
                                            {session["seats"].length} seats available
                                        </Typography>
                                    </Grid>
                                </Link> : null
                        ))}

                    </Grid>
                </Grid>
            </div> : <p>Loading...</p>}
        </div>
    );
}
export default FilmsInfo;