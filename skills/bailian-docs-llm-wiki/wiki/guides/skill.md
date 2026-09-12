# skill

skill 是百炼平台中用于封装和复用 AI 能力的标准化单元，支持将大模型调用、工具链、条件分支等逻辑打包为可配置、可编排、可共享的组件。开发者可通过控制台或 API 创建、调试和发布 skill，供工作流（Workflow）或其他 skill 调用。其设计目标是降低重复开发成本，提升能力复用率与维护一致性。

## 支持的模型与功能

skill 本身不绑定特定模型，但其内部节点（如 `llm_call`、`tool_call`）依赖所选模型的能力。当前支持在 skill 中调用 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）、Baichuan、GLM 等主流开源及百炼托管模型；部分高级功能（如多步推理、结构化输出约束）需模型具备相应 [prompt](prompt.md) 工程兼容性。工具调用（function calling）能力仅对明确声明 `tools` schema 的 skill 生效，且要求底层模型支持 OpenAI-style tool specification —— 具体兼容性请参考 [Skill](../../raw/application-user-guide/skill.md) 文档说明。

## 关键参数

- `name`：必填，skill 唯一标识符（仅限小写字母、数字、短横线，长度 ≤ 64）
- `description`：选填，用于控制台展示与搜索，建议简明描述用途
- `input_schema`：JSON Schema 格式，定义输入字段类型、必填项与默认值（若未提供则默认接受任意 object）
- `output_schema`：JSON Schema 格式，声明期望输出结构，影响 workflow 中下游节点的类型推导
- `timeout_ms`：超时时间，默认 30000（30 秒），最大支持 300000（5 分钟）

> **注意**：`input_schema` 和 `output_schema` 在旧版 skill 编辑器中曾允许留空并隐式 fallback 为 `{"type": "object"}`，但自 v2.3.0 起，API 创建时若缺失 `input_schema` 将直接报错 —— 详见 [Skill](../../raw/application-user-guide/skill.md) 的“参数校验规则”章节。

## 使用方式

1. **创建**：通过控制台「应用开发 → Skill」新建，或调用 `POST /v1/skills` API  
2. **调试**：在控制台编辑页点击「测试」，输入符合 `input_schema` 的 JSON 示例，实时查看执行日志与输出  
3. **调用**：在 Workflow 中添加 `skill_call` 节点，填写 skill ID 并传入参数；或通过 `POST /v1/skills/{skill_id}/invoke` 直接调用  
4. **版本管理**：每次保存即生成新版本（v1, v2...），发布后方可被其他应用引用；历史版本不可修改，仅可下线 —— 完整生命周期说明见 [Skill](../../raw/application-user-guide/skill.md)

## 限制和注意事项

- 单个 skill 最多包含 100 个节点（含条件分支、循环、子 skill 调用等）
- 输入总大小（序列化后 JSON 字符串）不得超过 2MB；输出同理
- 不支持跨 workspace 调用 skill，调用方与被调用方必须归属同一工作空间
- skill 内部不可嵌套调用自身（防止无限递归），运行时会主动检测并终止
- 若 skill 中使用了已下线的模型或工具，调用将失败，错误码为 `MODEL_NOT_FOUND` 或 `TOOL_NOT_AVAILABLE` —— 建议定期检查依赖项状态，参见 [Skill](../../raw/application-user-guide/skill.md) 的“依赖管理”小节

## 来源文档

- [Skill](../../raw/application-user-guide/skill.md)



