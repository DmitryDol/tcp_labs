import React, { useState } from "react";
import axios from "axios";
import { Container, Form, Button, Alert, Stack } from 'react-bootstrap';
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import "./AuthRegister.css"

const AuthPage = () => {
  const [formData, setFormData] = useState({ login: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError("");
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!formData.login || !formData.password) {
      setError("Пожалуйста, заполните оба поля.");
      return;
    }
    
    // const params = new URLSearchParams({
    //   username: formData.login,
    //   password: formData.password
    // }).toString();

    // try {
    //   await axios.post(
    //     "http://127.0.0.1:8000/auth/token",
    //     params,
    //     { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
    //   );
      
      navigate("/mainpage");
    // } catch (err) {
    //   alert(
    //     err.response?.data?.detail ||
    //     err.message ||
    //     "Ошибка входа"
    //   );
    // }
  };

  const handleRegister = () => {
    navigate("/register");
  };

  return (
    <div>
      <Header showButtons={false} />
        <Container className="mt-5 registration-container" style={{ maxWidth: '500px' }}>
          <h2 className="mb-4 text-center">Авторизация</h2>
          <Form onSubmit={handleLogin}>
            <Form.Group className="mb-3" controlId="formBasicLogin">
              <Form.Label>Логин</Form.Label>
              <Form.Control
                type="text" 
                placeholder="Введите логин"
                name="login" 
                value={formData.login}
                onChange={handleChange}
                autoComplete="username" 
                required
              />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPasswordLogin">
              <Form.Label>Пароль</Form.Label>
              <Form.Control
                type="password"
                placeholder="Введите пароль"
                name="password"
                value={formData.password}
                onChange={handleChange}
                autoComplete="current-password"
                required
              />
            </Form.Group>
            {error && <Alert variant="danger" className="mt-3">{error}</Alert>}

            <div className="d-flex justify-content-center gap-2">
              <Button type="submit" className="mt-3 btn-purple flex-grow-1">
                Войти
              </Button>
              <Button type="button" className="mt-3 btn-purple flex-grow-1" onClick={handleRegister}>
                Зарегистрироваться
              </Button>
            </div>
          </Form>
        </Container>
    </div>
  );
};


export default AuthPage;
