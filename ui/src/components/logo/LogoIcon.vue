<template>
  <svg
    v-if="!isDefaultTheme"
    :class="!isDefaultTheme ? 'custom-logo-color' : ''"
    :height="height"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 232.4409 232.4409"
  >
    <title>MaxKB</title>
    <path
      class="cls-1"
      d="M128.4532,177H98.7785L87.78,187.9985a4.6069,4.6069,0,0,0,3.2576,7.8644h45.1569a4.6069,4.6069,0,0,0,3.2575-7.8644Z"
    />
    <path
      class="cls-1"
      d="M210.0008,90.7042h-5.85v41.1511h5.85a4.4537,4.4537,0,0,0,4.4537-4.4537V95.1579A4.4537,4.4537,0,0,0,210.0008,90.7042Z"
    />
    <path
      class="cls-1"
      d="M28.29,90.7042H22.44a4.4538,4.4538,0,0,0-4.4538,4.4537v32.2437a4.4538,4.4538,0,0,0,4.4538,4.4537h5.85Z"
    />
    <path
      class="cls-1"
      d="M138.8087,96.1512a8.33,8.33,0,0,0-8.33,8.33v5.9727a8.33,8.33,0,1,0,16.6607,0v-5.9727A8.33,8.33,0,0,0,138.8087,96.1512Z"
    />
    <path
      class="cls-1"
      d="M95.3622,96.1512a8.33,8.33,0,0,0-8.33,8.33v5.9727a8.33,8.33,0,1,0,16.6607,0v-5.9727A8.33,8.33,0,0,0,95.3622,96.1512Z"
    />
    <path
      class="cls-1"
      d="M166.8344,48.8968H65.6064A33.7544,33.7544,0,0,0,31.89,82.6131v57.07A33.7548,33.7548,0,0,0,65.6064,173.4h101.228a33.7549,33.7549,0,0,0,33.7168-33.7168v-57.07A33.7545,33.7545,0,0,0,166.8344,48.8968Zm2.831,90.4457a6.0733,6.0733,0,0,1-6.0732,6.0733H114.2168a43.5922,43.5922,0,0,0-21.3313,5.5757l-16.5647,9.2946v-14.87h-7.472a6.0733,6.0733,0,0,1-6.0733-6.0733v-60.5a6.0733,6.0733,0,0,1,6.0733-6.0733h94.7434a6.0733,6.0733,0,0,1,6.0732,6.0733Z"
    />
  </svg>
  <img v-else src="@/assets/logo/logo.svg" :height="height" />
</template>
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import useStore from '@/stores'
defineOptions({ name: 'LogoIcon' })

defineProps({
  height: {
    type: String,
    default: '36px'
  }
})
const { theme } = useStore()
const isDefaultTheme = computed(() => {
  return theme.isDefaultTheme()
})
</script>
<style lang="scss" scoped>
.custom-logo-color {
  path {
    fill: var(--el-color-primary);
  }
}
</style>
