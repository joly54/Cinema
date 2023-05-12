import React, {useEffect} from "react";
import {Grid, Typography} from "@material-ui/core";
import * as api from "../utils/Api";
import {toast, ToastContainer} from "react-toastify";
import BackToTopButton from "./BackToTopButton";
import "./Styles/FIlmInfo.css"

function FilmsInfo({
                       handleSession
                   }){
    //get current url
    const film_id = window.location.pathname.split("/")[2];
    const [data, setData] = React.useState(null);
    const [sessions, setSessions] = React.useState(null);
    //const navigate = useNavigate();
    useEffect(() => {
        api.getSessions(film_id)
            .then(res => {
                if (res.ok) {
                    res.json().then(data => {
                        console.log(data);
                        setData(data);
                        setSessions(data["sessions"]);
                    });
                } else {
                    res.json().then(data => {
                        console.error(data);
                        toast.error(data["message"]);
                        //navigate("/")
                    });
                }
            });
    }, []);
    return (
        <div
            style={{
                height: "100%",
                width: "100%",
                //centering
                justifyContent: "center",
                alignItems: "center",
            }}
        >
            <ToastContainer />
            <BackToTopButton />
            {data && data["trailer"] ? <div>
                <Grid container spacing={2}
                      style={{
                          maxWidth: "100%",
                          justifyContent: "center",
                          alignItems: "center",


                      }}
                >
                    <Grid item xs={12} md={6}
                          style={{
                          }}
                    >
                        <Typography
                            className="FilmInfo"
                            style={{fontFamily: "Montserrat"}}
                            variant="h4"
                        >
                            {data["title"]}
                        </Typography>
                        <Typography
                            style={{fontFamily: "Montserrat"}}
                            variant="h6"
                            className="FilmInfo">
                            {data["sessions"].length + " available sessions"}
                        </Typography>
                        <br></br>
                        <Typography
                            mt={2}
                            className="FilmInfo"
                            variant="h6"
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
                            style={{
                        borderRadius: "10px",
                        }
                            }
                            title="Movie trailer"
                            width="500"
                            height="315"
                            src={`https://www.youtube.com/embed/${data["trailer"].split("v=")[1]}?autoplay=1&mute=1`}
                            title="YouTube video player"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                            allowFullScreen/>
                    </Grid>
                    <Grid
                    style={{
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",

                    }}
                    >
                        <img
                            style={{
                                width: "50%",
                                height: "auto",
                                padding: "10px",
                                objectFit: "cover",
                                borderRadius: "10px",
                            }}
                            src={data["poster"]}
                            alt="poster"></img>
                    </Grid>
                    <Grid
                        xs={12}
                        container
                    >
                        {sessions.map((session, index) => (
                            <Grid
                                onClick={() => handleSession(session["id"])}
                                key={index}
                                item
                                xs={12}
                                md={6}
                                lg={4}
                                spacing={2}
                                style={{
                                    cursor: "pointer",
                                    maxWidth: "100%",
                                    justifyContent: "center",
                                    alignItems: "center",
                                    padding: "10px",
                                    borderRadius: "10px",
                                    backgroundColor: "#f5f5f5",
                                    marginTop: "10px",
                                    marginBottom: "10px",
                                    paddingLeft: "10px",
                                }}
                            >
                                <Typography
                                    style={{ fontFamily: "Montserrat" }}
                                    variant="h6"
                                >
                                    {session["date"]}
                                </Typography>

                                <Typography
                                    style={{ fontFamily: "Montserrat" }}
                                    variant="h6"
                                >
                                    {session["time"]}
                                </Typography>
                                <Typography
                                    style={{ fontFamily: "Montserrat" }}
                                    variant="h6"
                                >
                                    {session["seats"].length} seats left
                                </Typography>
                            </Grid>
                        ))}
                    </Grid>
                </Grid>
            </div> : <p>Loading...</p>}
        </div>
    );
}
export default FilmsInfo;