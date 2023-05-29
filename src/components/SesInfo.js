import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast, ToastContainer } from "react-toastify";
import { Button, Grid, Typography } from "@material-ui/core";
import BackToTopButton from "./BackToTopButton";
import * as api from "../utils/Api";
import "./Styles/SesInfo.css";
import "./Styles/scrollBar.css";
import "./Styles/preloader.css";
import Preloader from "./preloader";

function SesInfo({ handlePayData }) {
  // get current url
  const session =
    window.location.href.split("/")[window.location.href.split("/").length - 1];
  const navigate = useNavigate();
  const [sessionInfo, setSessionInfo] = useState([]);
  const [aviSeats, setAviSeats] = useState([]);
  const [selected, setSelected] = useState([]);
  const username = localStorage.getItem("username");
  const token = localStorage.getItem("token");

  useEffect(() => {
    if (!username || !token) {
      toast.error("You are not logged in.", {
        position: "top-center",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: false,
        draggable: true,
      });
      // remove from history
      window.history.replaceState(null, null, "/Cinema");
      navigate("/login");
      return;
    } else {
      api
        .checktoken(username, token)
        .then((res) => {
          if (res.ok) {
            res.json().then((data) => {
              console.log(data);
            });
          } else {
            res.json().then((data) => {
              console.error(data);
              toast.error("Your session has expired. Please log in again.", {
                position: "top-center",
                autoClose: 5000,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: false,
                pauseOnFocusLoss: false,
                theme: "colored",
                draggable: true,
              });
              window.history.replaceState(null, null, "/Cinema");
              navigate("/login");
              return;
            });
          }
        })
        .catch((error) => {
          console.error(error);
          toast.error("Oops! Something went wrong.", {
            position: "top-center",
            autoClose: 5000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: false,
            pauseOnFocusLoss: false,
            theme: "colored",
            draggable: true,
          });

          navigate("/");
        });
    }

    api
      .getSessionInfo(session)
      .then((res) => {
        if (res.ok) {
          res.json().then((data) => {
            console.log(data);
            setSessionInfo(data);
            setAviSeats(data["seats"]);
            document.title =
              data["title"] +
              " - " +
              data["date"] +
              " " +
              data["time"] +
              " " +
              data["price"] +
              "UAH";
          });
        } else {
          res.json().then((data) => {
            console.error(data);
            navigate("/");
          });
        }
      })
      .catch((error) => {
        console.error(error);
        toast.error("Failed to get session info.", {
          position: "top-center",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: false,
          pauseOnFocusLoss: false,
          theme: "colored",
         draggable: true,
        });

        navigate("/");
      });
  }, [session, navigate, token, username]);

  const handleSeatSelection = (seatNumber) => {
    if (selected.includes(seatNumber)) {
      setSelected(selected.filter((seat) => seat !== seatNumber));
    } else {
      setSelected([...selected, seatNumber]);
    }
  };

  const handlePayment = () => {
    if (selected.length === 0) {
      toast.error("Please select at least one seat.", {
        position: "top-center",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: false,
        draggable: true,
      });
    } else {
      handlePayData(sessionInfo, selected);
      navigate("/payment");
    }
  };

  return (
    <div className="container">
      <Typography variant="h4" className="session-info-header">
        Session Information
      </Typography>

      {sessionInfo.length === 0 ? (
        <Preloader />
      ) : (
        <Grid container spacing={2} className="session-info-grid">
          <Grid item xs={12}>
            <Typography variant="h6">{sessionInfo.title}</Typography>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="body1">
              Date: {sessionInfo.date}
            </Typography>
            <Typography variant="body1">
              Time: {sessionInfo.time}
            </Typography>
            <Typography variant="body1">
              Price: {sessionInfo.price} UAH
            </Typography>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="h6">Available Seats</Typography>
          </Grid>
          <Grid item xs={12}>
            <div className="scrollable-container">
              <div className="scrollable-content">
                {aviSeats.map((seat) => (
                  <Button
                    key={seat}
                    variant="contained"
                    className={
                      selected.includes(seat)
                        ? "selected-seat-button"
                        : "seat-button"
                    }
                    onClick={() => handleSeatSelection(seat)}
                  >
                    {seat}
                  </Button>
                ))}
              </div>
            </div>
          </Grid>
          <Grid item xs={12} className="session-info-footer">
            <Button
              variant="contained"
              color="primary"
              onClick={handlePayment}
            >
              Proceed to Payment
            </Button>
          </Grid>
        </Grid>
      )}

      <ToastContainer />

      <BackToTopButton />
    </div>
  );
}

export default SesInfo;

