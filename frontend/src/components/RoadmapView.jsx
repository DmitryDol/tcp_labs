import React, { useState, useRef } from "react";
import Card from "react-bootstrap/Card";
import { Accordion, Button, Dropdown } from "react-bootstrap";
import { useLocation } from "react-router-dom";
import {BsBookmark,BsBookmarkFill,BsThreeDotsVertical} from "react-icons/bs";
import { EditRoadmap } from "./RoadmapRedact";
import "./RoadmapView.css";

function RoadmapView({ backgroundUrl, roadmapTitle }) {
  const location = useLocation();
  const pathWithCards = `${location.pathname}/cards`;
  const [isBookmarked, setIsBookmarked] = useState(false);

  // тут надо как то получать состояния роадмапа: кем он создан и можно ли редактировать
  let isMade = true;
  let mayRedact = true;

  const handleBookmark = () => {
    setIsBookmarked(!isBookmarked);
  };
  let roadmapToEdit
    
  const handleUpdateRoadmap=()=>{

  }
  const [modalShow, setModalShow] = React.useState(false);

  return (
    <Card className="bg-light text-dark roadmapcard">
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          height: "12rem",
        }}
      >
        <Card.Body className="cardbody">
          <Card.Title style={{ fontSize: "21px" }}>
            <Card.Link href={pathWithCards} className="roadmapname">
              {roadmapTitle}
            </Card.Link>
          </Card.Title>
          <Card.Footer
            style={{
              display: "flex",
              flexDirection: "row",
              justifyContent: "space-between",
              alignItems: "baseline",
            }}
          >
            <Card.Text>{"тут сложность"}</Card.Text>
            {location.pathname === "/myroadmaps" ? (
              <Dropdown drop="end">
                <Dropdown.Toggle
                  as={Button}
                  className="roadmap-button"
                  variant="outline-dark"
                >
                  <BsThreeDotsVertical />
                </Dropdown.Toggle>
                <Dropdown.Menu style={{ backgroundColor: "white" }}>
                  {isMade ? <Dropdown.Item
                    style={{
                      "--bs-dropdown-link-active-bg": "blueviolet",
                      textDecoration: " underline",
                    }}
                  >
                    Удалить роадмап
                  </Dropdown.Item> :
                  <Dropdown.Item
                    style={{
                      "--bs-dropdown-link-active-bg": "blueviolet",
                      textDecoration: " underline",
                    }}
                  >
                    Отписаться
                  </Dropdown.Item>}
                  {mayRedact && <Dropdown.Item
                    style={{
                      "--bs-dropdown-link-active-bg": "blueviolet",
                      textDecoration: " underline",
                    }}
                    onClick={() => setModalShow(true)}
                  >
                    Изменить роадмап
                  </Dropdown.Item>
                  }
                </Dropdown.Menu>
              </Dropdown>
            ) : (
              <Button
                className="roadmap-button"
                variant="outline-dark"
                onClick={handleBookmark}
              >
                {isBookmarked ? <BsBookmarkFill /> : <BsBookmark />}
              </Button>
            )}
            <EditRoadmap 
              show={modalShow}
              onHide={() =>setModalShow(false)}
              initialData={roadmapToEdit}
              onSave={handleUpdateRoadmap}
            />
          </Card.Footer>
        </Card.Body>
        <Card.Img src={backgroundUrl} alt="Card image" className="cardimg" />
      </div>
      <Accordion>
        <Accordion.Item eventKey="0">
          <Accordion.Header>Описание</Accordion.Header>
          <Accordion.Body>{"тут текст описания"}</Accordion.Body>
        </Accordion.Item>
      </Accordion>
    </Card>
  );
}

export default RoadmapView;
