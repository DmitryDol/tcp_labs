import React, { useState, useRef, useEffect } from "react";
import { useLocation, useParams } from "react-router-dom";
import Header from "../components/Header";
import CardView from "../components/CardView";
import { Button, Form, Card } from "react-bootstrap";
import { BsBookmark, BsBookmarkFill } from "react-icons/bs";
import { FaRegPlusSquare } from "react-icons/fa";
import CardModal, { CreateCard } from "../components/Cardredact";
import "./CardsPage.css";
import { minioAPI, roadmapAPI, userRoadmapAPI } from "../api/api";

const CardsPage = () => {
  let [isBookmarked, setIsBookmarked] = useState(false);
  const [modalShow, setModalShow] = useState(false);
  const location = useLocation();
  const { id } = useParams();
  const [background, setBackground] = useState();
  const [roadmapinfo, setRoadmapinfo] = useState();

  useEffect(() => {
    const getBackground = async () => {
    let filename = await userRoadmapAPI.getBackgroundFilename(id);
    if (filename===undefined)
    {filename = import.meta.env.VITE_DEFAULT_BACKGROUND}
    const imageurl = minioAPI.getImageUrl(filename, "backgrounds");
    console.log(filename)
    setBackground(imageurl);
    };
    const getRoadmapInfo = async () =>{
        const roadmap = await roadmapAPI.getRoadmapById(id);
        setRoadmapinfo(roadmap);
    };
    getBackground();
    getRoadmapInfo();
  }, [id]);
  useEffect(() => {
    console.log(roadmapinfo);
  }, [roadmapinfo]);

  const handleBookmark = () => {
    setIsBookmarked(!isBookmarked);
  };

  if (location.pathname === "/myroadmaps/cards") {
    isBookmarked = true;
  }
  const mayRedact = true;
  const handleCreateCard = () => {};

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
          {roadmapinfo?.cards?.map((card, index) => (
          <CardView key={index} cardInfo={card} mayRedact={roadmapinfo?.edit_permission==="view only"}/>
        ))}
          {location.pathname === "/myroadmaps/cards" && mayRedact && (
            <Button
              variant="light"
              className="addcardbutton"
              onClick={() => setModalShow(true)}
            >
              <FaRegPlusSquare />
            </Button>
          )}
        </div>
      </div>
      <CreateCard
        show={modalShow}
        onHide={() => setModalShow(false)}
        onSave={handleCreateCard}
      />
    </div>
  );
};

export default CardsPage;
