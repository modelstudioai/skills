# model high speed inference

百炼平台提供多种面向高吞吐、低延迟与确定性性能的推理加速能力，核心包括 Prime 模式（轻量级提速）、吞吐预留（TPM 专属容量保障）、PTU/DTU 专属部署（物理/逻辑资源隔离）以及智能路由与批量推理等场景化方案。所有方案均通过标准 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，无需修改客户端代码主体逻辑，仅需替换 `model` 参数或调整接入域名。

## 支持的模型/功能

- **Prime 模式**：专为输出速度敏感场景设计，TPS 提升至标准 API 的 1.5~2 倍，支持 `glm-5.2-fast-preview`、`glm-5.3-prime` 及 `wan3.0-video-prime` 等模型，[原文标题](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留（TPM Reservation）**：为指定模型锁定专属输入/输出 TPM 容量，保障高峰期不被公共限流影响；支持 Qwen3、GLM-5、DeepSeek-v4、Kimi-K 等主流模型，含“高速模式”（即 PTU）与“标准模式”两种性能档位，[原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **专属部署（PTU/DTU/MU）**：PTU（预置吞吐）与 DTU（独占吞吐）均按 TPM 计费，提供更强资源确定性；MU（模型单元）适用于需自定义性能指标的场景；三者均支持长输入、前缀缓存与 PD 分离计算，[原文标题](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)。
- **智能路由**：通过 `auto-model-xxxx` 统一入口，动态匹配备选模型集（如 `qwen3.8-flash`、`glm-5.2`、`deepseek-v4-pro-0813`），按“效果优先”或“成本优先”策略自动选模，计费按实际执行模型结算。
- **批量推理（Batch）**：异步处理大批量非实时请求，成本约为实时推理的 50%，支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus` 等 20+ 模型，但结果文件不返回 `reasoning_content` 字段。

> **注意**：文档 1 中称 `glm-5.2-fast-preview` 是 Prime 模式专用模型 ID，而文档 2 和文档 5 均指出 `glm-5.2` 本身也支持吞吐预留与 PTU 部署。二者无冲突——`glm-5.2-fast-preview` 是 Prime 模式下独立命名的优化版本，而 `glm-5.2` 是其基础模型，在吞吐预留/PTU 场景中通过专属 model code 调用，性能提升机制不同（前者为服务端推理栈优化，后者为资源隔离+预热）。

## 关键参数

| 参数 | 说明 | 示例值 | 生效范围 |
|------|------|--------|----------|
| `model` | 必填。取值为：<br>- Prime 模型 ID（如 `glm-5.2-fast-preview`）<br>- 吞吐预留生成的专属 model code（如 `tpm-glm52-abc123`）<br>- PTU/DTU 部署生成的 `deployed_model` ID<br>- 智能路由 model code（如 `auto-model-abcd1234`） | `"glm-5.2-fast-preview"` | 全局必填 |
| `base_url` | 接入域名需匹配部署类型：<br>- Prime 模式：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>- 标准吞吐预留/PTU/DTU/智能路由：`https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`<br>- DashScope 原生协议（非兼容）不支持吞吐预留与智能路由 | `"https://xxx.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"` | 全局必填 |
| `stream` | 流式响应开关。Prime 模式下若启用 `stream=true`，需分别解析 `delta.reasoning_content` 与 `delta.content` 字段 | `true` | Prime、标准部署 |
| `enable_thinking` | 控制是否启用深度思考模式。部分模型（如 Qwen3 系列）默认开启，批量推理中必须显式传入且与 `thinking_budget` 同级 | `false` | 实时推理（非 Batch） |
| `x-dashscope-ptu-overflow:true` | 响应 Header。仅当吞吐预留启用“自动溢出”策略且实际用量超限时返回，用于监控降级行为 | — | 吞吐预留（自动溢出） |

## 使用方式

1. **Prime 模式**：直接使用指定模型 ID（如 `glm-5.2-fast-preview`），无需额外参数，接入 `maas.aliyuncs.com` 域名即可。
2. **吞吐预留**：
   - 在控制台创建预留实例，选择模型、TPM 数量与溢出策略；
   - 复制生成的专属 model code；
   - 将 API 请求中的 `model` 替换为该 code，并确保 `base_url` 指向 `maas.aliyuncs.com`；
   - 注意：短时间内请求量快速拉升时存在短暂预热期，可能出现延迟波动，建议实现请求排队或重试机制。
3. **PTU/DTU 专属部署**：
   - 通过控制台或 API（`plan=ptu` 或 `plan=mu`）部署；
   - 获取 `deployed_model` 作为 model code；
   - 调用时使用该 code，`base_url` 同样须为 `maas.aliyuncs.com`；
   - DTU 部署支持更细粒度的性能配置（如 `rpm_limit`, `tpm_limit`, `max_context_length`）。
4. **智能路由**：
   - 创建后获取 `auto-model-xxxx` code；
   - 调用方式与普通模型完全一致，仅替换 `model`；
   - 响应体中 `model` 字段返回实际执行模型，`usage` 字段为真实 token 消耗。
5. **批量推理**：
   - 构造 JSONL 文件，每行包含 `custom_id`, `method`, `url`, `body`；
   - `body` 中 `model` 字段必须与文件内所有请求一致；
   - 通过 `/v1/batches` 接口提交任务，异步轮询状态后下载结果。

## 限制和注意事项

- **计费刚性**：吞吐预留、PTU、DTU、MU 均为预付费模式，创建成功即开始计费，**与是否调用无关**；即使零调用，费用也全额产生，详见 [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **模型兼容性**：Token 按量部署仅支持 LoRA 微调模型，不支持全参微调或原始预置模型；批量推理不返回 `reasoning_content`，需实时 API 获取思考过程。
- **地域约束**：智能路由仅支持华北2（北京）与新加坡地域；吞吐预留的 8 小时时段购买仅限每日 22:00–00:00 下单；所有 `maas.aliyuncs.com` 域名调用均不支持 `dashscope.aliyuncs.com` 的原生协议。
- **缓存与长输入**：PTU/DTU 支持前缀缓存折扣（如 `glm-5.2` 缓存命中部分按 25% 折算容量）与长输入阶梯系数（如 `qwen3.7-flash` 输入 >256K 时系数升至 6x），需在容量计算器中综合评估。
- **错误处理**：智能路由在目标模型返回 429、400、403、404、500 或超时时**不触发故障切换**，错误直接透出；吞吐预留“仅使用预留容量”策略下超限返回 429，不产生额外费用。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [高速容量（PTU）](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)
- [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)


