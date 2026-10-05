# preparations

`preparations` 是调用百炼模型 API 前必需完成的初始化步骤，涵盖认证凭证获取、开发环境配置及基础依赖安装。这些操作直接影响后续请求的合法性与稳定性，开发者需严格按顺序执行。所有步骤均以最小必要权限和安全实践为设计前提。

## 支持的模型/功能

当前 `preparations` 流程适用于全部百炼平台公开模型（如 Qwen 系列、Qwen-VL、Qwen-Audio）及配套能力（流式响应、异步任务、文件上传等）。不区分模型类型，统一使用同一套认证与 SDK 初始化机制。具体模型支持列表详见 [使用 API](../../raw/model-api-reference/preparations.md) 文档中“适用范围”章节。

## 关键参数

- `api_key`：必填，通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取，需在请求头 `Authorization: Bearer <api_key>` 中传递；
- `base_url`（可选）：用于私有化部署场景，覆盖默认 `https://dashscope.aliyuncs.com/api/v1`；
- `timeout`（SDK 默认 30s）：建议显式设置，避免因网络波动导致连接挂起；  
- `max_retries`（SDK 默认 2）：重试策略需结合幂等性设计，尤其对非 GET 请求。

## 使用方式

1. **获取 API Key**：登录百炼控制台，在「API 密钥管理」中创建并复制密钥，严禁硬编码或提交至版本库；  
2. **安装 SDK**：执行 `pip install dashscope`（Python）或对应语言 SDK，版本需 ≥ 1.18.0（见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）；  
3. **初始化客户端**：  
   ```python
   import dashscope
   dashscope.api_key = "YOUR_API_KEY"
   ```
   或使用环境变量 `DASHSCOPE_API_KEY`；  
4. **验证连通性**：调用任意轻量接口（如 `dashscope.models.list()`）确认配置生效。

> **注意**：[SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 文档中提及的 `ExpertClient` 类已在 v1.20.0+ 版本中废弃，应统一使用 `dashscope.Generation` 或 `dashscope.MultiModalConversation` 等标准客户端类，避免兼容性问题。

## 限制和注意事项

- 单个 API Key 默认限流 5 QPS（每秒查询数），超出将返回 `429 Too Many Requests` 错误，详细策略见 [错误码](../../raw/model-api-reference/preparations/error-code.md)；  
- API Key 仅限服务端使用，**禁止在前端 JavaScript 或移动端代码中直接暴露**；  
- 临时 Token（如 STS 临时凭证）不支持该流程，必须使用长期有效的主账号或子账号 API Key；  
- Windows 系统下若出现 SSL 证书验证失败，请优先升级 `certifi` 包而非禁用验证。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


