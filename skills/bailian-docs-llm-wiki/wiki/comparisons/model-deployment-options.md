# 模型部署方式对比：托管推理、压缩与高并发优化

为帮助开发者在百炼平台上高效、经济、稳定地落地大模型应用，本文系统对比三类核心部署能力：**托管推理（即标准 API 调用与专属部署）**、**模型压缩（轻量化部署）** 与 **高并发优化（Prime 模式 & 吞吐预留）**。三者定位不同：托管推理提供开箱即用的基础服务能力；模型压缩聚焦资源受限场景下的端侧/边缘适配；高并发优化则专为确定性 SLA、流量可预测的生产级负载设计。本对比不涵盖模型训练、微调或数据准备环节，仅聚焦**推理服务交付层的技术选型维度**，旨在辅助开发者根据业务特征（如延迟敏感度、流量稳定性、硬件约束、成本模型）快速决策。

## 关键维度对比表

| 维度 | 托管推理（标准/PTU/DTU/MU） | 模型压缩 | 高并发优化（Prime 模式 & 吞吐预留） |
|------|-----------------------------|-----------|----------------------------------------|
| **输入格式** | 完全兼容 OpenAI Chat Completions 协议（`messages`, `tools`, `stream` 等）；支持文本、图像（Qwen-VL）、视频（Wan3.0-video）等多模态输入（依模型能力而定） | 与原模型完全一致 —— 压缩后 endpoint 接收相同输入结构，无需修改客户端代码 | Prime：同标准 API；吞吐预留：需替换 `model` 字段为专属 model code，其余字段（含 `messages`, `stream`）完全一致 |
| **输出格式** | 标准 OpenAI 兼容响应（`choices[0].message.content`, `delta.content` 等）；流式响应结构统一 | 输出格式、字段语义、tokenization 行为与原模型完全一致（功能无损） | Prime：流式响应中额外返回 `delta.reasoning_content`（用于推理过程可视化）；吞吐预留：输出结构与基础模型一致，未声明特殊字段 |
| **支持模型** | • **标准/PTU/DTU/MU**：覆盖 Qwen、GLM、DeepSeek、Kimi、Wan 等全系列<br>• **Token 按量**：仅限 LoRA 微调模型<br>• **智能路由**：仅限文本 Chat Completions 场景 | 仅限 Qwen 系列（Qwen1.5/Qwen2/Qwen2.5/Qwen-VL）的 FP16 模型版本；不支持 LoRA 未合并权重模型 | • **Prime 模式**：专用模型 ID（如 `glm-5.3-prime`, `glm-5.2-fast-preview`, `wan3.0-video-prime`）<br>• **吞吐预留**：主流模型基础名（如 `qwen3.7-plus`, `GLM-5.2`, `deepseek-v3`），*不接受 `-prime` 或 `-fast-preview` 后缀* |
| **API 端点** | • 标准/Token 按量：`https://dashscope.aliyuncs.com/compatible-mode/v1`<br>• PTU/DTU/MU：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（地域绑定） | 与原模型部署 endpoint 完全一致（复用同一域名与路径），仅 `model_code` 不同 | • Prime：使用 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（华北2/新加坡专属域名）<br>• 吞吐预留：使用标准域名 `https://dashscope.aliyuncs.com/compatible-mode/v1`，但必须传入专属 model code |
| **计费方式** | • **标准/Token 按量**：按 token 实际消耗计费（输入/输出分开计价）<br>• **PTU**：预付费购买 TPM 容量（kTPM/月），溢出部分按量计费<br>• **DTU/MU**：预付费（DTU 按 TPM、MU 按单元数），支持 1.2 倍系数退费 | **无独立计费项** —— 压缩是部署配置选项，计费仍归属所部署模型的底层计费模式（如 PTU 或 MU） | • **Prime 模式**：按实际 token 消耗计费（同标准 API），但缓存单价独立（如 ¥4/百万 cached token）<br>• **吞吐预留**：按预购 kTPM 容量月付（输入/输出分项购买），溢出可选自动按量或限流（429） |
| **典型场景** | • 快速验证、A/B 测试、低频调用<br>• 需要物理隔离、定制化扩缩容、长上下文/前缀缓存的中高负载业务<br>• LoRA 效果试用（Token 按量） | • 边缘设备（Jetson、RK3588）、终端 App 内置推理<br>• 对首 token 延迟（TTFT）极度敏感的实时交互场景<br>• 显存受限但需保持模型能力的云上轻量服务 | • **Prime**：实时对话、Agent 多步链路、对平均 TPS 提升有明确需求但无法预估峰值的场景<br>• **吞吐预留**：金融风控、客服工单处理、SaaS 平台核心 API —— 要求刚性容量保障、零限流、SLA 可承诺 |

