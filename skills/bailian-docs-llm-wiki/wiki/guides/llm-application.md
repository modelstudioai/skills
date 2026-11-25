# llm application

`llm application` 是百炼平台提供的低代码/无代码 LLM 应用构建能力，支持通过可视化编排或配置化方式快速创建智能体（Agent）、工作流（Workflow）和文件问答等应用形态。开发者可基于预置组件（如 Prompt、插件、[工具调用](../concepts/tool-calling.md)）组合逻辑，无需从零编写推理服务。该能力面向生产级部署，提供统一的应用生命周期管理与调用接口。

## 支持的模型与功能

- **核心应用类型**：  
  - 新版智能体应用（Agent 2.0），支持多轮对话状态管理与自主工具选择；  
  - 工作流应用，支持 DAG 式节点编排（LLM 节点、条件分支、HTTP 请求、变量赋值等）；  
  - 文件问答应用，支持上传 PDF/Word/Excel 等文档并进行语义检索与摘要生成。  
- **扩展能力**：  
  - 可集成 [插件](../../raw/application-user-guide/llm-application.md) 实现外部系统调用（如数据库、CRM）；  
  - 支持自定义 [Prompt](../../raw/application-user-guide/llm-application.md) 模板与变量注入；  
  - 提供 [任务中心](../../raw/application-user-guide/llm-application.md) 查看异步执行日志与调试 trace。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，创建后由平台分配 |
| `input` | object | 是 | 用户输入，结构需与应用定义的 input schema 一致（如 `{ "query": "xxx", "file_ids": ["f123"] }`） |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 SSE 流式响应 |
| `trace_id` | string | 否 | 用于链路追踪，建议在调用方生成并透传 |

> **注意**：`input` 的 schema 定义以应用发布时的版本为准，若在 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application.md) 中修改了输入字段但未重新发布，调用将因 schema 校验失败而报错。

## 使用方式

1. **创建应用**：在控制台选择「应用」→「新建应用」→ 选择类型（Agent / Workflow / File QA）；  
2. **配置逻辑**：拖拽节点、设置 Prompt、绑定插件、定义输入/输出 Schema；  
3. **测试与发布**：使用内置调试器验证，通过 [应用发布与分享](../../raw/application-user-guide/llm-application.md) 完成上线；  
4. **调用接口**：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/chat \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"input": {"query": "你好"}, "stream": false}'
   ```

## 限制和注意事项

- 单次请求最大 `input` 大小为 2 MB；文件问答类应用单个上传文件上限为 100 MB；  
- 工作流中 LLM 节点最多嵌套 5 层，总 token 消耗（含 [prompt](prompt.md) + history + output）单次调用不超过 32k；  
- Agent 2.0 默认启用自动[工具调用](../concepts/tool-calling.md)，若禁用需在应用配置中关闭 `enable_auto_tool_call`，否则可能因插件权限缺失导致 fallback 失败；  
- 所有应用调用均受 [应用调用](../../raw/application-user-guide/llm-application.md) 文档中定义的 QPS 与并发数配额约束，超出将返回 `429 Too Many Requests`。

## 来源文档

- [Flow Agent](../../raw/application-user-guide/llm-application.md)


