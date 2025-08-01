<template>
  <UserLoginLayout v-if="!loading" v-loading="loading">
    <LoginContainer v-if="chatUser.chat_profile?.authentication_type == 'password'">
      <template #logo>
        <div class="flex-center">
          <el-avatar
            v-if="isAppIcon(chatUser.chat_profile?.icon)"
            shape="square"
            :size="32"
            class="mr-8"
            style="background: none"
          >
            <img :src="chatUser.chat_profile?.icon" alt=""/>
          </el-avatar>
          <LogoIcon v-else height="32px" class="mr-8"/>
          <h4>{{ chatUser.chat_profile?.application_name }}</h4>
        </div>
      </template>
      <PasswordAuth></PasswordAuth>
    </LoginContainer>

    <LoginContainer v-else>
      <template #logo>
        <div class="flex-center">
          <el-avatar
            v-if="isAppIcon(chatUser.chat_profile?.icon)"
            shape="square"
            :size="32"
            class="mr-8"
            style="background: none"
          >
            <img :src="chatUser.chat_profile?.icon" alt=""/>
          </el-avatar>
          <LogoIcon v-else height="32px" class="mr-8"/>
          <h4>{{ chatUser.chat_profile?.application_name }}</h4>
        </div>
      </template>
      <h2 class="mb-24" v-if="!showQrCodeTab && (loginMode === 'LDAP' || loginMode === 'LOCAL')">
        {{ loginMode == 'LOCAL' ? $t('views.login.title') : loginMode }}
      </h2>
      <div v-if="!showQrCodeTab && (loginMode === 'LDAP' || loginMode === 'LOCAL')">
        <el-form
          class="login-form"
          :rules="rules"
          :model="loginForm"
          ref="loginFormRef"
          @keyup.enter="loginHandle"
        >
          <div class="mb-24">
            <el-form-item prop="username">
              <el-input
                size="large"
                class="input-item"
                v-model="loginForm.username"
                :placeholder="$t('views.login.loginForm.username.placeholder')"
              >
              </el-input>
            </el-form-item>
          </div>
          <div class="mb-24">
            <el-form-item prop="password">
              <el-input
                type="password"
                size="large"
                class="input-item"
                v-model="loginForm.password"
                :placeholder="$t('views.login.loginForm.password.placeholder')"
                show-password
              >
              </el-input>
            </el-form-item>
          </div>
          <div class="mb-24" v-if="loginMode !== 'LDAP'">
            <el-form-item prop="captcha">
              <div class="flex-between w-full">
                <el-input
                  size="large"
                  class="input-item"
                  v-model="loginForm.captcha"
                  :placeholder="$t('views.login.loginForm.captcha.placeholder')"
                >
                </el-input>

                <img
                  :src="identifyCode"
                  alt=""
                  height="38"
                  class="ml-8 cursor border border-r-6"
                  @click="makeCode"
                />
              </div>
            </el-form-item>
          </div>
        </el-form>

        <el-button
          size="large"
          type="primary"
          class="w-full"
          @click="loginHandle"
          :loading="loading"
        >
          {{ $t('views.login.buttons.login') }}
        </el-button>
      </div>
      <div v-if="showQrCodeTab">
        <QrCodeTab :tabs="orgOptions"/>
      </div>
      <div class="login-gradient-divider lighter mt-24" v-if="modeList.length > 1">
        <span>{{ $t('views.login.moreMethod') }}</span>
      </div>
      <div class="text-center mt-16">
        <template v-for="item in modeList">
          <el-button
            v-if="item !== 'LOCAL' && loginMode !== item && item !== 'QR_CODE'"
            circle
            :key="item"
            class="login-button-circle color-secondary"
            @click="changeMode(item)"
          >
            <span
              :style="{
                'font-size': item === 'OAUTH2' ? '8px' : '10px',
                color: theme.themeInfo?.theme,
              }"
            >{{ item }}</span
            >
          </el-button>
          <el-button
            v-if="item === 'QR_CODE' && loginMode !== item"
            circle
            :key="item"
            class="login-button-circle color-secondary"
            @click="changeMode('QR_CODE')"
          >
            <img src="@/assets/icon_qr_outlined.svg" width="25px"/>
          </el-button>
          <el-button
            v-if="item === 'LOCAL' && loginMode != 'LOCAL'"
            circle
            :key="item"
            class="login-button-circle color-secondary"
            style="font-size: 24px"
            icon="UserFilled"
            @click="changeMode('LOCAL')"
          />
        </template>
      </div>
    </LoginContainer>
  </UserLoginLayout>
