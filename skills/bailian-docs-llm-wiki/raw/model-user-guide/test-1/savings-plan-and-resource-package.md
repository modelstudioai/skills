# 节省计划与资源包

为有效管理和优化在阿里云百炼平台上使用大模型的成本，阿里云百炼提供了节省计划、资源包等多种计费优惠方案。

## 选型指南

可参考以下选型指南快速选择：

-   [AI 通用型节省计划](#universal-savings-plan)**（推荐）**：通过承诺每月消费金额来换取阶梯式折扣，最高可享 5.3 折优惠。该方案可抵扣[阿里直供](#85a29cab67489)的全部模型，灵活性最高，**是绝大多数场景下的首选**。
    
-   [其他模型节省计划](#cb5e825e04esu)：一次性购买固定金额，用于抵扣特定模型系列的调用费用。仅适用于部分模型系列（如万相系列、语音模型系列等），且折扣通常不如AI 通用型节省计划，可按需使用。
    
-   [资源包](#0a9293f0f8tuj)：一次性购买具体资源量（如Tokens、生成图片数量等）。仅适用于抵扣单个特定模型（例如 qwen-plus），且折扣通常不如 AI 通用型节省计划，可按需使用。
    

为最大化成本效益，建议优先了解并选择 [AI 通用型节省计划](#universal-savings-plan)。

## **AI 通用型节省计划**

### **核心优势**

AI 通用型节省计划是针对大模型按量付费使用场景设计的折扣方案。只需承诺在一定期限内（3 个月、6 个月、12 个月或 24 个月）的月消费金额，即可在保留按量付费灵活性的基础上，享受阶梯式折扣，优化模型调用成本。其核心优势如下：

-   **覆盖全面**：可抵扣[阿里直供](#85a29cab67489)的全部模型，一次购买即可跨模型使用。
    
-   **成本优化显著**：承诺消费金额越高、周期越长，折扣力度越大，最高可享 5.3 折优惠。
    
-   **管理流程便捷**：购买后可立即或按指定时间生效，无需手动激活或绑定，自动抵扣，支持自动续费。
    

### **使用说明**

**生效时间**：可按需选择“开通后立即生效”或“指定时间（按小时）生效”。

**承诺周期说明**：**以月为单位**（从生效日到下个月的对应日），月承诺周期结束时，剩余额度自动过期，不可累积到下一周期。举例：如果一次性订阅了 3 个月的节省计划（月承诺额度 1000 元），**并非在 3 个月内获得 3000 元总额度，而是每月独立获得 1000 元额度**，当月未使用完的部分自动清零，不可累积到下个订阅月。

**抵扣范围**：

-   **支持抵扣**：模型调用（输入和输出 Tokens）、模型原生工具调用（如 Function Call、联网搜索、网页抓取等）、上下文缓存、批量推理等产生的费用。
    
-   **不支持抵扣**：模型调优、模型部署的费用，以及 MCP 广场和模型体验的联网搜索的费用。
    

**抵扣逻辑**：

-   抵扣顺序：**免费额度** **\> 资源包** **> 其他模型节省计划 > AI 通用型节省计划 > 按量付费**。
    
-   多个同类型的节省计划：优先抵扣先到期的节省计划。若到期时间相同，则优先抵扣先购买的节省计划。
    
-   超出部分处理：如果同类节省计划全部到期或额度全部抵扣完后，仍有超出部分，自动转为按量付费。
    

**查询账单**：请参见[如何查询节省计划账单](https://help.aliyun.com/zh/user-center/how-to-check-the-savings-plan-bill)。

### **购买指引**

**购买方式**

[点击购买 AI 通用型节省计划](https://common-buy.aliyun.com/?commodityCode=sfm_GenAI_spn_cn)

**适用地域**

华北2（北京）、美国（弗吉尼亚）、新加坡、德国（法兰克福）

**支持的抵扣范围**

不同档位享受不同的折扣。

-   A 类：千问（不含 qwen3.6-max-preview）、千问-开源、文本向量、多模态向量、排序模型、行业模型、模型原生工具调用（[Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling)、[联网搜索](https://help.aliyun.com/zh/model-studio/web-search)、[网页抓取](https://help.aliyun.com/zh/model-studio/web-extractor)等；不含 MCP 广场和模型体验的联网搜索）
    
-   B 类：图像生成、语音合成、语音识别与翻译、视频生成与编辑
    
-   C 类：qwen3.6-max-preview、DeepSeek、Kimi、GLM、MiniMax、HappyHorse
    
    > 三方直供模型不支持抵扣，详情参见[三方直供模型支持抵扣 AI 通用型节省计划吗？](#85a29cab67489)
    

**每月承诺消费金额**

用于抵扣模型服务按量计费的每月承诺消费额。可自定义金额，1000 元起，以 10 元为单位调整，不设上限。

**承诺周期**

可选择以下四个档位的承诺周期：3个月、6个月、12个月、24个月

**付费方式**

-   全预付：一次性支付整个**承诺周期**内的全部承诺消费金额，可享最大折扣。
    
-   零预付：购买时无需支付，之后按月支付承诺消费金额。**零预付需联系商务经理开通白名单后使用。**
    

**折扣**

请参考[折扣信息](#85335bf156qcf)。

**开通时间选择**

可按需选择“开通后立即生效”或“指定时间（按小时）生效”。

### 折扣信息

不同模型、不同档位、承诺周期和付款方式享受不同的折扣。

例如：选择了为期 12 个月、每月承诺消费 10,000 元的节省计划，采用全预付的方式支付，此时调用千问文本生成模型（A 类）时，享受 8 折优惠，即一次原价 1 元的模型调用，实际从节省计划额度中抵扣 0.8 元。

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

\[1,000, 5,000)

8.8折

8.6折

8.4折

8.2折

8.3折

8折

7.7折

7.4折

无折扣

\[5,000, 10,000)

8.6折

8.4折

8.2折

8折

8折

7.7折

7.4折

7.1折

无折扣

\[10,000, 30,000)

8.4折

8.2折

8折

7.8折

7.7折

7.4折

7.1折

6.8折

无折扣

\[30,000, 50,000)

8.2折

8折

7.8折

7.6折

7.4折

7.1折

6.8折

6.5折

无折扣

\[50,000, 100,000)

8折

7.8折

7.6折

7.4折

7.1折

6.8折

6.5折

6.2折

无折扣

\[100,000, 300,000)

7.8折

7.6折

7.4折

7.2折

6.8折

6.5折

6.2折

5.9折

无折扣

\[300,000, 1,000,000)

7.6折

7.4折

7.2折

7折

6.5折

6.2折

5.9折

5.6折

无折扣

\[1,000,000, ~)

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

\[1,000, 5,000)

9折

8.8折

8.6折

8.4折

8.5折

8.2折

7.9折

7.6折

无折扣

\[5,000, 10,000)

8.8折

8.6折

8.4折

8.2折

8.2折

7.9折

7.6折

7.3折

无折扣

\[10,000, 30,000)

8.6折

8.4折

8.2折

8折

7.9折

7.6折

7.3折

7折

无折扣

\[30,000, 50,000)

8.4折

8.2折

8折

7.8折

7.6折

7.3折

7折

6.7折

无折扣

\[50,000, 100,000)

8.2折

8折

7.8折

7.6折

7.3折

7折

6.7折

6.4折

无折扣

\[100,000, 300,000)

8折

7.8折

7.6折

7.4折

7折

6.7折

6.4折

6.1折

无折扣

\[300,000, 1,000,000)

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

#### 节省计划续订

登录[费用与成本](https://usercenter2.aliyun.com/home)控制台，左侧菜单选择**费用** > **我的订阅**，查看并管理节省计划的订阅状态、生效时间、自动续费状态等。

#### **查询折扣**

在 AI 通用型节省计划中，不同模型、不同档位、承诺周期和付款方式享受不同的折扣。可以访问[节省计划价格折扣详情页面](https://usercenter2.aliyun.com/resource/spn/price)，按以下条件筛选查询：

-   **适用商品**：参考下表选择对应的商品名称。
    
-   **被抵扣计费项**：参考下表选择对应的计费项。
    
-   **节省计划类型**：选择 **AI 通用型节省计划/百炼AI通用型节省计划。**
    
-   **订购时长**和**支付方式**：选择对应的选项，查看按量折扣。
    

**适用商品**

**被抵扣计费项**

百炼大模型推理

**文本**：文本生成Token用量

**图片**：图片生成张数用量、多规格图片生成张数用量、图片检测张数用量

**视频**：视频生成时长用量

**语音**：语音合成字数用量、语音识别时长用量、Cosyvoice语音合成字数用量、声音复刻及声音设计模型个数用量

**向量**：多模态向量模型用量、文本向量模型用量

**批量调用**：Batch模型用量、BatchChat模型用量、BatchChat Token用量、BatchChat视频生成时长用量

**工具调用**：计次用量

以及上述各计费项对应的全局用量。

> 查询华北2（北京）地域的调用费用折扣时，选择非全局计费项；查询其他地域时，选择对应的全局计费项。

百炼大模型-垂类模型

文本生成Token用量

阿里云百炼大模型-向量排序模型

多模态向量模型用量

百炼大模型-千问语音模型

语音合成字数用量、语音识别时长用量

百炼大模型-百聆语音模型

语音合成字数用量、语音识别时长用量

百炼大模型-万相模型

图片生成张数用量、视频生成时长用量

#### 查询账单

进入[费用与成本](https://usercenter2.aliyun.com/home)控制台，左侧菜单选择，**产品名称**选择**大模型服务平台百炼**，**商品名称**选择 **AI 通用型节省计划**。页面默认展示当月明细账单。详情请参考[如何查询节省计划账单](https://help.aliyun.com/zh/user-center/how-to-check-the-savings-plan-bill)。

## **其他模型节省计划**

其他模型节省计划

与 AI 通用型节省计划相比，其他模型节省计划更适合用量较小或需求高度集中于某一特定模型的场景。

### 使用说明

**生效时间**：节省计划购买后立即生效。

**有效期说明**：有效期根据购买套餐而定。超出有效期后，节省计划中剩余的金额，将无法使用，不支持退款。

**抵扣范围**：支持抵扣模型调用费用（输入和输出 Tokens）。不支持抵扣工具调用、上下文缓存、批量推理等产生的费用。不支持抵扣模型调优、模型部署产生的费用。

**抵扣逻辑**：

-   抵扣顺序：**免费额度** **\> 资源包** **> 其他模型节省计划 > AI 通用型节省计划 > 按量付费**。
    
-   多个同类型的节省计划：优先抵扣先到期的节省计划。若到期时间相同，则优先抵扣先购买的节省计划。
    
-   超出部分处理：如果同类节省计划全部到期或额度全部抵扣完后，仍有超出部分，自动转为按量付费。
    

**查询账单**：请参见[如何查询节省计划账单](https://help.aliyun.com/zh/user-center/how-to-check-the-savings-plan-bill)。

### **支持的节省计划**

## **大语言模型**

**购买方式**

[点击购买大语言模型推理节省计划](https://common-buy.aliyun.com/?commodityCode=sfm_llminference_spn_public_cn)

**档位**

阿里云百炼提供购买的档位包括：20元、100元、1,000元、5,000元、10,000元、20,000元、50,000元、100,000元、200,000元、300,000元、500,000元。

**折扣**

上述档位均无折扣，按[模型调用价格](https://help.aliyun.com/zh/model-studio/model-pricing)进行扣费。

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
    

**说明**

不支持向量模型（embedding）和排序模型（rerank）。如需抵扣这些模型，请参考[AI 通用型节省计划](#universal-savings-plan)或[向量及排序模型节省计划](#1a5d3540e3749)。

## **万相模型**

**购买方式**

[点击购买万相模型节省计划](https://common-buy.aliyun.com/?commodityCode=sfm_VideoAndImage_spn_cn)

**购买说明**

阿里云百炼提供五个购买档位，分别为：

-   20元：无折扣
    
-   100元：无折扣
    
-   1,000元：享 9.8 折优惠
    
-   10,000元：享 9.5 折优惠
    
-   30,000元：享 9 折优惠
    

优惠示例：以 1,000元 档位为例，假设生成某个视频消费1元，实际将从节省计划中抵扣1\*0.98=0.98元。

**有效期**

-   对于20元、100元两档，有效期3个月。
    
-   对于1,000元、10,000元、30,000元三档，有效期6个月。
    

**适用模型**

**图像生成**：wan2.6-image、wan2.6-t2i、wan2.5-t2i-preview、wan2.5-i2i-preview、wan2.2-t2i-plus、wan2.2-t2i-flash、wanx2.0-t2i-turbo、wanx2.1-t2i-plus、wanx2.1-imageedit、wanx2.1-t2i-turbo、wanx-sketch-to-image-lite、wanx-v1

**视频生成**：wan2.6-t2v、wan2.6-i2v、wan2.6-r2v、wan2.5-t2v-preview、wan2.5-i2v-preview、wan2.2-t2v-plus、wan2.2-i2v-flash、wan2.2-t2v-flash、wan2.2-i2v-plus、wanx2.1-vace-plus、wanx2.1-kf2v-plus、wanx2.1-t2v-turbo、wanx2.1-t2v-plus、wanx2.1-i2v-turbo、wanx2.1-i2v-plus

请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)查看全部模型及其调用价格。

## **千问语音模型**

**购买方式**

[点击购买千问语音模型节省计划](https://common-buy.aliyun.com/?commodityCode=sfm_VoiceModel_spn_cn)

**购买说明**

阿里云百炼提供五个购买档位，分别为：

-   20元：享 9.8 折优惠
    
-   100元：享 9.6 折优惠
    
-   500元：享 9 折优惠
    
-   1,000元：享 8.5 折优惠
    
-   5,000元：享 8 折优惠
    

优惠示例：以 1,000元 档位为例，假设消费1元，实际将从节省计划中抵扣1\*0.85=0.85元。

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
        
    -   **实时长语音识别/翻译（Gummy）：**gummy-realtime-v1
        
    -   **实时短语音（一句话）识别/翻译（Gummy）：**gummy-chat-v1
        
    -   **录音文件识别（Paraformer）：**paraformer-v2、paraformer-v1、paraformer-8k-v2、paraformer-8k-v1、paraformer-mtl-v1
        
    -   **录音文件识别（Fun-ASR）：**fun-asr、fun-asr-2025-11-07、fun-asr-2025-08-25、fun-asr-mtl、fun-asr-mtl-2025-08-25
        
    -   **录音文件识别（Qwen-ASR）：**qwen3-asr-flash-filetrans、qwen3-asr-flash-filetrans-2025-11-17、qwen3-asr-flash、qwen3-asr-flash-2025-09-08
        
    -   **录音文件识别（SenseVoice）：**sensevoice-v1
        
-   **新加坡：**
    
    -   **实时语音合成（Qwen-TTS-Realtime）：**qwen3-tts-flash-realtime、qwen3-tts-flash-realtime-2025-09-18
        
    -   **语音合成（Qwen-TTS）：**qwen3-tts-flash、qwen3-tts-flash-2025-09-18
        
    -   **实时语音识别（Qwen-ASR-Realtime）：**qwen3-asr-flash-realtime、qwen3-asr-flash-realtime-2025-10-27
        
    -   **录音文件识别（Fun-ASR）：**fun-asr、fun-asr-2025-11-07、fun-asr-2025-08-25
        
    -   **录音文件识别（Qwen-ASR）：**qwen3-asr-flash-filetrans、qwen3-asr-flash-filetrans-2025-11-17、qwen3-asr-flash、qwen3-asr-flash-2025-09-08
        

请前往百炼控制台查看全部模型。

## 向量及排序模型

**购买方式**

[点击购买向量及排序模型服务节省计划](https://common-buy.aliyun.com/?commodityCode=sfm_embeddingrerank_spn_cn)

**购买说明**

阿里云百炼提供五个购买档位，分别为：

-   100元：无折扣
    
-   500元：享 9 折优惠
    
-   2,000元：享 8 折优惠
    
-   5,000元：享 7.5 折优惠
    
-   10,000元：享 7 折优惠
    

优惠示例：以 1,000元 档位为例，假设消费 1 元，实际将从节省计划中抵扣1\*0.75=0.75（元）。

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

## **资源包**

资源包

预先购买的是具体的 Token 数量，用于抵扣特定模型**超出免费额度后**产生的实时推理用量。

### 使用说明

**生效时间**：资源包购买后立即生效，无需手动“激活”或“绑定”。

**有效期说明**：有效期根据购买套餐而定。超出有效期后，资源包中剩余的Tokens，自动作废。

**抵扣逻辑**：

-   抵扣顺序：**免费额度** **\> 资源包** **> 其他模型节省计划 > AI 通用型节省计划 > 按量付费**。
    
-   多个同类型的资源包：优先抵扣先到期的资源包。若到期时间相同，则优先抵扣先购买的资源包。
    
-   超出部分处理：如果同类资源包全部到期或额度全部抵扣完后，若仍有超出部分，自动转为按量付费。
    

**余量监控与预警：**

-   **查看余量**：点击[资源包](https://billing-cost.console.aliyun.com/ri/summary?commodityCode=fr)查看剩余量情况，点击**统计**查看使用信息。具体请参见[资源包介绍与选购](https://help.aliyun.com/zh/user-center/resource-package-instance-management)。
    
-   **设置预警**：建议[设置资源包余量预警](https://help.aliyun.com/zh/user-center/configure-balance-alerts)。当资源包使用量低于预设阈值时，系统将通过短信、邮件及站内信自动触发通知。
    

**退订说明**：

-   根据[退订规则](https://help.aliyun.com/zh/user-center/cancel-subscription/)，预付费商品未发生使用的部分，可按未使用额度费用[申请退款](https://billing-cost.console.aliyun.com/refund/refund?commodityType=RESOURCE_PLANS&refundType=NOREASON_REFUND)；已使用的部分则无法退款。
    

### **大语言模型推理资源包**

**订购地址**

[大语言模型推理资源包 qwen-plus](https://common-buy.aliyun.com/?commodityCode=sfm_llminference_dp_cn#/buy)

[大语言模型推理资源包 qwen-max](https://common-buy.aliyun.com/?commodityCode=sfm_llminference2_dp_cn#/buy)

[大语言模型推理资源包 qwen-turbo](https://common-buy.aliyun.com/?commodityCode=sfm_llminference3_dp_cn#/buy)

**适用地域**

华北2（北京）

华北2（北京）

华北2（北京）

**适用模型**

qwen-plus 及 qwen-plus-latest

的实时推理服务（[非思考模式](https://help.aliyun.com/zh/model-studio/deep-thinking)）

qwen-max及qwen-max-latest

的实时推理服务（[非思考模式](https://help.aliyun.com/zh/model-studio/deep-thinking)）

qwen-turbo及qwen-turbo-latest

的实时推理服务（[非思考模式](https://help.aliyun.com/zh/model-studio/deep-thinking)）

**包含输入和输出总Tokens**

1,200万/1.1亿

1,800万/3,900万/3.9亿/11.7亿/19.5亿

3,500万/3.5亿/17.5亿/35亿

**价格（元）**

11.66/114.4

57.6/125/1250/3750/6250

11.45/114.45/572.25/1144.5

**有效期**

自购买日起生效，有效期可选 3 个月、6 个月或 1 年。

自购买之日起有效期为 1 年。

自购买之日起有效期为 1 年。

**使用限制**

-   **qwen-plus**、**qwen-plus-latest**
    
    -   仅支持抵扣单次请求输入在`0<Token≤128K`阶梯范围内的实时推理费用（[非思考模式](https://help.aliyun.com/zh/model-studio/deep-thinking)，包含输入和输出）。
        
    -   不支持抵扣的费用包括：
        
        -   单次请求输入在`Token>128K`阶梯范围产生的费用。
            
        -   [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)、[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)、[模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)、[模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)产生的费用。
            
-   **qwen-max**、**qwen-max-latest、qwen-turbo**、**qwen-turbo-latest**
    
    -   仅支持抵扣实时推理产生的费用（[非思考模式](https://help.aliyun.com/zh/model-studio/deep-thinking)，包含输入和输出），不支持抵扣[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)、[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)、[模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)、[模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)产生的费用。
        

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

**资源包容量 (生成图片张数)**

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

资源包容量耗尽后，将自动转为按量付费模式，超出部分按各模型对应的价格进行计费，详见[模型调用计费](https://help.aliyun.com/zh/model-studio/model-pricing)。

生成或编辑一张图片消耗 1 张额度。

资源包容量耗尽后，将自动转为按量付费模式，超出部分按各模型对应的价格进行计费，详见[模型调用计费](https://help.aliyun.com/zh/model-studio/model-pricing)。

## **常见问题**

#### **节省计划和资源包是否支持退订？**

-   节省计划：自 2026 年 04 月 03 日 10:00:00（UTC+8）起，符合以下条件的节省计划支持自助退订，可在[资源退订](https://billing-cost.console.aliyun.com/refund/refund)控制台中操作：
    
    -   未生效的全预付节省计划。
        
    -   已生效但未发生任何抵扣的全预付节省计划。
        
    
    若购买的节省计划已发生抵扣，暂不支持退订，详见[公告](https://www.aliyun.com/notice/118142?spm=5176.29512420.J_JASdJ65l9Zg8lf6Fc9UC_.5.290219d5iwnIxR)。
    
-   资源包：未发生使用的部分，可按未使用额度费用[申请退款](https://billing-cost.console.aliyun.com/refund/refund?commodityType=RESOURCE_PLANS&refundType=NOREASON_REFUND)；已使用的部分则无法退款。
    

#### **资源包和节省计划如果同时存在，怎么扣费？**

系统的抵扣优先级为：**免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费**。即：先用免费额度；用完后扣资源包；资源包不够或不适用时，扣节省计划；最后才使用账户余额。

#### **为什么购买了节省计划，但没有抵扣？**

常见原因如下：

1.  **模型不匹配**：购买了其他节省计划，但调用的模型不在适用范围内。例如：购买了大语言模型节省计划，却调用了万相系列模型或向量模型（embedding）、排序模型（rerank）。可以选择购买 [AI 通用型节省计划](#universal-savings-plan)以实现跨模型抵扣。
    
2.  **使用了不支持的功能**：AI 通用型节省计划和其他节省计划均不支持抵扣[模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)、[模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)费用。只有 AI 通用型节省计划支持抵扣上下文缓存、批量推理、工具调用等产生的费用，而其他节省计划不支持。
    
3.  **免费额度未用完**：系统抵扣顺序为：**免费额度 > 节省计划**。节省计划仅抵扣免费额度用尽后产生的账单。
    

#### **三方直供模型支持抵扣 AI 通用型节省计划吗？**

[C 类模型](#standard-sp-row3)中，阿里直供的模型支持抵扣，三方直供的模型不支持抵扣。可以在[百炼模型广场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)中通过模型卡片右上角标识判断。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9433444771/p1062187.png)

#### **为什么购买了资源包，但没有抵扣？**

资源包的抵扣需要满足特定条件，常见原因如下：

1.  模型不匹配：调用的模型与购买的资源包不一致。例如，购买 qwen-max 资源包却调用了 qwen-plus 模型。
    
2.  使用了不支持的功能：资源包**不支持抵扣**这些功能产生的费用：[批量推理（Batch）](https://help.aliyun.com/zh/model-studio/batch-inference)、[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)、[模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)、[模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)。
    
3.  Token 长度超限：对于 qwen-plus 资源包，单次请求输入超过 128K Token 的部分无法抵扣。
    
4.  免费额度未用完：系统抵扣顺序为：**免费额度 > 资源包**。资源包仅抵扣免费额度用尽后产生的账单。
    

#### **如果先购买了资源包但未开通阿里云百炼服务，应该如何使用？**

请先[开通阿里云百炼的模型服务](https://help.aliyun.com/zh/model-studio/get-api-key#02dae3d7d6nip)。服务开通后，优先会抵扣免费额度，待免费额度消耗完后，才会开始抵扣资源包。

#### **购买了大语言模型节省计划，能抵扣向量模型（embedding）和排序模型（rerank）吗？**

不能。大语言模型推理节省计划仅适用于文本生成模型，不支持抵扣向量模型和排序模型。如果您的业务同时涉及大语言模型与向量、排序模型（例如 RAG 场景），建议选择[AI 通用型节省计划](#universal-savings-plan)，或单独购买[向量及排序模型节省计划](#1a5d3540e3749)。
