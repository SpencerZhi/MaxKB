<template>
  <div class="ai-chat__operate p-16" @drop.prevent="handleDrop" @dragover.prevent>
    <div class="text-center mb-8" v-if="loading">
      <el-button class="border-primary video-stop-button" @click="stopChat">
        <app-icon iconName="app-video-stop" class="mr-8"></app-icon>
        {{ $t('chat.operation.stopChat') }}</el-button
      >
    </div>
    <div class="operate-textarea">
      <el-scrollbar max-height="136">
        <div
          class="p-8-12"
          v-loading="uploadLoading"
          v-if="
            uploadDocumentList.length ||
            uploadImageList.length ||
            uploadAudioList.length ||
            uploadVideoList.length ||
            uploadOtherList.length
          "
        >
          <el-row :gutter="10">
            <el-col
              v-for="(item, index) in uploadDocumentList"
              :key="index"
              :xs="24"
              :sm="props.type === 'debug-ai-chat' ? 24 : 12"
              :md="props.type === 'debug-ai-chat' ? 24 : 12"
              :lg="props.type === 'debug-ai-chat' ? 24 : 12"
              :xl="props.type === 'debug-ai-chat' ? 24 : 12"
              class="mb-8"
            >
              <el-card
                shadow="never"
                style="--el-card-padding: 8px; max-width: 100%"
                class="file cursor"
              >
                <div
                  class="flex-between align-center"
                  @mouseenter.stop="mouseenter(item)"
                  @mouseleave.stop="mouseleave()"
                >
                  <div class="flex align-center">
                    <img :src="getImgUrl(item && item?.name)" alt="" width="24" />
                    <div class="ml-4 ellipsis-1" :title="item && item?.name">
                      {{ item && item?.name }}
                    </div>
                  </div>
                  <div
                    @click="deleteFile(item)"
                    class="delete-icon color-secondary"
                    v-if="showDelete === item.url"
                  >
                    <el-icon style="font-size: 16px; top: 2px">
                      <CircleCloseFilled />
                    </el-icon>
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col
              v-for="(item, index) in uploadOtherList"
              :key="index"
              :xs="24"
              :sm="props.type === 'debug-ai-chat' ? 24 : 12"
              :md="props.type === 'debug-ai-chat' ? 24 : 12"
              :lg="props.type === 'debug-ai-chat' ? 24 : 12"
              :xl="props.type === 'debug-ai-chat' ? 24 : 12"
              class="mb-8"
            >
              <el-card
                shadow="never"
                style="--el-card-padding: 8px; max-width: 100%"
                class="file cursor"
              >
                <div
                  class="flex-between align-center"
                  @mouseenter.stop="mouseenter(item)"
                  @mouseleave.stop="mouseleave()"
                >
                  <div class="flex align-center">
                    <img :src="getImgUrl(item && item?.name)" alt="" width="24" />
                    <div class="ml-4 ellipsis-1" :title="item && item?.name">
                      {{ item && item?.name }}
                    </div>
                  </div>
                  <div
                    @click="deleteFile(item)"
                    class="delete-icon color-secondary"
                    v-if="showDelete === item.url"
                  >
                    <el-icon style="font-size: 16px; top: 2px">
                      <CircleCloseFilled />
                    </el-icon>
                  </div>
                </div>
              </el-card>
            </el-col>

            <el-col
              :xs="24"
              :sm="props.type === 'debug-ai-chat' ? 24 : 12"
              :md="props.type === 'debug-ai-chat' ? 24 : 12"
              :lg="props.type === 'debug-ai-chat' ? 24 : 12"
              :xl="props.type === 'debug-ai-chat' ? 24 : 12"
              class="mb-8"
              v-for="(item, index) in uploadAudioList"
              :key="index"
            >
              <el-card shadow="never" style="--el-card-padding: 8px" class="file cursor">
                <div
                  class="flex-between align-center"
                  @mouseenter.stop="mouseenter(item)"
                  @mouseleave.stop="mouseleave()"
                >
                  <div class="flex align-center">
                    <img :src="getImgUrl(item && item?.name)" alt="" width="24" />
                    <div class="ml-4 ellipsis-1" :title="item && item?.name">
                      {{ item && item?.name }}
                    </div>
                  </div>
                  <div
                    @click="deleteFile(item)"
                    class="delete-icon color-secondary"
                    v-if="showDelete === item.url"
                  >
                    <el-icon style="font-size: 16px; top: 2px">
                      <CircleCloseFilled />
                    </el-icon>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
          <el-space wrap>
            <template v-for="(item, index) in uploadImageList" :key="index">
              <div
                class="file file-image cursor border border-r-6"
                @mouseenter.stop="mouseenter(item)"
                @mouseleave.stop="mouseleave()"
              >
                <div
                  @click="deleteFile(item)"
                  class="delete-icon color-secondary"
                  v-if="showDelete === item.url"
                >
                  <el-icon style="font-size: 16px; top: 2px">
                    <CircleCloseFilled />
                  </el-icon>
                </div>
                <el-image
                  v-if="item.url"
                  :src="item.url"
                  alt=""
                  fit="cover"
                  style="width: 40px; height: 40px; display: block"
                  class="border-r-6"
                />
              </div>
            </template>
          </el-space>
        </div>
      </el-scrollbar>

      <TouchChat
        v-if="isMicrophone"
        @TouchStart="startRecording"
        @TouchEnd="TouchEnd"
        :time="recorderTime"
        :start="recorderStatus === 'START'"
        :disabled="loading"
      />
      <el-input
        v-else
        ref="quickInputRef"
        v-model="inputValue"
        :autosize="{ minRows: 1, maxRows: isMobile ? 4 : 10 }"
        type="textarea"
        :placeholder="inputPlaceholder"
        :maxlength="100000"
        @keydown.enter="sendChatHandle($event)"
        @paste="handlePaste"
        class="chat-operate-textarea"
      />

      <div class="operate flex-between">
        <div>
          <slot name="userInput" />
        </div>
        <div class="flex align-center">
          <template v-if="props.applicationDetails.stt_model_enable">
            <span v-if="mode === 'mobile'">
              <el-button text @click="switchMicrophone(!isMicrophone)">
                <!-- 键盘 -->
                <AppIcon v-if="isMicrophone" iconName="app-keyboard"></AppIcon>
                <el-icon v-else>
                  <!-- 录音 -->
                  <Microphone />
                </el-icon>
              </el-button>
            </span>
            <span class="flex align-center" v-else>
              <el-button
                :disabled="loading"
                text
                @click="startRecording"
                v-if="recorderStatus === 'STOP'"
              >
                <el-icon>
                  <Microphone />
                </el-icon>
              </el-button>

              <div v-else class="operate flex align-center">
                <el-text type="info"
                  >00:{{ recorderTime < 10 ? `0${recorderTime}` : recorderTime }}</el-text
                >
                <el-button
                  text
                  type="primary"
                  @click="stopRecording"
                  :loading="recorderStatus === 'TRANSCRIBING'"
                >
                  <AppIcon iconName="app-video-stop"></AppIcon>
                </el-button>
              </div>
            </span>
          </template>

          <template v-if="recorderStatus === 'STOP' || mode === 'mobile'">
            <span v-if="props.applicationDetails.file_upload_enable" class="flex align-center ml-4">
              <el-upload
                action="#"
                multiple
                :auto-upload="false"
                :show-file-list="false"
                :accept="getAcceptList()"
                :on-change="(file: any, fileList: any) => uploadFile(file, fileList)"
                v-model:file-list="fileAllList"
                ref="upload"
              >
                <el-tooltip
                  :disabled="mode === 'mobile'"
                  effect="dark"
                  placement="top"
                  popper-class="upload-tooltip-width"
                >
                  <template #content>
                    <div class="break-all pre-wrap">
                      {{ $t('chat.uploadFile.label') }}：{{ $t('chat.uploadFile.most')
                      }}{{ props.applicationDetails.file_upload_setting.maxFiles
                      }}{{ $t('chat.uploadFile.limit') }}
                      {{ props.applicationDetails.file_upload_setting.fileLimit }}MB<br />{{
                        $t('chat.uploadFile.fileType')
                      }}：{{ getAcceptList().replace(/\./g, '').replace(/,/g, '、').toUpperCase() }}
                    </div>
                  </template>
                  <el-button text :disabled="checkMaxFilesLimit() || loading" class="mt-4">
                    <el-icon><Paperclip /></el-icon>
                  </el-button>
                </el-tooltip>
              </el-upload>
            </span>
            <el-divider
              direction="vertical"
              v-if="
                props.applicationDetails.file_upload_enable ||
                props.applicationDetails.stt_model_enable
              "
            />
            <el-button
              text
              class="sent-button"
              :disabled="isDisabledChat || loading || uploadLoading"
              @click="sendChatHandle"
            >
              <img
                v-show="isDisabledChat || loading || uploadLoading"
                src="@/assets/icon_send.svg"
                alt=""
              />
              <SendIcon v-show="!isDisabledChat && !loading && !uploadLoading" />
            </el-button>
          </template>
        </div>
      </div>
    </div>

    <div class="text-center" v-if="applicationDetails.disclaimer" style="margin-top: 8px">
      <el-text type="info" v-if="applicationDetails.disclaimer" style="font-size: 12px">
        <auto-tooltip :content="applicationDetails.disclaimer_value">
          {{ applicationDetails.disclaimer_value }}
        </auto-tooltip>
      </el-text>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, computed, onMounted, nextTick, reactive, type Ref } from 'vue'
