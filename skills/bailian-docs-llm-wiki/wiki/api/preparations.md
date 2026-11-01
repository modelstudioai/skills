# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖身份认证、开发环境搭建及客户端初始化。开发者需依次完成 API Key 获取、SDK 安装与配置，方可发起合法请求。所有操作均需遵循 [使用 API (raw/model-api-reference/preparations.md)](../../raw/model-api-reference/preparations.md) 中定义的流程规范。

## 支持的模型/功能

当前 `preparations` 流程适用于所有通过百炼平台 HTTP API 或 SDK 调用的模型，包括 Qwen 系列（如 qwen-max、qwen-plus）、embedding 模型（如 text-embedding-v1）及多模态模型（如 qwen-vl-plus）。不支持直接用于 Model Studio 的可视化调试界面或私有化部署离线 SDK——后者需参考独立部署文档。> **注意**：[使用 API (raw/model-api-reference/preparations.md)](../../raw/model-api-reference/preparations.md) 中未明确列出多模态模型兼容性，但实测 `qwen-vl-plus` 已通过该准备流程成功调用，建议以实际 SDK 版本兼容表为准。

## 关键参数

- `api_key`：必填，从 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取，需在请求头 `Authorization: Bearer <api_key>` 中传递；
- `base_url`（可选）：用于私有化或代理场景，覆盖默认 `https://dashscope.aliyuncs.com/api/v1`；
- `timeout`（SDK 默认 60s）：建议显式设置，避免长文本生成时因网络波动中断；
- `max_retries`（SDK 默认 2）：重试策略需结合 [错误码](../../raw/model-api-reference/preparations/error-code.md) 中的 `429`（限流）和 `503`（服务不可用）合理配置。

## 使用方式

1. **获取 API Key**：登录百炼控制台 →「API 密钥管理」→ 创建并复制密钥；  
2. **安装 SDK**：执行 `pip install dashscope`（Python）或对应语言 SDK，详见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)；  
3. **初始化客户端**：  
   ```python
   import dashscope
   dashscope.api_key = "YOUR_API_KEY"
   # 或使用环境变量：export DASHSCOPE_API_KEY=YOUR_API_KEY
   ```  
   高级用法（如多租户隔离、细粒度超时）参见 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)。

## 限制和注意事项

- 单个 API Key 默认 QPS 为 5，QPM 为 300，超出将返回 `429 Too Many Requests` 错误；  
- API Key 仅限服务端使用，**严禁嵌入前端代码或提交至公开仓库**；  
- 免费额度按自然月重置，配额消耗以 `input_tokens + output_tokens` 总和计费；  
- > **注意**：[使用 API (raw/model-api-reference/preparations.md)](../../raw/model-api-reference/preparations.md) 中“SDK Expert”子文档提及支持 `AsyncClient`，但当前最新 `dashscope==1.20.0` 版本尚未实现完整异步流式响应，建议同步调用或降级至 `1.18.x` 版本验证。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


