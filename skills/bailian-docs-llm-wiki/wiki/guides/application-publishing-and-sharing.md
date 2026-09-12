# application publishing and sharing

应用发布与分享是百炼平台中将已构建的 Agent 或 Workflow 对外提供服务的关键能力，支持以独立应用、嵌入式组件或 API 接口等多种形式分发。开发者可通过控制台或 OpenAPI 完成发布配置，并设置访问权限与 UI 表现。该能力依赖于应用的运行时环境和模型绑定策略，需确保所选模型具备对应权限。

## 支持的模型/功能

- 支持将应用发布为**独立 Web 应用**（含自定义域名、登录鉴权）、**嵌入式组件**（供其他系统通过 iframe 或 SDK 集成），或**后端 API 服务**（通过 `/v1/chat/completions` 等标准接口调用）  
- 发布时可绑定的模型限于当前工作空间已授权且处于 `ACTIVE` 状态的模型，包括 Qwen 系列大模型、多模态模型（如 Qwen-VL）及部分第三方模型（需单独开通）  
- UI 设计能力仅在发布为 Web 应用时生效，支持通过 [UI设计](https://help.aliyun.com/zh/model-studio/ui-designer) 进行可视化配置，该功能在 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing.md) 中有基础说明

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `publish_type` | string | 是 | 取值：`web_app`、`component`、`api`；决定发布形态和后续调用方式 |
| `access_control` | object | 否 | 包含 `auth_mode`（`none`/`aliyun_account`/`custom_token`）和白名单配置 |
| `ui_config` | object | 否 | 仅 `web_app` 有效；结构参考 [UI设计](https://help.aliyun.com/zh/model-studio/ui-designer)，实际字段定义详见 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing.md) |
| `component_options` | object | 否 | 仅 `component` 有效；含 `iframe_sandbox`、`sdk_version` 等，详细字段见 [发布为组件](https://help.aliyun.com/zh/model-studio/use-agent-or-workflow-as-component) 对应文档 |

> **注意**：`access_control.auth_mode=custom_token` 要求应用后端实现 token 校验逻辑，但当前 OpenAPI 文档中未明确校验协议细节；建议优先使用 `aliyun_account` 模式，其行为与 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing.md) 描述一致，避免兼容性风险。

## 使用方式

1. **控制台操作**：进入应用详情页 → 点击「发布」→ 选择发布类型 → 配置参数 → 点击「确认发布」  
2. **OpenAPI 调用**：调用 `POST /applications/{app_id}/publish`，请求体需符合上述关键参数结构  
3. **获取访问地址/API Endpoint**：发布成功后，控制台显示 `web_url`、`component_url` 或 `api_endpoint`，其中 `api_endpoint` 默认启用签名认证（`X-Bailian-Signature`）

## 限制和注意事项

- 单个工作空间最多发布 50 个 Web 应用，100 个组件实例，API 服务无数量限制但受 QPS 配额约束  
- 发布为组件时，`component_url` 仅支持 HTTPS 协议，且目标页面需启用 `X-Frame-Options: ALLOW-FROM` 或 `Content-Security-Policy: frame-ancestors` 白名单  
- 已发布的应用若修改底层 Workflow 或模型配置，**不会自动同步到已发布实例**；必须重新执行发布操作才能生效  
- 所有发布行为均受工作空间所属主账号的 RAM 权限控制，`bailian:PublishApplication` 权限为必需项  

> **注意**：文档中提及的 [应用分享](https://help.aliyun.com/zh/model-studio/share-an-application) 功能实际已被整合进「Web 应用发布」流程，旧版“分享链接”模式（无需登录即可访问）已在 v3.2.0 后废弃；请勿参考过时帮助页中的独立分享入口说明。

## 来源文档

- [应用发布与分享](../../raw/application-user-guide/application-publishing-and-sharing.md)


