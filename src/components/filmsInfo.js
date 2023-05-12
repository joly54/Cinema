import React, {useEffect} from "react";
import {Grid} from "@material-ui/core";
import * as api from "../utils/Api";
import {toast} from "react-toastify";
import {useNavigate} from "react-router-dom";

function FilmsInfo(){
    //get current url
    const film_id = window.location.pathname.split("/")[2];
    const [data, setData] = React.useState(null);
    const [sessions, setSessions] = React.useState(null);
    //const navigate = useNavigate();
    useEffect(() => {
        api.getSessions(film_id)
            .then(res => {
                if (res.ok) {
                    res.json().then(data => {
                        console.log(data);
                        setData(data);
                        setSessions(data["sessions"]);
                    });
                } else {
                    res.json().then(data => {
                        console.error(data);
                        toast.error(data["message"]);
                        //navigate("/")
                    });
                }
            });
    }, []);
    return(
        <Grid
            style={{
                width: "100%",
                height: "100vh",
                backgroundColor:  "#5C0099",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                flexDirection: "column"
            }}
        >
            {data && sessions ?
                <Grid
                    className="Info"
                    style={{
                        maxWidth: "100%",
                        borderRadius: "20px",
                        display: "flex",
                        justifyContent: "space-around",
                        //make it in top
                        alignItems: "flex-start",
                        flexDirection: "row",

                    }}
                >
                    <img
                        style={{
                            width: "50%",
                            objectFit: "cover"
                        }}
                        src={data["poster"]}
                    />
                </Grid>
                :
                <p>Loading</p>
            }
        </Grid>
    )
}
export default FilmsInfo;