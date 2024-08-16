<script setup lang="ts">
import { ElCard, ElForm, ElFormItem, ElRate, ElTag, ElStatistic, ElButton } from 'element-plus'
import { ref, toRefs } from 'vue'
import { useEmotionStore } from '@/stores/emotion'
import { useRouter } from 'vue-router'

const emotionStore = useEmotionStore()
const router = useRouter()

const props = withDefaults(defineProps<{
  complex: boolean
}>(), {
  complex: false
})

const { complex } = toRefs(props)

const { started, text, sentiment, entities, emotions } = toRefs(emotionStore)
</script>

<template>
  <ElCard shadow="never">
    <p class="text-center">Analysis</p>
    <ElTag type="warning" effect="plain" size="small" v-if="started">Does not apply</ElTag>
    <ElForm>
      <ElFormItem label="Text">{{ text }}</ElFormItem>
      <ElFormItem label="Sentiment">
        <ElRate read-only v-model="sentiment" show-text disabled show-score />
      </ElFormItem>
      <ElFormItem label="Entities">{{ entities }}</ElFormItem>
      <ElFormItem v-if="complex" label="Emotion">
        {{ emotions }}
        <ElStatistic v-for="emotion in emotions" :key="emotion[0]" :title="emotion[0]" v-model="emotion[1]" />
      </ElFormItem>
      <ElFormItem>
        <ElButton type="primary" @click="router.push('/llm')" class="w-full" bg text>Recognize</ElButton>
      </ElFormItem>
    </ElForm>
  </ElCard>
</template>

<style scoped>

</style>