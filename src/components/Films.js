import {useEffect, useState} from 'react';
import * as api from '../utils/Api'
import './Styles/Films.css';
import {Button, ImageList, ImageListItem, ImageListItemBar, Grid, Typography} from "@mui/material";

function Films() {
    const [movies, setMovies] = useState([]);

    useEffect(() => {
        api.getFilms()
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                setMovies(data);
            })
            .catch((error) => {
                console.error(error);
            });
    }, []);
    const [loaded, setLoading] = useState(false);
    return (
        <div className="movies-container"
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
                <ImageList cols={4} rowHeight={500} id = "films"
                >
                    {movies.map((item) => (
                        <Grid
                            lg={12}
                        >
                            <ImageListItem key={item.poster}
                                           style={{
                                               height: '100%',
                                               width: "100%",
                                               display: 'flex',
                                               flexDirection: 'column',
                                               justifyContent: 'center',
                                               alignItems: 'center',
                                           }}
                            >
                                <img src={item.poster} alt={item.title}
                                     style={{
                                         objectFit: 'cover',
                                         borderRadius: '10px',
                                     }}/>
                                <ImageListItemBar
                                    title={item.title}
                                    subtitle={<span>Price: {item.price}UAH</span>}
                                />
                            </ImageListItem>

                        </Grid>
                    ))}
                </ImageList>
            </Grid>
        </div>
    );
}

export default Films;
