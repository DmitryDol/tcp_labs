//TODO change ```create: async (userData) => {``` and other to ```create: async (name, login, password) => {``` and other

import axios from "axios";
import { useNavigate } from "react-router-dom";

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
        const navigate = useNavigate();
        navigate("/");
      }
    }
    return Promise.reject(error);
  }
);

// Обработчик ошибок для вывода в консоль и проброса дальше
const handleError = (error, context) => {
  // Axios автоматически обрабатывает не-2xx коды как ошибки
  console.error(`Error ${context}:`, error.response?.data || error.message);
  // Пробрасываем ошибку, чтобы компонент мог ее обработать (например, показать сообщение пользователю)
  throw error;
};

const cache = new Map();

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
        login: response.data.login,
        username: response.data.username,
      };

      localStorage.setItem("userData", JSON.stringify(userData));
      localStorage.setItem("avatar", response.data.avatar)
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
      console.log(response.data);
      return response.data;
    } catch (error) {
      handleError(error, "loging out");
    }
  },
  getCurrentUser: async () => {
    try {
      const response = await apiClient.get("/api/core/auth/me");
      userData = {
        login: response.data.login,
        username: response.data.username,
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
        login: response.data.login,
        username: response.data.username,
      };
      localStorage.setItem("userData", JSON.stringify(userData));
      localStorage.setItem("avatar", response.data.avatar)
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
      // currentAvatar = userAPI.getUserInfo().avatar
      const currentAvatar = localStorage.getItem('avatar')
      if (currentAvatar && currentAvatar !== import.meta.env.VITE_DEFAULT_AVATAR_FILENAME) {
        await minioAPI.deleteImage(currentAvatar, "avatars");
      }
      const newAvatar = await minioAPI.uploadImage(file, "avatars");
      const response = await apiClient.put(
        `/api/core/users`,
        { avatar: newAvatar.filename }
      );
      localStorage.setItem('avatar', response.data.filename)
      return response.data;
    } catch (error) {
      handleError(error, "changing user avatar");
    }
  },
  deleteUserAvatar: async () => {
    try {
      const currentAvatar = localStorage.getItem("avatar")
      const defaultAvatar = import.meta.env.VITE_DEFAULT_AVATAR_FILENAME
      if (currentAvatar && currentAvatar !== defaultAvatarFilename) {
        await minioAPI.deleteImage(currentAvatar, "avatars");
      }
      const response = await apiClient.patch(
        `/api/core/users`,
        { avatar: defaultAvatarFilename }
      );
      localStorage.setItem('avatar', defaultAvatarFilename);
      return response.data;
    } catch (error) {
      handleError(error, "deleting user avatar")
    }
  }
};

// --- Roadmaps ---
export const roadmapAPI = {
  getPublic: async (searchParams = {}) => {
    try {
      const { search, difficulty, limit } = searchParams;

      const params = {};
      if (search) params.search = search;
      if (difficulty) params.difficulty = difficulty;
      if (limit) params.limit = limit;

      const response = await apiClient.get("/api/core/roadmaps", { params });
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
      const { search, difficulty, limit } = searchParams;

      const params = {};
      if (search) params.search = search;
      if (difficulty) params.difficulty = difficulty;
      if (limit) params.limit = limit;

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
  unlinkUserFromRoadmap: async (roadmapId, userId) => {
    try {
      await apiClient.delete(
        `/api/core/user_roadmaps/${roadmapId}/users/${userId}`
      );
      return true;
    } catch (error) {
      handleError(error, "unlinking user from roadmap");
    }
  },
  getBackground: async (roadmapId) => {
    try {
      const response = await apiClient.get(
        `/api/core/user_roadmaps/${roadmapId}/background`
      );
      
      return minioAPI.getImageUrl(response.data.background, "backgrounds");
    } catch (error) {
      handleError(error, "getting background filename");
    }
  },
  changeRoadmapBackground: async (roadmapId, file) => {
    try {
      currentBackground = userRoadmapAPI.getBackgroundFilename(roadmapId);
      await minioAPI.deleteImage(currentBackground, "avatars");
      const background = await minioAPI.uploadImage(file, "backgrounds").filename;
      const response = await apiClient.put(
        `/api/core/user_roadmaps/${roadmapId}/background`,
        { background }
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
      const response = apiClient.post("/api/core/card_links", cardLinkData);
      return response.data;
    } catch (error) {
      handleError(error, "adding card link");
    }
  },
};

// --- Image Service (Java Backend - /api/images) ---

export const minioAPI = {
  uploadImage: async (file, bucket) => {
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await apiClient.post(
        `/api/images/files/${bucket}`,
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

    return `/api/images/files/${bucket}/${filename}`;
  },
  deleteImage: async (filename, bucket = "avatars") => {
    try {
      const response = await apiClient.delete(
        `/api/images/files/${bucket}/${filename}`
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
