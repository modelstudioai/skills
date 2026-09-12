# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的环境与凭证配置步骤，涵盖 API Key 获取、SDK/CLI 工具安装及基础认证设置。这些操作是所有模型调用（包括 `preparations` 相关接口）的前提条件，未完成将导致 401 或连接失败。开发者应优先参考 [使用 API](../../raw/model-api-reference/preparations.md) 文档执行标准化初始化。

## 支持的模型/功能

`preparations` 本身不是模型，而是通用前置准备流程，适用于所有通过百炼 API 调用的模型（如 Qwen 系列、Qwen-VL、Qwen-Audio 等）。其核心功能包括：API 认证初始化、客户端实例构建、请求上下文配置（如 `base_url`、`timeout`）。具体支持的模型列表请查阅 [使用 API](../../raw/model-api-reference/preparations.md) 中的 SDK 初始化示例所覆盖的模型范围。

## 关键参数

- `api_key`: 必填，用于身份认证，需通过 [获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 获取；
- `model`: 非 `preparations` 接口自身参数，但在后续调用中必须指定，SDK 初始化时通常不强制要求，但首次 `call()` 时必须传入；
- `base_url`: 可选，用于私有化部署或调试，若未设置则默认指向百炼公有云服务端点；
- `max_retries`: 可选，SDK 默认重试策略，建议生产环境显式设置为 `2`～`3`；  
> **注意**：部分旧版文档将 `api_key` 描述为“可选（当使用 CLI 时）”，但实际 CLI 所有命令均依赖 `DASHSCOPE_API_KEY` 环境变量或 `--api-key` 参数，因此 `api_key` 在所有使用场景下均为必需 —— 详见 [使用 API](../../raw/model-api-reference/preparations.md) 中的 CLI 和 SDK 示例。

## 使用方式

1. **获取 API Key**：访问 [获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，在百炼控制台创建并复制密钥；  
2. **安装 SDK**：运行 `pip install dashscope`（Python）或对应语言 SDK，参考 [安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)；  
3. **初始化客户端**：  
   ```python
   import dashscope
   dashscope.api_key = "YOUR_API_KEY"
   # 或使用环境变量：export DASHSCOPE_API_KEY=xxx
   ```  
   其他语言 SDK 初始化方式见 [SDK Expert](https://help.aliyun.com/zh/model-studio/dashscope-sdk-expert)；  
4. **验证连通性**：可调用任意轻量接口（如 `dashscope.models.list()`）确认配置生效。完整流程说明请参阅 [使用 API](../../raw/model-api-reference/preparations.md)。

## 限制和注意事项

- 单个 API Key 默认调用频率限制为 60 QPM（每分钟请求数），超出将返回 `429 Too Many Requests` 错误，详情见 [错误码](https://help.aliyun.com/zh/model-studio/error-code)；  
- API Key 不可跨阿里云账号共享，且不支持子账号直接继承主账号权限（需主账号授权 RAM 策略）；  
- CLI 工具需单独安装（`pip install dashscope-cli`），其配置逻辑与 SDK 独立，但共用同一 `DASHSCOPE_API_KEY` 环境变量 —— 具体命令用法见 [使用百炼CLI](https://help.aliyun.com/zh/model-studio/use-model-studio-cli)；  
> **注意**：原始文档中 [错误码](https://help.aliyun.com/zh/model-studio/error-code) 页面未明确列出 `401 Unauthorized` 的常见原因（如 `api_key` 格式错误、过期、权限不足），开发者应结合 [使用 API](../../raw/model-api-reference/preparations.md) 中的认证排查章节交叉验证。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


