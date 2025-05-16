import React, { useState, useRef, useEffect } from "react";
import Header from "../components/Header";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import { Form, Alert, Modal } from "react-bootstrap";
import "./EditProfilePage.css";
import { minioAPI, userAPI } from "../api/api";

// const avatar = "";
const EditProfilePage = () => {
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const [error, setError] = useState("");
  const [formData, setFormData] = useState({
    name: "",
    password: "",
    password2: "",
  });
  const [avatar, setAvatar] = useState(null);

  useEffect(() => {
    const getAvatar = async () => {
      let filename = localStorage.getItem("avatar");
      if (filename == "undefined") {
        filename = import.meta.env.VITE_DEFAULT_AVATAR;
      }
      const imageUrl = minioAPI.getImageUrl(filename, "avatars");
      setAvatar(imageUrl);
    };
    getAvatar();
  });

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const { name, password, password2 } = formData;

    if (password.length < 6 || password.length > 16) {
      setError("Пароль должен содержать от 6 до 16 символов");
      return;
    }
    if (password != password2) {
      setError("Пароли не совпадают");
      return;
    }
    // Здесь логика сохранения изменений
    await userAPI.editUserInfo(name, password);
    // alert("Изменения сохранены!");
  };

  const inputRef = useRef(null);

  const handleAvatarChangeClick = () => {
    inputRef.current.click();
  };

  const handleDeleteAvatar = async () => {
    try {
      const updatedUserInfo = await userAPI.deleteUserAvatar();
      filename = import.meta.env.VITE_DEFAULT_AVATAR;
      if (localStorage.getItem("avatar") !== undefined) {
        filename = localStorage.getItem("avatar");
      }
      setAvatar(minioAPI.getImageUrl(filename, "avatars"));
    } catch (err) {
      console.error("delete avatar");
    }
  };

  const handleNewAvatarSelected = async (e) => {
    const file = e.target.files[0];
    if (file) {
      try {
        const updatedUserInfo = await userAPI.changeUserAvatar(file);
        filename = import.meta.env.VITE_DEFAULT_AVATAR;
        if (localStorage.getItem("avatar") !== undefined) {
          filename = localStorage.getItem("avatar");
        }
        if (updatedUserInfo !== undefined) {
          filename = updatedUserInfo.avatar;
        }
        setAvatar(minioAPI.getImageUrl(filename, "avatars"));
      } catch (err) {
        console.error("selected_avatar");
      }
    }
  };

  return (
    <>
      <Header showButtons={true} avatar={avatar} />
      <div className="content">
        <h2 className="mb-4 text-left">Редактировать профиль</h2>
        <div className="top-block">
          <span className="avatar-wrapper">
            <img src={avatar} alt="avatar" className="avatar" />
          </span>
          <div className="user-info">
            <div>
              {JSON.parse(localStorage.getItem("userData"))?.username ||
                "Имя пользователя"}
            </div>
            <div>
              {JSON.parse(localStorage.getItem("userData"))?.login || "Логин"}
            </div>
          </div>
        </div>
        <ButtonGroup size="sm">
          <Button className="buttongroup" onClick={handleAvatarChangeClick}>
            Изменить аватар
          </Button>
          <input
            type="file"
            accept="image/*"
            ref={inputRef}
            style={{ display: "none" }}
            onChange={handleNewAvatarSelected}
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
            <Button className="button" onClick={handleShow}>
              Удалить аккаунт
            </Button>
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
              Вы действительно хотите удалить аккаунт? отменить это действие
              будет невозможно.
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
