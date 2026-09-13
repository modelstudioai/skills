# asset center page

资产中心是百炼平台中统一管理模型、数据集、Prompt 模板等 AI 资源的核心页面，为开发者提供可视化浏览、快速调用与权限协同能力。所有已发布至工作空间的资产均在此集中呈现，支持按类型、状态、标签等维度筛选。该页面不直接执行推理，而是作为资源发现与接入的入口枢纽。

## 支持的模型/功能

- 支持展示和调用以下资产类型：大语言模型（LLM）、嵌入模型（Embedding）、重排序模型（Rerank）、语音识别（ASR）与合成（TTS）模型、自定义训练模型（Fine-tuned Model），以及结构化数据集、[Prompt 工程](../concepts/prompt-engineering.md)模板和 Agent 配置包。  
- 提供“一键部署为 API”、“复制 SDK 调用代码”、“下载配置文件”等快捷操作，部分功能需对应资产已通过审核并处于 `Published` 状态。  
- 所有功能行为以 [资产中心](../../raw/model-user-guide/asset-center-page.md) 文档描述为准；若控制台实际按钮缺失，请确认当前工作空间角色是否具备 `AssetViewer` 或更高权限 —— 详见 [资产中心](../../raw/model-user-guide/asset-center-page.md) 中的权限说明。

## 关键参数

- `workspace_id`：必填，标识资产所属工作空间，影响可见范围与权限校验。  
- `asset_type`：可选值包括 `model`、`dataset`、`prompt_template`、`agent_config`，用于过滤资产列表。  
- `status`：默认为 `published`，支持传入 `draft`（仅对创建者可见）或 `archived`（需显式指定）。  
- `page` / `page_size`：分页参数，`page_size` 最大支持 50，超出将被服务端截断 —— 此限制在 [资产中心](../../raw/model-user-guide/asset-center-page.md) 的“API 接口规范”小节中有明确定义。

## 使用方式

1. 登录百炼控制台 → 进入目标工作空间 → 点击左侧导航栏 **Asset Center**；  
2. 使用顶部搜索框或筛选器定位资产；  
3. 点击资产卡片进入详情页，查看版本历史、元信息、调用示例及访问控制策略；  
4. 对于模型类资产，点击 **Deploy** 可跳转至部署向导；对于 Prompt 模板，点击 **Use in Playground** 可直接加载调试。  
> **注意**：新版资产中心（v2.3+）已移除“批量导出为 JSON Schema”功能，旧版文档中提及的该能力已失效，请勿依赖 [资产中心](../../raw/model-user-guide/asset-center-page.md) 中过时的“高级操作”章节。

## 限制和注意事项

- 单个工作空间内最多显示 10,000 条资产记录（含所有类型），超出部分需通过 `asset_type` + `tags` 组合过滤；  
- 数据集资产不支持跨工作空间共享，即使已授予 `Read` 权限，也无法在其他工作空间的资产中心列表中出现；  
- 所有资产的 `created_at` 时间戳精度为秒级，不支持毫秒级查询；  
- 若通过 OpenAPI 列表接口获取资产，响应中 `updated_at` 字段可能滞后于控制台操作 1–3 秒，属最终一致性设计，详见 [资产中心](../../raw/model-user-guide/asset-center-page.md) 的“同步延迟说明”。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page.md)


