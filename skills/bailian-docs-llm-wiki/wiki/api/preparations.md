# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的初始化步骤，涵盖认证凭证获取、开发环境配置及基础网络设置。开发者需按顺序完成 API Key 配置、SDK 安装与初始化、Base URL 适配等环节，方可发起合法请求。所有步骤均以安全、可复现和兼容性为设计前提。

## 支持的模型/功能

当前 `preparations` 流程适用于全部百炼平台公开模型（含 Qwen 系列、Baichuan、GLM 等）的同步/异步推理、流式响应、Function Calling 及多模态输入等核心能力。不区分模型类型，统一采用相同的认证与传输协议。具体模型支持列表请参考 [使用 API](../../raw/model-api-reference/preparations.md) 中的上下文说明。

## 关键参数

- `api_key`：必填，用于身份鉴权，需通过控制台申请并妥善保管；  
- `base_url`：可选，用于私有化部署或灰度环境，覆盖默认域名；默认值见 [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)；  
- `timeout`：建议显式设置（如 `30s`），避免因网络波动导致连接挂起；  
- `max_retries`：SDK 默认启用指数退避重试（最多 2 次），生产环境建议保留。

> **注意**：[SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md) 中的 `dashscope.api_key = "xxx"` 全局赋值方式已被弃用，新版 SDK（2.x+）要求通过 `DashScopeClient(api_key=...)` 实例化传参，否则将触发 `AuthenticationError`。

## 使用方式

1. **获取 API Key**：登录百炼控制台 →「API 密钥管理」→ 创建并复制密钥；  
2. **安装 SDK**：执行 `pip install dashscope`（Python）或对应语言客户端；  
3. **初始化客户端**：传入 `api_key` 和可选 `base_url`，例如：  
   ```python
   from dashscope import Generation
   Generation.call(model='qwen-max', api_key='YOUR_KEY', base_url='https://dashscope.aliyuncs.com/api/v1')
   ```  
   更多语言示例见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

## 限制和注意事项

- 单个 API Key 默认限流 60 QPS（每秒查询数），超出将返回 `429 Too Many Requests` 错误，详情见 [错误码](../../raw/model-api-reference/preparations/error-code.md)；  
- API Key 不可跨 Region 使用，若调用非默认地域模型（如 `qwen-vl` 在 cn-shanghai），必须显式指定对应 `base_url`；  
- 严禁在前端代码、Git 仓库或日志中硬编码 `api_key`，应通过环境变量（如 `DASHSCOPE_API_KEY`）注入；  
- SDK Expert 模式（如自动重试、指标上报）需额外启用，详见 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