import { t } from '@/locales'
import Recorder from 'recorder-core'
import TouchChat from './TouchChat.vue'
import applicationApi from '@/api/application/application'
import { MsgAlert } from '@/utils/message'
import { type chatType } from '@/api/type/application'
import { useRoute, useRouter } from 'vue-router'
import { getImgUrl } from '@/utils/common'
import bus from '@/bus'
import 'recorder-core/src/engine/mp3'
import 'recorder-core/src/engine/mp3-engine'
import { MsgWarning } from '@/utils/message'
import chatAPI from '@/api/chat/chat'
const router = useRouter()
const route = useRoute()
const {
  query: { mode, question },
} = route as any
const quickInputRef = ref()
const props = withDefaults(
  defineProps<{
    applicationDetails: any
    type: 'log' | 'ai-chat' | 'debug-ai-chat'
    loading: boolean
    isMobile: boolean
    appId?: string
    chatId: string
    sendMessage: (question: string, other_params_data?: any, chat?: chatType) => void
    openChatId: () => Promise<string>
    validate: () => Promise<any>
  }>(),
  {
    applicationDetails: () => ({}),
    available: true,
  },
)
const emit = defineEmits(['update:chatId', 'update:loading', 'update:showUserInput'])
const chartOpenId = ref<string>()
const chatId_context = computed({
  get: () => {
    if (chartOpenId.value) {
      return chartOpenId.value
    }
    return props.chatId
  },
  set: (v) => {
    chartOpenId.value = v
    emit('update:chatId', v)
  },
})
const localLoading = computed({
  get: () => {
    return props.loading
  },
  set: (v) => {
    emit('update:loading', v)
  },
})

