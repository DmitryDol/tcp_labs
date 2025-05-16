import React, { useState, useRef, useEffect } from "react";
import { useLocation, useParams } from "react-router-dom";
import Header from "../components/Header";
import CardView from "../components/CardView";
import { Button, Form, Card } from "react-bootstrap";
import { BsBookmark, BsBookmarkFill } from "react-icons/bs";
import { FaRegPlusSquare } from "react-icons/fa";
import CardModal, { CreateCard} from "../components/Cardredact";
import "./CardsPage.css";
import { minioAPI, userRoadmapAPI } from "../api/api";


const CardsPage = () => {
  let [isBookmarked, setIsBookmarked] = useState(false);
  const [modalShow, setModalShow] = useState(false);
  const location = useLocation();
  const { id } = useParams();
  const [background, setBackground] = useState(null);

  useEffect(() => {
    const getBackground = async () => {
      console.log(id)
      let filename = await userRoadmapAPI.getBackgroundFilename(id);
      console.log(filename)
      if (filename===undefined)
        {filename = import.meta.env.VITE_DEFAULT_BACKGROUND}
      const imageurl = minioAPI.getImageUrl(filename, "backgrounds");
      setBackground(imageurl);
    };
    getBackground();
  }, [id]);
  

  const handleBookmark = () => {
    setIsBookmarked(!isBookmarked);
  };
  
  if (location.pathname === "/myroadmaps/cards"){
    isBookmarked = true;
  }
  const mayRedact = true;
  const handleCreateCard = () =>{

  }

  return (
    <>
      <Header showButtons={true} />
      <div className="container-flex" style={{ backgroundImage: `url(${background})`, backgroundSize: 'cover',}}>
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
