# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，支持无需编码即可赋予智能体文件处理、数据分析等专业功能。通过语义匹配 description 字段，智能体可在对话中自动识别任务意图并调用对应 Skill 执行；官方 Skill 开箱即用，自定义 Skill 则通过 ZIP 包上传实现业务定制。详细背景与设计目标见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **官方 Skill**：由平台预置并统一维护，覆盖常见文件处理场景（如 `.xlsx`/`.csv` 解析、PDF 文本提取、图像 OCR 等），添加后立即生效，版本更新自动同步至已绑定的智能体应用。
- **自定义 Skill**：用户通过符合规范的 ZIP 包（含 `SKILL.md`）上传创建，适用于行业专属逻辑（如医疗报告结构化解析、金融对账单校验等）。其行为完全由 `SKILL.md` 中的 `description` 定义驱动，不依赖底层模型选型——即 Skill 本身无“模型绑定”概念，调用时由智能体主模型（如 Qwen-Max）负责意图识别与编排，实际执行由 Skill 内部封装的工具链完成。该机制说明详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

> **注意**：文档中未提及 Skill 对特定大模型版本（如 Qwen2-72B）存在兼容性限制，但实践中若 `description` 描述模糊或触发条件过宽，可能导致低版本模型调用准确率下降。建议在 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 的描述编写建议基础上，针对所用主模型做 A/B 测试验证。

## 关键参数

所有 Skill 的核心配置均集中于 ZIP 包根目录下的 `SKILL.md` 文件，其 YAML frontmatter 必须包含以下字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | Skill 唯一标识符，仅支持小写字母、数字和连字符（如 `invoice-parser`），同一账号下不可重复。 |
| `description` | 是 | **决定调用准确性的关键字段**：需明确输入类型、支持操作、典型触发关键词及明确排除的场景。长度建议 200–500 字，避免模糊表述（如“处理数据”应改为“清洗含缺失值和异常值的 CSV 表格，并输出标准化 .xlsx”）。 |

ZIP 包本身需满足：总大小 ≤ 10 MB；必须包含且仅包含一个 `SKILL.md`（位于根目录）；禁止嵌套子目录存放 `SKILL.md`。

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面查看并添加。  
   - 自定义 Skill：按规范编写 `SKILL.md` → 打包为 ZIP → 在控制台「组件 > Skill 管理 > 自定义 Skill」上传，系统自动审查（约 2 分钟）。

2. **绑定到智能体**  
   - 方式一：从 Skill 详情页点击「添加到智能体」，选择目标应用。  
   - 方式二：进入智能体「应用配置」→「技能」区域 → 点击「+」→ 从列表勾选。

3. **测试与验证**  
   在应用配置页右侧对话窗格中发送典型用户指令（如 `把附件里的销售报表按季度汇总成图表`），观察是否触发预期 Skill 并返回正确结果。

## 限制和注意事项

- **版本管理**：官方 Skill 版本由平台控制，已绑定应用自动升级；自定义 Skill 更新需重新上传同名 ZIP 包，旧版本仍保留在历史记录中，但新调用默认使用最新版。
- **审查失败常见原因**：`SKILL.md` 缺失或格式错误（如 YAML 未用 `---` 包裹）、`name` 重复、ZIP 超出 10 MB、`description` 为空或纯符号（如 `---` 后无内容）。
- **调用可靠性依赖 description 质量**：智能体不解析 Skill 内部代码，仅依据 `description` 语义匹配用户输入。若描述未覆盖真实用户表达（如忽略口语化说法“那个表格”），将导致漏触发；若未明确排除边界场景（如“生成 PPT”误触发 xlsx Skill），则引发误调用。
- **调试建议**：首次上线前，务必使用多样化测试语句（含否定句、多跳指令、简写/错别字）验证 `description` 鲁棒性，并参考 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的完整示例进行对标优化。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


