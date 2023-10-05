import axios from "axios";
export const createTournament = (data) => {
    return axios.post('/tour/tournament/', data)
}
export const getGround = () => {
    return axios.get('/tour/ground/')
}
//fetching team details
export const tournamentList = () => {
    return axios.get('/tour/tournament/')
}
export const alltournamentList = () => {
    return axios.get('/tour/home/')
}
/**Get tournament by id */
export const getTournamentById = (id) => {
    return axios.get('/tour/home/'+id)
}
/**Update tournament details */
export const updateTournament = (id,data) => {
    return axios.put('/tour/tournament/?id='+id , data)
}
    
//fetching paginated team list
export const tournamentListPages = (request) => {
    return axios.get('/tour/tournament/?page='+request)
}
//fetch details of teams in a tournament 
export const tournamentTeamList = (tournamentId,flag,search_term) => {
    return axios.get('tour/teams/'+tournamentId+'/?flag='+flag+'&search='+search_term)
}
//add teams to tournaments
export const addTeamsToTournament = (requestbody) => {
    return axios.post('/teamTour/addTeamtoTournament/',requestbody)
}
export const removeTournament = (data) => {
    return axios.put('/tour/tournamentDelete/', data)
}
export const tournamentDetails = (tournamentId) => {
    return axios.get('/tour/home/'+tournamentId)
}

//Remove team from tournament

export const removeTournamentTeam = (requestbody) => {
    return axios.put('/teamTour/removeTeamFromTournament/',requestbody)
}
export const getTournamentDetails = (id) => {
    return axios.get('/tour/home/'+id)
}
