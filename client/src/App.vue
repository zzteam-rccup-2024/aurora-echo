<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import {
  ElContainer,
  ElHeader,
  ElMain,
  ElFooter,
  ElAside,
  ElRow,
  ElCol,
  ElButton,
  ElRadio,
  ElForm,
  ElFormItem,
  ElRadioGroup,
  ElCard,
  ElTag,
  ElSwitch
} from 'element-plus'
import { ref } from 'vue'

const models = [
  { label: 'Llama-3-8B-Instruct', value: 'llama-offline', badge: ['llama', 'offline'] },
  { label: 'Qwen2-1.5B-Instruct', value: 'qwen-offline', badge: ['qwen', 'offline'] },
  { label: 'Llama-3-70B-Instruct', value: 'llama-online', badge: ['llama', 'online'] },
  { label: 'gpt-3.5-turbo', value: 'chatgpt-online', badge: ['chatgpt', 'online'] },
  { label: 'ERNIE-4.0-8K-Latest', value: 'ernie-online', badge: ['ernie', 'online'] }
]

const model = ref('llama-offline')
const mosaic = ref(false)
</script>

<template>
  <ElContainer>
    <ElHeader>
      <p class="text-2xl pl-8 pt-1">Aurora Echo</p>
    </ElHeader>
    <ElMain>
      <ElAside width="2em"></ElAside>
      <ElMain>
        <ElRow>
          <ElCol :span="8">
            <ElCard shadow="never">
              <p class="text-center">Configuration</p>
              <ElForm>
                <ElFormItem label="Model">
                  <ElRadioGroup v-model="model">
                    <ElRadio v-for="item in models" :key="item.value" :label="item.value" border>
                      {{ item.label }}
                      <ElTag v-for="tag in item.badge" :key="tag.toString()" type="success" effect="plain" size="small">
                        {{ tag }}
                      </ElTag>
                    </ElRadio>
                  </ElRadioGroup>
                </ElFormItem>
                <ElFormItem label="Mosaic">
                  <ElSwitch v-model="mosaic" active-text="On" inactive-text="Off" />
                </ElFormItem>
                <ElFormItem style="text-align: right">
                  <ElButton text bg type="primary" class="w-full">Start</ElButton>
                </ElFormItem>
              </ElForm>
            </ElCard>
          </ElCol>
        </ElRow>
      </ElMain>
    </ElMain>
  </ElContainer>
</template>
