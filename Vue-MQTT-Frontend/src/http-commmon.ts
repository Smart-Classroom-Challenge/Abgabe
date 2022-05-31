import type { AxiosInstance } from 'axios'
import axios from 'axios'
const apiClient: AxiosInstance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}/api`,
  headers: {
    'Content-type': 'application/json',
  },
})
export default apiClient
