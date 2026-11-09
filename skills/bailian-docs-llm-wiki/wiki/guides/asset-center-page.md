# asset center page

资产中心是百炼平台中统一管理、查看和调用各类模型资产（如大模型、Embedding 模型、重排序模型等）的核心界面。开发者可通过该页面快速筛选、测试及集成已部署或预置的模型服务，所有操作均基于平台统一的 API 接口规范。该功能面向模型调用方，不涉及模型训练或部署流程。

## 支持的模型/功能

资产中心当前支持以下三类模型资产：
- **大语言模型（LLM）**：包括 Qwen 系列（如 qwen-max、qwen-plus）、Baichuan、GLM 等，支持流式响应与非流式响应；
- **Embedding 模型**：如 text-embedding-v1、bge-large-zh、m3e-base，输出固定维度向量；
- **重排序（Rerank）模型**：如 bge-reranker-v2-m3，用于对检索结果进行相关性重打分。

所有模型均通过标准 `/v1/chat/completions`、`/v1/embeddings` 或 `/v1/rerank` 接口暴露，具体能力以 [资产中心](../../raw/model-user-guide/asset-center-page.md) 文档为准。

## 关键参数

调用资产中心所列模型时，需在请求体中显式指定以下关键参数（部分为可选）：

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | string | 必填，模型唯一标识符（如 `qwen-max`），可在资产中心列表页直接复制； |
| `input`（rerank） / `input`（embeddings） / `messages`（chat） | object/array | 根据接口类型不同而异，详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 的接口定义章节； |
| `stream` | boolean | 仅 chat 接口支持，设为 `true` 启用 SSE 流式响应； |
| `top_k`（rerank） / `dimensions`（embeddings） | integer / integer | 指定返回数量或向量维度，若未提供则使用模型默认值。 |

> **注意**：`temperature` 和 `max_tokens` 在部分旧版文档中被列为 LLM 必填参数，但根据最新 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 实际行为，二者均为可选，默认值由模型服务侧设定，客户端不传亦可正常调用。

## 使用方式

1. 登录百炼控制台 → 进入「模型服务」→ 点击「资产中心」；
2. 使用顶部搜索框或筛选器（按类型、提供商、是否启用）定位目标模型；
3. 点击模型卡片右上角「调试」按钮，填写参数并发送请求，实时查看响应；
4. 复制生成的 cURL 或 SDK 示例代码，在本地项目中集成调用。

所有调试请求均走真实线上服务通道，等效于生产环境调用，因此需确保账号具备对应模型的调用权限（见权限管理文档）。

## 限制和注意事项

- 单次 Embedding 请求最多支持 1024 个 token（按模型 tokenizer 计算），超长文本将被截断，不报错；
- Rerank 接口单次最多处理 100 个候选文档（`documents` 数组长度 ≤ 100）；
- 资产中心展示的模型列表实时同步平台服务注册状态，但**不保证所有模型均对所有地域可用**——例如 `qwen-turbo` 在华东 2 区域不可见，需切换地域后刷新；
- 若发现模型状态显示“已启用”但调用返回 `404 Not Found`，请确认当前 API Endpoint 是否匹配所选地域（参见 [资产中心](../../raw/model-user-guide/asset-center-page.md) 中的 endpoint 映射表）。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page.md)


