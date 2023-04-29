import React, { useState, useEffect } from "react";
import axios from "axios";
import "./Profile.css";
import { useNavigate } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { baseurl } from "../utils/api";

function Profile({ email }) {
  const [status, setStatus] = useState("");
  const [tickets, setTickets] = useState([]);

  const navigate = useNavigate();

  const token = localStorage.getItem("token");
  const validDue = localStorage.getItem("validDue");

  useEffect(() => {
      /*ТУТ БУДЕТ ПАДАТЬ ЕБАНАЯ ОШИБКА И РАЗЛОГИН ПОТОМУ ЧТО КАКАЯ ТО ВОНЮЧКА СДЕЛАЛА АСИНХРОННУЮ ФУНКЦИЮ ДЛЯ ЗАЩИЩЕННОГО РОУТА -_-*/
    const fetchData = async () => {
            try {
                const response = await axios.get(`${baseurl}userinfo?username=${email}&token=${token}`);
                setStatus(response.data['isEmailConfirmed'] ? "Email confirmed" : "Email not confirmed");
                setTickets(response.data['tikets']);
                console.log(tickets);
            } catch (error) {
                console.log(error.response.status);
                if (error.response.status !== 200) {
                    localStorage.removeItem('token');
                    localStorage.removeItem('validDue');
                    localStorage.removeItem('email');
                    navigate("/login");
                }
            }
        };
        fetchData();
  }, [navigate]);

  function confirmEmail() {
    fetch(baseurl + `resendEmailValidationCode?username=${email}f`)
      .then((response) => {
        if (response.status === 200) {
          toast.success("Email was sent!"); // add toast notification
        } else {
          toast.error("Error sending email."); // add error toast notification
        }
      })
      .catch((error) => {
        toast.error("Error sending email."); // add error toast notification
      });
  }

  return (
    <div className="profile-container">
      <ToastContainer />
      <div className="profile-header">
        <h2>{email}</h2>
        {/*{status === "Email not confirmed" ? (
                    <button className="btn" onClick={confirmEmail}>
                        Confirm email
                    </button>
                ) : null}*/}
      </div>
      {/*<div className="profile-content">
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
            </div>*/}
    </div>
  );
}

export default Profile;
