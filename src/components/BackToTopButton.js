import React from "react";
import {useEffect, useState} from "react";

function BackToTopButton() {
    const [backToTopButton, setBackToTopButton] = useState(false);

    useEffect(()=>{
        window.addEventListener("scroll", ()=>{
            if(window.scrollY > 2000){
                setBackToTopButton(true)
            }else{
                setBackToTopButton(false)
            }
        })
    },[])

    const scrollUp = () =>{
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        })
    }

    return(
        <div>
            {backToTopButton &&
                (<button style={({
                    position: "fixed",
                    bottom: "20px",
                    right: "20px",
                    width: "40px",
                    height: "40px",
                    border: "none",
                    backgroundColor: "#333",
                    color: "white",
                    fontSize: "20px",
                    cursor: "pointer",
                    animation: `${backToTopButton ? "fade-in 0.3s" : ""}`
                })} onClick={scrollUp}
                >▲</button>)}
        </div>
    )

}

export default BackToTopButton;