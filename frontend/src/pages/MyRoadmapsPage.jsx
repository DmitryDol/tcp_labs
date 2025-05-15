import React, { useState, useRef } from "react";
import Header from "../components/Header";
import RoadmapView from "../components/RoadmapView";
import CreateRoadmap from "../components/RoadmapRedact";
import { Pagination } from "react-bootstrap";
import { Button, Form } from "react-bootstrap";
import "./RoadmapSearchPage.css";

const background =
  "https://i.pinimg.com/736x/35/a8/19/35a8199c0fffa403c3b03fc5680c5041.jpg";
const background2 =
  "https://repository-images.githubusercontent.com/185094183/ff64fd00-706f-11e9-9b53-d05acb2d0989";

const MyRoadmapsPage = () => {
  const allRoadmaps = [];
  const totalRoadmaps = 3;

  for (let i = 0; i < totalRoadmaps; i++) {
    allRoadmaps.push({
      backgroundUrl: i % 2 === 0 ? background : background2,
      roadmapTitle: "hhhhhhhhhhhhhhhhh",
    });
  }
  const itemsPerPage = 6;
  const [activePage, setActivePage] = useState(1);

  const indexOfLastItem = activePage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentRoadmaps = allRoadmaps.slice(indexOfFirstItem, indexOfLastItem);

  const totalPages = Math.ceil(allRoadmaps.length / itemsPerPage);

  const handlePageChange = (pageNumber) => {
    setActivePage(pageNumber);
  };

  const [modalShow, setModalShow] = React.useState(false);

  const handleCreateRoadmap=()=>{

  }

  return (
    <>
      <Header showButtons={true} />
      <div
        style={{
          margin: "20px auto",
          display: "flex",
          justifyContent: "center",
        }}
      >
        <Button
          variant="outline-light"
          style={{
            "--bs-btn-hover-bg": "blueviolet",
            "--bs-btn-hover-color": "white",
          }}
          onClick={() => setModalShow(true)}
        >
          Создать роадмап
        </Button>
        <CreateRoadmap 
        show={modalShow}
        onHide={() => setModalShow(false)}
        onSave={handleCreateRoadmap}
        />
      </div>
      <div className="roadmaps-container">
        {currentRoadmaps.map((roadmap, index) => (
          <RoadmapView
            key={index + indexOfFirstItem}
            backgroundUrl={roadmap.backgroundUrl}
            roadmapTitle={roadmap.roadmapTitle}
          />
        ))}
      </div>
      <hr style={{ opacity: ".75", marginLeft: "20px", marginRight: "20px" }} />
      <div
        style={{ display: "flex", justifyContent: "center", marginTop: "20px" }}
      >
        <Pagination>
          {[...Array(totalPages)].map((_, index) => (
            <Pagination.Item
              key={index + 1}
              active={index + 1 === activePage}
              onClick={() => handlePageChange(index + 1)}
            >
              {index + 1}
            </Pagination.Item>
          ))}
        </Pagination>
      </div>
    </>
  );
};

export default MyRoadmapsPage;
