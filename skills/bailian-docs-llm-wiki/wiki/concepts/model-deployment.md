# 模型部署

模型部署是将训练或调优完成的模型（包括基础模型、微调模型、压缩模型等）发布为稳定、可扩展、生产就绪的 API 服务的过程。它在百炼平台中是连接模型能力与业务应用的关键环节，决定了服务的性能、成本、安全性和运维可控性。

## 在百炼平台的不同场景中，这个概念如何使用

- **基础模型服务化**：直接部署通义千问系列（如 `qwen-max`、`qwen-plus`）等系统预置模型，适用于快速验证或通用能力接入。支持按需（`on_demand`）和 TPM 预留（`tpm_reserved`）两种模式，前者免预置、有冷启动；后者保障最低吞吐，适合流量可预期的线上服务。

- **微调模型上线**：Fine-tuning 任务成功完成后，生成的 `ft-xxx` 模型 ID 可一键部署为专属 API 服务。该过程继承微调时的领域适配能力，并支持灰度发布、多版本路由等生产级功能。

- **压缩模型推理**：经 AWQ/GPTQ 量化压缩后的轻量模型（如 `qwen2-7b-int4-awq`）可作为独立模型 ID 直接部署，无需额外转换——部署后调用方式与原模型完全一致，仅需替换 `model` 参数。

- **合规与安全集成**：所有部署实例默认启用 HTTPS 加密；通过配置 `enable_security_check: true` 和 `security_level`，可在 API 层实时触发内容安全护栏；开启私网访问后，服务 endpoint 仅限 VPC 内网调用，满足金融、政务等强合规场景要求。

- **资源与成本精细化控制**：根据业务特征选择部署类型：  
  - 流量平稳 → 选用 `ptu` 或 `dtu` 模式锁定吞吐/算力；  
  - 突发或低频 → 选用 `token_based` 按量计费；  
  - 高 SLA 要求 → 选用 `dedicated` 专属实例，保障独占 GPU 与低延迟。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `deployment_type` | string | 是 | 取值：`dedicated`（专属）、`ptu`（预置吞吐）、`dtu`（独占算力）、`token_based`（按量）、`on_demand`（按需）、`tpm_reserved`（TPM 预留） |
| `model_id` | string | 是 | 模型唯一标识，支持系统模型（`qwen-max`）、微调模型（`ft-xxx`）、压缩模型（`qwen2-7b-int4-awq`）等 |
| `instance_type` | string | 否（`dedicated`/`dtu` 必填） | GPU 实例规格，如 `ecs.gn7i-c16g1.4xlarge`，需匹配模型显存需求 |
| `ptu_capacity` / `tpm_capacity` | int | 按模式必填 | `ptu`: 最小 10（1 PTU ≈ 10 QPS 基准）；`tpm`: 最小 100（单位：tokens/minute） |
| `min_replicas` / `max_replicas` | int | 否 | 仅 `dedicated` 支持固定副本数；其余类型自动扩缩容 |
| `enable_security_check` | boolean | 否 | 默认 `false`；设为 `true` 启用输入输出 AI 安全护栏 |
| `security_level` | string | 否（启用护栏时建议显式指定） | `"strict"` / `"balanced"`（默认） / `"relaxed"` |

> ⚠️ 注意：  
> - 所有部署均要求模型状态为 `Published`；草稿或校验失败模型不可部署。  
> - 模型版本更新后，已有部署**不会自动升级**，必须手动执行 `bailian deploy --update` 或重建。  
> - `token_based` 不支持流式响应（`stream: true`）和长上下文（>32k token）；`on_demand` 存在 <3s 冷启动延迟。

## 面向开发者，简洁实用

- ✅ **起步最快**：确认模型已发布 → 运行 `bailian deploy --model-id qwen-max --deployment-type ptu --ptu-capacity 30` → 获取 endpoint 直接调用。  
- ✅ **调试友好**：部署后立即在控制台「模型部署」页查看实时 QPS、延迟、错误率；也可调用 `/v1/deployments/{id}/metrics` 接口集成监控系统。  
- ✅ **灰度可控**：结合「模型路由」功能，将新部署的微调模型以 5% 流量接入，验证效果后再全量切换。  
- ✅ **安全开箱即用**：只需在请求 body 中添加 `"enable_security_check": true`，即可启用国家网信办要求的 12 类内容风险识别。  
- ❌ **避坑提示**：  
  - 不要使用旧版 Quick Start CLI（参数已不兼容 v2.3+ SDK）；请统一使用 `bailian deploy` 命令；  
  - `dtu` 部署绑定 GPU 型号，变更 `instance_type` 必须先删除再重建；  
  - 私网访问需提前在控制台「网络配置」中绑定交换机，API 调用时无法动态开启。

## 关联主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [model production](../api/model-production.md)
- [fine tuning](../guides/fine-tuning.md)
- [model compression](../guides/model-compression.md)
- [security and compliance](../guides/security-and-compliance.md)


