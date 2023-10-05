import axios from "axios";

/**Scedule a match*/
export const scheduleMatch = (data) => {
    return axios.post('/match/schedule/', data)
}

export const tournamentMatchList = (id) => {
    return axios.get(`/match/${id}/list/`)
}
export const removeTournamentMatch = (id) => {
    return axios.delete(`/match/${id}/delete/`)
}

export const tournamentMatchListPages = (id,request) => {
    return axios.get('/round/'+id+'/rounds/?page='+request)

}
export const saveScore = (data) => {
    return axios.post('/score/save/', data)
}
