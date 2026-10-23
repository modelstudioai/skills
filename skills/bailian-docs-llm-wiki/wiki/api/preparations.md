# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖认证凭证获取、开发环境搭建及 SDK 初始化等环节。这些操作直接影响后续请求的合法性与稳定性，开发者需严格按顺序执行。所有步骤均以最小可行配置为目标，避免冗余依赖。

## 支持的模型/功能

当前 `preparations` 流程适用于所有通过百炼 API 提供的模型服务（包括 Qwen 系列、Qwen-VL、Qwen-Audio 等），但**不适用于控制台直接调试或 Web UI 交互场景**。SDK 初始化后，可统一调用 `/v1/services/aigc/text-generation`、`/v1/services/aigc/multimodal-generation` 等标准接口。具体模型兼容性请参考 [使用 API](../../raw/model-api-reference/preparations.md) 中的接口路由映射表。

## 关键参数

- `api_key`：必填，需通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取，不可硬编码在客户端；
- `base_url`（可选）：默认为 `https://dashscope.aliyuncs.com/api/v1`，自建代理或私有部署时需显式指定；
- `max_retries`（SDK 默认 3）：建议生产环境设为 ≥2，避免因临时网络抖动导致请求失败；
- `timeout`（SDK 默认 60s）：对长上下文生成类任务（如文档摘要），应根据预期响应时间上调。

> **注意**：部分旧版文档中将 `api_key` 描述为“可选”，该说法已过时；实际所有 API 调用均强制校验 `api_key`，详见 [使用 API](../../raw/model-api-reference/preparations.md) 的认证章节。

## 使用方式

1. 访问 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 页面，创建并复制有效密钥；
2. 根据语言选择对应 SDK（Python/Java/Node.js），按 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 指南完成安装；
3. 初始化客户端时传入 `api_key` 和必要参数，例如 Python SDK：
   ```python
   from dashscope import Generation
   client = Generation(api_key="sk-xxx", base_url="https://dashscope.aliyuncs.com/api/v1")
   ```

## 限制和注意事项

- 单个 `api_key` 默认限流 10 QPS（每秒查询数），超出将返回 `429 Too Many Requests` 错误，详情见 [错误码](../../raw/model-api-reference/preparations/error-code.md)；
- API Key 仅支持 HTTPS 请求，HTTP 请求会被拒绝且不返回具体错误原因；
- 不支持跨区域复用 `api_key`：华东1（杭州）申请的密钥无法用于华北2（北京）Endpoint；
- SDK 初始化失败时，优先检查 `api_key` 格式（是否含空格、换行）及网络连通性，而非重装 SDK —— 多数问题源于 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 步骤中的密钥复制错误。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


