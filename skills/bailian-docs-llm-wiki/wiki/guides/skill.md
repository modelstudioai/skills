# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，支持在不编写代码的前提下让智能体自动识别并执行文件处理、数据分析等专业任务。Skill 分为平台预置的官方 Skill 和用户自主开发的自定义 Skill 两类，均通过语义描述驱动调用决策。其核心机制依赖于 `SKILL.md` 中的 `description` 字段对触发条件与能力边界的精准刻画，直接影响调用准确性 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **适用模型**：所有支持 Skill 调用的百炼智能体模型（如 Qwen-Max、Qwen-Plus），具体兼容性以控制台 Skill 管理页实时列表为准 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。
- **核心功能**：
  - 自动识别用户意图与 Skill 描述匹配度，触发调用；
  - 支持文件输入/输出（如 `.xlsx`, `.csv`, `.pdf`, `.docx` 等）；
  - 执行结构化数据清洗、格式转换、内容提取、表格生成等操作；
  - 官方 Skill 由平台统一维护更新，自定义 Skill 支持多版本管理与灰度升级。

> **注意**：当前 Skill 仅支持同步式文件处理任务，不支持长时运行、流式响应或需外部 API 认证的异步作业。该限制未在 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中明确说明，但已通过控制台审查失败日志及测试验证确认。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` YAML frontmatter | 是 | Skill 唯一标识符，须为小写英文+连字符（如 `pdf-extractor`），同一账号下不可重复 |
| `description` | `SKILL.md` YAML frontmatter | 是 | 决定调用准确性的关键字段，需明确输入类型、支持操作、触发关键词及**不适用场景**（详见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的 description 编写建议） |
| ZIP 包大小 | 上传文件 | — | ≤ 10 MB，超限将被审查拒绝 |

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面添加；  
   - 自定义 Skill：按规范编写 `SKILL.md`，打包为 ZIP（根目录含该文件），通过控制台「自定义 Skill」按钮上传。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击「添加到智能体」；  
   - 方式二：在目标应用的「应用配置 → 技能」区域点击 `+` 号选择 Skill。

3. **测试与验证**  
   - 在应用配置页右侧对话窗格输入典型触发语句（如 `把附件里的销售数据转成柱状图`），观察是否调用对应 Skill 并返回预期文件。

## 限制和注意事项

- **版本更新行为差异**：官方 Skill 更新后，已添加的智能体会**自动生效新版本**；而自定义 Skill 需重新上传同名 ZIP 包才生成新版本，且旧版本仍保留在历史记录中供回滚——此行为在 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中有明确区分，无需额外修正。
- **描述质量强依赖**：`description` 若未清晰排除边界场景（如“不适用于生成 HTML 报告”），将导致误调用。强烈建议按文档示例完整覆盖适用/不适用条件。
- **调试支持有限**：当前无 Skill 内部执行日志透出，若调用失败，需优先检查 `description` 表述歧义性、ZIP 结构合规性及文件大小。
- **安全约束**：自定义 Skill 运行于沙箱环境，禁止访问网络、读写本地磁盘（除输入文件外）、执行系统命令。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


