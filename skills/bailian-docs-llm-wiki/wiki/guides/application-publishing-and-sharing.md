# application publishing and sharing

应用发布与分享功能允许开发者将构建完成的应用对外提供服务或复用为组件。该能力覆盖公开分享、嵌入集成、UI定制及跨应用复用等典型场景，适用于工作流（Workflow）和智能体（Agent）两类核心应用形态。所有操作均通过百炼控制台或 OpenAPI 完成，无需修改底层代码。

## 支持的模型/功能

- **应用分享**：生成可公开访问的 HTTPS 链接，支持设置访问权限（公开/私有/指定用户），并可嵌入到第三方页面（iframe 或 SDK 方式）。详见 [应用分享](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **发布为组件**：将 Agent 或 Workflow 封装为可被其他应用调用的标准组件（如 API 端点或低代码拖拽节点），支持参数透传与异步回调。该能力仅适用于 workflow 类型应用，Agent 类型暂不支持同步响应模式——详见 [发布为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **UI 设计器**：提供可视化界面配置能力，支持自定义 Logo、主题色、输入框 placeholder、结果展示模板等；导出的 UI 配置可与分享链接或组件绑定。具体控件列表和约束参见 [UI设计](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

> **注意**：原始文档中“发布为组件”章节未明确说明 Agent 类型组件在 v2.3+ 版本中已支持 webhook 回调模式，但当前控制台 UI 仍默认禁用 Agent 的组件发布入口。建议优先使用 workflow 类型，或通过 OpenAPI `POST /v1/applications/{app_id}/components` 显式启用（需 `component_type=agent` + `callback_url`）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `share_mode` | string | 是 | 取值：`public` / `private` / `whitelist`；影响分享链接的访问控制策略 |
| `embed_config.allow_origin` | string[] | 否 | 指定 iframe 嵌入白名单域名，为空时禁止 iframe 加载（默认行为） |
| `ui_config` | object | 否 | 符合 [UI设计](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 规范的 JSON 对象，用于定制前端样式与交互 |
| `component_type` | string | 是（组件场景） | 仅限 `workflow` 或 `agent`；注意 `agent` 类型组件需额外配置 `callback_url` |

## 使用方式

1. **控制台操作**：进入应用详情页 →「发布与分享」标签页 → 选择「分享应用」或「发布为组件」→ 配置参数 → 点击「发布」；
2. **OpenAPI 调用**：
   - 分享应用：`POST /v1/applications/{app_id}/share`
   - 发布组件：`POST /v1/applications/{app_id}/components`
   - 所有请求需携带 `Authorization: Bearer <access_token>` 与正确 `Content-Type: application/json`；
3. **SDK 集成（Web）**：使用 `@bailian-ai/web-sdk` 的 `EmbedApp` 组件，传入分享 URL 与 `embedConfig` 即可渲染（参考 [应用分享](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 中的 embed 示例）。

## 限制和注意事项

- 单个应用最多同时存在 1 个 active 的分享链接和 1 个 active 的组件端点；
- UI 配置变更后需重新发布才能生效，历史分享链接/组件不自动更新；
- 私有分享链接有效期默认 30 天，可通过 API 的 `expires_in` 字段延长（最大 365 天）；
- 使用 [UI设计](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 中的「高级模板」功能需开通企业版权限；
- Agent 类型组件若未配置 `callback_url`，调用将立即返回 `{"status":"pending"}`，客户端须轮询或监听 webhook，此行为与文档 [发布为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) 中“同步返回结果”的旧描述存在偏差。

## 来源文档

- [应用发布与分享](../../raw/application-user-guide/application-publishing-and-sharing.md)


