# preparations

`preparations` 是调用百炼模型 API 前必需完成的环境与凭证配置步骤，涵盖 API Key 获取、SDK 安装与初始化、以及基础错误处理机制。这些操作是所有模型调用（如 `qwen-max`、`qwen-plus` 等）的前置依赖，直接影响请求的鉴权、路由与稳定性。开发者需按顺序完成，否则将触发 401 或连接失败等基础错误。

## 支持的模型/功能

当前 `preparations` 流程适用于全部百炼托管模型（包括 `qwen-max`、`qwen-plus`、`qwen-turbo`、`qwen-vl`、`qwen-audio` 等）及配套能力（如流式响应、Function Calling、多模态输入）。该准备逻辑**不区分模型类型**，统一通过 API Key 和 SDK 版本控制兼容性。详见 [使用 API](../../raw/model-api-reference/preparations.md) 文档中对各模型通用接入路径的说明。

## 关键参数

- `api_key`：必填，用于身份认证，须通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 正确生成并安全存储；
- `base_url`（可选）：仅在私有化部署或调试场景下覆盖默认网关地址；
- `timeout`（推荐显式设置）：建议设为 `60` 秒以上，避免因大模型推理延迟导致 SDK 默认超时（30 秒）误判失败；
- `max_retries`（可选）：SDK 默认重试 2 次，生产环境建议设为 `0` 或 `1` 并自行实现幂等逻辑，避免重复计费。

## 使用方式

1. **获取 API Key**：登录百炼控制台 →「API 密钥管理」→ 创建新密钥 → 复制保存（**切勿硬编码到客户端代码中**）；  
2. **安装 SDK**：执行 `pip install dashscope`（Python）或对应语言的官方包（见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）；  
3. **初始化客户端**：  
   ```python
   import dashscope
   dashscope.api_key = "sk-..."  # 或通过环境变量 DASHSCOPE_API_KEY 设置
   ```  
   如需高级能力（如异步调用、自定义会话上下文），请参考 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 文档。

## 限制和注意事项

- 单个 API Key 默认配额为 100 QPS，超出将返回 `429 Too Many Requests` 错误（具体策略见 [错误码](../../raw/model-api-reference/preparations/error-code.md)）；  
- API Key 仅支持服务端使用，**严禁嵌入前端 HTML/JS 或移动 App 客户端**，否则存在密钥泄露与盗刷风险；  
- > **注意**：部分旧版文档（如早期 `dashscope==1.10.0` 的 README）仍建议使用 `dashscope.init()` 初始化，但自 `dashscope>=1.15.0` 起已废弃该方法，应统一使用 `dashscope.api_key = ...` 赋值（参见 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 中的版本兼容性说明）；  
- 免费额度每月自动重置，但 API Key 本身长期有效，无需定期轮换（除非发生泄露）。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


