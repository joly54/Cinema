import React from 'react';
import { Link } from 'react-router-dom';
import './Styles/Navbar.css';
import './Styles/scrollBar.css';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap/dist/js/bootstrap.bundle.min.js.map';

function navigator() {
    window.location.href = "/";
}
function Header({ loggedIn, handleLogout }) {

    return (
        <Navbar variant="dark" bg="dark" expand="lg">
            <Container fluid>
                <Navbar.Brand onClick={navigator}>Cinema</Navbar.Brand>
                <Navbar.Toggle aria-controls="navbar-dark-example" />
                <Navbar.Collapse id="navbar-dark-example">
                    <Nav>
                        <Nav.Link>
                            <Link to={"/"} className="nav-link">Schedule</Link>
                        </Nav.Link>
                        <Nav.Link>
                            <Link to={"/films"} className="nav-link">Films</Link>
                        </Nav.Link>
                    </Nav>
                    <Nav>
                        <NavDropdown
                            id="nav-dropdown-dark-example"
                            title="Profile"
                            menuVariant="dark"
                        >
                            {loggedIn?
                                <>
                                <div
                                >
                                    <NavDropdown.Item>
                                        <Link to={"/profile"} className="nav-link">Profile</Link>
                                    </NavDropdown.Item>
                                    <NavDropdown.Item>
                                        <Link to={"/login"} className="nav-link" onClick={handleLogout}>Logout</Link>
                                    </NavDropdown.Item>
                                </div>
                                    </>
                                :
                                <>
                                    <div
                                    >
                                        <NavDropdown.Item>
                                            <Link to={"/login"} className="nav-link">Log in</Link>
                                        </NavDropdown.Item>
                                        <NavDropdown.Item>
                                            <Link to={"/register"} className="nav-link" onClick={handleLogout}>Sing up</Link>
                                        </NavDropdown.Item>
                                    </div>
                                </>
                            }
                        </NavDropdown>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
}

export default Header;
