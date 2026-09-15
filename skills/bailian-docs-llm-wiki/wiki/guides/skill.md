# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，支持无需编码即可让智能体自动识别并执行文件处理、数据分析等专业任务。Skill 分为平台预置的官方 Skill 和用户自主开发的自定义 Skill 两类，均通过语义描述驱动调用决策。其核心机制依赖于 `SKILL.md` 中的高质量 description 字段，直接影响智能体调用的准确性与鲁棒性，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **官方 Skill**：由百炼统一维护，覆盖常见文件处理场景（如 `.xlsx`、`.csv` 解析与生成、PDF 文本提取、图像 OCR 等），开箱即用，无需配置。列表持续更新，可在控制台 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面实时查看。
- **自定义 Skill**：通过上传符合规范的 ZIP 包实现，适用于行业专属逻辑（如医疗报告结构化解析、金融票据字段抽取）。其行为完全由 `SKILL.md` 中的 `description` 定义，智能体据此匹配用户意图——该设计使 Skill 功能不绑定具体模型或代码实现，而是聚焦于“能做什么”和“何时触发”，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

> **注意**：当前所有 Skill（含官方与自定义）均**不支持直接调用大语言模型生成代码或执行任意 Python 脚本**；其能力边界严格限定在 `description` 所声明的输入类型、操作范围及输出格式内。超出描述范围的请求将被智能体主动拒绝，而非降级执行。

## 关键参数

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `name` | 是 | string | Skill 唯一标识符，仅限小写字母、数字和连字符（如 `invoice-parser`），同一账号下不可重复。 |
| `description` | 是 | string | **决定调用准确性的核心字段**。需明确包含：① 支持的输入格式（如 `.pdf`, `base64 image`）；② 可执行操作（如“提取表格”、“识别手写文字”）；③ 典型触发关键词（如“转成 Excel”、“把发票信息列出来”）；④ 明确排除场景（如“不处理扫描件模糊的 PDF”）。示例见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的 xlsx Skill 描述。 |

## 使用方式

1. **创建自定义 Skill**  
   - 编写符合规范的 `SKILL.md`（YAML frontmatter，`---` 包裹），确保 `name` 和 `description` 准确完整；  
   - 将 `SKILL.md` 及相关代码/资源打包为 ZIP（≤10 MB），根目录无嵌套文件夹；  
   - 在控制台 **组件 > Skill 管理 > 自定义 Skill > 上传**，等待约 2 分钟自动审查。

2. **添加到智能体**  
   - 方式一：在 Skill 详情页点击 **添加到智能体**，选择目标应用；  
   - 方式二：进入智能体 **应用配置 > 技能** 区域，点击 `+` 号从列表选取；  
   - 添加后，智能体在对话中自动匹配 `description` 并调用，无需额外提示词或[函数调用](../concepts/function-calling.md)配置。

3. **测试与验证**  
   - 在应用配置页右侧对话窗格中发送典型请求（如 `把这张截图里的表格转成 CSV`），观察是否触发对应 Skill 并返回预期结果（如下载链接）。

## 限制和注意事项

- **版本管理**：官方 Skill 更新后，已添加的应用**自动生效最新版本**；自定义 Skill 需重新上传同名 ZIP 包以创建新版本，旧版本仍保留在历史记录中，但新对话默认使用最新版。
- **大小与结构**：ZIP 包必须包含且仅在根目录包含 `SKILL.md`，总大小 ≤10 MB；任何结构错误（如 `SKILL.md` 缺失、路径错误、YAML 格式非法）将导致审查失败。
- **调用可靠性**：`description` 描述越精确、覆盖边界越清晰，误触发率越低。避免使用模糊表述（如“处理文档”），应具体到格式、动作和约束（如“仅处理带表头的 UTF-8 编码 CSV，输出清洗后数据，不修改原始列顺序”）。
- **调试建议**：若 Skill 未被调用，优先检查 `description` 是否遗漏关键触发词或错误包含了排除场景；可通过控制台 **Skill 详情页 > 更新记录** 对比版本差异，确认 `description` 修改已生效。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


