# model high speed inference

百炼平台提供多种面向高性能、高吞吐、低延迟场景的推理加速能力，涵盖专属容量保障（TPU/PTU/DTU）、协议级加速（Prime 模式）、异步批量处理（Batch）及智能动态路由等方案。开发者可根据业务对确定性、成本、延迟和效果的综合诉求，选择最匹配的部署与调用方式。

## 支持的模型/功能

百炼支持以下四类高速推理能力，覆盖不同性能与成本权衡：

- **吞吐预留（TPU/PTU）**：为指定模型锁定专属输入/输出 TPM 容量，保障高峰期不被公共限流影响，适用于流量可预估、不能接受中断的生产环境。支持标准模式与高速模式（即 PTU），后者 TPS 提升约 1.5～2 倍 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **Prime 模式**：无需额外参数，仅需将 `model` 替换为带 `-prime` 或 `-fast-preview` 后缀的专用模型 ID（如 `glm-5.2-fast-preview`），即可获得更高 TPS 输出，适用于 AI 编程助手、实时对话等对输出速度敏感的场景 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **批量推理（Batch）**：异步处理大批量非实时请求，成本约为实时推理的 50%，适用于模型评测、数据标注等离线作业。支持千问 Max/Plus/Flash 系列、GLM、DeepSeek 及多模态模型 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **智能路由**：通过固定 `auto-model-xxxxxx` model code 发起请求，系统自动分析内容并路由至备选集中最优模型（效果优先或成本优先），实现效果与成本的动态平衡 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。

> **注意**：文档 1 中“吞吐预留”与文档 8 中“高速容量（PTU）”描述的是同一能力，但文档 8 明确指出“PTU 的创建与管理已迁移至[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)页面操作”，因此以文档 1 为准，文档 8 作为补充说明，不应视为独立部署路径。

## 关键参数

| 参数 | 说明 | 取值示例 | 来源 |
|------|------|----------|------|
| `model` | 接入高速能力的核心标识 | `your-dedicated-model-code`（吞吐预留）、`glm-5.2-fast-preview`（Prime）、`auto-model-abcd1234`（智能路由） | [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)、[Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)、[智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md) |
| `input_tpm` / `output_tpm` | 吞吐预留或 DTU 部署时需显式配置的容量额度（单位：kTPM） | `"input_tpm": 10000, "output_tpm": 1000` | [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md) |
| `plan` | API 部署时指定计费模式的关键字段 | `"plan": "ptu"`、`"plan": "mu"`、`"plan": "lora"` | [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md) |
| `enable_thinking` | 控制是否启用深度思考模式（影响 token 成本与响应结构） | `true` / `false`（部分模型默认开启） | [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md) |

## 使用方式

1. **吞吐预留（推荐用于高确定性场景）**  
   在控制台创建吞吐预留实例 → 获取专属 `model code` → 将 API 请求中的 `model` 参数替换为该 code → 调用即可。注意：容量费用按购买量一次性支付，与是否调用无关 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

2. **Prime 模式（零改造接入）**  
   直接使用文档 2 中列出的 Prime 专用 model ID（如 `glm-5.2-fast-preview`），调用域名需为 `https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`，无需修改其他参数。

3. **批量推理（离线低成本场景）**  
   构造符合规范的 JSONL 文件（每行一个请求，含 `custom_id`, `method`, `url`, `body`）→ 上传至控制台或调用 Batch API → 查询任务状态 → 下载结果文件。

4. **智能路由（效果/成本自适应场景）**  
   创建路由服务获取 `auto-model-xxxxxx` code → 以该 code 发起标准 OpenAI 兼容请求 → 响应体中 `model` 字段返回实际执行模型，token 用量按实际模型计费。

## 限制和注意事项

- **容量预热**：吞吐预留实例在短时间内请求量快速拉升时需短暂预热，预热期间可能出现延迟波动，建议客户端实现请求排队或重试机制 [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **模型兼容性**：并非所有模型均支持全部高速能力。例如，`qwen3.8-max` 支持吞吐预留和批量推理，但不支持 Prime 模式；`glm-5.2` 的 `thinking_budget` 参数在吞吐预留调用时不生效；批量推理结果文件不包含 `reasoning_content` 字段 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **地域与协议约束**：智能路由仅支持北京与新加坡地域，且**仅支持 `maas.aliyuncs.com` 域名**（不支持 `dashscope.aliyuncs.com`），同时不支持 DashScope 原生协议 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。
- **计费不可变性**：部署服务的计费方式（如 PTU、MU、Token 按量）创建后无法更改，切换需先下线原服务再重新部署 [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)。
- **缓存行为差异**：吞吐预留（PTU）支持长输入阶梯系数与前缀缓存折扣，而 Prime 模式与标准按量调用无此优化，其容量消耗严格按原始 token 数计算。

## 来源文档

- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [高速容量（PTU）](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)
- [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)


