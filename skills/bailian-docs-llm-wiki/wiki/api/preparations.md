# preparations

在调用百炼平台模型 API 前，需完成身份认证、环境配置与依赖安装等基础准备。这些步骤是所有模型调用（如 `qwen-max`、`qwen-plus`、文本嵌入、多模态等）的通用前置条件。开发者应优先阅读 [使用 API](../../raw/model-api-reference/preparations.md) 文档以获取完整路径指引。

## 支持的模型/功能

`preparations` 本身不绑定特定模型，而是为所有支持的模型服务，包括但不限于：  
- 大语言模型（`qwen-max`、`qwen-plus`、`qwen-turbo`）  
- 文本嵌入模型（`text-embedding-v1`）  
- 多模态模型（`qwen-vl-plus`）  
- [函数调用](../concepts/function-calling.md)与工具增强能力（需 SDK ≥ 2.0）  
> **注意**：部分旧版 SDK（如 1.x）对[函数调用](../concepts/function-calling.md)和流式响应的支持不完整，详见 [SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)，建议新项目统一使用 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 推荐的 2.x+ 版本。

## 关键参数

必需参数包括：  
- `api_key`：通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取，需安全存储，禁止硬编码；  
- `base_url`（可选）：默认为 `https://dashscope.aliyuncs.com/api/v1`，私有化部署场景需覆盖，详见 [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)；  
- `model`：必须显式指定，且需与所调用接口能力匹配（例如 `text-embedding-v1` 不支持 `messages` 字段）。

## 使用方式

1. 安装最新 SDK：`pip install dashscope>=2.0.0`（推荐）或按需安装轻量版 `pip install dashscope-core`；  
2. 配置环境变量：`export DASHSCOPE_API_KEY=your_api_key`；  
3. 初始化客户端并发起请求（Python 示例）：
   ```python
   import dashscope
   dashscope.api_key = "sk-..."  # 或省略，自动读取环境变量
   response = dashscope.Generation.call(model="qwen-max", prompt="Hello")
   ```

## 限制和注意事项

- 单次请求最大 token 数受模型限制（如 `qwen-turbo` 输入上限为 8K），超出将返回 `400 Bad Request`；  
- 免费额度仅限个人认证账号，企业账号需单独开通配额，具体规则见 [错误码](../../raw/model-api-reference/preparations/error-code.md) 中 `ResourceExhausted` 相关说明；  
- 所有 API 调用均需 HTTPS，HTTP 请求会被拒绝；  
- 若使用代理或内网环境，请确保 `base_url` 域名可解析且端口 443 可达。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


