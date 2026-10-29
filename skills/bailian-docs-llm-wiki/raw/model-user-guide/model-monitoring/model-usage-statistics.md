# 模型用量

介绍如何查看阿里云百炼各模型的用量。

> 如需了解免费额度相关内容，请参考[新人免费额度](raw/model-user-guide/test-1/new-free-quota.md)文档。您也可以在[免费额度](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota)页面查看和管理免费额度使用情况。

## 适用范围

-   **地域**：支持查看各地域的模型调用用量。美国（弗吉尼亚）地域暂不展示调用次数。
-   **模型**：模型列表中的全部模型均支持查看用量，包括基于它们[调优后的模型](raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)。
-   **统计范围**：Token 等用量用于核对费用，仅统计按 Token 后付费的模型调用，不含模型训练、预置吞吐单元、独占吞吐单元等调用；调用次数包含预置吞吐单元、独占吞吐单元等调用。模型调用产生的工具调用用量单独统计。

## 查看免费额度使用情况

免费额度页面顶部提供「免费额度使用概览」，按模型总数、额度充沛、使用超 50%、使用超 80%、无免费额度等维度汇总当前空间下各模型的免费额度消耗情况，并展示「免费额度即将用尽TOP3模型」列表，便于快速定位需要关注的模型。

「全部模型」表格列出各模型的**模型 Code**、**免费额度剩余量**、**过期时间**、**状态**（未开启/已开启/不支持开启）及**操作**。支持搜索、排序、筛选查找特定模型，点击单条可切换「免费额度用完即停」开关，或查看模型详情抽屉。

页面上方提供**批量操作**入口，可对所选模型**批量开启**或**批量关闭**「免费额度用完即停」，也可**一键开启/关闭所有模型**；操作前会弹出确认提示，操作完成后展示成功与失败结果，完成后可**退出批量操作**。还可在操作列通过**购买节省计划**或**优惠下单**购买资源包；若账号未绑定有效支付方式，批量操作将失败并提示绑定银行卡。

### 在控制台查看免费额度使用情况

1.  进入[免费额度](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota)页面，选择模型类型页签查看各模型的免费额度使用情况。
2.  在全部模型表格中，可通过搜索、排序、筛选等方式查找特定模型，并可切换**免费额度用完即停**开关或使用批量操作功能管理免费额度设置。

**说明****免费额度用完即停：** 开启后，免费额度用尽时服务将自动停止（返回403错误：AllocationQuota.FreeTierOnly），避免产生免费额度以外的费用。若您希望在免费额度用尽后仍继续使用模型服务，并根据实际产生的用量付费，请保持本功能关闭状态。您只能在账户内仍有未消耗的免费额度时开启本功能。一旦功能开启，若您需要关闭本功能，需要在免费额度完全消耗后再进行关闭（免费额度消耗记录可在账单中查看，账单记录按分钟汇总生成；控制台免费额度数据分钟级更新，支持手动刷新页面同步，请以控制台显示的免费额度数值为准。）

## 查看模型用量

