# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，支持在不编写代码的前提下让智能体自动识别并执行文件处理、数据分析等专业任务。Skill 分为平台预置的官方 Skill 和用户自主开发的自定义 Skill 两类，均通过语义描述驱动调用决策。其核心机制依赖于 `SKILL.md` 中的 `description` 字段对触发条件与能力边界的精准刻画，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **适用模型**：Skill 当前仅支持接入基于百炼大模型（如 Qwen 系列）构建的智能体应用，不适用于纯规则引擎或非百炼托管的推理服务。
- **核心功能**：
  - 自动识别用户意图与输入数据类型（如 `.xlsx`、`.csv`、PDF 表格等），匹配对应 Skill；
  - 执行文件读取、清洗、转换、生成、格式化等操作；
  - 输出结构化文件（如 Excel、CSV）或中间数据供后续链路使用；
  - 官方 Skill 覆盖常见办公文档与表格场景；自定义 Skill 可扩展至行业专用格式（如医疗 DICOM 元数据提取、金融 SWIFT 报文解析等）。

> **注意**：原始文档中“支持的操作”示例未明确限定输出形式是否支持流式响应或分块处理。实际调用中，Skill 的执行结果必须为完整文件对象（如 `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`），不支持返回 JSON 片段或文本流——该限制在 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 的“完整示例”中隐含体现，但未在“要求”章节显式声明。

## 关键参数

所有 Skill 的行为由 `SKILL.md` 文件中的 YAML frontmatter 控制，关键字段如下：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | Skill 唯一标识符，需全小写+连字符（如 `pdf-table-extractor`），同一账号下不可重复。 |
| `description` | 是 | **决定调用准确性的核心字段**。必须包含：① 输入类型（如 `"PDF 文件含表格"`）；② 支持操作（如 `"提取所有表格并转为 CSV"`）；③ 触发关键词（如 `"提取表格"`、`"转成 Excel"`）；④ 明确排除场景（如 `"不处理扫描件或图片型 PDF"`）。描述质量直接影响智能体路由准确率，参见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中 xlsx 示例的完整写法。 |

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面添加，无需配置。  
   - 自定义 Skill：打包 ZIP（≤10 MB），根目录含合规 `SKILL.md`，通过控制台「组件 > Skill 管理 > 自定义 Skill」上传。系统审查约 2 分钟，失败时按提示修正 `description` 后重试。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击「添加到智能体」，选择目标应用；  
   - 方式二：进入智能体「应用配置」→「技能」区域，点击 `+` 选择 Skill。

3. **测试验证**  
   在应用配置页右侧对话窗格输入典型指令（如 `把附件里的销售报表按季度汇总并生成图表`），观察是否触发 Skill 并返回预期文件。

## 限制和注意事项

- **大小限制**：ZIP 包总大小 ≤ 10 MB；`SKILL.md` 中 `description` 建议控制在 500 字以内，过长可能导致语义解析偏差。
- **版本管理**：官方 Skill 自动更新，已添加的应用即时生效；自定义 Skill 更新需重新上传同名 ZIP，旧版本保留在「更新记录」中可回溯，但**不会自动切换**——已部署的应用仍使用原版本，需手动触发更新（当前控制台无强制刷新入口，需重新添加）。
- **调试建议**：若 Skill 未被调用，优先检查 `description` 是否遗漏关键触发词或误写了排除条件；可通过控制台「技能详情 > 概览」切换历史版本对比描述差异。
- **安全约束**：自定义 Skill 运行于沙箱环境，禁止访问外网、执行系统命令或读取非用户显式上传的文件。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


