<script setup language="ts">
import { ref, onMounted, watch } from 'vue'
import { ElSegmented, ElButton, ElRow, ElCol } from 'element-plus'
import AEAnalysis from '@/components/AEAnalysis.vue'
import { start_llm, get_llm } from '@/plugins/apis'
import compileMarkdownToHTML from '@/plugins/markdown'

onMounted(() => {
  start_llm()
})

const perspectives = ['Service Provider', 'Customer']

const perspective = ref('Custormer')
const loaded = ref(false)

const interval = setInterval(async () => {
  if ((await get_llm('object')).status === 'success') {
    loaded.value = true
    clearInterval(interval)
    load_text()
  }
}, 2000)

const text = ref('')
const loading = ref(false)

async function load_text() {
  loading.value = true
  const response = await get_llm(perspective.value === 'Service Provider' ? 'subject' : 'object')
  const markdown = response.data
  text.value = await compileMarkdownToHTML(markdown)
  loading.value = false
}

watch(perspective, load_text)
</script>

<template>
  <ElRow>
    <ElCol :span="8">
      <AEAnalysis complex />
    </ElCol>
    <ElCol :span="1"></ElCol>
    <ElCol :span="15">
      <ElSegmented v-model="perspective" :options="perspectives" />
      <div class="py-2 w-full">
        <ElCard class="w-full font-serif text-lg" v-loading="loading || !loaded">
          <p v-html="text" />
        </ElCard>
      </div>
    </ElCol>
  </ElRow>
</template>