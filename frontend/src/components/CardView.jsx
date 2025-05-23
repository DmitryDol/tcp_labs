import React, { useState, useEffect} from "react";
import { Accordion, Button, ListGroup, Card, ButtonGroup, Form } from "react-bootstrap";
import { PiTrashBold } from "react-icons/pi";
import { PiNotePencilBold } from "react-icons/pi";
import "./CardView.css"
import { useLocation } from "react-router-dom";
import { EditCard } from "./CardRedact";
import { cardAPI, userCardAPI } from "../api/api";

function CardView({cardInfo, mayRedact, onDelete}) {
    const location = useLocation();
    const [modalShow, setModalShow] = React.useState(false);
    const [selectedStatus, setSelectedStatus] = useState('');
    useEffect(() => {
        setSelectedStatus(cardInfo.status);
    }, [cardInfo.id, cardInfo.status]);
    const handleStatusChange = async (event) => {
        const newStatus = event.target.value;
        setSelectedStatus(newStatus);
        await userCardAPI.editCardStatus(cardInfo.id, newStatus); 
    }
    const handleDeleteCard = async() => {
        await cardAPI.deleteCard(cardInfo.id);
        onDelete(cardInfo.id); 
    };
    
    function handleUpdate(){

    }
    return(
        <Card className="cardcard">
            <Card.Header className="cardhead">
                <span>{cardInfo.title}</span>
                {location.pathname === `/myroadmaps/${cardInfo.roadmap_id}` && mayRedact && 
                <div className="settingsgroup">
                    <Form.Select size="sm" 
                    onChange={handleStatusChange}
                    value={selectedStatus}
                    >
                    <option value="to_do">К выполнению</option>
                    <option value="in_progress">В процессе</option>
                    <option value="done">Выполнено</option>
                </Form.Select>
                <ButtonGroup>
                    <Button size="sm" className="cardbutton" onClick={() => setModalShow(true)}><PiNotePencilBold/></Button>
                    <Button size="sm" className="cardbutton" onClick={handleDeleteCard}><PiTrashBold/></Button>
                </ButtonGroup>
                </div>}
            </Card.Header>
            <ListGroup variant="flush">
                {/* работает только если есть описание */}
                {cardInfo.description && 
                <Accordion className="cardaccordion">
                <Accordion.Item eventKey="0" >
                <Accordion.Header>{"Описание"}</Accordion.Header>
                <Accordion.Body>
                    {cardInfo.description}
                </Accordion.Body>
                </Accordion.Item>
                </Accordion>}
            {cardInfo.links.map((link, index) => (
                <ListGroup.Item key={index}><Card.Link href={link.link_content}>{link.link_title}</Card.Link></ListGroup.Item>
            ))}
                  
            </ListGroup>
            <EditCard 
                show={modalShow} 
                onHide={() => setModalShow(false)}
                initialData={cardInfo}
                onSave={handleUpdate} 
            />
        </Card>
    )
}

export default CardView