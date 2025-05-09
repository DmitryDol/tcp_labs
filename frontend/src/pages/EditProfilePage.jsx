import React, { useState, useRef} from "react";
import Header from "../components/Header";
import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup'
import { Form } from "react-bootstrap";
import './EditProfilePage.css'; 

const avatarUrl = "https://i0.wp.com/sbcf.fr/wp-content/uploads/2018/03/sbcf-default-avatar.png?ssl=1";

const EditProfilePage = () => {
  const [formData, setFormData] = useState({});

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Здесь логика сохранения изменений
    alert("Изменения сохранены!");
  };

  const inputRef = useRef(null);

  const handleButtonClick = () => {
    inputRef.current.click();
  };
  const handleDeleteAvatar = (e) => {
    //тут логика удаления аватара
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      //тут что то с файлом сделать
      console.log(file);
    }
  };

  return (
    <div>
      <Header
        showButtons={true}
        avatarUrl={avatarUrl}
      />
      <div className="content">
      <h2 className="mb-4 text-left">Редактировать профиль</h2>
        <div className="top-block">
          <span className="avatar-wrapper">
            <img src={avatarUrl} alt="avatar" className="avatar" />
          </span>
          <div className="user-info">
            {/* тут должно быть имя пользователя который сейчас в системе */}
            <div>username</div> 
            <div>login</div>
          </div>
        </div>
            <ButtonGroup size="sm">
              <Button className="buttongroup" onClick={handleButtonClick}>Изменить аватар</Button>
              <input
                type="file"
                accept="image/*"
                ref={inputRef}
                style={{ display: 'none' }}
                onChange={handleFileChange}
              />
              <Button className="buttongroup" onClick={handleDeleteAvatar}>Удалить аватар</Button>
            </ButtonGroup>
        <Form className="form" onSubmit={handleSubmit}>
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
                  name="password1"
                  value={formData.password1}
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
          <div className="d-flex justify-content-center">
            <Button className="button" type="submit">
              Сохранить изменения
            </Button>
          </div>
        </Form>
      </div>
    </div> 
  );
};

export default EditProfilePage;
