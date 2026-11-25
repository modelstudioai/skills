# changelog group

`changelog group` 是百炼 CLI 的版本演进记录集合，用于追踪各功能模块（如精调、部署、语音、翻译等）的新增、变更与修复。该日志按语义化版本号组织，每个版本条目明确标注功能归属、行为变更及兼容性影响，是开发者验证 CLI 行为、排查问题和适配新特性的核心参考依据。所有变更均经服务端能力对齐，本地 CLI 逻辑严格遵循控制台 API 规范。

## 支持的模型/功能

- **精调相关**：支持决策模型精调（`bl finetune decision create`）、文本精调（`bl finetune text create`）、强化学习（`bl finetune rl`）和在线蒸馏（`bl finetune opd`）；支持 LoRA / efficient_sft 训练类型，动态训练选项（`--modality`, `--reasoning-mode`）需通过 `bl finetune train-options` 查询 [原文标题](../../raw/cli/changelog-group/changelog.md)。
- **语音合成与克隆**：`bl speech voice` 管理自定义音色（CosyVoice / Qwen-Audio / Omni），`bl speech generate` 支持播客/对话类音频生成，参考音频仅限 WAV/MP3/OGG Opus 格式 [原文标题](../../raw/cli/changelog-group/changelog.md)。
- **翻译能力**：`bl text translate`（Qwen-MT）、`bl image translate`（图文排版保留）、`bl omni translate`（多模态统一翻译），均支持术语表与敏感词过滤 [原文标题](../../raw/cli/changelog-group/changelog.md)。
- **部署与容量管理**：支持后付费模型路由（`bl deploy router`）、PTU 闲时容量（8 小时）、自动续费开关（`bl deploy capacity auto-renew enable/disable`）。
- **其他关键能力**：`bl flow-agent`（替代已废弃的 `bl app`）、`bl parsex`（文档/音视频结构化解析）、`bl knowledge`（知识库全链路）、`bl memory`（记忆基础设施）。

## 关键参数

- `--modality` / `--reasoning-mode`：仅对配置了动态训练选项的模型生效，须先通过 `bl finetune train-options` 确认支持范围。
- `--training-type`：默认值为 `sft`，可选 `rl`, `opd`, `decision`；`bl finetune text create` 中该参数影响参数预检逻辑。
- `--biz-from <source>`：全局参数，所有命令均支持，用于声明调用方业务来源（如 skill、agent），便于 PV/UV 统计。
- `--workspace-id`：Memory、Knowledge、Deploy 等命令必需显式传入，不再静默回退；空白值将被拒绝 [原文标题](../../raw/cli/changelog-group/changelog.md)。
- `--output`：仅接受 `text` 或 `json`，非法取值在命令执行前即被拦截（2.10.1 版本修复）。

## 使用方式

- 所有 `bl finetune *` 命令在提交前执行精调参数预检：登录态可用时自动补齐默认值并拦截非法组合；无登录态时降级为警告并透传服务端。`bl finetune params` 的 JSON 输出含 `precheck` 字段标识是否执行预检。
- `bl finetune rl run` 和 `bl finetune opd run` 支持 `--dry-run` 预览任务规格，避免误提交。
- `bl deploy router create` 要求显式指定 `--strategy`（`EFFECT_FIRST` / `COST_FIRST`）与 `--candidates`，创建后立即进入 RUNNING 状态，无需额外启停。
- `bl speech generate` 使用参考音频时，必须以 `@voice1`…`@voice3` 形式引用本地文件路径，不接受音色 ID；使用默认北京 MaaS 端点时需指定 `--workspace-id`。
- `bl dataset validate` 可校验决策样本 JSONL 格式，配合 `bl dataset generate` 和 `bl dataset split` 构成完整精调数据流水线。

## 限制和注意事项

> **注意**：`bl app` 命令组（如 `bl app create`, `bl app list`）已在 2.10.0 版本废弃，必须迁移至 `bl flow-agent`；该弃用状态在 [原文标题](../../raw/cli/changelog-group/changelog.md) 中明确标注，且将在未来版本彻底移除。

> **注意**：Omni 音色仅支持 `clone` / `list` / `delete`，不支持 `update` / `preview` / `get`；且 `bl speech voice design` 不支持 Omni 目标模型，此限制在 2.11.0 版本引入，与 `bl speech voice` 其他子命令能力不一致。

- `bl finetune rl` 仅支持 macOS/Linux，沙箱运行时依赖宿主出站网络；若遇 `EPERM` / `EACCES` 等连接级拒绝，CLI 会给出双语提示并建议放行网络或设置 `HTTPS_PROXY`。
- `bl deploy capacity create --pricing-cycle Hour` 创建的 8 小时闲时实例不可变配、续订、自动续费、释放或退订，到期自动失效；售卖时段（UTC+8 22:00–24:00）由服务端强校验。
- `bl memory add` 默认异步提交抽取任务，最多等待 120 秒；`--wait 0` 仅提交不等待，JSON 输出需解析 `event_id` 和 `events` 字段，**提交成功不等于抽取完成**（2.5.0 版本变更）。

## 来源文档

- [更新日志](../../raw/cli/changelog-group/changelog.md)


