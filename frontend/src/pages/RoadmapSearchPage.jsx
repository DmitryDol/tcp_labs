import React, { useState, useRef, useEffect} from "react";
import Header from "../components/Header";
import RoadmapView from "../components/RoadmapView";
import { Pagination } from "react-bootstrap";
import { Button, Form } from "react-bootstrap";
import { FaSearch } from 'react-icons/fa';
import { roadmapAPI } from "../api/api";
import "./RoadmapSearchPage.css"


const RoadmapSearchPage = () => {

  const itemsPerPage = 6;
  const [roadmaps, setRoadmaps] = useState([]);
  useEffect(() => {
    const fetchRoadmaps = async () => {
      const roadmapsData = await roadmapAPI.getPublic(itemsPerPage,0); 
      setRoadmaps(roadmapsData);
    }
    fetchRoadmaps();
  }, [itemsPerPage]); 
  
  const [activePage, setActivePage] = useState(1);

  const indexOfLastItem = activePage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentRoadmaps = roadmaps.slice(indexOfFirstItem, indexOfLastItem);

  const totalPages = Math.ceil(roadmaps.length / itemsPerPage);

  const handlePageChange = (pageNumber) => {
    setActivePage(pageNumber);
  };

  const [searchText, setSearchText] = useState('');
    
  
  const handleInputChange = (e) => {
    setSearchText(e.target.value);
  };
    
  const handleSearch = () => {
    alert(searchText);
    //тут логика поиска по названию
    setSearchText('');
  };

    return(
      <>
        <Header showButtons={true}/>
        <div style={{ 
        maxWidth: '600px', 
        margin: '20px auto' 
        }}>
         <Form className="d-flex">
            <Form.Control
              type="search"
              placeholder="Поиск роадмапов"
              className="me-2"
              aria-label="Search"
              onChange={handleInputChange}
              value={searchText}
            />
            <Button className="searchbutton" onClick={handleSearch}> <FaSearch /></Button>
          </Form>
        </div>
        <div className="roadmaps-container">
        {currentRoadmaps.map((roadmap, index) => (
          <RoadmapView 
            key={index + indexOfFirstItem}
            roadmapData = {roadmap}
          />
        ))}
        </div>
        <hr style={{ opacity: '.75', marginLeft: '20px', marginRight: '20px'}}/>
        <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
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
    )
}

export default RoadmapSearchPage;