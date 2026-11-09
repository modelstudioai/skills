# support

阿里云百炼平台为开发者提供覆盖模型调用、部署、训练及运维全链路的技术支持服务，包括免费的基础技术支持与可选的付费增值服务。支持范围聚焦于百炼平台自身能力（如API、控制台、计费系统、SDK）及官方文档明确承诺的功能，不延伸至第三方工具、用户本地环境或业务代码实现。所有服务均以《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)》为法律基准。

## 支持的模型/功能

- **模型支持**：覆盖千问系列（Qwen-Max、Qwen-Plus、Qwen3.5-Flash、qwen3-vl-plus等）、万相及其他百炼市场提供的大模型；支持文本生成、多模态推理、SFT微调、RAG增强等核心能力。
- **功能支持**：
  - 模型调用（Completion / Assistant / Realtime API）
  - 应用构建与发布（含展示答案来源、Bot/User上下文管理）
  - 模型训练与部署（含图片训练、结构化数据对接规划）
  - CLI 工具（`bl` 命令行客户端，支持 [Token](../concepts/token.md) Plan Profile 鉴权）
- **不支持场景**：  
  > **注意**：万相会员权益**不支持百炼API调用**，二者计费体系完全独立 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)；  
  > **注意**：当前**不支持直接对接 MySQL/Hive 等结构化数据库**，RDS 接入正在开发中 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)；  
  > **注意**：`doc_reference_type` 参数**仅在旧版本应用中生效**，新版本需通过控制台开关启用“展示回答来源” [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 关键参数

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `temperature` / `top_p` / `top_k` | 控制输出随机性与确定性 | 降低值可抑制幻觉，但可能削弱创造性；需结合任务人工评估效果 |
| `max_tokens` | 限制响应长度 | 过长易引发冗余或捏造，建议按实际需求设合理上限 |
| `RequestId` | 全局唯一请求标识 | 必须符合 UUID 格式（如 `B8265C3E-9248-56C0-8665-A37A12F06F6B`），用于问题排查与计费追溯 |
| `AppId` | 百炼应用唯一ID | 调用 Completion API 时必需，需在控制台创建应用后获取 |

## 使用方式

- **基础支持（免费）**：  
  通过官网、电话（95187 / 4008013260）、阿里云APP提供 7×24 小时智能在线与工单支持，覆盖：  
  - 百炼模型服务与产品功能咨询  
  - API/SDK 故障诊断（含错误码 `100004` 等参数类问题）  
  - 控制台操作、账号权限、计费明细核查  
  - 方向性连通性测试建议（如 `curl` 测试服务可达性）  

- **增值服务（付费）**：  
  可订购支持计划（如企业级SLA保障），详情见 [客户服务权益](https://www.aliyun.com/service/customer-service-benefits?spm=5176.support-home.J_3451238410.1.12d1156fPBBxO0)；深度定制需求（如业务代码指导、私有化集成方案）需联系商务经理。

- **自助资源**：  
  - 错误码详解：[错误码](../../raw/model-api-reference/preparations/error-code.md)  
  - SDK安装：[安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)（Python/Java）  
  - CLI鉴权：使用 `bl auth login --config token-plan` 切换 [Token](../concepts/token.md) Plan Profile [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)

## 限制和注意事项

- **责任边界明确**：  
  阿里云仅对百炼平台自身（API接口、服务端、计量计费、控制台）负责；**不承担第三方工具（如 Cursor、Windsurf）、用户本地环境（代理/防火墙/OS）、业务代码或非标集成问题的责任** [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)。

- **数据与安全**：  
  - 所有传输数据经 AES-256 加密；  
  - **绝不将用户数据用于模型训练**；  
  - 模型调用日志依法律法规留存，具体条款见 [《阿里云百炼服务协议》](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)。

- **其他关键限制**：  
  - 服务开通后**不可关闭**，仅可通过删除 API Key 阻断调用；  
  - 控制台体验中心最多保留 **100 条历史对话记录**（未登录/报错对话不保存）；  
  - 模型限流触发后重试时间取决于配置的 RPS/RPM，例如 120 RPM 下需等待约 0.8 秒 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 来源文档

- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)
- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)


