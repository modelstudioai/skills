# 模型部署

模型部署是将训练或调优完成的模型（包括预置大模型、LoRA/全参微调模型、OSS导入模型及量化压缩模型）发布为稳定、可扩展、可计费的在线推理服务的关键环节。它标志着模型从开发态进入生产态，是百炼平台模型生产链路（Fine-tuning → Import → Compression → Deployment）的最终交付步骤。

## 在百炼平台的不同场景中，这个概念如何使用

- **面向生产服务**：作为专属推理服务统一入口，支持 PTU（预置吞吐）、DTU/MU（独占算力）和 Token 按量三种核心部署模式，分别适配高并发低延迟、强隔离SLA保障、低成本验证等典型业务需求。
- **多模态全覆盖**：支持文本、图像、视频、语音四类生成模型的一致化部署流程（如 `qwen3.8-max`、`wan2.7-i2v`、`cosyvoice-v3-flash`），所有部署接口当前仅在华北2（北京）地域开放（PTU 部署除外，支持跨地域）。
- **与加速能力协同**：部署后的服务可叠加启用「高密推理」（Prime 模式或 TPM 预留），进一步降低首 token 延迟或保障最低吞吐水位，但需注意该能力仅对部分 Qwen 系列基础模型生效，不适用于自定义微调模型。
- **与智能路由集成**：无需独立部署，通过 `auto-model-xxxx` 这类路由模型 Code 即可动态分发请求至多个已部署模型，实现灰度发布、AB测试与故障自动降级。
- **作为模型压缩下游动作**：量化压缩产出的新模型（如 `my-qwen-ft-awq8`）必须通过模型部署才能对外提供服务，压缩本身不产生可调用端点。

## 关键参数和配置

| 参数 | 说明 | 必填性 | 所属部署模式 | 注意事项 |
|------|------|--------|----------------|----------|
| `plan` | 部署计费方案标识 | 是 | 全部 | 取值：`ptu` / `mu` / `lora` / `auto-router`；创建后不可变更 |
| `ptu_capacity` | 预置吞吐额度（输入/输出 TPM） | `plan=ptu` 时必填 | PTU | 如 `{ "input_tpm": 10000, "output_tpm": 1000 }`；单位为 kTPM |
| `deploy_spec` 或 `model_unit_spec` | 独占算力规格模板 | `plan=mu` 时必填 | MU/DTU | 如 `"MU1"`、`"MU2 x 8"`；决定单副本算力与 `capacity` 约束规则 |
| `capacity` | 模型单元数量（MU）或 LoRA 实例数（Token 按量） | `plan=mu` 或 `plan=lora` 时必填 | MU / Token 按量 | `mu` 下取值受 `deploy_spec` 约束（如 `MU2` 要求为 8 的倍数）；`lora` 下通常固定为 `1` |
| `enable_thinking` | 是否启用思考模式（影响推理路径与计费） | 否（默认 `false`） | MU / DTU / Token 按量 | 需模型显式支持，调用时生效 |
| `max_context_length` | 最长上下文长度（单位：token） | 否 | MU / DTU | 依模型能力而定（如 `qwen3.8-max` 支持 1M），超出将触发降级 |
| `rpm_limit` / `tpm_limit` | 服务级限流阈值 | 否 | MU / DTU | 整数，用于防刷或资源保护；建议结合业务峰值设置 |

> ⚠️ 提示：  
> - 所有部署均需使用**部署成功后生成的模型 Code**（非模型名称）进行调用，格式如 `qwen3-8b-ptu-xxxxx` 或 `auto-model-xxxx`；  
> - 调用域名须匹配部署地域（如北京地域使用 `cn-beijing.maas.aliyuncs.com`）；  
> - Token 按量部署**仅支持 LoRA 微调模型**，且不支持自助扩缩容；  
> - 智能路由（`auto-router`）不占用独立资源，按实际调用模型计费。

## 面向开发者，简洁实用

- ✅ **快速上手**：控制台一键部署（[专属部署控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)）或调用 `/api/v1/deployments` API，5 分钟内获得可用 endpoint。  
- ✅ **调试友好**：部署状态实时可见（`创建中` → `运行中` → `异常`），失败时控制台直接展示错误原因（如权限不足、模型不支持、地域不可用）。  
- ✅ **调用标准**：推理请求完全兼容 OpenAI 格式，只需将 `model` 字段替换为部署生成的模型 Code，其余参数（`messages`、`temperature` 等）保持不变。  
- ✅ **运维可控**：支持通过控制台或 API 对服务进行启停、扩缩容（MU/PTU）、限流配置与日志查看，无须接触底层基础设施。  
- ❌ **避坑提醒**：  
> - 切勿复用模型名称（如 `qwen3.8-max`）代替部署 Code，否则请求将被路由至共享池，无法享受专属资源与 SLA；  
> - 切换部署模式（如从 `lora` 改为 `mu`）必须先下线旧服务再新建，平台不支持原地升级；  
> - 所有部署操作均需确保当前工作空间已开通目标模型的调用权限，否则返回 `Workspace xxx does not have deployment privilege for model xxx`。

## 关联主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [model production](../api/model-production.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [fine tuning](../guides/fine-tuning.md)
- [model compression](../guides/model-compression.md)


