# preparations

在调用百炼模型服务前，开发者需完成 API Key 获取与配置、SDK 安装、Base URL 选择等基础准备。这些步骤直接影响鉴权、路由、功能可用性及稳定性，是所有模型调用的前提。本文汇总关键配置项、参数约束、使用方式及常见限制，帮助开发者快速建立可运行的调用环境。

## 支持的模型/功能

百炼支持文本生成、多模态对话、图像/视频生成、语音识别与合成、向量嵌入、重排序、智能体应用等多种能力。具体模型列表请参见 [模型列表](raw/model-user-guide/get-started-with-models/models.md)。  
- **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**：支持 Python、Node.js、Java、Go 等多语言 SDK 调用，适用于 `qwen-plus`、`qwen-max`、`deepseek-v4-pro` 等主流模型（详见 [安装SDK](raw/model-api-reference/preparations/install-sdk.md)）。  
- **DashScope 原生接口**：推荐用于生产环境，提供更细粒度控制和更高性能，支持全部模型类型（如 `qwen3-vl-plus` 多模态、`wan3.0-video` 视频生成等）。  
- **实时语音与多模态模型**：需通过 AOQ SDK 调用，不适用标准 DashScope 或 OpenAI SDK（参见 [AOQ SDK 下载](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/realtime-sdk-download.md)）。  
> **注意**：部分模型（如 `qwen3.7-plus`）强制要求 `enable_thinking=true`，而结构化输出（`response_format={"type": "json_object"}`）仅在 `enable_thinking=false` 时可用，二者不可共存 —— 具体兼容性请以 [支持的模型](https://help.aliyun.com/zh/model-studio/qwen-structured-output#7a8e438e89xeq) 文档为准，而非错误码文档中笼统描述。

## 关键参数

| 参数 | 说明 | 取值范围/格式 | 来源依据 |
|------|------|----------------|----------|
| `DASHSCOPE_API_KEY` | 鉴权凭证，必须与 Base URL 所属地域匹配 | `sk-` 开头字符串，创建后仅显示一次 | [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) |
| `base_url` | API 入口地址，决定请求路由与计费归属 | DashScope 域名（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）或业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`） | [Base URL总览](../../raw/model-api-reference/preparations/base-url.md) |
| `stream` | 是否启用[流式输出](../concepts/streaming-output.md) | `true` / `false`；部分模型（如思考模式模型、音频输出）强制要求 `true` | [错误码](../../raw/model-api-reference/preparations/error-code.md) 中 `InvalidParameter` 类错误说明 |
| `incremental_output` | 流式内容是否增量返回 | `true`（推荐）；2.0 SDK 默认增量，1.x 需显式设置 | [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md) |
| `temperature`, `top_p`, `max_tokens` | 生成控制参数 | `temperature ∈ [0.0, 2.0)`；`top_p ∈ (0.0, 1.0]`；`max_tokens ∈ [1, 模型最大输出 Token]` | [错误码](../../raw/model-api-reference/preparations/error-code.md) 中 `InvalidParameter` 错误详情 |

## 使用方式

1. **获取并配置 API Key**：在控制台按地域创建 API Key，**务必确保 Key 所属地域与 Base URL 地域一致**；推荐配置为环境变量 `DASHSCOPE_API_KEY`（Linux/macOS/Windows 各系统配置方法详见 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）。  
2. **选择并设置 Base URL**：生产环境优先使用业务空间专属域名（低延迟、流量隔离），测试可选试用域名；OpenAI 兼容调用需使用 `/compatible-mode/v1` 路径，原生调用使用 `/api/v1`。  
3. **安装 SDK**：  
   - Python：`pip install -U "dashscope>=2.0.1"`（推荐）或 `pip install -U openai`（OpenAI 兼容）；  
   - Java/Node.js/Go：按 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 文档添加对应依赖。  
4. **初始化客户端**：  
   - DashScope SDK 2.0：`client = dashscope.Client(api_key=..., region="cn-beijing", workspace="...")`；  
   - OpenAI SDK：设置 `OPENAI_BASE_URL` 和 `OPENAI_API_KEY` 环境变量后直接使用 `openai.OpenAI()`。  
5. **调用验证**：使用 `qwen-plus` 等通用模型发起最简请求，确认 `200 OK` 响应及 `content` 字段返回。

## 限制和注意事项

- **地域隔离**：API Key 与 Base URL 必须同地域，跨地域使用将触发 `401 InvalidApiKey` 错误（[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 明确强调）。  
- **Key 生命周期**：API Key 无自动过期时间，但删除后关联的[异步任务](../concepts/asynchronous-task.md)仍会执行（需手动终止）；RAM 用户创建的 Key 在 2026年3月25日前删除 RAM 用户会导致 Key 级联删除，之后创建的 Key 不再级联（[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 的“时效性与限制”章节）。  
- **SDK 版本兼容性**：新项目必须使用 DashScope SDK 2.0+（1.x 已冻结维护）；存量项目迁移需注意接口名、错误处理（2.0 默认抛异常）、流式行为（2.0 默认增量）等差异（[DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md) 提供完整对照）。  
- **安全实践**：禁止在客户端（浏览器/移动 App）硬编码长期 API Key；高敏感场景应使用 [临时 API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)（最长 1800 秒）。  
- **错误排查**：常见 `401`/`403`/`429` 错误请优先查阅 [错误码](../../raw/model-api-reference/preparations/error-code.md) 文档；复杂问题可借助 [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 进行代码诊断与修复。

## 来源文档

- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)
- [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)
- [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)


