import { SourceTypeEnum } from '@/enums/common'
import { get_next_route } from '@/utils/permission'

import { EditionConst, PermissionConst, RoleConst } from '@/utils/permission/data'
import { ComplexPermission } from '@/utils/permission/type'

const ApplicationDetailRouter = {
  path: '/application/:id/:type',
  name: 'ApplicationDetail',
  meta: { title: 'views.applicationOverview.title', activeMenu: '/application', breadcrumb: true },
  component: () => import('@/layout/layout-template/MainLayout.vue'),
  hidden: true,
  children: [
    {
      path: 'overview',
      name: 'AppOverview',
      meta: {
        icon: 'app-all-menu',
        iconActive: 'app-all-menu-active',
        title: 'views.applicationOverview.title',
        active: 'overview',
        parentPath: '/application/:id/:type',
        parentName: 'ApplicationDetail',
        permission: [
          () => {
              const to: any = get_next_route()
           return new ComplexPermission([RoleConst.USER],[PermissionConst.APPLICATION.getApplicationWorkspaceResourcePermission( to ? to.params.id : '',)],[],'AND')},

          RoleConst.WORKSPACE_MANAGE.getWorkspaceRole,
          PermissionConst.APPLICATION_OVERVIEW_READ.getWorkspacePermissionWorkspaceManageRole,
          () => {
            const to: any = get_next_route()
            return PermissionConst.APPLICATION_OVERVIEW_READ.getApplicationWorkspaceResourcePermission(
              to ? to.params.id : '',
            )
          }
        ]
      },
      component: () => import('@/views/application-overview/index.vue'),
    },
    {
      path: 'setting',
      name: 'AppSetting',
      meta: {
        icon: 'app-setting',
        iconActive: 'app-setting-active',
        title: 'common.setting',
        active: 'setting',
        parentPath: '/application/:id/:type',
        parentName: 'ApplicationDetail',
        permission: [
          () => {
              const to: any = get_next_route()
           return new ComplexPermission([RoleConst.USER],[PermissionConst.APPLICATION.getApplicationWorkspaceResourcePermission( to ? to.params.id : '',)],[],'AND')},
          RoleConst.WORKSPACE_MANAGE.getWorkspaceRole,
          PermissionConst.APPLICATION_EDIT.getWorkspacePermissionWorkspaceManageRole,
          () => {
            const to: any = get_next_route()
            return PermissionConst.APPLICATION_EDIT.getApplicationWorkspaceResourcePermission(
              to ? to.params.id : '',
            )
          }
        ]
      },
      component: () => import('@/views/application/ApplicationSetting.vue'),
    },
    {
      path: 'access',
      name: 'AppAccess',
      meta: {
        icon: 'app-access',
        iconActive: 'app-access-active',
        title: 'views.application.applicationAccess.title',
        active: 'access',
        parentPath: '/application/:id/:type',
        parentName: 'ApplicationDetail',
        permission: [
          () => {
              const to: any = get_next_route()
           return new ComplexPermission([RoleConst.USER],[PermissionConst.APPLICATION.getApplicationWorkspaceResourcePermission( to ? to.params.id : '',)],[EditionConst.IS_EE, EditionConst.IS_PE],'AND')},
          new ComplexPermission([RoleConst.WORKSPACE_MANAGE.getWorkspaceRole,],[PermissionConst.APPLICATION_ACCESS_READ.getWorkspacePermissionWorkspaceManageRole],[EditionConst.IS_EE, EditionConst.IS_PE],'OR'),
          new ComplexPermission([],[() => {
            const to: any = get_next_route()
            return PermissionConst.APPLICATION_ACCESS_READ.getApplicationWorkspaceResourcePermission(
              to ? to.params.id : '',)
          }],[EditionConst.IS_EE, EditionConst.IS_PE],'OR'),
        ]
      },
      component: () => import('@/views/application/ApplicationAccess.vue'),
    },
    {
      path: 'chat-user',
      name: 'applicationChatUser',
      meta: {
        icon: 'app-user-chat',
        iconActive: 'app-user-chat',
        title: 'views.chatUser.title',
        active: 'chat-user',
        parentPath: '/application/:id/:type',
        parentName: 'ApplicationDetail',
        resourceType: SourceTypeEnum.APPLICATION,
        permission: [
          () => {
              const to: any = get_next_route()
           return new ComplexPermission([RoleConst.USER],[PermissionConst.APPLICATION.getApplicationWorkspaceResourcePermission( to ? to.params.id : '',)],[EditionConst.IS_EE, EditionConst.IS_PE],'AND')},
          new ComplexPermission([RoleConst.WORKSPACE_MANAGE.getWorkspaceRole],[PermissionConst.APPLICATION_CHAT_USER_READ.getWorkspacePermissionWorkspaceManageRole],[EditionConst.IS_EE, EditionConst.IS_PE],'OR')
           ,
          () => {
            const to: any = get_next_route()
            return new ComplexPermission([],[PermissionConst.APPLICATION_CHAT_USER_READ.getApplicationWorkspaceResourcePermission(
              to ? to.params.id : '',)],[EditionConst.IS_EE, EditionConst.IS_PE],'OR')
          }
        ]
      },
      component: () => import('@/views/chat-user/index.vue'),
    },
    {
      path: 'chat-log',
      name: 'ChatLog',
      meta: {
        icon: 'app-document',
        iconActive: 'app-document-active',
        title: 'views.chatLog.title',
        active: 'chat-log',
        parentPath: '/application/:id/:type',
        parentName: 'ApplicationDetail',
        permission: [
          () => {
              const to: any = get_next_route()
           return new ComplexPermission([RoleConst.USER],[PermissionConst.APPLICATION.getApplicationWorkspaceResourcePermission( to ? to.params.id : '',)],[],'AND')},
          RoleConst.WORKSPACE_MANAGE.getWorkspaceRole,
          PermissionConst.APPLICATION_CHAT_LOG_READ.getWorkspacePermissionWorkspaceManageRole,
          () => {
            const to: any = get_next_route()
            return PermissionConst.APPLICATION_CHAT_LOG_READ.getApplicationWorkspaceResourcePermission(
              to ? to.params.id : '',
            )
          }
        ]
      },
      component: () => import('@/views/chat-log/index.vue'),
    },
  ],
}

export default ApplicationDetailRouter
