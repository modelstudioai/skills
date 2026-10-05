# skill

Skill 是百炼平台提供的可插拔能力包，用于扩展智能体在对话中自动处理特定任务（如文件解析、数据清洗等）的能力，无需额外编码或外部工具集成。开发者可通过添加官方 Skill 或上传自定义 ZIP 技能包快速赋予智能体专业功能。Skill 的调用由智能体根据 `SKILL.md` 中的 `description` 自动决策，其准确性高度依赖描述的完整性与精确性。

## 支持的模型/功能

Skill 本身不绑定特定大模型，而是作为独立能力模块被智能体（无论底层使用 Qwen 系列或其他支持模型）在推理过程中动态调用。当前支持两类 Skill：  
- **官方 Skill**：平台预置并持续更新的通用能力，如 `xlsx`、`pdf-parser`、`csv-cleaner` 等，覆盖主流文件格式处理与基础数据分析场景，详情见 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面；  
- **自定义 Skill**：通过符合规范的 ZIP 包上传创建，适用于行业定制需求（如医疗报告结构化解析、ERP 导出文件转换等），其行为完全由 `SKILL.md` 定义，详见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

> **注意**：官方 Skill 的具体列表和能力边界以控制台实时展示为准，文档中列举的示例（如 `xlsx`）仅作说明用途，实际可用 Skill 可能因平台版本更新而增减，请始终以 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中指引的控制台页面为准。

## 关键参数

自定义 Skill 的核心元信息全部定义在 ZIP 包根目录的 `SKILL.md` 文件中，采用 YAML frontmatter 格式，必填字段如下：  
- `name`：唯一标识符，须为小写英文+连字符（如 `invoice-parser`），不可与当前账号下已有 Skill 名称重复；  
- `description`：**最关键字段**，直接影响智能体是否触发该 Skill。必须明确说明适用输入类型、支持操作、典型触发关键词及明确排除的不适用场景（例如：“Do NOT trigger when the primary deliverable is a Word document…”），详见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的完整示例。

## 使用方式

1. **创建 Skill**：  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面点击“添加到智能体”；  
   - 自定义 Skill：按规范编写 `SKILL.md`，打包为 ≤10 MB 的 ZIP，通过控制台 **组件 > Skill 管理 > 自定义 Skill > 上传** 提交，系统自动审查（约 2 分钟）。  

2. **添加到智能体**：  
   - 方式一：从 Skill 详情页点击“添加到智能体”，选择目标应用；  
   - 方式二：进入智能体 **应用配置 > 技能** 区域，点击“+”号从列表选取。  

3. **测试与验证**：在应用配置页右侧对话窗格中发送符合 `description` 触发条件的指令（如“把附件里的 csv 按销售额排序并导出新表格”），观察 Skill 是否被正确调用及输出是否符合预期。

## 限制和注意事项

- ZIP 包总大小严格限制为 ≤10 MB，超限将导致上传失败；  
- `name` 字段在账号维度全局唯一，重名上传会触发版本更新而非新建；  
- 自定义 Skill 更新需重新上传 ZIP 包，已添加该 Skill 的智能体会**自动切换至最新通过审查的版本**（无须手动重新配置）；  
- 官方 Skill 的更新由平台统一推送，用户无法修改其 `description` 或逻辑，但可随时在控制台查看变更记录；  
- `description` 缺失、模糊或未明确排除边界场景，将显著增加误触发概率——强烈建议严格遵循 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的编写建议，尤其包含“不适用场景”条款。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


