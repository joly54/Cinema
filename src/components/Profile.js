import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast, ToastContainer } from 'react-toastify';
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
    Slide,
    Typography
} from '@material-ui/core';
import BackToTopButton from './BackToTopButton';
import * as api from '../utils/Api';
import { baseurl } from '../utils/Api';
import 'react-toastify/dist/ReactToastify.css';
import './Styles/Profile.css';
import './Styles/scrollBar.css';

const Transition = React.forwardRef(function Transition(props, ref) {
    return <Slide direction="up" ref={ref} {...props} />;
});

function Profile() {
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
                console.log(response);
                if (response.ok) {
                    response.json().then((data) => {
                        console.log(data);
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
        fetch(baseurl + `/resendEmailValidationCode?username=${email}`)
            .then((response) => {
                if (response.status === 200) {
                    toast.success('Email was sent!');
                } else {
                    toast.error('Error sending email.');
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
                    <button className="btn-confirm" onClick={confirmEmail}>
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
                            width: '100%', // Используйте фиксированную ширину вместо minWidth
                            display: 'flex',
                            justifyContent: 'center',
                        }}
                    >
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
