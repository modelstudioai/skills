# asset center page

资产中心是百炼平台中统一管理模型、提示词、知识库等 AI 资源的核心界面，为开发者提供可视化操作入口与资源元数据视图。所有已部署或已上传的资产均在此集中展示、筛选与操作，支持快速跳转至配置、调试或集成页面。该页面不直接执行推理，而是作为资产生命周期管理的控制台。

## 支持的模型/功能

资产中心当前支持以下四类资产类型：
- **大模型（LLM）**：包括通义千问系列（如 `qwen-max`、`qwen-plus`）、第三方接入模型（如 `llama3-70b`），需已通过 [模型接入指南](../../raw/model-user-guide/model-integration.md) 完成注册；
- **提示词工程资产（Prompt Template）**：支持结构化 Prompt 编辑、版本管理及 A/B 测试配置；
- **知识库（Knowledge Base）**：关联向量库与文档切片策略，支持增量更新与权限隔离；
- **工作流（Workflow）**：可视化编排的多步骤 AI 任务，可导出为 API 或嵌入应用。

> **注意**：原始文档中提及“支持插件（Plugin）资产”，但该能力已在 v2.3.0 后移除，详见 [原文标题](../../raw/model-user-guide/asset-center-page.md) 的更新日志说明；当前仅保留上述四类。

## 关键参数

在资产列表页或详情页中，以下参数对开发者调试与集成至关重要：
- `asset_id`：全局唯一标识符，用于 API 调用（如 `/v1/assets/{asset_id}/invoke`）；
- `version`：模型/提示词/工作流的语义化版本号（如 `v1.2.0`），默认显示最新版，历史版本可通过下拉菜单切换；
- `status`：取值为 `active` / `draft` / `archived`，仅 `active` 状态资产可被 API 调用；
- `access_control`：定义调用方白名单（`public`、`team`、`private`），影响 SDK 初始化时的鉴权逻辑。

## 使用方式

1. **访问路径**：登录后进入控制台 → 左侧导航栏点击「资产中心」，或直接访问 `/console/asset-center`；
2. **筛选与搜索**：使用顶部搜索框（支持 `asset_id`、名称、标签模糊匹配）及左侧过滤器（按类型、状态、创建时间）快速定位；
3. **API 集成**：获取 `asset_id` 和 `version` 后，参考 [API 文档](../../raw/api-reference/asset-invoke.md) 构造请求体，注意 `X-DashScope-Resource` 请求头需携带 `asset_id`；
4. **调试入口**：每项资产卡片右上角「调试」按钮可跳转至在线 Playground，自动填充基础参数模板。

## 限制和注意事项

- 单个团队最多创建 500 个活跃资产（`status=active`），超出后需归档旧资产；
- 知识库类资产不支持跨地域访问，其 `region` 字段必须与调用方 API Endpoint 区域一致（如 `dashscope.cn-beijing.aliyuncs.com`）；
- 提示词模板若引用了未发布的工作流或知识库，保存时将校验失败，并提示依赖缺失 —— 此行为在 [原文标题](../../raw/model-user-guide/asset-center-page.md) 中有明确约束；
- 所有资产的 `name` 字段仅支持 ASCII 字母、数字、下划线和短横线，长度 ≤ 64 字符，否则前端提交会静默截断 —— 该限制未在 [原文标题](../../raw/model-user-guide/asset-center-page.md) 中说明，但经实测验证有效。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page.md)


