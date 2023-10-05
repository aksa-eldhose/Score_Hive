import axios from "axios";
/**send verification link to the user's email */
export const sendEmail = (data) => {
    return axios.post('/accounts/register/', data)
}
export const sendForgotEmail = (data) => {
    return axios.post('/accounts/forgotPassword/', data)
}
export const ChangePassword = (data) => {
    return axios.patch('/accounts/changePassword/', data)
}
export const checkCurrentPassword = (data) => {
    return axios.post('accounts/checkCurrentPassword/', data)
}
/*Email verification after clicking on the link for registration */
export const verifyEmail = (data) => {
    return axios.post('/accounts/registerTokenVerify/', data)
}
/*Users details registration */
export const register = (data) => {
    return axios.post('/accounts/registerUserDetails/', data)
}
export const sendToken = (data) => {
    return axios.post('/accounts/resetPasswordToken/', data)
}
export const Forgotpassword = (data) => {
    return axios.post('/accounts/resetPassword/', data)
}
export const login = (data) => {
    return axios.post('accounts/login/', data)
}
export const logout = () => {
    localStorage.clear();
    // Clear browser history
    window.history.pushState({}, '', '/');
    window.history.replaceState({}, '', '/');
    window.history.go(0);
    
}
//Fetching currently logged in user details
export const userProfile = () => {
    return axios.get('accounts/getUserDetails/')
}
//Editing the logged in users profile
export const userProfileEdit = (data) => {
    return axios.patch('accounts/getUserDetails/', data)
}
//fetching team details
export const teamList = () => {
    return axios.get('/team/teams/')
}
//fetching paginated team list
export const teamListPages = (request) => {
    return axios.get('/team/teams/?page='+request)
}
//delete the spacific team details
export const teamDelete = (teamId) =>{
    return axios.delete('/team/teams/?id='+teamId)
}

