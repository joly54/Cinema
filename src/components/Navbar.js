import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
    const [loggedIn, setLoggedIn] = useState(false);

    useEffect(() => {
        const validDue = localStorage.getItem('validDue');
        if (validDue && validDue >= Date.now() / 1000) {
            setLoggedIn(true);
        } else {
            setLoggedIn(false);
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [localStorage.getItem('validDue')]);

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('validDue');
        setLoggedIn(false);
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
