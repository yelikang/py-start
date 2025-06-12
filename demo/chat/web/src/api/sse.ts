import http from './http'
import { cache } from '@/utils/cache'

export default {
    sendSSE: (params: any, progress: (content: any) => void) => {
        let lastprogressIndex = 0

        return http.post('/chat/ask', params, {
            responseType: 'stream',
            onDownloadProgress: async (progressEvent: any) => {
                // axios 
                // 0.26.1版本使用 progressEvent.target ，
                // 1.9.0版本使用 progressEvent.event.target
                const xhr = progressEvent.target || progressEvent.event.target as XMLHttpRequest
                const resposeText = xhr.responseText
                // 截取文件流内容
                const newlines = resposeText
                    .split('\n\n')
                    .filter((i: string) => i.startsWith('data:'))
                    .map((i: string) => {
                        const data = i.split('data:')[1]
                        if (data) {
                            const jsonData = JSON.parse(data)
                            return jsonData
                        }
                    })

                for (let i = lastprogressIndex; i < newlines.length; i++) {
                    const line = newlines[i]
                    progress(line.content || '')
                }
                lastprogressIndex = newlines.length
            }
        })
    }

    // sendSSE(params: any, progress: (data: any) => void) {
    //     return new Promise((resolve, reject) => {
    //         const eventSource = new EventSource(`/api/chat/ask?query=${encodeURIComponent(params.query)}`)

    //         eventSource.onmessage = (event) => {
    //             try {
    //                 const data = JSON.parse(event.data)

    //                 if (data.type === 'stream' && data.content) {
    //                     progress(data.content)
    //                 } else if (data.type === 'end') {
    //                     eventSource.close()
    //                     resolve('完成')
    //                 }
    //             } catch (error) {
    //                 console.error('解析数据失败:', error)
    //             }
    //         }

    //         eventSource.onerror = (error) => {
    //             eventSource.close()
    //             reject(error)
    //         }
    //     })
    // }
}