const uploadLoading = ref(false)

const inputPlaceholder = computed(() => {
  return recorderStatus.value === 'START'
    ? `${t('chat.inputPlaceholder.speaking')}...`
    : recorderStatus.value === 'TRANSCRIBING'
      ? `${t('chat.inputPlaceholder.recorderLoading')}...`
      : `${t('chat.inputPlaceholder.default')}`
})

const upload = ref()

const imageExtensions = ['JPG', 'JPEG', 'PNG', 'GIF', 'BMP']
const documentExtensions = ['PDF', 'DOCX', 'TXT', 'XLS', 'XLSX', 'MD', 'HTML', 'CSV']
const videoExtensions: any = []
const audioExtensions = ['MP3', 'WAV', 'OGG', 'AAC', 'M4A']
let otherExtensions = ref(['PPT', 'DOC'])

const getAcceptList = () => {
  const { image, document, audio, video, other } = props.applicationDetails.file_upload_setting
  let accepts: any = []
  if (image) {
    accepts = [...imageExtensions]
  }
  if (document) {
    accepts = [...accepts, ...documentExtensions]
  }
  if (audio) {
    accepts = [...accepts, ...audioExtensions]
  }
  if (video) {
    accepts = [...accepts, ...videoExtensions]
  }
  if (other) {
    // 其他文件类型
    otherExtensions.value = props.applicationDetails.file_upload_setting.otherExtensions
    accepts = [...accepts, ...otherExtensions.value]
  }

  if (accepts.length === 0) {
    return `.${t('chat.uploadFile.tipMessage')}`
  }
  return accepts.map((ext: any) => '.' + ext).join(',')
}

