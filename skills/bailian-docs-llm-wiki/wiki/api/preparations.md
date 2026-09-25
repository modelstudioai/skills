# preparations

`preparations` 是调用百炼模型 API 前必需完成的初始化步骤，涵盖身份认证、开发环境配置及基础依赖安装。这些操作直接影响后续请求的合法性与稳定性，开发者需严格按顺序执行。所有步骤均基于 [使用 API (raw/model-api-reference/preparations.md)](../../raw/model-api-reference/preparations.md) 文档定义。

## 支持的模型/功能

当前 `preparations` 流程适用于所有通过百炼 Model API 提供的模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio 等），但**不适用于控制台直接调试或 Web UI 交互场景**。SDK 初始化与 API Key 配置是通用前置条件，无论调用文本生成、多模态推理或流式响应均需完成。具体模型兼容性请参考 [使用 API (raw/model-api-reference/preparations.md)](../../raw/model-api-reference/preparations.md) 中的 SDK Expert 指南。

## 关键参数

- `api_key`：必填，用于服务端鉴权，需通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取并安全存储；
- `base_url`（可选）：仅当使用私有部署或代理网关时需显式指定，否则默认指向百炼生产环境；
- `timeout`（推荐设置）：建议设为 60s 以上，避免因模型长尾响应导致连接中断；  
- `max_retries`（推荐设置）：SDK 默认重试策略可能不满足高可用要求，建议在初始化客户端时显式配置（详见 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)）。

## 使用方式

1. **获取 API Key**：登录百炼控制台，在「API 密钥管理」中创建并复制密钥，严禁硬编码到源码中；
2. **安装 SDK**：运行 `pip install dashscope`（Python）或对应语言的官方包（见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）；
3. **初始化客户端**：  
   ```python
   import dashscope
   dashscope.api_key = "YOUR_API_KEY"
   ```
   或使用 `dashscope.Client(api_key=...)` 实例化（推荐，便于多租户隔离）。

> **注意**：部分旧版文档示例仍使用全局 `dashscope.api_key = ...` 赋值方式，但 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 明确指出该方式在并发场景下存在线程安全风险，应优先采用 Client 实例化方式。

## 限制和注意事项

- 单个 API Key 默认限速 10 QPS（每秒查询数），超出将返回 `429 Too Many Requests` 错误（详见 [错误码](../../raw/model-api-reference/preparations/error-code.md)）；
- API Key 仅对创建者所在工作空间生效，跨工作空间调用需单独申请密钥；
- 未配置 `User-Agent` 或使用非标准 HTTP Header 可能触发风控拦截；
- 本地调试时若遇到 `ConnectionResetError`，优先检查是否遗漏 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 步骤或版本过低（要求 dashscope >= 1.15.0）。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


