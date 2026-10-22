# preparations

`preparations` 是调用百炼模型 API 前必需完成的环境与凭证配置步骤，涵盖 API Key 获取、SDK 安装与初始化、以及基础错误处理机制。这些操作是所有模型请求（如 `qwen-max`、`qwen-plus` 等）的前置依赖，直接影响调用成功率与调试效率。完整流程请参考 [使用 API](../../raw/model-api-reference/preparations.md)。

## 支持的模型/功能

当前 `preparations` 流程适用于所有通过百炼 Model API 提供的模型，包括但不限于 `qwen-max`、`qwen-plus`、`qwen-turbo` 及 `qwen-vl` 等多模态模型。SDK 初始化后，可统一调用 `dashscope.Generation.call()` 或 `dashscope.MultiModalConversation.call()` 等接口，无需为不同模型重复配置认证逻辑。具体模型能力与兼容性详见 [使用 API](../../raw/model-api-reference/preparations.md) 中的 SDK Expert 指南。

## 关键参数

- `api_key`：必填，需通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取并安全存储；
- `model`：调用时指定，非 preparation 阶段参数，但 SDK 初始化不校验该值，实际调用时才校验；
- `api_base`（可选）：用于私有化部署场景，覆盖默认 endpoint，详见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 中的高级配置说明。

> **注意**：部分旧版文档将 `region` 列为初始化参数，但自 dashscope v1.20.0 起该参数已被废弃，仅保留 `api_key` 和 `api_base` 两个有效配置项；请以 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 的最新说明为准。

## 使用方式

1. 访问 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 页面，登录百炼控制台，在「API 密钥管理」中创建并复制密钥；
2. 执行 `pip install dashscope` 安装 SDK（Python），或参考 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 获取其他语言支持；
3. 在代码中设置环境变量或显式传入 `api_key`，例如：  
   ```python
   import dashscope
   dashscope.api_key = "sk-xxx"  # 或 os.environ["DASHSCOPE_API_KEY"]
   ```

## 限制和注意事项

- 单个 API Key 默认配额受项目级限制约束，超出将返回 `429 Too Many Requests`，详细码表见 [错误码](../../raw/model-api-reference/preparations/error-code.md)；
- API Key 不可跨阿里云主账号共享，且不支持子用户独立生成（需主账号操作）；
- 本地开发建议使用 `.env` 文件管理密钥，严禁硬编码或提交至 Git；生产环境应使用 KMS 或 Secret Manager 注入。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


