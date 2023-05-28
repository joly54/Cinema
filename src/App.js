import React, {useEffect, useState} from "react";
import {Routes, Route, useNavigate} from 'react-router-dom';
import {toast, ToastContainer} from "react-toastify";
import { createTheme, ThemeProvider } from '@material-ui/core/styles';
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
import Cookies from 'js-cookie';
import * as api from "./utils/Api";
import 'react-toastify/dist/ReactToastify.css';
import "../src/components/Styles/App.css";
import bcrypt from 'bcryptjs'
import Footer from "./components/footer";
import NotFound from "./components/404";
import fav from "./components/img/fav.jpg";
import md5 from "md5";
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
    const [PayData, setPayData] = useState({});
    let validDue = localStorage.getItem('validDue');
    const [addition, setAddition] = useState([]);
    const md5 = require('md5');

    function handleToastErr(text){
        toast.error(text, {
            position: "top-center",
            autoClose: 5000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: false,
            draggable: true
        });
    }

    function handleToastSuc(text){
        toast.success(text, {
            position: "top-center",
            autoClose: 5000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: false,
            draggable: true
        });
    }

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
                                if(data['additional'] !== undefined){
                                    setAddition(data['additional']);
                                }
                                console.log(addition);
                            } else{
                                localStorage.removeItem('token');
                                localStorage.removeItem('username');
                                localStorage.removeItem('validDue');
                                setIsLogin(false);
                                handleToastErr("Your session expired, please login again");
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
        //hash using bcrypt
        const pass = md5(password)
        console.log(pass);
        // console.log(username);
        api.login(
            username,
            pass
        ).then(
            (res) => {
                res.json().then(data => {
                        console.log(data);
                        if (res.ok) {
                            setIsLogin(true);
                            localStorage.setItem('token', data['token']);
                            localStorage.setItem('username', username);
                            localStorage.setItem('validDue', data['validDue']);
                            handleToastSuc(data['message'])
                            console.log(navigate)
                            navigate("/profile");
                        } else{
                            handleToastErr(data['message'])
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
        //hash using bcrypt
        const pass = md5(password)
        api.register(
            username,
            pass
        ).then(
            (res) => {
                res.json().then(data =>{
                        console.log(data);
                        if(res.ok){
                            setIsLogin(true);
                            localStorage.setItem('token', data['token']);
                            localStorage.setItem('username', username);
                            localStorage.setItem('validDue', data['validDue']);
                            handleToastSuc(data['message'])
                            navigate('/profile');
                        }else {
                            handleToastErr(data['message'])
                        }
                    }
                )
            }
        )

    }
    function handleLogout(){
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        localStorage.removeItem('validDue');
        setIsLogin(false);
        navigate('/login');
    }
    function handleChangePayData(value){
        setPayData(value)
        navigate("/Payment")
    }
    return (
        <ThemeProvider theme={theme}>
            <div className="BackGroundColor">
                <ToastContainer />
                <Header loggedIn={isLogin} handleLogout={handleLogout} additionals={addition}/>
                <Routes>
                    <Route path="/" element={<Schedule />} />
                    <Route path="/films/:id" element={<FilmsInfo />} />
                    <Route path="/films" element={<Films />} />
                    <Route path="/profile" element={<Profile />} />
                    <Route path="/login" element={<Login handleChangeUsername={handleChangeUsername} handleChangePassword={handleChangePassword} handleLogin={handleLogin}/>} />
                    <Route path="/register"  element={<Register handleRegister={handleRegister} handleChangeUsername={handleChangeUsername} handleChangePassword={handleChangePassword} />}/>
                    <Route path="/forgotPassword" element={<ForgotPassword handleChangeUsername={handleChangeUsername} handleToastErr={handleToastErr} handleToastSuc={handleToastSuc}/>} />
                    <Route path="/sessionInfo/:id" element={<SesInfo ses_id={sessionId} handlePayData={handleChangePayData} />} />
                    <Route path="/Payment" element={<Payment data={PayData}/>} />
                    <Route path="*" element={<NotFound />} />
                </Routes>
                <Footer />
            </div>
        </ThemeProvider>
    );
}
export default App;