const checkMaxFilesLimit = () => {
  return (
    props.applicationDetails.file_upload_setting.maxFiles <=
    uploadImageList.value.length +
      uploadDocumentList.value.length +
      uploadAudioList.value.length +
      uploadVideoList.value.length +
      uploadOtherList.value.length
  )
}

const uploadFile = async (file: any, fileList: any) => {
  const { maxFiles, fileLimit } = props.applicationDetails.file_upload_setting
  // 单次上传文件数量限制
  const file_limit_once =
    uploadImageList.value.length +
    uploadDocumentList.value.length +
    uploadAudioList.value.length +
    uploadVideoList.value.length +
    uploadOtherList.value.length
  if (file_limit_once >= maxFiles) {
    MsgWarning(t('chat.uploadFile.limitMessage1') + maxFiles + t('chat.uploadFile.limitMessage2'))
    fileList.splice(0, fileList.length)
    return
  }
  if (fileList.filter((f: any) => f.size > fileLimit * 1024 * 1024).length > 0) {
    // MB
    MsgWarning(t('chat.uploadFile.sizeLimit') + fileLimit + 'MB')
    fileList.splice(0, fileList.length)
    return
  }
  const inner = reactive(file)
  fileAllList.value.push(inner)
  if (!chatId_context.value) {
    const res = await props.openChatId()
    chatId_context.value = res
  }
  const api =
    props.type === 'debug-ai-chat'
      ? applicationApi.postUploadFile(
          file.raw,
          'TEMPORARY_120_MINUTE',
          'TEMPORARY_120_MINUTE',
          uploadLoading,
        )
      : chatAPI.postUploadFile(file.raw, chatId_context.value, 'CHAT', uploadLoading)
  api.then((ok) => {
    inner.url = ok.data
    const split_path = ok.data.split('/')
    inner.file_id = split_path[split_path.length - 1]
  })
  if (!inputValue.value && uploadImageList.value.length > 0) {
    inputValue.value = t('chat.uploadFile.imageMessage')
  }
}
// 粘贴处理
const handlePaste = (event: ClipboardEvent) => {
  if (!props.applicationDetails.file_upload_enable) return
  const clipboardData = event.clipboardData
  if (!clipboardData) return

  // 获取剪贴板中的文件
  const files = clipboardData.files
  if (files.length === 0) return

  // 转换 FileList 为数组并遍历处理
  Array.from(files).forEach((rawFile: File) => {
    // 创建符合 el-upload 要求的文件对象
    const elFile = {
      uid: Date.now(), // 生成唯一ID
      name: rawFile.name,
      size: rawFile.size,
      raw: rawFile, // 原始文件对象
      status: 'ready', // 文件状态
      percentage: 0, // 上传进度
    }

    // 手动触发上传逻辑（模拟 on-change 事件）
    uploadFile(elFile, [elFile])
  })

  // 阻止默认粘贴行为
  event.preventDefault()
}
// 新增拖拽处理
const handleDrop = (event: DragEvent) => {
  if (!props.applicationDetails.file_upload_enable) return
  event.preventDefault()
  const files = event.dataTransfer?.files
  if (!files) return

  Array.from(files).forEach((rawFile) => {
    const elFile = {
      uid: Date.now(),
      name: rawFile.name,
      size: rawFile.size,
      raw: rawFile,
      status: 'ready',
      percentage: 0,
    }
    uploadFile(elFile, [elFile])
  })
}
// 语音录制任务id
const intervalId = ref<any | null>(null)
// 语音录制开始秒数
const recorderTime = ref(0)
// START:开始录音 TRANSCRIBING:转换文字中
const recorderStatus = ref<'START' | 'TRANSCRIBING' | 'STOP'>('STOP')

