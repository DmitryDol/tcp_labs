import React, { useState, useEffect } from "react";
import Header from "../components/Header";
import RoadmapView from "../components/RoadmapView";
import { Pagination } from "react-bootstrap";
import { Button, Form } from "react-bootstrap";
import { FaSearch } from 'react-icons/fa';
import { roadmapAPI } from "../api/api";
import "./RoadmapSearchPage.css"

const RoadmapSearchPage = () => {
  const itemsPerPage = 1;
  const [roadmaps, setRoadmaps] = useState([]);
  const [activePage, setActivePage] = useState(1);
  const [searchText, setSearchText] = useState('');
  const [searchQuery, setSearchQuery] = useState(''); 
  
  useEffect(() => {
    const fetchRoadmaps = async () => {
      const params = {
        "limit": itemsPerPage,
        "page": activePage
      };
      
      if (searchQuery) {
        params.search = searchQuery;
      }
      const roadmapsData = await roadmapAPI.getPublic(params);
      setRoadmaps(roadmapsData);
    }
    fetchRoadmaps();
  }, [itemsPerPage, activePage, searchQuery]); 
  

  const handleInputChange = (e) => {
    const newValue = e.target.value;
    setSearchText(newValue);
    
    if (newValue === '' && searchQuery !== '') {
      setSearchQuery('');
      setActivePage(1);
    }
  };
    
  const handleSearch = () => {
    setSearchQuery(searchText);
    setActivePage(1);
  };
  
  const handleClear = () => {
    setSearchText('');
    setSearchQuery('');
    setActivePage(1);
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
          <Button className="searchbutton" onClick={handleSearch}><FaSearch /></Button>
          {searchText && (
            <Button variant="outline-secondary" onClick={handleClear} className="ms-1">✕</Button>
          )}
        </Form>
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
            <p>Роадмапы не найдены</p>
          </div>
        )}
      </div>
      <hr style={{ opacity: '.75', marginLeft: '20px', marginRight: '20px'}}/>
      <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
        <Pagination>
          {roadmaps.total_pages > 0 && [...Array(roadmaps.total_pages)].map((_, index) => (
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
  )
}

export default RoadmapSearchPage;
