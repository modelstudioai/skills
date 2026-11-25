# support

阿里云百炼平台的 `support` 模块涵盖服务开通、计费、API/SDK 使用、故障排查、协议合规及售后响应等全链路支持能力。面向开发者，核心目标是保障模型调用稳定、权限配置正确、问题可定位、责任边界清晰。所有支持行为均以官方文档、SLA 协议及控制台实际功能为准，不依赖非官方渠道信息。

## 支持的模型/功能

- **模型覆盖**：支持千问系列（Qwen-Max、Qwen-Plus、Qwen3.5-Flash、Qwen3-VL-Plus 等）、开源模型及部分三方模型；其中 Qwen3-VL-Plus 已支持图像微调训练 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **核心功能支持**：
  - Completion / Assistant API 调用（含 Function Calling 基础能力，但**不支持单次请求中依次调用两个本地函数**）；
  - RAG 应用构建与 `doc_reference_type` 参数控制（仅在旧版应用中生效，新版需通过控制台开关启用）；
  - CLI 工具（`bl`）的鉴权、Profile 切换与 [Token](../concepts/token.md) Plan 使用；
  - 业务空间（Workspace）级数据隔离，实现多租户数据物理/逻辑分离；
  - 模型训练、微调、评估全流程（但**不支持导出自训练模型**，且本地训练模型不可上传）。

> **注意**：文档 1 中提及“Assistant API 当前暂不支持 memory 配置功能”，而部分 SDK 示例代码中存在 `memory` 字段占位。该字段为预留接口，**当前版本无实际作用，不应依赖其状态或行为** [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 关键参数

| 参数名 | 说明 | 生效条件 | 参考 |
|--------|------|----------|------|
| `doc_reference_type` | 控制答案来源展示方式（如 `all`/`none`/`selected`） | **仅旧版应用生效**；新版需在应用配置中开启「展示回答来源」开关 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) | |
| `temperature` / `top_p` / `top_k` | 影响输出随机性与确定性 | 全模型通用，推荐降低 `temperature`（如设为 0.1–0.3）以抑制幻觉 | |
| `max_tokens` | 限制生成最大 token 数 | 防止冗余输出导致幻觉延伸，尤其适用于结构化响应场景 | |
| `RequestId` | 全局唯一请求标识 | 必填，用于问题定位与工单追踪，格式需符合 UUID v4 标准 | |

## 使用方式

- **服务开通**：无需手动开通。使用阿里云主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号登录 [百炼控制台](https://bailian.console.aliyun.com/)，完成实名认证后自动启用。
- **API 调用**：
  - 必须携带 `Authorization: Bearer <API-Key>` 请求头；
  - 推荐使用 DashScope SDK（Python/Java），安装方式见 [安装SDK](../../model-api-reference/preparations/install-sdk.md)；
  - CLI 工具需显式切换 Profile（如 `bl config use --name token-plan`）以启用 [Token](../concepts/token.md) Plan 计费。
- **问题反馈**：
  - 技术问题 → 提交标准工单或通过 [官网-售后服务](https://smartservice.console.aliyun.com/service/robot-chat)；
  - 业务合作 → 拨打 4008013260 或使用 [官网-售前咨询](https://smartservice.console.aliyun.com/service/pre-sales-chat)；
  - 错误码解析 → 查阅 [错误码](../../model-api-reference/preparations/error-code.md) 文档。

## 限制和注意事项

- **服务不可关闭**：百炼服务开通后无法主动关闭，如需停用，应删除全部 API-Key 并停止调用。
- **数据留存策略**：
  - 控制台体验中心最多保留 **100 条历史对话记录**（无时间限制），未登录或报错对话不保存；
  - 所有调用数据按《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.2020520104.0.0.52a63a98OYNqWq)》要求加密存储，**绝不用于模型再训练**。
- **第三方工具边界**：
  - 阿里云仅支持百炼服务端本身（API 可达性、计费明细、官方 SDK 行为）；
  - **不支持**第三方工具（如 Cursor、Windsurf）的安装、配置、本地环境（代理/防火墙/VPN）或业务代码调试 [阿里云百炼平台售后服务范围说明 (raw/model-user-guide/support/after-sales-service-scope.md)](../../raw/model-user-guide/support/after-sales-service-scope.md)。
- **计费与额度**：
  - 后付费按分钟出账、按月结算；
  - 账户余额必须 ≥ 0 元方可开通服务；
  - 万相会员权益**不适用于百炼 API 调用**，二者计费体系完全独立 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)


