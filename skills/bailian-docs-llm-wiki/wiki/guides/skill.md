# skill

skill 是百炼平台中用于封装和复用 AI 能力的可调用单元，支持将大模型能力、工具调用、[Prompt 工程](../concepts/prompt-engineering.md)或 API 集成逻辑打包为标准化接口。开发者可通过统一入口配置、调试与发布 skill，并在工作流（Workflow）或 API 服务中直接调用。其设计目标是降低重复开发成本，提升能力复用率与维护一致性。

## 支持的模型/功能

skill 支持绑定以下类型的能力：
- 百炼托管模型（如 Qwen-Max、Qwen-Plus、Qwen-Turbo）
- 自定义 Prompt 模板（含变量注入、输出 Schema 约束）
- 外部 HTTP API（需配置请求方法、Headers、Body 模板及响应解析规则）
- 内置工具（如时间查询、计算器、知识库检索等），具体可用工具列表见 [Skill](../../raw/application-user-guide/skill.md)  
- 多步编排能力（通过子 skill 组合实现复杂逻辑）

> **注意**：文档 [Skill](../../raw/application-user-guide/skill.md) 中提及“支持直接调用 DashScope SDK”，但当前 v2.3.0 平台版本已移除此能力，仅保留 HTTP API 和内置工具两类外部集成方式；请以控制台实际可选类型为准。

## 关键参数

创建或更新 skill 时需配置以下核心参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `name` | string | 是 | skill 唯一标识符（限小写字母、数字、短横线，长度 3–32） |
| `description` | string | 否 | 功能简述，用于控制台展示与搜索 |
| `type` | enum | 是 | 取值：`llm`（大模型）、`prompt`（模板）、`api`（HTTP）、`tool`（内置工具） |
| `config` | object | 是 | 根据 `type` 动态变化，例如 `llm.model_id`、`api.url`、`tool.name` 等 |
| `output_schema` | JSON Schema | 否 | 强制结构化输出，影响调用返回格式与校验 |

完整参数定义与示例详见 [Skill](../../raw/application-user-guide/skill.md)。

## 使用方式

1. **控制台操作**：进入「应用」→「Skill 管理」→ 创建新 Skill → 选择类型并填写配置 → 保存并发布  
2. **API 调用**：发布后通过 `/v1/skills/{skill_id}/invoke` 接口发起同步调用，需携带 `Authorization` 与 `X-DashScope-SSE: disable`（若禁用流式）  
3. **集成至 Workflow**：在 Workflow 编辑器中拖入「Skill 节点」，选择已发布的 skill 并传入 `input` 字段（JSON 对象）  
4. **调试建议**：首次调用前务必使用控制台「测试」功能验证输入/输出行为，尤其关注 `output_schema` 是否匹配实际返回 —— 此处常见错误可参考 [Skill](../../raw/application-user-guide/skill.md) 的调试章节。

## 限制和注意事项

- 单个 skill 最多绑定 1 个主能力（不支持同时挂载 LLM + API）  
- `api` 类型 skill 的超时默认为 15s，不可修改；`llm` 类型受所选模型自身 timeout 限制  
- skill 调用日志保留 7 天，审计日志需通过 SLS 单独配置  
- 发布状态变更（如从 `draft` 到 `published`）不触发自动版本快照，历史版本需手动导出备份  
- 所有 skill 输入均经平台统一清洗（过滤控制字符、截断超长字段），详细处理规则见 [Skill](../../raw/application-user-guide/skill.md)

## 来源文档

- [Skill](../../raw/application-user-guide/skill.md)


