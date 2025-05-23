import React, { useState, useRef, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Navbar, Nav, Container, Button, Dropdown , Image, NavDropdown} from 'react-bootstrap';
import { authAPI, minioAPI } from "../api/api";
import 'bootstrap/dist/css/bootstrap.min.css';
import "./Header.css"

//const avatar = "https://i0.wp.com/sbcf.fr/wp-content/uploads/2018/03/sbcf-default-avatar.png?ssl=1";

const Header = ({ showButtons}) => {
  const navigate = useNavigate();
  const location = useLocation();

  const [avatar, setAvatar] = useState(null)

  useEffect(() => {
    const getAvatar = async () => {
      // console.log(import.meta.env.VITE_DEFAULT_AVATAR)
      let filename = localStorage.getItem("avatar")
      if (filename === undefined){
        filename = import.meta.env.VITE_DEFAULT_AVATAR
      }
      const imageUrl = minioAPI.getImageUrl(filename, "avatars")
      setAvatar(imageUrl)
    };
    getAvatar();
  })

  const handleLogout = async() => {
    await authAPI.logout();
    navigate("/")
  };
   
    return (
        <Navbar className="fixed-header" expand="lg" variant="dark" style={{backgroundColor:"#8a2be2"}} >
        <Container>
          <Navbar.Brand href="/myroadmaps">Трекер карьеры</Navbar.Brand>
          {showButtons && (<Navbar.Toggle aria-controls="responsive-navbar-nav" />)}
          {showButtons && (
          <Navbar.Collapse id="responsive-navbar-nav"> 
            <Nav className="me-auto"/>    
            <Nav activeKey={location.pathname}>
            <Nav.Link href="/myroadmaps" className="menu-button">Мои роадмапы</Nav.Link>
              <Nav.Link href="/roadmapsearch" className="menu-button">Поиск роадмапов</Nav.Link>
              <NavDropdown title="Профиль" style={{backgroundColor:'#8a2be2'}} id="collapsible-nav-dropdown">
                <NavDropdown.Item style={{color:'#fff', backgroundColor: '#8a2be2', fontSize:"15px"}}>
                  <div>{JSON.parse(localStorage.getItem('userData')).username}</div>
                  <div>{JSON.parse(localStorage.getItem('userData')).login}</div>
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