# support

本页汇总阿里云百炼平台的使用支持信息，覆盖[计费](../concepts/billing.md)规则、API/SDK 调用常见报错、模型训练与微调最佳实践、模型幻觉治理以及相关服务协议。开发者可据此快速定位开通、调用、训练、合规等环节的关键约束与处置方式，详见 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 与 [相关协议](../../raw/model-user-guide/support/related-agreements.md)。

## 服务开通与关闭

- 百炼服务需按地域开通：使用阿里云主账号进入百炼控制台，在右上角切换目标地域，阅读并同意协议后自动开通；未弹出协议则表示已开通该地域。若提示"您尚未进行实名认证"，需先完成实名认证。
- 开通后暂不支持关闭。若仅需停止调用，可在 [API-Key（北京）](https://bailian.console.aliyun.com/?apiKey=1&tab=globalset#/efm/api_key) 或 [API-Key（新加坡）](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/api_key) 页面删除已创建的 API-Key。
- 开通时若提示"账户可用额度小于0"，需保证阿里云账户余额不小于 0 元。

## [计费](../concepts/billing.md)与发票

- 模型调用单价见 [模型调用计费](https://help.aliyun.com/zh/model-studio/model-pricing)；部署与训练[计费](../concepts/billing.md)见 [模型部署计费](https://help.aliyun.com/zh/model-studio/model-training-and-deployment-billing)。
- 后付费按分钟级出账、按月结算；扣款明细可在 [费用与成本](https://usercenter2.aliyun.com/finance/expense-report/expense-detail) 查看。
- 部分模型支持预付费，见 [节省计划与资源包](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package)。
- 开票：登录费用与成本控制台，进入 [发票管理](https://usercenter2.aliyun.com/invoice/list/aliyun?pageIndex=1&pageSize=20&ownerId=1990699401005016&invoiceType=aliyun&1990699401005016%23ownerId=1990699401005016) 页面，在"开具发票"页签申请。
- 万相会员与百炼计费体系相互独立，万相会员权益不适用于百炼 API 调用。

## API/SDK 调用

- SDK 支持 Java 与 Python，详见 [安装 SDK](https://help.aliyun.com/zh/model-studio/install-sdk)；错误码及解决方案见 [错误码](https://help.aliyun.com/zh/model-studio/error-code)。
- Completion API 报错"参数缺失"（错误码 100004）：检查必填参数是否缺失及格式是否正确。调用需携带 `RequestId`、`AppId`、`Prompt`、`User`、`Bot` 等字段，示例 endpoint 为 `https://bailian.aliyuncs.com/v2/app/completions`，并在 `Authorization: Bearer <API-Key>` 头中携带 API-Key。
- Assistant API 的 function call 当前不支持依次分别调用两个本地函数；可手动创建两个 Assistant API 分别承载。Assistant API 暂不支持 memory 配置。
- `doc_reference_type` 参数仅在旧版本应用生效；新版本应用需在应用操作页面开启"展示回答来源"开关，否则该参数不生效。

## 模型与训练

- 模型体验可前往 [模型体验中心（北京）](https://bailian.console.aliyun.com/?&tab=model#/efm/model_experience_center/text) 或 [模型体验中心（新加坡）](https://modelstudio.console.aliyun.com/?tab=dashboard#/efm/model_experience_center/text)。
- 已支持图片训练，`qwen-vl-plus` 支持微调；本地自训练模型不支持上传到平台，平台"自定义模型"指已训练完成、用于二次训练的模型。训练完的开源模型暂不支持导出。
- 千问系列模型支持 14 种语言：中文、英文、阿拉伯语、西班牙语、法语、葡萄牙语、德语、意大利语、俄语、日语、韩语、越南语、泰语、印度尼西亚语。
- qwen-turbo 注重速度与资源效率、费用更低；qwen-max 聚焦顶级性能与复杂任务能力，按需权衡。
- 生成速度非固定，受服务整体负载与请求并发影响；限流触发后的等待时间取决于 RPS/RPM 限流值，例如 120 RPM（每秒 2 次）时，0.2 秒内连续提交 2 次后第 3 次需等约 0.8 秒。

## 训练最佳实践

- 数据质量优先于单纯堆量：任务定义清晰（同一 [prompt](prompt.md) 不对应模棱两可答案）、答案准确简洁、数据多样性（同一语义用多种 [prompt](prompt.md) 表达）。高质量训练数据通常需多次迭代。
- 仅用垂直领域数据做 SFT 可能导致模型遗忘通用知识，需评估是否混入千问原始 SFT 数据。
- 循环次数等超参无固定规律，需按任务实验确定（如数千条数据的复杂任务通常约 20 轮）。大模型不应仅凭 loss 判断过拟合，最终效果以人工评估为准。
- base model 出现重复说话属幻觉问题；微调后更严重通常意味着训练不足，与数据质量、多样性相关。

## 模型幻觉治理

模型幻觉指 LLM 无中生有、虚构事实或逻辑矛盾，核心在于"无依据的自信断言"，区别于事实性错误或明确要求的创造性虚构。降低方式详见 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)：

1. 选择更强的模型（千问系列 Max > Plus > Turbo）。
2. 提示词工程：RAG 场景加"仅基于提供的文档回答，信息不足请说'我不知道'"、要求引用具体数据、分步引导、设定严谨角色。
3. RAG：严格限制模型在检索知识范围内回答，确保检索系统高质量、清晰标注来源、优雅拒答。
4. 插件/MCP：将数值计算等易幻觉任务交给数据库客户端等工具完成，再把结果返回模型总结。
5. 参数调优：降低 `temperature`、`top_k`、`top_p`，必要时降低 `max_tokens`。
6. 后处理验证：用 AI 二次校验回复，但会增加成本并降低处理速度。

## 数据与隐私

- 阿里云不会将您的数据用于模型训练；构建应用或训练时传输的数据经 AES-256 加密。
- 依相关法律法规，百炼会存储模型与应用调用产生的数据，具体以 [阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html) 中数据处理、隐私与安全条款为准。
- 模型体验页最多展示 100 条历史对话记录，不设时间限制；未登录状态下的体验对话及推理报错时的对话记录不会被保存。
- 业务数据隔离可通过主账号给不同子账号授予不同[业务空间](../concepts/workspace.md)权限实现。
- 百炼生成的文本不支持添加隐式标识；目前无官方独立手机应用，主要通过 Web 控制台访问。

## 合规与合作

- 接入千问大模型需上架微信小程序等应用商店时：备案号获取见 [应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)；申请千问系列合作协议请提交 [阿里云工单](https://smartservice.console.aliyun.com/service/create-ticket)。
- 业务合作联系官方服务热线 4008013260 或 [官网-售前咨询](https://smartservice.console.aliyun.com/service/pre-sales-chat)；产品使用问题通过 [官网-售后服务](https://smartservice.console.aliyun.com/service/robot-chat) 反馈。

## 相关协议

使用百炼服务即视为接受以下协议，完整清单见 [相关协议](../../raw/model-user-guide/support/related-agreements.md)：

- 阿里云百炼服务协议
- 阿里云百炼模型推理服务等级协议（SLA）
- 阿里云百炼服务特别说明
- 开源模型协议条款说明
- 三方模型服务协议和使用条款清单

## 来源文档

- [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)
- [相关协议](../../raw/model-user-guide/support/related-agreements.md)



