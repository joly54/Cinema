import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Profile.css';
import {useNavigate} from "react-router-dom";

export const baseurl = "https://vincinemaApi.pythonanywhere.com/";
let token = ""

function Profile() {
    const navigate = useNavigate();
    token = localStorage.getItem('token');
    const validDue = localStorage.getItem('validDue');
    if(validDue < Date.now()/1000){
        localStorage.removeItem('token');
        localStorage.removeItem('validDue');
        navigate("/login")
    }
    const [email, setEmail] = useState("");
    const [status, setStatus] = useState("");
    const [tickets, setTickets] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            const result = await axios.get(`${baseurl}userinfo?username=perepelukdanilo@gmail.com&token=${token}`);
            setEmail(result.data.username);
            setStatus(result.data.isEmailConfirmed ? "Email confirmed" : "Email not confirmed");
            setTickets(result.data.tikets);
            console.log(tickets);
        };
        fetchData();
    }, []);

    return (
        <div className="profile-container">
            <div className="profile-header">
                <h2>{email}</h2>
                <p>{status}</p>
            </div>
            <div className="profile-content">
                <h3>My Tickets</h3>
                {tickets && tickets.map((ticket) => (
                    <div key={ticket.id}>
                        <p>Title: {ticket["title"]}</p>
                        <p>Date: {ticket['date']}</p>
                        <p>Time: {ticket['time']}</p>
                        <p>Number: {ticket['number']}</p>
                        <button className="btn" onClick={() => window.open(ticket["urltoqr"])}>Get qr code</button>
                    </div>
                ))}

            </div>
        </div>
    );
}

export default Profile;
