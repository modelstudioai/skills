# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖身份认证、开发环境搭建及客户端初始化。开发者需按顺序完成 API Key 获取、SDK 安装与配置，方可发起合法请求。所有操作均需遵循 [使用 API](../../raw/model-api-reference/preparations.md) 文档中定义的流程规范。

## 支持的模型/功能

当前 `preparations` 流程适用于全部百炼平台公开模型（如 qwen-max、qwen-plus、qwen-turbo）及配套能力（如流式响应、Function Calling、多模态输入）。不支持仅限控制台试用的内部灰度模型。具体模型兼容性请以 [使用 API](../../raw/model-api-reference/preparations.md) 中“适用范围”章节为准。

## 关键参数

- `api_key`：必填，通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取，需在请求头 `Authorization: Bearer <api_key>` 中传递  
- `base_url`：可选，用于私有化部署场景，默认为 `https://dashscope.aliyuncs.com/api/v1`  
- `timeout`：建议显式设置（如 60 秒），避免因网络波动导致 SDK 默认超时行为不一致；详见 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 中的连接管理说明  

> **注意**：部分旧版 SDK 示例代码中将 `api_key` 作为请求体参数传入，该方式已废弃；请严格按 [使用 API](../../raw/model-api-reference/preparations.md) 要求置于请求头。

## 使用方式

1. 访问 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 页面，创建并复制有效密钥  
2. 根据语言选择对应 SDK，执行 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 步骤（如 `pip install dashscope`）  
3. 初始化客户端时传入 `api_key` 和必要参数，例如 Python 中：  
   ```python
   import dashscope
   dashscope.api_key = "YOUR_API_KEY"
   ```

## 限制和注意事项

- 单个 API Key 默认 QPS 限制为 5，超出将返回 `429 Too Many Requests` 错误（参见 [错误码](../../raw/model-api-reference/preparations/error-code.md)）  
- API Key 不可跨 Region 使用；华东 1（杭州）密钥无法调用华北 2（北京）部署的模型实例  
- 严禁在前端 JavaScript 等公开环境中硬编码 `api_key`，否则将导致密钥泄露和账户风险 —— 此安全要求在 [使用 API](../../raw/model-api-reference/preparations.md) 中被明确强调

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


