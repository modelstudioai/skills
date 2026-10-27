# asset center page

资产中心是百炼平台中统一管理模型、提示词、知识库等 AI 资源的核心控制台，支持开发者快速发现、复用和编排已有资产。所有资产均按类型分类组织，具备权限隔离、版本管理和 API 直接调用能力。该页面不提供训练功能，仅面向推理与集成场景。

## 支持的模型/功能

- **模型类资产**：支持 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）、Qwen-VL、Qwen-Audio 及第三方接入模型（如 Llama-3-8B-Instruct），需已通过模型市场审核并发布至组织可见范围  
- **非模型类资产**：包括 Prompt 模板（支持变量注入与多轮上下文配置）、RAG 知识库（支持 PDF/DOCX/TXT/MD 格式，自动切片与向量化）、工作流（Workflow）及自定义函数（Function Calling）  
- 所有资产均可通过 `POST /v1/assets/{asset_id}/invoke` 接口直接调用，详见 [资产中心](../../raw/model-user-guide/asset-center-page.md) 的接口规范章节  

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `asset_id` | string | 是 | 资产唯一标识符，可在资产详情页 URL 或列表页“复制 ID”按钮获取 |
| `input` | object | 否（模型/Prompt 类必需） | 输入数据结构，格式依资产类型而异；Prompt 类资产需匹配定义的 `variables` 字段 |
| `parameters` | object | 否 | 推理参数，如 `temperature`、`max_tokens`，仅对模型类资产生效；RAG 类资产支持 `top_k`、`score_threshold` |
| `trace_id` | string | 否 | 用于链路追踪的可选字段，建议在生产环境传入 |

> **注意**：`parameters` 中的 `stop` 字段在 Qwen2.5 模型中已弃用，应改用 `stop_sequences`；该变更未在 [资产中心](../../raw/model-user-guide/asset-center-page.md) 的参数表格中同步更新，请以 [Qwen2.5 模型文档](../../raw/model-user-guide/qwen2.5.md) 为准。

## 使用方式

1. **Web 控制台操作**：登录后进入「资产中心」→ 选择资产类型标签页 → 点击目标资产 → 「在线调试」或「复制调用代码」生成 SDK 示例  
2. **API 调用**：使用平台 AccessKey + SecretKey 签名，构造 `Authorization: Bearer <token>` 请求头，参考 [资产中心](../../raw/model-user-guide/asset-center-page.md) 的完整请求示例  
3. **SDK 集成**：Python SDK 中调用 `client.invoke_asset(asset_id, input=..., parameters=...)`，Java SDK 对应 `AssetClient.invoke()` 方法  

## 限制和注意事项

- 单次调用 `input` 总长度上限为 128KB（含 JSON 序列化开销），超限返回 `413 Payload Too Large`  
- RAG 知识库资产不支持跨组织共享，即使资产状态为“公开”，也仅对创建者所在组织及其子组织可见  
- Prompt 类资产若引用了已删除的知识库 ID，调用时将返回 `404 Not Found`，而非静默降级；该行为与 [工作流调试机制](../../raw/model-user-guide/workflow-debug.md) 中描述的容错逻辑存在不一致，建议在部署前校验全部依赖项

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page.md)


