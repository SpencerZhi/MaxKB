<template>
  <div class="breadcrumb ml-4 mt-4 mb-12 flex">
    <back-button :to="toBackPath" class="mt-4"></back-button>
    <div class="flex align-center">
      <el-avatar
        v-if="isApplication"
        shape="square"
        :size="24"
        style="background: none"
        class="mr-8"
      >
        <img :src="resetUrl(current?.icon, resetUrl('./favicon.ico'))" alt="" />
      </el-avatar>
      <LogoIcon
        v-else-if="isApplication"
        height="28px"
        style="width: 28px; height: 28px; display: block"
        class="mr-8"
      />
      <KnowledgeIcon v-else-if="isKnowledge" :type="current?.type" class="mr-8" />

      <div class="ellipsis" :title="current?.name">{{ current?.name }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { onBeforeRouteLeave, useRouter, useRoute } from 'vue-router'
import { resetUrl } from '@/utils/common'
import { loadSharedApi } from '@/utils/dynamics-api/shared-api'
import useStore from '@/stores'
const { common, application } = useStore()
const route = useRoute()

const {
  meta: { activeMenu },
  params: { id, folderId },
  query: { isShared },
} = route as any

const apiType = computed(() => {
  if (route.path.includes('shared')) {
    return 'systemShare'
  } else if (route.path.includes('resource-management')) {
    return 'systemManage'
  } else {
    return 'workspace'
  }
})

const shareDisabled = computed(() => {
  return folderId === 'share' || isShared === 'true'
})

onBeforeRouteLeave((to, from) => {
  common.saveBreadcrumb(null)
})

const loading = ref(false)

const current = ref<any>(null)

const isApplication = computed(() => {
  return activeMenu.includes('application')
})
const isKnowledge = computed(() => {
  return activeMenu.includes('knowledge')
})

const toBackPath = computed(() => {
  if (route.path.includes('shared')) {
    return '/system/shared' + activeMenu
  } else if (route.path.includes('resource-management')) {
    return '/system/resource-management' + activeMenu
  } else {
    return activeMenu
  }
})

function getKnowledgeDetail() {
  loading.value = true
  loadSharedApi({ type: 'knowledge', isShared: shareDisabled.value, systemType: apiType.value })
    .getKnowledgeDetail(id)
    .then((res: any) => {
      current.value = res.data
      loading.value = false
    })
    .catch(() => {
      loading.value = false
    })
}

function getApplicationDetail() {
  loading.value = true
  application
    .asyncGetApplicationDetail(id)
    .then((res: any) => {
      current.value = res.data
      loading.value = false
    })
    .catch(() => {
      loading.value = false
    })
}

onMounted(() => {
  if (isKnowledge.value) {
    getKnowledgeDetail()
  } else if (isApplication.value) {
    getApplicationDetail()
  }
})
</script>

<style scoped lang="scss">
:deep(.dropdown-active) {
  background-color: var(--el-dropdown-menuItem-hover-fill);
  .el-dropdown-menu__item {
    color: var(--el-dropdown-menuItem-hover-color);
  }
}
.breadcrumb {
  .breadcrumb-hover {
    padding: 4px;
    border-radius: 4px;
    &:hover {
      background: var(--el-color-primary-light-9);
      color: var(--el-color-primary);
    }
  }
  &__footer {
    &:hover {
      background-color: var(--app-text-color-light-1);
    }
  }
}
</style>
