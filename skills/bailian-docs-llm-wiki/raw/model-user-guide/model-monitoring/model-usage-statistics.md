# 模型用量

> 如需了解免费额度相关内容，请参考[新人免费额度](raw/model-user-guide/test-1/new-free-quota.md)文档。您也可以在[免费额度](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota)页面查看和管理免费额度使用情况。

## 适用范围

-   **支持的模型**：模型列表中的所有模型均支持查看用量，包括基于它们[调优后的模型](raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

## 查看免费额度使用情况

免费额度页面顶部提供「免费额度使用概览」，按模型总数、额度充沛、使用超 50%、使用超 80%、无免费额度等维度汇总当前空间下各模型的免费额度消耗情况，并展示「免费额度即将用尽TOP3模型」列表，便于快速定位需要关注的模型。

「全部模型」表格列出各模型的**模型 Code**、**免费额度剩余量**、**过期时间**、**状态**（未开启/已开启/不支持开启）及**操作**。支持搜索、排序、筛选查找特定模型，点击单条可切换「免费额度用完即停」开关，或查看模型详情抽屉。

页面上方提供**批量操作**入口，可对所选模型**批量开启**或**批量关闭**「免费额度用完即停」，也可**一键开启/关闭所有模型**；操作前会弹出确认提示，操作完成后展示成功与失败结果，完成后可**退出批量操作**。还可在操作列通过**购买节省计划**或**优惠下单**购买资源包；若账号未绑定有效支付方式，批量操作将失败并提示绑定银行卡。

### 在控制台查看免费额度使用情况

1.  进入[免费额度](https://bailian.console.aliyun.com/cn-beijing/?tab=costing-balance#/costing-balance/free-quota)页面，选择模型类型页签查看各模型的免费额度使用情况。
2.  在全部模型表格中，可通过搜索、排序、筛选等方式查找特定模型，并可切换**免费额度用完即停**开关或使用批量操作功能管理免费额度设置。

**说明****免费额度用完即停：** 开启后，免费额度用尽时服务将自动停止（返回403错误：AllocationQuota.FreeTierOnly），避免产生免费额度以外的费用。若您希望在免费额度用尽后仍继续使用模型服务，并根据实际产生的用量付费，请保持本功能关闭状态。您只能在账户内仍有未消耗的免费额度时开启本功能。一旦功能开启，若您需要关闭本功能，需要在免费额度完全消耗后再进行关闭（免费额度消耗记录可在账单中查看，账单记录按分钟汇总生成；控制台免费额度数据分钟级更新，支持手动刷新页面同步，请以控制台显示的免费额度数值为准。）

## 查看模型用量

在[模型用量](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/usage-statistics)页面查看。数据按业务空间维度统计，不支持按阿里云账号维度统计（[如何解决](raw/model-user-guide/model-monitoring/model-usage-statistics.md)）。数据延迟**约为 1 小时**。

1.  进入页面后，选择对应的模型类型（如**大语言模型**）页签，再按需选择时间范围。页面将汇总展示所选时间段内，该推理类型下所有已调用过模型的用量。
    
    > **统计时间范围：**不支持查看**30**天以前的统计数据。如需查询更早的用量信息，请通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance?month=2025-02&statisticItem=DEFAULT_CHARGE_ITEM&commodityCode%5BfilterMode%5D=IN&commodityCode%5Bvalues%5D=sfm_deployment_public_cn%26sfm_inference_public_cn%26sfm_training_public_cn&statisticCycle=MONTHLY_SUMMARY)页面查询。
    
    > **按推理类型筛选：**仅「大语言模型」页签支持按推理类型（[实时推理](https://help.aliyun.com/zh/model-studio/model-usage-statistics#fde237cc636jb) 或 [批量推理](https://help.aliyun.com/zh/model-studio/model-usage-statistics#fde237cc636jb)）筛选；若该空间下从未产生过「批量推理」用量数据，推理类型下拉框只会显示「实时推理」。
    
    > **时间精度：**支持按**分钟**、**小时**、**天**三种精度查看。时间跨度超过 1 天时分钟精度不可选，超过 7 天时仅支持按天查看。
    
    > **按 API-KEY 筛选：**可通过 API-KEY 下拉框筛选指定 API Key 调用产生的用量。
    
2.  如需查询某个具体模型的用量，可在页面右侧搜索框输入模型名称（如`qwen-plus`）筛选对应数据。
    
    > 可前往模型列表查询模型名称。
    
3.  页面底部「总调用成功次数 Top 10 模型」区域汇总展示调用次数最多的 10 个模型，支持全屏查看和下载数据。
    

「调用模型」表格按模型 Code 列出各模型的调用量、Token 用量等用量指标（指标列随所选模型类型不同而不同）。表格与图表区域的常用操作：

-   点击单行**查看详情**，进入模型用量详情页查看该模型更细粒度的调用趋势。
-   筛选条件较多时可用**重置**清空，并按需**收起/展开**筛选区域。
-   「概览」页签以指标卡片汇总关键用量；「更多指标」页签可切换不同用量维度的趋势图。

## 查看费用概览

在[费用概览](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/overview)页面，可查看百炼服务的费用汇总信息，包括：

-   **费用卡片**：展示当前账期的总消费金额、订阅购买费用和账单费用，并可跳转查看明细。
-   **账单趋势**：以图表或列表形式展示费用趋势，支持按月或按天统计，可按产品分类、API Key ID、模型筛选。
-   **费用告警**：可设置费用告警，在费用异常时及时收到通知。

## 模型用量统计单位说明

在阿里云百炼，不同模型的用量统计口径如下：

**类型**

**二级分类**

**统计单位**

**计费说明（模型调用）**

**大语言模型**

[文本生成模型](https://help.aliyun.com/zh/model-studio/model-pricing#2b7020e41703h)

[Token](raw/model-user-guide/model-monitoring/model-usage-statistics.md)

按输入和输出对应的 Token 数计费。

[深度思考模型](https://help.aliyun.com/zh/model-studio/deep-thinking)

[视觉理解模型](https://help.aliyun.com/zh/model-studio/vision)

**视觉模型**

[图像生成](https://help.aliyun.com/zh/model-studio/model-pricing#8cdb63420ce6j)

**张**

按成功生成的 **图像张数**计费。

视频生成

**秒**

按成功生成的 **视频秒数** 计费。

**语音模型**

[语音合成模型](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide)

**秒、字符或 Token**

可能按音频时长（秒）、对应的文本字符数或 Token 数计费，视模型而定。

[实时语音合成模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)

[录音文件识别模型](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)

[实时语音识别模型](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide)

[音视频翻译模型](https://help.aliyun.com/zh/model-studio/qwen3-livetranslate-flash)

**全模态模型**

[全模态模型](https://help.aliyun.com/zh/model-studio/qwen-omni)

**Token**

文本部分按 Token 数，其他模态（音频、图像、视频）按对应的 Token 数计费。

[实时多模态模型](https://help.aliyun.com/zh/model-studio/realtime)

**向量模型**

[多模态向量模型](raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)

**Token**

按输入文本的 Token 数计费。

文本向量模型

## 应用于生产环境

管理模型用量建议：

-   **控制模型输出长度：** 在调用模型 API 时，合理[限制思考长度](https://help.aliyun.com/zh/model-studio/deep-thinking#6f0633b9cdts1)和设置 `max_tokens` 参数，可限制模型单次生成内容的最大长度（从而控制费用）。
-   **根据任务类型选择模型：** 对于分类、摘要等简单任务，优先选择成本更低的轻量级模型，而不是始终使用功能强大但价格也较高的模型。
-   **监控与告警：** 通过[模型监控](raw/model-user-guide/model-monitoring/model-telemetry.md)监控用量趋势，并可配置用量告警，当用量出现异常时及时收到通知。
-   **优化 Prompt：** 简洁、清晰的 Prompt 不仅能提升模型输出质量，也能减少不必要的输入 Token 消耗。
-   **使用批量推理：** 对于非实时、大批量的处理任务，使用[批量推理](https://help.aliyun.com/zh/model-studio/batch-inference)通常比实时调用更具成本优势。

## 名词解释

**名词**

**解释**

**Token**

大模型以 Token 为单位处理输入和输出。一个 Token 可能是：

-   **单个字符：**如`A`、`我`
    
-   **完整的单词：**如`large`、`Model`
    
-   **长单词的一部分：**一个长单词通常会被拆分为多个 Token，拆分的过程称为分词。
    

根据经验，平均**1**个汉字约对应 **1.5-2** 个 Token；**1** 个英文字母约对应 **0.25** 个 Token；**1** 个英文单词约对应 **1.3** 个 Token：

-   `阿里云百炼`：约 **4-5** 个 Token
    
-   `Hello World`：约 **2** 个 Token
    

每个模型都有最大输入和输出 Token 数（详见模型列表），超过限制会导致请求失败。

**实时推理**

指对模型的所有直接和间接调用，主要涵盖以下场景：

-   API调用
    
-   模型广场
    
-   [阿里云百炼应用](raw/application-user-guide/llm-application/application-introduction.md)（智能体/工作流/智能体编排应用，以及涉及到模型调用的节点，如大模型节点、意图分类节点以及智能体群组节点等）的测试态和发布态
    
-   [Assistant API（下线中）](https://help.aliyun.com/zh/model-studio/assistant-api)调用
    
-   应用调用
    
-   [Prompt反馈优化](raw/application-user-guide/prompt/prompt-feedback-optimization.md)
    
-   [模型评测](raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
    

**批量推理**

对于无需实时响应的场景，通过[OpenAI兼容-Batch（文件输入）](raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)接口以离线方式进行的大规模数据处理。

## 常见问题

**Q: 如何查我的阿里云账号的 Token 总用量？**

A: 使用阿里云账号（主账号）访问[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面并导出账单，然后在账单中查看 Token 用量。

在**账单详情**页面，按以下条件筛选并导出：

1.  将**账单月份**设置为目标月份（如 `2025-05`）
2.  在**产品名称**中选择**大模型服务平台百炼**
3.  单击表格右上方的下载图标导出账单数据

**Q: 可以在阿里云 App 查看免费额度和模型用量吗？**

A: 暂不支持。阿里云 App 目前不支持查看百炼的免费额度使用情况和模型用量数据。请登录 PC 端，进入百炼控制台的[免费额度](https://bailian.console.aliyun.com/cn-beijing/?tab=costing-balance#/costing-balance/free-quota)或[模型用量](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/usage-statistics)页面查看。
