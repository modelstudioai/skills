# 文本模型参考

> 本文件补充 [`SKILL.md`](../SKILL.md) 中文本模型微调链路的模态特异性细节（数据格式、模型、超参、推理）。通用流程见 SKILL.md。

## 适用场景

文本对话/推理模型的微调与部署。当前常见基座：

| 基座模型 | 说明 |
|---|---|
| `qwen3-8b` | Qwen3 8B，支持思维链，通用对话 |
| `qwen3-14b` | Qwen3 14B，更强推理 |
| `qwen3.6-flash` | Qwen3.6 Flash，轻量快速 |

## 数据格式

文本模型数据为 `.jsonl` 文件，每行一个 JSON 对象。支持的 schema：

| Schema | 每行格式 | 适用训练类型 |
|---|---|---|
| `chatml` | `{"messages":[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}` | sft / sft-lora |
| `dpo` | `{"messages":[...],"chosen":"...","rejected":"..."}` | dpo / dpo-lora |
| `cpt` | `{"text":"..."}` | cpt |

CLI 自动探测 schema（按 chosen/rejected → text&&!messages → chatml 顺序），也可显式指定 `--schema`。

### 校验

```bash
bl dataset validate --file <jsonl-path>              # 自动探测 schema
bl dataset validate --file <jsonl-path> --schema dpo  # 显式指定
```

## 创建训练任务

```bash
bl finetune text create \
  --base-model qwen3-8b \
  --datasets <path-or-file-id> \
  --training-type sft-lora \
  --n-epochs 3 \
  --output json
```

### training-type 选择

详见 [`finetune.md`](finetune.md)。要点：
- `sft-lora`（默认）：LoRA，便宜快，大多数场景
- `sft`：全参 SFT，效果上限高，成本显著增加
- `dpo-lora` / `dpo`：偏好对齐，需 preference 数据
- `cpt`：继续预训练，注入领域知识

### 超参建议

- `--n-epochs` 默认 3；小数据集（几百条）3 够用，过拟合降到 1-2
- `--learning-rate` 必须**字符串**（如 `"1e-4"`）避免 JSON 精度丢失；LoRA 默认 `3e-4`
- `--batch-size` 一般不手动设（<100KB 自动设 8）
- `--validations <path>` 可选，传验证集观察指标

## 部署

```bash
bl deploy text create \
  --model-name <finetuned_output> \
  --display-name <display-name> \
  --plan lora \
  --output json \
  --yes
```

- `--yes` 必填（高风险命令）：先用 `--dry-run` 预览请求，用户确认后再加 `--yes`

- 文本微调模型支持 `lora`（默认，token 计费）和 `mu` plan
- `lora` 安全默认，闲置一般不计费
- `mu` plan 需 `--deploy-spec` + `--capacity`，详见 [`deploy.md`](deploy.md)

## 推理与调用

```bash
bl text chat --model <DEPLOYED_MODEL> --message "你的问题"
```

- `--model` 必须用 `deploy text create` 响应中的 `deployed_model`，**不是** `finetuned_output`
- 建议带一个推理类问题演示效果