const inputValue = ref<string>('')

const fileAllList = ref<Array<any>>([])

const fileFilter = (fileList: Array<any>, extensionList: Array<string>) => {
  return fileList.filter((f) => {
    return extensionList.includes(f.name.split('.').pop().toUpperCase())
  })
}
const uploadImageList = computed(() => fileFilter(fileAllList.value, imageExtensions))
const uploadDocumentList = computed(() => fileFilter(fileAllList.value, documentExtensions))
const uploadVideoList = computed(() => fileFilter(fileAllList.value, videoExtensions))
const uploadAudioList = computed(() => fileFilter(fileAllList.value, audioExtensions))
const uploadOtherList = computed(() =>
  fileFilter(
    fileAllList.value,
    otherExtensions.value.map((item) => item.toUpperCase()),
  ),
)

const showDelete = ref('')

const isDisabledChat = computed(
  () => !(inputValue.value.trim() && (props.appId || props.applicationDetails?.name)),
)
// 是否显示移动端语音按钮
const isMicrophone = ref(false)
const switchMicrophone = (status: boolean) => {
  if (status) {
    // 如果显示就申请麦克风权限
    recorderManage.open(() => {
      isMicrophone.value = true
    })
  } else {
    // 关闭麦克风
    recorderManage.close()
    isMicrophone.value = false
  }
}

const TouchEnd = (bool?: Boolean) => {
  if (bool) {
    stopRecording()
    recorderStatus.value = 'STOP'
  } else {
    stopTimer()
    recorderStatus.value = 'STOP'
  }
}
// 取消录音控制台日志
Recorder.CLog = function () {}

class RecorderManage {
  recorder?: any
  uploadRecording: (blob: Blob, duration: number) => void
  constructor(uploadRecording: (blob: Blob, duration: number) => void) {
    this.uploadRecording = uploadRecording
  }
  open(callback?: () => void) {
    const recorder = new Recorder({
      type: 'mp3',
      bitRate: 128,
      sampleRate: 16000,
    })
    if (!this.recorder) {
      recorder.open(() => {
        this.recorder = recorder
        if (callback) {
          callback()
        }
      }, this.errorCallBack)
    }
  }
  start() {
    if (this.recorder) {
      this.recorder.start()
      recorderStatus.value = 'START'
      handleTimeChange()
    } else {
      const recorder = new Recorder({
        type: 'mp3',
        bitRate: 128,
        sampleRate: 16000,
      })
      recorder.open(() => {
        this.recorder = recorder
        recorder.start()
        recorderStatus.value = 'START'
        handleTimeChange()
      }, this.errorCallBack)
    }
  }
  stop() {
    if (this.recorder) {
      this.recorder.stop(
        (blob: Blob, duration: number) => {
          if (mode !== 'mobile') {
            this.close()
          }
          this.uploadRecording(blob, duration)
        },
        (err: any) => {
          MsgAlert(t('common.tip'), err, {
            confirmButtonText: t('chat.tip.confirm'),
            dangerouslyUseHTMLString: true,
            customClass: 'record-tip-confirm',
          })
        },
      )
    }
  }
  close() {
    if (this.recorder) {
      this.recorder.close()
      this.recorder = undefined
    }
  }

