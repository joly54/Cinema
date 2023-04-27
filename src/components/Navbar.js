import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
    return (
        <nav>
            <ul>
                <li>
                    <Link to="/">My Profile</Link>
                </li>
                <li>
                    <Link to="/films">Films</Link>
                </li>
                <li>
                    <Link to="/schedule">Schedule</Link>
                </li>
            </ul>
        </nav>
    );
}

export default Navbar;
