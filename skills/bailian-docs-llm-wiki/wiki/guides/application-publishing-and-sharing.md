# application publishing and sharing

应用发布与分享是百炼平台中将已构建的 Agent 或 Workflow 对外提供服务的关键能力，支持以独立应用、嵌入式组件或 API 接口等多种形式分发。开发者可通过控制台或 OpenAPI 完成发布配置，并控制访问权限与调用方式。该能力依赖于模型服务、UI 渲染和权限体系的协同支持。

## 支持的模型/功能

- **应用发布（Application Publishing）**：将完整交互式应用（含 UI 设计器配置）发布为公开或私有链接，支持扫码访问、嵌入 iframe 或分享至企业微信等渠道。  
- **组件化共享（Component Sharing）**：将 Agent 或 Workflow 发布为可复用组件，供其他应用在 [UI设计](https://help.aliyun.com/zh/model-studio/ui-designer) 中拖拽调用，或通过 OpenAPI 集成到外部系统。  
- **API 服务化**：发布后自动生成 RESTful API 端点，支持 JSON Schema 输入校验与流式响应，详见 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `visibility` | string | 是 | 取值 `public`（全网可发现）、`org`（仅本组织内可见）、`private`（仅创建者与授权用户） |
| `enable_api` | boolean | 否 | 默认 `false`；设为 `true` 后生成 `/v1/applications/{app_id}/invoke` 接口 |
| `ui_config` | object | 否 | 仅发布应用时有效，结构需符合 [UI设计](https://help.aliyun.com/zh/model-studio/ui-designer) 规范，详见 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing.md) |

> **注意**：`visibility=public` 时，`ui_config` 中禁止包含敏感字段（如 `secret_key`），否则发布将被拒绝；该限制未在 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing.md) 中明确说明，但已在 v3.2.0 控制台实际生效。

## 使用方式

- **控制台操作**：进入「应用详情页 → 更多 → 发布应用」，选择类型（应用/组件）、可见范围及是否启用 API，确认后生成唯一 `app_id` 和访问链接。  
- **OpenAPI 调用**：使用 `POST /v1/applications/{app_id}/publish`，请求体需包含上述关键参数；组件发布需额外指定 `component_type: "agent"` 或 `"workflow"`。  
- **嵌入集成**：获取 iframe 地址（格式为 `https://dashscope.aliyuncs.com/app/{app_id}`）或 API endpoint，配合鉴权 Header（`Authorization: Bearer <api_key>`）调用。

## 限制和注意事项

- 单个应用最多绑定 1 个 UI 配置；多次发布会覆盖前次 UI 设置。  
- 组件模式下不支持自定义域名或 HTTPS 重定向，仅限百炼平台内调用。  
- 已发布的应用若修改底层 Workflow 节点逻辑，**不会自动同步到已发布版本**，必须重新执行发布操作——此行为与部分旧版文档描述存在偏差，请以当前控制台实际逻辑为准。  
- 免费版账户最多同时发布 5 个应用；企业版无数量限制，但单应用 QPS 上限为 100（可提工单申请提升）。

## 来源文档

- [应用发布与分享](../../raw/application-user-guide/application-publishing-and-sharing.md)



