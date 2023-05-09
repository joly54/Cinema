import { useEffect, useState } from 'react';
import { Grid, Card, CardActionArea, CardMedia, CardContent, Typography } from '@material-ui/core';
import * as api from '../utils/Api'

import './Styles/Films.css';

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

    return (
        <div className="movies-container">
            <h1 className="movies-title">Movies</h1>

            <Grid container spacing={4}>
                {movies.map((movie) => (
                    <Grid item xs={12} md={6} lg={4} key={movie.id}>
                        <Card className="movie-card">
                            <CardActionArea>
                                <CardMedia
                                    component="img"
                                    image={movie.poster}
                                    title={movie.title}
                                    className="movie-poster"
                                />
                                <CardContent>
                                    <Typography gutterBottom variant="h5" component="h2">
                                        {movie.title}
                                    </Typography>
                                    <Typography variant="body2" color="textSecondary" component="p">
                                        {movie.description}
                                    </Typography>
                                </CardContent>
                            </CardActionArea>
                        </Card>
                    </Grid>
                ))}
            </Grid>
        </div>
    );
}

export default Films;
