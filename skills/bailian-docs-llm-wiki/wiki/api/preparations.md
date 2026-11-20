# preparations

在调用百炼平台模型 API 前，需完成身份认证、环境配置与依赖安装等基础准备。这些步骤是所有模型调用（如 `qwen-max`、`qwen-plus`、文本嵌入、多模态等）的通用前提，直接影响请求的合法性与稳定性。请严格按顺序执行，避免因配置缺失导致 `401 Unauthorized` 或 `404 Not Found` 等错误。

## 支持的模型/功能

`preparations` 本身不对应具体模型，而是所有模型 API 调用的前置条件集合，适用于：
- 通义千问系列（`qwen-max`、`qwen-plus`、`qwen-turbo` 等）
- 文本嵌入模型（`text-embedding-v1`）
- 多模态模型（`qwen-vl-plus`、`qwen-audio`）
- 工具调用与函数增强（Function Calling）场景  
相关模型能力说明详见 [使用 API](../../raw/model-api-reference/preparations.md) 中的上下文链接。

## 关键参数

必须配置以下参数（环境变量或代码内显式传入）：
- `DASHSCOPE_API_KEY`：通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取，**不可硬编码到生产代码中**；
- `DASHSCOPE_BASE_URL`（可选）：默认为 `https://dashscope.aliyuncs.com/api/v1`；若使用私有部署或特定 Region，需参考 [Base URL总览](../../raw/model-api-reference/preparations/base-url.md) 设置；
- `DASHSCOPE_TIMEOUT`（推荐）：建议设为 `60` 秒以上，避免大模型响应超时中断。

> **注意**：SDK 1.x 版本中 `api_key` 参数名曾为 `dashscope_api_key`，而 2.x+ 统一为 `api_key`；旧版参数名已废弃，请以 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 文档为准，避免兼容性问题。

## 使用方式

1. **安装 SDK**：运行 `pip install dashscope`（Python）或对应语言客户端，详见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)；
2. **初始化客户端**：使用 `dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")` 或构造时传入 `api_key`；
3. **发起请求**：调用 `Generation.call()`、`MultiModalConversation.call()` 等方法，无需额外初始化 preparation 模块。

## 限制和注意事项

- 单个 API Key 默认 QPS 限制为 5，可通过控制台申请提升；
- 免费额度仅限新用户首月，过期后需绑定支付方式，否则请求将被拒绝；
- 错误响应需结合 [错误码](../../raw/model-api-reference/preparations/error-code.md) 文档解析，常见 `InvalidAPIKey`、`ResourceNotFound` 均指向 preparation 阶段配置失败；
- 不支持跨 Region 复用 Base URL：例如杭州 Region 的 Key 不可搭配北京 Base URL 使用，否则返回 `403 Forbidden`。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


