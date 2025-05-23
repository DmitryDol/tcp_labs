import React, { useState, useRef, useEffect } from "react";
import Header from "../components/Header";
import RoadmapView from "../components/RoadmapView";
import CreateRoadmap from "../components/RoadmapRedact";
import { Pagination } from "react-bootstrap";
import { Button, Form } from "react-bootstrap";
import "./RoadmapSearchPage.css";
import { userRoadmapAPI } from "../api/api";

const MyRoadmapsPage = () => {
  const itemsPerPage = 2;
  const [roadmaps, setRoadmaps] = useState([]);
  const [activePage, setActivePage] = useState(1);
  
  useEffect(() => {
    const fetchRoadmaps = async () => {
      const params = {
        limit: itemsPerPage,
        page: activePage,
      };
      const roadmapsData = await userRoadmapAPI.getLinkedRoadmaps(params);
      setRoadmaps(roadmapsData);
    };
    fetchRoadmaps();
  }, [itemsPerPage, activePage, roadmaps]);

  const removeRoadmap = (id) => {
    setRoadmaps((prev) => {
      const updated = {
        ...prev,
        roadmaps: prev.roadmaps.filter((r) => r.id !== id),
      };
      if (updated.roadmaps.length === 0 && activePage > 1) {
        setActivePage(activePage - 1);
      }
      return updated;
    });
  };
  const handleAddRoadmap = (newRoadmap) => {
  setRoadmaps((prev) => ({
    ...prev,
    roadmaps: [...(prev.roadmaps || []), newRoadmap], 
  }));
  };

  const [modalShow, setModalShow] = React.useState(false);

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
          onSave={handleAddRoadmap}
        />
      </div>
      <div className="roadmaps-container">
        {roadmaps.roadmaps?.length > 0 ? (
          roadmaps.roadmaps.map((roadmap, index) => (
            <RoadmapView 
              key={roadmap.id || index}
              roadmapData={roadmap}
              onRemove={removeRoadmap}
            />
          ))
        ) : (
          <div className="text-center w-100 my-5">
            <p>У вас еще нет добавленных роадмапов</p>
          </div>
        )}
      </div>
      <hr style={{ opacity: ".75", marginLeft: "20px", marginRight: "20px" }} />
      <div
        style={{ display: "flex", justifyContent: "center", marginTop: "20px" }}
      >
      <Pagination>
        {roadmaps.total_pages > 0 &&
          [...Array(roadmaps.total_pages)].map((_, index) => (
            <Pagination.Item
              key={index + 1}
              active={index + 1 === activePage}
              onClick={() => setActivePage(index + 1)}
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
