# skill

skill 是百炼平台中用于封装和复用 AI 能力的标准化单元，支持将大模型调用、工具链、条件分支等逻辑打包为可配置、可编排、可共享的组件。开发者可通过控制台或 API 创建、调试和发布 skill，供工作流（Workflow）或其他 skill 调用。其设计目标是降低重复开发成本，提升能力复用率与交付一致性。

## 支持的模型与功能

skill 本身不绑定特定模型，但其内部节点（如 `llm_call`、`tool_call`）支持调用百炼平台当前全部公开模型，包括 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）、Qwen-VL、Qwen-Audio 等，以及已接入的第三方模型（如通过 Model Studio 接入的自定义模型）。技能可包含多步骤逻辑：LLM 推理、[函数调用](../concepts/function-calling.md)、变量赋值、条件判断（`if-else`）、循环（`for`）、HTTP 请求等。详细能力列表见 [Skill](../../raw/application-user-guide/skill.md)。

## 关键参数

- `name`（必填）：技能唯一标识符，仅支持小写字母、数字、下划线，长度 3–64 字符  
- `description`（可选）：简明功能说明，用于控制台展示与搜索  
- `input_schema`（可选）：JSON Schema 格式，定义输入参数结构与校验规则（如 `{"type": "object", "properties": {"query": {"type": "string"}}}`）  
- `output_schema`（可选）：同上，定义输出结构，影响下游节点类型推断  
- `timeout`（可选）：单位秒，默认 30，最大 300；超时后 skill 状态为 `failed`  

> **注意**：`input_schema` 和 `output_schema` 在 [Skill](../../raw/application-user-guide/skill.md) 中被标记为“推荐配置”，但实际在 API v2.1+ 中已变为强校验字段——若未提供且 skill 被 Workflow 引用，将触发 schema 不匹配错误。请以最新 API 文档为准。

## 使用方式

1. **创建**：通过控制台「技能中心」→「新建技能」，或调用 `POST /v2/skills` API  
2. **编辑**：在画布中拖入节点、连线、配置参数；支持实时调试（需填写测试输入）  
3. **发布**：点击「发布」生成 `published_version`，仅已发布版本可被 Workflow 或其他 skill 调用  
4. **调用**：  
   - 控制台内：在 Workflow 编辑器中搜索并拖入 skill 节点  
   - API：通过 `POST /v2/skills/{skill_id}/invoke`，传入 `input` JSON 对象  
   - SDK：使用 `BailianClient.invoke_skill()` 方法（Python SDK v1.3.0+）  
   完整调用示例参见 [Skill](../../raw/application-user-guide/skill.md)。

## 限制和注意事项

- 单个 skill 最多包含 100 个节点，总执行时间（含所有子调用）不得超过 `timeout` 设置值  
- 不支持跨项目（project）直接引用 skill；如需共享，须导出为 `.skill.json` 文件后导入目标项目  
- skill 内部不可递归调用自身（即禁止 A → A），但允许间接循环（A → B → A），此时需自行处理终止条件，否则可能触发平台级超时中断  
- 所有敏感参数（如 API Key、数据库密码）必须通过「密钥管理」注入，禁止硬编码；密钥引用语法为 `{{secrets.MY_API_KEY}}`，该机制在 [Skill](../../raw/application-user-guide/skill.md) 中有明确说明。

## 来源文档

- [Skill](../../raw/application-user-guide/skill.md)


