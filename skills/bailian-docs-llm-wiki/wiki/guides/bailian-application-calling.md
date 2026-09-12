# bailian application calling

百炼平台支持通过 API 方式调用已发布的智能体（Agent）应用和工作流（Workflow）应用，适用于集成到自有系统或自动化流程中。调用过程需使用应用 ID、认证凭证及可选的输入参数，返回结构化响应结果。所有调用均基于 HTTPS 协议，遵循 RESTful 设计规范。

## 支持的模型/功能

- **智能体应用**：支持单步推理型 Agent，适用于问答、摘要、代码生成等任务；调用时自动加载其绑定的模型与提示词配置。  
- **工作流应用**：支持多节点编排型 Workflow，可串联多个模型调用、条件分支与外部工具；执行逻辑由工作流定义决定。  
- 两类应用均支持参数透传（如 `user_id`、`session_id`、自定义上下文字段），详见 [应用的参数传递](../../raw/application-user-guide/bailian-application-calling.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，可在控制台「应用管理」中获取 |
| `input` | object | 否 | 用户输入内容，结构需与应用定义的 input schema 一致；例如 `{ "query": "今天天气如何？" }` |
| `parameters` | object | 否 | 运行时覆盖参数，如 `temperature`、`max_tokens` 等，仅对底层模型生效（若应用未锁定参数）；具体可配项见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling.md) 和 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling.md) 文档说明 |

> **注意**：`parameters` 中设置的 `top_p`、`seed` 等参数在工作流应用中可能被节点级配置覆盖，实际生效以工作流定义为准；该行为与 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling.md) 中“参数优先级”章节描述一致，但与旧版文档中“全局参数强制生效”的说法存在冲突，以当前控制台发布版本逻辑为准。

## 使用方式

1. 获取应用 `app_id`（控制台 → 应用管理 → 查看详情）  
2. 构造 POST 请求，Endpoint 为 `https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/chat`  
3. 设置请求头：`Authorization: Bearer <api_key>`，`Content-Type: application/json`  
4. 请求体示例：
   ```json
   {
     "input": { "query": "解释量子纠缠" },
     "parameters": { "temperature": 0.3 }
   }
   ```
5. 解析响应中的 `output.text` 或 `output.choices[0].message.content` 字段（格式依应用类型略有差异）

## 限制和注意事项

- 单次调用最大输入长度为 32768 token（含系统提示与用户输入），超长将触发截断并返回警告；  
- 智能体应用默认启用会话状态保持（基于 `session_id`），工作流应用默认无状态，如需持久化上下文须自行管理 `session_id` 并透传；  
- 调用频率受 API Key 配额限制，超出将返回 `429 Too Many Requests`；详细配额策略参见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling.md)。

## 来源文档

- [应用调用](../../raw/application-user-guide/bailian-application-calling.md)


