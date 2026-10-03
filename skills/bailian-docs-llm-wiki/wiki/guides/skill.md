# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，使智能体能在对话中自动识别并执行特定类型任务（如文件解析、数据清洗等），无需开发者编写集成代码或调用外部 API。官方 Skill 开箱即用，自定义 Skill 支持 ZIP 包上传，通过 `SKILL.md` 定义元信息与触发逻辑。其核心机制依赖于 description 字段的语义描述质量来驱动智能体的自动调用决策，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **适用模型**：Skill 与底层大模型解耦，所有支持智能体应用的模型（如 Qwen 系列、Baichuan 等）均可使用 Skill，调用行为由平台运行时统一调度。
- **功能范围**：
  - 官方 Skill：覆盖通用文件处理场景（如 `xlsx`、`pdf`、`csv` 解析与生成），由平台预置并持续更新，详情见 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面；
  - 自定义 Skill：支持任意 Python 逻辑封装（需符合 ZIP 包规范），适用于行业专属格式解析、定制化数据转换等场景；
- > **注意**：Skill 不支持直接调用外部 HTTP 接口或访问私有数据库；所有执行均在百炼沙箱环境中完成，网络出向受限。该限制在 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中未明确说明，但实际审查阶段会拦截含 `requests.post` 等外联调用的代码。

## 关键参数

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `name` | 是 | string | Skill 唯一标识符，仅限小写字母、数字和连字符（如 `invoice-parser`），不可与当前账号下已有 Skill 重名 |
| `description` | 是 | string | 决定调用准确率的核心字段，必须清晰声明输入类型、支持操作、触发关键词及**不适用场景**（参见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的完整示例） |
| ZIP 包大小 | 是 | ≤10 MB | 整个 ZIP 文件（含代码、依赖、SKILL.md）不得超过 10 MB |

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面添加；  
   - 自定义 Skill：按规范编写 `SKILL.md`（YAML frontmatter 格式），打包为 ZIP，通过控制台「组件 > Skill 管理 > 自定义 Skill」上传。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击「添加到智能体」；  
   - 方式二：在目标智能体的「应用配置 > 技能」区域点击加号选择 Skill。

3. **测试调用**  
   在应用配置页右侧对话窗格中发送符合 `description` 触发条件的自然语言指令（如“把附件里的 CSV 按销售额排序并导出为 Excel”），观察是否自动调用并返回预期结果。

## 限制和注意事项

- **版本管理**：官方 Skill 自动更新，已添加的智能体会即时生效；自定义 Skill 更新需重新上传同名 ZIP 包，系统创建新版本，旧版本仍保留在历史记录中，但新对话默认使用最新版。
- **审查耗时**：ZIP 包上传后需约 2 分钟自动审查，失败时需根据提示修改 `SKILL.md` 或代码逻辑后重试。
- **安全约束**：Skill 运行于隔离沙箱，禁止读写宿主机文件系统、执行 shell 命令、建立非白名单域名的网络连接；依赖需全部打包进 ZIP（不支持 `pip install` 动态安装）。
- > **注意**：文档中“description 编写建议”强调需包含“不适用场景”，但部分早期自定义 Skill 的 `SKILL.md` 示例遗漏该条，易导致误触发。强烈建议严格遵循 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的完整示例结构。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


