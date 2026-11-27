# 百炼模型训练→部署闭环

> [English →](README.md)

**阿里云百炼**平台的「训练 → 部署 → 调用」端到端 Skill —— 用百炼 CLI `bl` 走完完整闭环：数据集校验/上传 → 创建微调任务（文本 SFT/DPO/CPT、音频 CosyVoice TTS 或图像生成 Wan2.7）→ 等待训练 → 导出 checkpoint → 创建推理部署 → 等待就绪 → 交付可调用示例。也可跳过训练，直接部署基座模型。

## 功能简介

告诉 Agent「训练一个模型」或「把我的微调模型部署到百炼」，这个 Skill 会：

1. **前置检查** —— 验证认证（`bl auth status`）、查询训练能力（`bl finetune capability`），选定支持的基座与训练类型
2. **准备数据** —— 本地文件、已上传数据集或生成示例数据；提交前用 `bl dataset validate` 校验通过
3. **创建微调任务** —— `bl finetune <模态> create`，选对 `--training-type`（`sft-lora` / `sft` / `dpo` / `cpt`）与合理超参
4. **异步等待** —— 用 Monitor 脚本轮询训练状态（不阻塞），到 `SUCCEEDED` / `FAILED` / `CANCELED` 终态退出
5. **创建部署** —— `bl deploy <模态> create`，把微调（或基座）模型变成专属推理实例
6. **等待就绪** —— 轮询部署状态直到 `RUNNING`
7. **交付调用** —— 给出可直接运行的推理示例：文本模型用 `bl text chat`，音频 TTS 用 `bl speech synthesize --voice default`，图像生成用异步 API + 触发词，加常用运维命令

## 适用场景

**显式训练/部署：**
- "用我的数据微调一个模型并部署"
- "在百炼上训练 SFT/LoRA/DPO 模型"
- "把我的微调模型部署起来，能调用"
- "微调一个 CosyVoice 语音合成模型"
- "用我自己的声音数据训练一个 TTS 模型"
- "微调一个 Wan2.7 文生图/图生图模型"
- "用我自己的图片数据训练一个图像生成模型"

**隐式（描述目标，Skill 跑完整链路）：**
- "用我的客服问答训练一个推理模型"
- "在我的领域文档上继续预训练"
- "我想要一个自己部署的 Qwen 实例"
- "训练一个用我声音的语音合成模型"
- "用我的图片训练一个定制风格的文生图模型"

**直接部署基座（跳过训练）：**
- "把 `qwen3-8b` 部署成我自己的服务"

**不适用（反触发路由）：**
- 只想试模型效果 / 一次性对话 → `bailian-cli`：`bl text chat --model qwen3-8b --message "..."`
- 不知道选哪个基座 / 模型选型 → `bailian-model-recommend`
- 纯查模型参数 / 价格 / 上下文窗口 → `bailian-docs-llm-wiki`
- 已有训练任务 / 部署的查删（生命周期管理）→ `bl` 直接：`bl finetune list` / `bl deploy list` / `bl deploy delete --deployed-model <id>`
- 量化压缩（`bl finetune compress`）、吞吐预留 / ModelCode 容量（`bl deploy capacity`）→ `bailian-finetune`

> 本 skill 只负责"新建训练任务 + 新建部署 + 调用交付"闭环；全生命周期管理（list/pause/resume/delete）不在流程内。

## 安全护栏

`bl finetune <模态> create` 与 `bl deploy <模态> create` 都是真实写操作，会产生计费资源。两者都支持 `--dry-run`：先用 `--dry-run` 预览请求，再做真实预检，并设置计费闸门：

