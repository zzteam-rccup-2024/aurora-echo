import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { get_value } from '@/plugins/apis'
import { useRouter } from 'vue-router'

export const useEmotionStore = defineStore('counter', () => {
  const router = useRouter()
  const started = ref(false)
  const text = ref('')
  const sentiment = ref(Math.random() * 5)
  const entities = ref([])
  const emotions = ref<Array<[string, string]>>([])
  const thumbs = ref<Array<['thumb up' | 'thumb down', string]>>([])

  setInterval(async () => {
    if (started.value) {
      const result = await get_value('text')
      if (result.status === 'success') {
        started.value = false
        text.value = result.data
        sentiment.value = ((await get_value('sentiment')).data * 5)
        entities.value = (await get_value('named_entities')).data
        emotions.value = (await get_value('emotion')).data
        thumbs.value = (await get_value('thumb')).data
        setTimeout(() => {
          router.push('/llm')
        }, 500)
      }
    }
  }, 200)

  return { started, text, sentiment, entities, emotions, thumbs }
})
