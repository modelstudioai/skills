# preparations

`preparations` 是调用百炼模型 API 前必需完成的初始化步骤，涵盖身份认证、开发环境配置及基础依赖安装。这些操作直接影响后续请求的合法性与稳定性，开发者需严格按顺序执行。所有步骤均基于 [使用 API](../../raw/model-api-reference/preparations.md) 文档定义。

## 支持的模型/功能

当前 `preparations` 流程适用于所有通过百炼 Model API 提供的模型（包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 等），但**不适用于控制台直接调试或 Web UI 场景**。SDK 初始化后支持同步调用、流式响应、[异步任务](../concepts/asynchronous-task.md)提交等核心能力，具体能力边界请参考 [使用 API](../../raw/model-api-reference/preparations.md) 中的 SDK Expert 指南。

## 关键参数

- `api_key`：必填，用于身份鉴权，须通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取并安全存储；
- `model`：非 prep 阶段参数，但 SDK 初始化时若指定默认 model（如 `DashScope(api_key=..., model="qwen-turbo")`），将影响后续 `.call()` 的默认行为；
- `base_url`（可选）：仅在私有化部署场景下需显式覆盖，默认指向百炼公有云服务端点。

> **注意**：部分旧版文档示例中将 `api_key` 作为 `.call()` 参数传入，该用法已废弃；正确方式是初始化 Client 时传入，详见 [使用 API](../../raw/model-api-reference/preparations.md)。

## 使用方式

1. **获取 API Key**：访问控制台「API 密钥管理」页面创建并复制密钥，禁止硬编码到源码中；
2. **安装 SDK**：运行 `pip install dashscope`（Python）或对应语言的官方包，版本需 ≥ 1.18.0（见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）；
3. **初始化 Client**：使用 `dashscope.Generation` 或 `dashscope.MultiModalConversation` 等类实例化，传入 `api_key` 及必要配置；
4. （可选）启用日志调试：设置 `logging.basicConfig(level=logging.DEBUG)` 查看请求/响应详情。

## 限制和注意事项

- 单个 API Key 默认限速 5 QPS，超出将返回 `429 Too Many Requests` 错误（具体策略见 [错误码](../../raw/model-api-reference/preparations/error-code.md)）；
- 免费试用额度仅对新注册账号生效，且不可跨项目共享；
- Windows 系统下若出现 SSL 证书验证失败，请先执行 `pip install --upgrade certifi`，该问题已在 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 中明确说明；
- `api_key` 泄露将导致账户被滥用，务必通过环境变量（如 `DASHSCOPE_API_KEY`）注入，而非明文写入代码。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


