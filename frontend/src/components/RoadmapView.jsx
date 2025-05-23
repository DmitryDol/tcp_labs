import React, { useState, useEffect } from "react";
import Card from "react-bootstrap/Card";
import { Accordion, Button, Dropdown } from "react-bootstrap";
import { useLocation } from "react-router-dom";
import {
  BsBookmark,
  BsBookmarkFill,} from "react-icons/bs";
import { PiTrashBold } from "react-icons/pi";
import "./RoadmapView.css";
import { minioAPI, userRoadmapAPI } from "../api/api";

function RoadmapView({ roadmapData, onRemove}) {
  const location = useLocation();
  const pathWithCards = `${location.pathname}/${roadmapData.id}`;
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [background, setBackground] = useState();
  const isMade = (roadmapData.owner_id == JSON.parse(localStorage.getItem("userData")).id);

  useEffect(() => {
    const getBackground = async () => {
      const filename = await userRoadmapAPI.getBackgroundFilename(
        roadmapData.id
      );
      const imageurl = minioAPI.getImageUrl(filename, "backgrounds");
      setBackground(imageurl);
    };
    getBackground();
  }, [roadmapData.id]);

  useEffect(() => {
    const checkLinked = async () => {
      let linkedRoadmaps = await userRoadmapAPI.getLinkedRoadmaps();
      const linkedIds = Object.values(linkedRoadmaps.roadmaps).map(
        (item) => item.id
      );
      setIsBookmarked(linkedIds.includes(roadmapData.id));
    };
    checkLinked();
  }, [roadmapData.id]);

  const handleBookmark = async () => {
    if (isBookmarked == false) {
      await userRoadmapAPI.linkUserToRoadmap(roadmapData.id);
      setIsBookmarked(true);
    } else {
      await userRoadmapAPI.unlinkUserFromRoadmap(roadmapData.id);
      setIsBookmarked(false);
    }
  };

  const handleUnsubscribe = async () => {
    await userRoadmapAPI.unlinkUserFromRoadmap(roadmapData.id);
    onRemove(roadmapData.id);

  };

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
              {roadmapData.title}
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
            <Card.Text>{roadmapData.difficulty}</Card.Text>
            {location.pathname === "/myroadmaps" ? (
              <Button
                className="roadmap-button"
                variant="outline-dark"
                onClick={handleUnsubscribe}
              >
                <PiTrashBold />
              </Button>
            ) : (
              !isMade && (
                <Button
                  className="roadmap-button"
                  variant="outline-dark"
                  onClick={handleBookmark}
                >
                  {isBookmarked ? <BsBookmarkFill /> : <BsBookmark />}
                </Button>
              )
            )}
            
          </Card.Footer>
        </Card.Body>
        <Card.Img src={background} alt="Card image" className="cardimg" />
      </div>
      <Accordion>
        <Accordion.Item eventKey="0">
          <Accordion.Header>Описание</Accordion.Header>
          <Accordion.Body>{roadmapData.description}</Accordion.Body>
        </Accordion.Item>
      </Accordion>
    </Card>
  );
}

export default RoadmapView;