在[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)页面查看。数据按[业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)维度统计，不支持按阿里云账号维度统计（[如何解决](#common-questions)）。调用次数统计延迟通常低于其他用量指标：调用后约 1 分钟可看到调用次数，Token 用量和费用可能延迟约 10 分钟。批量离线推理和批量在线推理不展示调用次数。

1.  选择统计周期和起止时间。支持按分钟、按小时、按天、按月查看：按分钟最多查询 1 天，按小时最多查询 7 天，按天最多查询 31 天，按月最多查询 12 个月。按分钟或按小时查看时，趋势图不支持分组。
2.  选择分组维度：按模型、API Key、业务空间、地域、服务区域或规格分组。规格包括输入/输出/缓存命中、上下文长度、是否开启思考模式、视频生成分辨率等影响单价的因素。
3.  按需筛选模型、API Key、业务空间、地域、服务区域、调用来源和推理类型。推理类型包括在线推理、批量离线推理（Batch File）和批量在线推理（Batch Chat）；当前业务空间没有批量调用数据时，仅显示在线推理。
4.  查看指标卡片：调用次数、Tokens 用量、图片数量、视频/语音时长、语音合成字数、工具调用次数等。卡片按收费量纲汇聚，例如文本模型和全模态模型都按 Token 计费，均计入 Tokens 用量。可在「总量」和「平均单次用量」之间切换；平均单次用量为用量除以成功调用次数。
5.  在「模型用量明细」表格中查看各模型的模型类型、调用次数、模型用量和工具用量。点击「详情」查看该模型不同类型用量的汇总、趋势和工具用量；点击「查看费用」查看这些用量对应的应付金额。
6.  页面底部「总调用成功次数」区域按调用次数从多到少展示全部模型，支持全屏查看和下载。

**说明**

-   失败次数、失败率、限流错误次数和内容安全拦截次数已移至[模型监控](raw/model-user-guide/model-monitoring/model-telemetry.md)页面，不再在模型用量详情中展示。
-   旧版「批量推理」现拆分为批量离线推理（Batch File）和批量在线推理（Batch Chat）。

**说明**页面仅支持查询 2026 年 9 月 1 日及之后的用量数据；更早的数据请通过[费用与成本](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)查看。

## 查看费用概览

在[费用概览](https://bailian.console.aliyun.com/cn-beijing/costing-balance/overview)页面查看模型调用和模型训练产生的费用，包括总消费金额、订阅购买费用、账单费用和账单趋势。费用概览的详细说明请参见[账单查询与成本管理](https://help.aliyun.com/zh/model-studio/bill-query-and-cost-management#a309aa68b2rxe)。

## 模型用量统计单位说明

模型用量页面的指标卡片按收费量纲汇聚，不同模型的统计单位如下：

**类型**

**二级分类**

**统计单位**

**计费说明（模型调用）**

**大语言模型**

[文本生成模型](https://help.aliyun.com/zh/model-studio/model-pricing#e90fd1458c2vm)

[Token](raw/model-user-guide/model-monitoring/model-usage-statistics.md)

按输入和输出对应的 Token 数计费。

[深度思考模型](raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md)

[视觉理解模型](raw/model-user-guide/model-experience/vision-model/vision.md)

**视觉模型**

[图像生成](https://help.aliyun.com/zh/model-studio/model-pricing#26310bc5cf4do)

**张**

按成功生成的 **图像张数**计费。

视频生成

**秒**

按成功生成的 **视频秒数** 计费。

**语音模型**

[语音合成模型](raw/model-user-guide/model-experience/speech-synthesis/non-realtime-tts-user-guide.md)

**秒、字符或 Token**

可能按音频时长（秒）、对应的文本字符数或 Token 数计费，视模型而定。

[实时语音合成模型](raw/model-user-guide/model-experience/speech-synthesis/realtime-tts-user-guide.md)

[录音文件识别模型](raw/model-user-guide/model-experience/speech-recognition/non-realtime-speech-recognition-user-guide.md)

[实时语音识别模型](raw/model-user-guide/model-experience/speech-recognition/real-time-speech-recognition-user-guide.md)

[音视频翻译模型](raw/model-user-guide/model-experience/speech-to-speech/qwen3-livetranslate-flash.md)

**全模态模型**

[全模态模型](raw/model-user-guide/model-experience/omni-modal/qwen-omni.md)

**Token**

文本部分按 Token 数，其他模态（音频、图像、视频）按对应的 Token 数计费。

[实时多模态模型](raw/model-user-guide/model-experience/omni-modal/realtime.md)

**向量模型**

[多模态向量模型](raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)

**Token**

按输入文本的 Token 数计费。

文本向量模型

## 应用于生产环境

管理模型用量建议：

-   **控制模型输出长度：** 在调用模型 API 时，合理[限制思考长度](raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md)和设置 `max_tokens` 参数，可限制模型单次生成内容的最大长度（从而控制费用）。
-   **根据任务类型选择模型：** 对于分类、摘要等简单任务，优先选择成本更低的轻量级模型，而不是始终使用功能强大但价格也较高的模型。
-   **监控与告警：** 通过[模型监控](raw/model-user-guide/model-monitoring/model-telemetry.md)监控用量趋势，并可配置用量告警，当用量出现异常时及时收到通知。
-   **优化 Prompt：** 简洁、清晰的 Prompt 不仅能提升模型输出质量，也能减少不必要的输入 Token 消耗。
-   **使用批量推理：** 对于非实时、大批量的处理任务，使用[批量推理](raw/model-user-guide/model-high-speed-inference/batch-inference.md)通常比实时调用更具成本优势。

## 名词解释

**名词**

**解释**

**Token**

Token 是模型处理输入和输出的基本单位。一个 Token 可能是：

-   **单个字符：**如`A`、`我`
    
-   **完整的单词：**如`large`、`Model`
    
-   **长单词的一部分：**一个长单词通常会被拆分为多个 Token，拆分的过程称为分词。
    

文本的 Token 数量由所用模型的分词器确定，实际用量以接口返回的用量统计为准。

每个模型都有最大输入和输出 Token 数（详见模型列表），超过限制会导致请求失败。

**在线推理**

指对模型的全部直接和间接调用，主要涵盖以下场景：

-   API调用
    
-   模型广场
    
-   [阿里云百炼应用](raw/application-user-guide/llm-application/llm-application-start-using/flow-agent-introduction.md)（智能体/工作流/智能体编排应用，以及涉及到模型调用的节点，如大模型节点、意图分类节点以及智能体群组节点等）的测试态和发布态
    
-   [Assistant API（下线中）](https://help.aliyun.com/zh/model-studio/assistant-api)调用
    
-   [应用调用](https://help.aliyun.com/zh/model-studio/application-calling-guide)
    
-   [Prompt反馈优化](raw/application-user-guide/prompt/prompt-feedback-optimization.md)
    
-   [模型评测](raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
    

**批量离线推理（Batch File）**

对于无需实时响应的场景，通过[OpenAI兼容-Batch（文件输入）](raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)接口以离线方式进行的大规模数据处理。

**批量在线推理（Batch Chat）**

通过 Batch Chat 接口发起的批量在线调用。

## 常见问题

**Q: 如何查我的阿里云账号的 Token 总用量？**

A: 使用阿里云账号（主账号）访问[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面并导出账单，然后在账单中查看 Token 用量。

在**账单详情**页面，按以下条件筛选并导出：

1.  将**账单月份**设置为目标月份（如 `2025-05`）
2.  在**产品名称**中选择**大模型服务平台百炼**
3.  单击表格右上方的下载图标导出账单数据

**Q: 可以在阿里云 App 查看免费额度和模型用量吗？**

A: 暂不支持。阿里云 App 目前不支持查看百炼的免费额度使用情况和模型用量数据。请登录 PC 端，进入百炼控制台的[免费额度](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota)或[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)页面查看。

为什么图表或明细中会出现“-”或空值？

按模型、API Key、业务空间等维度查看时，部分数据可能显示“-”或为空，常见原因如下：

-   “-”可能表示模型不支持该计量方式。
-   细分维度的数据有延迟，刚产生调用时可能显示“-”，几分钟或十几分钟后显示实际值。
-   API Key 为空通常表示调用来自控制台页面。
-   通过 Batch Chat 发起的调用，API Key ID 相关数据为空。
-   部分模型的地域信息为空。
-   语音模型的调用方式为空。
