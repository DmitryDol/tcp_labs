import React, { useState, useRef, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Navbar, Nav, Container, Button, Dropdown , Image, NavDropdown} from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./Header.css"

const avatar = "https://i0.wp.com/sbcf.fr/wp-content/uploads/2018/03/sbcf-default-avatar.png?ssl=1";

const Header = ({ showButtons, avatarUrl, user}) => {
  const navigate = useNavigate();
  const location = useLocation();

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
            <Nav activeKey={location.pathname}>
            <Nav.Link href="/myroadmaps" className="menu-button">Мои роадмапы</Nav.Link>
              <Nav.Link href="/roadmapsearch" className="menu-button">Поиск роадмапов</Nav.Link>
              <NavDropdown title="Профиль" style={{backgroundColor:'#8a2be2'}} id="collapsible-nav-dropdown">
                <NavDropdown.Item style={{color:'#fff', backgroundColor: '#8a2be2', fontSize:"15px"}}>
                  {/* тут должно быть имя и логин пользователя, который в системе */}
                  <div>{'Name'}</div>
                  <div>{'login'}</div>
                </NavDropdown.Item>
                <NavDropdown.Item href="/editprofile" className="dropdownitem">Настройки профиля</NavDropdown.Item>
                <NavDropdown.Item onClick={handleLogout} className="dropdownitem">Выйти</NavDropdown.Item>
              </NavDropdown>
              <Image 
                src={avatar} 
                alt="Аватар" 
                roundedCircle 
                style={{ width: '40px',
                  height: '40px',
                  objectFit: 'cover',
                  marginLeft: '5px'}}
              />

            </Nav>
          </Navbar.Collapse>)}
        </Container>
      </Navbar>
    );
  };


export default Header;