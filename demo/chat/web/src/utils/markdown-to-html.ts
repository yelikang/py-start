import { unified } from 'unified'
import remarkParse from 'remark-parse'
import remarkRehype from 'remark-rehype'
import rehypeStringify from 'rehype-stringify'

const processor = unified()
    .use(remarkParse)
    .use(remarkRehype)
    .use(rehypeStringify)


export default async function markdownToHtml(markdown: string) {
    const result = await processor.process(markdown)
    return result.toString()
}
