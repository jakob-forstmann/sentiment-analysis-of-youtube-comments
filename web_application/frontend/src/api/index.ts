import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

export const connectApi = () => API.get(`/`);

export const fetchAllCommentsFromVideo = (videoId) => API.get(`fetch_all_comments/${videoId}`);
