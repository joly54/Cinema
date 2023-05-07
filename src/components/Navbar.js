import React from 'react';
import {Link, useNavigate} from 'react-router-dom';
import './Styles/Navbar.css';
function Navbar({loggedIn, handleLogout}) {
    const navigate = useNavigate();

    return (
        <nav>
            <ul>
                <li>
                    {loggedIn ? (
                        <Link to="/profile">My Profile</Link>
                    ) : (
                        <div></div>
                    )}

                </li>
                <li>
                    <Link to="/films">Films</Link>
                </li>
                <li>
                    <Link to="/">Schedule</Link>
                </li>
                <li>
                    {loggedIn ? (
                        <Link to="/login" onClick={handleLogout}>
                            Log out
                        </Link>
                    ) : (
                        <Link to="/login">Log in</Link>
                    )}
                </li>
                <li>
                    {!loggedIn ? (
                        <Link to="/register">Register</Link>
                    ) : (
                        <div></div>
                    )}
                </li>
            </ul>
        </nav>
    );
}

export default Navbar;
