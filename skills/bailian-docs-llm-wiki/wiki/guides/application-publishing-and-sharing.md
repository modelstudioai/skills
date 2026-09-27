# application publishing and sharing

应用发布与分享功能允许开发者将构建完成的应用对外公开、嵌入到第三方系统，或作为可复用组件供其他应用调用。该能力覆盖 Web 端分享、API 接口发布、UI 定制化导出及跨应用组件复用等核心场景。所有操作均通过百炼控制台「发布」页签或 OpenAPI 完成，无需修改应用底层逻辑。

## 支持的模型/功能

- **公开分享**：生成带访问权限控制（公开/仅链接可见/指定用户）的 Web URL，支持自定义域名和 HTTPS 强制跳转  
- **API 发布**：为 Workflow 或 Agent 自动生成 RESTful API 端点（`POST /v1/applications/{app_id}/invoke`），兼容 OpenAPI 3.0 规范  
- **UI 组件化嵌入**：导出轻量级 `<script>` 标签代码，支持在任意 HTML 页面中以 iframe 或 SDK 方式加载应用 UI [原文标题](../../raw/application-user-guide/application-publishing-and-sharing.md)  
- **作为组件复用**：将当前应用注册为 `component` 类型资源，供其他 Workflow 的「调用组件」节点直接引用，支持输入/输出 Schema 显式声明 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)  

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `visibility` | string | 是 | 取值：`public` / `link_only` / `private`；影响分享链接的默认访问策略 |
| `custom_domain` | string | 否 | 仅限企业版；需提前在控制台绑定并验证域名，格式如 `ai.example.com` |
| `enable_cors` | boolean | 否 | 仅 API 发布时生效；启用后自动配置 `Access-Control-Allow-Origin: *`（生产环境建议显式指定 origin） |
| `input_schema` | object | 否 | 当发布为组件时必填；JSON Schema 格式，用于校验上游传入参数 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |

> **注意**：文档中提及的 `ui_designer` 功能（如拖拽布局导出）目前仅支持基础模板，高级交互定制（如动态表单联动）尚未开放 API 控制，详见 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 中的「限制说明」章节——该描述与当前 v2.3.0 控制台实际能力一致，但 OpenAPI 文档未同步更新此约束。

## 使用方式

1. **控制台操作**：进入应用详情页 → 左侧导航选择「发布」→ 配置 visibility、domain 等参数 → 点击「发布」获取 URL 或 API [Token](../concepts/token.md)  
2. **OpenAPI 调用**：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/applications/{app_id}/publish \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"visibility":"link_only","enable_cors":true}'
   ```
3. **前端嵌入**：发布成功后，在「分享」页复制 `<script src="https://.../embed.js?app_id=xxx"></script>` 并插入 HTML body

## 限制和注意事项

- 单个应用最多同时发布 5 个不同 `visibility` 配置的实例（例如：1 个 public + 2 个 link_only + 2 个 private）  
- API 发布后，`/invoke` 端点默认启用流式响应（`text/event-stream`），若客户端不支持 SSE，需在请求头添加 `X-Disable-Stream: true`  
- 作为组件被调用时，调用方 Workflow 的超时时间（`timeout_seconds`）将覆盖被调用方自身的超时设置，且不可继承重试策略  
- 免费版用户无法使用 `custom_domain` 和 `enable_cors` 参数，相关字段在 API 请求中会被静默忽略

## 来源文档

- [应用发布与分享](../../raw/application-user-guide/application-publishing-and-sharing.md)


