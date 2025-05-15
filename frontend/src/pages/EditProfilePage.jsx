import React, { useState, useRef } from "react";
import Header from "../components/Header";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import { Form, Alert, Modal } from "react-bootstrap";
import "./EditProfilePage.css";

const avatarUrl = "";
const EditProfilePage = () => {
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const [error, setError] = useState("");
  const [formData, setFormData] = useState({
    name: "",
    username: "",
    password: "",
    password2: "",
  });

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const { name, username, password, password2 } = formData;
    if (password.length < 6 || password.length > 16) {
      setError("Пароль должен содержать от 6 до 16 символов");
      return;
    }
    if (password != password2) {
      setError("Пароли не совпадают");
      return;
    }
    // Здесь логика сохранения изменений
    alert("Изменения сохранены!");
  };

  const inputRef = useRef(null);

  const handleButtonClick = () => {
    inputRef.current.click();
  };
  const handleDeleteAvatar = (e) => {
    //тут логика удаления аватара
  };

  const handleNewAvatar = (e) => {
    const file = e.target.files[0];
    if (file) {
      //тут что то с файлом сделать, сохранение сразу произвести
      console.log(file);
    }
  };

  return (
    <>
      <Header showButtons={true} avatarUrl={avatarUrl} />
      <div className="content">
        <h2 className="mb-4 text-left">Редактировать профиль</h2>
        <div className="top-block">
          <span className="avatar-wrapper">
            <img src={avatarUrl} alt="avatar" className="avatar" />
          </span>
          <div className="user-info">
            {/* тут должно быть имя пользователя который сейчас в системе */}
            <div>{"username"}</div>
            <div>{"login"}</div>
          </div>
        </div>
        <ButtonGroup size="sm">
          <Button className="buttongroup" onClick={handleButtonClick}>
            Изменить аватар
          </Button>
          <input
            type="file"
            accept="image/*"
            ref={inputRef}
            style={{ display: "none" }}
            onChange={handleNewAvatar}
          />
          <Button className="buttongroup" onClick={handleDeleteAvatar}>
            Удалить аватар
          </Button>
        </ButtonGroup>
        <Form className="userinfo-form" onSubmit={handleSubmit}>
          <Form.Group className="mb-3" controlId="formName">
            <Form.Label>Изменить имя</Form.Label>
            <Form.Control
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Введите новое имя"
            />
          </Form.Group>
          <Form.Group className="mb-3" controlId="formPassword1">
            <Form.Label>Изменить пароль</Form.Label>
            <Form.Control
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Введите новый пароль"
            />
          </Form.Group>
          <Form.Group className="mb-3" controlId="formPassword2">
            <Form.Control
              type="password"
              name="password2"
              value={formData.password2}
              onChange={handleChange}
              placeholder="Повторите пароль"
            />
          </Form.Group>
          {error && (
            <Alert variant="danger" className="mt-3 erroralert">
              {error}
            </Alert>
          )}
          <div className="d-grid justify-content-center gap-2">
            <Button className="button" type="submit">
              Сохранить изменения
            </Button>
            <Button className="button" onClick={handleShow}>Удалить аккаунт</Button>
          </div>
          <Modal
            show={show}
            onHide={handleClose}
            backdrop="static"
            keyboard={false}
          >
            <Modal.Header closeButton>
              <Modal.Title>Удалить аккаунт</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              Вы действительно хотите удалить аккаунт? отменить это действие будет невозможно.
            </Modal.Body>
            <Modal.Footer>
              <Button variant="secondary" onClick={handleClose}>
                Закрыть
              </Button>
              <Button variant="danger">Удалить</Button>
            </Modal.Footer>
          </Modal>
        </Form>
      </div>
    </>
  );
};

export default EditProfilePage;
