# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，使智能体能在对话中自动识别并执行特定类型的任务（如文件解析、数据清洗、格式转换等），无需开发者编写集成代码或调用外部 API。Skill 分为平台预置的官方 Skill 和用户自主开发的自定义 Skill 两类，均通过语义描述驱动调用决策。其核心设计目标是降低专业能力接入门槛，同时保障调用准确性与可维护性。

## 支持的模型/功能

Skill 本身不依赖特定大模型，而是作为独立于 LLM 推理链之外的能力模块，在智能体运行时由系统根据用户输入和 Skill 的 `description` 描述动态路由调用。当前所有 Skill 均面向**文件处理与结构化数据操作**场景，包括但不限于：  
- 表格文件（`.xlsx`, `.csv`, `.tsv`, `.xlsm`）的读取、编辑、生成与格式转换；  
- PDF 文档的文本提取与基础结构解析；  
- 图像文件（`.png`, `.jpg`）的 OCR 与内容识别；  
- JSON/YAML 配置文件的校验与字段提取。  

> **注意**：原始文档 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中提及“支持数据分析”，但实际当前所有官方 Skill 均不提供统计建模、机器学习推理或数据库查询能力——该表述易引发误解，应以控制台中实时显示的 Skill 功能列表为准。

## 关键参数

Skill 的行为完全由其元信息文件 `SKILL.md` 中的 YAML 字段定义，关键参数如下：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 全局唯一标识符，仅允许小写字母、数字和连字符（如 `pdf-extractor`），不可与同账号下其他 Skill 冲突。 |
| `description` | 是 | **决定调用准确性的核心字段**，必须明确包含：输入类型（如 “.pdf 文件”）、支持操作（如 “提取全部文本及表格”）、典型触发词（如 “把PDF转成文字”、“提取发票信息”）、排除场景（如 “不处理扫描件模糊度 >30% 的文件”）。该字段直接影响 LLM 的路由判断，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的完整示例。 |
| `version` | 否 | 自定义 Skill 可选字段，用于显式标记版本；若未声明，系统按上传时间戳自动生成。 |

## 使用方式

1. **添加 Skill**：  
   - 在控制台 **组件 > Skill 管理** 页面，选择官方 Skill 卡片点击 **添加到智能体**；或进入目标智能体的 **应用配置 > 技能** 区域，点击 `+` 按钮从列表选取。  
2. **测试调用**：  
   - 在应用配置页右侧对话窗格中输入符合 `description` 触发条件的自然语言指令（如 `把附件里的销售报表.xlsx 按季度汇总并高亮超预算项`），观察是否自动调用对应 Skill 并返回预期文件。  
3. **更新自定义 Skill**：  
   - 修改本地 ZIP 包中的 `SKILL.md`（尤其优化 `description`），重新上传同名包即可创建新版本；已绑定该 Skill 的智能体会在下次请求时自动加载最新版，无需重启或重新配置——此机制已在 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中明确说明。

## 限制和注意事项

- **大小限制**：ZIP 包总大小 ≤ 10 MB，超出将导致上传失败。  
- **审查延迟**：自定义 Skill 上传后需约 2 分钟完成内容审查（校验 `SKILL.md` 格式、字段完整性及 ZIP 结构），期间无法添加至应用。  
- **描述质量强依赖**：`description` 缺乏具体触发词或未明确排除边界场景，将直接导致误调用或漏调用；建议严格遵循文档中列出的四项编写建议。  
- **无状态执行**：每个 Skill 调用均为独立会话，不共享上下文或临时文件，多次调用间无隐式状态传递。  
- **调试支持弱**：当前不提供 Skill 内部日志输出或单步执行追踪能力，问题定位主要依赖 `description` 重写与对话样本迭代测试。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


