<script setup lang="ts">
import {
  ElContainer,
  ElHeader,
  ElMain,
  ElImage,
  ElAside,
  ElRow,
  ElCol
} from 'element-plus'
import { ref, watch } from 'vue'

const entered = ref(false)
const color = ref('#493f59')

document.body.style.backgroundColor = color.value

watch(entered, () => {
  if (entered.value) {
    color.value = '#ffffff'
  } else {
    color.value = '#493f59'
  }
  document.body.style.backgroundColor = color.value
})
</script>

<template>
  <ElContainer>
    <ElHeader v-if="entered">
      <p class="text-2xl pl-8 pt-1">
        <ElImage src="/aurora-echo.png" style="width: 24px; height: 24px" class="px-2" />
        Aurora Echo
      </p>
    </ElHeader>
    <ElMain>
      <ElAside width="2em" v-if="entered"></ElAside>
      <ElMain>
        <RouterView v-if="entered" />
        <!--493f59-->
        <div class="absolute inset-0 flex h-full w-full flex-col items-center justify-center dark" v-else>
          <ElRow>
            <ElCol :span="7">

            </ElCol>
            <ElCol :span="2">
              <ElImage src="/aurora-echo.png" alt="Aurora Echo Logo" />
            </ElCol>
            <ElCol :span="13">
              <p
                class="ml-8 mb-1 text-left text-5xl font-ubuntu delay-100 sm:text-6xl md:text-7xl duration-700 transition-[opacity,filter] text"
                style="color: #efefef">Aurora Echo</p>
            </ElCol>
          </ElRow>
          <p
            class="mb-5 text-left text-xl delay-100 duration-700 transition-[opacity,filter]"
            style="font-family: Ubuntu; color: #a6a6a6"
          >
            Audio-visual Feedback System integrated with AI.
          </p>
          <ElCol :span="4">
            <ElButton type="primary" round @click="entered = true"><span class="px-2">Let's Start.</span></ElButton>
            <ElButton text bg type="primary" round href="https://github.com/zzteam-rccup/aurora-echo" tag="a"
                      target="_blank"
                      rel="noopener noreferrer"><span
              class="px-2">Learn More.</span></ElButton>
          </ElCol>
        </div>
      </ElMain>
    </ElMain>
  </ElContainer>

</template>

<style scoped>
.container {
  @apply flex flex-col items-center justify-center bg-[#2E2F4F] w-full h-full;
}

.text {
  transform: translateY(-50px);
  font-family: Ubuntu;
}
</style>
