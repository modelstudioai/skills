# llm application

`llm application` 是百炼平台提供的面向大语言模型应用的统一构建与部署能力，支持从低代码智能体到高代码定制化应用的全栈开发范式。开发者可通过可视化编排或代码集成方式快速创建生产级 LLM 应用，并复用平台提供的模型、工具、记忆与安全能力。该能力覆盖推理调用、状态管理、多轮交互等核心场景。

## 支持的模型与功能

- **应用类型**：支持五类应用形态：[新版智能体应用（Agent 2.0）](https://help.aliyun.com/zh/model-studio/new-single-agent-application)、[智能体应用（Agent 1.0）](https://help.aliyun.com/zh/model-studio/single-agent-application)、[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application)、[高代码应用](https://help.aliyun.com/zh/model-studio/rich-code-application) 和 [文件问答](https://help.aliyun.com/zh/model-studio/file-q-a)。  
- **模型接入**：默认支持百炼托管的 Qwen 系列（如 qwen-max、qwen-plus）、GLM 系列及第三方 API 模型（需配置凭证）。所有模型均通过 `model_id` 字符串标识，详见 [应用开发](../../raw/application-user-guide/llm-application.md) 文档。  
- **扩展能力**：内置工具调用（Function Calling）、RAG 检索增强、会话历史管理（`session_id` 驱动）、自定义 Prompt 模板及敏感词过滤策略。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，例如 `"qwen-max"`；取值范围见 [应用开发](../../raw/application-user-guide/llm-application.md) |
| `input` | object | 是 | 用户输入，结构为 `{ "query": "..." }`，支持可选 `files` 字段（仅文件问答类应用） |
| `parameters` | object | 否 | 推理参数，如 `temperature: 0.7`, `top_p: 0.9`, `max_tokens: 2048` |
| `session_id` | string | 否 | 用于多轮对话上下文维护；若未提供，系统生成临时 session |

> **注意**：`parameters` 中的 `stop` 字段在 Agent 2.0 应用中已被弃用，实际生效以应用后台配置为准；旧版文档中提及的 `stream` 参数需显式设为 `true` 才启用流式响应，但 [应用开发](../../raw/application-user-guide/llm-application.md) 未明确说明其默认行为，建议始终显式传入。

## 使用方式

1. **API 调用（推荐）**：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/llm-application \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model_id": "qwen-max",
           "input": {"query": "你好，请总结以下内容：..."},
           "parameters": {"temperature": 0.5}
         }'
   ```

2. **SDK 调用（Python）**：  
   ```python
   from dashscope import Application
   resp = Application.call(
       app_id='your-app-id',
       api_key='your-api-key',
       input={'query': '...'},
       parameters={'temperature': 0.5}
   )
   ```

3. **前端集成**：通过 `@alibaba/bailian-js-sdk` 初始化 `ApplicationClient` 实例，调用 `.run()` 方法（参考 [应用开发](../../raw/application-user-guide/llm-application.md) 中的 SDK 示例章节）。

## 限制和注意事项

- 单次请求 `input.query` 最长支持 32768 字符；文件问答类应用单次上传文件总大小 ≤ 100 MB（PDF/TXT/DOCX 等格式）。
- Agent 1.0 应用已进入维护期，新项目请优先使用 [新版智能体应用（Agent 2.0）](https://help.aliyun.com/zh/model-studio/new-single-agent-application)，其支持更完善的工具编排与错误恢复机制。
- 所有应用调用均受配额限制（QPS/TPM），具体阈值取决于所选模型与账号等级，详情参见控制台「配额管理」页面。
- 若使用自定义模型后端（如私有部署的 vLLM 服务），需确保其兼容 [OpenAI 兼容接口](../concepts/openai-compatibility.md)规范，否则可能触发解析失败——该兼容性要求未在 [应用开发](../../raw/application-user-guide/llm-application.md) 中明确说明，属隐式约束。

## 来源文档

- [应用开发](../../raw/application-user-guide/llm-application.md)


