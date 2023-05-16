import React from 'react';
import {CircularProgress} from "@material-ui/core";
import "./Styles/preloader.css"

function Preloader(){
    return(
        <div
            style={{
                minHeight: "100vh",
                height: "100%",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
            }}
        >
            <div className="spinner"></div>
        </div>
    )
}
export default Preloader;