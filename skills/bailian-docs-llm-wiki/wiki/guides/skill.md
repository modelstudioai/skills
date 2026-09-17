# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，支持无需编码即可让智能体自动识别并执行文件处理、数据分析等专业任务。官方 Skill 由平台预置并统一维护，自定义 Skill 则通过符合规范的 ZIP 包上传实现业务定制。其核心机制依赖 `SKILL.md` 中的语义描述驱动智能体调用决策，而非硬编码规则。

## 支持的模型/功能

- **适用模型**：所有支持 Skill 调用的百炼智能体模型（当前为 Qwen 系列大模型，具体以 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中“添加 Skill 到智能体”章节说明为准）。
- **核心功能**：
  - 自动识别用户意图与 Skill 描述匹配度，触发调用；
  - 支持文件输入/输出（如 `.xlsx`, `.csv`, `.pdf` 等格式解析与生成）；
  - 官方 Skill 覆盖通用办公文档、表格、文本处理场景；自定义 Skill 可扩展至行业专用格式（如医疗 DICOM 元数据提取、金融 SWIFT 报文解析等）。

> **注意**：原始文档未明确列出支持的模型列表，仅说明“所有智能体应用均可添加”，但实际调用能力取决于底层模型是否启用 Skill 执行[插件](../concepts/plugin.md)。请以控制台技能管理页的可用性状态及 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中测试流程为准。

## 关键参数

关键参数全部定义在 ZIP 包根目录的 `SKILL.md` 文件 YAML frontmatter 中：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | Skill 唯一标识符，需全局唯一（同账号下），建议小写+连字符（如 `pdf-summarizer`）；不支持空格或特殊字符。 |
| `description` | 是 | **决定调用准确性的核心字段**，必须包含：输入类型、支持操作、典型触发关键词、明确的不适用边界（详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中“description 编写建议”）。 |

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面点击“添加到智能体”；  
   - 自定义 Skill：按规范编写 `SKILL.md`，打包为 ZIP（≤10 MB），在“自定义 Skill”标签页上传。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击“添加到智能体”，选择目标应用；  
   - 方式二：进入智能体“应用配置” → “技能”区域 → 点击 `+` 号选择 Skill。

3. **测试效果**  
   在应用配置页右侧对话窗格输入典型用户指令（如“把附件里的 CSV 按销售额排序并导出为 Excel”），观察是否触发 Skill 并返回预期文件。

## 限制和注意事项

- **大小限制**：ZIP 包总大小 ≤ 10 MB，超限将导致审查失败；
- **版本更新**：重新上传同名 ZIP 即创建新版本，已接入该 Skill 的智能体会**自动切换至最新版**（官方 Skill 强制更新，自定义 Skill 需手动重传）；
- **description 质量强相关**：若描述模糊（如仅写“处理表格”），会导致误触发或漏触发——务必遵循 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 提供的完整示例结构；
- **调试提示**：审查失败时，错误信息仅提示“SKILL.md 格式错误”或“name 冲突”，需检查 YAML 语法、字段缺失及名称唯一性；
- **安全约束**：自定义 Skill 运行于沙箱环境，无法访问外网、本地文件系统或执行任意 shell 命令。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