  private errorCallBack(err: any, isUserNotAllow: boolean) {
    if (isUserNotAllow) {
      MsgAlert(t('common.tip'), err, {
        confirmButtonText: t('chat.tip.confirm'),
        dangerouslyUseHTMLString: true,
        customClass: 'record-tip-confirm',
      })
    } else {
      MsgAlert(
        t('common.tip'),
        `${err}
        <div style="width: 100%;height:1px;border-top:1px var(--el-border-color) var(--el-border-style);margin:10px 0;"></div>
        ${t('chat.tip.recorderTip')}
    <img src="${new URL(`/tipIMG.jpg`, import.meta.url).href}" style="width: 100%;" />`,
        {
          confirmButtonText: t('chat.tip.confirm'),
          dangerouslyUseHTMLString: true,
          customClass: 'record-tip-confirm',
        },
      )
    }
  }
}
const getSpeechToTextAPI = () => {
  if (props.type === 'ai-chat') {
    return (id?: any, data?: any, loading?: Ref<boolean>) => {
      return chatAPI.speechToText(data, loading)
    }
  } else {
    return applicationApi.speechToText
  }
}
const speechToTextAPI = getSpeechToTextAPI()
// 上传录音文件
const uploadRecording = async (audioBlob: Blob) => {
  try {
    // 非自动发送切换输入框
    if (!props.applicationDetails.stt_autosend) {
      switchMicrophone(false)
    }
    recorderStatus.value = 'TRANSCRIBING'
    const formData = new FormData()
    formData.append('file', audioBlob, 'recording.mp3')
    if (props.applicationDetails.stt_autosend) {
      bus.emit('on:transcribing', true)
    }
    speechToTextAPI(props.applicationDetails.id as string, formData, localLoading)
      .then((response) => {
        inputValue.value = typeof response.data === 'string' ? response.data : ''
        // 自动发送
        if (props.applicationDetails.stt_autosend) {
          nextTick(() => {
            autoSendMessage()
          })
        } else {
          switchMicrophone(false)
        }
      })
      .catch((error) => {
        console.error(`${t('chat.uploadFile.errorMessage')}:`, error)
      })
      .finally(() => {
        recorderStatus.value = 'STOP'
        bus.emit('on:transcribing', false)
      })
  } catch (error) {
    recorderStatus.value = 'STOP'
    console.error(`${t('chat.uploadFile.errorMessage')}:`, error)
  }
}
const recorderManage = new RecorderManage(uploadRecording)
// 开始录音
const startRecording = () => {
  recorderManage.start()
}

// 停止录音
const stopRecording = () => {
  recorderManage.stop()
}

const handleTimeChange = () => {
  recorderTime.value = 0
  if (intervalId.value) {
    return
  }
  intervalId.value = setInterval(() => {
    if (recorderStatus.value === 'STOP') {
      clearInterval(intervalId.value!)
      intervalId.value = null
      return
    }

    recorderTime.value++

    if (recorderTime.value === 60) {
      if (mode !== 'mobile') {
        stopRecording()
        clearInterval(intervalId.value!)
        intervalId.value = null
        recorderStatus.value = 'STOP'
      }
    }
  }, 1000)
}
// 停止计时的函数
const stopTimer = () => {
  if (intervalId.value !== null) {
    clearInterval(intervalId.value)
    recorderTime.value = 0
    intervalId.value = null
  }
}

function autoSendMessage() {
  props
    .validate()
    .then(() => {
      props.sendMessage(inputValue.value, {
        image_list: uploadImageList.value,
        document_list: uploadDocumentList.value,
        audio_list: uploadAudioList.value,
        video_list: uploadVideoList.value,
        other_list: uploadOtherList.value,
      })
      inputValue.value = ''
      fileAllList.value = []
      if (upload.value) {
        upload.value.clearFiles()
      }

      if (quickInputRef.value) {
        quickInputRef.value.textarea.style.height = '45px'
      }
    })
    .catch(() => {
      emit('update:showUserInput', true)
    })
}

