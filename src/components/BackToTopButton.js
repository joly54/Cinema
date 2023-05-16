import React from "react";
import {useEffect, useState} from "react";
import './Styles/BackToTopButton.css';
function BackToTopButton() {
    const [backToTopButton, setBackToTopButton] = useState(false);
    useEffect(() => {
        const handleScroll = () => {
            if (window.scrollY > 2000) {
                setBackToTopButton(true);
            } else {
                setBackToTopButton(false);
            }
        };

        window.addEventListener("scroll", handleScroll);

        return () => {
            window.removeEventListener("scroll", handleScroll);
        };
    }, []);


    const scrollUp = () => {
        window.scrollTo({
            top: 0,
            behavior: "smooth",
        });
    };

    return (
        <div className={`to-top-button ${backToTopButton ? "show" : ""}`}>
            <button onClick={scrollUp}>▲</button>
        </div>
    );
}

export default BackToTopButton;