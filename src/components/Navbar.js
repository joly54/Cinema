import React from 'react';
import {Link, useNavigate} from 'react-router-dom';
import './Navbar.css';
function Navbar({loggedIn}) {
    const navigate = useNavigate();
    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('validDue');
        localStorage.removeItem('username');
        navigate('/login', { replace: true })

    };

    return (
        <nav>
            <ul>
                <li>
                    <Link to="/profile">My Profile</Link>
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
            </ul>
        </nav>
    );
}

export default Navbar;
