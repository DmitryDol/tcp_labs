import axios from "axios";

const apiClient = axios.create({
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

// перехватчики для токенов авторизации
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("accessToken");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      try {
        const response = await axios.post("/api/core/auth/refresh");
        localStorage.setItem("accessToken", response.data.access_token);
        // Повторяем исходный запрос с новым токеном
        return apiClient(error.config);
      } catch (refreshError) {
        // Если не удалось обновить токен, перенаправляем на логин
        localStorage.removeItem("accessToken");
        localStorage.removeItem("userData");
        window.location = "/";
      }
    }
    return Promise.reject(error);
  }
);

const handleError = (error, context) => {
  console.error(`Error ${context}:`, error.response?.data || error.message);
  throw error;
};


// --- Core Service (Python Backend - /api/core) ---

// --- Auth ---
export const authAPI = {
  create: async (name, login, password) => {
    try {
      const userData = { name: name, login: login, password_hash: password };
      const response = await apiClient.post("/api/core/auth", userData);
      return response.data;
    } catch (error) {
      handleError(error, "registering");
    }
  },
  login: async (credentials) => {
    try {
      const response = await apiClient.post(
        "/api/core/auth/token",
        new URLSearchParams(credentials),
        { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
      );

      localStorage.setItem("accessToken", response.access_token);
      const userData = {
        id: response.data.id,
        login: response.data.login,
        username: response.data.username,
      };

      localStorage.setItem("userData", JSON.stringify(userData));
      localStorage.setItem("avatar", response.data.avatar);
      return response.data;
    } catch (error) {
      handleError(error, "logging in");
    }
  },
  logout: async () => {
    try {
      localStorage.removeItem("accessToken");
      const response = await apiClient.post("/api/core/auth/logout");

      localStorage.removeItem("userData");
      // console.log(response.data);
      return response.data;
    } catch (error) {
      handleError(error, "loging out");
    }
  },
  getCurrentUser: async () => {
    try {
      const response = await apiClient.get("/api/core/auth/me");
      const userData = {
        login: response.data.login,
        username: response.data.username,
        id: response.data.id
      };
      localStorage.setItem("userData", JSON.stringify(userData));
    } catch (error) {
      handleError(error, "getting current user");
    }
  },
};

// --- Users ---
export const userAPI = {
  getUserInfo: async () => {
    try {
      const response = await apiClient.get("/api/core/users");
      userData = {
        id: response.data.user_id,
        login: response.data.login,
        username: response.data.username,
      };
      localStorage.setItem("userData", JSON.stringify(userData));
      localStorage.setItem("avatar", response.data.avatar);
      return response.data;
    } catch (error) {
      handleError(error, "getting user info");
    }
  },
  deleteUser: async () => {
    try {
      const response = await apiClient.delete("/api/core/users");
      return response.data;
    } catch (error) {
      handleError(error, "deleting user");
    }
  },
  editUserInfo: async (name, password) => {
    try {
      const dataToUpdate = {};
      if (name !== undefined) {
        dataToUpdate.name = name;
      }
      if (password !== undefined) {
        dataToUpdate.password_hash = password;
      }
      const response = await apiClient.patch("/api/core/users", dataToUpdate);
      // Обновляем userData в localStorage, если бэкенд возвращает актуальные username и login
      // Предполагается, что бэкенд возвращает { login, username, ... }
      if (response.data && response.data.login && response.data.username) {
        const userData = {
          login: response.data.login,
          username: response.data.username,
        };
        localStorage.setItem("userData", JSON.stringify(userData));
      }
      return response.data;
    } catch (error) {
      handleError(error, "editing user info");
    }
  },
  changeUserAvatar: async (file) => {
    try {
      const currentAvatar = localStorage.getItem("avatar");
      if (currentAvatar != import.meta.env.VITE_DEFAULT_AVATAR) {
        await minioAPI.deleteImage(currentAvatar, "avatars");
      }
      const newAvatar = await minioAPI.uploadImage(file, "avatars");
      const response = await apiClient.put("/api/core/users/avatar", {
        avatar: newAvatar.filename,
      });
      localStorage.setItem("avatar", newAvatar.filename);

      if (!response.data?.avatar) {
        response.data.avatar = newAvatar.filename;
      }

      return response.data;
    } catch (error) {
      handleError(error, "changing user avatar");
    }
  },
  deleteUserAvatar: async () => {
    try {
      const currentAvatar = localStorage.getItem("avatar");
      if (currentAvatar != import.meta.env.VITE_DEFAULT_AVATAR) {
        await minioAPI.deleteImage(currentAvatar, "avatars");
      }
      await apiClient.delete("/api/core/users/avatar");
      const response = await apiClient.get("/api/core/users/avatar");
      localStorage.setItem("avatar", response.data?.avatar);
      return response.data;
    } catch (error) {
      handleError(error, "deleting user avatar");
    }
  },
};

// --- Roadmaps ---
export const roadmapAPI = {
  getPublic: async (searchParams = {}) => {
    try {
      const { search, difficulty, limit, page } = searchParams;

      const params = {};
      if (search) params.search = search;
      if (difficulty) params.difficulty = difficulty;
      if (limit) params.limit = limit;
      if (page) params.page = page;

      const response = await apiClient.get("/api/core/roadmaps/public", {
        params,
      });
      return response.data;
    } catch (error) {
      handleError(error, "getting public roadmaps");
    }
  },
  addRoadmap: async (
    ownerId,
    title,
    description,
    difficulty,
    editPermission,
    visibility
  ) => {
    try {
      const roadmapData = {
        owner_id: ownerId,
        title,
        description,
        difficulty,
        edit_permission: editPermission,
        visibility,
      };
      const response = await apiClient.post("/api/core/roadmaps", roadmapData);
      return response.data;
    } catch (error) {
      handleError(error, "adding roadmap");
    }
  },
  getRoadmapById: async (roadmapId) => {
    try {
      const response = await apiClient.get(`/api/core/roadmaps/${roadmapId}`);
      return response.data;
    } catch (error) {
      handleError(error, "getting roadmap details");
    }
  },
  editRoadmap: async (
    roadmapId,
    title,
    description,
    difficulty,
    editPermission,
    visibility
  ) => {
    try {
      const roadmapData = {};
      if (title !== undefined) roadmapData.title = title;
      if (description !== undefined) roadmapData.description = description;
      if (difficulty !== undefined) roadmapData.difficulty = difficulty;
      if (editPermission !== undefined)
        roadmapData.edit_permission = editPermission;
      if (visibility !== undefined) roadmapData.visibility = visibility;
      const response = await apiClient.patch(
        `/api/core/roadmaps/${roadmapId}`,
        roadmapData
      );
      return response.data;
    } catch (error) {
      handleError(error, "editing roadmap");
    }
  },
  deleteRoadmap: async (roadmapId) => {
    try {
      await apiClient.delete(`/api/core/roadmaps/${roadmapId}`);
      return true;
    } catch (error) {
      handleError(error, "deleting roadmap");
      return false;
    }
  },
};

// --- User Roadmaps ---
export const userRoadmapAPI = {
  getLinkedRoadmaps: async (searchParams = {}) => {
    try {
      const { search, difficulty, limit, page } = searchParams;

      const params = {};
      if (search) params.search = search;
      if (difficulty) params.difficulty = difficulty;
      if (limit) params.limit = limit;
      if (page) params.page = page;

      const response = await apiClient.get("/api/core/user_roadmaps", {
        params,
      });
      return response.data;
    } catch (error) {
      handleError(error, "getting linked to user roadmaps");
    }
  },
  linkUserToRoadmap: async (roadmapId) => {
    try {
      const response = await apiClient.post(
        `/api/core/user_roadmaps/${roadmapId}`
      );
      return response.data;
    } catch (error) {
      handleError(error, "linking user to roadmap");
    }
  },
  unlinkUserFromRoadmap: async (roadmapId) => {
    try {
      await apiClient.delete(`/api/core/user_roadmaps/${roadmapId}`);
      return true;
    } catch (error) {
      handleError(error, "unlinking user from roadmap");
    }
  },
  getBackgroundFilename: async (roadmapId) => {
    try {
      const response = await apiClient.get(
        `/api/core/user_roadmaps/${roadmapId}/background`
      );
      return response?.data?.background;
    } catch (error) {
      handleError(error, "getting background filename");
    }
  },
  changeRoadmapBackground: async (roadmapId, file) => {
    try {
      const currentBackground = await userRoadmapAPI.getBackgroundFilename(roadmapId);
      if (currentBackground !== import.meta.env.VITE_DEFAULT_BACKGROUND) {
        await minioAPI.deleteImage(currentBackground, "backgrounds");
      }
      const background = await minioAPI.uploadImage(file, "backgrounds");
      console.log(background);
      console.log(roadmapId);
      const response = await apiClient.put(
        `/api/core/user_roadmaps/${roadmapId}/background`,
        {"background": background.filename }
      );
      return response.data;
    } catch (error) {
      handleError(error, "changing roadmap background");
    }
  },
};

// --- Cards ---
// TODO: Add functions for cards (createCard, fetchCard, updateCard, deleteCard)
export const cardAPI = {
  addCard: async (roadmapId, title, description, orderPosition) => {
    try {
      const cardData = {
        roadmap_id: roadmapId,
        title,
        description,
        order_position: orderPosition,
      };
      const response = await apiClient.post("/api/core/cards", cardData);
      return response.data;
    } catch (error) {
      handleError(error, "adding card");
    }
  },
  getCard: async (cardId) => {
    try {
      const response = await apiClient.get(`/api/core/cards/${cardId}`);
      return response.data;
    } catch (error) {
      handleError(error, "getting card info");
    }
  },
  deleteCard: async (cardId) => {
    try {
      const response = await apiClient.delete(`/api/core/cards/${cardId}`);
      return response.data;
    } catch (error) {
      handleError(error, "deleting card");
    }
  },
  editCard: async (cardId, title, description, orderPosition) => {
    try {
      const cardEditData = {};
      if (title !== undefined) cardEditData.title = title;
      if (description !== undefined) cardEditData.description = description;
      if (orderPosition !== undefined)
        cardEditData.order_position = orderPosition;
      const response = await apiClient.patch(
        `/api/core/cards/${cardId}`,
        cardEditData
      );
      return response.data;
    } catch (error) {
      handleError(error, "editing card");
    }
  },
};

// --- Card Links ---
// TODO: Add functions for card links (createCardLink, deleteCardLink)
export const cardLinkAPI = {
  deleteLinkFromCard: async (cardLinkId) => {
    try {
      const response = await apiClient.delete(
        `/api/core/card_links/${cardLinkId}`
      );
      return response.data;
    } catch (error) {
      handleError(error, "deleting card link");
    }
  },
  editCardLink: async (cardLinkId, linkTitle, linkContent) => {
    try {
      const cardLinkData = {};
      if (linkTitle !== undefined) cardLinkData.link_title = linkTitle;
      if (linkContent !== undefined) cardLinkData.link_content = linkContent;
      const response = await apiClient.patch(
        `/api/core/card_links/${cardLinkId}`,
        cardLinkData
      );
      return response.data;
    } catch (error) {
      handleError(error, "editing card link");
    }
  },
  addCardLink: async (cardId, linkTitle, linkContent) => {
    try {
      const cardLinkData = {
        card_id: cardId,
        link_title: linkTitle,
        link_content: linkContent,
      };
      const response = await apiClient.post("/api/core/card_links", cardLinkData);
      return response.data;
    } catch (error) {
      handleError(error, "adding card link");
    }
  },
};

// --- User Card ---
export const userCardAPI = {
  editCardStatus: async (cardId, cardStatus) => {
    try {
      const editUserCardData = {
        status: cardStatus,
        card_id: cardId
      }
      const response = await apiClient.put('/api/core/user_cards/status', editUserCardData)
      return response.data
    } catch (error) {
      handleError(error, "changing user card status")
    }
  }
}

// --- Image Service (Java Backend - /api/images) ---

export const minioAPI = {
  uploadImage: async (file, bucket) => {
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await apiClient.post(
        `http://localhost:8080/files/${bucket}`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      return response.data;
    } catch (error) {
      handleError(error, `uploading image to bucket ${bucket}`);
    }
  },
  getImageUrl: (filename, bucket = "avatars") => {
    if (!filename) return null;

    return `http://localhost:8080/files/${bucket}/${filename}`;
  },
  deleteImage: async (filename, bucket = "avatars") => {
    try {
      const response = await apiClient.delete(
        `http://localhost:8080/files/${bucket}/${filename}`
      );
      return response.data;
    } catch (error) {
      handleError(error, `deleting image ${filename} from bucket ${bucket}`);
    }
  },
};
/*
// Функция для получения URL изображения
// Мы не делаем запрос через axios, так как URL должен использоваться напрямую в <img> тегах
// Предполагается, что GET /api/images/files/{bucket}/{filename} доступен без явной передачи токена в заголовке,
// если используется аутентификация через куки (withCredentials=true должен помочь браузеру отправить куки)
export const getImageUrl = (filename, bucket = "avatars") => {
  if (!filename) return null; // Или вернуть URL плейсхолдера
  // Собираем URL, который будет обработан прокси Vite
  // Формат соответствует GET /files/{bucket}/{filename} в Java FileController
  // if (cache.has(filename)){
  //     return cache.get(filename)
  // }

  return `/api/images/files/${bucket}/${filename}`;
};

*/
