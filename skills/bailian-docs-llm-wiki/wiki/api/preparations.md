# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖身份认证、开发环境搭建及 SDK 集成。开发者需按顺序完成 API Key 获取、SDK 安装与初始化，方可发起有效请求。所有操作均需遵循 [使用 API](../../raw/model-api-reference/preparations.md) 文档的流程指引。

## 支持的模型/功能

当前 `preparations` 流程适用于所有通过百炼平台 HTTP API 或 SDK 调用的模型，包括 Qwen 系列大语言模型（如 qwen-max、qwen-plus）、多模态模型（如 qwen-vl）及 Embedding 模型（如 text-embedding-v1）。不支持直接用于 Model Studio 的可视化调试界面或私有化部署的离线 SDK 初始化流程——后者需参考独立部署手册。具体模型兼容性请以 [使用 API](../../raw/model-api-reference/preparations.md) 中列出的 endpoint 清单为准。

## 关键参数

- `api_key`：必填，从 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 页面申请并安全存储，不可硬编码于客户端代码中  
- `base_url`（可选）：仅在私有化部署或调试代理场景下覆盖默认网关地址，生产环境通常无需设置  
- `timeout`（推荐显式设置）：建议设为 60s 以上，避免因模型推理耗时波动导致连接中断；该参数在 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 中有详细说明  

> **注意**：部分旧版文档示例中将 `api_key` 作为 query 参数传递，此方式已废弃且存在安全风险；必须通过 `Authorization: Bearer <api_key>` 请求头传递，详见 [使用 API](../../raw/model-api-reference/preparations.md) 的安全规范章节。

## 使用方式

1. 访问 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 页面，在控制台创建并复制密钥  
2. 根据语言选择对应 SDK：Python 用户执行 `pip install dashscope`，Node.js 用户执行 `npm install @dashscope/nodejs`，其他语言参见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)  
3. 初始化客户端时传入 `api_key`，例如 Python 中：  
   ```python
   import dashscope
   dashscope.api_key = "sk-xxx"
   ```  
   更健壮的初始化方式（如环境变量注入、自动重试）见 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)

## 限制和注意事项

- 单个 API Key 默认限流 5 QPS（每秒查询数），超出将返回 `429 Too Many Requests` 错误，详情见 [错误码](../../raw/model-api-reference/preparations/error-code.md)  
- API Key 仅对创建者所在工作空间生效，跨工作空间调用需单独申请对应 Key  
- 不支持在浏览器前端直连 API（CORS 策略阻止），必须通过服务端代理转发请求  
- 免费额度仅适用于首次开通账号的用户，续订或升级需联系商务；额度规则以 [使用 API](../../raw/model-api-reference/preparations.md) 中“计费说明”为准

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


