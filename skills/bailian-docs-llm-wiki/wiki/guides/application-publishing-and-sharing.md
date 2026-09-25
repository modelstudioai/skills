# application publishing and sharing

应用发布与分享功能允许开发者将构建完成的应用对外提供服务或复用为组件。该能力覆盖公开分享、嵌入集成、UI定制化及跨应用复用等典型场景，适用于私有部署和百炼云环境。具体行为受模型类型、权限配置及平台版本约束，需结合 [应用发布与分享](../../raw/application-user-guide/application-publishing-and-sharing.md) 文档整体理解。

## 支持的模型/功能

- **公开分享**：生成可访问的 URL，支持设置访问密码与过期时间（仅限 Standard 和 Pro 版本）  
- **嵌入式集成**：通过 iframe 或 SDK 将应用嵌入第三方页面，需启用「允许嵌入」开关  
- **发布为组件**：将 Agent 或 Workflow 发布为可被其他应用调用的组件，支持输入/输出 Schema 声明 —— 详见 [发布为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)  
- **UI 定制**：使用可视化 UI 设计器调整对话界面布局、按钮文案、主题色等，导出后生效于所有分享渠道  

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `share_mode` | string | 是 | 取值：`public`（无需登录）、`password`（密码保护）、`internal`（仅组织内可见） |
| `embeddable` | boolean | 否 | 默认 `false`；设为 `true` 后支持 iframe 嵌入，需配合 CSP 白名单配置 |
| `component_schema` | object | 仅当发布为组件时必填 | 遵循 OpenAPI 3.0 格式定义 inputs/outputs，参考 [发布为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) 中的字段规范 |

> **注意**：`share_mode=public` 在私有化部署中默认禁用，需管理员在 `settings.yaml` 中显式开启 `enable_public_sharing: true`；该限制未在 [应用分享](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 中明确说明，以平台实际配置为准。

## 使用方式

1. 在应用编辑页点击「发布」→「分享设置」，配置 `share_mode` 与访问控制策略  
2. 如需嵌入，勾选「允许嵌入」并复制 iframe 代码或调用 `@bailian-sdk/embed`  
3. 如需发布为组件，在「组件管理」页选择目标 Agent/Workflow，填写 `component_schema` 后提交审核（审核由平台自动完成，通常 <30 秒）  
4. 所有操作均需调用 `/v1/applications/{app_id}/publish` API 或通过控制台触发，底层逻辑详见 [应用发布与分享](../../raw/application-user-guide/application-publishing-and-sharing.md)

## 限制和注意事项

- 单个应用最多同时存在 5 个有效分享链接（含 password/internal 模式）  
- UI 设计器修改仅影响分享后的前端渲染，不影响 API 调用的响应结构  
- 发布为组件后，原始应用的调试模式（Debug Mode）将自动关闭，且不可逆；此行为在 [UI设计](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 文档中未提及，属隐式约束  
- 私有化部署环境下，`embeddable=true` 需额外配置 Nginx 反向代理头 `X-Frame-Options: ALLOWALL`，否则 iframe 加载失败

## 来源文档

- [应用发布与分享](../../raw/application-user-guide/application-publishing-and-sharing.md)


