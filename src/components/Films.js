import React, {useEffect, useState} from 'react';
import {Link} from "react-router-dom";
import {Grid, ImageList, ImageListItem, ImageListItemBar, Typography} from "@mui/material";
import * as api from '../utils/Api'
import './Styles/Films.css';
import './Styles/preloader.css';
import Preloader from "./preloader";
import NotFoundImage from './img/404.png';

function Films() {
    useEffect(() => {
        window.scrollTo(0, 0)
    }, [])
    document.title = "Films";
    const [movies, setMovies] = useState([]);
    useEffect(() => {
        api.getFilms()
            .then((response) => response.json())
            .then((data) => {
                setMovies(data);
                document.getElementById("preloader").style.display = "none";
            })
            .catch((error) => {
                console.error(error);
            });
    }, []);
    return (
        <>
            <div className={"preload"} id={"preloader"}>
                <Preloader/>
            </div>
            <div className="movies-container"
                 id={"films"}
                 style={{
                     height: '100%',
                     maxWidth: '100%',
                 }}
            >
                <Grid
                    style={{
                        height: '100%',
                        display: 'flex',
                        flexDirection: 'column',
                        justifyContent: 'center',
                        alignItems: 'center',
                    }}
                >
                    <Typography
                        variant="h2"
                        style={{
                            color: 'white',
                            textAlign: 'center',
                            fontFamily: 'Montserrat',
                            fontSize: '50px',
                            paddingTop: '50px',
                            paddingBottom: '50px',
                        }}>
                        Films
                    </Typography>
                    <ImageList cols={4} rowHeight={500} id="films">
                        {movies.map((item) => (
                            <Link to={`/films/${item.id}`}
                                  style={{
                                      textDecoration: 'none',
                                  }}>
                                <Grid
                                    item
                                    className={"movie"}
                                    lg={12}>
                                    <ImageListItem key={item.poster}
                                                   style={{
                                                       height: '100%',
                                                       width: "100%",
                                                       display: 'flex',
                                                       flexDirection: 'column',
                                                       justifyContent: 'center',
                                                       alignItems: 'center',
                                                       cursor: 'pointer',
                                                   }}>
                                        <img src={item.poster} alt={item.title}
                                             className={"movie-image"}
                                             onError={(e) => {
                                                 e.target.onerror = null;
                                                 e.target.src = NotFoundImage;
                                             }
                                             }
                                             style={{
                                                 height: "300px",
                                                 objectFit: 'cover',
                                                 borderRadius: '10px',
                                             }}/>
                                        <ImageListItemBar
                                            title={item.title}
                                            subtitle={<span>Price: {item.price}UAH</span>}
                                        />
                                    </ImageListItem>

                                </Grid>
                            </Link>
                        ))}
                    </ImageList>
                </Grid>
            </div>
        </>
    );
}
export default Films;