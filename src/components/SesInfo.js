import React, {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import {toast, ToastContainer} from "react-toastify";
import {Button, Grid, Typography} from "@material-ui/core";
import BackToTopButton from "./BackToTopButton";
import * as api from "../utils/Api";
import "./Styles/SesInfo.css";
import './Styles/scrollBar.css';
import './Styles/preloader.css';
import LoadingBar from "./Progress.js";


function SesInfo({handlePayData, moneyFormatter}) {
    useEffect(() => {
        window.scrollTo(0, 0)
    }, [])
    const [isLoading, setIsLoading] = useState(false);

    const session = window.location.href.split("/")[window.location.href.split("/").length - 1];
    const navigate = useNavigate();
    const [sessionInfo, setSessionInfo] = useState([]);
    const [aviSeats, setAviSeats] = useState([]);
    const [selected, setSelected] = useState([]);
    useEffect(() => {

        api.isAuthenticated()
            .then((res) => {
                if (res.ok) {
                } else {
                    navigate('/login');
                }
            })
            .catch((err) => {
                console.log(err);
            });

        api.getSessionInfo(session)
            .then(res => {
                if (res.ok) {
                    res.json().then(data => {
                        setSessionInfo(data);
                        setAviSeats(data["seats"])
                        document.title = data["title"] + " - " + data["date"] + " " + data["time"] + " " + moneyFormatter(data["price"]) + "UAH";
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
                toast.error("Failed to get session info.",{
                        position: "top-center",
                        autoClose: 5000,
                        hideProgressBar: false,
                        closeOnClick: true,
                        pauseOnHover: false,
                        pauseOnFocusLoss: false,
                        theme: "colored",
                        draggable: true
                    }
                    );
            });
    }, [moneyFormatter, navigate, session]);
    Array.from({length: 49}, (_, i) => i + 1);

    function setSelect(id) {
        if (document.getElementById(id).classList.contains("occupied")) {
            return;
        }

        document.getElementById(id).classList.toggle("selected");

        const items = [...selected];

        if (document.getElementById(id).classList.contains("selected")) {
            items.push(id);
        } else {
            const index = items.indexOf(id);
            if (index !== -1) {
                items.splice(index, 1);
            }
        }

        items.sort(function(a, b) {
            return a - b;
        });

        setSelected(items);

        document.getElementById("selected").innerHTML = moneyFormatter(items.length * sessionInfo["price"]) + " UAH";
        if (items.length === 0) {
            document.getElementById("selected").innerHTML = "0 UAH";
        }
    }


    function buy() {
        setIsLoading(true);
        api.buyTicket(session, selected)
            .then(res => {
                setIsLoading(false);
                if (res.ok) {
                    res.json().then(data => {
                        toast.success("Payment created successfully!",{
                            position: "top-center",
                            autoClose: 5000,
                            hideProgressBar: false,
                            closeOnClick: true,
                            pauseOnHover: false,
                            pauseOnFocusLoss: false,
                            theme: "colored",
                            draggable: true
                        });
                        handlePayData(
                            {
                                pay_id: data["id"],
                                pay_amount: data["amount"],
                                pay_title: data["title"],
                                pay_date: data["date"],
                                pay_time: data["time"],
                                pay_seats: data["seats"].join(", "),
                            }
                        )
                        navigate("/payment");
                    });
                } else {
                    res.json().then(data => {
                        console.error(data);
                        toast.error(data["message"],{
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
    }

    return (
        <div
            style={{
                height: "100%",
                width: "100%",

                justifyContent: "center",
                alignItems: "center",
            }}
        >
            <ToastContainer/>
            <BackToTopButton/>
            {sessionInfo && sessionInfo["trailer"] ? <div>
                <Grid container spacing={2}
                      style={{
                          maxWidth: "100%",
                          justifyContent: "center",
                          alignItems: "center",
                            marginTop: "20px",
                      }}
                >
                    <Grid item xs={12} md={6}
                          style={{}}
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
                                alt="poster"
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
                                    Total:
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
                                    0 UAH
                                </Typography>
                            </div>
                            <Grid container spacing={1}>
                                {[...Array(5)].map((_, row) => (
                                    <Grid key={row} item xs={15} container justifyContent="center">
                                        {[...Array(12)].map((_, col) => (
                                            <div id={(row * 12) + col + 1} className={
                                                (aviSeats.includes((row * 12) + col + 1) ? "available" : "occupied") + " square"
                                            } onClick={() => {
                                                setSelect((row * 12) + col + 1);
                                            }
                                            }>
                                                <Typography
                                                    className="typography"
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
                                    <div className="">
                                        <Button
                                            className="btn"
                                            variant="contained"
                                            color="primary"
                                            onClick={buy}
                                            disabled={isLoading}
                                            style={{
                                                width: "150px",
                                                borderRadius: "10px",
                                                boxShadow: "0 0 10px rgba(0, 0, 0, 0.9)",
                                            }}
                                        >
                                            {
                                                isLoading ? <LoadingBar/> : null
                                            }
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