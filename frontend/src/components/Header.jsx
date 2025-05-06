import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Navbar, Nav, Container, Button, Dropdown , Image, NavDropdown} from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./Header.css"

const Header = ({ showButtons, avatarUrl}) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    //тут логика выхода
    alert("вы вышли из профиля")
    navigate("/")
  };
   
    return (
        <Navbar className="fixed-header" expand="lg" variant="dark" style={{backgroundColor:"#8a2be2"}} >
        <Container>
          <Navbar.Brand href="/mainpage">Трекер карьеры</Navbar.Brand>
          {showButtons && (<Navbar.Toggle aria-controls="responsive-navbar-nav" />)}
          {showButtons && (
          <Navbar.Collapse id="responsive-navbar-nav"> 
            <Nav className="me-auto"/>    
            <Nav>
            <Nav.Link href="/myroadmaps" className="menu-button">Мои роадмапы</Nav.Link>
              <Nav.Link href="/roadmapsearch" className="menu-button">Поиск роадмапов</Nav.Link>
              <NavDropdown title="Профиль" style={{backgroundColor:'#8a2be2'}} id="collapsible-nav-dropdown">
                <NavDropdown.Item style={{color:'#fff', backgroundColor: '#8a2be2', fontSize:"15px"}}>
                  <div>Name</div>
                  <div>login</div>
                </NavDropdown.Item>
                <NavDropdown.Item href="/editprofile" style={{color:'#fff', backgroundColor: '#8a2be2'}}>Настройки профиля</NavDropdown.Item>
                <NavDropdown.Item onClick={handleLogout} style={{color:'#fff', backgroundColor: '#8a2be2'}}>Выйти</NavDropdown.Item>
              </NavDropdown>
              {avatarUrl && (
                <Image 
                  src={avatarUrl} 
                  alt="Аватар" 
                  roundedCircle 
                  style={{ width: '40px',
                    height: '40px',
                    objectFit: 'cover',
                    marginLeft: '5px'}}
                />
              )}
            </Nav>
          </Navbar.Collapse>)}
        </Container>
      </Navbar>
    );
  };


export default Header;