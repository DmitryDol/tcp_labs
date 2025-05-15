import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import AuthPage from "./pages/AuthPage";
import RegisterPage from "./pages/RegisterPage";
import MainPage from "./pages/MainPage";
import EditProfilePage from "./pages/EditProfilePage"
import RoadmapSearchPage from "./pages/RoadmapSearchPage"
import 'bootstrap/dist/css/bootstrap.min.css';
import CardsPage from "./pages/CardsPage";
import MyRoadmapsPage from "./pages/MyRoadmapsPage";


const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AuthPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/mainpage" element={<MainPage />} />
        <Route path="/editprofile" element={<EditProfilePage />} />
        <Route path="/roadmapsearch" element={<RoadmapSearchPage />} />
        <Route path="/roadmapsearch/cards" element={<CardsPage />} />
        <Route path="/myroadmaps/cards" element={<CardsPage />} />
        <Route path="/myroadmaps" element={<MyRoadmapsPage />} />
      </Routes>
    </Router>
  );
};

export default App;
