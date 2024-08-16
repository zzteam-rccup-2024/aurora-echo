<script setup lang="ts">
import { start_record, set_llm, set_mosaic } from '@/plugins/apis'
import {
  ElRow,
  ElCol,
  ElButton,
  ElRadio,
  ElForm,
  ElFormItem,
  ElRadioGroup,
  ElCard,
  ElTag,
  ElSwitch,
  ElImage
} from 'element-plus'
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import AEAnalysis from '@/components/AEAnalysis.vue'
import { useEmotionStore } from '@/stores/emotion'

const emotion = useEmotionStore()

const router = useRouter()

const models = [
  { label: 'GPT-4o', value: 'chatgpt', badge: ['chatgpt', 'online'] },
  { label: 'Claude 3.5 Sonnet', value: 'claude', badge: ['claude', 'online'] },
  { label: 'Mistral AI', value: 'mistral', badge: ['mistral', 'online'] },
  { label: 'Llama 3.1', value: 'llama', badge: ['llama', 'offline'] },
  { label: 'Qwen 2', value: 'qwen', badge: ['qwen', 'offline'] }
]

const model = ref('llama-offline')
const mosaic = ref(false)

async function call_recognition() {
  emotion.started = true
  await start_record()
}

watch(mosaic, async () => {
  await set_mosaic(mosaic.value)
})

watch(model, async () => {
  await set_llm(model.value)
})

const colors = {
  // According to the similar color of the product
  'chatgpt': 'success',
  'claude': 'danger',
  'mistral': 'warning',
  'llama': undefined,
  'qwen': 'info',
  'online': 'warning',
  'offline': 'success'
} as Record<string, 'success' | 'warning' | 'danger' | 'info' | undefined>
</script>

<template>
  <ElRow>
    <ElCol :span="8">
      <div class="py-2">
        <ElCard shadow="never">
          <p class="text-center">Configuration</p>
          <ElForm>
            <ElFormItem label="Model">
              <ElRadioGroup v-model="model">
                <ElRadio v-for="item in models" :key="item.value" :label="item.value" border>
                  {{ item.label }}
                  <ElTag v-for="tag in item.badge" :key="tag.toString()" :type="tag in colors ? colors[tag.toString()] : undefined" effect="plain"
                         size="small" class="px-1">
                    {{ tag }}
                  </ElTag>
                </ElRadio>
              </ElRadioGroup>
            </ElFormItem>
            <ElFormItem label="Mosaic">
              <ElSwitch v-model="mosaic" active-text="On" inactive-text="Off" />
            </ElFormItem>
            <ElFormItem style="text-align: right">
              <ElButton v-if="!emotion.started" text bg type="primary" class="w-full" @click="call_recognition">Start
              </ElButton>
            </ElFormItem>
          </ElForm>
        </ElCard>
      </div>
      <div class="py-2">
        <AEAnalysis complex />
      </div>
    </ElCol>
    <ElCol :span="1"></ElCol>
    <ElCol :span="15">
      <ElImage src="http://localhost:8000/camera" />
    </ElCol>
  </ElRow>
</template>
