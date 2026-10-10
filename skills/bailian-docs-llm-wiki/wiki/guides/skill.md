# skill

`skill` 是百炼平台中用于封装和复用特定任务逻辑的可调用单元，支持以函数式接口被工作流或 API 调用。它可绑定模型、提示词、工具链及后处理逻辑，实现端到端任务抽象（如“提取合同关键条款”“生成合规摘要”）。每个 skill 具有唯一 ID 和版本管理，适用于低代码编排与高代码集成两种场景。

## 支持的模型与功能

- 支持绑定 Qwen 系列大模型（Qwen1.5、Qwen2、Qwen2.5）及部分第三方模型（需开通白名单）；
- 支持内置工具调用（如 HTTP 请求、数据库查询、知识库检索），也可通过 `tool_call` 协议接入自定义工具；
- 支持结构化输出（JSON Schema 约束）、流式响应、异步执行模式；
- 多模态能力暂未开放，文本类 skill 为当前唯一稳定支持类型。  
> **注意**：文档 [Skill](raw/application-user-guide/skill.md) 中提及“支持图像理解 skill”，但该能力尚未上线生产环境，实际使用请以 [introduction-to-skill.md](../../raw/application-user-guide/skill/introduction-to-skill.md) 的当前描述为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `skill_id` | string | 是 | 平台分配的唯一标识，格式如 `sk-abc123` |
| `version` | string | 否 | 默认为 `latest`；指定版本号（如 `v1.2.0`）可确保行为确定性 |
| `input` | object | 是 | 符合 skill 定义的 JSON Schema 的输入对象，字段名与 schema 严格匹配 |
| `stream` | boolean | 否 | `true` 时返回 SSE 流；默认 `false` |
| `timeout` | integer | 否 | 单位秒，范围 `5–300`；超时将中断执行并返回 `504` |

## 使用方式

1. **API 调用**（推荐）：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/skills/{skill_id} \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"input": {"text": "请总结以下会议纪要..."}, "stream": false}'
   ```

2. **工作流内嵌入**：在百炼控制台「工作流编排」中拖入 Skill 节点，配置 `skill_id` 与输入映射；支持上游节点输出自动绑定至 `input` 字段。  
3. **SDK 调用**（Python）：  
   ```python
   from dashscope import Skill
   resp = Skill.call(skill_id='sk-xxx', input={'text': '...'})
   ```

详细协议规范见 [introduction-to-skill.md](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 限制和注意事项

- 单次请求 `input` 总大小 ≤ 1MB；超出将返回 `413 Payload Too Large`；
- 每个 skill 最多绑定 5 个工具；工具间调用深度限制为 3 层（含主 skill 自身）；
- `version` 若指定为不存在的版本号，将返回 `404 Not Found`，**不会自动 fallback 到 latest**；
- 异步执行（`async=True`）需配合 `/result` 接口轮询，详见 [introduction-to-skill.md](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 来源文档

- [Skill](../../raw/application-user-guide/skill.md)


