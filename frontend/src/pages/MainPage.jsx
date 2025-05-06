import React from "react";
import Header from "../components/Header";


const avatarUrl = "https://i0.wp.com/sbcf.fr/wp-content/uploads/2018/03/sbcf-default-avatar.png?ssl=1";

const MainPage = () => {
  return (
    <div>
      <Header
        showButtons={true}
        avatarUrl={avatarUrl}
      />
      {/* Содержимое главной страницы */}
    </div>
  );
};


export default MainPage;
