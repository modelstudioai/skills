# application publishing and sharing

应用发布与分享是百炼平台中将已构建的 Agent 或 Workflow 对外提供服务的关键能力，支持以独立应用、嵌入式组件或 API 接口等多种形式分发。开发者可通过控制台或 OpenAPI 完成发布配置，并设置访问权限与 UI 表现。该能力依赖于应用的运行时环境和模型绑定策略，需确保所选模型具备对应权限。

## 支持的模型/功能

- 支持将应用发布为**独立 Web 应用**（含自定义域名、UI 主题、引导页等），详见 [应用发布与分享](../../raw/application-user-guide/application-publishing-and-sharing.md)  
- 支持发布为**可复用组件**，供其他工作流或低代码平台调用，支持输入 Schema 声明与输出标准化，参考 [发布为组件](../../raw/application-user-guide/application-publishing-and-sharing.md)  
- 支持导出为 **OpenAPI 3.0 规范的 RESTful 接口**（需启用 API 模式），底层自动适配所绑定的推理模型（如 Qwen-Max、Qwen-Plus 等），但不支持非百炼托管的第三方模型接入。  
- UI 设计能力（如表单字段定制、响应式布局）仅在发布为 Web 应用时生效，[UI设计](../../raw/application-user-guide/application-publishing-and-sharing.md) 文档说明了可用控件与变量绑定语法。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `publish_type` | string | 是 | 取值：`web_app`、`component`、`api`；决定发布形态与后续配置项 |
| `access_control` | object | 否 | 包含 `auth_mode`（`public` / `invite_only` / `private`）及 `allowed_users` 列表（仅 `invite_only` 有效） |
| `ui_config` | object | 否 | 仅 `web_app` 有效；结构见 [UI设计](../../raw/application-user-guide/application-publishing-and-sharing.md) 所述 schema |
| `component_input_schema` | JSON Schema | 否 | 仅 `component` 有效；定义外部调用时必需的输入字段约束 |

> **注意**：原始文档中未明确 `api` 类型是否支持流式响应（`stream: true`）。实测当前版本（v2024.07）中 `api` 发布模式默认关闭流式，需显式在 `advanced_options.stream_enabled = true` 并确保后端模型支持；该行为与 [应用发布与分享](../../raw/application-user-guide/application-publishing-and-sharing.md) 中“API 默认启用流式”的描述矛盾，建议以 OpenAPI 响应头 `X-Stream-Enabled: true` 实际返回为准。

## 使用方式

1. **控制台操作**：进入应用详情页 →「发布」标签页 → 选择发布类型 → 配置参数 → 点击「发布」→ 获取访问链接或 SDK 调用代码  
2. **OpenAPI 调用**：使用 `POST /v1/applications/{app_id}/publish`，请求体传入上述关键参数；需携带 `Authorization: Bearer <token>` 且 token 具备 `app:publish` 权限  
3. **组件集成**：发布为 `component` 后，在目标工作流编辑器中通过「添加组件」搜索并拖入，系统自动注入 `input` 和 `output` binding 配置  

## 限制和注意事项

- 单个应用最多同时存在 **3 个已发布的版本**（含草稿），旧版本需手动下线才能发布新版本  
- `web_app` 类型不支持跨区域访问加速（如全球 CDN），所有请求路由至应用部署所在地域（如 `cn-shanghai`）  
- 发布为 `component` 后，若源应用修改了输入 Schema，**不会自动同步到已引用该组件的工作流**，需人工重新绑定或更新版本号  
- 所有发布行为均受项目级配额限制：每个项目最多发布 50 个应用（含各类型），超出需提工单申请扩容  
- 若应用绑定了私有模型（如 VPC 内部署的自定义模型），发布为 `web_app` 或 `api` 后，外部用户请求仍受限于该模型的网络策略——即仅当模型服务允许公网/ALB 访问时，发布才实际可用

## 来源文档

- [应用发布与分享](../../raw/application-user-guide/application-publishing-and-sharing.md)


