# 模型路由

模型路由（Model Routing）是百炼平台提供的智能调度能力，用于在多个候选模型之间自动选择最适配当前请求的模型，实现效果、成本、延迟或资源保障等维度的动态优化。它不改变标准 API 调用方式，开发者仅需指定一个统一的路由模型 ID（如 `auto-model-20260908`），平台即在服务端完成模型匹配与执行，并通过响应头 `x-dashscope-resolved-model` 透出实际执行模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能效果/成本权衡**：当业务对输出质量敏感但预算有限时，可启用「效果优先」或「成本优先」策略的模型路由。例如，对相同 prompt，路由系统可能将简单问答分发至 `qwen3.8-flash`（低延迟低成本），而将复杂推理任务交由 `glm-5.2` 或 `deepseek-v4-pro-0813`（高能力高成本）。
- **高可用与容灾**：路由组内模型具备能力同构性（如均支持 `function-calling` 和 `structured-outputs`）。当主模型临时不可用或触发限流时，系统自动降级至备选模型，保障调用成功率，无需客户端重试或切换 endpoint。
- **灰度发布与A/B测试**：通过配置路由权重（如 `qwen3.8-max:70%, glm-5.2:30%`），可将流量按比例分发至新旧模型版本，验证性能、准确率与计费表现，支撑平滑升级。
- **多厂商能力聚合**：路由组可跨供应商组合模型（如 `qwen` + `zhipu-ai` + `moonshot-ai`），屏蔽底层异构性，对外提供统一能力接口，降低业务方模型选型与维护成本。
- **与加速能力协同**：模型路由与 Prime 模式、吞吐预留（PTU）、DTU 等加速方案正交——路由决策发生在请求入口，后续执行仍可叠加专属算力保障；但注意：路由模型本身**不支持**直接配置 PTU/DTU，需在路由组内各成员模型上单独开通。

> ⚠️ 使用约束：  
> - 仅支持 OpenAI 兼容模式调用，Endpoint 必须为 `https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`；不支持 `dashscope.aliyuncs.com` 域名。  
> - 不适用于专用模型（如 `qwen-ocr`, `gui-plus`, `qwen-intent`）和异步模型（如 `wanx2.1-t2i-turbo`），这些模型需显式指定 `model` 并走独立路径。  
> - 路由结果以响应头 `x-dashscope-resolved-model` 为准，计费、配额消耗、日志追踪均基于该实际模型。

## 关键参数和配置

- **路由模型 ID（必填）**：`model=auto-model-xxxx`，由控制台创建路由组后生成，格式固定，不可自定义。  
- **策略标识（可选）**：通过请求 Header 设置 `X-DashScope-Model-Routing-Strategy: effect`（效果优先）或 `cost`（成本优先）；默认为 `effect`。  
- **强制指定子模型（调试用）**：Header 中添加 `X-DashScope-Force-Model: qwen3.8-max` 可绕过路由逻辑，强制使用指定模型（仅限调试，生产环境禁用）。  
- **响应头反馈（只读）**：
  - `x-dashscope-resolved-model`: 实际执行的模型 ID（如 `qwen3.8-flash`），用于监控、计费核对与问题定位；  
  - `x-dashscope-routing-group-id`: 当前生效的路由组唯一标识，便于审计策略版本。

> 📌 注意：模型路由本身无独立 API 配置接口。所有管理操作（创建/更新/删除路由组、增删成员、调整权重）均通过百炼控制台完成，或调用内部管理 API（非公开 SDK 接口）。

## 面向开发者，简洁实用

- ✅ **快速接入**：替换原有 `model=qwen-plus` 为 `model=auto-model-20260908`，一行代码升级，零逻辑改造。  
- ✅ **可观测性**：务必检查响应头 `x-dashscope-resolved-model`，确认路由是否按预期生效；建议在日志中记录该字段，用于效果归因与成本分析。  
- ✅ **调试技巧**：开发阶段用 `X-DashScope-Force-Model` 锁定模型复现问题；上线后移除该 Header，交由路由系统决策。  
- ❌ **避免误用**：不要将路由模型 ID 用于模型管理 API（如 `/models/permissions` 或 `/models/limits`）——这些接口只接受真实模型 ID；路由模型本身不可授权、不可限流。  
- 💡 **最佳实践**：结合模型管理能力，为路由组内每个成员模型单独配置合理的 QPM/TPM 限额，防止某成员过载拖累整体路由稳定性。

## 关联主题页

- [model management](../api/model-management.md)
- [more about models](../api/more-about-models.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [more models](../api/more-models.md)
- [application component api reference](../api/application-component-api-reference.md)


