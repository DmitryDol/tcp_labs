import React, { useState, useEffect } from "react";
import { Modal, Button, Form } from "react-bootstrap";
import { minioAPI, roadmapAPI, userRoadmapAPI } from "../api/api";

function RoadmapModal(props) {
  const { isEditing, initialData, onHide, onSave } = props;
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [image, setImage] = useState(null);
  const [difficulty, setDifficulty] = useState("");
  const [visibility, setVisibility] = useState("");
  const [editPermission, setEditPermission] = useState("");

  // Загрузка начальных значений при редактировании
  useEffect(() => {
    if (isEditing && initialData) {
      setTitle(initialData.title || "");
      setDescription(initialData.description || "");
      setDifficulty(initialData.difficulty || "");
      setVisibility(initialData.visibility || "");
      const editPermissionValue = initialData.edit_permission === "view only" ? "view_only": 
      initialData.edit_permission === "can edit" ? "can_edit": "";
      setEditPermission(editPermissionValue || "");
    }
  }, [isEditing, initialData]);

  const handleClose = () => {
    setTitle('');
    setDescription('');
    setDifficulty('');
    setVisibility('');
    setEditPermission('');
    onHide();
  };

 const handleSave = async () => {
  if (!isEditing) {
    const response = await roadmapAPI.addRoadmap(
      JSON.parse(localStorage.getItem("userData")).id,
      title,
      description,
      difficulty,
      editPermission,
      visibility
    );
    console.log(response.roadmap_id)
    if(image){
      await userRoadmapAPI.changeRoadmapBackground(response.roadmap_id, image)
    }
    const newRoadmap = {
      id: response.roadmap_id,
      title,
      description,
      difficulty,
      visibility,
      editPermission,
    };
    onSave(newRoadmap);
  } else {
    await roadmapAPI.editRoadmap(
      initialData.id,
      title,
      description,
      difficulty,
      editPermission,
      visibility
    );
    if (image) {
      await userRoadmapAPI.changeRoadmapBackground(initialData.id, image);
    }
    window.location.reload();
  }
  handleClose();
};
// ... existing code ...

  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          {isEditing ? "Редактировать роадмап" : "Новый роадмап"}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Form.Group className="mb-3" controlId="formRoadmapTitle">
            <Form.Label>Название</Form.Label>
            <Form.Control
              type="text"
              placeholder="Введите название"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formRoadmapDescription">
            <Form.Label>Описание</Form.Label>
            <Form.Control
              as="textarea"
              rows={2}
              placeholder="Введите описание"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </Form.Group>
          <Form.Group className="mb-3" controlId="formRoadmapImage">
            <Form.Label>Фоновое изображение</Form.Label>
            <Form.Control
              type="file"
              accept="image/*"
              aria-label="Выберите изображение для фона роадмапа"
              onChange={(e) => setImage(e.target.files[0])}
            />
            {isEditing && initialData && initialData.imageName && (
              <Form.Text className="text-muted">
                Текущее изображение: {initialData.imageName}
              </Form.Text>
            )}
          </Form.Group>

          <div
            style={{
              display: "flex",
              alignItems: "flex-end",
              gap: "10px",
            }}
          >
            <Form.Group className="mb-3" controlId="formDifficulty">
              <Form.Label>Сложность</Form.Label>
              <Form.Select
                aria-label="Выбор сложности"
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value)}
              >
                <option value="">Уровень сложности</option>
                <option value="easy">Легкий</option>
                <option value="medium">Средний</option>
                <option value="hard">Сложный</option>
              </Form.Select>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formVisibility">
              <Form.Label>Видимость</Form.Label>
              <Form.Select
                aria-label="Выбор видимости"
                value={visibility}
                onChange={(e) => setVisibility(e.target.value)}
              >
                <option value="">Настройки видимости</option>
                <option value="public">Публичный</option>
                <option value="link_only">Только по ссылке</option>
                <option value="private">Приватный</option>
              </Form.Select>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formEditPermission">
              <Form.Label>Права редактирования</Form.Label>
              <Form.Select
                aria-label="Выбор прав редактирования"
                value={editPermission}
                onChange={(e) => setEditPermission(e.target.value)}
              >
                <option value="">Тип прав доступа</option>
                <option value="view_only">Только просмотр</option>
                <option value="can_edit">Можно редактировать</option>
              </Form.Select>
            </Form.Group>
          </div>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button
          onClick={handleSave}
          style={{
            "--bs-btn-bg": "blueviolet",
            "--bs-btn-hover-bg": "blueviolet",
            "--bs-btn-active-bg": "#a45be8",
          }}
        >
          Сохранить
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

export function CreateRoadmap(props) {
  return <RoadmapModal {...props} isEditing={false} initialData={null} />;
}

export function EditRoadmap(props) {
  return <RoadmapModal {...props} isEditing={true} />;
}

export default RoadmapModal;
