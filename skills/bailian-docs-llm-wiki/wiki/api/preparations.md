# preparations

在调用百炼模型服务前，开发者需完成 API Key 获取与配置、SDK 安装、Base URL 选择等基础准备。这些步骤直接影响鉴权、路由、功能可用性及稳定性。本文汇总关键配置项、参数约束、使用方式及常见限制，帮助开发者快速建立可运行的调用环境。

## 支持的模型/功能

百炼支持通过 DashScope 原生 SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用多种模型类型，包括文本生成（如 `qwen-plus`、`qwen3.7-plus`）、多模态对话（如 `qwen3-vl-plus`）、图像/视频生成（`wanx2.1-t2i-turbo`、`wan3.0-video`）、语音识别与合成（`paraformer-v2`、`cosyvoice-v3-flash`）、向量嵌入（`qwen3.7-text-embedding`）及重排序（`bge-reranker-v2-m3`）等。具体模型清单请参见 [模型列表](raw/model-user-guide/get-started-with-models/models.md)。  
> **注意**：部分模型存在强约束——例如 `qwen3.7-plus` 要求 `enable_thinking` 必须为 `true`；思考模式模型（如 `qwen3.7-plus`）不支持结构化输出（`response_format="json_object"`），且必须启用[流式输出](../concepts/streaming-output.md)（`stream=true`）和增量输出（`incremental_output=true`）[原文标题](../../raw/model-api-reference/preparations/error-code.md)。此外，`qwen-image-3.0-pro` 等纯多模态模型不接受非数组型 `content`，而纯文本模型（如 `qwen-plus`）则要求 `content` 为字符串而非对象数组 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

## 关键参数

核心参数包括 `model`（必需，严格匹配模型市场名称，如 `qwen-plus`，不可混用开源 ID 如 `Qwen/Qwen3.7-Plus`）、`messages`（必需，格式为 `{"role": "user", "content": "..."}` 数组）、`stream`（布尔值，控制是否流式返回）、`max_tokens`（整数，范围 `[1, 模型最大输出 Token]`）、`temperature`（浮点数，范围 `[0.0, 2.0)`）、`top_p`（浮点数，范围 `(0.0, 1.0]`）等。  
`enable_thinking`、`incremental_output`、`result_format` 等高级参数存在强互斥关系：开启思考模式时，`result_format` 必须为 `"message"`，且 `incremental_output` 必须为 `true`；启用结构化输出时，`enable_thinking` 必须为 `false` [原文标题](../../raw/model-api-reference/preparations/error-code.md)。所有参数取值均需符合模型能力边界，超限将触发 `InvalidParameter` 错误。

## 使用方式

1. **获取并配置 API Key**：在百炼控制台按地域创建 API Key，其归属业务空间决定可调用模型范围；推荐配置为环境变量 `DASHSCOPE_API_KEY`，避免硬编码 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。  
2. **选择 Base URL**：按计费方案和部署需求选用——生产环境推荐业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`），测试可选试用域名，跨空间调用可沿用 DashScope 域名（如 `https://dashscope.aliyuncs.com/api/v1`）[原文标题](../../raw/model-api-reference/preparations/base-url.md)。  
3. **安装 SDK**：Python 项目需安装 `dashscope>=2.0.1`（新项目）或 `openai`（OpenAI 兼容）；Java/Node.js/Go 等语言亦有对应 SDK [原文标题](../../raw/model-api-reference/preparations/install-sdk.md)。  
4. **初始化客户端**：DashScope SDK 2.0 推荐通过 `Client(api_key=..., workspace=..., region=...)` 构造，优先级高于环境变量；1.x 版本已冻结维护，仅建议存量项目参考迁移指南 [原文标题](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)。  
5. **调用辅助工具**：`dashscope` CLI 内置 SDK Expert，支持自然语言生成校验代码、诊断报错（如 `Throttling.RateQuota`）、解释源码逻辑等，需联网且消耗 token [原文标题](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)。

## 限制和注意事项

- **地域隔离**：API Key 与 Base URL 必须同地域，跨地域调用将返回 `401 InvalidApiKey`；各地域接入域名、模型列表独立 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。  
- **配额与限流**：单账号+地域维度最多 50 个 API Key；自定义权限下最多勾选 30 个模型；IP 白名单最多 20 个地址；临时 API Key 最长 1800 秒 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。  
- **安全实践**：禁止在客户端（浏览器/移动 App）暴露长期 API Key；生产服务应使用 systemd 等服务管理器加载密钥文件，避免环境变量泄露；`sudo` 执行脚本需加 `-E` 参数传递环境变量 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。  
- **错误处理**：`401` 鉴权失败需检查 Key/地域/URL 匹配；`403` 访问拒绝需确认业务空间授权及模型开通状态；`429` 限流需降低并发或申请配额；所有错误均应记录 `Request ID` 用于排查 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)
- [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)
- [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)


