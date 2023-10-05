import axios from "axios";

export const createTeam = (data) => {
    return axios.post('/team/teams/', data)
}

export const updateTeam = (data, id) => {
    return axios.put('/team/teams/?id=' + id, data)
}

export const getCity = () => {
    return axios.get('/team/cities/')
}

export const getTeamDetail = (id) => {
    return axios.get('/team/teams/' + id)
}

//get joined team details
export const getJoinedTeams = () => {
    return axios.get('/team/playingTeams/')
}

//Exist from joined team
export const exitFromTeam = (teamId) => {
    return axios.put('/player/'+teamId+'/exitFromTeam/')
}

