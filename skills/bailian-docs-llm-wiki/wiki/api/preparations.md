# preparations

`preparations` 是调用百炼模型 API 前必需完成的初始化步骤，涵盖身份认证、开发环境配置及基础依赖安装。这些操作直接影响后续请求的合法性与稳定性，开发者需严格按顺序执行。所有步骤均基于 [使用 API (raw/model-api-reference/preparations.md)](../../raw/model-api-reference/preparations.md) 文档定义。

## 支持的模型/功能

当前 `preparations` 流程适用于所有通过百炼 Model API 提供的模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio 等），但**不适用于控制台直接调试或 Web UI 交互场景**。SDK 初始化与 API Key 配置是通用前置条件，无论调用文本生成、多模态推理或流式响应均需完成。详见 [使用 API (raw/model-api-reference/preparations.md)](../../raw/model-api-reference/preparations.md) 中的模块划分。

## 关键参数

- `api_key`：必填，用于身份鉴权，须通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取并安全存储；
- `base_url`（可选）：仅在私有化部署或调试时覆盖默认 endpoint，生产环境通常无需设置；
- `timeout`（推荐显式设置）：建议设为 60s 以上，避免因模型响应延迟导致客户端超时中断；
- `max_retries`（SDK v3.20.0+）：默认为 2，可在初始化 Client 时调整，该行为在 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 中有详细说明。

> **注意**：部分旧版文档示例中将 `api_key` 写入环境变量 `DASHSCOPE_API_KEY` 后未做空值校验，而最新 SDK（v3.25.0+）已强制要求非空校验——若环境变量未设置且未传参，将直接抛出 `ValueError`，而非静默降级。请以 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 的运行时行为为准。

## 使用方式

1. **获取 API Key**：登录百炼控制台，在「API 密钥管理」中创建并复制密钥；  
2. **安装 SDK**：执行 `pip install dashscope>=3.25.0`（推荐指定版本，避免兼容问题）；  
3. **初始化 Client**：  
   ```python
   import dashscope
   dashscope.api_key = "sk-xxx"  # 或通过环境变量注入
   ```
   更健壮的方式见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 中的 `Client` 构造示例。

## 限制和注意事项

- 单个 API Key 默认限流 10 QPS（具体配额以控制台显示为准），超出将返回 `429 Too Many Requests` 错误，对应错误码说明见 [错误码](../../raw/model-api-reference/preparations/error-code.md)；
- API Key 不可跨区域复用（如杭州 region 的 key 无法调用上海 region 的专属模型 endpoint）；
- 严禁在前端代码（如浏览器 JS、移动端 APK）中硬编码 `api_key`，否则存在密钥泄露风险；
- 若使用代理或内网环境，需确保 `dashscope` SDK 能访问 `https://dashscope.aliyuncs.com` 及其健康检查域名，防火墙策略须同步放开。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


