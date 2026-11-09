# preparations

在调用阿里云百炼模型服务前，开发者需完成 API Key 获取与配置、SDK 安装、Base URL 选择等基础准备。这些步骤直接影响鉴权、路由、功能可用性及错误排查效率。本文汇总关键配置项、参数约束与常见陷阱，并明确各环节的官方文档依据。

## 支持的模型/功能

百炼支持文本生成、多模态对话、图像/视频生成、语音识别与合成、[向量嵌入](../concepts/embedding.md)、重排序及智能体应用等多种能力。具体模型列表见 [模型列表](raw/model-user-guide/get-started-with-models/models.md)，但**并非所有模型均支持全部功能**。例如：
- 思考模式（`enable_thinking=true`）仅限特定模型（如 `qwen3.7-plus`），且该模型强制要求 `enable_thinking=true`，不可设为 `false` [原文标题](../../raw/model-api-reference/preparations/error-code.md)；
- 联网搜索（`enable_search=true`）仅适用于明确标注支持该能力的模型，否则将报 `This model does not support enable_search` 错误 [原文标题](../../raw/model-api-reference/preparations/error-code.md)；
- 结构化输出（`response_format={"type": "json_object"}`）要求提示词中必须包含 `json` 关键词，且不支持与思考模式共用 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

> **注意**：文档 1 中“`The thinking_budget parameter must be a positive integer and not greater than xxx`”未说明 `xxx` 的具体值来源；实际应以 [模型列表](raw/model-user-guide/get-started-with-models/models.md) 中各模型标注的“最大思维链长度”为准，而非硬编码数值。

## 关键参数

以下参数在多数模型调用中通用，且有严格取值范围：

| 参数 | 约束条件 | 说明 |
|------|----------|------|
| `temperature` | `[0.0, 2.0)` | 小于 2.0，不可等于 2.0 |
| `top_p` | `(0.0, 1.0]` | 大于 0，可等于 1.0 |
| `top_k` | `≥ 0` | 整数，可为 0 |
| `repetition_penalty` | `> 0.0` | 必须为正浮点数 |
| `presence_penalty` | `[-2.0, 2.0]` | 包含端点 |
| `n`（返回结果数） | `[1, 4]` | 最多 4 个候选 |
| `max_tokens` | `[1, 模型最大输出 Token 数]` | 上限见模型文档 |
| `seed` | `[0, 9223372036854775807]` | DashScope 协议下有效范围 |

此外，流式调用相关参数需协同设置：
- 若启用 `enable_thinking=true`，则 `incremental_output` 必须为 `"true"`，且 `result_format` 必须为 `"message"`；
- 音频输出（`audio`）仅支持 `stream=true`；
- `stop` 参数仅接受 `str`、`list[str]`、`list[int]` 或 `list[list[int]]` 四种类型 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

## 使用方式

### 1. 获取并配置 API Key  
前往百炼控制台 [API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key) 页面创建，**必须与 Base URL 所属地域匹配**。推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），其提供流量隔离与更高性能 [原文标题](../../raw/model-api-reference/preparations/base-url.md)。API Key 应通过环境变量（`DASHSCOPE_API_KEY`）安全注入，避免硬编码 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。

### 2. 安装 SDK  
- **Python**：安装 `dashscope>=2.0.1`（推荐）或 `openai` SDK（兼容 OpenAI 接口）；
- **Java/Node.js/Go**：按需引入对应语言的 DashScope 或 OpenAI SDK [原文标题](../../raw/model-api-reference/preparations/install-sdk.md)。  
存量项目若使用 DashScope 1.x，需注意其已冻结维护，新项目请直接采用 2.0 [原文标题](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)。

### 3. 调用示例（DashScope SDK 2.0）  
```python
from dashscope import Client
client = Client(api_key=os.getenv("DASHSCOPE_API_KEY"), region="cn-beijing")
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你好"}],
    stream=True
)
for chunk in response:
    print(chunk.choices[0].delta.content, end="", flush=True)
```

## 限制和注意事项

- **地域隔离**：API Key、Base URL、模型可用性均按地域独立，跨地域混用将导致 `401` 鉴权失败 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。
- **流式强制约束**：部分模型（如 `qwen3-vl-plus`）仅支持流式调用，若未设 `stream=true` 将报 `This model only support stream mode` [原文标题](../../raw/model-api-reference/preparations/error-code.md)。
- **[异步任务](../concepts/asynchronous-task.md)清理**：删除 API Key 后，其关联的[异步任务](../concepts/asynchronous-task.md)仍会继续执行并产生费用；如需终止，须手动调用任务取消接口 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。
- **SDK Expert 依赖联网**：DashScope SDK 内置的智能助手需有效 API Key 并联网调用模型，不支持离线诊断 [原文标题](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)。
- **错误重试策略**：对 `429`（限流）或 `5xx`（临时服务异常）应采用指数退避重试，但对 `400`（参数错误）等客户端错误需修正后重试，而非盲目重试 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [错误码](../../raw/model-api-reference/preparations/error-code.md)
- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)
- [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)
- [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)


