import Axios from 'axios'

const request = Axios.create({
    baseURL: '/api',
    timeout: 2 * 60 * 1000,
    withCredentials: true
})


request.interceptors.response.use((response) => {
    return response.data
})

export default request