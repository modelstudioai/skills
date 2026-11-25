# changelog group

`changelog group` 是百炼 CLI 中用于组织和管理各功能模块版本演进信息的逻辑分组，涵盖部署、精调、智能体、知识库、Memory、可观测性等核心能力的命令新增、参数变更与行为修复。该分组不对应单一命令，而是通过 CLI 各子命令（如 `bl deploy`、`bl finetune`、`bl flow-agent`）的迭代共同构成，所有变更均在 [更新日志](../../raw/cli/changelog-group/changelog.md) 中按版本号集中记录。开发者应结合具体子命令文档与本 changelog group 的上下文理解兼容性影响。

## 支持的模型/功能

- **模型路由（MR）**：支持后付费模型路由管理（`bl deploy router`），含 `EFFECT_FIRST` / `COST_FIRST` 策略及候选模型动态编排；8 小时闲时容量（`--pricing-cycle Hour --duration 8`）仅限特定时段（UTC+8 22:00–24:00）且不可变配或续费。
- **精调训练**：覆盖强化学习（`bl finetune rl`）与在线蒸馏（`bl finetune opd`）两种范式，沙箱运行时基于固定版本 CPython + dashscope，网络受限时提供双语拒绝提示；超参校验由服务端权威配置驱动，本地不再填充未指定参数（见 [更新日志](../../raw/cli/changelog-group/changelog.md) 2.8.5 节）。
- **智能体与工作流**：`bl flow-agent` 为当前推荐命令组（替代已废弃的 `bl app`），支持草稿合并更新、乐观锁保存、触发器规范化发布；`bl omni` 默认模型已更新为 `qwen3.8-omni-flash`（见 [更新日志](../../raw/cli/changelog-group/changelog.md) 2.9.0 节）。
- **Memory 与 Knowledge**：Memory 命令全面切换至业务空间专属端点，强制要求 `--workspace-id`；Knowledge 支持音视频解析、流式上传与纯图片检索，建库过程含计费说明与资源清理指引。

## 关键参数

- `--biz-source <source>`：全局参数，所有命令支持，用于声明业务来源并上报至 AEM `c6` 列；缺省省略，空白或非法值归一化为 `unknown`（见 [更新日志](../../raw/cli/changelog-group/changelog.md) 2.11.0 节）。
- `--enable-search`：`bl text chat` 支持模型内置联网搜索，`qwen3.8-max` 默认开启；与 `--mode model` / `mcp` 搜索模式联动，凭证自动按模式选择。
- `--output {text,json}`：严格校验取值，非 `text` 或 `json` 将在执行前拒绝（见 [更新日志](../../raw/cli/changelog-group/changelog.md) 2.10.1 节）。
- `--workspace-id`：Memory、Knowledge、Decision 等空间敏感命令的必需参数，显式传入空白值将被拒绝，避免静默回退（见 [更新日志](../../raw/cli/changelog-group/changelog.md) 2.8.6 节）。

## 使用方式

- 所有 `changelog group` 相关功能均通过 `bl <subcommand>` 调用，例如：
  - 部署路由：`bl deploy router create --name my-router --route-version v1 --strategy COST_FIRST --candidates qwen3.8-max,qwen3.5-turbo`
  - RL 训练：`bl finetune rl run --config-file rl.yaml --dry-run`（预览规格）
  - 工作流发布：`bl flow-agent workflow publish --workflow-id wf-xxx`
- 全局参数（如 `--biz-source`, `--workspace-id`, `--output`）可置于命令路径前或后，但鉴权参数（如 `--config`）必须位于路径之后。
- JSON 模式下，业务结果输出到 stdout，警告与错误以 JSONL 格式写入 stderr；quiet 模式仅隐藏进度提示，仍保留完整结果与错误。

## 限制和注意事项

> **注意**：`bl app` 命令组已在 2.10.0 版本废弃，`bl flow-agent` 为其完全替代方案；脚本中若仍在使用 `bl app`，需立即迁移，否则将在未来版本失效（见 [更新日志](../../raw/cli/changelog-group/changelog.md) 2.10.0 节）。

> **注意**：8 小时闲时容量实例到期后自动失效，**不可释放、退订、续订或修改配置**；创建时必须指定 `--service-tier ptu_default`（PTU 场景）且 `--auto-renewal false`，服务端会校验售卖时段与模型支持。

- `bl finetune rl` / `opd` 沙箱仅支持 macOS/Linux，Windows 下无法执行；沙箱内禁止出站网络访问时，会明确提示 `EPERM` / `EACCES` 等错误并建议设置 `HTTPS_PROXY`。
- `bl deploy delete` 对 RUNNING 状态的模型路由（`plan=mr`）支持直接删除，无需先停机；但对 PTU 实例，删除前需确保其非 RUNNING 或已手动停机。
- `bl decision` 仅支持北京/新加坡地域，且依赖工作空间专属 Endpoint；dry-run 不发送实际请求，仅返回规格预览与地域路由决策。

## 来源文档

- [更新日志](../../raw/cli/changelog-group/changelog.md)


