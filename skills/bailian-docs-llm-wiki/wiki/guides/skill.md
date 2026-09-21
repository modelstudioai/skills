# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔功能单元，支持无需编码即可为智能体赋予文件处理、数据分析等专业能力。它通过语义匹配自动触发，由官方预置 Skill 和用户自定义 ZIP 技能包两类构成。开发者可通过控制台完成 Skill 的创建、添加与版本管理，其行为高度依赖 `SKILL.md` 中的描述质量与格式规范。

## 支持的模型/功能

- **官方 Skill**：平台预置并统一维护的通用能力，如 `xlsx`、`pdf`、`csv` 等文件处理 Skill，开箱即用，无需配置，且已添加到智能体的实例会自动升级至最新版本。最新列表请参考 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面。
- **自定义 Skill**：通过上传符合规范的 ZIP 包创建，适用于行业定制场景（如发票解析、专有格式转换）。ZIP 包必须包含根目录下的 `SKILL.md` 文件，并满足命名唯一性、10 MB 大小限制等要求。详情见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 关键参数

核心参数均定义于 ZIP 包内的 `SKILL.md` 文件 YAML frontmatter 中：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | Skill 唯一标识符，仅限小写字母、数字和连字符（如 `invoice-parser`），不可与当前账号下已有 Skill 重名。 |
| `description` | 是 | 决定智能体是否调用该 Skill 的关键字段，需明确输入类型、支持操作、触发关键词及**不适用场景**。描述模糊将导致误触发或漏触发。 |

> **注意**：`description` 不是简单功能说明，而是面向模型的“调用策略说明书”。例如官方 `xlsx` Skill 的完整示例已在 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中给出，其明确排除了产出 Word/HTML/Python 脚本等非表格文件的场景——此约束直接影响调用准确性，不可省略。

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面选择添加；  
   - 自定义 Skill：按规范编写 `SKILL.md`，打包 ZIP 后在控制台 **组件 > Skill 管理 > 自定义 Skill** 中上传。系统审查约 2 分钟，失败时需根据提示修改后重传。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击 **添加到智能体**，选择目标应用；  
   - 方式二：在目标智能体的 **应用配置 > 技能** 区域点击 `+` 号选取 Skill。  
   添加后，智能体在对话中依据 `description` 语义自动识别并调用，无需额外代码集成。

3. **更新与测试**  
   - 更新自定义 Skill：重新上传同名 ZIP 包，审查通过后所有已引用该 Skill 的智能体自动切换至新版本；  
   - 测试效果：在应用配置页右侧对话窗格中发送典型请求（如 `帮我创建一个包含本月销售数据的表格`），观察是否正确触发并返回预期文件。该流程说明详见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 限制和注意事项

- **大小限制**：ZIP 包总大小 ≤ 10 MB，超限将导致上传失败；
- **名称冲突**：同一账号下 `name` 字段全局唯一，重复上传同名包将触发版本更新而非新建；
- **描述质量强依赖**：`description` 缺失“不适用场景”或触发关键词模糊，会导致高误触发率，建议严格参照官方示例撰写；
- **版本可见性**：官方 Skill 的历史版本不可查看；自定义 Skill 在详情页的 **概览** 标签中支持版本切换，**更新记录** 标签展示全部变更日志；
- **审查机制**：ZIP 包上传后需经平台自动化审查（校验 `SKILL.md` 存在性、YAML 格式、字段完整性等），审查失败需按提示修正后重传。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