1. **预检 + dry-run 预览** —— `bl finetune capability --base-model <base>`（训练支持）、`bl deploy models --source custom|base`（可部署 + 可用 plan）、`bl deploy list --status RUNNING`（复用已有同模型部署，不再建第二个计费实例）。
2. **mu/ptu 计费闸门** —— `lora`（token 计费，闲置一般免费）是安全默认；`mu`/`ptu` 是预留资源、闲置也计费，创建前**必须取得用户显式确认**，在 agent/CI 等非交互环境**不能自动开通预留资源**。`bl deploy <模态> create` 是高风险命令，不带 `--yes` 会直接停止；先用 `--dry-run` 预览，用户确认后再加 `--yes`。
3. **账号就绪** —— 先 `bl auth status`，未认证即停。

## 使用示例

```
我有一份本地 jsonl 客服问答数据（ChatML 格式），
用 qwen3-8b 做 LoRA 微调，3 个 epoch，
然后部署起来，让我能像普通模型一样调用。
```

Skill 会走两段链路，在两处「等待」用 Monitor 异步轮询：

```
链路 A（先训练后部署）：
数据集 → finetune <模态> create → 等 SUCCEEDED → (自动导出) → deploy <模态> create → 等 RUNNING → text chat

链路 B（直接部署基座，跳过训练）：
基座 → deploy <模态> create → 等 RUNNING → text chat
```

每一步捕获正确的 id（`job_id` / `finetuned_output` → `deployed_model`），并绕开常见坑（例如直接用 `qwen3-8b-ft-...` 名字调用会 404 —— 必须先部署，再用响应里的 `deployed_model` 实例 id 调用）。

## 前置要求

- 已安装 `bl`（bailian-cli）并完成认证（`bl auth status`，或 `bl auth login --api-key sk-...`）
- 文本推理推荐基座：Qwen3 系列（`qwen3-8b` / `qwen3-14b` / `qwen3.6-flash`）
- 音频 TTS 推荐基座：`cosyvoice-v3-flash`
- 图像生成推荐基座：`wan2.7-image-pro` / `wan2.7-image`

## 内部工作流程

```
用户请求
  → 前置检查：认证 + 训练能力（listFoundationModels，走 API key）
  → 模态分发：文本 → text.md | 音频 TTS → audio.md | 图像生成 → image.md
  → 准备并校验数据集（文本 .jsonl / 音频 .zip / 图像 .zip）
  → finetune <模态> create（默认 sft-lora；CLI 值映射到服务端字段；音频/图像超参自动注入）
  → Monitor wait.sh finetune <JOB_ID>  （30s 轮询，异步）
  → 自动导出 best checkpoint（通常跳过手动导出）
  → deploy <模态> create（按模型来源和模态选 plan：文本微调用 lora/mu，音频 TTS 只支持 mu，图像生成只支持 lora）
  → Monitor wait.sh deploy <DEPLOYED_MODEL> （15s 轮询，异步）
  → 调用：文本 → text chat | 音频 TTS → speech synthesize | 图像生成 → 异步 API + 触发词
```

Skill 把完整编排和高频避坑点都固化进去（zsh 的 `status` 是只读变量、`--model` 在 `deploy <模态> create` 与推理命令里含义不同、刚到 `RUNNING` 时状态传播延迟导致 404、`lora` / `mu` / `ptu` 闲置计费差异、音频 TTS 只支持 mu plan、图像生成只支持 lora plan、图像推理需异步调用 + 触发词），让 Agent 不必重新踩坑。

## 模态扩展架构

本 Skill 采用「通用流程 + 模态参考文件」的分层设计，避免随模态增加而膨胀：

- `SKILL.md` — 通用 7 步流程骨架（所有模态共享）
- `references/text.md` — 文本模型特异性（数据格式、超参、推理命令）
- `references/audio.md` — 音频 TTS 特异性（ZIP 格式、CosyVoice 超参、speech synthesize）
- `references/image.md` — 图像生成特异性（ZIP 格式、Wan2.x 超参、异步 API + 触发词）
- `references/finetune.md` — training-type 映射表（跨模态通用）
- `references/deploy.md` — plan/deploy-spec 参考（跨模态通用）

新增模态 = 新增一个 `references/<modality>.md` 文件，主流程骨架零改动。

## License

Apache-2.0
