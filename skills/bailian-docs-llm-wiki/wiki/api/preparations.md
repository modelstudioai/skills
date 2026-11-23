# preparations

在调用百炼平台模型服务前，开发者需完成 API Key 获取与配置、SDK 安装、Base URL 选择等基础准备。这些步骤直接影响鉴权、路由、性能与功能可用性，是所有模型调用的前提。本文汇总关键配置项、参数约束及常见陷阱，帮助开发者快速建立稳定可靠的调用环境。

## 支持的模型/功能

百炼支持通过 DashScope 原生 API 和 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用多种模型类型，包括文本生成（如 `qwen-plus`、`qwen3.7-plus`）、多模态（`qwen3-vl-plus`）、图像/视频生成（`wanx2.1-t2i-turbo`、`wan3.0-video`）、语音识别与合成（`paraformer-realtime-v2`、`cosyvoice-v3-flash`）、向量嵌入（`qwen3.7-text-embedding`）及重排序（`bge-reranker-v2-m3`）等。具体模型清单请参见 [模型列表](raw/model-user-guide/get-started-with-models/models.md)。  
> **注意**：部分模型有强制约束，例如 `qwen3.7-plus` 要求 `enable_thinking=true`，而结构化输出（`response_format={"type": "json_object"}`）仅在 `enable_thinking=false` 时可用；`qwen-image-3.0-pro` 等多模态模型要求 `messages.content` 为数组格式，纯文本模型则要求 `content` 为字符串——详见 [错误码](raw/model-api-reference/preparations/error-code.md) 中的 `InvalidParameter` 分类。

## 关键参数

核心参数包括 `model`（必须匹配[模型列表](raw/model-user-guide/get-started-with-models/models.md)中的标准 ID，如 `qwen-plus`，不可混用开源社区名称）、`messages`（结构需严格符合角色规范，`tool` 消息必须响应前置 `tool_calls`）、`stream`（流式开关，音频输出或思考模式模型强制要求 `true`）、`enable_thinking`（思考模式，开启时 `incremental_output` 和 `result_format="message"` 必须同时设置）、`max_tokens`（范围 `[1, 模型最大输出 Token]`）、`temperature`（`[0.0, 2.0)`）、`top_p`（`(0.0, 1.0]`）等。所有参数取值范围和格式约束均在 [错误码](raw/model-api-reference/preparations/error-code.md) 文档中有明确校验规则。

## 使用方式

1. **获取并配置 API Key**：前往控制台对应地域的 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 页面创建 Key，并按业务需求选择归属账号（主账号或 RAM 用户）和业务空间。Key 创建后仅显示一次，请立即保存。  
2. **选择 Base URL**：必须与 API Key 所属地域和计费方案严格匹配。生产环境推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），测试可选试用域名；DashScope 域名（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）仍可用但已不推荐。详情见 [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)。  
3. **安装 SDK**：推荐使用 DashScope Python SDK 2.0（`pip install -U "dashscope>=2.0.1"`）或 OpenAI 多语言 SDK（Python/Node.js/Java/Go）。旧版 SDK 1.x 已冻结维护，新项目请勿使用，存量项目迁移参考 [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)。  
4. **环境变量配置**：将 `DASHSCOPE_API_KEY` 和 `DASHSCOPE_HTTP_BASE_URL`（如使用专属域名）设为环境变量，避免硬编码。注意：客户端代码中禁止直接嵌入长期有效 Key，敏感场景应使用 [临时 API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。  
5. **调试与排障**：推荐使用内置的 [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)，它可基于自然语言需求生成可运行代码、诊断报错（如 `Throttling.RateQuota`）、读取源码定位根因，并提供修复建议与验证闭环。

## 限制和注意事项

- **地域隔离**：API Key、Base URL、模型列表均按地域独立，华北2（北京）、新加坡等地域的 Key 和域名不可混用，否则返回 `401 InvalidApiKey`。  
- **权限继承**：API Key 的模型调用权限完全由其**归属业务空间**决定，同一空间内所有 Key 权限一致；子业务空间下的 Key 仅能调用该空间已授权的模型。  
- **数量限制**：单个主账号+地域维度最多 50 个 API Key；自定义权限下最多勾选 30 个模型；IP 白名单最多 20 个地址。  
- **安全警告**：API Key 是长期凭证，切勿在浏览器、移动 App 或公开仓库中泄露；若需自动化管理，应调用 [ModelStudio OpenAPI](https://next.api.aliyun.com/api/ModelStudio/2026-02-10) 并严格管控 RAM 权限。  
- **版本兼容性**：DashScope SDK 2.0 与 1.x 接口差异显著（如 `Generation.call` → `client.chat.completions.create`），错误处理从自查 `status_code` 改为抛 `DashScopeError` 异常，流式默认增量输出——迁移时务必参考 [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)。  
> **注意**：文档 5 中“Token Plan”和“Coding Plan”的 Base URL 明确标注“仅限 Claude Code、Codex 等 AI 工具交互式使用，不能用于后端服务”，而文档 1 中未强调此限制，实际生产部署必须避开这两类域名，否则将触发调用失败。

## 来源文档

- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)
- [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)
- [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)


