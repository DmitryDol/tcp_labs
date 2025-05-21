import React, { useState, useRef, useEffect } from "react";
import Header from "../components/Header";
import RoadmapView from "../components/RoadmapView";
import CreateRoadmap from "../components/RoadmapRedact";
import { Pagination } from "react-bootstrap";
import { Button, Form } from "react-bootstrap";
import "./RoadmapSearchPage.css";
import { userRoadmapAPI } from "../api/api";

const background =
  "https://i.pinimg.com/736x/35/a8/19/35a8199c0fffa403c3b03fc5680c5041.jpg";
const background2 =
  "https://repository-images.githubusercontent.com/185094183/ff64fd00-706f-11e9-9b53-d05acb2d0989";

const MyRoadmapsPage = () => {
  const itemsPerPage = 1;
  const [roadmaps, setRoadmaps] = useState([]);
  const [activePage, setActivePage] = useState(1);
  const [searchText, setSearchText] = useState("");
  const [searchQuery, setSearchQuery] = useState("");

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
  }, [itemsPerPage, activePage]);

  const handlePageChange = (pageNumber) => {
    setActivePage(pageNumber);
  };

  const [modalShow, setModalShow] = React.useState(false);

  const handleCreateRoadmap = () => {};

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
        {roadmaps.roadmaps?.length > 0 ? (
          roadmaps.roadmaps.map((roadmap, index) => (
            <RoadmapView 
              key={roadmap.id || index}
              roadmapData={roadmap}
            />
          ))
        ) : (
          <div className="text-center w-100 my-5">
            <p>Вы еще не добавили себе роадмапов</p>
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
