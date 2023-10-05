import axios from "axios";
export const playerList = (id) => {
    return axios.get('/player/listPlayers/' + id)
}

export const playerCheck = (data) => {
    return axios.post('/player/checkIfTeamMember/', data)
}

export const playerJoinTeam = (data) => {
    return axios.post('/player/joinToTeam/', data)
}

export const searchPlayer = (data) => {
    return axios.post('/player/searchPlayer/', data)
}

export const invitePlayer = (data) => {
    return axios.post('/player/invitePlayer/', data)
}

export const addPlayer = (data) => {
    return axios.post('/player/addtoPlayertoTeam/', data)
}
export const removePlayer = (data) => {
    return axios.put('/player/removeFromTeam/', data)
}