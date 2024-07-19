<script setup lang="ts">
import { start_record, get_value, set_llm, set_mosaic } from '@/plugins/apis'
import {
  ElRate,
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
  { label: 'Llama-3-8B-Instruct', value: 'llama-offline', badge: ['llama', 'offline'] },
  { label: 'Qwen2-1.5B-Instruct', value: 'qwen-offline', badge: ['qwen', 'offline'] },
  { label: 'Llama-3-70B-Instruct', value: 'llama-online', badge: ['llama', 'online'] },
  { label: 'gpt-3.5-turbo', value: 'chatgpt-online', badge: ['chatgpt', 'online'] },
  { label: 'ERNIE-4.0-8K-Latest', value: 'ernie-online', badge: ['ernie', 'online'] }
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
                  <ElTag v-for="tag in item.badge" :key="tag.toString()" type="success" effect="plain"
                         size="small">
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
