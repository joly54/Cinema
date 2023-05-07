import React, { useState, useEffect } from 'react';
import './Styles/Profile.css';
import { useNavigate } from "react-router-dom";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import * as api from '../utils/Api';
import './Styles/scrollBar.css';
import BackToTopButton from "./BackToTopButton";
export const baseurl = "https://vincinemaApi.pythonanywhere.com";

function Profile() {
    const navigate = useNavigate()
    const [email] = useState(localStorage.getItem('username') === null ? "null" : localStorage.getItem('username'));
    const [status, setStatus] = useState("");
    const [tickets, setTickets] = useState([]);
    const token = localStorage.getItem('token');

    useEffect(() => {
        api.userInfo(email, token)
            .then((response) => {
                console.log(response)
                if (response.ok) {
                    response.json()
                        .then(data => {
                            console.log(data);
                            setStatus(data["isEmailConfirmed"]);
                            //alert(data["isEmailConfirmed"]);
                            setTickets(data["tikets"]);
                        })
                } else {
                    navigate('/login', { replace: true })

                }
            })

    }, [email, navigate, token])
    function confirmEmail() {
        fetch(baseurl + `/resendEmailValidationCode?username=${email}`)
            .then((response) => {
                if (response.status === 200) {
                    toast.success("Email was sent!");
                } else {
                    toast.error("Error sending email.");
                }
            })
            .catch((error) => {
                toast.error("Error sending email." + error);
            });
    }

    return (
        <div className="profile-container">
            <ToastContainer/>
            <div className="profile-header">
                <h2>{email}</h2>
                {status === false ? (
                    <button className="btn" onClick={confirmEmail}>
                        Confirm email
                    </button>
                ) : null}
            </div>
            <div className="profile-content">
                <h3>My Tickets</h3>
                {tickets &&
                    tickets.map((ticket) => (
                        <div key={ticket.id}>
                            <p>Title: {ticket["title"]}</p>
                            <p>Date: {ticket["date"]}</p>
                            <p>Time: {ticket["time"]}</p>
                            <p>Number: {ticket["number"]}</p>
                            <button
                                className="btn"
                                onClick={() => window.open(ticket["urltoqr"])}
                            >
                                Get qr code
                            </button>
                        </div>
                    ))}
            </div>
        </div>
    );
}

export default Profile;
