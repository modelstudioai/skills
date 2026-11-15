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
- `DASHSCOPE_API_KEY`：通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取，**不可硬编码**；
- `DASHSCOPE_BASE_URL`（可选）：默认为 `https://dashscope.aliyuncs.com/api/v1`；若使用私有部署或特定 Region，需覆盖此值，参考 [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)；
- `DASHSCOPE_TIMEOUT`（推荐）：建议设为 `60` 秒以上，避免大模型响应超时中断。

> **注意**：SDK 1.x 版本中曾支持 `api_key` 作为构造函数参数直接传入，但该方式在 SDK 2.x+ 中已被弃用，仅保留环境变量方式。请勿参考 [SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md) 中的初始化示例，应以 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 为准。

## 使用方式

1. **获取并安全存储 API Key**：从 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 页面完成创建与权限配置；
2. **安装 SDK**：运行 `pip install dashscope`（Python）或对应语言 SDK，详见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)；
3. **设置环境变量**（推荐）：
   ```bash
   export DASHSCOPE_API_KEY=sk-xxxxxx
   export DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/api/v1
   ```
4. **发起首次调用**：验证连通性，例如调用 `/models/list` 或简单 `chat` 接口。

## 限制和注意事项

- 单个 API Key 默认 QPS 限制为 5，可通过控制台申请提升；
- 免费额度仅限新用户首月，过期后需绑定支付方式；
- 错误响应统一遵循标准结构，常见问题请查阅 [错误码](../../raw/model-api-reference/preparations/error-code.md)；
- 所有请求必须携带 `Content-Type: application/json`，且 Body 必须为合法 JSON（空对象 `{}` 亦可接受）；
- 不支持跨域直接浏览器调用（CORS），前端需通过后端代理转发。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


