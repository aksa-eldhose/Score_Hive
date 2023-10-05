import axios from "axios";

//fetching team details
export const roundList = () => {
    return axios.get('/round/rounds/')
}
export const tournamentRoundList = (id) => {
    return axios.get(`/round/${id}/rounds/`)
}
export const addRound = (data) => {
    return axios.post('/round/addRound/',data)
}
export const removeTournamentRound = (data) => {
    return axios.put('/round/remove/',data)
}

export const tournamentRoundListPages = (id,request) => {
    return axios.get('/round/'+id+'/rounds/?page='+request)

}