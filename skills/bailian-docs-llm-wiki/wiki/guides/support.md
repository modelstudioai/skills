# support

阿里云百炼平台的 `support` 体系面向开发者提供覆盖产品使用、API调用、计费运维及法律合规的全链路支持能力。它包含自助文档、自动化工具、人工服务与法律协议四层保障，核心目标是确保模型服务稳定、可预期、可审计。开发者应优先查阅结构化文档与错误码说明，并在必要时通过标准工单或售前/售后通道升级问题。

## 支持的模型/功能

- **模型范围**：支持千问系列（Qwen-Max、Qwen-Plus、Qwen3.5-Flash、Qwen3-VL-Plus 等）、万相（文生图）及其他第三方模型，但需注意：[**万相会员**](https://tongyi.aliyun.com/wan/pricing?whereToMemberShip=upgrade)权益**不适用于百炼API调用**，二者计费体系完全独立 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **功能覆盖**：
  - Completion / Assistant API 调用（含 function call 基础能力，但**暂不支持单次请求中连续调用两个本地函数**）；
  - RAG 应用构建与 `doc_reference_type` 参数控制（仅在旧版应用中生效，新版需通过控制台开关启用）；
  - 模型微调（SFT）、[多模态](../concepts/multi-modal.md)训练（qwen3-vl-plus 支持图片训练）；
  - CLI 工具（`bl`）的鉴权、Profile 切换与 [Token](../concepts/token.md) Plan 使用；
  - 业务空间权限隔离、数据加密（AES-256）与合规备案支持。

> **注意**：文档 1 中提到“当前暂不支持 memory 配置功能”（Assistant API），而文档 3 未涉及该能力；该限制仍有效，无更新说明，以 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 为准。

## 关键参数

| 参数 | 说明 | 生效条件 |
|------|------|----------|
| `temperature`, `top_k`, `top_p`, `max_tokens` | 控制生成随机性、候选集范围与输出长度，可用于抑制幻觉 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) | 所有 Completion/Assistant API 请求体中传入 |
| `doc_reference_type` | 控制答案来源标注格式（如 `inline` / `footnote`） | **仅在旧版应用中生效**；新版应用需在控制台开启「展示回答来源」开关，否则该参数无效 |
| `RequestId`, `AppId`, `User`, `Bot` | Completion API 必填字段 | 缺失或格式错误将返回错误码 `100004` |

## 使用方式

- **自助排查**：  
  - 查看错误码详情 → [错误码](raw/model-api-reference/preparations/error-code.md)；  
  - 安装 SDK → [安装SDK](raw/model-api-reference/preparations/install-sdk.md)（Python/Java）；  
  - CLI 鉴权与 Profile 管理 → 使用 `bl auth login --config token-plan` 切换至订阅凭据 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **人工支持**：  
  - 技术问题 → 提交标准工单或通过 [官网-售后服务](https://smartservice.console.aliyun.com/service/robot-chat)；  
  - 业务合作 → 拨打 4008013260 或使用 [官网-售前咨询](https://smartservice.console.aliyun.com/service/pre-sales-chat)；  
  - 合规备案 → 使用 [大模型百炼合作协议备案自助申请助手](https://smartservice.console.aliyun.com/service/self-service-center/search?id=28023&mode=toolPage&trackFrom=topic-llm2&showDrawer=true)。

## 限制和注意事项

- **服务开通与关闭**：  
  - 开通无需手动操作，满足实名认证 + 主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 账号即可自动启用；  
  - **服务开通后暂不支持关闭**，如需停用，应删除所有 API-Key [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **数据与隐私**：  
  - 百炼**不会将用户数据用于模型训练**，传输全程 AES-256 加密；  
  - 根据法规要求，调用日志等数据会被存储，具体条款见 [《阿里云百炼服务协议》](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.2020520104.0.0.52a63a98OYNqWq) [相关协议 (raw/model-user-guide/support/related-agreements.md)](../../raw/model-user-guide/support/related-agreements.md)。
- **第三方工具支持边界**（重要）：  
  - 百炼**仅对自身服务端状态、API 可达性、官方 SDK 行为负责**；  
  - 不支持 Cursor/Windsurf/OpenClaw 等第三方工具的安装、配置、本地环境（代理/防火墙/VPN）、业务代码调试或其内部统计与阿里云计费差异解释 [阿里云百炼平台售后服务范围说明 (raw/model-user-guide/support/after-sales-service-scope.md)](../../raw/model-user-guide/support/after-sales-service-scope.md)。  
  > **注意**：文档 3 明确声明“第三方工具不构成我们的代理、受托或联合服务主体”，此为法律责任边界，非技术建议范围。

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)


