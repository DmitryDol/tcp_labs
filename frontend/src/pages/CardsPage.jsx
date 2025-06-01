import React, { useState, useRef, useEffect } from "react";
import { useLocation, useParams } from "react-router-dom";
import Header from "../components/Header";
import CardView from "../components/CardView";
import { Button, Form, Card } from "react-bootstrap";
import { BsBookmark, BsBookmarkFill } from "react-icons/bs";
import { FaRegPlusSquare } from "react-icons/fa";
import { PiNotePencilBold } from "react-icons/pi";
import CardModal, { CreateCard } from "../components/CardRedact";
import { EditRoadmap } from "../components/RoadmapRedact";
import "./CardsPage.css";
import { minioAPI, roadmapAPI, userRoadmapAPI } from "../api/api";

const CardsPage = () => {
  let [isBookmarked, setIsBookmarked] = useState(false);
  const [roadmapModalShow, setRoadmapModalShow] = useState(false);
  const [cardModalShow, setCardModalShow] = useState(false);
  const location = useLocation();
  const { id } = useParams();
  const [background, setBackground] = useState();
  const [roadmapinfo, setRoadmapinfo] = useState();
  const [isMade, setIsMade] = useState();
  const [mayRedact, setMayRedact] = useState();
  const [cards, setCards] = useState([]);

  useEffect(() => {
    const getBackground = async () => {
      let filename = await userRoadmapAPI.getBackgroundFilename(id);
      if (filename === undefined) {
        filename = import.meta.env.VITE_DEFAULT_BACKGROUND;
      }
      const imageurl = minioAPI.getImageUrl(filename, "backgrounds");
      setBackground(imageurl);
    };
    const getRoadmapInfo = async () => {
      const roadmap = await roadmapAPI.getRoadmapById(id);
      setRoadmapinfo(roadmap);
      setCards(roadmap.cards || []); 
      setIsMade(roadmap.owner_id === JSON.parse(localStorage.getItem("userData")).id);
      setMayRedact(roadmap.edit_permission === "can edit" || roadmap.owner_id === JSON.parse(localStorage.getItem("userData")).id);
    };
    getBackground();
    getRoadmapInfo();
  }, [id]);

  useEffect(() => {
    const checkLinked = async () => {
      let linkedRoadmaps = await userRoadmapAPI.getLinkedRoadmaps();
      const linkedIds = Object.values(linkedRoadmaps.roadmaps).map((item) => item.id);
      setIsBookmarked(linkedIds.includes(roadmapinfo?.id));
    };
    checkLinked();
  }, [id, roadmapinfo]);

  useEffect(() => {
    const updateCards = async () => {
      const cards = await roadmapAPI.getRoadmapById(id);
      setCards(cards.cards || []);
    };
    updateCards();
  }, [cardModalShow]);

  const handleBookmark = async () => {
    if (isBookmarked == false) {
      await userRoadmapAPI.linkUserToRoadmap(roadmapinfo.id);
      setIsBookmarked(true);
    } else {
      await userRoadmapAPI.unlinkUserFromRoadmap(roadmapinfo.id);
      setIsBookmarked(false);
    }
  };

  const handleDeleteCard = (cardId) => {
    setCards((prev) => prev.filter((card) => card.id !== cardId));
  };
  // const handleAddCard = (newCard) => {
  //   setCards((prev) => [...prev, newCard]);
  // };
  return (
    <div>
      <Header showButtons={true} />
      <div
        className="container-flex"
        style={{
          backgroundImage: `url(${background})`,
          backgroundSize: "cover",
        }}
      >
        <Card className="left-card">
          <Card.Header>{roadmapinfo?.title}</Card.Header>
          <Card.Body>
            <Card.Text>{roadmapinfo?.description}</Card.Text>
          </Card.Body>
          <Card.Footer style={{ display: "flex", justifyContent: "flex-end" }} className="gap-3">
            {location.pathname === `/myroadmaps/${roadmapinfo?.id}` ? (
              mayRedact && (
                <Button
                  className="add-button"
                  variant="outline-dark"
                  onClick={() => setRoadmapModalShow(true)}
                >
                  <PiNotePencilBold />
                </Button>
              )
            ) : (
              !isMade && (
                <Button
                  className="add-button"
                  variant="outline-dark"
                  onClick={handleBookmark}
                >
                  {isBookmarked ? <BsBookmarkFill /> : <BsBookmark />}
                </Button>
              )
            )}
          </Card.Footer>
        </Card>

        <div className="cardblock">
          {cards?.map((card, index) => (
            <CardView key={index} cardInfo={card} mayRedact={mayRedact} onDelete={handleDeleteCard} />
          ))}
          {location.pathname === `/myroadmaps/${roadmapinfo?.id}` && mayRedact && (
            <Button
              variant="light"
              className="addcardbutton"
              onClick={() => setCardModalShow(true)}
            >
              <FaRegPlusSquare />
            </Button>
          )}
        </div>
      </div>
      <CreateCard
        show={cardModalShow}
        onHide={() => setCardModalShow(false)}
        roadmapId={roadmapinfo?.id}
        // onSave={handleAddCard}
        numberOfCards={cards.length > 0 ? cards[cards.length-1]?.order_position   : 1}
      />
      <EditRoadmap
        show={roadmapModalShow}
        onHide={() => setRoadmapModalShow(false)}
        initialData={roadmapinfo}
      />
    </div>
  );
};

export default CardsPage;
