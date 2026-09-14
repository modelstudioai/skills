# llm application

`llm application` 是百炼平台中用于封装和部署大语言模型能力的核心应用类型，支持通过低代码/高代码方式构建面向终端用户的 AI 服务。开发者可基于预置模板或自定义逻辑快速创建智能体、工作流、文件问答等形态的应用，并统一接入 API 或嵌入前端。该能力依托 [应用开发](../../raw/application-user-guide/llm-application.md) 文档定义的基础分类与架构原则。

## 支持的模型与功能

- **应用类型**：当前支持五类 LLM 应用形态，包括新版智能体应用（Agent 2.0）、智能体应用（Agent 1.0）、工作流应用、高代码应用、文件问答应用，详见 [应用开发](../../raw/application-user-guide/llm-application.md)。
- **模型绑定**：所有应用类型均支持绑定百炼平台托管的任意 LLM 模型（如 Qwen 系列、Qwen-VL、Qwen-Audio），但 Agent 2.0 和工作流应用额外支持多模型编排与条件路由；文件问答仅支持启用 RAG 的文本模型。
- **扩展能力**：高代码应用支持 Python SDK 调用外部服务、自定义工具函数及异步回调；其余类型仅支持平台内置组件（如知识库、插件、系统提示词）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，由平台生成，见 [应用开发](../../raw/application-user-guide/llm-application.md) 中“应用管理”章节 |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；仅对 `/v1/chat/completions` 接口生效 |
| `temperature` | number | 否 | 控制输出随机性，范围 `[0.0, 2.0]`，默认 `0.8`；Agent 2.0 中该参数在节点级覆盖全局设置 |
| `max_tokens` | integer | 否 | 最大生成长度，上限取决于所选模型上下文窗口（如 Qwen2-72B 最高支持 32768） |

> **注意**：`top_p` 参数在部分旧版 SDK 示例中被错误标注为“推荐设为 1.0”，但根据最新 [应用开发](../../raw/application-user-guide/llm-application.md) 实际行为，其默认值为 `0.8`，且在 Agent 2.0 中已改为节点级独立配置，全局设置无效。

## 使用方式

1. **创建应用**：在 Model Studio 控制台选择「创建应用」→ 选定类型（如“新版智能体应用”）→ 配置基础信息与模型；
2. **调试与发布**：使用内置 Playground 测试输入输出，确认无误后点击「发布」获取 `app_id`；
3. **调用接口**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/chat \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"input": {"text": "你好"}, "parameters": {"stream": true}}'
   ```
   更多请求格式与字段说明参见官方 API 文档，其设计依据源自 [应用开发](../../raw/application-user-guide/llm-application.md) 中的接口契约约定。

## 限制和注意事项

- 单次请求最大输入 tokens 数受所选模型上下文限制（如 Qwen2-7B 为 4096，Qwen2-72B 为 32768），超出将返回 `400 Bad Request`；
- 文件问答应用不支持上传 `.exe`、`.dll` 等可执行文件，且单文件大小上限为 100 MB；
- Agent 1.0 已进入维护期，新项目应优先选用 Agent 2.0；二者在工具调用协议与错误码定义上存在不兼容，迁移前需验证业务逻辑；
- 所有应用的并发调用数默认上限为 10 QPS，如需提升，请提交工单申请配额调整。

## 来源文档

- [应用开发](../../raw/application-user-guide/llm-application.md)


