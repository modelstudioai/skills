# 技能（Skill）

技能（Skill）是百炼平台中面向**结构化文件与数据处理任务**的声明式能力单元，以 ZIP 包形式封装，包含可执行逻辑、元数据定义（`SKILL.md`）及必要资源。它不依赖运行时环境配置，由平台自动解析、安全扫描并注入智能体工作流，在用户自然语言请求触发下完成如“解析PDF合同”“生成Excel统计表”等确定性操作。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）调用**：Skill 是智能体的“内置工具”，无需显式[函数调用](function-calling.md)声明。智能体根据 `SKILL.md` 中的 `description` 字段（需明确描述输入类型、操作意图和触发词）自动匹配用户请求，并在后台静默执行；例如描述含“xlsx”“分列”“汇总”，则对“把销售数据按地区分列并求和”自动触发 xlsx Skill。
- **Agent Store 统一管理**：Skill 与 MCP 服务并列为 `agent store` 的两大核心能力类型。官方 Skill（如 `pdf`、`xlsx`）开箱即用；自定义 Skill 需上传 ZIP 包并通过控制台或 CLI 添加至智能体，支持一键启用/禁用。
- **全生命周期 API 管理**：通过 Skill API（`/api/v1/skills`）实现创建、版本发布、状态查询与删除。每个 Skill 具有独立 ID，其版本遵循 `major.minor` 格式（如 `1.0`），支持多版本共存与灰度切换。
- **开发者工作流集成**：在 Flow Agent 或 Managed Agent 配置中，Skill 作为预注册能力直接勾选启用；Sandbox Agent 虽不原生支持 Skill，但可通过 HTTP 调用 Skill 对应的内部服务端点（需平台授权）间接集成。
- **CLI 快速操作**：`bl skill list`、`bl skill upload --file skill.zip --version 1.1`、`bl skill delete --id sk-xxx` 等命令提供脚本化管理能力，适配 CI/CD 流程。

## 关键参数和配置

- **ZIP 包要求**：
  - 顶层目录平铺，不得嵌套；
  - 必须包含 `SKILL.md`（YAML frontmatter 格式），至少定义 `name`（全局唯一）、`description`（影响触发精度）、`version`；
  - 总大小 ≤ 10 MB。
- **核心元数据字段（`SKILL.md`）**：
  ```yaml
  name: "xlsx-table-generator"
  description: "创建 Excel 表格，支持多列分组、数值汇总和条件格式；输入为 CSV 或 JSON 数据，不处理图片或 PDF。"
  category: "data-processing"
  ```
- **API 关键参数**：
  - `workspace_id`：必需路径变量，用于路由到对应工作空间；
  - `pageNo` / `pageSize`：分页查询参数（默认 `pageNo=1`, `pageSize=20`）；
  - `version`：上传新版本时显式指定，格式严格为 `X.Y`（如 `2.0`）；
  - `Authorization: Bearer <API_KEY>`：所有 Skill API 请求必需携带有效凭证。

- **状态机**：Skill 版本具有四种状态：
  - `checking`：上传后自动触发安全扫描，期间不可调用；
  - `active`：扫描通过，对调用方可见且可用（官方 Skill 仅 `active` 版本可被访问）；
  - `rejected`：扫描失败，需修正 ZIP 后重新上传；
  - `deleted`：已删除，不可恢复（仅适用于自定义 Skill）。

## 面向开发者，简洁实用

- ✅ **快速上手**：从控制台「Agent Store → 技能」上传 ZIP → 在智能体配置页点击“添加” → 即刻生效。
- ✅ **调试建议**：若 Skill 未被触发，请检查 `SKILL.md` 的 `description` 是否包含用户请求中的关键词（如“表格”“Excel”“汇总”），避免模糊表述（如“处理数据”）。
- ✅ **版本升级**：重新上传同名 Skill 的新 ZIP 包即覆盖旧版本；已绑定该 Skill 的智能体**自动使用最新 `active` 版本**，无需重新发布。
- ⚠️ **注意限制**：
  - 自定义 Skill **仅当前账号可见**，不支持跨账号共享（需导出 ZIP 后由其他账号手动上传）；
  - 官方 Skill 不可删除、不可修改，仅可通过启用/禁用控制可见性；
  - ZIP 下载链接（预签名 URL）有效期仅 2 小时，需及时保存。

> 提示：所有 Skill 均在隔离沙箱中执行，禁止网络外连、系统调用及内网访问，确保安全可控。

## 关联主题页

- [overview 1efecd5ed9835b67](../api/overview-1efecd5ed9835b67.md)
- [agent store](../guides/agent-store.md)
- [capabilities](../guides/capabilities.md)
- [agent development](../guides/agent-development.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


