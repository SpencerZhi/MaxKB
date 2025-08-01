<template>
  <el-dialog
    :title="$t('views.chatLog.editContent')"
    v-model="dialogVisible"
    width="600"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
  >
    <el-form
      ref="formRef"
      :model="form"
      label-position="top"
      require-asterisk-position="right"
      :rules="rules"
      @submit.prevent
    >
      <el-form-item :label="$t('views.paragraph.relatedProblem.title')">
        <el-input
          v-model="form.problem_text"
          :placeholder="$t('views.paragraph.relatedProblem.title')"
          maxlength="256"
          show-word-limit
        >
        </el-input>
      </el-form-item>
      <el-form-item :label="$t('common.content')" prop="content">
        <MdEditor
          v-model="form.content"
          :placeholder="$t('views.chatLog.form.content.placeholder')"
          :maxLength="100000"
          :preview="false"
          :toolbars="toolbars"
          style="height: 300px"
          @onUploadImg="onUploadImg"
          :footers="footers"
        >
          <template #defFooters>
            <span style="margin-left: -6px">/ 100000</span>
          </template>
        </MdEditor>
      </el-form-item>
      <el-form-item :label="$t('common.title')">
        <el-input
          show-word-limit
          v-model="form.title"
          :placeholder="$t('views.chatLog.form.title.placeholder')"
          maxlength="256"
        >
        </el-input>
      </el-form-item>
    </el-form>
    <SelectKnowledgeDocument
      ref="SelectKnowledgeDocumentRef"
      :apiType="apiType"
      @changeKnowledge="changeKnowledge"
      @changeDocument="changeDocument"
      :isApplication="true"
    />
    <template #footer>
      <span class="dialog-footer">
        <el-button @click.prevent="dialogVisible = false"> {{ $t('common.cancel') }} </el-button>
        <el-button type="primary" @click="submitForm(formRef)" :loading="loading">
          {{ $t('common.save') }}
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>
<script setup lang="ts">
import { ref, watch, reactive, computed } from 'vue'
import { useRoute } from 'vue-router'
import SelectKnowledgeDocument from '@/components/select-knowledge-document/index.vue'
import type { FormInstance, FormRules } from 'element-plus'
import chatLogApi from '@/api/application/chat-log'
import imageApi from '@/api/image'
import { t } from '@/locales'

const route = useRoute()
const {
  params: { id },
} = route as any

const emit = defineEmits(['refresh'])

const apiType = computed<'workspace'>(() => {
  return 'workspace'
})
const formRef = ref()

const toolbars = [
  'bold',
  'underline',
  'italic',
  '-',
  'title',
  'strikeThrough',
  'sub',
  'sup',
  'quote',
  'unorderedList',
  'orderedList',
  'task',
  '-',
  'codeRow',
  'code',
  'link',
  'image',
  'table',
  'mermaid',
  'katex',
  '-',
  'revoke',
  'next',
  '=',
  'pageFullscreen',
  'preview',
  'htmlPreview',
] as any[]

const footers = ['markdownTotal', 0, '=', 1, 'scrollSwitch']

const SelectKnowledgeDocumentRef = ref()
const dialogVisible = ref<boolean>(false)
const loading = ref(false)

const form = ref<any>({
  chat_id: '',
  record_id: '',
  problem_text: '',
  title: '',
  content: '',
})

const rules = reactive<FormRules>({
  content: [
    { required: true, message: t('views.chatLog.form.content.placeholder'), trigger: 'blur' },
  ],
})

watch(dialogVisible, (bool) => {
  if (!bool) {
    form.value = {
      chat_id: '',
      record_id: '',
      problem_text: '',
      title: '',
      content: '',
    }
    formRef.value?.clearValidate()
    SelectKnowledgeDocumentRef.value?.clearValidate()
  }
})

const onUploadImg = async (files: any, callback: any) => {
  const res = await Promise.all(
    files.map((file: any) => {
      return new Promise((rev, rej) => {
        const fd = new FormData()
        fd.append('file', file)

        imageApi
          .postImage(fd)
          .then((res: any) => {
            rev(res)
          })
          .catch((error) => rej(error))
      })
    }),
  )

  callback(res.map((item) => item.data))
}

function changeKnowledge(knowledge_id: string) {
  localStorage.setItem(id + 'chat_knowledge_id', knowledge_id)
}

function changeDocument(document_id: string) {
  localStorage.setItem(id + 'chat_document_id', document_id)
}

const open = (data: any) => {
  form.value.chat_id = data.chat_id
  form.value.record_id = data.id
  form.value.problem_text = data.problem_text ? data.problem_text.substring(0, 256) : ''
  form.value.content = data.answer_text
  formRef.value?.clearValidate()
  dialogVisible.value = true
}
const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate(async (valid) => {
    if (valid) {
      if (await SelectKnowledgeDocumentRef.value?.validate()) {
        const obj = {
          title: form.value.title,
          content: form.value.content,
          problem_text: form.value.problem_text,
        }
        chatLogApi
          .putChatRecordLog(
            id,
            form.value.chat_id,
            form.value.record_id,
            SelectKnowledgeDocumentRef.value.form.knowledge_id,
            SelectKnowledgeDocumentRef.value.form.document_id,
            obj,
            loading,
          )
          .then((res: any) => {
            emit('refresh', res.data)
            dialogVisible.value = false
          })
      }
    }
  })
}

defineExpose({ open })
</script>
<style lang="scss" scoped></style>
