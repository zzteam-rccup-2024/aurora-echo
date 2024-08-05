<script setup lang="ts">
import {
  ElContainer,
  ElHeader,
  ElMain,
  ElImage,
  ElAside,
} from 'element-plus'
</script>

<template>
  <ElContainer>
    <ElHeader>
      <p class="text-2xl pl-8 pt-1"><ElImage src="/aurora-echo.png" style="width: 24px; height: 24px" class="px-2" />Aurora Echo</p>
    </ElHeader>
    <ElMain>
      <ElAside width="2em"></ElAside>
      <ElMain>
        <RouterView />
      </ElMain>
    </ElMain>
  </ElContainer>
</template>
