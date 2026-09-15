# model deployment 1

百炼平台的 model deployment 1 是面向生产环境的专属推理服务部署能力，提供资源隔离、性能保障与灵活计费的统一入口。它覆盖 PTU（预置吞吐）、DTU/MU（独占算力）和 Token 按量三种核心部署模式，支持预置模型、LoRA 微调模型及部分导入模型的上线与运维。所有部署均通过百炼控制台或 API 统一管理，计费方式在创建后不可变更。

## 支持的模型/功能

- **PTU 预置吞吐**：适用于高并发、低延迟场景，支持千问3.8-Max、qwen3.7-plus-2026-05-26、deepseek-v4-flash 等主流大模型，且明确支持长输入（最高 1M token）与前缀缓存 [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
- **DTU/MU 独占算力**：提供物理级资源隔离，支持基础模型与自定义模型（含 LoRA/全参微调），DTU 按输入/输出 TPM 计费，MU 按模型单元数量计费；支持 PD 分离计算模式与思考/非思考推理模式切换 [独占算力部署（DTU）](../../raw/model-user-guide/model-deployment-1/dtu-model-deployment.md)。
- **Token 按量部署**：仅限 LoRA 微调模型，不使用不计费，适用于效果验证与低成本轻量场景；但不支持自助扩缩容，需人工审核扩容申请 [Token 按量部署](../../raw/model-user-guide/model-deployment-1/model-deployment-token.md)。
- **智能路由**：非独立部署模式，而是动态路由服务，通过 `auto-model-xxxx` model-code 将请求分发至备选模型集（如 qwen3.8-max、deepseek-v4-flash-0731 等），按实际调用模型计费，本身不额外收费 [智能路由](../../raw/model-user-guide/model-deployment-1/model-routing.md)。
- **模型来源**：支持平台预置模型、百炼调优模型（SFT/LoRA）及从 OSS 导入的 LoRA 模型；全参微调模型导入为白名单功能，需联系客户经理开通 [我的模型](../../raw/model-user-guide/model-deployment-1/my-model-center.md)。

> **注意**：文档 1 中称“部分预置模型与所有调优后模型”支持 PTU，但文档 2 的价格表与文档 4 的支持列表均明确限定 PTU 仅支持特定版本（如 `qwen3.7-plus-2026-05-26`），且 Token 按量部署明确限定“仅支持 LoRA 微调模型”。因此，“所有调优后模型”为过时表述，应以各部署模式下具体支持的模型代码为准。

## 关键参数

| 参数 | 说明 | 取值约束 | 所属模式 |
|------|------|----------|----------|
| `plan` | 部署计费方案标识 | `ptu` / `mu` / `lora` / `auto-router` | API 部署必需 [API 部署指南](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `ptu_capacity` | PTU 吞吐额度配置 | `{ "input_tpm": 10000, "output_tpm": 1000 }`，单位为 TPM | PTU 模式 |
| `deploy_spec` / `model_unit_spec` | MU 规格标识 | 如 `"MU1"`、`"MU2 x 8"`，决定单副本算力 | MU 模式 |
| `enable_thinking` | 是否启用思考模式 | `true` / `false`，影响推理路径与计费单价 | MU / DTU / Token 模式（部分模型支持） |
| `max_context_length` | 最长上下文长度 | 依模型能力而定（如 qwen3.8-max 支持 1M），超出将触发降级 | MU 模式（部分模型支持） |
| `rpm_limit` / `tpm_limit` | 服务级限流阈值 | 整数，用于限制每分钟请求数或 Token 数 | MU 模式（部分模型支持） |
| `capacity` | Token 按量模式占位参数 | 必填但无效，值任意（如 `1`） | Token 模式 |

## 使用方式

1. **控制台部署**：登录[专属部署控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)，选择「部署新模型」→ 填写服务名称 → 选择模型 → 选择计费方式（PTU/DTU/MU/Token）→ 配置对应参数（如吞吐额度、模型单元规格）→ 确认创建。部署状态变为「运行中」即成功。
2. **API 部署**：使用 `curl` 或 DashScope SDK 调用 `/api/v1/deployments` 接口，必须指定 `plan` 字段，并按模式传入对应参数（如 `ptu_capacity` 或 `deploy_spec`）。示例详见 [API 部署指南](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
3. **调用已部署服务**：推理时 `model` 参数必须使用部署成功后生成的 **模型 Code**（非模型名称），该 Code 在控制台部署列表或 API 返回体 `deployed_model` 字段中获取；调用域名需匹配部署地域（如北京用 `cn-beijing.maas.aliyuncs.com`）。
4. **智能路由调用**：直接使用 `auto-model-xxxx` model-code 发起 OpenAI 兼容或 DashScope SDK 请求，无需修改业务逻辑；响应头 `x-dashscope-resolved-model` 返回实际执行模型。

## 限制和注意事项

- **计费不可变**：服务创建后计费方式无法更改，切换需先下线旧服务再新建 [专属部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **模型权限**：部署前需确保业务空间已开通目标模型的调用权限，否则报错 `Workspace xxx does not have deployment privilege for model xxxx` [API 部署指南](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **OSS 导入约束**：LoRA 模型导入要求 `rank` 为 8/16/32/64，词汇表与 chat_template 必须与基础模型一致，视觉模型需冻结 VIT；Bucket 必须添加 `bailian-datahub-access=read` 标签 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。
- **Token 按量自动释放**：一个月内无调用将自动释放服务，不产生费用 [Token 按量部署](../../raw/model-user-guide/model-deployment-1/model-deployment-token.md)。
- **智能路由限制**：仅支持文本 Chat Completions，不支持图片/视频输入、Embedding/Rerank、Anthropic 协议、WebSocket 及 `top_p`/`temperature` 等采样参数 [智能路由](../../raw/model-user-guide/model-deployment-1/model-routing.md)。
- **DTU API 限制**：DTU 部署暂不支持通过 API 创建与管理，必须在控制台操作 [独占算力部署（DTU）](../../raw/model-user-guide/model-deployment-1/dtu-model-deployment.md)。

## 来源文档

- [专属部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [独占算力部署（DTU）](../../raw/model-user-guide/model-deployment-1/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-deployment-1/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [智能路由](../../raw/model-user-guide/model-deployment-1/model-routing.md)
- [我的模型](../../raw/model-user-guide/model-deployment-1/my-model-center.md)


