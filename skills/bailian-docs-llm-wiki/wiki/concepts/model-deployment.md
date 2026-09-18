# 模型部署与加速

模型部署与加速是百炼平台中将训练/调优完成的模型转化为稳定、高效、可生产调用服务的核心能力集合，涵盖资源调度策略、性能优化路径、容量保障机制与计费模型的统一抽象。它不改变模型本身的能力边界，而是通过底层基础设施编排与推理引擎优化，在满足业务SLA的前提下，实现吞吐（TPS/TPM）、延迟（首Token/端到端）、成本（单位token或预付额度）三者的最优平衡。

## 在百炼平台的不同场景中，这个概念如何使用

模型部署与加速不是单一功能，而是按业务需求分层落地的**能力矩阵**，开发者应根据流量特征、稳定性要求与成本敏感度选择对应方案：

- **轻量级提速（无容量承诺）**：选用 **Prime 模式**，适用于对响应速度有感知但可接受弹性波动的场景（如AI编程助手实时补全、客服对话流式响应）。只需将请求中的 `model` 替换为带 `-prime` 后缀的专用ID（如 `qwen3.8-max-prime`），零改造接入，性能提升1.5~2倍，计费与标准API完全一致。

- **刚性容量保障（生产级SLA）**：选用 **吞吐预留（PTU）**，适用于SaaS服务、核心业务链路等要求“绝不限流”的场景。需在控制台创建预留实例，配置输入/输出TPM（kTPM单位），获取专属 `model_code`（如 `tpm-reserved-abc123`）后替换调用。该模式提供逻辑/物理隔离，溢出行为可配置（默认自动切至按量），是唯一规避公共池限流的方案。

- **专属算力控制（高定制化）**：选用 **MU（Model Unit）部署**，适用于需精细控制GPU规格、支持长上下文（最高1M token）、要求PD分离降低首Token延迟、或需独立限流/扩缩容的场景。通过 `deploy_spec`（如 `MU5`）指定算力单元，`max_context_length` 等参数可显式配置，适合全参微调模型或LoRA模型的生产部署。

- **效果验证与多租户轻量服务**：选用 **Token按量部署（LORA）**，仅支持LoRA微调模型，按实际token用量计费，不调用不计费。适合A/B测试、灰度发布或中小客户多租户共享场景，但不支持自助扩缩容。

> ⚠️ 注意：**Prime 模式与吞吐预留（PTU）不可混用**——前者是预置优化模型别名，后者是运行时生成的容量绑定标识；`glm-5.2-fast-preview` 与 `GLM-5.2`（预留对象）逻辑不同，调用时必须严格匹配所选方案的 `model` 字符串。

## 关键参数和配置

| 场景 | 关键参数 | 说明 | 典型值示例 |
|------|----------|------|------------|
| **所有部署方式** | `model` | 必填，模型唯一标识符 | `qwen3.8-max-prime`, `tpm-reserved-abc123`, `qwen3-8b-mu-xyz` |
| **PTU / 吞吐预留** | `ptu_capacity` | 吞吐配额，单位kTPM（1000 tokens/分钟） | `{"input_tpm": 20000, "output_tpm": 2000}` |
| **MU 部署** | `deploy_spec` | 算力单元规格 | `"MU2"`, `"MU9"` |
| | `max_context_length` | 最大上下文长度（仅MU支持） | `1048576`（即1M token） |
| **通用控制** | `enable_thinking` | 是否启用思考模式（影响计费与性能） | `true` / `false` |
| **异步任务（视频/图像）** | `aigc_config` | 提示词生成策略（视频生成必需） | `{"use_input_prompt": false, "prompt": "..."}` |

> ✅ 所有部署均通过统一控制台或 `/api/v1/deployments` API 创建，无需自行运维GPU；部署成功后，通过控制台「部署列表」获取 `model_code`，直接用于标准DashScope或OpenAI兼容接口调用。

## 面向开发者，简洁实用

- **选型口诀**：  
  → 要快不要稳？→ 用 **Prime**（改一个 `model`，立刻生效）  
  → 要稳不能抖？→ 用 **PTU**（控制台配TPM，拿专属code）  
  → 要控要长要低首延？→ 用 **MU**（选MU规格，配max_context_length）  
  → 只验证不长期？→ 用 **LORA**（按token付费，开箱即用）

- **避坑提醒**：  
  - Prime 模式**不隔离资源**，高峰仍可能被限流；PTU/MU才是真隔离。  
  - PTU 和 MU 的 `model_code` 由系统生成，**不可手写或猜测**，务必从控制台复制。  
  - 所有部署均**不支持创建后切换计费模式**（如PTU→MU），需下线重建。  
  - 华北2（北京）是当前绝大多数部署能力的**唯一可用地域**，跨地域调用会失败。  
  - 调用含OSS文件的模型（如多模态）时，**必须添加Header**：`X-DashScope-OssResourceResolve: enable`。

- **快速起步**：  
  1. 登录 [百炼控制台 > 模型推理 > 专属部署](https://bailian.console.aliyun.com/cn-beijing/model/deploy)  
  2. 选模型 → 选方案（PTU/MU/LORA）→ 填参数 → 创建  
  3. 复制生成的 `model_code`  
  4. 用 DashScope SDK 发起请求（`model` 参数替换即可）：  
     ```python
     response = dashscope.Generation.call(
         model="tpm-reserved-abc123",  # ← 替换为你自己的model_code
         prompt="你好",
         stream=True
     )
     ```

## 关联主题页

- [model high speed inference](../guides/model-high-speed-inference.md)
- [model deployment index](../guides/model-deployment-index.md)
- [model production](../api/model-production.md)
- [preparations](../api/preparations.md)
- [more about models](../api/more-about-models.md)


