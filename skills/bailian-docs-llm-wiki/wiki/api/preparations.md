# preparations

在调用百炼平台模型 API 前，需完成身份认证、环境配置与依赖安装等基础准备。这些步骤是所有模型调用（如 `qwen-max`、`qwen-plus`、文本嵌入、[多模态](../concepts/multi-modal.md)等）的通用前提，直接影响请求的合法性与稳定性。请严格按顺序执行，避免因配置缺失导致 `401 Unauthorized` 或 `404 Not Found` 等错误。

## 支持的模型/功能

`preparations` 本身不对应具体模型，而是所有模型 API 调用的前置条件集合，适用于：
- 通义千问系列（`qwen-max`、`qwen-plus`、`qwen-turbo` 等）
- 文本嵌入模型（`text-embedding-v1`）
- [多模态](../concepts/multi-modal.md)模型（`qwen-vl-plus`、`qwen-audio`）
- 工具调用与函数增强（Function Calling）场景  
相关模型能力说明详见 [使用 API](../../raw/model-api-reference/preparations.md) 中的上下文链接。

## 关键参数

必须配置以下参数（环境变量或代码内显式传入）：
- `DASHSCOPE_API_KEY`：通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取，**不可硬编码到生产代码中**；
- `DASHSCOPE_BASE_URL`（可选）：默认为 `https://dashscope.aliyuncs.com/api/v1`；若使用私有部署或特定 Region，需参考 [Base URL总览](../../raw/model-api-reference/preparations/base-url.md) 设置；
- `DASHSCOPE_TIMEOUT`（推荐）：建议设为 `60` 秒以上，避免大模型响应延迟触发超时中断。

> **注意**：SDK 1.x 版本中 `api_key` 参数名曾为 `dashscope_api_key`，而 2.x+ 统一为 `api_key`；旧版文档 [SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md) 中的示例已过时，实际开发请以 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 为准。

## 使用方式

1. **安装 SDK**：运行 `pip install dashscope`（Python）或对应语言客户端（见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）；  
2. **初始化客户端**：设置 `DASHSCOPE_API_KEY` 后，直接调用 `dashscope.Generation.call(...)` 或 `dashscope.MultiModalConversation.call(...)`；  
3. **验证连通性**：建议首次使用前调用 `dashscope.models.List.list()`（需权限）或发送最小 payload 测试（如 `qwen-turbo` 的空 prompt）。

## 限制和注意事项

- 单个 API Key 默认 QPS 限制为 5，QPM 为 300，超出将返回 `429 Too Many Requests`（详见 [错误码](../../raw/model-api-reference/preparations/error-code.md)）；  
- 免费额度仅限新注册用户首月，后续需绑定支付宝完成实名认证并开通按量付费；  
- 所有请求必须携带 `Content-Type: application/json`，且 body 必须为合法 JSON（空对象 `{}` 不被接受）；  
- 非中国大陆地域用户需确认网络可达 `dashscope.aliyuncs.com`，部分企业防火墙可能拦截该域名。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


