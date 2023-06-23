import React, {useEffect, useState} from "react";
import {Route, Routes, useNavigate} from 'react-router-dom';
import {toast, ToastContainer} from "react-toastify";
import {createTheme, ThemeProvider} from '@material-ui/core/styles';
import Header from './components/Navbar';
import Profile from './components/Profile';
import Films from './components/Films';
import Schedule from './components/Schedule';
import Login from "./components/Login";
import Register from "./components/Register";
import ForgotPassword from "./components/ForgotPassword";
import SesInfo from "./components/SesInfo";
import FilmsInfo from "./components/filmsInfo";
import Payment from "./components/Payment"
import * as api from "./utils/Api";
import 'react-toastify/dist/ReactToastify.css';
import "../src/components/Styles/App.css";
import Footer from "./components/footer";
import NotFound from "./components/404";

function App() {
    const theme = createTheme({
        palette: {
            primary: {
                main: '#56376B',
            },
        },
    });
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isLogin, setIsLogin] = useState(true);
    const [sessionId, setsession] = useState(null);
    const [PayData, setPayData] = useState({});
    const [addition, setAddition] = useState([]);
    const md5 = require('md5');

    function handleToastErr(text) {
        toast.error(text, {
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

    function handleToastSuc(text) {
        toast.success(text, {
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

    useEffect(() => {
        api.isAuthenticated()
            .then((res) => {
                if (res.ok) {
                    setIsLogin(true);
                } else {
                    setIsLogin(false);
                    navigate('/login');
                }
            })
            .catch((err) => {
                console.log(err);
            });

        api.get_navbar()
            .then((res) => {
                res.json()
                    .then(data => {
                        console.log(data);
                        if (res.ok) {
                            setAddition(data);
                        } else {
                            handleToastErr(data['message']);
                        }
                    })
            })
            .catch((err) => {
                console.log(err);
            });
    }, []);

    function handleChangeUsername(value) {
        setUsername(value);
        console.log(username);
    }

    function handleChangePassword(value) {
        setPassword(value);
    }

    function handleLogin() {
        //hash using bcrypt
        const pass = md5(password)
        api.login(
            username,
            md5(pass)
        ).then(
            (res) => {
                res.json().then(data => {
                        console.log(data);
                        if (res.ok) {
                            setIsLogin(true);
                            handleToastSuc("Welcome back ")
                            navigate("/profile");
                        } else {
                            handleToastErr(data['message'])
                        }
                    }
                )
            }
        ).catch(
            (err) => {
                console.log(err)
            }
        )
    }

    function handleRegister() {
        //hash using bcrypt
        const pass = md5(password)
        api.register(
            username,
            md5(pass)
        ).then(
            (res) => {
                res.json().then(data => {
                        console.log(data);
                        if (res.ok) {
                            setIsLogin(true);
                            handleToastSuc(data['message'])
                            navigate('/profile');
                        } else {
                            handleToastErr(data['message'])
                        }
                    }
                )
            }
        )

    }

    function handleLogout() {
        api.logout()
            .then((res) => {
                if (res.ok) {
                    setIsLogin(false);
                    navigate('/login');
                } else {
                    handleToastErr("Something went wrong")
                }
            })
            .catch((err) => {
                console.log(err);
            });
    }

    function handleChangePayData(value) {
        setPayData(value)
        navigate("/Payment")
    }

    return (
        <ThemeProvider theme={theme}>
            <div className="BackGroundColor">
                <ToastContainer/>
                <Header loggedIn={isLogin} handleLogout={handleLogout} additionals={addition}/>
                <Routes>
                    <Route path="/" element={<Schedule/>}/>
                    <Route path="/films/:id" element={<FilmsInfo/>}/>
                    <Route path="/films" element={<Films/>}/>
                    <Route path="/profile" element={<Profile/>}/>
                    <Route path="/login" element={<Login handleChangeUsername={handleChangeUsername}
                                                         handleChangePassword={handleChangePassword}
                                                         handleLogin={handleLogin}/>}/>
                    <Route path="/register" element={<Register handleRegister={handleRegister}
                                                               handleChangeUsername={handleChangeUsername}
                                                               handleChangePassword={handleChangePassword}/>}/>
                    <Route path="/forgotPassword" element={<ForgotPassword handleChangeUsername={handleChangeUsername}
                                                                           handleToastErr={handleToastErr}
                                                                           handleToastSuc={handleToastSuc}/>}/>
                    <Route path="/sessionInfo/:id"
                           element={<SesInfo ses_id={sessionId} handlePayData={handleChangePayData}/>}/>
                    <Route path="/Payment" element={<Payment data={PayData}/>}/>
                    <Route path="*" element={<NotFound/>}/>
                </Routes>
                <Footer/>
            </div>
        </ThemeProvider>
    );
}

export default App;
