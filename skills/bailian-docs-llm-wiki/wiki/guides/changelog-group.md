# changelog group

`changelog group` 是百炼 CLI 的版本更新日志聚合机制，用于结构化呈现各版本新增功能、行为变更、修复项及兼容性调整。它不提供运行时能力，而是作为开发者掌握 CLI 演进节奏、评估升级影响、排查行为差异的核心参考依据。所有变更均经严格测试并遵循语义化版本规范，关键行为变更（如参数默认值调整、废弃命令、鉴权逻辑重构）均明确标注 BREAKING 或兼容性说明。

## 支持的模型/功能

- **强化学习与在线蒸馏**：自 `2.10.4` 起支持 `bl finetune rl` 和 `bl finetune opd` 命令组，覆盖端到端训练链路与纯模型在线蒸馏，依赖托管沙箱运行时（仅 macOS/Linux），详见 [更新日志](../../raw/cli/changelog-group/changelog.md)。
- **智能体与工作流管理**：`2.10.0` 引入 `bl flow-agent` 命令组，全面替代已废弃的 `bl app` 系列（`bl app call` / `bl app list` 等），统一通过控制台网关管理智能体、工作流及版本；`2.9.0` 中同类功能曾以 `bl app` 形式发布，但已被明确标记为废弃，需迁移至新命令组。
- **知识库与 Memory**：`2.6.0` 新增 `bl knowledge` 系列命令，支持知识库初始化、文档同步与检索；`2.5.0` 新增 `bl memory` 系列命令，提供记忆节点、画像模板与技能记忆的全生命周期管理，其使用方法见 [Memory](../../raw/cli/capabilities/agent-infrastructure/memory.md)。
- **模型自动路由与 MCP 集成**：`2.7.2` 起 `bl image generate` 等 AIGC 命令支持 `--model auto`，由百炼自研 MCP 实现模型自动路由；`2.0.0` 新增 `bl mcp connect/disconnect`，原生注册 MCP 服务至主流 Agent 工具链。

> **注意**：`bl app` 命令组在 `2.10.0` 版本中被正式废弃，而 `2.9.0` 文档仍将其列为“新增”，此为文档时效性矛盾。实际开发中应以 `2.10.0` 的 `bl flow-agent` 为准，避免使用 `bl app`。

## 关键参数

- `--output`：全局参数，仅接受 `text` 或 `json`，其他值在执行前即被拒绝（`2.10.1` 修复）。
- `--workspace-id`：多数命令（如 `bl memory`、`bl decision`、`bl deploy capacity`）必需显式传入，空白值将被拒绝，不再静默回退（`2.8.6` 修复）。
- `--dry-run`：广泛用于预览任务规格（如 `bl finetune opd run`、`bl finetune compress create`、`bl decision choice`），不触发真实资源创建或计费。
- `--yes`：高风险操作（如 `bl flow-agent delete`、`bl memory delete`）强制要求确认，防止误删。
- `--model auto`：AIGC 类命令（`bl image generate` 等）启用自动模型路由，依赖百炼 MCP 服务（`2.7.2` 新增）。

## 使用方式

- 日志按语义化版本号组织，每个版本条目以 `## <version> | <date>` 开头，后接 `-` 列表形式的变更点。
- CLI 自带 `bl version` 可查看当前版本；`bl update` 可检查并升级至最新版（`2.3.2` 起失败返回非零退出码，便于脚本判断）。
- 所有命令均支持 `--help` 获取实时帮助；`--introspect` 可输出结构化命令说明（`2.6.0` 新增）。
- 配置优先级固定：命令参数 > 百炼环境变量（如 `BAILIAN_ACCESS_KEY_ID`）> 百炼配置文件 > 阿里云环境变量（`2.8.0` 明确）。

## 限制和注意事项

- **[沙箱环境](../concepts/sandbox.md)限制**：`bl finetune rl` 与 `bl finetune opd` 的沙箱运行时仅支持 macOS/Linux，Windows 不可用；沙箱内出站网络被阻断时会抛出 `EPERM`/`EACCES` 等错误并给出双语提示，建议放行网络或设置 `HTTPS_PROXY`（`2.10.4` 新增）。
- **地域限制**：自定义模型导入（`bl cmodel base-models/import`）API 当前仅在北京地域开放；临时文件上传服务官方仅支持北京与新加坡，其他地域明确报错（`2.8.0`、`2.6.1`）。
- **废弃与迁移**：`bl app` 命令组已在 `2.10.0` 废弃，`bl usage free` 与 `bl usage freetier` 在未解析模型列表时会明确标注“尚未解析”，避免误判为确定集合（`2.10.1` 修复）。
- **JSON 模式行为变更**：`2.6.2` 起 `bl alert`/`bl monitor`/`bl log` 默认 JSON 输出，即使 Profile 配置为 text；quiet 模式下仅隐藏进度提示，结果、警告、错误仍完整保留（`2.8.0` 明确），脚本需适配 JSON 字段提取而非文本解析。

> **注意**：`bl finetune params`（`2.8.4` 新增）与 `bl finetune metrics`（`2.8.4` 新增）虽属精调能力，但其本身不构成独立命令组，而是 `bl finetune` 下的子命令，不应与 `changelog group` 混淆。该分组仅指日志本身的组织逻辑，而非功能模块。

## 来源文档

- [更新日志](../../raw/cli/changelog-group/changelog.md)


