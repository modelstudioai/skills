# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖身份认证、开发环境搭建及客户端初始化。这些操作直接影响后续请求的合法性与稳定性，开发者需严格按顺序执行。所有步骤均以 [使用 API](../../raw/model-api-reference/preparations.md) 为统一入口文档。

## 支持的模型/功能

当前 `preparations` 流程适用于所有通过百炼 API 提供的模型服务，包括但不限于 Qwen 系列大语言模型、多模态模型（如 Qwen-VL）及 Embedding 模型。SDK 初始化后，可通过统一客户端调用 `call`、`stream`、`async_call` 等方法，具体能力取决于所选模型是否支持对应接口——详见 [使用 API](../../raw/model-api-reference/preparations.md) 中的 SDK 功能矩阵说明。

## 关键参数

- `api_key`：必填，用于身份鉴权，须通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取并安全存储；
- `model`：请求时指定，非初始化参数，但 SDK 实例需兼容目标模型的输入格式（如 `qwen-max`、`qwen2-72b-instruct`）；
- `base_url`（可选）：用于私有化部署场景，覆盖默认 API 地址，需与 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 文档中描述的自定义 endpoint 机制一致。

> **注意**：部分旧版 SDK 示例代码中将 `api_key` 作为 `call()` 方法参数传入，该方式已废弃；当前强制要求在初始化客户端时传入，否则触发 `AuthenticationError` ——请以 [错误码](../../raw/model-api-reference/preparations/error-code.md) 中 `AuthKeyMissing` 条目为准。

## 使用方式

1. 访问 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 页面，登录百炼控制台，在「API 密钥管理」中创建并复制密钥；
2. 根据语言选择安装对应 SDK：Python 用户执行 `pip install dashscope`，TypeScript 用户执行 `npm install @dashscope/llm`；
3. 初始化客户端（以 Python 为例）：
   ```python
   import dashscope
   dashscope.api_key = "sk-..."  # 或传入 dashscope.Client(api_key=...)
   ```
   更多初始化模式（如多 key 轮询、超时配置）见 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)。

## 限制和注意事项

- 单个 API Key 默认限流 5 QPS，超出将返回 `429 Too Many Requests`，需参考 [错误码](../../raw/model-api-reference/preparations/error-code.md) 处理重试逻辑；
- API Key 不可跨地域使用（如杭州 region 的 key 无法调用上海 region 的模型 endpoint），region 配置需与 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 中生成时选择的区域严格一致；
- 环境变量 `DASHSCOPE_API_KEY` 优先级高于代码中显式赋值，调试时需注意冲突风险。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


