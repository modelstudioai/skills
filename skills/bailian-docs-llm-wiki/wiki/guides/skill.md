# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，支持无需编码即可让智能体自动识别并执行特定类型任务（如文件解析、数据清洗、格式转换等）。官方 Skill 开箱即用，自定义 Skill 则通过 ZIP 包形式灵活适配业务场景。其核心机制依赖 `SKILL.md` 中的语义描述驱动智能体调用决策，而非硬编码规则。

## 支持的模型/功能

- **适用模型**：所有支持 Skill 调用的百炼智能体模型（当前为 Qwen 系列大模型，具体兼容性见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)）。
- **核心功能**：
  - 自动识别用户意图与 Skill 描述匹配度，触发调用；
  - 支持文件输入/输出（如 `.xlsx`, `.csv`, `.pdf` 等）；
  - 官方 Skill 覆盖通用文件处理场景（如表格操作、PDF 提取），自定义 Skill 可扩展至行业专属逻辑；
  - 版本化管理：官方 Skill 自动更新，自定义 Skill 通过同名 ZIP 重传实现版本迭代。

> **注意**：文档中未明确说明 Skill 是否支持流式响应或长上下文窗口下的多轮 Skill 协同调用；实际开发中需以 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的测试用例为准，避免假设跨 Skill 状态共享能力。

## 关键参数

关键参数均定义在 ZIP 包根目录的 `SKILL.md` 文件 YAML frontmatter 中：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | Skill 唯一标识符，仅限小写字母、数字和连字符（如 `invoice-parser`），不可与账号下已有 Skill 重名。 |
| `description` | 是 | 决定调用准确率的核心字段，必须包含：输入类型、支持操作、典型触发关键词、明确的不适用场景（详见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的完整示例）。 |

> **注意**：`description` 字段长度无显式限制，但过长可能导致模型理解偏差；建议控制在 500 字以内，并优先使用具体动词（如“提取表格”“合并列”）而非模糊表述（如“处理数据”）。

## 使用方式

1. **创建 Skill**：
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面添加；
   - 自定义 Skill：按规范编写 `SKILL.md`，打包为 ≤10 MB 的 ZIP，通过控制台「组件 > Skill 管理 > 自定义 Skill」上传。

2. **添加到智能体**：
   - 方式一：从 Skill 详情页点击「添加到智能体」；
   - 方式二：在目标应用的「应用配置 > 技能」区域点击 `+` 添加。

3. **验证效果**：
   - 在应用配置页右侧对话窗格中发送符合 `description` 触发条件的指令（如 `帮我清洗这个 CSV 文件中的空行和重复列`），观察是否生成预期文件输出。

## 限制和注意事项

- **大小限制**：ZIP 包总大小 ≤10 MB，超限将导致审查失败；
- **命名冲突**：同一账号下 `name` 字段全局唯一，重名上传会拒绝（非覆盖）；
- **审查耗时**：自定义 Skill 上传后需约 2 分钟自动审查，失败时需根据提示修改 `SKILL.md` 后重传；
- **版本生效**：自定义 Skill 更新后，已添加该 Skill 的智能体**立即**使用新版本（无需重启或重新发布）；
- **调用边界**：Skill 仅处理其 `description` 明确声明的输入类型和操作；超出范围（如要求生成 Python 脚本但 description 限定输出为 `.xlsx`）将被主动规避——此行为由模型推理层强制保障，非客户端可控。

> **注意**：当前 Skill 不支持运行时传入动态参数（如用户指定列名列表），所有行为均由 `description` 静态约束；若需参数化控制，应通过拆分多个 Skill 或在 `description` 中预设枚举值实现（参考 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中 xlsx Skill 对“按地区分列统计”的显式覆盖写法）。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


