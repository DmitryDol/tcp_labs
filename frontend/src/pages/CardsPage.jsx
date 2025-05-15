import React, { useState, useRef } from "react";
import { useLocation } from "react-router-dom";
import Header from "../components/Header";
import CardView from "../components/CardView";
import { Button, Form, Card } from "react-bootstrap";
import { BsBookmark, BsBookmarkFill } from "react-icons/bs";
import { FaRegPlusSquare } from "react-icons/fa";
import CardModal, { CreateCard} from "../components/Cardredact";
import "./CardsPage.css";

const background2 ="https://repository-images.githubusercontent.com/185094183/ff64fd00-706f-11e9-9b53-d05acb2d0989"
const CardsPage = () => {
  let [isBookmarked, setIsBookmarked] = useState(false);
  const [modalShow, setModalShow] = React.useState(false);

  const handleBookmark = () => {
    setIsBookmarked(!isBookmarked);
  };
  const location = useLocation();
  if (location.pathname === "/myroadmaps/cards"){
    isBookmarked = true;
  }
  const mayRedact = true;
  const handleCreateCard = () =>{

  }

  return (
    <>
      <Header showButtons={true} />
      <div className="container-flex" style={{ backgroundImage: `url(${background2})`, backgroundSize: 'cover',}}>
        <Card className="left-card">
          <Card.Header>{"название роадмапа"}</Card.Header>
          <Card.Body>
            <Card.Text>{"описание роадмапа"}</Card.Text>
          </Card.Body>
          <Card.Footer style={{ display: "flex", justifyContent: "flex-end" }}>
            <Button
              className="add-button"
              variant="outline-dark"
              onClick={handleBookmark}
            >
              {isBookmarked ? <BsBookmarkFill /> : <BsBookmark />}
            </Button>
          </Card.Footer>
        </Card>

        <div className="cardblock">
          {/* тут сделать создание карточек из массива */}
          <CardView />
          <CardView />
          {location.pathname === "/myroadmaps/cards" && mayRedact &&
          <Button variant="light" className="addcardbutton" onClick={() => setModalShow(true)}><FaRegPlusSquare/></Button>
          }
        </div>
      </div>
      <CreateCard
        show={modalShow}
        onHide={() => setModalShow(false)}
        onSave={handleCreateCard}
      />
    </>
  );
};

export default CardsPage;
