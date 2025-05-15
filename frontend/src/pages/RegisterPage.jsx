import React, { useState } from "react";
import axios from "axios";
import { Container, Form, Button, Alert } from 'react-bootstrap';
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import "./AuthRegister.css"


const RegisterPage = () => {
  const [formData, setFormData] = useState({
    name: "",
    username: "",
    password: "",
    password2: ""
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError("");
  };

  const handleSubmit = async (e) => {
    // обработка создания нового пользователя
    e.preventDefault();
    const { name, username, password, password2 } = formData;
    if (password.length < 6 || password.length > 16){
      setError("Пароль должен содержать от 6 до 16 символов")
      return;
    }
    if(password!=password2){
      setError("Пароли не совпадают")
      return;
    }
    await axios.post("http://127.0.0.1:8000/auth", {
      name: name,
      login: username,
      password_hash: password,
    }, {
      headers: {
        "Content-Type": "application/json",
      },
    });
    // тут обработку ошибок добавить и только потом переход
    navigate("/mainpage");
  };

  return (
    <div>
      <Header showButtons={false} />

    <Container className="mt-5 registration-container" style={{ maxWidth: '500px' }}>
      <h2 className="mb-4 text-center">Регистрация</h2>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="formBasicName">
          <Form.Label>Имя</Form.Label>
          <Form.Control
            type="text"
            placeholder="Введите имя"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicUsername">
          <Form.Label>Логин</Form.Label>
          <Form.Control
            type="text"
            placeholder="Введите логин"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Пароль</Form.Label>
          <Form.Control
            type="password"
            placeholder="Введите пароль"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Control
            type="password"
            placeholder="Повторите пароль"
            name="password2"
            value={formData.password2}
            onChange={handleChange}
            required
          />
        </Form.Group>

        {error && <Alert variant="danger" className="mt-3 erroralert">{error}</Alert>}

        <div >
          <Button type="submit" className="mt-3 btn-purple">
            Создать аккаунт
          </Button>
          <Button className="mt-3 btn-purple" href="/">Назад</Button>
        </div>
      </Form>
    </Container>
    </div>
  );
};


export default RegisterPage;
