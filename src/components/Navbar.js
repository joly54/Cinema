import React from 'react';
import { Link } from 'react-router-dom';
import './Styles/Navbar.css';
import './Styles/scrollBar.css';

function Navbar({ loggedIn, handleLogout }) {

    return (
        <nav>
            <ul>
                <li>
                    <Link to="/films">Films</Link>
                </li>
                <li>
                    <Link to="/">Schedule</Link>
                </li>
                <div className="RightMenu">
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
                    <li>
                        {loggedIn ? <Link to="/profile">My Profile</Link> : <div></div>}
                    </li>
                </div>
                <li>
                </li>
            </ul>
        </nav>
    );
}

export default Navbar;
