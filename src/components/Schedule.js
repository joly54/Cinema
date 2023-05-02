import React, { useState, useEffect } from 'react';
import './Schedule.css'

function CinemaSchedule() {
    const [schedule, setSchedule] = useState(null);

    useEffect(() => {
        async function fetchData() {
            const response = await fetch('http://vincinemaapi.pythonanywhere.com//fullSchedule');
            const data = await response.json();
            setSchedule(data);
        }
        fetchData();
    }, []);

    function handleSelectFilm(date, index) {
        const updatedSchedule = { ...schedule };
        updatedSchedule[date].films.forEach((film, i) => {
            film.selected = i === index;
        });
        setSchedule(updatedSchedule);
    }

    if (!schedule) {
        return <div>Loading...</div>;
    }

    return (
        <div className="Schedule">
            <h1>Cinema Schedule</h1>
            {Object.entries(schedule).map(([date, { films }], index) => (
                <div key={date} className={`row${index % 2 === 0 ? ' even' : ' odd'}`}>
                    <h2>{date}</h2>
                    <div className="movie-list">
                        {films.map((film, index) => (
                            <div
                                key={index}
                                className={`movie${film.selected ? ' selected' : ''}`}
                                onClick={() => handleSelectFilm(date, index)}
                            >
                                <h3>{film.title}</h3>
                                <p>Duration: {film.duration} min</p>
                                <p>Available tickets: {film.aviableTikets.length}</p>
                                <p>Begin time: {film.beginTime}</p>
                            </div>
                        ))}
                    </div>
                </div>
            ))}
        </div>
    );
}

export default CinemaSchedule;
