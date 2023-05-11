import {Routes, Route, useNavigate} from 'react-router-dom';
import Header from './components/Navbar';
import Profile from './components/Profile';
import Films from './components/Films';
import Schedule from './components/Schedule';
import Login from "./components/Login";
import {toast, ToastContainer} from "react-toastify";
import React, {useEffect, useState} from "react";
import * as api from "./utils/Api";
import 'react-toastify/dist/ReactToastify.css';
import Register from "./components/Register";
import ForgotPassword from "./components/ForgotPassword";
import { createTheme, ThemeProvider } from '@material-ui/core/styles';
import SesInfo from "./components/SesInfo";
import "../src/components/Styles/App.css";
import Cookies from 'js-cookie';
import Payment from "./components/Payment"

function App() {
    useEffect(() => {
        Cookies.set('cookieName', 'cookieValue', { sameSite: 'none', secure: "Lax" });
    }, []);
    const theme = createTheme({
        palette: {
            primary: {
                main: '#56376B',
            },
        },
    });
    document.cookie = 'cookieName=cookieValue; SameSite=Lax';
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isLogin, setIsLogin] = useState(false);
    const [sessionId, setsession] = useState(null);
    let validDue = localStorage.getItem('validDue');
    useEffect(() =>{
        if (validDue) {
            let now = new Date()/1000
            if (now > validDue) {
                localStorage.removeItem('token');
                localStorage.removeItem('username');
                localStorage.removeItem('validDue');
                setIsLogin(false);
                navigate('/login');
            }
            api.checktoken(localStorage.getItem("username"), localStorage.getItem("token"))
                .then((res) => {
                    res.json().then(data => {
                            console.log(data);
                            if (res.ok) {
                                setIsLogin(true);
                            } else{
                                localStorage.removeItem('token');
                                localStorage.removeItem('username');
                                localStorage.removeItem('validDue');
                                setIsLogin(false);
                                toast("Your session expired, please login again", {
                                    position: "top-center",
                                    autoClose: 5000,
                                    hideProgressBar: false,
                                    closeOnClick: true,
                                    pauseOnHover: false,
                                    draggable: true
                                })
                                navigate('/login');
                            }
                        }

                    )})
        } else {
            setIsLogin(false);
        }
    }, [navigate, validDue])
    function handleChangeUsername(value){
        setUsername(value);
        console.log(username);
    }
    function handleChangePassword(value){
        setPassword(value);
    }
    function handleLogin(){
        api.login(
            username,
            password
        ).then(
            (res) => {
                res.json().then(data => {
                    console.log(data);
                    if (res.ok) {
                        setIsLogin(true);
                        localStorage.setItem('token', data['token']);
                        localStorage.setItem('username', username);
                        localStorage.setItem('validDue', data['validDue']);
                        toast.success(data['message'], {
                            position: "top-center",
                            autoClose: 5000,
                            hideProgressBar: false,
                            closeOnClick: true,
                            pauseOnHover: false,
                            draggable: true
                        })
                        navigate('/profile');
                    } else{
                        toast.error(data['message'], {
                            position: "top-center",
                            autoClose: 5000,
                            hideProgressBar: false,
                            closeOnClick: true,
                            pauseOnHover: false,
                            draggable: true
                        })
                    }
            }
                )}
        ).catch(
            (err) => {
                console.log(err)
            }
        )
    }

    function handleRegister(){
        api.register(
            username,
            password
        ).then(
            (res) => {
                res.json().then(data =>{
                        console.log(data);
                        if(res.ok){
                            setIsLogin(true);
                            localStorage.setItem('token', data['token']);
                            localStorage.setItem('username', username);
                            localStorage.setItem('validDue', data['validDue']);
                            toast.success(data['message'], {
                                position: "top-center",
                                autoClose: 5000,
                                hideProgressBar: false,
                                closeOnClick: true,
                                pauseOnHover: false,
                                draggable: true
                            })
                            navigate('/profile');
                        }else {
                            toast.error(data['message'], {
                                position: "top-center",
                                autoClose: 5000,
                                hideProgressBar: false,
                                closeOnClick: true,
                                pauseOnHover: false,
                                draggable: true
                            })
                        }
                    }
                )
            }
        )

    }
    function ResetPassword(){
        document.getElementById("code").removeAttribute("disabled");
        toast.success("Please check your email for the code", {
            position: "top-center",
            autoClose: 5000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: false,
            draggable: true
        })
    }

    function handleLogout(){
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        localStorage.removeItem('validDue');
        setIsLogin(false);
        navigate('/login');
    }
    function handleSession(ses_id){
        setsession(ses_id);
        navigate('/sessionInfo');
    }
  return (
      <ThemeProvider theme={theme}>
      <div className="BackGroundColor">
          <ToastContainer />
          <Header loggedIn={isLogin} handleLogout={handleLogout}/>
        <Routes>
            <Route path="/" element={<Schedule handleFilm={handleSession} />} />
            <Route path="/films" element={<Films />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/login" element={<Login handleChangeUsername={handleChangeUsername} handleChangePassword={handleChangePassword} handleLogin={handleLogin}/>} />
            <Route path="/register"  element={<Register handleRegister={handleRegister} handleChangeUsername={handleChangeUsername} handleChangePassword={handleChangePassword} />}/>
            <Route path="/forgot-password" element={<ForgotPassword handleChangeUsername={handleChangeUsername} ResetPassword={ResetPassword} />} />
            <Route path="/sessionInfo" element={<SesInfo ses_id={sessionId} />} />
            <Route path="/payment" element={<Payment/>} />
        </Routes>
      </div>
      </ThemeProvider>
  );
}

export default App;
