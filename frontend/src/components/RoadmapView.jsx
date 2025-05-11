import React, { useState, useRef} from "react";
import Card from 'react-bootstrap/Card';
import { Accordion, Button } from "react-bootstrap";
import { BsBookmark,BsBookmarkFill } from "react-icons/bs";
import "./RoadmapView.css"

function RoadmapView({ backgroundUrl, roadmapTitle}) {
   const [isBookmarked, setIsBookmarked] = useState(false);
  
  const handleBookmark = () => {
    setIsBookmarked(!isBookmarked);
  };

    return (
      <Card className="bg-light text-dark roadmapcard">
        <div style={{
          display: 'flex', 
          flexDirection: 'row',
          height: '12rem'}}>
        <Card.Body className="cardbody">
          <Card.Title style={{fontSize: '18px'}}>
            <Card.Link href="/путь-к-странице" className="roadmapname">{roadmapTitle}</Card.Link>
          </Card.Title>
          <Card.Footer style={{display: 'flex', 
          flexDirection: 'row', justifyContent: "space-between"}}>
          <Card.Text>{"тут сложность"}</Card.Text>
          <Button className="add-button" variant="outline-dark" onClick={handleBookmark}>
            {isBookmarked ? <BsBookmarkFill /> : <BsBookmark />}
          </Button>
          </Card.Footer>
        </Card.Body>
        <Card.Img src={backgroundUrl} alt="Card image" className="cardimg"/>
        </div>
        <Accordion >
      <Accordion.Item eventKey="0">
        <Accordion.Header>Описание</Accordion.Header>
        <Accordion.Body>
            {"тут текст описания"}
        </Accordion.Body>
      </Accordion.Item>
    </Accordion>
      </Card>
    );
}

export default RoadmapView