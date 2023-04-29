import {BrowserRouter as Router, Routes, Route, useNavigate} from 'react-router-dom';
import Navbar from './components/Navbar';
import Profile from './components/Profile';
import Films from './components/Films';
import Schedule from './components/Schedule';
import Login from "./components/Login";
import {toast, ToastContainer} from "react-toastify";
import React, {useState} from "react";
import * as api from "./utils/Api";
import 'react-toastify/dist/ReactToastify.css';

function App() {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isLogin, setIsLogin] = useState(false);
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
                //alert(res.status)
                res.json().then(data => {
                    console.log(data);
                    if (res.ok) {
                        setIsLogin(true);
                        localStorage.setItem('token', data['token']);
                        localStorage.setItem('username', username);
                        localStorage.setItem('validDue', data['validDue']);
                        navigate('/profile');
                    }
            }
                )}
        ).catch(
            (err) => {
                console.log(err);
                //make toast
                //toast.error('Login failed');
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
  return (
      <div>
          <ToastContainer />
          <Navbar loggedIn={isLogin} handleLogout={handleLogout}/>
        <Routes>
          <Route path="/" element={<Schedule />} />
          <Route path="/films" element={<Films />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/login" element={<Login handleChangeUsername={handleChangeUsername} handleChangePassword={handleChangePassword} handleLogin={handleLogin}/>} />
        </Routes>
      </div>
  );
}

export default App;
