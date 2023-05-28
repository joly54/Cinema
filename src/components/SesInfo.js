import React, {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import {toast, ToastContainer} from "react-toastify";
import {Button, Grid, Typography} from "@material-ui/core";
import BackToTopButton from "./BackToTopButton";
import * as api from "../utils/Api";
import "./Styles/SesInfo.css";
import './Styles/scrollBar.css';
import './Styles/preloader.css';
import Preloader from "./preloader";
function SesInfo({handlePayData}){

    //get current url
    const session =  window.location.href.split("/")[window.location.href.split("/").length-1];
    const navigate = useNavigate();
    const [sessionInfo, setSessionInfo] = useState([]);
    const [aviSeats, setAviSeats] = useState([]);
    const [selected, setSelected] = useState([]);
    const username = localStorage.getItem("username");
    const token = localStorage.getItem("token");
    useEffect(() => {
        if(!username || !token){
            toast.error("You are not logged in.",
                {
                    position: "top-center",
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: false,
                    draggable: true}
            );
            //remove from history
            window.history.replaceState(null, null, "/Cinema");
            navigate("/login");
            return;
        } else{
            api.checktoken(username, token)
                .then(res => {
                    if (res.ok) {
                        res.json().then(data => {
                            console.log(data);
                        });
                    } else {
                        res.json().then(data => {
                            console.error(data);
                            toast.error("Your session has expired. Please log in again.",
                                {
                                    position: "top-center",
                                    autoClose: 5000,
                                    hideProgressBar: false,
                                    closeOnClick: true,
                                    pauseOnHover: false,
                                    draggable: true}
                            );
                            window.history.replaceState(null, null, "/Cinema");
                            navigate("/login");
                            return;
                        });
                    }
                })
                .catch(error => {
                    console.error(error);
                    //toast message from server

                    navigate("/")
                });
                }
        api.getSessionInfo(session)
            .then(res => {
                if (res.ok) {
                    res.json().then(data => {
                        console.log(data);
                        setSessionInfo(data);
                        setAviSeats(data["seats"])
                        document.title = data["title"] + " - " + data["date"] + " " + data["time"] + " " + data["price"] + "UAH";
                    });
                } else {
                    res.json().then(data => {
                        console.error(data);
                        navigate("/");
                    });
                }
            })
            .catch(error => {
                console.error(error);
                toast.error("Failed to get session info.");
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
        document.getElementById("selected").innerHTML = selected;

    }
    function buy(){
        api.buyTicket(session, localStorage.getItem("username"), localStorage.getItem("token"), selected)
            .then(res => {
                if (res.ok) {
                    res.json().then(data => {
                        console.log(data);
                        toast.success("Payment created successfully!");
                        handlePayData(
                            {
                                pay_id: data["id"],
                                pay_amount: data["amount"],
                                pay_title: data["title"],
                                pay_date: data["date"],
                                pay_time: data["time"],
                                pay_seats: data["seats"],
                            }
                        )
                        navigate("/payment");
                    });
                } else {
                    res.json().then(data => {
                        console.error(data);
                        toast.error(data["message"]);
                    });
                }
            })
    }
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
            {sessionInfo && sessionInfo["trailer"] ? <div>
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
                                style={{
                                    fontFamily: "Montserrat",
                                    marginLeft: "17px",
                                }}
                                variant="h4"
                            >
                                {sessionInfo["title"]}
                            </Typography>
                            <Typography
                                style={{
                                    fontFamily: "Montserrat",
                                    marginLeft: "17px",
                                }}
                                variant="h6"
                                className="FilmInfo">
                                {sessionInfo["date"] + " " + sessionInfo["time"] + " " + sessionInfo["seats"].length + " seats left"}
                            </Typography>
                            <br></br>
                            <Typography
                                style={{
                                    marginLeft: "17px",
                                }}
                                mt={2}
                                className="FilmInfo"
                                variant="h6"
                            >
                                {sessionInfo["description"]}
                            </Typography>
                        </Grid>
                        <Grid item xs={11} md={6}
                              style={{
                                  marginLeft: "17px",
                                  display: "flex",
                                  justifyContent: "center",
                                  alignItems: "center",
                              }}
                        >
                            <iframe
                                style={{borderRadius: "10px"}}
                                title="Movie trailer"
                                width="500"
                                height="315"
                                src={`https://www.youtube.com/embed/${sessionInfo["trailer"].split("v=")[1]}?autoplay=1&mute=1`}
                                title="YouTube video player"
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                                allowFullScreen/>
                        </Grid>
                    </Grid>
                <Grid>
                    <div>
                        <div className="Seats"
                        style={{
                            maxWidth: "99%",
                            justifyContent: "center",
                            alignItems: "center",
                        }}>
                            <img
                            src={sessionInfo["poster"]}
                            className="screen"
                            >
                            </img>
                            <div style={{
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                flexDirection: "row",
                            }}>
                                <Typography
                                    component="h1"
                                    variant="h5"
                                    style={{
                                        fontFamily: "Montserrat",
                                        fontSize: "1.5rem",
                                        fontWeight: "bold",
                                        textAlign: "center",
                                        margin: "1rem",
                                        color: "white",
                                        marginRight: "0.5rem"
                                    }}
                                >
                                    Selected seats:
                                </Typography>
                                <Typography
                                    component="h1"
                                    variant="h5"
                                    id="selected"
                                    style={{
                                        fontFamily: "Montserrat",
                                        fontSize: "1.5rem",
                                        fontWeight: "bold",
                                        textAlign: "center",
                                        margin: "1rem",
                                        color: "orange",
                                    }}
                                >
                                    {null}
                                </Typography>
                            </div>
                            <Grid container spacing={1}>
                                {[...Array(5)].map((_, row) => (
                                    <Grid key={row} item xs={15} container justifyContent="center">
                                        {[...Array(12)].map((_, col) => (
                                            <div id={(row * 12) + col + 1} className={
                                                ( aviSeats.includes((row * 12) + col + 1) ? "available" : "occupied") + " square"
                                            } onClick={()=>{
                                                setSelect((row * 12) + col + 1);}
                                            }>
                                                <Typography

                                                    style={{
                                                        fontSize: "1rem",
                                                        color: "white",
                                                        fontFamily: "Montserrat",
                                                        textAlign: "center",
                                                        fontWeight: "bold",
                                                        display: "flex",
                                                        alignItems: "center",
                                                        justifyContent: "center",
                                                    }}
                                                >
                                                    {(row * 12) + col + 1}
                                                </Typography>
                                            </div>
                                        ))}
                                    </Grid>
                                ))}
                                <div className="center-button-container">
                                    <div className="button">
                                        <Button
                                            variant="contained"
                                            color="primary"
                                            onClick={buy}
                                            style={{
                                                width: "150px",
                                                borderRadius: "10px",
                                                boxShadow: "0 0 10px rgba(0, 0, 0, 0.9)",
                                            }}
                                        >
                                            Pay
                                        </Button>
                                    </div>
                                </div>
                            </Grid>
                        </div>
                    </div>
                </Grid>
                </div> : <p>Loading...</p>}
        </div>
    );

}
export default SesInfo;