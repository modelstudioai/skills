# changelog group

`changelog group` 是百炼 CLI 的版本演进记录集合，集中呈现各功能模块的新增、变更与修复。该文档按语义化版本号组织，每个版本条目聚焦具体命令行为、参数扩展、权限模型调整及底层机制优化。开发者可通过此文档快速定位某项能力的引入时间、使用方式变更及兼容性注意事项。

## 支持的模型/功能

- **精调训练**：支持决策模型（`bl finetune decision create`）、文本模型（`bl finetune text create`）、强化学习（`bl finetune rl`）和在线蒸馏（`bl finetune opd`）四类训练范式；其中决策模型精调流水线包含 `bl dataset generate` / `split` / `validate` 等配套数据命令 [更新日志](../../raw/cli/changelog-group/changelog.md)。
- **语音合成与音色管理**：`bl speech voice` 命令组支持 CosyVoice / Qwen-Audio / Omni 三类音色克隆与管理，`bl speech generate` 支持多参考音频播客生成；Omni 音色仅支持 `clone` / `list` / `delete`，不支持 `preview` 或 `update` [更新日志](../../raw/cli/changelog-group/changelog.md)。
- **模型路由与容量部署**：`bl deploy router` 支持后付费模型路由（`plan=mr`），策略包括 `EFFECT_FIRST` 和 `COST_FIRST`；`bl deploy capacity` 新增 8 小时闲时容量（`--pricing-cycle Hour --duration 8`），但该实例不可变配、续订或释放 [更新日志](../../raw/cli/changelog-group/changelog.md)。
- **智能体与工作流**：`bl flow-agent` 命令组已替代废弃的 `bl app` 系列（如 `bl app call`），统一通过控制台网关管理智能体生命周期与工作流画布操作。

## 关键参数

- `--modality` 和 `--reasoning-mode`：用于 `bl finetune text create` 及 `bl finetune params`，仅对配置了动态训练选项的模型生效；其取值需与模型服务端定义一致，否则预检失败。
- `--training-type`：默认为 `sft`，可选 `rl` / `opd` / `decision`；在 `bl finetune params` 和 `bl finetune train-options` 中用于筛选超参配置。
- `--biz-from <source>`：全局参数，所有命令均支持，用于声明调用方来源（如 `skill` / `agent`），便于后端按来源统计 PV/UV。
- `--workspace-id`：Memory 相关命令（如 `bl memory node show`）强制要求显式传入，不再静默回退；空值将被拒绝 [更新日志](../../raw/cli/changelog-group/changelog.md)。

## 使用方式

- **精调参数预检**：`bl finetune params` 输出含 `precheck` 字段，标识是否执行了本地预检；有控制台登录态时自动补齐默认值并拦截非法组合，无登录态则降级为警告并透传服务端。
- **RL/OPD 沙箱运行时管理**：需先执行 `bl finetune runtime prepare` 下载并校验 CPython + dashscope 运行时，再通过 `bl finetune rl run` 或 `bl finetune opd run` 提交任务；沙箱内禁止出站网络访问，遇 `EPERM` / `ENETUNREACH` 等错误会给出双语提示。
- **模型自动路由**：`bl image generate` 等 AIGC 命令支持 `--model auto`，由百炼自研 MCP 实现模型自动选择，无需手动指定型号。
- **异步任务处理**：`bl memory add` 默认等待至多 120 秒，`--wait 0` 表示仅提交任务；JSON 输出中需解析 `event_id` 和 `events` 字段，而非依赖返回状态码判断完成。

## 限制和注意事项

> **注意**：`bl app` 命令组（如 `bl app create`）已在 v2.10.0 中废弃，必须迁移至 `bl flow-agent`；官方文档 [更新日志](../../raw/cli/changelog-group/changelog.md) 明确指出“将在未来版本移除”，未迁移脚本存在兼容性风险。

> **注意**：`bl speech voice` 克隆 Omni 音色时，后续 `bl omni` 调用必须使用相同 `--target-model`；而 `bl speech synthesize` 仅支持 CosyVoice / Qwen-Audio 音色，二者模型绑定关系不可混用 [更新日志](../../raw/cli/changelog-group/changelog.md)。

- 8 小时闲时容量实例（`--pricing-cycle Hour --duration 8`）仅在 UTC+8 22:00–24:00 售卖，且到期自动失效，不支持任何生命周期操作（变配、续费、释放、退订）。
- `bl finetune rl run` 仅支持 macOS/Linux，不支持 Windows；沙箱内 Python 运行时为固定版本，由 `bl finetune runtime prepare` 下载并 SHA256 校验。
- `--output json` 已成为 `bl alert` / `bl monitor` / `bl log` 等可观测命令的默认输出格式，依赖文本输出的脚本需显式加 `--output text`。

## 来源文档

- [更新日志](../../raw/cli/changelog-group/changelog.md)


