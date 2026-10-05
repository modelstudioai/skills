# model deployment index

百炼平台提供多种模型部署方式，支持从高吞吐保障的预置资源到按需计费的弹性调用，覆盖生产级稳定服务、私有化推理和效果验证等典型场景。所有部署均通过统一控制台或 API 管理，底层资源由平台全托管，开发者无需运维 GPU 基础设施。核心能力包括 PTU（预置吞吐）、DTU/MU（独占算力）和 Token 按量三种计费模式，以及智能路由等高级调度能力。

## 支持的模型/功能

- **预置吞吐（PTU）**：支持千问、DeepSeek、GLM、千问VL 等主流文本与多模态模型，适用于高并发、低延迟场景；支持长输入（最高 1M token）与前缀缓存折扣，详见[PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)。
- **独占算力（DTU/MU）**：DTU 面向新发布模型（按输入/输出 TPM 计费），MU 面向已有模型（按模型单元数量计费），均支持基础模型、LoRA 微调模型及用户导入模型；支持 PD 分离计算模式、自定义推理模式（Instruct/Thinking）与最长上下文配置，详见[DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)。
- **Token 按量**：仅支持 LoRA 微调模型，不使用不计费，适用于效果验证；不支持自助扩缩容，扩容需人工审核，详见[Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)。
- **智能路由**：通过 `auto-model-xxxxxx` model-code 动态路由至备选模型集中的最优模型，仅支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与文本 Chat Completions，不支持 DashScope 协议，详见[智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。
- **自定义模型导入**：支持从 OSS 导入 LoRA 模型（含 rank、词汇表、chat_template 等严格校验），不支持全参微调模型导入；导入后可在“我的模型”中统一管理并部署，详见[模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)。

> **注意**：文档 6 和文档 8 均描述模型导入流程，但文档 6 明确指出“导入全参微调后的模型属于白名单功能，如需开通请联系客户经理”，而文档 8 则表述为“当前版本支持导入 LoRA 模型，不支持导入全参微调模型”。二者存在矛盾，以文档 8 的明确否定表述为准——全参微调模型不可导入，除非获得白名单授权。

## 关键参数

| 参数 | 说明 | 取值约束 | 所属部署模式 |
|------|------|----------|--------------|
| `plan` | 计费方案标识 | `ptu` / `mu` / `lora` / `auto`（智能路由） | API 部署必需 |
| `ptu_capacity` | PTU 吞吐额度 | `{ "input_tpm": number, "output_tpm": number }`，单位为 TPM | `plan=ptu` 时必填 |
| `deploy_spec` / `model_unit_spec` | 模型单元规格 | 如 `MU1`, `MU2`, `MU9` 等 | `plan=mu` 时必填 |
| `enable_thinking` | 是否启用思考模式 | `true` / `false` | MU/DTU 部署可选；智能路由中设置为 `true` 将自动排除 non-thinking 模型 |
| `max_context_length` | 最长上下文长度 | 依模型能力而定（如千问3.8-Max 支持 1M） | MU/DTU 部署可选；智能路由上限 = 备选集中最小上下文窗口 |
| `rpm_limit` / `tpm_limit` | 服务限流阈值 | 正整数 | MU/DTU 部署可选；智能路由按实际路由模型的账号/空间配额生效 |
| `response_format` | 响应格式 | 如 `{ "type": "json_object" }` | 智能路由中仅路由至支持该参数的备选模型 |

## 使用方式

- **控制台部署**：登录[百炼专属部署控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)，选择「部署新模型」→ 选择模型 → 指定计费方式（PTU/DTU/MU/Token/智能路由）→ 填写参数 → 确认创建。部署状态变为「运行中」后即可调用，模型 Code 在部署列表页获取。
- **API 部署**：使用 `curl` 或 DashScope/OpenAI SDK 调用 `/api/v1/deployments` 接口。关键字段包括 `name`（服务名）、`model_name`（模型 ID 或 code）、`plan`（计费类型）及对应容量参数（如 `ptu_capacity` 或 `deploy_spec`）。完整示例见[API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。
- **调用已部署服务**：API 请求中 `model` 字段必须填写部署成功后生成的 **model code**（非服务名称），而非原始模型名。例如 PTU 部署 `qwen-flash-2025-07-28` 后，实际调用时 `model="qwen-flash-2025-07-28-xxxxxx"`。
- **智能路由调用**：使用 `model="auto-model-xxxxxxxx"` 发起 OpenAI 兼容请求，响应头 `x-dashscope-resolved-model` 返回实际执行模型，计费按该模型单价结算。

## 限制和注意事项

- **计费方式不可变**：服务创建后无法切换计费方式，必须下线旧服务并重新部署新服务，详见[专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **地域与协议限制**：智能路由仅支持北京（`cn-beijing`）和新加坡（`ap-southeast-1`）地域，且**仅支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与 `maas.aliyuncs.com` 域名**，不支持 DashScope 协议或 `dashscope.aliyuncs.com`。
- **模型导入约束**：LoRA 模型必须满足 rank ∈ {8,16,32,64}、词汇表与 chat_template 未修改、视觉模型 VIT 部分冻结等要求；OSS Bucket 必须添加 `bailian-datahub-access=read` 标签，且模型文件须置于子目录（非根目录）。
- **扩缩容能力差异**：
  - PTU/DTU/MU 支持自助扩缩容（手动或自动伸缩策略）；
  - Token 按量部署**不支持自助扩缩容**，扩容需在控制台提交申请并等待人工审核；
  - DTU 部署暂不支持 API 创建与管理，仅限控制台操作。
- **权限与配额**：部署前需确保业务空间已开通目标模型的调用权限；智能路由的备选模型若配额不足（RPM/TPM），可能导致路由失败；RAM 用户只能勾选其已获模型调用权限的备选模型。

## 来源文档

- [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)
- [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)
- [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)
- [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)
- [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)


