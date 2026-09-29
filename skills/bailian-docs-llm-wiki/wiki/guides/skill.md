# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔组件，使智能体无需编码即可自动识别并执行特定类型的任务（如文件解析、数据清洗、格式转换等）。Skill 通过语义描述驱动调用，由平台在对话上下文中动态匹配和触发。其设计兼顾开箱即用性与业务定制灵活性，适用于通用场景与垂直领域需求。

## 支持的模型/功能

- **官方 Skill**：平台预置、统一维护的通用能力包（如 `xlsx`、`pdf`、`csv` 等），覆盖主流文件处理与数据分析任务，添加后立即可用，且已添加的实例会自动升级至最新版本。完整列表请参见 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面，该页面也同步更新了各 Skill 的适用范围与变更日志 —— 具体说明详见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。
- **自定义 Skill**：支持用户上传 ZIP 包实现私有化扩展，适用于行业专属格式（如医疗 DICOM 元数据提取）、定制化逻辑（如合同关键条款结构化）等官方未覆盖场景。ZIP 包必须包含符合规范的 `SKILL.md`，且整体大小 ≤10 MB —— 详细要求见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

> **注意**：当前文档未提及 Skill 对多模态模型（如 Qwen-VL）或[流式输出](../concepts/streaming-output.md)场景的适配能力；若实际使用中发现图像类输入无法触发 PDF 或 OCR 相关 Skill，请优先参考 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的 description 编写建议，确保描述中明确包含“图像中的表格”“扫描件”等触发关键词，避免因语义覆盖不足导致调用失败。

## 关键参数

所有 Skill 的行为核心由 `SKILL.md` 中的两个必填字段控制：

- `name`：唯一标识符，仅允许小写字母、数字和连字符（如 `invoice-parser`），同一账号下不可重复；
- `description`：决定 Skill 是否被调用的关键字段，需同时包含：
  - 输入约束（如支持的文件扩展名、数据结构特征）；
  - 支持操作（如“提取发票金额”“合并多个 CSV 表”）；
  - 触发信号（如用户提及“对账单”“导出为 Excel”）；
  - 明确排除项（如“不处理 Word 文档”“不生成 API 调用代码”）。

description 质量直接影响调用准确率，示例可参考 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中 `xlsx` Skill 的完整 YAML 描述。

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面点击“添加到智能体”；  
   - 自定义 Skill：打包含合规 `SKILL.md` 的 ZIP 文件，在 Skill 管理页点击“自定义 Skill”按钮上传，审查通过后出现在“自定义 Skill”标签页。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击“添加到智能体”，选择目标应用；  
   - 方式二：进入智能体“应用配置” → “技能”区域 → 点击对应 Skill 右侧“+”号。

3. **测试验证**  
   在应用配置页右侧对话窗格中发送典型请求（如“把附件里的销售数据按季度汇总成图表”），观察是否触发 Skill 并返回预期结果（如 `.xlsx` 文件下载链接）。

## 限制和注意事项

- **版本管理**：官方 Skill 自动更新，无需人工干预；自定义 Skill 更新需重新上传同名 ZIP 包，系统将创建新版本，已添加的应用**自动切换至最新版**（无须手动重配）；
- **审查机制**：上传后约 2 分钟完成静态校验（检查 `SKILL.md` 存在性、YAML 格式、字段完整性），失败时需根据提示修改后重传；
- **调用边界**：Skill 仅响应与 `description` 语义强匹配的用户意图，不支持显式指令调用（如“调用 xlsx Skill”无效），也不支持跨 Skill 协同编排（如先调 PDF 再调 xlsx）；
- **安全约束**：ZIP 包内禁止包含可执行文件（`.exe`, `.sh`, `.py` 等）、外部网络请求逻辑或敏感凭证，审查阶段将拦截非常规文件类型。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


