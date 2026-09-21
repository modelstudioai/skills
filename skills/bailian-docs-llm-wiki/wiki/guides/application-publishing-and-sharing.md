# application publishing and sharing

应用发布与分享功能允许开发者将构建完成的应用对外提供服务，或作为可复用组件集成到其他系统中。支持两种主要模式：生成公开访问链接（Share）和封装为标准组件（Publish as Component）。该能力依赖于百炼平台的运行时环境与权限体系，需在应用配置中明确设置可见性与调用方式。

## 支持的模型/功能

- **应用分享（Share）**：生成带身份校验的 HTTPS 访问链接，支持设置访问密码、有效期及查看/编辑权限；适用于快速协作或灰度验证。  
- **发布为组件（Publish as Component）**：将应用封装为符合 OpenAPI 3.0 规范的 HTTP API 组件，或导出为 SDK（Python/Node.js），供其他应用或外部系统调用。  
- **UI 设计器集成**：发布前可通过 [UI 设计器](raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 自定义前端交互逻辑与布局，该能力直接影响分享链接的用户界面表现，详见 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `visibility` | string | 是 | 取值：`public`（无需鉴权）、`internal`（仅同租户）、`private`（需邀请）；影响分享链接和组件的默认访问策略 |
| `auth_mode` | string | 否 | 取值：`none` / `api_key` / `oauth2`；仅当 `visibility != public` 时生效，控制组件 API 的认证方式 |
| `ttl_seconds` | integer | 否 | 分享链接有效期（秒），最大 2592000（30 天），默认 86400（24 小时） |
| `ui_config` | object | 否 | 由 [UI 设计器](raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 导出的 JSON 配置，决定分享页面的渲染行为；其 schema 定义见 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing.md) |

## 使用方式

1. 在应用编辑页点击「发布」→ 选择「分享」或「发布为组件」；  
2. 根据向导填写参数（如 `visibility`、`ttl_seconds` 等），UI 配置项自动从当前 [UI 设计器](raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 状态同步；  
3. 点击「确认发布」，平台返回分享链接或 OpenAPI 文档 URL；  
4. （组件模式）调用方通过 `curl` 或 SDK 初始化客户端，传入 `api_key`（若启用）即可调用，示例见 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing.md)。

## 限制和注意事项

- 单个应用最多同时存在 5 个有效分享链接（含过期未清理者），超出需先撤销旧链接；  
- 发布为组件后，其 OpenAPI 接口不支持动态修改请求体结构（如新增 required 字段），变更需重新发布；  
- > **注意**：文档中提及“支持 WebSocket 流式响应”（见 `share-an-application.md`）与当前平台实际能力不符——截至 v2.4.0，组件 API 仅支持 HTTP/1.1 短连接，流式响应需通过 `/stream` 子路径显式启用，且不兼容所有客户端 SDK。  
- 私有分享链接的访问日志仅保留 7 天，组件 API 调用日志需配合百炼监控服务单独开启。

## 来源文档

- [应用发布与分享](../../raw/application-user-guide/application-publishing-and-sharing.md)


