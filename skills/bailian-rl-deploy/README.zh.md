# 百炼强化学习训练→部署闭环

> [English →](README.md)

**阿里云百炼**平台的「RL 训练 → 观测 → 发布 → 部署 → 调用」端到端 Skill —— 用百炼 CLI `bl` 走完强化学习完整闭环：授权探测 → 托管沙箱运行时 → 数据与 Rollout/Reward 代码 → 提交 RL 任务（`bl finetune rl run`）→ 观测训练 → Checkpoint 自动发布 → 创建推理部署 → 交付可调用示例。RL 通过生成（Rollout）→ 打分（Reward）→ 优化的循环让模型自主探索最优策略，无需标准答案标签。

## 功能简介

告诉 Agent「在百炼上用强化学习训练一个推理模型」或「提交一个 AgenticRL 任务」，这个 Skill 会：

1. **澄清与闸门** —— 请求缺少输入时先问用户（基座模型 / 训练数据 / Rollout-Reward 代码 / MTU 计费 / 是否部署，并提供“官方 demo 默认配置”一键选项）；再确认 CLI 具备 `rl` 命令组、验证认证（`bl auth status`）、探测 RL 开通状态（`bl finetune rl authorize`）、准备并体检托管沙箱运行时（`bl finetune runtime prepare` / `doctor`）
2. **准备数据与代码** —— JSONL（`messages` + `rollout_extra`）加 Rollout/Reward 函数包；官方数学计算 Agent demo 开箱即用
3. **带计费闸门提交** —— `bl finetune rl run --dry-run`（零网络、零计费）→ 披露 MTU 规格 × 数量 × 费用 → 用户确认 → `--yes`
4. **观测训练** —— `bl finetune rl watch / logs / get` 加控制台 Metrics 页（`critic/rewards/mean`）；FAILED 先读日志再动手
5. **发布与部署** —— 最后一个 checkpoint 自动发布到「我的模型」；`bl deploy text create` 变成可调用服务，用 `bl text chat --model <deployed_model>` 推理

## 适用场景

**显式 RL 训练：**
- "在百炼上用强化学习训练模型"
- "提交一个 GRPO/GSPO 强化学习任务"
- "用我的奖励函数跑 AgenticRL 训练"
- "用 RL 训练数学推理 / Agent 工具调用能力"

**隐式（描述目标，Skill 跑完整链路）：**
- "我想让模型通过试错提升多步工具调用能力"
- "用自定义奖励优化 Agent 策略——没有标注答案"
- "用官方 demo 跑通我的第一次 RL 训练"

**不适用（反触发路由）：**
- SFT / DPO / CPT / LoRA 监督微调、音频/图像/视频微调 → `bailian-finetune`（CLI registry，`bl skill init` 安装）
- OPD 蒸馏（`pg_opd`、`teacher_model`）→ `bailian-finetune`（`bl finetune opd *`）
- 只想试模型效果 / 一次性对话 → `bailian-cli`：`bl text chat`
- 不知道选哪个基座 / 模型选型 → `bailian-model-recommend`
- 训练额度 / 用量问题 → `bailian-cli`：`bl quota` / `bl usage`

## 安全护栏

RL 任务开通的是 **MTU（模型训练单元）专属资源——创建即计费**，且不支持按 token 计费：

1. **dry-run → 确认 → `--yes`** —— `rl run` / `cancel` / `delete` / `authorize --authorize` / `runtime clean` 均为高风险写操作。先 `--dry-run` 预览，披露规格 × 数量 × 预计时长与费用量级，取得用户显式确认后才加 `--yes`。exit 7 / `requires_confirmation` 是正常控制流——停下来询问，绝不自动批准。
2. **费用透明** —— IV 型 MTU4 后付费 41.00 元/小时/实例；官方 qwen3.5-9b demo 需 24 × MTU4 ≈ **984 元/小时**。预付费需客户经理提供的 `--instance-id`。
3. **容量公式** —— `--mtu-count` 必须等于 `nnodes_rollout × n_gpus_rollout + nnodes_training × n_gpus_training`；调并行超参时容量同步联动。
4. **等待 ≠ 取消** —— `--watch` 超时（或 Ctrl-C）只停止等待，云端任务继续运行并计费；只有显式 `rl cancel`（经确认）才能止损。
5. **平台与准入闸门** —— 沙箱仅支持 macOS/Linux（Windows 直接拒绝）；RL 训练需客户经理开通白名单。CLI **绝不创建服务关联角色（SLR）**——必需角色缺失时停止流程并引导用户去控制台一键授权，完成后重新探测；advisory 项（遥测 SLR / AppTrace / SLS 开通）不阻塞。

## 前置条件

- 具备 `rl` 命令组的 `bl`（bailian-cli）（`bl finetune rl run --help` 能正常输出；旧版 CLI 先 `bl update`）
- 已认证：`bl auth status`，或 `bl auth login --api-key sk-...`
- macOS 或 Linux；账号已开通 RL 训练白名单
- **无需本地安装 Python / dashscope** —— CLI 自带经审核的托管运行时（钉版 CPython + dashscope 基线），自动下载、校验、缓存
- **出站网络可达**（运行时下载与任务提交均需）。agent 宿主沙箱（如 Codex 默认 `workspace-write`）默认阻断网络：`runtime doctor` 会以增强项 `host-network-reachability` 报告——请在 agent 设置放行网络，或在普通终端执行 prepare / 提交；CLI 支持 `HTTPS_PROXY` / `HTTP_PROXY`（大小写均可）

## 使用示例

```
用官方 agentic-rl demo 在百炼跑我的第一次 RL 训练：
qwen3.5-9b、GSPO、最小计算数据集、MTU4 后付费。
先预览费用，我确认后再提交，训练完部署起来让我能调用。
```

Skill 按五步链路推进：

```
authorize → runtime prepare/doctor → 数据与函数 → rl run（dry-run → 确认 → --yes）
  → rl watch/logs（critic/rewards/mean）→ checkpoint 自动发布 → deploy text create → text chat
```

每一步捕获正确的 ID（`job_id` → 发布后模型名 → `deployed_model`），并绕开常见坑（用 `qwen3.5-9b-ft-...` 名字直接推理会 404——推理必须用部署响应里的 `deployed_model`）。

## 底层原理

```
用户请求
  → 版本/平台/认证闸门 + rl authorize 探测（Console 鉴权）
  → runtime prepare（托管 CPython + dashscope，完整性校验）+ doctor 自检
  → 数据 JSONL + Rollout/Reward 包（--requirements 只上传 FC，绝不装进本地沙箱）
  → rl run --dry-run（零网络 spec 预览）→ 用户确认 → --yes 提交
  → rl watch --follow / logs / get（宿主直连，查询无需沙箱）
  → 最后一个 checkpoint 自动发布 → deploy text create → bl text chat --model <deployed_model>
```

Skill 沉淀了编排流程与实测踩坑：qwen3.5-9b 的 11 个 GSPO 必填超参（空 `hyper_parameters` 会被服务端拒绝）、`--code-dir` / 数据文件用绝对路径而 `--requirements` 相对 code-dir 的路径规则、Reward 指标名须与 `--reward-metric` 键逐字一致、沙箱任务目录随单次调用销毁、服务端错误原样透传不翻译。

## License

Apache-2.0