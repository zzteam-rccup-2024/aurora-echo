import { marked } from 'marked'

export default async function(markdown: string) {
  return marked.parse(markdown)
}
