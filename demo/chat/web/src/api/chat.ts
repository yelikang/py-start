import { cache } from '../utils/cache'
export default {
    getChatList: () => {
        return new Promise((resolve) => {
            const history: any[] = cache.get('chat_messages', [])
            resolve(history)
        })
    },
    createMessage: (params: any) => {
        return new Promise((resolve) => {
            const history: any[] = cache.get('chat_messages', [])
            history.push(params)
            cache.set('chat_messages', history)
            resolve(true)
        })
    },
    updateChatList: (history: any[]) => {
        return new Promise((resolve) => {
            cache.set('chat_messages', history)
            resolve(true)
        })
    },
    clearChatList: () => {
        cache.remove('chat_messages')
    }
}
