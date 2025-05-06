import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import AuthPage from "./pages/AuthPage";
import RegisterPage from "./pages/RegisterPage";
import MainPage from "./pages/MainPage";
import EditProfilePage from "./pages/EditProfilePage"
import 'bootstrap/dist/css/bootstrap.min.css';


const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AuthPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/mainpage" element={<MainPage />} />
        <Route path="/editprofile" element={<EditProfilePage />} />
      </Routes>
    </Router>
  );
};

export default App;
