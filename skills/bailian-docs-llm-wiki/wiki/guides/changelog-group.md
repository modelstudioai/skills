# changelog group

`changelog group` 是百炼 CLI 的版本更新日志聚合模块，用于集中记录各功能模块（如部署、精调、知识库、Memory 等）的迭代变更。它不提供运行时能力，而是作为开发者掌握 CLI 行为演进、兼容性边界与新特性入口的关键参考。所有变更均通过语义化版本号（如 `2.10.5`）组织，并严格标注影响范围（新增/变更/修复）与风险等级（如“高风险计费操作”）。

## 支持的模型/功能

- **[模型路由](../concepts/model-routing.md)管理**：`bl deploy router` 命令组支持后付费[模型路由](../concepts/model-routing.md)（`plan=mr`），包括 `versions`、`create`（支持 `EFFECT_FIRST` / `COST_FIRST` 策略）、`list`、`get`、`update` 与 `delete`；详见 [更新日志](../../raw/cli/changelog-group/changelog.md) 中 `2.10.5` 版本说明。
- **强化学习与在线蒸馏**：`bl finetune rl` 和 `bl finetune opd` 命令组覆盖端到端训练链路，含沙箱运行时准备（`prepare`）、健康检查（`doctor`）与清理（`clean`）；其超参查询能力由 `bl finetune params` 提供，支持按 `--training-type`、`--modality` 等动态筛选。
- **智能体与工作流**：`bl flow-agent` 命令组替代已废弃的 `bl app`（自 `2.10.0` 起），支持 `create`/`publish`/`delete` 等全生命周期操作；工作流画布管理（`save`/`export`）遵循控制台编辑器逻辑规范化触发器。
- **知识库与 Memory**：`bl knowledge` 系列命令（`init`/`doc sync`/`parsex`）和 `bl memory` 系列命令（`node show`/`profile list`/`search`）均已集成至 changelog group，其中 Memory 命令自 `2.5.0` 起强制要求 `--workspace-id`，且参数名统一为 `--library-id`；具体用法见 [Memory](../../raw/cli/capabilities/agent-infrastructure/memory.md)。

## 关键参数

- `--biz-source <source>`：全局参数（`2.11.0` 新增），用于声明业务来源，归一化后上报至 AEM 扁平列 `c6`；空白或非法值默认为 `unknown`。
- `--output {text,json}`：严格校验取值（`2.10.1` 修复），非 `text` 或 `json` 将在执行前拒绝；`2.6.2` 起 `bl alert`/`bl monitor`/`bl log` 默认 JSON 输出，需显式传 `--output text` 以保持文本行为。
- `--enable-search`：`bl text chat` 支持模型内置联网搜索（`qwen3.8-max` 默认开启），关闭时不再发送 `thinking_budget`（`2.8.5` 修复）。
- `--model auto`：适用于 `bl image generate` 等 AIGC 命令，通过自研 MCP 实现自动[模型路由](../concepts/model-routing.md)（`2.7.2` 新增）。

## 使用方式

- 所有命令均通过 `bl <subcommand>` 调用，例如：
  ```bash
  bl deploy router create --name my-router --route-version v1 --strategy COST_FIRST --candidates qwen3.8-max,qwen3.8-plus
  bl finetune rl run --config-file train.yaml --dry-run
  bl flow-agent publish --id abc123
  ```
- 全局参数（如 `--config`、`--workspace-id`、`--biz-source`）可置于命令路径前或后，但鉴权参数（如 `--api-key`）必须位于命令路径之后。
- `--dry-run` 广泛用于高风险操作（如容量续费、路由创建、OPD 训练），预览规格与资源消耗，不触发实际变更。
- JSON 模式下，业务结果输出至 stdout，警告与错误以 JSONL 格式写入 stderr（`2.8.0` 引入）；quiet 模式仅隐藏进度提示，仍保留完整结果与错误。

## 限制和注意事项

- **模型路由删除**：`bl deploy delete` 支持直接删除 RUNNING 状态的 `plan=mr` 路由（`2.10.5` 变更），但 `bl deploy router delete` 仍需确认，且不可逆。
- **闲时容量限制**：8 小时闲时实例（`--pricing-cycle Hour --duration 8`）不可变配、续订、自动续费、释放或退订，到期自动失效；售卖时段（UTC+8 22:00–24:00）与模型支持由服务端强校验。
- **沙箱网络隔离**：RL/OPD 沙箱内出站网络被阻断时（`EPERM`/`EACCES` 等），CLI 给出双语提示并建议放行网络、改用普通终端或设置 `HTTPS_PROXY`（`2.10.4` 新增）。
- > **注意**：`bl app` 命令组已在 `2.10.0` 版本废弃，`bl flow-agent` 为其正式替代；但原始文档中 `2.9.0` 仍描述 `bl app` 为“新增应用控制面命令”，该表述已过时，应以 [更新日志](../../raw/cli/changelog-group/changelog.md) 中 `2.10.0` 的废弃声明为准。
- > **注意**：`bl usage token-plan` 在 `2.2.0` 后仅展示月度额度，而 `2.7.1` 新增 `hasQuotaData` 字段用于区分无配额数据与正常结果——二者无冲突，但开发者需注意 `2.2.0` 移除了 5 小时/1 周窗口，避免依赖已移除字段。
- > **注意**：`bl memory add` 自 `2.5.0` 起改为异步任务，默认等待 120 秒，JSON 输出需解析 `event_id` 与 `events` 字段；而旧版文档未明确此行为变更，实际使用必须依据 [Memory](../../raw/cli/capabilities/agent-infrastructure/memory.md) 中的说明。

## 来源文档

- [更新日志](../../raw/cli/changelog-group/changelog.md)