</template>
<script setup lang="ts">
import {onMounted, ref, onBeforeMount} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import type {FormInstance, FormRules} from 'element-plus'
import type {LoginRequest} from '@/api/type/login'
import LoginContainer from '@/layout/login-layout/LoginContainer.vue'
import UserLoginLayout from '@/layout/login-layout/UserLoginLayout.vue'
import loginApi from '@/api/chat/chat.ts'
import {t, getBrowserLang} from '@/locales'
import useStore from '@/stores'
import {useI18n} from 'vue-i18n'
import QrCodeTab from '@/views/chat/user-login/scanCompinents/QrCodeTab.vue'
import {MsgConfirm, MsgError} from '@/utils/message.ts'
import PasswordAuth from '@/views/chat/auth/component/password.vue'
import {isAppIcon} from '@/utils/common'

const router = useRouter()
const {theme, chatUser} = useStore()
const {locale} = useI18n({useScope: 'global'})
const loading = ref<boolean>(false)
const route = useRoute()
const identifyCode = ref<string>('')
const {
  params: {accessToken},
} = route as any
const loginFormRef = ref<FormInstance>()
const loginForm = ref<LoginRequest>({
  username: '',
  password: '',
  captcha: '',
})

const rules = ref<FormRules<LoginRequest>>({
  username: [
    {
      required: true,
      message: t('views.login.loginForm.username.requiredMessage'),
      trigger: 'blur',
    },
  ],
  password: [
    {
      required: true,
      message: t('views.login.loginForm.password.requiredMessage'),
      trigger: 'blur',
    },
  ],
  captcha: [
    {
      required: true,
      message: t('views.login.loginForm.captcha.requiredMessage'),
      trigger: 'blur',
    },
  ],
})

const loginHandle = () => {
  loginFormRef.value?.validate().then(() => {
    if (loginMode.value === 'LDAP') {
      chatUser.ldapLogin(loginForm.value).then((ok) => {
        router.push({
          name: 'chat',
          params: {accessToken: chatUser.accessToken},
          query: route.query,
        })
      })
    } else {
      chatUser.login(loginForm.value).then((ok) => {
        router.push({
          name: 'chat',
          params: {accessToken: chatUser.accessToken},
          query: route.query,
        })
      })
    }
  })
}

function makeCode() {
  loginApi.getCaptcha().then((res: any) => {
    identifyCode.value = res.data.captcha
  })
}

onBeforeMount(() => {
  locale.value = chatUser.getLanguage()
  makeCode()
})

const modeList = ref<string[]>([])
const QrList = ref<any[]>([''])
const loginMode = ref('')
const showQrCodeTab = ref(false)

interface qrOption {
  key: string
  value: string
}

const orgOptions = ref<qrOption[]>([])

function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    const r = (Math.random() * 16) | 0
    const v = c === 'x' ? r : (r & 0x3) | 0x8
    return v.toString(16)
  })
}

