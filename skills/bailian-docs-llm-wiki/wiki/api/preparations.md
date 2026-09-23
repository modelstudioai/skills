# preparations

`preparations` 是调用百炼模型 API 前必需完成的初始化步骤，涵盖身份认证、开发环境配置及基础依赖安装。这些操作直接影响后续请求的可用性与稳定性，开发者需严格按顺序执行。所有步骤均基于 [使用 API (raw/model-api-reference/preparations.md)](../../raw/model-api-reference/preparations.md) 文档定义。

## 支持的模型/功能

当前 `preparations` 流程适用于所有通过百炼 Model API 提供的模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio 等），但**不适用于控制台直接调试或 Web UI 交互场景**。SDK 初始化与 API Key 配置是通用前置条件，无论调用文本生成、多模态理解或流式响应功能均需完成。具体模型兼容性请参考 [使用 API (raw/model-api-reference/preparations.md)](../../raw/model-api-reference/preparations.md) 中的 SDK Expert 指南部分。

## 关键参数

- `api_key`：必填，用于身份鉴权，须通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取并安全存储；
- `base_url`（可选）：仅在私有化部署或调试环境下需显式指定，公有云默认使用官方 endpoint；
- `timeout`（推荐设置）：建议设为 60s 以上，避免因模型推理耗时波动导致连接中断；
- `max_retries`（推荐设置）：SDK 默认重试策略可能不满足高并发场景，建议显式配置为 2–3 次。

## 使用方式

1. **获取 API Key**：登录百炼控制台，在「API 密钥管理」中创建并复制密钥，严禁硬编码到客户端或公开仓库；  
2. **安装 SDK**：运行 `pip install dashscope`（Python）或对应语言 SDK，版本需 ≥ 1.18.0（旧版存在 token 刷新缺陷，详见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）；  
3. **初始化客户端**：  
   ```python
   import dashscope
   dashscope.api_key = "sk-..."  # 或通过环境变量 DASHSCOPE_API_KEY
   ```  
   多线程/异步场景下，建议使用 `dashscope.AsyncClient()` 并复用实例。

## 限制和注意事项

- 单个 API Key 默认 QPS 限制为 5，超出将返回 `429 Too Many Requests` 错误（见 [错误码](../../raw/model-api-reference/preparations/error-code.md)）；  
- API Key 不支持跨区域使用（如华东 region 的 key 无法调用华北 endpoint），且无法用于百炼控制台内嵌的 Playground；  
- > **注意**：[使用 API (raw/model-api-reference/preparations.md)](../../raw/model-api-reference/preparations.md) 中提及的“SDK 可自动读取 `~/.dashscope/config` 配置文件”，该功能在 v1.19.0+ 已废弃，实际行为以 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 文档为准——当前仅支持环境变量或代码显式赋值。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


