import React from 'react';
import './Styles/scrollBar.css';
import BackToTopButton from "./BackToTopButton";

function Films() {
    return (
        <div>
            <BackToTopButton />
            <h1>Films</h1>
            <p>Here are some of my favorite films:</p>
            <ul>
                <li>The Godfather</li>
                <li>The Shawshank Redemption</li>
                <li>The Dark Knight</li>
            </ul>
        </div>
    );
}

export default Films;
