# skill

Skill 是百炼平台中用于封装和复用 AI 能力的标准化单元，支持将大模型调用、工具集成、Prompt 编排等逻辑打包为可配置、可调试、可发布的服务接口。开发者可通过控制台或 API 管理 Skill 生命周期，并在应用中以统一方式调用。其设计目标是降低 AI 功能集成门槛，提升工程化复用效率。

## 支持的模型与功能

Skill 当前支持绑定以下模型类型：Qwen-Max、Qwen-Plus、Qwen-Turbo（含对应多模态版本），以及通过 `tool_call` 方式接入的自定义工具（如 HTTP 工具、数据库查询插件等）。Skill 内部可组合系统 Prompt、用户输入模板、输出解析规则及后处理函数。不支持直接部署非百炼托管的私有模型权重，相关能力请参考 [Skill](../../raw/application-user-guide/skill.md) 文档说明。

## 关键参数

创建或更新 Skill 时需配置以下核心字段：
- `name`：唯一标识符（仅限字母、数字、下划线，长度 ≤ 64）
- `description`：简要功能描述（≤ 512 字符）
- `model_id`：指定模型 ID（必须为当前项目已开通的模型）
- `prompt_template`：Jinja2 格式模板，支持 `{{ input }}`、`{{ history }}` 等上下文变量
- `output_schema`：可选 JSON Schema，用于结构化输出校验与自动解析  
详细字段约束见 [Skill](../../raw/application-user-guide/skill.md) 中“参数说明”章节。

## 使用方式

Skill 可通过三种方式调用：
1. **API 调用**：向 `/v1/skills/{skill_id}/invoke` 发送 POST 请求，携带 `input` 字段（字符串或对象）；
2. **SDK 调用**：使用 `alibabacloud_bailian20231229` SDK 的 `InvokeSkillRequest`；
3. **低代码集成**：在百炼应用画布中拖入 Skill 组件并绑定输入/输出节点。  
调用时若未显式传入 `model_id`，则默认使用 Skill 创建时绑定的模型；该行为与 [Skill](../../raw/application-user-guide/skill.md) 所述一致。

## 限制和注意事项

- 单个 Skill 最大 [Token](../concepts/token.md) 输入限制为 32768（受底层模型上下文窗口约束）；
- Skill 不支持跨项目共享，权限隔离以项目为边界；
- > **注意**：原始文档中提及“Skill 可继承父 Skill 的参数配置”，但该功能已于 v2.3.0 版本下线，实际行为以控制台最新 UI 和 [Skill](../../raw/application-user-guide/skill.md) 当前版本为准；
- 异步调用（`invoke_async`）暂不支持流式响应，需等待完整结果返回；
- 输出解析失败时（如 `output_schema` 校验不通过），默认返回原始模型输出而非抛出错误，建议在业务层增加容错处理。

## 来源文档

- [Skill](../../raw/application-user-guide/skill.md)


