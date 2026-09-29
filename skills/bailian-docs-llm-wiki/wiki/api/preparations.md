# preparations

`preparations` 是调用百炼模型 API 前必需完成的环境与凭证配置步骤，涵盖 API Key 获取、SDK 安装与初始化等基础准备。这些操作是所有模型调用（如 `qwen-max`、`qwen-plus` 等）的前提条件，直接影响请求能否成功发起与鉴权。开发者需严格按顺序完成，否则将触发 [错误码](../../raw/model-api-reference/preparations/error-code.md) 中定义的 401 或 403 类错误。

## 支持的模型/功能

本阶段不直接关联具体模型，但所有支持通过 API 调用的模型（包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 及多模态模型 `qwen-vl-plus`）均依赖此准备流程。SDK 初始化后，可通过统一客户端实例调用任意已开通权限的模型——权限控制在 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 步骤中完成，而非 SDK 层。

## 关键参数

- `api_key`：必填，由 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 页面指导生成，需安全存储，禁止硬编码；
- `base_url`（可选）：用于私有化部署场景，覆盖默认百炼服务地址；
- `timeout`（可选）：SDK 默认超时为 60 秒，建议根据实际任务类型显式设置（如长文本生成需延长）；
- `max_retries`（可选）：默认重试 2 次，适用于网络抖动场景，但不缓解配额耗尽类错误。

## 使用方式

1. **获取 API Key**：登录百炼控制台，在「API 密钥管理」中创建并复制密钥；  
2. **安装 SDK**：执行 `pip install dashscope`（Python）或对应语言 SDK，详见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)；  
3. **初始化客户端**：  
   ```python
   import dashscope
   dashscope.api_key = "YOUR_API_KEY"  # 或通过环境变量 DASHSCOPE_API_KEY
   ```  
   > **注意**：[SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 文档中提及的 `DashScopeClient` 类在 v1.18.0+ 已废弃，当前推荐直接配置 `dashscope.api_key` 全局变量或使用 `dashscope.base_http_api` 显式传参，避免兼容性问题。

## 限制和注意事项

- 单个 API Key 默认限流 5 QPS（每秒查询数），超出将返回 `429 Too Many Requests` 错误，详情见 [错误码](../../raw/model-api-reference/preparations/error-code.md)；  
- API Key 仅对创建者所在工作空间生效，跨工作空间调用需单独申请；  
- SDK 初始化后未设置 `api_key` 时，首次调用会静默失败（非抛异常），建议在初始化后立即验证 `dashscope.api_key is not None`；  
- 本地开发建议使用 `.env` 文件管理密钥，并通过 `python-dotenv` 加载，避免泄露风险。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


