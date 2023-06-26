import React, {useEffect, useState} from 'react';
import {useNavigate} from 'react-router-dom';
import {toast, ToastContainer} from 'react-toastify';
import {
    Button,
    Card,
    CardContent,
    CircularProgress,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    Grid,
    Slide
} from '@material-ui/core';
import BackToTopButton from './BackToTopButton';
import * as api from '../utils/Api';
import {baseurl} from '../utils/Api';
import 'react-toastify/dist/ReactToastify.css';
import './Styles/Profile.css';
import './Styles/scrollBar.css';
import LoadingBar from "./Progress.js";


const Transition = React.forwardRef(function Transition(props, ref) {
    return <Slide direction="up" ref={ref} {...props} />;
});

function Profile() {
    const [isEmailLoading, setIsEmailLoading] = useState(false);
    document.title = 'Profile';
    const [loading, setLoading] = useState(true);
    const [open, setOpen] = React.useState(false);
    const [ticket, setTicket] = React.useState({});
    const handleClose = () => {
        setOpen(false);
    };
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [status, setStatus] = useState('');
    const [tickets, setTickets] = useState([]);
    const token = localStorage.getItem('token');

    useEffect(() => {
        api.userInfo(email, token)
            .then((response) => {
                if (response.ok) {
                    response.json().then((data) => {
                        setStatus(data['isEmailConfirmed']);
                        setEmail(data['username']);
                        data['tikets'].sort((a, b) => {
                            return new Date(a.date) - new Date(b.date);
                        });
                        setTickets(data['tikets']);
                    });
                } else {
                    navigate('/login', { replace: true });
                }
            });
    }, [email, navigate, token]);

    function confirmEmail() {
        setIsEmailLoading(true);
        fetch(baseurl + `/resendEmailValidationCode?username=${email}`)
            .then((response) => {
                setTimeout(
                    function () {
                        setIsEmailLoading(false);
                    },
                    3000
                )
                if (response.status === 200) {
                    toast.success('Email was sent!',{
                        position: "top-center",
                        autoClose: 5000,
                        hideProgressBar: false,
                        closeOnClick: true,
                        pauseOnHover: false,
                        pauseOnFocusLoss: false,
                        theme: "colored",
                        draggable: true
                    });
                } else {
                    toast.error('Error sending email.',{
                        position: "top-center",
                        autoClose: 5000,
                        hideProgressBar: false,
                        closeOnClick: true,
                        pauseOnHover: false,
                        pauseOnFocusLoss: false,
                        theme: "colored",
                        draggable: true
                    });
                }
            })
            .catch((error) => {
                toast.error('Error sending email.' + error);
            });
    }

    return (
        <div className="div-div-container" style={{ minHeight: '100vh',
        }}>
            <div className="profile-header">
                <h2>{email}</h2>
                <h3>My Tickets</h3>
                {status === false ? (
                        <button
                            style={{
                                display: 'flex',
                                flexDirection: 'row',
                                justifyContent: 'center',
                                alignItems: 'center',
                            }}
                            disabled={isEmailLoading}
                            className="btn-confirm" onClick={confirmEmail}>
                            {isEmailLoading ? (
                                <LoadingBar />
                            ) : null}
                            Confirm email
                        </button>
                ) : null}
            </div>
            <div
                className="profile-container"
                style={{
                    minWidth: '300px'
                }}
            >
                <BackToTopButton />
                <ToastContainer />
                <div className="profile-content">
                    <Grid
                        container
                        spacing={2}
                        style={{
                            width: '100%',
                            display: 'flex',
                            justifyContent: 'center',
                        }}
                    >
                        {
                            tickets.length === 0 ? (
                                <div
                                    style={{
                                        display: 'flex',
                                        flexDirection: 'column',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        height: '100%',
                                    }}
                                >
                                    <h2>You don't have any tickets yet.</h2>
                                    <Button
                                        variant="contained"
                                        color="primary"
                                        style={{
                                            marginTop: '20px',
                                            borderRadius: '10px',
                                            color: 'white',
                                            fontWeight: 'bold',
                                            padding: '10px 20px',
                                        }}
                                        onClick={() => {
                                            navigate('/', { replace: true });
                                        }}
                                    >
                                        Buy tickets
                                    </Button>
                                </div>
                            ) : null
                        }
                        {tickets.map((ticket) => (
                            <Grid
                                item
                                key={ticket.id}
                                xs={12}
                                sm={6}
                                md={4}
                                lg={2}
                                style={{
                                    minWidth: '300px',
                                    marginLeft: '5px',
                                    marginRight: '5px'
                                }}
                            >
                                <Card
                                    className={"ticket-card"}
                                    style={{
                                        borderRadius: '1.5rem',
                                        display: 'flex',
                                        flexDirection: 'column',
                                        cursor: "pointer",
                                        minWidth: '300px',
                                        backgroundColor: ticket.checked ? 'rgb(220 252 231)' : 'white'
                                    }}
                                    onClick={() => {
                                        const prevsrc = document.getElementById('qr-code').src;
                                        if (prevsrc !== ticket.urltoqr) {
                                            document.getElementById('qr-code').src = 'fdsfadf';
                                            document.getElementById('qr-code').src = ticket.urltoqr;
                                            setLoading(true);
                                        } else {
                                            setLoading(false);
                                        }
                                        setTicket(ticket);
                                        setOpen(true);
                                    }}
                                >
                                    <CardContent
                                        style={{
                                            display: 'flex',
                                            flexDirection: 'column',
                                            height: '100%',
                                        }}
                                    >
                                        <h4>{ticket.title}</h4>
                                        <p>Time: {ticket.time}</p>
                                        <p>Date: {ticket.date}</p>
                                        <Button
                                            variant="contained"
                                            color="primary"
                                            onClick={() => {
                                                const prevsrc = document.getElementById('qr-code').src;
                                                if (prevsrc !== ticket.urltoqr) {
                                                    document.getElementById('qr-code').src = 'fdsfadf';
                                                    document.getElementById('qr-code').src = ticket.urltoqr;
                                                    setLoading(true);
                                                } else {
                                                    setLoading(false);
                                                }
                                                setTicket(ticket);
                                                setOpen(true);
                                            }}
                                            style={{
                                                borderRadius: '0.5rem',
                                                textDecoration: 'none',
                                                color: 'white',
                                                fontWeight: 'semi-bold',
                                            }}
                                        >
                                            {ticket.checked ? 'TICKET ALREDY USED' : 'ADDITIONAL INFO'}
                                        </Button>
                                    </CardContent>
                                </Card>
                            </Grid>
                        ))}
                    </Grid>
                </div>
            </div>
            <Dialog
                open={open}
                TransitionComponent={Transition}
                keepMounted
                onClose={handleClose}
                aria-describedby="alert-dialog-slide-description"
            >
                <DialogTitle>{"Your qr code"}</DialogTitle>
                <DialogContent>
                    <DialogContentText id="alert-dialog-slide-description">
                        <p style={{
                            textAlign: 'center'
                        }}>Seat{
                            ticket.seats ? ticket.seats.length > 1 ? 's' : null : null
                        }: {ticket.seats ? ticket.seats.join(', ') : null
                        }</p>
                        <h1 style={{
                            textAlign: 'center'
                        }}>Your QR-code</h1>
                    </DialogContentText>
                    <img
                        id="qr-code"
                        src={ticket.urltoqr}
                        onLoad={() => {
                            setTimeout(() => {
                                setLoading(false);
                            }, 500);
                        }}
                        alt="qr code"
                        style={{
                            maxWidth: '100%',
                            maxHeight: '100%',
                            objectFit: 'contain',
                            margin: 'auto',
                            display: 'block',
                            marginTop: '10px',
                        }}
                    />
                    {loading ? (
                        <div
                            style={{
                                display: 'flex',
                                justifyContent: 'center',
                                alignItems: 'center',
                                height: '100%',
                                width: '100%',
                                position: 'absolute',
                                top: '0',
                                left: '0',
                                backgroundColor: 'white',
                                zIndex: '100',
                            }}
                        >
                            <CircularProgress color="secondary" />
                        </div>
                    ) : null}
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose}>Okay</Button>
                </DialogActions>
            </Dialog>
        </div>
    );
}

export default Profile;
