# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖身份认证、开发环境搭建及客户端初始化。开发者需依次完成 API Key 获取、SDK 安装与配置，方可发起合法请求。所有操作均需遵循平台安全规范与配额约束。

## 支持的模型/功能

当前 `preparations` 流程适用于所有通过百炼 API 提供的模型服务，包括但不限于 Qwen 系列大语言模型、[多模态](../concepts/multimodal.md)模型（如 Qwen-VL）及 Embedding 模型。该准备流程不区分模型类型，统一采用 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 和 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 作为前置依赖。

## 关键参数

- `api_key`：必填，用于身份鉴权，需通过控制台申请并妥善保管；  
- `model`：虽非 preparation 阶段直接配置，但在 SDK 初始化后首次调用时必须指定，其取值须与所购模型权限匹配；  
- `base_url`（可选）：用于私有化部署场景，覆盖默认 API 地址，详见 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 中的高级配置说明。

## 使用方式

1. 访问控制台，按指引完成实名认证并[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)；  
2. 根据语言选择对应 SDK，执行 `pip install dashscope`（Python）或参考 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 中的其他语言命令；  
3. 初始化客户端：  
   ```python
   import dashscope
   dashscope.api_key = "YOUR_API_KEY"
   ```  
   更灵活的初始化方式（如多 key 轮询、超时设置）请参阅 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)。

## 限制和注意事项

- 单个 API Key 默认享有基础调用配额，超出后将返回 `429 Too Many Requests` 错误，具体错误码含义见 [错误码](../../raw/model-api-reference/preparations/error-code.md)；  
- API Key 不可跨区域使用（例如华东 region 的 key 无法调用华北 endpoint），且不支持在浏览器前端直接暴露；  
> **注意**：部分旧版文档提及可通过环境变量 `DASHSCOPE_API_KEY` 自动加载密钥，但 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 明确指出该方式自 v1.16.0 起已被弃用，推荐显式赋值 `dashscope.api_key` 或使用 `dashscope.init()`。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