function redirectAuth(authType: string, needMessage: boolean = false) {
  if (authType === 'LDAP' || authType === '') {
    return
  }
  loginApi.getAuthSetting(authType, loading).then((res: any) => {
    if (!res.data || !res.data.config) {
      return
    }

    const config = res.data.config
    const redirectUrl = eval(`\`${config.redirectUrl}/${accessToken}\``)
    let url
    if (authType === 'CAS') {
      url = config.ldpUri
      url +=
        url.indexOf('?') !== -1
          ? `&service=${encodeURIComponent(redirectUrl)}`
          : `?service=${encodeURIComponent(redirectUrl)}`
    } else if (authType === 'OIDC') {
      const scope = config.scope || 'openid+profile+email'
      url = `${config.authEndpoint}?client_id=${config.clientId}&redirect_uri=${redirectUrl}&response_type=code&scope=${scope}`
      if (config.state) {
        url += `&state=${config.state}`
      }
    } else if (authType === 'OAuth2') {
      url = `${config.authEndpoint}?client_id=${config.clientId}&response_type=code&redirect_uri=${redirectUrl}&state=${uuidv4()}`
      if (config.scope) {
        url += `&scope=${config.scope}`
      }
    }
    if (!url) {
      return
    }
    if (needMessage) {
      MsgConfirm(t('views.login.jump_tip'), '', {
        confirmButtonText: t('views.login.jump'),
        cancelButtonText: t('common.cancel'),
        confirmButtonClass: '',
      })
        .then(() => {
          window.location.href = url
        })
        .catch(() => {
        })
    } else {
      console.log('url', url)
      window.location.href = url
    }
  })
}

function changeMode(val: string) {
  loginMode.value = val === 'LDAP' ? val : 'LOCAL'
  if (val === 'QR_CODE') {
    loginMode.value = val
    showQrCodeTab.value = true
    return
  }
  showQrCodeTab.value = false
  loginForm.value = {
    username: '',
    password: '',
    captcha: '',
  }
  redirectAuth(val)
  loginFormRef.value?.clearValidate()
}

onBeforeMount(() => {
  if (chatUser.chat_profile?.login_value) {
    modeList.value = chatUser.chat_profile.login_value
    if (modeList.value.includes('LOCAL')) {
      modeList.value = ['LOCAL', ...modeList.value.filter((item) => item !== 'LOCAL')]
    } else if (modeList.value.includes('LDAP')) {
      modeList.value = ['LDAP', ...modeList.value.filter((item) => item !== 'LDAP')]
    }
    loginMode.value = modeList.value[0] || 'LOCAL'
    if (!modeList.value.includes('LOCAL') && !modeList.value.includes('LDAP')) {
      loginMode.value = ''
    }
    if (modeList.value.length == 1 && ['CAS', 'OIDC', 'OAuth2'].includes(modeList.value[0])) {
      redirectAuth(modeList.value[0])
    }
    // 这里的modeList 是oauth2 cas ldap oidc 这四个 还会有 lark wecom dingtalk
    // 获取到的 modeList中除'CAS', 'OIDC', 'OAuth2' LOCAL之外的登录方式
    QrList.value = modeList.value.filter((item) => !['CAS', 'OIDC', 'OAuth2', 'LOCAL', 'LDAP'].includes(item))
    // modeList需要去掉lark wecom dingtalk
    modeList.value = modeList.value.filter((item) => !['lark', 'wecom', 'dingtalk'].includes(item))
    if (QrList.value.length > 0) {
      modeList.value.push('QR_CODE')
      QrList.value.forEach((item) => {
        orgOptions.value.push({
          key: item,
          value:
            item === 'wecom'
              ? t('views.system.authentication.scanTheQRCode.wecom')
              : item === 'dingtalk'
                ? t('views.system.authentication.scanTheQRCode.dingtalk')
                : t('views.system.authentication.scanTheQRCode.lark'),
        })
      })
    }
  }
})
</script>
<style lang="scss" scoped>
.login-gradient-divider {
  position: relative;
  text-align: center;
  color: var(--el-color-info);

  ::before {
    content: '';
    width: 25%;
    height: 1px;
    background: linear-gradient(90deg, rgba(222, 224, 227, 0) 0%, #dee0e3 100%);
    position: absolute;
    left: 16px;
    top: 50%;
  }

  ::after {
    content: '';
    width: 25%;
    height: 1px;
    background: linear-gradient(90deg, #dee0e3 0%, rgba(222, 224, 227, 0) 100%);
    position: absolute;
    right: 16px;
    top: 50%;
  }
}

.login-button-circle {
  padding: 20px !important;
  margin: 0 4px;
  width: 32px;
  height: 32px;
  text-align: center;
}
</style>
