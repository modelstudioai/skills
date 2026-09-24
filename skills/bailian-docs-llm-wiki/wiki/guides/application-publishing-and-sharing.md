# application publishing and sharing

应用发布与分享功能允许开发者将构建完成的应用对外分发，支持以公开链接、嵌入式组件或 API 形式提供服务。该能力覆盖从单页应用分享到跨平台复用的完整链路，适用于内部协作、客户交付及生态集成等场景。具体行为受模型类型、权限配置及部署环境共同约束。

## 支持的模型/功能

- **公开分享（Share）**：生成可访问的 HTTPS 链接，支持设置访问密码与有效期（见 [应用分享](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)）  
- **发布为组件（Publish as Component）**：将 Agent 或 Workflow 封装为可嵌入第三方页面的 `<iframe>` 或 React/Vue 组件（见 [发布为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)）  
- **UI 设计器集成**：在 UI 设计器中直接预览并导出发布后的界面样式与交互逻辑（见 [UI设计](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)）

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `share_mode` | string | 可选 `"public"`、`"password"`、`"invite_only"`；默认为 `"public"` |
| `expire_at` | ISO8601 timestamp | 仅对 `password` 和 `invite_only` 模式生效；超过时间后链接自动失效 |
| `embed_config` | object | 控制嵌入行为，含 `height`、`width`、`autoResize` 等字段，详见 [发布为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |

> **注意**：文档 [UI设计](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 中提及的 `theme_override` 参数在 v2.3+ 版本已废弃，实际生效需通过 `ui_config.theme` 字段配置，以 [应用分享](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 的最新描述为准。

## 使用方式

1. 在应用编辑页点击「发布」→「分享」或「发布为组件」  
2. 根据目标场景选择模式并填写参数（如密码、过期时间、嵌入尺寸）  
3. 调用 `POST /v1/applications/{app_id}/publish` 接口提交配置（SDK 示例见 [应用分享](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)）  
4. 获取返回的 `share_url` 或 `embed_code` 并集成使用  

## 限制和注意事项

- 免费版账户最多同时存在 5 个有效分享链接；企业版无此限制  
- 嵌入组件不支持跨域 Cookie 传递，身份鉴权需通过 `auth_token` 查询参数或后端代理实现  
- 所有分享链接默认继承应用当前版本（非 draft），但若在分享后更新应用逻辑，需手动重新发布以同步变更  
- **重要**：`share_mode=invite_only` 模式下，邀请链接仅对首次打开者有效，且无法通过 API 批量生成；该行为与 [发布为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) 中描述的“批量邀请”功能存在不一致，建议以控制台实际行为为准

## 来源文档

- [应用发布与分享](../../raw/application-user-guide/application-publishing-and-sharing.md)


