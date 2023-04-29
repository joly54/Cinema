import {BrowserRouter as Router, Routes, Route, useNavigate} from 'react-router-dom';
import Navbar from './components/Navbar';
import Profile from './components/Profile';
import Films from './components/Films';
import Schedule from './components/Schedule';
import Login from "./components/Login";
import {ToastContainer} from "react-toastify";
import React, {useState} from "react";
import * as api from "./utils/Api";

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
        ).then((res) => {
            console.log(res);
            setIsLogin(true);
        }).catch((err) => {
            console.log(err);
        })
    }
  return (
      <div>
          <Navbar loggedIn={isLogin} />
          <ToastContainer />
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
