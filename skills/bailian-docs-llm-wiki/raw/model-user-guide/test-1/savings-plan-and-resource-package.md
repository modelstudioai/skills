# 节省计划与资源包

为有效管理和优化在阿里云百炼平台上使用大模型的成本，阿里云百炼提供了节省计划、资源包等多种计费优惠方案。

## 选型指南

可参考以下选型指南快速选择：

-   [AI 通用型节省计划](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#bi9fizb4qqi7x)**（推荐）**：通过承诺每月消费金额来换取阶梯式折扣，最高可享 5.3 折优惠。该方案可抵扣[阿里直供](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#85a29cab67489)的全部模型，灵活性最高，**是绝大多数场景下的首选**。
-   [其他模型节省计划](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#cb5e825e04esu)：一次性购买固定金额，用于抵扣特定模型系列的调用费用。仅适用于特定模型系列（如语音模型系列），且折扣通常不如AI 通用型节省计划，可按需使用。
-   [资源包](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#0a9293f0f8tuj)：一次性购买具体资源量（如Tokens、生成图片数量等）。仅适用于抵扣单个特定模型（例如 qwen-plus），且折扣通常不如 AI 通用型节省计划，可按需使用。

为最大化成本效益，建议优先了解并选择 [AI 通用型节省计划](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#bi9fizb4qqi7x)。

若不确定该如何选择，可参考以下对比：

**维度**

**节省计划**

**资源包**

**Token Plan**

计费模式

承诺月消费换阶梯折扣

一次性购买固定 Token 量

一次性购买 credits 额度

模型覆盖

覆盖全模型（阿里直供）

仅适用单个特定模型

仅支持部分模型

适用场景

长期稳定使用

用量小或集中特定模型

团队协作使用

选型建议：长期稳定使用大模型服务，选择**节省计划**；用量较小或调用集中在特定模型，选择**资源包**；需要团队协作共享额度，选择**Token Plan**。

百炼平台默认采用**按量后付费**模式，不支持直接提前赠送 Token 额度。如需提前锁定额度或降低使用成本，可选择购买**资源包**（一次性购买固定 Token 额度，立即生效抵扣）或**节省计划**（承诺每月消费金额换取阶梯折扣）。

## AI 通用型节省计划

### 核心优势

AI 通用型节省计划是针对大模型按量付费使用场景设计的折扣方案。只需承诺在一定期限内（3 个月、6 个月、12 个月或 24 个月）的月消费金额，即可在保留按量付费灵活性的基础上，享受阶梯式折扣，优化模型调用成本。其核心优势如下：

-   **覆盖全面**：可抵扣[阿里直供](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#85a29cab67489)的全部模型，一次购买即可跨模型使用。
-   **成本优化显著**：承诺消费金额越高、周期越长，折扣力度越大，最高可享 5.3 折优惠。
-   **管理流程便捷**：购买后可立即或按指定时间生效，无需手动激活或绑定，自动抵扣，支持自动续费。

### 使用说明

**生效时间**：可按需选择”下单后立即生效”或”指定时间（按小时）生效”。

**承诺周期说明**：节省计划以**动态月**为周期分配额度——从购买日/生效日起算，每满一个月为一个周期，**非自然月月初重置**；订购日次日 0 点重置为当月满额。月承诺周期结束时，剩余额度自动过期，不可累积到下一周期。举例：如果一次性订阅了 3 个月的节省计划（月承诺额度 1,000 元），**并非在 3 个月内获得 3,000 元总额度，而是每月独立获得 1,000 元额度**，当月未使用完的部分自动清零，不可累积到下个订阅月。若选择**包季**套餐（如 27 元抵 60 元），总额度 60 元分 3 个月按月发放（每月 20 元），不一次性到账。**包月**套餐则一次性发放当月全额额度，仅限购买日起动态月内使用。节省计划额度的扣减基于**实际出账时间**，而非任务提交时间。系统出账通常存在 2~10 分钟延迟，控制台数据刷新也存在延迟：若任务提交时账户显示仍有额度，但实际出账时节省计划已过期或额度已耗尽，仍会产生按量计费费用。建议设置较高的消费预警阈值以监控费用，避免因出账延迟导致意外欠费。

**调用方式**：百炼控制台模型体验、API 代码调用、接入第三方工具（如[OpenClaw](raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)等，填写按量计费接入凭证）。

**抵扣范围**：

-   **支持抵扣**：模型调用（输入和输出 Tokens）、模型原生工具调用（如 Function Call、网页抓取等）、上下文缓存、批量推理等产生的费用。
    
    节省计划的抵扣与调用方**服务器所在地域**无关（包括通过 **ECS** 等实例调用百炼 API 的场景）。只要服务器位于国内，且调用百炼 API 时选择华北2（北京）地域的 **Base URL**，产生的调用费用即可正常被节省计划抵扣，不受**跨区域调用**影响。
    
-   **不支持抵扣**：模型调优、模型部署的费用；**联网搜索插件**（独立计费，以实际账单为准）、**MCP 广场**、**通义深度搜索**、**案例检索**等插件或工具产生的费用；**Qoder** CN 产品当前仅支持通过 **Credits** 调用，不支持使用 AI 通用型节省计划抵扣。第三方工具可通过 API 接入百炼，但相关联网搜索费用不在节省计划抵扣范围内；通过**百炼 API** 调用模型产生的费用仍属于支持抵扣范围。
    

**知识库（RAG）费用与节省计划说明**：知识库使用过程中产生的向量模型（Embedding）和排序模型（Rerank）调用费用，属于 A 类模型调用范畴，可被 AI 通用型节省计划抵扣；如需专项抵扣，也可单独购买[向量及排序模型节省计划](raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。知识库的规格费用（运行时长，标准版 0.03 元/知识库/小时、旗舰版 0.2 元/RCU/小时）不属于模型调用费用，不在节省计划抵扣范围内，需通过资源包或按量付费结算。

**抵扣逻辑**：

-   抵扣顺序：**免费额度> 资源包> 其他模型节省计划 > AI 通用型节省计划 > 按量付费**。
-   多个同类型的节省计划：优先抵扣先到期的节省计划。若到期时间相同，则优先抵扣先购买的节省计划。
-   超出部分处理：如果同类节省计划全部到期或额度全部抵扣完后，仍有超出部分，自动转为按量付费。
-   多套餐并存场景：当同时拥有新订阅套餐（如**尊享坐席**）和原有加油包（资源包）时，优先使用新订阅套餐内的额度，待该套餐额度耗尽后，才使用加油包（资源包）额度。此规则是对上述「免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费」通用抵扣顺序的场景化补充。

**说明**若在模型设置中开启了**免费额度用完即停**功能（即**安心模式**，也称**仅使用免费额度**），当该模型的免费额度耗尽时，服务将自动停止，不产生后续按量计费账单，节省计划因此无法进行抵扣。如需继续使用节省计划抵扣调用费用，请在免费额度用尽后，进入模型设置手动关闭**免费额度用完即停**功能，服务即可恢复并切换至节省计划正常抵扣。

**查询账单**：请参见[如何查询节省计划账单](https://help.aliyun.com/zh/user-center/how-to-check-the-savings-plan-bill)。

### 购买指引

**购买方式**

[点击购买 AI 通用型节省计划](https://common-buy.aliyun.com/?commodityCode=sfm_GenAI_spn_cn)

**适用地域**

华北2（北京）、美国（弗吉尼亚）、新加坡、德国（法兰克福）、日本（东京）

**支持的抵扣范围**

不同档位享受不同的折扣。

-   A 类：千问（不含 qwen3.6-max-preview）、千问-开源、文本向量、多模态向量、排序模型、行业模型、模型原生工具调用（[Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling)、[网页抓取](https://help.aliyun.com/zh/model-studio/web-extractor)等）
    
-   B 类：图像生成、语音合成、语音识别与翻译、视频生成与编辑
    
-   C 类：qwen3.6-max-preview、DeepSeek、Kimi、GLM、MiniMax、HappyHorse
    
    > C 类中仅**阿里直供**版本支持抵扣，**三方直供**版本不支持抵扣。模型是否有阿里云直供版本，请以控制台模型广场实际展示为准。详情参见[三方直供模型支持抵扣 AI 通用型节省计划吗？](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#85a29cab67489)
    

**每月承诺消费金额范围**

用于抵扣模型服务按量计费的每月承诺消费额。可自定义金额，1000 元起，以 10 元为单位调整，不设上限。

**购买时长**

可选择以下四个档位的购买时长：3个月、6个月、1年、2年

**分期付费类型**

-   全预付：一次性支付整个**承诺周期**内的全部承诺消费金额，可享最大折扣。
-   零预付：购买时无需支付，之后按月支付承诺消费金额。**零预付需联系商务经理申请开通后使用。**

**折扣**

请参考[折扣信息](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#85335bf156qcf)。

**开通时间选择**

可按需选择“下单后立即生效”或“指定时间（按小时）生效”。

**支付方式限制**：节省计划和资源包仅支持**现金支付**。通过充值卡充值到账的金额虽会进入账户余额，但不可用于购买节省计划、资源包等预付费套餐。

### 折扣信息

不同模型、不同档位、承诺周期和付款方式享受不同的折扣。

例如：选择了为期 12 个月、每月承诺消费 10,000 元的节省计划，采用全预付的方式支付，此时调用千问文本生成模型（A 类）时，享受 8 折优惠，即一次原价 1 元的模型调用，实际从节省计划额度中抵扣 0.8 元。

以下表格中的金额范围含起始值、不含结束值。例如 1,000 - 5,000 表示金额大于等于 1,000 且小于 5,000。

**付款方式**

**月承诺金额（元）**

**A 类**

**B 类**

**C 类**

3个月

6个月

12个月

24个月

3个月

6个月

12个月

24个月

全周期

**全预付**

1,000 - 5,000

8.8折

8.6折

8.4折

8.2折

8.3折

8折

7.7折

7.4折

无折扣

5,000 - 10,000

8.6折

8.4折

8.2折

8折

8折

7.7折

7.4折

7.1折

无折扣

10,000 - 30,000

8.4折

8.2折

8折

7.8折

7.7折

7.4折

7.1折

6.8折

无折扣

30,000 - 50,000

8.2折

8折

7.8折

7.6折

7.4折

7.1折

6.8折

6.5折

无折扣

50,000 - 100,000

8折

7.8折

7.6折

7.4折

7.1折

6.8折

6.5折

6.2折

无折扣

100,000 - 300,000

7.8折

7.6折

7.4折

7.2折

6.8折

6.5折

6.2折

5.9折

无折扣

300,000 - 1,000,000

7.6折

7.4折

7.2折

7折

6.5折

6.2折

5.9折

5.6折

无折扣

1,000,000+

7.4折

7.2折

7折

6.8折

6.2折

5.9折

5.6折

5.3折

无折扣

**零预付**

> 需联系商务经理开通

1,000 - 5,000

9折

8.8折

8.6折

8.4折

8.5折

8.2折

7.9折

7.6折

无折扣

5,000 - 10,000

8.8折

8.6折

8.4折

8.2折

8.2折

7.9折

7.6折

7.3折

无折扣

10,000 - 30,000

8.6折

8.4折

8.2折

8折

7.9折

7.6折

7.3折

7折

无折扣

30,000 - 50,000

8.4折

8.2折

8折

7.8折

7.6折

7.3折

7折

6.7折

无折扣

50,000 - 100,000

8.2折

8折

7.8折

7.6折

7.3折

7折

6.7折

6.4折

无折扣

100,000 - 300,000

8折

7.8折

7.6折

7.4折

7折

6.7折

6.4折

6.1折

无折扣

300,000 - 1,000,000

7.8折

7.6折

7.4折

7.2折

6.7折

6.4折

6.1折

5.8折

无折扣

1,000,000 及以上

7.6折

7.4折

7.2折

7折

6.4折

6.1折

5.8折

5.5折

无折扣

### 生命周期管理

访问[节省计划总览页面](https://usercenter2.aliyun.com/resource/spn/overview)管理节省计划。

您也可通过**阿里云 App**查看节省计划的剩余额度、使用率等基本信息，功能与网页端控制台基本一致。但退订、配置变更等详细操作，建议使用网页端控制台完成。

#### 节省计划续订

登录[费用与成本](https://usercenter2.aliyun.com/home)控制台，左侧菜单选择**费用我的订阅**，查看并管理节省计划的订阅状态、生效时间、自动续费状态等。

**到期处理**：节省计划（含入门型 AI 通用节省计划）到期后会自动失效/作废，无需手动释放、退订或查找关联实例，也不会因到期本身产生额外费用。若后续不再使用大模型服务，建议删除对应的 **API Key**，避免因服务未停用而产生按量付费账单。

**入门型 AI 通用节省计划续费规则**：入门型 AI 通用节省计划为新客专享活动，到期后不支持续费；再次购买该计划时，无法再享受首购优惠价格。

#### 查询折扣

在 AI 通用型节省计划中，不同模型、不同档位、承诺周期和付款方式享受不同的折扣。可以访问[节省计划总览页面的「价格折扣详情表」页签](https://usercenter2.aliyun.com/resource/spn/overview)，按以下条件筛选查询：

-   **适用商品**：参考下表选择对应的商品名称。
-   **计费项**：参考下表选择对应的计费项。
-   **节省计划类型**：选择**AI 通用型节省计划/百炼AI通用型节省计划。**
-   **订购时长**和**支付方式**：选择对应的选项，查看按量折扣。

**适用商品**

**计费项**

百炼大模型推理

**文本**：全局文本生成Token用量

**图片**：全局图片生成张数用量、全局多规格图片生成张数用量、全局图片检测张数用量

**视频**：全局视频生成时长用量

**语音**：全局语音合成字数用量、全局语音识别时长用量、全局Cosyvoice语音合成字数用量、全局声音复刻及声音设计模型个数用量

**向量**：全局多模态向量模型用量、全局文本向量模型用量

**批量调用**：全局Batch模型用量、全局BatchChat模型用量、全局BatchChat Token用量、全局BatchChat视频生成时长用量

**工具调用**：全局计次用量

上述各计费项同时存在对应的非全局版本（如"文本用量"）。

> 查询华北2（北京）地域的调用费用折扣时，选择非全局计费项；查询其他地域时，选择对应的全局计费项。

百炼大模型-垂类模型

文本生成Token用量

阿里云百炼大模型-向量排序模型

多模态向量模型用量

百炼大模型-千问语音模型

语音合成字数用量、语音识别时长用量

百炼大模型-百聆语音模型

语音合成字数用量、语音识别时长用量

#### 查询账单

进入[费用与成本](https://usercenter2.aliyun.com/home)控制台，左侧菜单选择**账单详情**，**产品名称**选择**大模型服务平台百炼**，**商品名称**选择 **AI 通用型节省计划**。页面默认展示当月明细账单。详情请参考[如何查询节省计划账单](https://help.aliyun.com/zh/user-center/how-to-check-the-savings-plan-bill)。

#### 余量预警与到期提醒

节省计划不支持自定义余量预警阈值：系统默认在剩余额度降至 **20%** 时发送一次提醒，该阈值不可更改。如需自定义消费预警阈值，可前往**费用中心**的**可用额度预警**功能中设置消费金额阈值。

到期提醒方面，系统会在节省计划到期前通过短信发送 **3 次**提醒；到期后不再发送提醒。

## 其他模型节省计划

其他模型节省计划

与 AI 通用型节省计划相比，其他模型节省计划更适合用量较小或需求高度集中于某一特定模型的场景。

### 使用说明

**生效时间**：节省计划购买后立即生效。

**有效期说明**：有效期根据购买套餐而定。超出有效期后，节省计划中剩余的金额，将无法使用，不支持退款。

**抵扣范围**：支持抵扣模型调用费用（输入和输出 Tokens）。不支持抵扣工具调用、上下文缓存、批量推理等产生的费用。不支持抵扣模型调优、模型部署产生的费用。

**抵扣逻辑**：

-   抵扣顺序：**免费额度> 资源包> 其他模型节省计划 > AI 通用型节省计划 > 按量付费**。
-   多个同类型的节省计划：优先抵扣先到期的节省计划。若到期时间相同，则优先抵扣先购买的节省计划。
-   超出部分处理：如果同类节省计划全部到期或额度全部抵扣完后，仍有超出部分，自动转为按量付费。

**查询账单**：请参见[如何查询节省计划账单](https://help.aliyun.com/zh/user-center/how-to-check-the-savings-plan-bill)。

### 支持的节省计划

#### 大语言模型

**购买方式**

[点击购买大语言模型推理节省计划](https://common-buy.aliyun.com/?commodityCode=sfm_llminference_spn_public_cn)

**档位**

阿里云百炼提供购买的档位包括：20元、100元、1,000元、5,000元、10,000元、20,000元、50,000元、100,000元、200,000元、300,000元、500,000元。

**折扣**

上述档位均无折扣，按[模型调用价格](raw/model-user-guide/test-1/model-pricing.md)进行扣费。

**有效期**

-   对于20元档，有效期1个月。
    
-   对于100元档，有效期3个月。
    
-   对于1,000元档，有效期6个月。
    
-   对于5,000元、10,000元、20,000元、50,000元、100,000元、200,000元、300,000元、500,000元八档，有效期1年。
    

**适用地域**

华北2（北京）

**适用模型**

适用于已上架阿里云百炼平台并以 Token 计费的文本生成模型，模型范围包括：

-   通用大语言模型：
    
    -   商业版：千问 Max、千问 Plus、千问 Flash、千问 Turbo、QwQ、千问 Long
        
    -   开源版：Qwen3.5、Qwen3、QwQ、QwQ-Preview、Qwen2.5、Qwen-Math、Qwen-Coder
        
    -   第三方模型：DeepSeek、GLM、Kimi、MiniMax
        
-   多模态模型：
    
    -   商业版：千问Omni（不含 qwen3.5-omni 系列）、千问Omni-Realtime（不含 qwen3.5-omni-realtime 系列）、QVQ、千问VL、千问OCR
        
    -   开源版：Qwen-Omni、Qwen3-Omni-Captioner、Qwen-VL、QVQ
        
-   领域模型：千问Coder、千问翻译模型、千问数据挖掘模型、千问深入研究模型
    

不支持向量模型（embedding）和排序模型（rerank）。如需抵扣这些模型，请参考[AI 通用型节省计划](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#bi9fizb4qqi7x)或[向量及排序模型节省计划](raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

#### 千问语音模型

**购买方式**

[点击购买千问语音模型节省计划](https://common-buy.aliyun.com/?commodityCode=sfm_VoiceModel_spn_cn)

**购买说明**

阿里云百炼提供五个购买档位，分别为：

-   20元：享 9.8 折优惠
    
-   100元：享 9.6 折优惠
    
-   500元：享 9 折优惠
    
-   1,000元：享 8.5 折优惠
    
-   5,000元：享 8 折优惠
    

优惠示例：以 1,000元 档位为例，假设消费1元，实际将从节省计划中抵扣1\*0.85=0.85元。

ASR模型按秒计费，TTS模型按字符计费，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)查看模型调用价格。

**有效期**

-   对于20元、100元两档，有效期为6个月。
    
-   对于500元、1,000元、5,000元三档，有效期可选 6 个月或 12 个月。
    

**适用模型**

因地域而异：

-   华北2（北京）**：**
    
    -   **实时语音合成（CosyVoice）：**cosyvoice-v3-plus、cosyvoice-v3-flash、cosyvoice-v2、cosyvoice-v1
        
    -   **实时语音合成（Qwen-TTS-Realtime）：**qwen3-tts-flash-realtime、qwen3-tts-flash-realtime-2025-09-18、qwen-tts-realtime、qwen-tts-realtime-latest、qwen-tts-realtime-2025-07-15
        
    -   **语音合成（Qwen-TTS）：**qwen3-tts-flash、qwen3-tts-flash-2025-09-18、qwen-tts、qwen-tts-latest、qwen-tts-2025-05-22、qwen-tts-2025-04-10
        
    -   **实时语音识别（Paraformer）：**paraformer-realtime-v2、paraformer-realtime-v1、paraformer-realtime-8k-v2、paraformer-realtime-8k-v1
        
    -   **实时语音识别（Fun-ASR）：**fun-asr-realtime、fun-asr-realtime-2025-11-07、fun-asr-realtime-2025-09-15
        
    -   **实时语音识别（Qwen-ASR-Realtime）：**qwen3-asr-flash-realtime、qwen3-asr-flash-realtime-2025-10-27
        
    -   **录音文件识别（Paraformer）：**paraformer-v2、paraformer-v1、paraformer-8k-v2、paraformer-8k-v1、paraformer-mtl-v1
        
    -   **录音文件识别（Fun-ASR）：**fun-asr、fun-asr-2025-11-07、fun-asr-2025-08-25、fun-asr-mtl、fun-asr-mtl-2025-08-25
        
    -   **录音文件识别（Qwen-ASR）：**qwen3-asr-flash-filetrans、qwen3-asr-flash-filetrans-2025-11-17、qwen3-asr-flash、qwen3-asr-flash-2025-09-08
        
-   **新加坡：**
    
    -   **实时语音合成（Qwen-TTS-Realtime）：**qwen3-tts-flash-realtime、qwen3-tts-flash-realtime-2025-09-18
        
    -   **语音合成（Qwen-TTS）：**qwen3-tts-flash、qwen3-tts-flash-2025-09-18
        
    -   **实时语音识别（Qwen-ASR-Realtime）：**qwen3-asr-flash-realtime、qwen3-asr-flash-realtime-2025-10-27
        
    -   **录音文件识别（Fun-ASR）：**fun-asr、fun-asr-2025-11-07、fun-asr-2025-08-25
        
    -   **录音文件识别（Qwen-ASR）：**qwen3-asr-flash-filetrans、qwen3-asr-flash-filetrans-2025-11-17、qwen3-asr-flash、qwen3-asr-flash-2025-09-08
        

请前往百炼控制台查看全部模型。

#### 向量及排序模型

**购买方式**

[点击购买向量及排序模型服务节省计划](https://common-buy.aliyun.com/?commodityCode=sfm_embeddingrerank_spn_cn)

**购买说明**

阿里云百炼提供五个购买档位，分别为：

-   100元：无折扣
    
-   500元：享 9 折优惠
    
-   2,000元：享 8 折优惠
    
-   5,000元：享 7.5 折优惠
    
-   10,000元：享 7 折优惠
    

优惠示例：以 5,000元 档位为例，假设消费 1 元，实际将从节省计划中抵扣1\*0.75=0.75（元）。

**有效期**

-   对于100元、500元档位，有效期3个月。
    
-   对于2,000元档位，有效期6个月。
    
-   对于5,000元、10,000元档位，有效期12个月。
    

**适用地域**

华北2（北京）

**适用模型**

**文本向量**：text-embedding-v4、text-embedding-v3、text-embedding-v2、text-embedding-v1、text-embedding-async-v2、text-embedding-async-v1

**多模态向量**：qwen2.5-vl-embedding、tongyi-embedding-vision-plus、tongyi-embedding-vision-flash、multimodal-embedding-v1

**文本排序**：qwen3-rerank、gte-rerank-v2

请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)查看全部模型及其调用价格。

#### 万相模型节省计划

**购买方式**

[点击购买万相模型节省计划](https://common-buy.aliyun.com/?commodityCode=sfm_VideoAndImage_spn_cn)

**购买说明**

阿里云百炼提供五个购买档位，分别为：

-   20元：无折扣
    
-   100元：无折扣
    
-   1,000元：享 9.8 折优惠
    
-   10,000元：享 9.5 折优惠
    
-   30,000元：享 9 折优惠
    

优惠示例：以 1,000元 档位为例，假设生成某个视频消费 1 元，实际将从节省计划中抵扣1\*0.98=0.98（元）。

**有效期**

-   对于20元、100元两档，有效期3个月。
    
-   对于1,000元、10,000元、30,000元三档，有效期6个月。
    

**适用模型**

**图像生成**：wan2.6-image、wan2.6-t2i、wan2.5-t2i-preview、wan2.5-i2i-preview、wan2.2-t2i-plus、wan2.2-t2i-flash、wanx2.0-t2i-turbo、wanx2.1-t2i-plus、wanx2.1-imageedit、wanx2.1-t2i-turbo、wanx-sketch-to-image-lite、wanx-v1

**视频生成**：wan2.6-t2v、wan2.6-i2v、wan2.6-r2v、wan2.5-t2v-preview、wan2.5-i2v-preview、wan2.2-t2v-plus、wan2.2-i2v-flash、wan2.2-t2v-flash、wan2.2-i2v-plus、wan2.1-vace-plus、wan2.1-kf2v-plus、wan2.1-t2v-turbo、wanx2.1-t2v-plus、wanx2.1-i2v-turbo、wanx2.1-i2v-plus

请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)查看全部模型及其调用价格。

## 资源包

资源包

预先购买的是具体的 Token 数量，用于抵扣特定模型**超出免费额度后**产生的实时推理用量。

### 使用说明

**生效时间**：资源包购买后立即生效，无需手动“激活”或“绑定”。

**有效期说明**：有效期根据购买套餐而定。超出有效期后，资源包中剩余的Tokens，自动作废。

**抵扣逻辑**：

-   抵扣顺序：**免费额度> 资源包> 其他模型节省计划 > AI 通用型节省计划 > 按量付费**。
-   多个同类型的资源包：优先抵扣先到期的资源包。若到期时间相同，则优先抵扣先购买的资源包。
-   超出部分处理：如果同类资源包全部到期或额度全部抵扣完后，若仍有超出部分，自动转为按量付费。

**余量监控与预警：**

-   **查看余量**：点击[资源包](https://billing-cost.console.aliyun.com/ri/summary?commodityCode=fr)查看剩余量情况，点击**使用明细**查看使用信息。具体请参见[资源包介绍与选购](https://help.aliyun.com/zh/user-center/resource-package-instance-management)。
-   **设置预警**：建议[设置资源包余量预警](https://help.aliyun.com/zh/user-center/configure-balance-alerts)。当资源包使用量低于预设阈值时，系统将通过短信、邮件及站内信自动触发通知。

**退订说明**：

-   根据[退订规则](https://help.aliyun.com/zh/user-center/cancel-subscription/)，预付费商品未发生使用的部分，可按未使用额度费用[申请退款](https://billing-cost.console.aliyun.com/refund/refund?commodityType=RESOURCE_PLANS&refundType=NOREASON_REFUND)；已使用的部分则无法退款。退款将原路返回至支付账户，不会退至阿里云账户余额。
    
    若账号下存在**未到期**的节省计划或资源包，无法直接完成账号注销。建议等待节省计划/资源包**自然到期**失效后再申请账号注销；或在符合退订条件时先完成退订操作。需注意，节省计划一旦生效并发生过抵扣，通常不支持退订，只能等待自然到期。
    
    如需自助退订大语言模型推理资源包，操作步骤如下：登录**阿里云控制台**，访问[资源退订](https://billing-cost.console.aliyun.com/refund/refund)页面，在列表中找到对应的大语言模型推理资源包，单击**自助退订**按钮完成退订。
    

**使用限制**：资源包按模型名称严格匹配，**跨版本或子型号不通用**，请以资源包购买页标注的适用模型为准。例如，qwen-plus 资源包不支持抵扣 qwen-max 的调用费用；若需要同时覆盖多个模型版本的调用费用，建议选择 AI 通用型节省计划。

### 大语言模型推理资源包

**订购地址**

[大语言模型推理资源包 qwen-plus](https://common-buy.aliyun.com/?commodityCode=sfm_llminference_dp_cn#/buy)

[大语言模型推理资源包 qwen-max](https://common-buy.aliyun.com/?commodityCode=sfm_llminference2_dp_cn#/buy)

**适用地域**

华北2（北京）

华北2（北京）

**适用模型**

qwen-plus 及 qwen-plus-latest的实时推理服务（[非思考模式](https://help.aliyun.com/zh/model-studio/deep-thinking)）

qwen-max的实时推理服务（[非思考模式](https://help.aliyun.com/zh/model-studio/deep-thinking)）

**包含输入和输出总Tokens**

1,200万/1.1亿

1,800万/3,900万/3.9亿/11.7亿/19.5亿

**价格（元）**

11.66/114.4

57.6/125/1250/3750/6250

**有效期**

自购买日起生效，有效期可选 3 个月、6 个月或 1 年。

自购买之日起有效期为 1 年。

**使用限制**

-   **qwen-plus**、**qwen-plus-latest**
    
    -   仅支持抵扣单次请求输入在`0<Token≤128K`阶梯范围内的实时推理费用（[非思考模式](https://help.aliyun.com/zh/model-studio/deep-thinking)，包含输入和输出）。
        
    -   不支持抵扣的费用包括：
        
        -   单次请求输入在`Token>128K`阶梯范围产生的费用。
            
        -   [Batch调用](raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)、[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)、[模型调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)、[模型部署](raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)产生的费用。
            
-   **qwen-max**
    
    -   仅支持抵扣实时推理产生的费用（[非思考模式](https://help.aliyun.com/zh/model-studio/deep-thinking)，包含输入和输出），不支持抵扣[Batch调用](raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)、[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)、[模型调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)、[模型部署](raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)产生的费用。
        

### 图像生成模型资源包

**订购地址**

[千问图像生成模型资源包qwen-image](https://common-buy.aliyun.com/?commodityCode=sfm_qwenimage_dp_cn)

[千问图像生成模型资源包qwen-image-plus](https://common-buy.aliyun.com/?commodityCode=sfm_qwenimageplus_dp_cn)

**适用地域**

华北2（北京）

华北2（北京）

**适用模型**

**文生图**：qwen-image

**图像编辑**：qwen-image-edit

**文生图**：qwen-image-plus

**图像编辑**：qwen-image-edit-plus

**资源包容量（生成图片张数）**

80/400

100/1,000/10,000/100,000/500,000

**价格（元）**

20/100

享阶梯折扣：

20/196（9.8折）/1,900（9.5折）/18,000（9折）/85,000（8.5折）

**有效期**

自购买之日起有效期为 3 个月。

对于100、1,000张档位，自购买之日起有效期为3个月。

对于10,000、100,000张档位，自购买之日起有效期为6个月。

对于500,000张档位，自购买之日起有效期为12个月。

**说明**

使用文生图模型生成一张图片消耗 1 张额度，使用图片编辑模型编辑一张图片消耗 1.2 张额度。

资源包容量耗尽后，将自动转为按量付费模式，超出部分按各模型对应的价格进行计费，详见[模型调用计费](raw/model-user-guide/test-1/model-pricing.md)。

生成或编辑一张图片消耗 1 张额度。

资源包容量耗尽后，将自动转为按量付费模式，超出部分按各模型对应的价格进行计费，详见[模型调用计费](raw/model-user-guide/test-1/model-pricing.md)。

## 常见问题

### 节省计划和资源包是否支持退订？

-   节省计划：自 2026 年 04 月 03 日 10:00:00（UTC+8）起，符合以下条件的节省计划支持自助退订，可在[资源退订](https://billing-cost.console.aliyun.com/refund/refund)控制台中操作：
    
    -   未生效的全预付节省计划。
    -   已生效但未发生任何抵扣的全预付节省计划。
    
    若购买的节省计划已发生抵扣，暂不支持退订，详见[公告](https://www.aliyun.com/notice/118142?spm=5176.29512420.J_JASdJ65l9Zg8lf6Fc9UC_.5.290219d5iwnIxR)。
    
-   资源包：未发生使用的部分，可按未使用额度费用[申请退款](https://billing-cost.console.aliyun.com/refund/refund?commodityType=RESOURCE_PLANS&refundType=NOREASON_REFUND)；已使用的部分则无法退款。
    

### 资源包和节省计划如果同时存在，怎么扣费？

系统的抵扣优先级为：**免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费**。即：先用免费额度；用完后扣资源包；资源包不够或不适用时，扣节省计划；最后才使用账户余额。

### 为什么购买了节省计划，但没有抵扣？

常见原因如下：

1.  **模型不匹配**：购买了其他节省计划，但调用的模型不在适用范围内。例如：购买了大语言模型节省计划，却调用了万相系列模型或向量模型（embedding）、排序模型（rerank）。可以选择购买 [AI 通用型节省计划](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#bi9fizb4qqi7x)以实现跨模型抵扣。
2.  **使用了不支持的功能**：AI 通用型节省计划和其他节省计划均不支持抵扣[模型调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)、[模型部署](raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)费用。只有 AI 通用型节省计划支持抵扣上下文缓存、批量推理、工具调用等产生的费用，而其他节省计划不支持。
3.  **免费额度未用完**：系统抵扣顺序为：**免费额度 > 节省计划**。节省计划仅抵扣免费额度用尽后产生的账单。
4.  **按分钟出费**：百炼按分钟计费，账单中的计费时间区间精确到分钟（例如 17:20:00–17:25:00），且不与整点对齐。购买节省计划后，自下一分钟产生的用量起开始抵扣，因此购买时刻正在计量的那个分钟区间可能仍按按量付费出账。
5.  **起效时间对齐整点**：节省计划的起效时间会自动对齐至购买时刻所在的整点。例如 14:56 购买，起效时间为 14:00，该整点之内（14:00 至购买时刻）已产生的用量会被回溯抵扣；早于该整点产生的费用不在抵扣范围内。
6.  **账单中如何确认已抵扣**：在**账单详情**中，一条账单的**应付金额**为 0 表示该笔费用已被节省计划全额抵扣。展开该账单行可查看**目录总价**与**优惠抵扣明细**，据此确认抵扣是否已发生。

### 三方直供模型支持抵扣 AI 通用型节省计划吗？

[C 类模型](raw/model-user-guide/test-1/savings-plan-and-resource-package.md)中，阿里直供的模型支持抵扣，三方直供的模型不支持抵扣。您可以在[百炼模型广场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)中通过模型卡片右上角标识（"阿里直供"或"三方直供"标签）确认模型的供应方式。

### 购买节省计划后如何使用？

节省计划在生效后无需重新配置 **API Key** 或 **Base URL**，购买后自动生效。您通过百炼控制台模型体验、API 代码调用或接入第三方工具调用模型时，产生的费用会按[抵扣顺序](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#59b7ecf08fiac)自动抵扣。节省计划仅对**生效后产生的费用**进行抵扣，购买前已产生的费用无法追溯抵扣。您可以在[节省计划总览页面](https://usercenter2.aliyun.com/resource/spn/overview)查看抵扣明细和剩余额度。

### 为什么购买了资源包，但没有抵扣？

资源包的抵扣需要满足特定条件，常见原因如下：

1.  模型不匹配：调用的模型与购买的资源包不一致。例如，购买 qwen-max 资源包却调用了 qwen-plus 模型。
2.  使用了不支持的功能：资源包**不支持抵扣**这些功能产生的费用：[批量推理（Batch）](https://help.aliyun.com/zh/model-studio/batch-inference)、[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)、[模型调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)、[模型部署](raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
3.  Token 长度超限：对于 qwen-plus 资源包，单次请求输入超过 128K Token 的部分无法抵扣。
4.  免费额度未用完：系统抵扣顺序为：**免费额度 > 资源包**。资源包仅抵扣免费额度用尽后产生的账单。

### 如果先购买了资源包但未开通阿里云百炼服务，应该如何使用？

请先[开通阿里云百炼的模型服务](raw/model-api-reference/preparations/get-api-key.md)。服务开通后，优先会抵扣免费额度，待免费额度消耗完后，才会开始抵扣资源包。

### 购买了大语言模型节省计划，能抵扣向量模型（embedding）和排序模型（rerank）吗？

不能。大语言模型推理节省计划仅适用于文本生成模型，不支持抵扣向量模型和排序模型。如果您的业务同时涉及大语言模型与向量、排序模型（例如 RAG 场景），建议选择[AI 通用型节省计划](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#bi9fizb4qqi7x)，或单独购买[向量及排序模型节省计划](raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

### 入门型AI通用节省计划和 AI 通用型节省计划有什么区别？

两者的主要区别如下：

**对比项**

**AI 通用型节省计划**

**入门型AI通用节省计划**

**购买入口**

通过[AI通用型节省计划购买页](https://common-buy.aliyun.com/?commodityCode=sfm_GenAI_spn_cn)购买

通过[AI优惠活动页](https://www.aliyun.com/benefit/scene/ai-discount)的"全模型通享"模块购买

**活动限制**

无首购限制

活动价格仅限**首购**

**适用模型**

详见[购买指引](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#nqdi1bsux4qx0)中的抵扣范围

与 AI 通用型节省计划支持的模型范围相同，详见[购买指引](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#nqdi1bsux4qx0)中的抵扣范围

**折扣方式**

不同档位对应不同按量付费折扣，档位越高折扣越大

按量计费，无按量付费折扣；仅首次购买时有优惠，档位以购买页为准（例如：10 元抵 20 元、27 元抵 60 元、135 元抵 300 元）

入门型 AI 通用节省计划还需注意以下使用规则：

-   **额度清零**：每月额度按动态月独立发放，当月未使用完的部分自动清零，不累积到下一周期。**包季**套餐（如 27 元抵 60 元）总额度分 3 个月按月发放（每月 20 元），不一次性到账。
-   **退订政策**：一经支付，不支持退订，请在购买前确认档位和需求。
-   **抵扣范围**：与 AI 通用型节省计划相同，仅支持抵扣阿里直供模型产生的调用费用，**不支持**第三方直供模型（C 类中的三方直供模型）。

节省计划账单请参见[节省账单使用明细](https://billing-cost.console.aliyun.com/resource/spn/detail)。

### 退订节省计划后，关联权益是否受影响？

退订节省计划或优惠到期后，请注意以下规则：

-   **新客优惠**：入门型 AI 通用节省计划的活动优惠**仅限首次购买**，退订后无法再次以优惠价格参与同一活动。
-   **赠品处理**：若购买时附带赠品（如代金券、优惠券、延长服务期等），退订后赠品**自动作废清零**，不予保留或退还。
-   **余额与转移**：节省计划余额及订单**不支持跨账号转移**，也**不支持转换为账户现金余额**。
