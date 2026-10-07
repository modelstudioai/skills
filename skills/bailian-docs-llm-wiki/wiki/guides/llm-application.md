# llm application

`llm application` 是百炼平台提供的核心应用构建能力，用于将大语言模型能力封装为可部署、可调用的服务。它支持从低代码智能体到高代码自定义逻辑的多种应用形态，适用于对话交互、文档处理、自动化流程等场景。开发者可通过控制台或 OpenAPI 快速创建、调试和发布应用。

## 支持的模型与功能

- 支持接入平台托管的全部 LLM（如 Qwen 系列、Qwen2、Qwen3）、Embedding 模型及 Rerank 模型  
- 提供五类预置应用类型：[新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)、[智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)、[工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)、[高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md) 和 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)  
- 所有类型均支持 Prompt 编排、知识库绑定、插件调用（仅 Agent 2.0 及工作流应用）、流式响应与回调通知  

> **注意**：Agent 1.0 已进入维护期，新项目应优先使用 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)，其在工具调用稳定性、多轮上下文管理及错误恢复机制上均有显著增强。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 模型 ID（如 `qwen-max`, `qwen2-72b`），需与所选应用类型兼容 |
| `prompt_template` | string | 否 | 自定义系统 Prompt，长度 ≤ 8192 字符；若为空则使用应用模板默认值 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 SSE 流式响应 |
| `temperature` | number | 否 | 范围 `[0.0, 2.0]`，默认 `0.8`；Agent 类型建议 ≤ 1.0 以保障推理稳定性 |

## 使用方式

1. **控制台创建**：进入「应用开发」→「新建应用」→ 选择类型 → 配置模型、Prompt 与知识库 → 发布  
2. **OpenAPI 调用**：  
   - 创建应用：`POST /v1/applications`（需指定 `type` 字段，如 `"agent2"` 或 `"workflow"`）  
   - 调用应用：`POST /v1/applications/{app_id}/chat`，请求体含 `inputs`（用户输入）和 `user`（可选用户标识）  
3. **调试建议**：首次调用前务必通过控制台「测试」页验证基础响应；流式调用需正确处理 `data:` 前缀与 `event: message` 事件分隔符  

## 限制和注意事项

- 单次请求最大 token 数受所选模型 context length 限制（如 `qwen-max` 为 32768），实际可用量需扣除系统 Prompt 与历史消息开销  
- 文件问答应用仅支持上传 PDF、DOCX、TXT、PPTX、XLSX 格式，单文件 ≤ 50MB；解析结果以文本块形式存入知识库，不保留原始格式  
- Agent 2.0 应用默认启用自动工具选择，但若 `tools` 列表为空或未配置有效插件，则降级为纯 LLM 推理 —— 此行为与 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md) 的显式节点编排逻辑存在范式差异，请按业务确定性要求选型  
- 所有应用默认开启敏感词过滤（基于平台统一策略），不可关闭；如需绕过，须提交白名单申请并经安全审核

## 来源文档

- [应用开发](../../raw/application-user-guide/llm-application.md)


