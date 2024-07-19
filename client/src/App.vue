<script setup lang="ts">
import { start_record, get_value } from '@/plugins/apis'
import {
  ElContainer,
  ElHeader,
  ElMain,
  ElFooter,
  ElAside,
} from 'element-plus'
</script>

<template>
  <ElContainer>
    <ElHeader>
      <p class="text-2xl pl-8 pt-1">Aurora Echo</p>
    </ElHeader>
    <ElMain>
      <ElAside width="2em"></ElAside>
      <ElMain>
        <RouterView />
      </ElMain>
    </ElMain>
  </ElContainer>
</template>
