# preparations

`preparations` 是调用百炼模型 API 前必需完成的初始化步骤，涵盖身份认证、开发环境配置及基础依赖安装。这些操作直接影响后续请求的可用性与稳定性，开发者需严格按顺序执行。所有步骤均基于 [使用 API (raw/model-api-reference/preparations.md)](../../raw/model-api-reference/preparations.md) 文档定义。

## 支持的模型/功能

当前 `preparations` 流程适用于所有通过百炼 Model API 提供的模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio 等），但**不适用于控制台直接调试或 Web UI 交互场景**。SDK 初始化与 API Key 配置是通用前置条件，无论调用文本生成、多模态理解或流式响应功能均需完成。具体模型兼容性请参考 [使用 API (raw/model-api-reference/preparations.md)](../../raw/model-api-reference/preparations.md) 中的 SDK Expert 指南部分。

## 关键参数

- `api_key`：必填，用于身份鉴权，须通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取并安全存储；
- `base_url`（可选）：仅在私有化部署或调试环境下需显式指定，公有云默认使用官方 endpoint；
- `timeout`（推荐设置）：建议设为 60 秒以上，避免因模型推理耗时导致连接中断；
- `max_retries`（推荐设置）：SDK 默认重试策略可能不满足高可用需求，建议在初始化客户端时显式配置。

## 使用方式

1. **获取 API Key**：登录百炼控制台，在「API 密钥管理」中创建并复制密钥；  
2. **安装 SDK**：运行 `pip install dashscope`（Python）或对应语言 SDK，版本需 ≥ 1.20.0（详见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）；  
3. **初始化客户端**：在代码中设置 `api_key` 并实例化 `dashscope.Generation` 或 `dashscope.MultiModalConversation` 等对应客户端类；  
4. **验证连通性**：建议首次调用前使用 `dashscope.get_version()` 或轻量级健康检查接口确认环境就绪。

> **注意**：[SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 文档中提及的 `DashScopeClient` 类已在 v1.22.0+ 版本中废弃，应统一使用 `dashscope.*` 模块下的具体客户端类，旧示例代码存在过时风险。

## 限制和注意事项

- 单个 API Key 默认限流 10 QPS（每秒查询数），超出将返回 `429 Too Many Requests` 错误（详见 [错误码](../../raw/model-api-reference/preparations/error-code.md)）；  
- API Key 不可跨 Region 使用，华东 1（cn-shanghai）密钥无法调用华北 2（cn-beijing）模型 endpoint；  
- 本地开发环境禁止硬编码 `api_key`，必须通过环境变量（如 `DASHSCOPE_API_KEY`）或配置文件注入；  
- 若使用代理或内网环境，需确保 `https://dashscope.aliyuncs.com` 可达，且 TLS 版本 ≥ 1.2。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


