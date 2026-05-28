# preparations

接入阿里云百炼大模型服务前，开发者需完成鉴权凭证配置、依赖环境初始化及基础链路调试。本文档系统梳理了模型接入的标准化前置步骤，涵盖密钥管理、多语言 SDK 依赖、核心参数约束及调用规范，帮助您快速构建安全、可维护的模型调用链路。

## 支持的模型与功能
平台全面兼容 [[openai-compatible-api]]，同时提供官方 [[dashscope-sdk]] 以降低多语言接入成本。当前支持的功能矩阵包括：
- **文本生成与理解**：支持标准指令对话、长文本解析、机器翻译。
- **多模态处理**：涵盖视觉理解、视频生成、语音合成（TTS）与实时/离线语音识别。
- **工程化能力**：内置 [[embedding]] 向量化、[[reranking]] 排序、[[structured-output]] 结构化输出及 [[function-calling]] 工具调用。

详细依赖安装指南及版本要求请参见：[安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
| 语言 | 环境要求 | 推荐包 |
|------|----------|--------|
| Python | `>= 3.8` | `openai` 或 `dashscope` |
| Java | `Java 8+` | `com.alibaba:dashscope-sdk-java` 或 `com.openai:openai-java` |
| Node.js | 无特殊要求 | `openai` |
| Go | `Go 1.22+` | `github.com/openai/openai-go/v3` |

## 关键参数规范
基于接口调用高频校验规则，核心入参需严格遵守以下约束（详见完整排错指南：[错误码](../../raw/model-api-reference/preparations/error-code.md)）：
- **流式与思考模式**：启用 `[[thinking-mode]]` (`enable_thinking=true`) 时，必须同步开启 `[[streaming-output]]` (`stream=true`)，并设置 `incremental_output=true`。非流式调用思考模型将触发 400 错误。
- **生成控制**：
  - `temperature`：范围 `[0.0, 2.0)`
  - `top_p`：范围 `(0.0, 1.0]`
  - `top_k` / `repetition_penalty`：需 `≥ 0`
  - `presence_penalty`：范围 `[-2.0, 2.0]`
- **结构化输出与工具调用**：使用 `response_format: {"type": "json_object"}` 时，Prompt 中必须显式包含 `json` 关键词，且需关闭思考模式。`tool_choice` 仅支持 `"auto"` 或 `"none"`。
- **上下文与长度**：单次请求 `messages` 总 Token 不得超过模型上下文窗口；连续对话客户端易累积历史导致超限，需主动管理上下文或重置会话。

## 使用方式
模型调用主要依赖 API 密钥鉴权与环境变量注入，具体流程如下：
1. **获取与配置凭证**：通过控制台创建 API Key，并强烈建议通过 [[environment-variables]] 注入，严禁硬编码。详细步骤参考：[获取API Key](../../raw/model-api-reference/preparations/get-api-key.md) 与 [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)
2. **Base URL 路由**（按地域切换）：
   - 华北2（北京）：`https://dashscope.aliyuncs.com/compatible-mode/v1`
   - 新加坡：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
   - 美国（弗吉尼亚）：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
   - 德国（法兰克福）：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`（需替换实际业务空间 ID）
3. **调用路径选择**：
   - **代码集成**：推荐通过环境变量读取 `DASHSCOPE_API_KEY`，初始化 SDK Client 后发起请求。
   - **第三方工具**：在 Chatbox、Dify、Cline 等客户端中填入 API Key、对应地域 Base URL 及模型名称（如 `qwen-plus`）即可直连。

## 限制和注意事项
- **配额与可见性**：北京/新加坡/法兰克福地域单账号上限 50 个 Key；弗吉尼亚地域上限 20 个。主账号可查看所有 Key，子账号仅可见自身创建记录。删除 RAM 用户将同步失效其名下所有 Key。
- **权限隔离**：Key 权限完全由归属 [[workspace]] 决定。子空间 Key 仅可调用已授权模型及本空间应用；调优后模型仅允许原空间 Key 调用。
- **安全策略**：平台不设置 Key 自动过期时间。针对临时授权场景，应使用有效期 60 秒的临时 API Key 替代长期密钥。

> **注意**：
> 1. **IP 白名单限制**：目前仅华北2（北京）地域支持在创建 Key 时配置自定义 IP 访问白名单，其他地域默认全量放行。如需跨地域网络隔离，请结合 API 网关或安全组策略实现。
> 2. **Coding Plan 专属密钥**：若使用 Coding Plan 套餐，请勿使用通用 Key（`sk-xxxxx`），必须获取专属 Key（`sk-sp-xxxxx`）并配套专用 Base URL，否则鉴权将失败。
> 3. **临时 Key 不可复用**：临时 API Key 仅支持单次或极短时间内调用，不可缓存或用于生产环境常驻服务；关闭弹窗后无法再次查看完整明文 Key，丢失后需立即重置或新建。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)

