import React, { useState} from "react";
import { Accordion, Button, ListGroup, Card, ButtonGroup, Form } from "react-bootstrap";
import { PiTrashBold } from "react-icons/pi";
import { PiNotePencilBold } from "react-icons/pi";
import "./CardView.css"
import { useLocation } from "react-router-dom";
import { EditCard } from "./Cardredact";

function CardView(cardInfo){
    const description = "";
    const mayRedact = true;
    const location = useLocation();
    const [modalShow, setModalShow] = React.useState(false);
    const cardToEdit = {}
    function handleDeleteCard(){

    }
    function handleUpdate(){

    }
    return(
        <Card className="cardcard">
            <Card.Header className="cardhead">
                <span>{"название карточки"}</span>
                {location.pathname === "/myroadmaps/cards" && mayRedact && 
                <div className="settingsgroup">
                <ButtonGroup>
                    <Button size="sm" className="cardbutton" onClick={() => setModalShow(true)}><PiNotePencilBold/></Button>
                    <Button size="sm" className="cardbutton" onClick={handleDeleteCard}><PiTrashBold/></Button>
                </ButtonGroup>
                <Form.Select size="sm">
                    <option value="to_do">К выполнению</option>
                    <option value="in_progress">В процессе</option>
                    <option value="done">Выполнено</option>
                </Form.Select>
                </div>}
            </Card.Header>
            <ListGroup variant="flush">
                {/* работает только если есть описание */}
                {description && 
                <Accordion className="cardaccordion">
                <Accordion.Item eventKey="0" >
                <Accordion.Header>Описание</Accordion.Header>
                <Accordion.Body>
                    {"тут текст описания"}
                </Accordion.Body>
                </Accordion.Item>
                </Accordion>}
            {/* по хорошему надо отрисовывать карточки используя массив полученных значений */}
                <ListGroup.Item><Card.Link href={""}>{"ссылка1"}</Card.Link></ListGroup.Item>
                <ListGroup.Item><Card.Link href={""}>{"ссылка2"}</Card.Link></ListGroup.Item>
                <ListGroup.Item><Card.Link href={""}>{"ссылка3"}</Card.Link></ListGroup.Item>
            </ListGroup>
            <EditCard 
                show={modalShow} 
                onHide={() => setModalShow(false)}
                initialData={cardToEdit}
                onSave={handleUpdate} 
            />
        </Card>
    )
}

export default CardView