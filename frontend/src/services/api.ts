import axios from 'axios';

const API = 'http://localhost:8000/api';

export interface ProductInput {
  product_title: string;
  about_this_product: string;
  product_description: string;
  image_url?: string;
}

export const generatePrompt = async (input: ProductInput) => {
  const res = await axios.post(`${API}/generate`, input);
  return res.data;
};

export const getHistory = async () => {
  const res = await axios.get(`${API}/history`);
  return res.data.history || [];
};

export const deleteGeneration = async (id: string) => {
  await axios.delete(`${API}/history/${id}`);
};

export const deleteAllHistory = async () => {
  await axios.delete(`${API}/history`);
};
