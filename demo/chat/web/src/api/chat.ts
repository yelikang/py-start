import http from './http'

export default {
    getChatList: (params: any) => {
        return http.get('/chat/list', { params })
    }
}
