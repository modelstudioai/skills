# application publishing and sharing

应用发布与分享是百炼平台中将已构建的 Agent 或 Workflow 对外提供服务的关键能力，支持以独立应用、嵌入式组件或 API 接口等多种形式分发。开发者可通过控制台或 OpenAPI 完成发布配置，并设置访问权限与 UI 表现。该能力依赖于应用的运行时环境和模型绑定策略，需确保所选模型具备对应权限。

## 支持的模型/功能

- 支持发布为**独立 Web 应用**（含自定义域名、UI 主题、登录鉴权等），适用于终端用户直接访问；
- 支持发布为**可复用组件**（Component），供其他 Agent 或 Workflow 调用，详见 [发布为组件](../../raw/application-user-guide/application-publishing-and-sharing.md)；
- 支持导出为 **OpenAPI v3 标准接口**，兼容主流集成工具（如 Postman、低代码平台）；
- 所有发布形态均支持绑定百炼托管模型（如 qwen-max、qwen-plus）或用户自有模型（需已通过 [模型接入与管理](../../raw/model-management/model-registration.md) 完成注册）。

## 关键参数

| 参数 | 说明 | 是否必填 | 示例 |
|------|------|----------|------|
| `publish_type` | 发布类型：`app`（Web 应用）、`component`（组件）、`api`（OpenAPI） | 是 | `"app"` |
| `visibility` | 可见性：`public`（公开）、`org`（组织内）、`private`（仅自己） | 是 | `"org"` |
| `ui_config` | UI 配置对象（仅 `app` 类型生效），含 `title`、`description`、`theme_color` 等字段 | 否 | `{"title": "客服助手", "theme_color": "#1677FF"}` |
| `component_input_schema` | 组件输入 Schema（JSON Schema 格式），用于定义调用方传参结构（仅 `component` 类型生效） | 是（当 `publish_type=component`） | `{"type": "object", "properties": {"query": {"type": "string"}}}` |

> **注意**：`component_input_schema` 的校验逻辑在 [发布为组件](../../raw/application-user-guide/application-publishing-and-sharing.md) 文档中未明确说明，但实际调用时若 schema 不匹配会导致 400 错误；建议严格遵循 JSON Schema Draft-07 规范。

## 使用方式

1. **控制台操作**：进入应用详情页 → 点击「发布」→ 选择类型 → 填写参数 → 提交审核（组织管理员审批后生效）；
2. **OpenAPI 调用**：使用 `POST /v1/applications/{app_id}/publish` 接口，请求体需符合上述关键参数结构，参考 [应用分享](../../raw/application-user-guide/application-publishing-and-sharing.md) 中的权限说明；
3. **组件嵌入**：发布为 component 后，在目标 Agent 的节点配置中选择「外部组件」，输入 component ID 即可自动拉取输入/输出定义。

## 限制和注意事项

- 单个应用最多同时发布为 **1 种类型**（即不能同一时间既是 `app` 又是 `api`），如需多形态，须先下线再重新发布；
- `public` 类型应用默认启用内容安全过滤（基于百炼内置审核模型），不可关闭；
- 自有模型若未开启「跨应用调用」权限（见 [模型接入与管理](../../raw/model-management/model-registration.md)），则无法在 `component` 或 `api` 场景中被引用；
- UI 设计能力（如拖拽布局、变量绑定）仅对 `app` 类型生效，且依赖 [UI设计](../../raw/application-user-guide/application-publishing-and-sharing.md) 模块启用状态，未开通组织将忽略 `ui_config` 字段。

## 来源文档

- [应用发布与分享](../../raw/application-user-guide/application-publishing-and-sharing.md)