function sendChatHandle(event?: any) {
  const isMobile = /Mobi|Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
    navigator.userAgent,
  )
  // 如果是移动端，且按下回车键，不直接发送
  if ((isMobile || mode === 'mobile') && event?.key === 'Enter') {
    // 阻止默认事件
    return
  }
  if (!event?.ctrlKey && !event?.shiftKey && !event?.altKey && !event?.metaKey) {
    // 如果没有按下组合键，则会阻止默认事件
    event?.preventDefault()
    if (!isDisabledChat.value && !props.loading && !event?.isComposing && !uploadLoading.value) {
      if (inputValue.value.trim()) {
        autoSendMessage()
      }
    }
  } else {
    // 如果同时按下ctrl/shift/cmd/opt +enter，则会换行
    insertNewlineAtCursor(event)
  }
}
const insertNewlineAtCursor = (event?: any) => {
  const textarea = quickInputRef.value.$el.querySelector(
    '.el-textarea__inner',
  ) as HTMLTextAreaElement
  const startPos = textarea.selectionStart
  const endPos = textarea.selectionEnd
  // 阻止默认行为（避免额外的换行符）
  event.preventDefault()
  // 在光标处插入换行符
  inputValue.value = inputValue.value.slice(0, startPos) + '\n' + inputValue.value.slice(endPos)
  nextTick(() => {
    textarea.setSelectionRange(startPos + 1, startPos + 1) // 光标定位到换行后位置
  })
}

function deleteFile(item: any) {
  fileAllList.value = fileAllList.value.filter((i) => i != item)
}

function mouseenter(row: any) {
  showDelete.value = row.url
}

function mouseleave() {
  showDelete.value = ''
}

function stopChat() {
  bus.emit('chat:stop')
}
onMounted(() => {
  bus.on('chat-input', (message: string) => {
    inputValue.value = message
  })
  if (question) {
    inputValue.value = decodeURIComponent(question.trim())
    sendChatHandle()
    setTimeout(() => {
      // 获取当前路由信息
      const route = router.currentRoute.value
      // 复制query对象
      const query = { ...route.query }
      // 删除特定的参数
      delete query.question
      const newRoute =
        Object.entries(query)?.length > 0
          ? route.path +
            '?' +
            Object.entries(query)
              .map(([key, value]) => `${key}=${value}`)
              .join('&')
          : route.path

      history.pushState(null, '', '/ui' + newRoute)
    }, 100)
  }
  setTimeout(() => {
    nextTick(() => {
      quickInputRef.value.textarea.style.height = '0'
    })
  }, 800)
})
</script>
<style lang="scss" scoped>
.ai-chat {
  &__operate {
    position: relative;
    width: 100%;
    box-sizing: border-box;
    z-index: 10;

    :deep(.operate-textarea) {
      box-shadow: 0px 6px 24px 0px rgba(31, 35, 41, 0.08);
      background-color: #ffffff;
      border-radius: 8px;
      border: 1px solid #ffffff;
      box-sizing: border-box;

      &:has(.el-textarea__inner:focus) {
        border: 1px solid var(--el-color-primary);
      }

      .el-textarea__inner {
        border-radius: 8px !important;
        box-shadow: none;
        resize: none;
        padding: 13px 16px;
        box-sizing: border-box;
        min-height: 47px !important;
        height: 0;
      }

      .operate {
        padding: 6px 10px;
        .el-icon {
          font-size: 20px;
        }

        .sent-button {
          max-height: none;
          .el-icon {
            font-size: 24px;
          }
        }

        .el-loading-spinner {
          margin-top: -15px;

          .circular {
            width: 31px;
            height: 31px;
          }
        }
      }
    }
    .file-image {
      position: relative;
      overflow: inherit;

      .delete-icon {
        position: absolute;
        right: -5px;
        top: -5px;
        z-index: 1;
      }
    }

    .upload-tooltip-width {
      width: 300px;
    }
  }
}

@media only screen and (max-width: 768px) {
  .ai-chat {
    &__operate {
      position: fixed;
      bottom: 0;
      font-size: 1rem;
      .el-icon {
        font-size: 1.4rem !important;
      }
    }
  }
}
.popperUserInput {
  position: absolute;
  z-index: 999;
  left: 0;
  bottom: 50px;
  width: calc(100% - 50px);
  max-width: 400px;
}
</style>
