import axios from "axios";
/**Create group */
export const createGroup = (data) => {
    return axios.post('/group/addGroup/', data)
}
/**Group list of a particular tournament */
export const GroupList = (tournamentId) => {
    return axios.get('/group/'+tournamentId+'/listGroup/')
}

/**Fetching teams list that are not added in any of the tournament-groups */

export const GroupTeamList = (tournamentId) => {
    return axios.get('/group/'+tournamentId+'/listTeam/')
}

/**Group details by id */
export const GroupDetailsById = (groupId) => {
    return axios.get('/group/details/'+groupId)
}
/**Delete a particulat group details from tournament */
export const removeGroup = (data) => {
    return axios.put('/group/remove/',data)
}

//Update group
export const editGroup = (data) => {
    return axios.put('group/editGroup/',data)
}
