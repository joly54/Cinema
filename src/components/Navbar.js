import React from 'react';
import {Link, useNavigate} from 'react-router-dom';
import './Styles/Navbar.css';
import './Styles/scrollBar.css';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap/dist/js/bootstrap.bundle.min.js.map';

function Header({loggedIn, handleLogout, additionals}) {
    console.log(additionals);
    const navigate = useNavigate();
    return (
        <Navbar variant="dark" bg="dark" expand="lg">
            <Container fluid

            >
                <Navbar.Brand
                    style={{
                        cursor: "pointer",
                    }
                    }
                    onClick={() => navigate("/")}>Cinema</Navbar.Brand>
                <Navbar.Toggle aria-controls="navbar-dark-example"/>
                <Navbar.Collapse id="navbar-dark-example">
                    <Nav>
                        <Nav.Link>
                            <Link to={"/"} className="nav-link">Schedule</Link>
                        </Nav.Link>
                        <Nav.Link>
                            <Link to={"/films"} className="nav-link">Films</Link>
                        </Nav.Link>
                    </Nav>
                    {/*map by aditionals*/}
                    {additionals.map((item, index) => {
                        return (
                            <Nav key={index}>
                                <a
                                    href={item.url}
                                    className="nav-link"
                                    target="_blank"
                                    rel="noreferrer"
                                >
                                    {item.title}
                                </a>
                            </Nav>
                        );
                    })}

                    <Nav>
                        {loggedIn ? (
                            <>
                                <Nav.Link>
                                    <Link to={"/profile"} className="nav-link">Profile</Link>
                                </Nav.Link>
                                <Nav.Link>
                                    <Link to={"/login"} className="nav-link" onClick={handleLogout}>Logout</Link>
                                </Nav.Link>
                            </>
                        ) : (
                            <>
                                <Nav.Link>
                                    <Link to={"/login"} className="nav-link">Log in</Link>
                                </Nav.Link>
                                <Nav.Link>
                                    <Link to={"/register"} className="nav-link" onClick={handleLogout}>Sign up</Link>
                                </Nav.Link>
                            </>
                        )}
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
}

export default Header;