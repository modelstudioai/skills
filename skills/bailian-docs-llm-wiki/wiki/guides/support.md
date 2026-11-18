# support

阿里云百炼平台的 `support` 体系涵盖技术咨询、故障排查、计费答疑、协议保障及售后响应等多个维度，面向开发者提供覆盖全生命周期的服务支持。核心支持能力基于官方控制台、API/SDK、CLI 工具及文档资源展开，不依赖第三方工具或非标集成环境。所有服务均以阿里云主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 账号为操作主体，且严格遵循《阿里云百炼服务协议》等法律文件约束。

## 支持的模型/功能

- **模型调用**：支持千问系列（Qwen-Max、Qwen-Plus、Qwen3.5-Flash、qwen3-vl-plus 等）及部分多模态模型的 API 推理调用；qwen3-vl-plus 已支持图片训练微调 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **应用与部署**：支持通过控制台快速创建和调试应用，但当前 Assistant API **暂不支持 memory 配置**，也**不支持单次 function call 中依次调用两个本地函数** [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **数据与安全**：所有传输数据默认 AES-256 加密；平台**不将用户数据用于模型训练**；历史对话记录在控制台最多保留 100 条，未登录或推理报错时的对话不保存 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 关键参数

- `doc_reference_type`：仅在旧版本应用中生效；新版本需在应用配置页开启「展示回答来源」开关，否则该参数无效 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- `temperature` / `top_p` / `top_k` / `max_tokens`：可用于抑制幻觉（如降低 `temperature` 使输出更保守），但需结合人工评估验证效果，不可单凭 loss 判断过拟合 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- 限流参数（RPS/RPM）：触发限流后重试等待时间取决于配额值，例如 120 RPM 下连续请求超限后需等待约 0.8 秒 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 使用方式

- **开通服务**：无需手动开通，使用阿里云主账号或已授权 `AliyunBailianFullAccess` 的 RAM 账号登录控制台，满足实名认证即可自动启用。
- **API 调用**：需配置有效 API Key（北京或新加坡区域），并确保请求头含 `Authorization: Bearer <token>`；错误码 `100004` 表示必填参数缺失或格式错误 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **CLI 工具**：Token Plan 需显式切换 Profile（如 `bl config use --name token-plan`），且仅模型调用类命令可用；控制台类命令（如 `app list`）仍需控制台登录凭证 [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。
- **售后渠道**：
  - 技术问题：通过[官网-售后服务](https://smartservice.console.aliyun.com/service/robot-chat)提交工单；
  - 业务合作：拨打 4008013260 或使用[官网-售前咨询](https://smartservice.console.aliyun.com/service/pre-sales-chat)；
  - 协议查阅：详见[相关协议](../../raw/model-user-guide/support/related-agreements.md)中列出的 SLA、服务协议等法律文件 [相关协议 (raw/model-user-guide/support/related-agreements.md)](../../raw/model-user-guide/support/related-agreements.md)。

## 限制和注意事项

> **注意**：文档 1 中提及“万相会员不支持百炼 API 调用”，但未说明其是否影响控制台内体验功能；实际使用中，万相会员权益与百炼计费体系完全隔离，**任何百炼 API 调用均需独立计费，与万相账户无关**。

> **注意**：文档 1 称“百炼不支持对接 MySQL/Hive 等结构化数据”，而文档 3 明确指出“已在开发中，优先对接 RDS 服务”。此处无矛盾，但需注意当前（文档发布时）**结构化数据库直连能力尚未上线**，仅可通过插件/MCP 方式间接调用（如数据库客户端计算后返回结果供模型总结） [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

- **服务关闭**：百炼服务开通后**暂不支持主动关闭**；如需停用，建议删除全部 API Key 并停止调用。
- **第三方工具支持边界**：阿里云仅对百炼服务端状态、API 示例、计费明细及基础连通性提供方向性建议；**不支持 Cursor、Windsurf 等第三方工具的安装、配置、调试或本地环境（代理/防火墙/VPN）问题排查** [阿里云百炼平台售后服务范围说明 (raw/model-user-guide/support/after-sales-service-scope.md)](../../raw/model-user-guide/support/after-sales-service-scope.md)。
- **数据导出与模型上传**：训练完成的开源模型**不支持导出**；自定义模型仅支持平台内二次训练，**不支持上传本地训练的模型文件** [常见问题 (raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/model-user-guide/support/after-sales-service-scope.md)


