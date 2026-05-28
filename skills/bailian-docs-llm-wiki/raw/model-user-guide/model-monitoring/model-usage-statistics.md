# 模型用量

介绍如何查看阿里云百炼各模型的用量。

> 如需了解免费额度相关内容，请参考[新人免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)文档。您也可以在[免费额度](https://bailian.console.aliyun.com/?tab=model#/model-usage/free-quota)页面查看和管理免费额度使用情况。

## 适用范围

-   **支持的模型**：[模型列表](https://help.aliyun.com/zh/model-studio/models)中的所有模型均支持查看用量，包括基于它们[调优后的模型](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#f17bf700c06k5)。
    

## 查看免费额度使用情况

### 在控制台查看免费额度使用情况

1.  进入[模型用量：免费额度](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-usage/free-quota)页面，选择模型类型页签查看各模型的免费额度使用情况。
    
2.  在全部模型表格中，可通过搜索、排序、筛选等方式查找特定模型，并可切换**免费额度用完即停**开关或使用批量操作功能管理免费额度设置。
    

**说明**

**免费额度用完即停：**开启后，免费额度用尽时服务将自动停止（返回403错误：AllocationQuota.FreeTierOnly），避免产生免费额度以外的费用。若您希望在免费额度用尽后仍继续使用模型服务，并根据实际产生的用量付费，请保持本功能关闭状态。您只能在账户内仍有未消耗的免费额度时开启本功能。一旦功能开启，若您需要关闭本功能，需要在免费额度完全消耗后再进行关闭（免费额度出账周期为分钟级；控制台免费额度数据非实时、可能有延迟，请以控制台显示的免费额度数值为准）

## 查看模型用量

在[模型用量：用量统计](https://bailian.console.aliyun.com/?tab=model#/model-usage/usage-statistics)页面查看。数据按[业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)维度统计，不支持按阿里云账号维度统计（[如何解决](#c030d2aac0bxx)）。数据延迟**约为 1 小时**。

1.  进入页面后，选择对应的模型类型（如**大语言模型**）页签，再按需选择统计时间范围。页面将汇总展示所选时间段内，该推理类型下所有已调用过模型的用量。
    
    > **统计时间范围：**不支持查看 **30** 天以前的统计数据。如需查询更早的用量信息，请通过[费用与成本](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance?month=2025-02&statisticItem=DEFAULT_CHARGE_ITEM&commodityCode%5BfilterMode%5D=IN&commodityCode%5Bvalues%5D=sfm_deployment_public_cn%26sfm_inference_public_cn%26sfm_training_public_cn&statisticCycle=MONTHLY_SUMMARY)页面查询。
    
    > **按推理类型筛选：**仅「大语言模型」页签支持按推理类型（[实时推理](#fde237cc636jb) 或 [批量推理](#fde237cc636jb)）筛选；若该空间下从未产生过「批量推理」用量数据，推理类型下拉框只会显示「实时推理」。
    
2.  如需查询某个具体模型的用量，可在页面右侧搜索框输入模型名称（如`qwen-plus`）筛选对应数据。
    
    > 可前往[模型列表](https://help.aliyun.com/zh/model-studio/models)查询模型名称。
    

## **模型用量统计单位说明**

在阿里云百炼，不同模型的用量统计口径如下：

**类型**

**二级分类**

**统计单位**

**计费说明（模型调用）**

**大语言模型**

[文本生成模型](https://help.aliyun.com/zh/model-studio/model-pricing#2b7020e41703h)

[Token](#eae8bce7dd72t)

按输入和输出对应的 Token 数计费。

[深度思考模型](https://help.aliyun.com/zh/model-studio/deep-thinking)

[视觉理解模型](https://help.aliyun.com/zh/model-studio/vision)

**视觉模型**

[图像生成](https://help.aliyun.com/zh/model-studio/model-pricing#8cdb63420ce6j)

**张**

按成功生成的 **图像张数** 计费。

[视频生成](https://help.aliyun.com/zh/model-studio/models#a42bdc182c8ee)

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

[多模态向量模型](https://help.aliyun.com/zh/model-studio/multimodal-embedding-api-reference)

**Token**

按输入文本的 Token 数计费。

文本向量模型

## **应用于生产环境**

管理模型用量建议：

-   **控制模型输出长度：** 在调用模型 API 时，合理[限制思考长度](https://help.aliyun.com/zh/model-studio/deep-thinking#6f0633b9cdts1)和设置 `[max_tokens](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)` 参数，可限制模型单次生成内容的最大长度（从而控制费用）。
    
-   **根据任务类型选择模型：** 对于分类、摘要等简单任务，优先选择成本更低的轻量级模型（如 `qwen-turbo`），而不是始终使用功能强大但价格也较高的模型（如 `qwen-max`）。
    
-   **监控与告警：** 通过[模型监控](https://help.aliyun.com/zh/model-studio/model-telemetry/)监控用量趋势，并可配置用量告警，当用量出现异常时及时收到通知。
    
-   **优化 Prompt：** 简洁、清晰的 Prompt 不仅能提升模型输出质量，也能减少不必要的输入 Token 消耗。
    
-   **使用批量推理：** 对于非实时、大批量的处理任务，使用[批量推理](https://help.aliyun.com/zh/model-studio/batch-inference)通常比实时调用更具成本优势。
    

## **名词解释**

**名词**

**解释**

**Token**

大模型以 Token 为单位处理输入和输出。一个 Token 可能是：

-   **单个字符：**如`A`、`我`
    
-   **完整的单词：**如`large`、`Model`
    
-   **长单词的一部分：**一个长单词通常会被拆分为多个 Token，拆分的过程称为分词。
    

根据经验，平均 **1** 个汉字约对应 **1.5-2** 个 Token；**1** 个英文字母约对应 **0.25** 个 Token；**1** 个英文单词约对应 **1.3** 个 Token：

-   `阿里云百炼`：约 **4-5** 个 Token
    
-   `Hello World`：约 **2** 个 Token
    

每个模型都有最大输入和输出 Token 数（详见[模型列表](https://help.aliyun.com/zh/model-studio/models)），超过限制会导致请求失败。

**实时推理**

指对模型的所有直接和间接调用，主要涵盖以下场景：

-   API调用
    
-   模型广场
    
-   [阿里云百炼应用](https://help.aliyun.com/zh/model-studio/application-introduction)（智能体/工作流/智能体编排应用，以及涉及到模型调用的节点，如大模型节点、意图分类节点以及智能体群组节点等）的测试态和发布态
    
-   [Assistant API](https://help.aliyun.com/zh/model-studio/assistant-api/)调用
    
-   [应用调用](https://help.aliyun.com/zh/model-studio/application-calling-guide)
    
-   [Prompt反馈优化](https://help.aliyun.com/zh/model-studio/prompt-feedback-optimization)
    
-   [模型评测](https://help.aliyun.com/zh/model-studio/model-evaluation-overview)
    

**批量推理**

对于无需实时响应的场景，通过[OpenAI兼容-Batch（文件输入）](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)接口以离线方式进行的大规模数据处理。

## 常见问题

**Q: 如何查我的阿里云账号的 Token 总用量？**

A: 使用阿里云账号（主账号）访问[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面并导出账单，然后在账单中查看 Token 用量。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3694117471/p952403.png)
