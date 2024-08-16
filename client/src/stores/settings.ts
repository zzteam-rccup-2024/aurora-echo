import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSettingsStore = defineStore('settings', () => {
  const llm = ref<'chatgpt' | 'llama' | 'claude' | 'deepseek' | 'qwen'>('chatgpt')
  const mosaic = ref(false)
  return { llm, mosaic }
})
