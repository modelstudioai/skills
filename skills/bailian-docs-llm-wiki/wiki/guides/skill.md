# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，支持无需编码即可让智能体自动识别并执行特定类型任务（如文件解析、数据清洗、格式转换等）。官方 Skill 开箱即用，自定义 Skill 则通过 ZIP 包形式灵活适配业务场景。其核心机制依赖 `SKILL.md` 中的语义描述驱动智能体调用决策，而非硬编码规则。

## 支持的模型/功能

- **适用模型**：所有支持 Skill 调用的百炼智能体模型（当前为 Qwen 系列大模型，具体以 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中“添加 Skill 到智能体”章节说明为准）。
- **核心功能**：
  - 自动触发：基于用户输入语义与 `description` 字段匹配，动态决定是否调用；
  - 文件处理：覆盖 `.xlsx`, `.csv`, `.tsv`, `.xlsm` 等主流表格格式（详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中 xlsx 示例）；
  - 多阶段操作：支持读取、编辑、创建、转换、清洗等端到端处理；
  - 版本管理：官方 Skill 自动更新；自定义 Skill 支持多版本上传与回滚。

> **注意**：文档未明确说明 Skill 是否支持非表格类文件（如 PDF、图像）的原生处理。当前所有示例和要求均聚焦于结构化/半结构化数据，若需处理其他格式，应参考 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中“自定义 Skill”章节确认 ZIP 包内实际实现逻辑。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` YAML frontmatter | 是 | Skill 唯一标识符，仅限小写字母、数字、连字符；同一账号下不可重复。 |
| `description` | `SKILL.md` YAML frontmatter | 是 | 决定调用准确性的关键字段，需明确输入类型、支持操作、触发关键词及**不适用场景**（见原文完整示例）。 |
| ZIP 包大小 | 上传时校验 | — | ≤ 10 MB，超限将拒绝上传。 |

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面查看并添加；  
   - 自定义 Skill：按规范编写 `SKILL.md`，打包为 ZIP（根目录必须含该文件），通过控制台 **组件 > Skill 管理 > 自定义 Skill** 上传。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击 **添加到智能体**，选择目标应用；  
   - 方式二：进入智能体 **应用配置 > 技能** 区域，点击 Skill 右侧 `+` 添加。

3. **测试效果**  
   在应用配置页右侧对话窗格中输入典型指令（如“帮我清洗这个 CSV 的空行和重复列”），观察是否触发对应 Skill 并返回预期结果。

## 限制和注意事项

- **触发依赖描述质量**：`description` 字段是唯一调度依据，模糊或遗漏不适用场景将导致误调用（例如 xlsx Skill 明确排除产出 Word 文档的场景）；
- **无运行时调试接口**：Skill 执行过程不可见，失败时仅返回通用错误提示，需依赖 `description` 严谨性和本地 ZIP 包功能验证；
- **版本更新策略差异**：官方 Skill 自动生效；自定义 Skill 需重新上传同名 ZIP 包触发新版本，已添加的应用**立即使用最新版**（无需手动切换）；
- **安全限制**：ZIP 包内禁止包含可执行二进制、shell 脚本或外部网络请求逻辑；所有处理必须在平台沙箱内完成。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


