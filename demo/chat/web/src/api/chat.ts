import http from './http'

export default {
    getChatList: (params: any) => {
        return http.get('/chat/list', { params })
    },
    ask: (params: any) => {
        return http.post('/chat/ask', params)
    }
}
