import React from "react";
import {
  Routes,
  Route,
  useNavigate,
} from "react-router-dom";
import Navbar from "./components/Navbar";
import Profile from "./components/Profile";
import Login from "./components/Login";
import { useState } from "react";
import * as api from "./utils/api";

function App() {
  const navigate = useNavigate();

  const [loggedIn, setLoggedIn] = React.useState(false);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleEmailChange = (email) => {
    setEmail(email);
  };

  const handlePasswordChange = (passwordValue) => {
    setPassword(passwordValue);
  };

  function handleLogin() {
    api.login(email, password);
    setLoggedIn(true);
    navigate("/profile");
  }

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("validDue");
    localStorage.removeItem("username");
    navigate("/login", { replace: true });
  }

  return (
    <div>
      <Navbar loggedIn={loggedIn} handleLogout={handleLogout} />
      <Routes>
        {/*<Route path="/" element={<Schedule />} />
          <Route path="/films" element={<Films />} />*/}
        <Route path="/profile" element={<Profile email={email} />} />
        <Route
          path="/login"
          element={
            <Login
              handleEmailChange={handleEmailChange}
              handlePasswordChange={handlePasswordChange}
              handleLogin={handleLogin}
            />
          }
        />
      </Routes>
    </div>
  );
}

export default App;
