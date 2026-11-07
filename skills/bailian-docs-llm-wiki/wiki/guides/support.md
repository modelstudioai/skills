# support

阿里云百炼平台为开发者提供覆盖全生命周期的技术支持服务，包括基础咨询、故障诊断、API/SDK 问题排查及计费答疑。支持范围聚焦于百炼平台自身能力（如模型服务、控制台、API 接口、计量计费系统），不延伸至第三方工具、用户本地环境或业务代码实现。所有服务均以《阿里云百炼服务协议》和 SLA 为法律与服务基准 [相关协议](../../raw/model-user-guide/support/related-agreements.md)。

## 支持的模型/功能

- **模型服务**：支持千问系列（Qwen-Max、Qwen-Plus、Qwen3.5-Flash、qwen-plus-latest 等）、万相（文生图）、多模态交互模型等，具体以[百炼控制台模型市场](https://bailian.console.aliyun.com/cn-beijing/model/market)为准；  
- **核心功能**：模型调用（Completion/Assistant API）、RAG 应用构建、模型微调（SFT）、部署与推理、Token Plan 使用、CLI 工具链（`bl` 命令）；  
- **数据与安全**：支持业务空间级数据隔离、AES-256 传输加密，**不将用户数据用于模型训练**；模型调用日志按法规要求存储，详情见 [相关协议](../../raw/model-user-guide/support/related-agreements.md)；  
- **体验与测试**：提供北京/新加坡双地域[体验中心](https://bailian.console.aliyun.com/model/experience/text)，支持免密快速试用（未登录状态对话不保存）。

> **注意**：文档 3 中“qwen-plus-latest 属于 Qwen3 系列”与部分内部命名习惯存在歧义，实际版本映射请以控制台模型详情页及 [模型介绍](https://help.aliyun.com/zh/model-studio/tongyi-qianwen) 为准，避免与 Qwen3.5/Qwen3.7 等并行列名混淆。

## 关键参数

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `temperature` / `top_p` / `top_k` | 控制输出随机性与多样性 | 降低可缓解幻觉，但可能削弱创造性；`temperature=0` 时输出最确定 |
| `max_tokens` | 限制响应最大 token 数 | 过长易引发幻觉续写，建议根据任务明确设限 |
| `doc_reference_type` | 控制答案来源展示方式 | **仅在旧版应用中生效**；新版需在控制台开启「展示回答来源」开关，否则该参数无效 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) |
| `RequestId` | 全局唯一请求标识 | 强烈建议每次调用显式传入，便于工单排查与计费溯源 |

## 使用方式

- **基础支持**：7×24 小时通过官网在线客服、电话（95187 / 4008013260）、阿里云 APP 及标准工单获取响应；  
- **技术问题定位**：  
  - API 报错（如错误码 `100004`）请核对必填参数格式与签名，参考 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中的 curl 示例；  
  - SDK 问题请确认已安装对应语言版本（Python/Java），详见 [安装SDK](raw/model-api-reference/preparations/install-sdk.md)；  
- **CLI 鉴权**：Token Plan 需显式使用 `--config token-plan` 登录，普通 `default` Profile 不触发扣减；切换凭据执行 `bl config use --name token-plan`；  
- **深度支持**：定制化集成、业务代码指导等超出平台边界的需求，需订购付费支持计划或联系商务经理协商 [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)。

## 限制和注意事项

- **不支持范围**（明确排除）：  
  - 第三方工具（Cursor/Windsurf/OpenClaw 等）的安装、配置、升级及故障诊断；  
  - 用户本地环境（代理、VPN、防火墙、操作系统兼容性）导致的连通性问题；  
  - 业务代码编写、调试与实现；  
  - 非阿里云百炼服务的第三方产品（含其他云厂商服务）运维支持；  
  - 万相会员权益不可用于百炼 API 调用，二者计费体系完全独立 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)；  
- **服务边界声明**：阿里云仅对百炼服务端（API 接口、控制台、计量计费系统）负责；第三方工具运行维护由其提供方或用户自行承担，阿里云不对其陈述、行为担责 [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)；  
- **模型能力限制**：  
  - 当前不支持直接对接 MySQL/Hive 等结构化数据库（RDS 对接开发中）；  
  - Assistant API 暂不支持 memory 配置、不支持连续调用多个 function call；  
  - 训练完成的开源模型暂不支持导出；  
- **限流与重试**：RPM/RPS 触发限流后，等待时间取决于配额（如 120 RPM ≈ 每秒 2 次），建议按配额间隔匀速请求，避免突发重试。

## 来源文档

- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)
- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)


