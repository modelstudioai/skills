# preparations

在调用百炼平台模型服务前，开发者需完成 API Key 获取与配置、SDK 安装、Base URL 选择等基础准备。这些步骤直接影响鉴权、路由、功能可用性及稳定性，是所有模型调用的前提。本文汇总关键配置项、参数约束、使用方式及常见限制，面向生产环境实践整理。

## 支持的模型/功能

百炼支持通过 DashScope 原生协议或 OpenAI 兼容协议调用全系列模型，包括文本生成（如 `qwen-plus`、`qwen-max`）、多模态（如 `qwen3-vl-plus`）、图像/视频生成（如 `wanx2.1-t2i-turbo`、`wan3.0-video`）、语音识别与合成（如 `paraformer-v2`、`cosyvoice-v3-flash`）、[向量嵌入](../concepts/vector-embedding.md)（如 `qwen3.7-text-embedding`）及重排序等。部分模型具备专属能力约束，例如：
- 思考模式（`enable_thinking`）仅支持[流式输出](../concepts/streaming-output.md)，且要求 `incremental_output=true`；
- 联网搜索（`enable_search`）仅限明确标注支持该能力的模型；
- 某些模型（如 `qwen-image-3.0-pro`）要求 `messages.content` 为结构化数组，不可传纯字符串 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

SDK 层面，DashScope Python SDK 2.0+（≥2.0.1）为当前推荐版本，全面覆盖上述能力；OpenAI SDK（Python/Node.js/Java/Go）可用于调用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，但不支持百炼特有功能（如业务空间专属域名、临时 API Key 等）[安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

## 关键参数

调用时需关注以下核心参数及其取值范围，违反将触发 `InvalidParameter` 错误：

| 参数 | 合法范围 | 说明 |
|------|----------|------|
| `temperature` | `[0.0, 2.0)` | 必须为浮点数，超出范围将报错 [错误码](../../raw/model-api-reference/preparations/error-code.md) |
| `top_p` | `(0.0, 1.0]` | 必须为浮点数 |
| `top_k` | `≥ 0` | 整数 |
| `repetition_penalty` | `> 0.0` | 浮点数 |
| `presence_penalty` | `[-2.0, 2.0]` | 浮点数 |
| `n` | `[1, 4]` | 返回结果数量上限 |
| `max_tokens` | `[1, 模型最大输出 Token 数]` | 具体上限见各模型文档 |
| `seed` | `[0, 9223372036854775807]` | 仅 DashScope 协议支持 |
| `thinking_budget` | `(0, 模型最大思维链长度]` | 需查模型列表确认上限 |

> **注意**：文档 5 中 DashScope SDK 1.x 的 `Generation.call` 接口默认 `stream=False` 且 `incremental_output=False`，而 2.0 版本流式调用默认增量输出，行为已变更。新项目必须使用 2.0，存量项目迁移时需同步调整参数逻辑 [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)。

## 使用方式

### 1. API Key 获取与配置
- **获取**：在控制台对应地域（如[华北2（北京）](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)）创建 API Key，归属账号可选主账号或 RAM 用户，归属业务空间决定模型访问权限 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **配置**：推荐设为环境变量 `DASHSCOPE_API_KEY`，支持 Linux/macOS/Windows 多种方式（永久/临时/服务管理器）。**严禁在客户端代码中硬编码或暴露长期 API Key**，生产环境应使用临时 API Key（最长 1800 秒）。

### 2. Base URL 选择
Base URL 必须与 API Key 所属地域及计费方案严格匹配，否则返回 `401 InvalidApiKey`：
- **生产推荐**：业务空间专属域名（`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`），提供流量隔离与更高性能；
- **兼容过渡**：DashScope 域名（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`），仍可使用但建议迁移；
- **测试专用**：试用域名（如 `https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），限流严格，仅用于验证 [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)。

### 3. SDK 调用
- **Python**：安装 `dashscope>=2.0.1` 或 `openai`，构造 Client 时传入 `api_key` 和 `workspace`/`region`（DashScope）或 `base_url`（OpenAI）；
- **其他语言**：Java/Node.js/Go 均通过 OpenAI SDK 调用兼容接口，依赖配置见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)；
- **排障辅助**：启用 DashScope SDK Expert（`pip install -U "dashscope[acli]"`），支持自然语言提问生成可运行代码、诊断报错、修复源码 [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)。

## 限制和注意事项

- **地域隔离**：API Key、Base URL、模型列表均按地域独立，**不可跨地域混用**。华北2（北京）的 Key 无法调用新加坡地域模型。
- **API Key 生命周期**：无自动过期，但删除后不可恢复；RAM 用户创建的 Key 在 2026年3月25日前删除用户会级联删除，之后创建的 Key 不再级联 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **配额与限流**：触发 `Throttling.RateQuota` 或 `Throttling.AllocationQuota` 时需降低请求频率、并发或申请配额提升；免费额度耗尽将返回 `Arrearage`。
- **安全红线**：
  - 禁止在浏览器、移动 App 等客户端环境配置长期 API Key；
  - 禁止在 Git 仓库、日志、错误响应中泄露 API Key、`Request ID` 或敏感业务数据；
  - 使用 `sudo` 运行脚本时需加 `-E` 参数传递环境变量，否则 `DASHSCOPE_API_KEY` 不生效 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **模型能力约束**：非流式调用思考模式模型、对不支持联网搜索的模型设置 `enable_search=true`、`messages` 中 `content` 类型错误（如传数组给纯文本模型）等，均会导致明确的 `InvalidParameter` 错误，需按 [错误码](../../raw/model-api-reference/preparations/error-code.md) 文档修正。

## 来源文档

- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)
- [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)
- [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)


