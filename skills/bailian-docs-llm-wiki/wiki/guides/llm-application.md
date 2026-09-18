# llm application

`llm application` 是百炼平台提供的核心应用构建能力，支持开发者基于大语言模型快速创建可部署、可集成的 AI 应用。它抽象了模型调用、[提示工程](../concepts/prompt-engineering.md)、状态管理与输入输出处理等共性逻辑，覆盖从低代码智能体到高代码定制化场景。所有应用类型均通过统一 API 接口暴露服务，适用于 Web、App、Bot 等多端集成。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 LLM 模型（如 qwen-max、qwen-plus），不支持 BYOM（Bring Your Own Model）；模型选择需在应用创建时指定，运行时不可动态切换。  
- **应用类型**：包括新版智能体应用（Agent 2.0）、智能体应用（Agent 1.0）、工作流应用、高代码应用和文件问答五类，详见 [应用开发](../../raw/application-user-guide/llm-application.md)。其中 Agent 2.0 是推荐默认选项，具备更优的工具调用与多步推理能力；Agent 1.0 已进入维护模式，新项目不应选用。  
- **内置能力**：所有类型均原生支持上下文管理、历史会话保持、流式响应（`stream: true`）及结构化输出（`response_format`）。文件问答类型额外支持 PDF/DOCX/TXT 等格式解析与切片检索，其实现细节见 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，创建后生成，用于 API 调用路径 `/v1/applications/{app_id}/chat` |
| `inputs` | object | 否 | 用户输入变量映射，如 `{"query": "今天天气如何？", "location": "杭州"}`；字段名需与应用配置中定义的变量一致 |
| `user` | string | 否 | 用户标识符，用于会话隔离与审计追踪；若未提供，系统将生成临时 ID |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 SSE 流式响应，适用于前端实时渲染场景 |
| `response_format` | object | 否 | 指定输出 JSON Schema，触发模型结构化生成（需模型支持）；示例见 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md) |

> **注意**：`inputs` 中的键名必须严格匹配应用配置界面中定义的「输入变量名」，大小写敏感；文档 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md) 中提及的 `input_params` 字段已废弃，实际接口仅接受 `inputs` 对象。

## 使用方式

1. **创建应用**：在控制台「应用开发」页选择类型，完成模型、提示词、工具（如需）及输入变量配置；Agent 2.0 和工作流应用支持可视化编排。  
2. **获取凭证**：应用发布后，在详情页获取 `app_id` 及 API Key（需绑定有效 API 计费组）。  
3. **调用 API**：  
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/applications/{app_id}/chat" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"inputs":{"query":"解释量子纠缠"},"stream":true}'
   ```
   响应体结构与标准 LLM Chat API 兼容，便于迁移。

## 限制和注意事项

- 单次请求最大 `inputs` 总长度为 100 KB；文件问答类应用单次上传文件总大小 ≤ 50 MB（PDF 解析后文本上限 200 万字符）。  
- Agent 2.0 应用默认启用自动工具调用，但若 `inputs` 中包含敏感字段（如 `api_key`），需在应用配置中显式标记为「不参与工具参数注入」，否则存在泄露风险。  
- 所有应用均不支持跨区域调用：`app_id` 仅在其创建时所属地域（如 `cn-beijing`）的 API Endpoint 有效；该约束在 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md) 文档中未明确说明，但实测验证成立。  
- 调试阶段建议开启 `debug: true`（非公开参数，仅控制台调试面板可用），可查看中间步骤日志；生产环境禁用。

## 来源文档

- [应用开发](../../raw/application-user-guide/llm-application.md)


