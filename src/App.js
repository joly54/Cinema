import {Routes, Route, useNavigate} from 'react-router-dom';
import Navbar from './components/Navbar';
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

function App() {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isLogin, setIsLogin] = useState(false);
    let validDue = localStorage.getItem('validDue');
    //alert(validDue)
    useEffect(() =>{
        if (validDue) {
            let now = new Date();
            let validDueDate = new Date(validDue);
            if (now > validDueDate) {
                localStorage.removeItem('token');
                localStorage.removeItem('username');
                localStorage.removeItem('validDue');
                setIsLogin(false);
                navigate('/login');
            } else {
                setIsLogin(true);
            }
        } else {
            setIsLogin(false);
        }
    }, [navigate, validDue])
    function handleChangeUsername(value){
        setUsername(value);
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
  return (
      <div>
          <ToastContainer />
          <Navbar loggedIn={isLogin} handleLogout={handleLogout}/>
        <Routes>
            <Route path="/" element={<Schedule />} />
            <Route path="/films" element={<Films />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/login" element={<Login handleChangeUsername={handleChangeUsername} handleChangePassword={handleChangePassword} handleLogin={handleLogin}/>} />
            <Route path="/register"  element={<Register handleRegister={handleRegister} handleChangeUsername={handleChangeUsername} handleChangePassword={handleChangePassword} />}/>
            <Route path="/forgot-password" element={<ForgotPassword handleChangeUsername={handleChangeUsername} ResetPassword={ResetPassword} />} />
        </Routes>
      </div>
  );
}

export default App;
