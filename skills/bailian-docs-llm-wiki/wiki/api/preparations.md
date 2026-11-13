# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖认证凭证获取、SDK 集成、服务端点配置等关键环节。开发者需按顺序完成这些准备，否则将无法发起有效请求。所有操作均需遵循 [使用 API](../../raw/model-api-reference/preparations.md) 文档中定义的规范流程。

## 支持的模型/功能

当前 `preparations` 流程适用于所有通过百炼平台 HTTP API 或官方 SDK 调用的模型，包括 Qwen 系列大语言模型、多模态模型（如 Qwen-VL）、语音与文本嵌入模型等。不支持直接通过控制台界面触发的[异步任务](../concepts/asynchronous-task.md)（如批量数据处理）所需的额外鉴权方式。具体模型兼容性请参考 [使用 API](../../raw/model-api-reference/preparations.md) 中的适用范围说明。

## 关键参数

- `api_key`：必填，用于身份认证，须通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取并安全存储；
- `base_url`：可选，默认为 `https://dashscope.aliyuncs.com/api/v1`，如需私有化部署或调试，应按 [Base URL总览](../../raw/model-api-reference/preparations/base-url.md) 配置对应地址；
- `model`：非 preparation 阶段参数，但部分 SDK 初始化时会预设默认模型，需注意与实际调用时指定的模型一致，避免因版本差异导致行为异常。

> **注意**：[SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md) 中描述的 `auth_token` 参数已被弃用，新版 SDK（2.x+）仅接受 `api_key`；若混用旧文档示例，将导致 `401 Unauthorized` 错误。

## 使用方式

1. **获取 API Key**：登录百炼控制台，在「API 密钥管理」中创建并复制密钥，严禁硬编码或提交至代码仓库；
2. **安装 SDK**：执行 `pip install dashscope`（Python）或按 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 中对应语言指南操作；
3. **初始化客户端**：设置 `api_key` 和（可选）`base_url`，例如：
   ```python
   import dashscope
   dashscope.api_key = "sk-xxx"
   # 或显式初始化 client（推荐用于多 key 场景）
   ```
4. **验证连接**：建议首次使用前调用轻量接口（如 `/status` 或 `models/list`）确认鉴权与网络连通性。

## 限制和注意事项

- 单个 API Key 默认限流 10 QPS（具体以控制台配额页为准），超限返回 `429 Too Many Requests`，详情见 [错误码](../../raw/model-api-reference/preparations/error-code.md)；
- `api_key` 有效期永久，但可随时在控制台禁用或轮换，轮换后旧 key 立即失效；
- 不同地域（Region）的 Base URL 不互通，跨域请求将失败，务必核对 [Base URL总览](../../raw/model-api-reference/preparations/base-url.md) 中的地域映射；
- SDK Expert 模式（见 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)）提供底层请求控制能力，适用于调试与定制化场景，但需自行处理重试、超时等逻辑。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


