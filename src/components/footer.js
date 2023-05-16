import { Avatar, Grid, Typography } from "@material-ui/core";
import React from "react";
import "./Styles/footer.css"
import GitHubIcon from '@mui/icons-material/GitHub';
import TelegramIcon from '@mui/icons-material/Telegram';
import EmailIcon from '@mui/icons-material/Email';
import {Link} from "react-router-dom";
function Footer() {
    return (
        <div className="footer">
            <Grid container spacing={0}>
                <Grid item xs={12} sm={6} md={6} lg={4} className="column"
                style={{
                    //center
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    justifyContent: "center",

                }}
                >
                    <div className="author"
                    style={{
                        display: "flex",
                        flexDirection: "row",
                        alignItems: "center",
                        justifyContent: "center",
                        gap: "1rem",
                    }}
                    >
                        <Avatar
                            src="https://avatars.githubusercontent.com/u/37771218?s=400&u=f0b7ff749b366656907f79568918d19d231da896&v=4"
                            alt="Logo"
                            className="authorImage"
                        />
                        <Grid
                        xs={12}
                        lg={12}

                            style={{
                                display: "flex",
                                flexDirection: "column",
                                alignItems: "flex-start",
                                justifyContent: "center",
                                paddingLeft: "1rem",
                            }}
                        >
                            <Typography
                                style={{
                                    fontSize: "1.5rem",
                                    fontFamily: "Montserrat",
                                    fontWeight: "bold",
                                }}
                                variant="subtitle1">Perepeluk Danilo</Typography>
                            <Typography
                                style={{
                                    fontFamily: "Montserrat",
                                    fontWeight: "bold",
                                }}
                                variant="body2">Backend & Frontend developer</Typography>
                            <Typography
                                style={{
                                    fontFamily: "Montserrat",
                                    fontWeight: "bold",
                                }}
                                variant="body2">Backend - python & flask</Typography>
                            <Typography
                                style={{
                                    fontFamily: "Montserrat",
                                    fontWeight: "bold",
                                }}
                                variant="body2">Frontend - react & material-ui</Typography>
                            <Grid
                            xs={6}
                            lg={6}
                            style={{
                                display: "flex",
                                flexDirection: "row",
                                gap: "1rem",
                                paddingTop: "1rem",
                                justifyContent: "space-between",
                                width: "100%",
                                alignItems: "center",

                            }}
                            >
                               <Link
                                   className={"link"}
                                   to={"https://github.com/joly54"}
                                   //open in new tab
                                      target={"_blank"}
                               style={{
                                      color: "white",
                                      textDecoration: "none",
                               }}
                               >
                                      <GitHubIcon/>
                               </Link>
                                <Link
                                    className={"link"}
                                    to={"https://t.me/joly541"}
                                    target={"_blank"}
                                    style={{
                                        color: "white",
                                        textDecoration: "none",
                                    }}>
                                    <TelegramIcon/>
                                </Link>
                                <Link
                                    className={"link"}
                                    to={"mailto:perepelukdanilo@gmail.com"}
                                    target={"_blank"}
                                    style={{
                                        color: "white",
                                        textDecoration: "none",
                                    }}>
                                    <EmailIcon/>
                                </Link>
                            </Grid>
                        </Grid>

                    </div>
                </Grid>

                {/*---------------------Space for faggots-------------------*/}

                <Grid item xs={12} sm={4} className="column">
                    <div className="author">
                        <img
                            src="/author3.jpg"
                            alt="Author 3"
                            className="authorImage circular"
                        />
                        <Typography variant="subtitle1">Author 3</Typography>
                        <Typography variant="body2">Author 3 bio goes here</Typography>
                    </div>
                </Grid>

                <Grid item xs={12} sm={6} md={6} lg={4} className="column"
                      style={{
                          //center
                          display: "flex",
                          flexDirection: "column",
                          alignItems: "center",
                          justifyContent: "center",

                      }}
                >
                    <div className="author"
                         style={{
                             display: "flex",
                             flexDirection: "row",
                             alignItems: "center",
                             justifyContent: "center",
                             gap: "1rem",
                         }}
                    >
                        <Avatar
                            src="https://avatars.githubusercontent.com/u/129663889?s=400&u=e9dedc0f9c4eaebda61dd75357696073004aaa1a&v=4"
                            alt="Logo"
                            className="authorImage"
                        />
                        <Grid
                            xs={12}
                            lg={12}

                            style={{
                                display: "flex",
                                flexDirection: "column",
                                alignItems: "flex-start",
                                justifyContent: "center",
                                paddingLeft: "1rem",
                            }}
                        >
                            <Typography
                                style={{
                                    fontSize: "1.5rem",
                                    fontFamily: "Montserrat",
                                    fontWeight: "bold",
                                }}
                                variant="subtitle1">DMITRIY KUZMIK</Typography>
                            <Typography
                                style={{
                                    fontFamily: "Montserrat",
                                    fontWeight: "bold",
                                }}
                                variant="body2">Frontend developer</Typography>
                            <Typography
                                style={{
                                    fontFamily: "Montserrat",
                                    fontWeight: "bold",
                                }}
                                variant="body2">Frontend - HTML/CSS & JS</Typography>
                            <Typography
                                style={{
                                    fontFamily: "Montserrat",
                                    fontWeight: "bold",
                                }}
                                variant="body2">Moral and Mental support :)</Typography>
                            <Grid
                                xs={6}
                                lg={6}
                                style={{
                                    display: "flex",
                                    flexDirection: "row",
                                    gap: "1rem",
                                    paddingTop: "1rem",
                                    justifyContent: "space-between",
                                    width: "100%",
                                    alignItems: "center",

                                }}
                            >
                                <Link
                                    className={"link"}
                                    to={"https://github.com/31CRIMSON"}
                                    target={"_blank"}
                                    style={{
                                        color: "white",
                                        textDecoration: "none",
                                    }}
                                >
                                    <GitHubIcon/>
                                </Link>
                                <Link
                                    className={"link"}
                                    to={"https://t.me/CRIMSON31"}
                                    target={"_blank"}
                                    style={{
                                        color: "white",
                                        textDecoration: "none",
                                    }}>
                                    <TelegramIcon/>
                                </Link>
                                <Link
                                    className={"link"}
                                    to={"mailto:dmitriy.kuzzmik@gmail.com"}
                                    target={"_blank"}
                                    style={{
                                        color: "white",
                                        textDecoration: "none",
                                    }}>
                                    <EmailIcon/>
                                </Link>
                            </Grid>
                        </Grid>

                    </div>
                </Grid>



            </Grid>
        </div>
    );
}

export default Footer;
