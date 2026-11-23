# changelog group

`changelog group` 是百炼 CLI 的版本更新日志集合，用于追踪各功能模块的迭代演进、行为变更与修复项。它不提供运行时能力，而是作为开发者理解 CLI 行为边界、兼容性要求和迁移路径的核心参考依据。所有变更均以语义化版本（如 `2.10.4`）组织，按时间倒序排列，并严格标注影响范围（命令、参数、鉴权、输出格式等）。

## 支持的模型/功能

- **强化学习训练（RL）**：自 `2.10.4` 起新增 `bl finetune rl` 命令组，覆盖授权检查、任务提交、状态观测与生命周期管理，依赖托管沙箱环境（仅 macOS/Linux），计费单位为 MTU 算力；详情见 [更新日志](../../raw/cli/changelog-group/changelog.md)。
- **在线蒸馏（OPD）**：同版本引入 `bl finetune opd`，支持基于教师模型的纯模型蒸馏，含 `--dry-run` 预览与超参查询能力；该能力与 RL 共享沙箱运行时管理命令（`bl finetune runtime prepare/doctor/clean`），详见 [更新日志](../../raw/cli/changelog-group/changelog.md)。
- **智能体与工作流**：`2.10.0` 起 `bl app` 命令组已废弃，统一迁移至 `bl flow-agent`；`2.9.0` 引入的 `bl app` 与 `2.10.0` 的 `bl flow-agent` 在功能上完全对齐，但后者为当前唯一维护路径；注意两者在 `delete` 操作中均强制要求 `--yes` 确认，避免误删。
- **知识库与 Memory**：`2.6.0` 新增 `bl knowledge` 系列命令，`2.5.0` 引入 `bl memory` 命令组，二者均采用业务空间专属端点，必须显式传入 `--workspace-id` 或通过环境变量/配置项指定；> **注意**：`2.5.0` 文档中明确要求 Memory 命令“需通过 `--workspace-id` 提供业务空间 ID”，而部分早期知识库命令（如 `2.6.0` 中的 `bl knowledge init`）未在变更说明中强调此约束，实际调用时若缺失 workspace 上下文将失败，应统一补全。

## 关键参数

- `--output`：全局参数，仅接受 `text` 或 `json`；其他值在命令执行前即被拒绝（`2.10.1` 修复）；`2.6.2` 起 `bl alert`/`bl monitor`/`bl log` 默认 JSON 输出，脚本需显式指定 `--output text`。
- `--workspace-id`：多数新功能（Memory、Knowledge、Decision、Prime 模式）的强制参数；`2.5.0` 起 Memory 命令改用业务空间专属端点，`2.8.3` 起 Profile 可按搜索模式声明凭证，切换时自动匹配 workspace。
- `--dry-run`：广泛用于预览任务规格（如 `bl finetune opd run`、`bl finetune compress templates create`、`bl decision choice`），不触发真实资源创建或计费。
- `--model auto`：`2.7.2` 起在 AIGC 类命令（`bl image generate/edit` 等）中启用百炼自研 MCP 自动路由，替代硬编码模型名。

## 使用方式

- CLI 版本升级：使用 `bl update`，失败时返回非零退出码（`2.3.2`），便于 CI/CD 脚本判断。
- 鉴权优先级：AK/SK 按“命令参数 → 百炼环境变量（`BAILIAN_ACCESS_KEY_ID`）→ 百炼配置 → 阿里云环境变量”解析（`2.8.0`）；控制台登录凭证可自动获取 AK/SK（`2.8.0`）。
- 沙箱网络调试：若遇 `EPERM`/`EACCES`/`ENETUNREACH`/`EHOSTUNREACH`，CLI 将给出双语提示，建议放行出站网络、改用普通终端或设置 `HTTPS_PROXY`（`2.10.4`）。
- 配置诊断：`bl config show` 显示 API Key 与 Base URL 的生效来源，当二者来自不同配置源时会明确提示（`2.7.0`）；`bl auth status` 在未配置模型 API Key 时会主动提醒（`2.3.3`）。

## 限制和注意事项

- **沙箱环境限制**：RL/OPD 沙箱仅支持 macOS/Linux，不支持 Windows；沙箱内禁止出站网络访问，需手动配置代理或改用宿主环境执行（`2.10.4`）。
- **地域限制**：`bl cmodel base-models/import` 导入 API 当前仅在北京地域开放（`2.8.0`）；临时文件上传服务官方仅支持北京和新加坡，其他地域及 Token Plan 明确报错（`2.6.1`）。
- **废弃与迁移**：`bl app` 命令组已在 `2.10.0` 标记为废弃，`bl app call/list` 必须替换为 `bl flow-agent call/list`，未来版本将移除（`2.10.0`）；旧推荐流程库接口（`getModels` 等）于 `2.6.1` 移除，调用方需适配新引擎（`LegacyIntentProfile` 等导出类型仅作兼容）。
- **quiet 模式行为变更**：`2.8.0` 起 quiet 模式仅隐藏进度提示，保留完整结果、警告及错误；依赖 quiet 提取 ID/路径/回答的脚本，必须改为解析 JSON 字段（`2.8.0`）；[更新日志](../../raw/cli/changelog-group/changelog.md) 中多次强调此行为变更对自动化脚本的影响。

## 来源文档

- [更新日志](../../raw/cli/changelog-group/changelog.md)


