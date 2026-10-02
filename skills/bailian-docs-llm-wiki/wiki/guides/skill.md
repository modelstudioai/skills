# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，支持无需编码即可让智能体自动识别并执行特定类型任务（如文件解析、数据清洗、格式转换等）。官方 Skill 开箱即用，自定义 Skill 则通过 ZIP 包形式灵活适配业务场景。其核心机制依赖 `SKILL.md` 中的语义描述驱动智能体调用决策，而非硬编码规则。

## 支持的模型/功能

- **适用模型**：所有支持 Skill 调用的百炼智能体模型（当前为 Qwen 系列大模型，具体兼容性见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)）。
- **核心功能**：
  - 自动识别用户意图与 Skill 描述匹配度，触发调用；
  - 支持文件输入/输出（如 `.xlsx`, `.csv`, `.pdf` 等格式处理）；
  - 官方 Skill 覆盖通用办公文档、表格、文本处理；自定义 Skill 可扩展至行业专属格式（如医疗 DICOM 元数据提取、金融 SWIFT 报文解析等）。

> **注意**：部分旧版文档提及 Skill 可直接调用外部 API，但根据最新实现，Skill 本身不包含网络请求能力，所有 I/O 均通过百炼[沙箱](../concepts/sandbox.md)环境受控完成，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` YAML frontmatter | 是 | Skill 唯一标识符，仅限小写字母、数字、连字符；全局同账号下不可重复。 |
| `description` | `SKILL.md` YAML frontmatter | 是 | 决定调用准确率的核心字段，需明确输入类型、支持操作、触发关键词及**不适用场景**（避免误触发）。 |
| ZIP 包大小 | 上传时校验 | — | ≤ 10 MB；超限将被拒绝，审查失败提示不包含具体压缩建议，参见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。 |

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面添加；  
   - 自定义 Skill：编写符合规范的 `SKILL.md`，打包为 ZIP（根目录含该文件），上传至控制台「组件 > Skill 管理 > 自定义 Skill」。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击「添加到智能体」；  
   - 方式二：在目标应用的「应用配置 > 技能」区域点击 `+` 添加。

3. **测试验证**  
   在应用配置页右侧对话窗格发送典型指令（如 `整理附件中的销售数据为透视表`），观察是否触发对应 Skill 并返回预期文件。

## 限制和注意事项

- **版本管理**：官方 Skill 自动更新，已添加的应用即时生效；自定义 Skill 需重新上传同名 ZIP 才生成新版本，旧版本不会自动替换。
- **调用边界**：Skill 无法访问外部网络、本地文件系统或用户私有数据库；所有文件处理均在百炼安全[沙箱](../concepts/sandbox.md)内完成。
- **描述质量强相关**：`description` 字段若未明确排除歧义场景（例如未声明“不处理图片中的表格”），可能导致误触发。强烈建议按示例完整覆盖适用/不适用条件。
- **审查耗时**：ZIP 上传后审查约需 2 分钟，失败时仅提示 YAML 格式或字段缺失，不提供语义合理性检查——开发者需自行验证描述准确性。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


