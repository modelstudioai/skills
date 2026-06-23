# support

本页汇总阿里云百炼平台在使用过程中常见的支持类信息，涵盖计费、API/SDK、模型训练与幻觉优化、数据合规与服务协议等高频问题，并给出官方协议清单，便于开发者快速定位答案与合规依据。

## 计费与账单

百炼模型服务的计费按调用与部署分别结算。模型调用单价可在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)或[模型调用计费](https://help.aliyun.com/zh/model-studio/model-pricing)查询；模型部署与训练的单价请参见[模型部署计费](https://help.aliyun.com/zh/model-studio/model-training-and-deployment-billing)。部分模型支持预付费，详见[节省计划与资源包](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package)。后付费按分钟级出账、按月结算，扣款明细可在[费用与成本](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)查看，开票请在[发票管理](https://usercenter2.aliyun.com/invoice/list/aliyun?pageIndex=1&pageSize=20&ownerId=1990699401005016&invoiceType=aliyun&1990699401005016%23ownerId=1990699401005016)页面申请。

> **注意**：开通服务时若提示“您的账户可用额度小于0”，需先充值至账户余额不小于0元。此外，[万相会员](https://tongyi.aliyun.com/wan/pricing?whereToMemberShip=upgrade)权益与百炼 API 计费体系相互独立，不适用于百炼 API 调用。

更多计费问题与解答可参考 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## API/SDK

百炼提供 Completion API 与 Assistant API 两种调用方式，支持 Java 与 Python 语言 SDK，安装方式参见[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。调用返回的状态码及解决方案见[错误码](https://help.aliyun.com/zh/model-studio/error-code)；例如错误码 `100004` 表示参数缺失，需检查必选参数是否齐全及格式是否正确。

调用示例：

```
curl --location 'https://bailian.aliyuncs.com/v2/app/completions' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer 85763*************cf050f' \
--data '{
  "RequestId":"B8265C3E-9248-56C0-8665-A37A12F06F6B",
  "AppId":"3cc760a7ef5d47d09255dd28b06b94d8",
  "Prompt":"今天深圳天气如何？",
  "User":"1",
  "Bot":"1"
}'
```

部分能力的已知限制：

- Assistant API 调用 function call 时，暂不支持依次分别调用两个本地函数，需手动创建两个 Assistant API 分别处理。
- Assistant API 当前暂不支持 memory 配置。
- `doc_reference_type` 参数仅在旧版本应用中生效，新版本应用需在操作页面开启“展示答案来源”开关，否则参数不生效。

## 产品与账号

百炼服务按地域开通，需使用阿里云主账号在[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/model-market)右上角切换目标地域并同意协议后自动开通；若未弹出协议则表示该地域已开通。服务开通后暂不支持关闭，若仅通过 API 调用，可在 [API-Key（北京）](https://bailian.console.aliyun.com/?apiKey=1&tab=globalset#/efm/api_key)或[API-Key（新加坡）](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/api_key)页面删除 API-Key 以避免后续调用。

- 实名认证：开通时若提示“您尚未进行实名认证”，请先完成[实名认证](https://help.aliyun.com/zh/account/verify-your-identity-individual-account)。
- 业务隔离：通过主账号给不同子账号授予不同[业务空间](../concepts/workspace.md)权限，实现数据隔离，详见[业务空间权限管理](https://help.aliyun.com/zh/model-studio/permission-management-overview#5f86c82cbc6pb)。
- 模型体验：可在[模型体验中心](https://bailian.console.aliyun.com/?&tab=model#/efm/model_experience_center/text)体验，控制台最多展示 100 条历史对话记录，不设时间限制；未登录或推理报错时的对话记录不会被保存。
- 移动端：百炼目前没有官方独立手机应用，主要通过 Web 控制台访问。

## 模型训练与微调

百炼已支持文字与图片训练，其中 `qwen-vl-plus` 支持图片微调。本地自行训练的模型不支持上传，训练完的开源模型也不支持导出。千问系列模型支持 14 种语言：中文、英文、阿拉伯语、西班牙语、法语、葡萄牙语、德语、意大利语、俄语、日语、韩语、越南语、泰语、印度尼西亚语。

在模型选型上，`qwen-turbo` 注重速度与资源效率、费用更低，适合对响应速度和部署便捷性要求较高的场景；`qwen-max` 聚焦顶级性能与全面知识，适合对精度和复杂任务能力要求严格的环境。详见 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中模型中心部分。

训练数据与超参的最佳实践要点：

- 仅使用垂直领域数据进行 SFT 易导致模型遗忘通用知识；建议任务定义清晰、答案准确简洁、数据表达多样。
- 数据量较少（如 100 条）时增大循环次数通常有益；数据量较多（如 1000 条以上）时循环次数过多更易过拟合。
- 不要仅凭 loss 判断是否过拟合，大模型即便 loss 显示过拟合，实际效果仍可能提升，最终以人工评估为准。
- 生成速度并非固定，受整体负载与请求并发影响；限流触发后的等待时间取决于 RPS/RPM 限流值。

## 模型幻觉

模型幻觉指大语言模型无中生有、虚构事实、扭曲信息或产生逻辑矛盾的现象，其输出看似合理但与输入或真实世界知识严重不符。降低幻觉的主要方式包括：选择更强的模型（千问系列中 Max > Plus > Turbo）、提示词工程、RAG 检索增强、插件/MCP 调用结构化数据源、降低 `temperature`/`top_k`/`top_p` 等随机性参数、以及在推理后做后处理验证。详细策略见 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 的模型幻觉部分。

## 数据安全与合规

阿里云承诺不会将您的数据用于模型训练，构建应用或训练过程中传输的数据均经过 AES-256 加密。根据相关法律法规要求，百炼会存储模型与应用调用时产生的数据，具体条款见《阿里云百炼服务协议》。百炼生成的文本不支持添加隐式标识；接入千问模型上架微信小程序等应用商店时，备案号获取流程见[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)，如需千问系列模型合作协议请提交[阿里云工单](https://smartservice.console.aliyun.com/service/create-ticket)申请。

## 相关协议

百炼涉及的服务协议与条款清单如下，使用前请仔细阅读 [相关协议](../../raw/model-user-guide/support/related-agreements.md)：

- [阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html)
- [阿里云百炼模型推理服务等级协议（SLA）](https://terms.alicdn.com/legal-agreement/terms/b_end_product_protocol/20250923215800868/20250923215800868.html)
- [阿里云百炼服务特别说明](https://help.aliyun.com/zh/model-studio/bailian-service-notes)
- [开源模型协议条款说明](https://help.aliyun.com/zh/model-studio/open-source-model-terms)
- [三方模型服务协议和使用条款清单](https://terms.alicdn.com/legal-agreement/terms/common_product_agreement/20260207131114217/20260207131114217.html)

## 联系我们

- 业务合作：拨打官方服务热线 **4008013260**，或通过[官网-售前咨询](https://smartservice.console.aliyun.com/service/pre-sales-chat)沟通。
- 产品使用问题：登录阿里云官网，通过[官网-售后服务](https://smartservice.console.aliyun.com/service/robot-chat)反馈。

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)


