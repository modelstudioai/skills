# 模型部署与高速推理

模型部署是将百炼平台的预置模型、微调模型或导入模型发布为独立、资源专享的在线推理服务的过程；高速推理则是在部署之上（或独立）为调用提供容量刚性兑付与更高输出速度的一组能力。两者共同解决生产环境对高并发、低延迟和确定性吞吐的需求。

## 在百炼平台的使用场景

模型生产的完整链路为：**模型调优（Fine-tuning）→ 模型压缩（可选量化）→ 模型部署 → 推理调用**。开发者可通过调优 API 定制专属模型，用模型压缩降低部署规格与成本，再通过部署 API 发布为在线服务，最后调用端点进行推理。

围绕"部署 + 推理"，平台提供多种资源与容量形态，按业务诉求选型：

- **需要私有推理服务、资源独占**：用模型部署（PTU / 模型单元 / 按 Token）创建专属服务。
- **只需锁定容量、抵御公共限流**：用 **TPM 预留**，为指定模型预留专属吞吐量。
- **只需更快出字、计费不变**：用**快速模式（Fast mode）**，把输出速度提升到标准 API 的 1.5~2 倍。
- **需要降低部署成本**：先对微调模型做**模型压缩（量化）**，再部署。

## 部署的三种计费方式

计费方式在服务创建时选定，创建后不可更改（需下线后重新部署）：

- **预置吞吐（PTU）**：预留资源保障特定 TPM，额度内不限速，TPS 通常较按 Token 提升约 1.5~2.0 倍。适合流量稳定、需并发/延迟确定性的高负载场景。支持按小时后付费与按天预付费。
- **模型单元（MU）**：按时长 × 单元数计费，资源独占、性能可自定义，支持 PD 分离（拆分 Prefill/Decode 降低首 Token 延迟）。适合私有微调模型与长时任务。支持按分钟后付费与按月预付费。
- **按 Token 使用量**：仅对 SFT 高效训练（LoRA）后的自定义模型开放，主要用于调优效果验证。

> 预付费无法提前退费，首月内提前退订按单价 1.2 倍计费；PTU 超出购买吞吐或输入超模型上限时，自动切换为按量付费（响应头 `x-dashscope-ptu-overflow:true`）。

## PTU 长输入与前缀缓存

- **长输入阶梯系数**：部分模型对超过 32K 的输入按更高系数折算 TPM（如 glm-5.1 在 [32K, 200K] 区间输入 1.33 / 输出 1.17），部分模型无阶梯（1.0）。
- **前缀缓存折扣**：命中缓存的输入 token 按折扣系数消耗额度（glm-5.1 为 0.2，deepseek-v4-pro 低至 0.08），显著降低多轮对话与重复前缀场景成本。
- **额度识别字段**：`service_tier`（`ptu-standard` 走 PTU 额度）、`provisioned_tokens`（折算后实际消耗）、`cached_tokens`（缓存命中数）。这些字段在 OpenAI Chat 兼容、OpenAI Responses、Anthropic 兼容、DashScope 四种协议下的 JSON 路径不同，需分别读取；Anthropic 兼容格式暂不返回 `cached_tokens`。

建议创建或扩容前用控制台**容量计算器**（依据 RPM、平均输入/输出长度、预估缓存命中率）估算所需 TPM，避免额度不足产生意外按量费用。

## 模型导入（LoRA）

部署自训练模型前需从 OSS 导入 LoRA 微调版本，核心要求：

- 仅支持 **LoRA**，不支持全参微调；必需文件 `adapter_model.safetensors` 与 `adapter_config.json`。
- **rank** 必须为 8/16/32/64 之一，且同模型各 LoRA 层 rank 一致。
- 不得新增 token、修改 vocab 或 chat_template，须与开源基础模型完全一致；VL 模型必须冻结 VIT（含 `visual` 权重则无法导入）。
- **OSS 前提**：Bucket 需添加 `bailian-datahub-access` 标签（值 `read`）、文件须放子目录、不支持归档类存储；首次导入需完成服务关联角色授权。

支持基础模型涵盖千问3、千问3-VL、千问2.5、千问2.5-VL 系列。

## 使用 API / 命令行部署

部署接口统一为 `POST https://dashscope.aliyuncs.com/api/v1/deployments`（仅华北2·北京，需先配置 `DASHSCOPE_API_KEY`），通过 `plan` 字段区分计费方式：

- **PTU**：`"plan": "ptu"`，配合 `ptu_capacity.input_tpm` / `output_tpm`。
- **模型单元**：`"plan": "mu"`，配合 `deploy_spec`（如 `MU1`）、`capacity`（副本数）、`enable_thinking`、`max_context_length`、`rpm_limit`、`tpm_limit` 等。
- **按 Token（LoRA）**：`"plan": "lora"`，`capacity` 必填但无效，扩缩容需在控制台申请。

部署自定义模型时 `model_name` 使用**模型 ID**（在"我的模型"页面获取）。查询状态用 `GET /deployments/{id}`。

## 模型压缩（量化）降本

模型压缩特指量化（不含剪枝/蒸馏），将全精度微调模型转为低精度版本以降低部署所需 MU 规格。例如 qwen3.5-flash 微调模型压缩前 MU1*2（108 元/小时），压缩后 MU8*1（47 元/小时），成本节省约 56%。压缩不可逆，压缩后不支持继续微调或二次压缩，仅华北2（北京）可用。量化模板中 MU 编号越大规格越小、成本越低但精度损失可能越大；校准数据应选择与推理场景语义相近的数据集。

## 高速推理能力

### TPM 预留：锁定专属容量

- **专属模型 code**：创建预留后系统生成专属 `model` code，需将请求中的 `model` 替换为该 code 才命中预留容量。
- **超额不中断**：超出预留自动降级为公共池按量计费，无需改代码，可在详情页查看超额降级统计。
- **计费**：按 kTPM（1 kTPM = 1000 Tokens/分钟）预付费，部署成功即计费。
- **管理**：支持在线扩缩容；退订不可恢复，缩容/退订退费按已用部分 1.5 倍系数结算；到期后 2 小时内可调用，2~14 小时转已停止（可续费），14 小时后删除。

### 快速模式（Fast mode）：更高输出速度

当前处于 **preview 阶段**，面向 AI 编程助手、Agent 多步推理、实时对话等对输出速度敏感的场景：

- **高速输出**：TPS 达标准 API 的 1.5~2 倍（约 80~100 TPS）。
- **计费不变**：仍按输入/输出 token 计费。
- **特殊限流**：超出 TPM 不立即限流，请求进入排队队列（区别于 TPM 预留的"超额降级按量"）。
- **使用方式**：将 `model` 指定为支持快速模式的 model ID（如 `glm-5.2-fast-preview`），域名格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。`glm-5.2` 默认返回 `reasoning_content`，[流式输出](streaming.md)时思考与回答分别通过 `delta.reasoning_content` 与 `delta.content` 推送。

## 选型建议

- 追求成本优化且流量波动大：**按量付费**。
- 流量可预估、不能接受公共限流：**TPM 预留**。
- 高吞吐 + 高性能确定性：**PTU 专属部署**。
- 只想更快出字、代码改动最小：**快速模式**。
- 私有微调模型且要降本：先**模型压缩**再按 **MU** 部署。

## 关联主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [model production](../api/model-production.md)
- [model compression](../guides/model-compression.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


