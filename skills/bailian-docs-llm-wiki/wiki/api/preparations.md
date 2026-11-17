# preparations

在调用百炼平台模型 API 前，需完成身份认证、环境配置与依赖安装等基础准备。这些步骤是所有模型调用（如 `qwen-max`、`qwen-plus`、文本嵌入、多模态等）的通用前提，直接影响请求的合法性与稳定性。请严格按顺序执行，避免因配置缺失导致 401、403 或连接失败。

## 支持的模型/功能

preparations 本身不绑定特定模型，而是为所有支持的模型服务，包括但不限于：  
- 大语言模型（`qwen-max`、`qwen-plus`、`qwen-turbo`）  
- 文本嵌入模型（`text-embedding-v1`）  
- 多模态模型（`qwen-vl-plus`）  
- [函数调用](../concepts/function-calling.md)与工具增强能力（需 SDK ≥ 2.0）  
详细模型列表及能力说明见 [使用 API](../../raw/model-api-reference/preparations.md)。

## 关键参数

必须配置以下参数方可发起有效请求：  
- `api_key`：通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取，需妥善保管并禁止硬编码至前端；  
- `base_url`：默认为 `https://dashscope.aliyuncs.com/api/v1`，国内用户可选 `https://dashscope.aliyuncs.com/compatible-mode/v1`（兼容 OpenAI 格式），详见 [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)；  
- `model`：必须显式指定，且须与所选 endpoint 兼容（例如 `text-embedding-v1` 不支持 `messages` 字段）。

## 使用方式

1. **安装 SDK**：推荐使用最新版 DashScope Python SDK（≥ 2.0）：  
   ```bash
   pip install dashscope
   ```  
   历史项目若依赖 SDK 1.x，请参考 [SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)，但该版本已停止维护，不建议新项目使用。  
2. **初始化客户端**：  
   ```python
   import dashscope
   dashscope.api_key = "YOUR_API_KEY"
   # 或传入参数方式（更安全）
   client = dashscope.Client(api_key="YOUR_API_KEY")
   ```  
3. **调用示例**（以 `qwen-turbo` 为例）：  
   ```python
   from dashscope import Generation
   resp = Generation.call(model='qwen-turbo', prompt='你好')
   ```

## 限制和注意事项

- 单个 API Key 默认有 QPS 和日调用量限制，超出将返回 `429 Too Many Requests`，具体配额见控制台；  
- 错误响应结构统一，常见错误码含义参见 [错误码](../../raw/model-api-reference/preparations/error-code.md)；  
- SDK Expert 功能（如自动重试、流式响应封装）需启用 `dashscope.experimental.enable()`，详见 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)；  
> **注意**：[SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md) 中的 `dashscope.Generation` 初始化方式（如 `dashscope.Generation(api_key=...)`）在 SDK 2.0+ 中已废弃，直接使用将引发 `AttributeError`。请务必迁移至 `Client` 实例化模式。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


