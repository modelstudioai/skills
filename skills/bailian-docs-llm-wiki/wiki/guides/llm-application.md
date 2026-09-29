# llm application

`llm application` 是百炼平台提供的核心能力，用于将大语言模型封装为可部署、可调用的生产级应用。它支持多种交互范式（如智能体、工作流、文件问答等），开发者可通过配置或代码方式快速构建定制化 AI 应用。该能力基于统一的应用抽象层，兼顾低代码灵活性与高代码可控性。

## 支持的模型与功能

- 支持所有已接入百炼平台的 LLM 模型（包括 Qwen 系列、Baichuan、GLM 等），具体可用模型列表见 [应用开发](../../raw/application-user-guide/llm-application.md) 中的“模型兼容性说明”章节。
- 提供四类预置应用类型：**智能体应用（Agent 2.0）**（推荐新项目使用）、**工作流应用**（支持多节点编排）、**高代码应用**（完全自定义推理逻辑）、**文件问答**（基于上传文档的 RAG 场景）。
- Agent 1.0 已进入维护模式，不建议新项目采用；其能力已被 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 全面覆盖和增强。

## 关键参数

- `model_id`: 必填，指定底层 LLM（如 `qwen-max`, `qwen-plus`），需与应用类型兼容。
- `prompt_template`: 可选，用于覆盖默认系统提示；在工作流和高代码应用中支持 Jinja2 语法。
- `retrieval_config`: 仅文件问答和部分 Agent 场景生效，控制向量检索范围与重排序策略。
- `stream`: 布尔值，启用流式响应（默认 `true`），影响返回格式与客户端处理逻辑。
- > **注意**：`temperature` 和 `top_p` 在 Agent 2.0 中默认由平台自动管理，若显式设置可能被忽略——详见 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 的“参数覆盖规则”。

## 使用方式

1. **低代码方式**：在控制台「应用开发」页选择模板 → 配置模型与提示词 → 发布 → 获取 API Endpoint。
2. **API 调用**：使用 `POST /v1/applications/{app_id}/chat`，请求体为 JSON 格式，含 `inputs`（用户输入）和可选 `user`（用户 ID）字段。
3. **SDK 调用**（Python 示例）：
   ```python
   from alibabacloud_bailian20231219 import models as bailian_models
   client = BailianClient(...)
   req = bailian_models.ChatRequest(app_id="app-xxx", inputs={"query": "你好"})
   resp = client.chat(req)
   ```
   完整参数与错误码参考 [应用开发](../../raw/application-user-guide/llm-application.md)。

## 限制与注意事项

- 单次请求最大 `inputs` 文本长度为 32768 字符（含上下文拼接后）；超长将触发截断并返回警告。
- 文件问答应用仅支持 `.pdf`, `.docx`, `.txt`, `.md` 四种格式，且单文件 ≤ 50MB；解析失败时不会抛出异常，而是静默跳过该文件。
- Agent 2.0 默认启用工具调用（Tool Calling）能力，但若未配置任何工具，则自动退化为普通对话模式——此行为与 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md) 不同，后者需显式关闭工具开关。

## 来源文档

- [应用开发](../../raw/application-user-guide/llm-application.md)


