import React, { useState, useEffect } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import { FaRegTrashAlt } from 'react-icons/fa';
import { cardAPI, cardLinkAPI } from '../api/api';

function CardModal(props) {
  const { roadmapId, isEditing, initialData, numberOfCards, onHide } = props;
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [links, setLinks] = useState([]);

  useEffect(() => {
    if (initialData) {
      setTitle(initialData.title || '');
      setDescription(initialData.description || '');
      setLinks(initialData.links);
    } else {
      setTitle('');
      setDescription('');
      setLinks([]);
    }
  }, [props.initialData]);

  const addLinkField = () => {
    setLinks([...links, { title: "", content: "" }]);
  };

  const handleLinkChange = (index, field, value) => {
    const newLinks = [...links];
    newLinks[index][field] = value;
    setLinks(newLinks);
  };

  const handleClose = () => {
    setLinks([]);
    setTitle('');
    setDescription('');
    onHide();
  };

  const removeLink = (index) => {
    const newLinks = [...links];
    newLinks.splice(index, 1);
    setLinks(newLinks);
  };

  const handleSave = async () => {
    if (!isEditing) {
      const result = await cardAPI.addCard(roadmapId, title, description, numberOfCards + 1)
      const addedLinks = []
      for (let link of links) {
        const linkResult = await cardLinkAPI.addCardLink(result.card_id, link.link_title, link.link_content)
        addedLinks.push({ id: linkResult, title: link.link_title, content: link.link_content })
      }

      // const newCard = {
      //   id: result.card_id,
      //   title,
      //   description,
      //   links: addedLinks,
      //   roadmap_id: roadmapId,
      //   order_position: numberOfCards + 1
      // };
      // onSave(newCard);
      handleClose();
    }
    else {
      await cardAPI.editCard(initialData.id, title, description);

      const originalLinks = initialData.links || [];
      const currentLinks = links || [];
      const processedLinkIds = new Set(); 

      const updatedLinks = [];
      for (const link of currentLinks) {
        if (link.id) {
          await cardLinkAPI.editCardLink(link.id, link.link_title, link.link_content);
          processedLinkIds.add(link.id);
          updatedLinks.push(link);
        } else if (link.link_title || link.link_content) {
          console.log(link)
          const linkResult = await cardLinkAPI.addCardLink(initialData.id, link.link_title, link.link_content);
          if (linkResult && linkResult.id) {
              processedLinkIds.add(linkResult.id);
              updatedLinks.push({ id: linkResult.id, title: link.link_title, content: link.link_content });
          } else {
              console.error("Failed to add link or get link ID", linkResult);
          }
        }
      }

      for (const originalLink of originalLinks) {
        if (originalLink.id && !processedLinkIds.has(originalLink.id)) {
          await cardLinkAPI.deleteLinkFromCard(originalLink.id);
        }
      }
    }

    handleClose();
  };

  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
      onHide={handleClose}
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          {isEditing ? "Редактирование карточки" : "Новая карточка"}
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
          <Button
            variant="secondary"
            style={{ backgroundColor: "blueviolet" }}
            onClick={addLinkField}
          >
            Добавить ссылку
          </Button>
          {links.map((link, index) => (
            <div key={index}>
              <Form.Group className="mt-3" controlId={`formLinkTitle${index}`}>
                <Form.Label style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <span>{index + 1}</span>
                  <Button variant="danger" size="sm" onClick={() => removeLink(index)}>
                    <FaRegTrashAlt />
                  </Button>
                </Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Введите название ссылки"
                  value={link.link_title}
                  onChange={(e) =>
                    handleLinkChange(index, "link_title", e.target.value)
                  }
                />
                <Form.Control
                  type="text"
                  placeholder="Введите содержимое ссылки"
                  value={link.link_content}
                  onChange={(e) =>
                    handleLinkChange(index, "link_content", e.target.value)
                  }
                />
              </Form.Group>
            </div>
          ))}
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

export function CreateCard(props) {
  return <CardModal {...props} initialData={null} isEditing={false} />;
}

export function EditCard(props) {
  return <CardModal {...props} initialData={props.initialData} isEditing={true} />;
}

export default CardModal;
