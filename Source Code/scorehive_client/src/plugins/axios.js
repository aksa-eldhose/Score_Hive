"use strict";
import axios from "axios";
axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL;
let Access_Token = localStorage.getItem('Access_Token')

axios.defaults.headers.common['Authorization'] = `Bearer ${Access_Token}`;
axios.defaults.headers.post['Content-Type'] = 'application/json';

// intercept every request
axios.interceptors.request.use(
  (config) => {
    // get access token from local storage
    
     Access_Token = localStorage.getItem('Access_Token')
    // if access token exists and request is not a login request
    if (Access_Token && config.url !== 'accounts/login/') {
      // append authorization header with access token
      config.headers.Authorization = `Bearer ${Access_Token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// intercept every response error
axios.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config
    // if error is due to access token expiry
    if (error.response.data.detail === "The token used is expired" && !originalRequest._retry) {
      originalRequest._retry = true
      // get refresh token from local storage
      const Refresh_Token = localStorage.getItem('Refresh_Token')
      try {
        // call an API to get new access token using refresh token
        const response = await axios.post('accounts/accessTokenRefresh/', { refresh: Refresh_Token })
        // save new access token to local storage
        localStorage.setItem('Access_Token', response.data.access)
        // append new access token to original request
        originalRequest.headers.Authorization = `Bearer ${response.data.access}`
        // retry original request
        return axios(originalRequest)
      } catch (err) {
        localStorage.clear();
        window.location.reload();
        return Promise.reject(err)
      }
    }
    return Promise.reject(error)
  }
)

export default axios