## 各方案适用场景建议

- **优先选择「托管推理」当**：  
  ✅ 项目处于 PoC 或灰度阶段，需快速验证效果；  
  ✅ 流量波动剧烈且不可预测（如社交类 App 的突发热点）；  
  ✅ 需要灵活切换模型（如 A/B 测试多个微调版本）；  
  ✅ 使用 LoRA 微调模型进行低成本试用（Token 按量）；  
  ❌ *不推荐*：对 P99 延迟有硬性要求（如 <300ms）、或需保障每分钟万级请求不丢包。

- **优先选择「模型压缩」当**：  
  ✅ 部署目标为边缘设备、移动端或显存 ≤24GB 的云实例；  
  ✅ 业务对首 token 延迟（TTFT）极其敏感（如语音助手唤醒响应）；  
  ✅ 已确认 Qwen 系列满足业务能力需求，且可接受 INT4 量化带来的极小精度损失（实测通常 <0.5% Acc 下降）；  
  ❌ *不推荐*：使用 GLM/DeepSeek/Kimi 等非 Qwen 模型；或需部署 LoRA 未合并权重的定制模型。

- **优先选择「高并发优化」当**：  
  ✅ **Prime 模式**：已上线标准 API，但观测到平均 TPS 不足，希望以最小改造（仅换 model ID）获得 1.5~2× 吞吐提升，且能接受平台动态资源调度；  
  ✅ **吞吐预留**：业务有明确、稳定的分钟级流量基线（如日均 500k TPM），合同要求 99.95% 请求成功率，且愿意为确定性支付预付成本；  
  ❌ *不推荐*：流量日间峰谷比 >10:1 且无法接受溢出费用（吞吐预留）；或需要跨地域复用同一 model ID（Prime 模型 ID 与地域强绑定）。

## 技术选型参考（面向开发者）

| 你的关键诉求 | 推荐方案 | 关键操作提示 |
|--------------|----------|--------------|
| “我想立刻跑通一个 Qwen2-7B 对话接口，不关心性能” | 托管推理（标准 API） | 直接调用 `dashscope.aliyuncs.com`，`model=qwen2-7b` |
| “我的 App 需在手机端运行 7B 模型，显存只有 8GB” | 模型压缩 | 在 `model.deploy` 中配置 `compression.type=int4_weight_only`，部署后使用新 `model_code` |
| “我们 SaaS 平台每天稳定消耗 200k TPM，客户合同要求 99.9% 可用性” | 吞吐预留 | 控制台创建吞吐预留实例 → 获取专属 model code → 替换所有请求中的 `model` 字段 |
| “Agent 服务当前 TPS 卡在 120，但客户抱怨响应慢，能否不改代码提速？” | Prime 模式 | 将请求中的 `model` 改为 `qwen3.7-plus-prime`（需确认地域支持），域名切至 workspace 专属地址 |
| “既要低延迟又要高可用，还能自动扩缩容应对促销高峰” | 托管推理（PTU） + 自动溢出策略 | 购买 150k TPM 基础 PTU，开启「自动溢出至按量」，配合客户端重试逻辑 |
| “我微调了一个 GLM-5.2-LoRA，想先免费试用一周” | 托管推理（Token 按量） | 部署时指定 `plan=lora`，注意：仅支持 LoRA，且一个月无调用将自动释放 |

> **重要提醒**：  
> - **模型能力一致性是底线**：所有方案均保证与基础模型在功能、上下文长度、输出格式上完全一致，性能优化不以牺牲能力为代价。  
> - **迁移成本极低**：除吞吐预留需替换 `model` 字段外，其余方案均兼容标准 OpenAI SDK 与请求体，无需重写业务逻辑。  
> - **组合使用更强大**：例如，对 `qwen3.7-plus` 启用吞吐预留保障基线容量，同时为其部署一个 INT4 压缩版本供边缘场景调用；或在 Prime 模式下启用前缀缓存进一步降低重复请求成本。  
> - **务必验证地域与模型匹配性**：Prime 模型 ID、吞吐预留地域、PTU/MU 部署地域均需显式指定且不可混用，控制台会实时校验兼容性。

## 被对比主题页

- [model high speed inference](../guides/model-high-speed-inference.md)
- [model compression](../guides/model-compression.md)
- [model deployment index](../guides/model-deployment-index.md)


