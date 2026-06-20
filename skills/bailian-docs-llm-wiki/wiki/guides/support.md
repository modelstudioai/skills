# support

本页汇总阿里云百炼平台的常见问题解答、服务协议及支持渠道，帮助开发者快速解决使用过程中遇到的问题。内容涵盖计费、API/SDK、模型训练与调优、模型幻觉处理，以及平台相关协议与联系方式。

## 计费相关

百炼平台模型服务按**分钟级出账、按月结算**。各模型单价可在 [百炼控制台模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all) 查看，详细计费规则参见 [模型调用计费](https://help.aliyun.com/zh/model-studio/model-pricing) 和 [模型部署计费](https://help.aliyun.com/zh/model-studio/model-training-and-deployment-billing)。

关键要点：

- **预付费**：部分模型支持预付费，详见 [节省计划与资源包](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package)。
- **账单查询**：前往 [费用与成本](https://usercenter2.aliyun.com/finance/expense-report/expense-detail) 查看扣款明细。
- **开通条件**：阿里云账户余额需不小于 0 元，否则无法开通服务。
- **万相会员**：万相会员与百炼计费体系独立，会员权益不适用于百炼 API 调用。

## API 与 SDK

百炼目前支持 Java 和 Python 语言的 SDK，安装方式详见 [安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。API 调用返回的错误码及解决方案参见 [错误码文档](https://help.aliyun.com/zh/model-studio/error-code)。

常见问题：

- **Completion API 报错 100004**：缺少必须参数或参数格式不正确。请确认 `Content-Type`、`Authorization`、`AppId`、`Prompt` 等字段格式无误。
- **`doc_reference_type` 不生效**：该参数仅在旧版本应用中生效。新版本应用需在操作页面开启"展示回答来源"开关。
- **Assistant API 限制**：当前不支持在单次调用中分别调用两个本地函数（function call），也暂不支持 memory 配置功能。

更多 API/SDK 使用细节可参阅 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 原文。

## 模型训练与调优

### 模型选择

- **qwen-turbo**：注重速度与资源效率，费用较低，适合对响应速度要求高的场景。
- **qwen-max**：聚焦顶级性能与全面知识，适合对精度和复杂任务处理有严格要求的场景。
- 千问系列模型支持 **14 种语言**（中文、英文、日语、韩语等）。

### 训练注意事项

- 已支持**图片训练**（qwen-vl-plus 模型支持训练微调）。
- 训练完成的开源模型**不支持导出**，本地训练的模型也不支持上传至平台。
- 仅使用垂直领域数据进行 SFT 可能导致模型遗忘通用知识。建议保证训练数据的**任务定义清晰、数据质量高、数据多样性**。
- 循环次数等超参数无固定规律，需根据具体任务实验确定。评估大模型不应仅依赖 loss 值，最终效果需以人工评估为准。

更多训练最佳实践可参考 [自定义模型最佳实践](https://help.aliyun.com/zh/model-studio/model-training-best-practices)。

## 模型幻觉与应对

模型幻觉是指 LLM 在生成内容时虚构事实、扭曲信息或产生逻辑矛盾的现象。降低幻觉的主要方法：

| 方法 | 说明 |
|------|------|
| 选择更强模型 | Max > Plus > Turbo，更大模型幻觉率更低 |
| 提示词工程 | 添加"仅基于文档回答"等约束，引导分步推理 |
| RAG | [检索增强生成](../concepts/rag.md)，限制回答在检索到的知识范围内 |
| 插件/MCP | 通过外部工具完成数值计算等任务，避免模型直接处理 |
| 参数调优 | 降低 `temperature`、`top_k`、`top_p` 等随机性参数 |
| 后处理验证 | 推理完成后通过 AI 再次校验回答正确性（会增加成本） |

## 服务开通与数据安全

- **开通服务**：使用阿里云主账号访问百炼控制台，阅读并同意协议后自动开通。如提示未实名认证，需先完成 [实名认证](https://help.aliyun.com/zh/account/verify-your-identity-individual-account)。
- **关闭服务**：开通后暂不支持关闭。可通过删除已创建的 API-Key 避免后续调用。
- **数据隐私**：阿里云不会将用户数据用于模型训练。传输数据经过 AES-256 加密。根据法规要求，平台会存储调用时产生的数据。
- **数据隔离**：通过主账号为不同子账号授予不同业务空间权限实现隔离，详见 [业务空间权限管理](https://help.aliyun.com/zh/model-studio/permission-management-overview#5f86c82cbc6pb)。
- **历史对话**：控制台最多展示 100 条历史对话记录，不设时间限制。

## 限流与速率

- 模型生成速度不固定，受服务整体负载和请求并发影响。
- 限流触发后等待时间取决于具体限流值（RPS/RPM）。例如 120 RPM 下，在 0.2 秒内提交 2 次请求后第 3 次会被限流，需等待约 0.8 秒。

## 相关协议

百炼平台涉及的主要协议包括：

- [阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html)
- [阿里云百炼模型推理服务等级协议（SLA）](https://terms.alicdn.com/legal-agreement/terms/b_end_product_protocol/20250923215800868/20250923215800868.html)
- [阿里云百炼服务特别说明](https://help.aliyun.com/zh/model-studio/bailian-service-notes)
- [开源模型协议条款说明](https://help.aliyun.com/zh/model-studio/open-source-model-terms)
- [三方模型服务协议和使用条款清单](https://terms.alicdn.com/legal-agreement/terms/common_product_agreement/20260207131114217/20260207131114217.html)

协议全文参见 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 原文。

## 联系支持

- **售前咨询**：阿里云官方服务热线 4008013260 或 [官网售前咨询](https://smartservice.console.aliyun.com/service/pre-sales-chat)
- **售后服务**：登录阿里云官网通过 [官网售后服务](https://smartservice.console.aliyun.com/service/robot-chat) 反馈
- **合规备案**：应用上架需获取备案号，流程参见 [应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)
- **合作协议**：如需千问系列模型合作协议，请提交 [阿里云工单](https://smartservice.console.aliyun.com/service/create-ticket) 申请

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)


