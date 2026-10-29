# 新人免费额度

当您首次开通阿里云百炼时，平台会自动为您发放各模型的新人专属免费额度。

**说明**

-   仅华北2（北京）地域模型享有免费额度，其他地域无免费额度。
-   未认证用户免费额度用完后无法继续调用，需完成[认证](https://myaccount.console.aliyun.com/cert-info)并[充值](https://billing-cost.console.aliyun.com/fortune/fund-management/recharge)后方能继续按量付费。
-   已认证用户免费额度用完后自动转为按量付费。如需避免意外扣费，可提前开启[免费额度用完即停](https://help.aliyun.com/zh/model-studio/new-free-quota#d1cb80ac11i92)，额度耗尽时服务自动停止。

## 规则说明

### 有效期

免费额度的有效期为 90 天，从开通阿里云百炼、模型发布或模型申请通过之日起计算（以较晚者为准）。额度到期或耗尽后，继续调用模型推理服务将[产生计费](https://help.aliyun.com/zh/model-studio/billing-for-model-studio)。

**重要****2025年9月8日11点**前已开通阿里云百炼的用户，免费额度有效期可能不足90天；在此之后开通的用户有效期为90天。详情参考[阿里云百炼新人免费额度有效期调整通知](https://help.aliyun.com/zh/model-studio/new-free-quota-validity-adjustment)。

免费额度过期后自动失效，不支持补发、延期或重置：

-   额度有效期内是否使用均不会暂停计时；
-   额度过期后，剩余部分自动作废，不会重新发放或延长；
-   同一实名认证主体下重新注册账号，无法再次领取新人免费额度。

### 适用范围

免费额度仅抵扣模型**实时推理**（调用）产生的费用。

**警告**[Batch调用](raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)、[模型调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)、[模型部署](raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)、自定义模型（调优后模型、已部署模型）、PAI-DSW、OSS 存储及请求费用不支持用免费额度抵扣。

### 注意事项

阿里云主账号与其RAM子账号共享免费额度。

> 例如：qwen-max的总免费额度为100万Token。主账号消耗了10万Token，RAM子账号消耗了20万Token，qwen-max的剩余免费额度为70万Token。

不同模型（含同一模型的不同快照版本）的免费额度相互独立，不互通、不共享。

-   每个模型均有独立的免费额度（通常为 100 万 Token），不能跨模型合并或转移使用。
-   带日期后缀的快照版本（如 `qwen-max-2026-05-17`）与不带日期的最新版本（如 `qwen-max`）视为两个独立模型，各自拥有独立额度。
-   当某个模型额度用完后，系统不会自动切换到其他有额度的模型。如需使用其他模型的免费额度，需在代码或工具配置中手动修改 `model` 参数。

## 获取免费额度

访问[阿里云百炼-华北2（北京）地域](https://bailian.console.aliyun.com/model/market)，阅读并同意协议后，系统将自动开通阿里云百炼并发放**免费推理额度**。

> 如果未弹出服务协议，表示您已经开通过阿里云百炼且获得免费额度。

首次开通阿里云百炼后由系统自动发放，无需手动领取或购买任何产品。无需**实名认证**即可获取和使用免费额度。如需在免费额度用完后按量付费继续使用，则需先完成实名认证。

开通后免费额度可能存在延迟，通常两小时内生效，若刚开通未立即显示请耐心等待。有免费额度的模型在列表中以蓝色额度条标识。

ASR 类模型需在百炼控制台业务空间逐一开通权限后方可调用并消耗免费额度。

## 查看剩余额度

可通过以下三种方式查看模型的免费额度。

免费额度剩余量为输入 Token 和输出 Token 共用的总额度，不单独区分输入或输出计算。调用时产生的输入 Token 和输出 Token 会共同扣减该总额度，控制台显示的剩余量即为扣除后的总剩余 Token 数。

#### 方式一：通过免费额度页面查看

在控制台的[免费额度](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota)页面，查看所有模型的免费额度余量及过期时间。页面顶部提供**购买节省计划**按钮入口，可快捷前往节省计划购买页。下方以四张指标卡片汇总免费额度整体情况：**有额度模型总数**、**使用率超50%模型**、**使用率超80%模型**、**额度用尽或过期模型**，便于快速定位需关注的模型。可按模型类型筛选或搜索模型。

页面下方表格列出各模型的**模型 Code**、**模型类型**、**剩余额度**、**到期时间**、**状态**及**用完即停**开关。

#### 方式二：通过模型广场查看

1.  在控制台的[**模型广场**](https://bailian.console.aliyun.com/model/market)页面，找到目标模型系列并单击进入详情页。
    
2.  在**模型Code**选择模型版本，在**免费额度**区域查看余量。若无免费额度显示，可能额度已到期，具体有效期参见模型列表。
    
    **362,917/1,000,000** 表示剩余 362,917 个Token，总共 1,000,000 个Token。
    
    > 控制台显示的免费额度为分钟级更新（需手动刷新页面）。
    

#### 方式三：通过模型用量页面查看

-   在控制台的[**模型用量**](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)页面，查看各模型的免费额度使用与剩余情况。

## 使用免费额度

实时调用大模型将自动扣除免费额度，请参考[开始使用阿里云百炼](raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

### 免费额度用完即停

免费额度用完即停（部分用户称“安心模式”）。开启此功能后，免费额度耗尽时将停止响应并返回 HTTP 403 错误，错误码为 `AllocationQuota.FreeTierOnly`，不会继续扣费。

-   **未完成实名认证**：该功能默认开启，无法关闭，控制台不显示开关。
-   **已完成实名认证**：该功能默认关闭，可在控制台自行开启或关闭。

#### 如何开启

##### 方式一：在免费额度页面开启

**为单个模型开启：**

1.  在控制台的[免费额度](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota)页面。
2.  在列表中找到目标模型，在其右侧操作列开启**免费额度用完即停**开关（无免费额度的模型无法开启，开启成功后开关显示为**已开启**状态）。
3.  若目标模型的**状态**列显示为**不支持开启**，说明该模型不提供**免费额度**，无法为其开启此功能；可在页面顶部搜索框中输入模型名称，快速定位并查看目标模型的状态。

**批量开启：**

1.  在控制台的[免费额度](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota)页面。
2.  点击**批量设置**，在下拉菜单中选择**批量开启**。
3.  勾选目标模型，点击**批量开启**。如需为所有支持且未开启的模型启用，可点击**一键开启所有模型**。
4.  在确认弹窗中点击**开启免费额度用完即停**。

##### 方式二：在模型广场页面开启

以 qwen3.8-max 为例。前往[qwen3.8-max 模型详情页](https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen3.8-max?serviceSite=asia-pacific-china&ref=suggest)，开启**免费额度用完即停**开关。

若模型未显示开关，说明该模型免费额度已耗尽或过期，或模型本身不提供免费额度。

#### 如何关闭

已完成实名认证的用户，该功能默认关闭，开启后可随时关闭；未完成实名认证的用户由系统强制开启该功能，无法自行关闭。可在免费额度页面操作列关闭单个模型的**免费额度用完即停**开关，或经批量操作下拉菜单选择**批量关闭**。

百炼移动端暂不支持开启或关闭该功能，需使用电脑端访问控制台操作。

开启或关闭配置生效需要一定时间，建议等待片刻后再尝试调用。若在配置变更生效期间仍在调用，可能因生效延迟导致免费额度用完后依旧产生计费。免费额度已耗尽的模型无法开启该功能（详见本文“如何开启”说明）；此时如需停止计费，可删除 API Key（参见本文“如何避免扣费”）或购买**节省计划**。

控制台显示的**未启用**或**不支持开启**状态，是“免费额度用完即停”的保护状态提示，并非功能故障，无需额外手动启用服务。关闭该开关后状态同步存在延迟，需等待约半小时后重试方可恢复按量付费调用。生产环境不建议开启此功能，以免额度耗尽导致服务不可用。

## 已下架的免费额度

部分模型的免费额度由平台下架。下架后，新用户不再获得该模型的免费额度；已发放给老用户的额度仍可继续使用，直至到期或耗尽。

后续新模型上线时，平台依然会发放新模型的免费额度。

已下架免费额度的模型列表

#### 2026-10-29

-   wan2.7-t2v
-   wan3.0-video-prime
-   wan2.7-i2v
-   wan2.7-r2v
-   wan2.7-videoedit
-   wan2.2-dancer
-   wan2.7-t2v-2026-04-25
-   wan2.7-i2v-2026-04-25
-   wan2.7-t2v-2026-06-12
-   wan2.7-r2v-2026-06-12
-   qwen3.5-omni-plus-realtime-2026-03-15
-   qwen3.5-omni-flash-realtime
-   qwen3.5-omni-flash-2026-03-15
-   qwen3.5-omni-flash
-   qwen3.5-omni-flash-realtime-2026-03-15
-   qwen3.5-omni-plus-2026-03-15
-   happyhorse-1.0-i2v
-   happyhorse-1.0-t2v
-   happyhorse-1.0-r2v
-   happyhorse-1.5-t2v
-   happyhorse-1.5-video-edit
-   happyhorse-1.5-i2v
-   happyhorse-1.5-r2v
-   qwen3-asr-flash-realtime-2026-02-10
-   qwen3-asr-flash-2026-02-10
-   qwen3-tts-instruct-flash-realtime
-   qwen3-tts-instruct-flash-realtime-2026-01-22
-   qwen3-tts-instruct-flash
-   qwen3-tts-instruct-flash-2026-01-26
-   qwen3-tts-vc-2026-01-22
-   qwen3-tts-vd-2026-01-26
-   qwen-flash-character-2026-02-26
-   qwen3.5-livetranslate-flash-realtime
-   qwen3.5-livetranslate-flash-realtime-2026-05-19
-   tongyi-embedding-vision-flash-2026-03-06
-   tongyi-embedding-vision-plus-2026-03-06
-   fun-asr-flash-8k-realtime-2026-01-28
-   fun-asr-realtime-2026-02-28
-   fun-music-preview
-   qwen-audio-3.0-asr-flash
-   qwen-audio-3.0-asr-flash-filetrans
-   qwen-audio-3.0-asr-flash-streaming
-   qwen-audio-3.0-realtime-flash
-   qwen-audio-3.0-realtime-plus
-   qwen-audio-3.0-tts-flash
-   qwen-audio-3.0-tts-plus
-   aitryon
-   aitryon-parsing-v1
-   aitryon-plus
-   aitryon-refiner
-   animate-anyone-detect-gen2
-   animate-anyone-gen2
-   animate-anyone-template-gen2
-   avatar-dialog
-   cosyvoice-clone-v1
-   cosyvoice-v1
-   cosyvoice-v2
-   cosyvoice-v3
-   cosyvoice-v3-flash
-   cosyvoice-v3-plus
-   deepseek-r1
-   deepseek-r1-0528
-   deepseek-r1-distill-qwen-14b
-   deepseek-r1-distill-qwen-32b
-   deepseek-r1-distill-qwen-7b
-   deepseek-v3
-   deepseek-v3.1
-   deepseek-v3.2
-   deepseek-v3.2-exp
-   deepseek-v4-flash
-   emo-detect-v1
-   emo-v1
-   emoji-detect-v1
-   emoji-v1
-   facechain-generation
-   fun-asr-2025-08-25
-   fun-asr-2025-11-07
-   fun-asr-mtl
-   fun-asr-mtl-2025-08-25
-   fun-asr-mtl-realtime
-   fun-asr-mtl-realtime-2025-12-10
-   fun-asr-realtime-2025-09-15
-   fun-asr-realtime-2025-11-07
-   glm-4.5
-   glm-4.5-air
-   glm-4.6
-   glm-4.7
-   glm-5
-   glm-5.1
-   glm-5.2
-   gte-rerank-v2
-   gui-plus-2026-02-26
-   gummy-chat-v1
-   gummy-realtime-v1
-   image-out-painting
-   kimi-k2-thinking
-   kimi-k2.5
-   kimi-k2.6
-   liveportrait
-   liveportrait-detect
-   MiniMax-M2.1
-   Moonshot-Kimi-K2-Instruct
-   multimodal-embedding-v1
-   opennlu-v1
-   paraformer-8k-lite-v1
-   paraformer-8k-v1
-   paraformer-mtl-v1
-   paraformer-realtime-8k-v1
-   paraformer-realtime-v1
-   paraformer-v1
-   qvq-72b-preview
-   qvq-max
-   qvq-max-2025-03-25
-   qvq-max-2025-05-15
-   qvq-max-latest
-   qvq-plus
-   qvq-plus-2025-05-15
-   qvq-plus-latest
-   qwen-coder-plus
-   qwen-coder-plus-1106
-   qwen-coder-plus-latest
-   qwen-coder-turbo
-   qwen-coder-turbo-0919
-   qwen-coder-turbo-latest
-   qwen-flash
-   qwen-flash-2025-07-28
-   qwen-image
-   qwen-image-2.0
-   qwen-image-2.0-2026-03-03
-   qwen-image-2.0-pro
-   qwen-image-2.0-pro-2026-03-03
-   qwen-image-2.0-pro-2026-04-22
-   qwen-image-2.0-pro-2026-06-22
-   qwen-image-edit-max-2026-01-16
-   qwen-image-edit-plus-2025-10-30
-   qwen-image-edit-plus-2025-12-01
-   qwen-image-edit-plus-2025-12-15
-   qwen-image-max-2025-12-30
-   qwen-image-plus-2026-01-09
-   qwen-long
-   qwen-long-2025-01-25
-   qwen-long-latest
-   qwen-math-plus
-   qwen-math-plus-0816
-   qwen-math-plus-0919
-   qwen-math-plus-latest
-   qwen-math-turbo
-   qwen-math-turbo-0919
-   qwen-math-turbo-latest
-   qwen-max
-   qwen-max-0403
-   qwen-max-0428
-   qwen-max-0919
-   qwen-max-1201
-   qwen-max-2025-01-25
-   qwen-max-latest
-   qwen-mt-turbo
-   qwen-omni-turbo
-   qwen-omni-turbo-2025-01-19
-   qwen-omni-turbo-2025-03-26
-   qwen-omni-turbo-latest
-   qwen-omni-turbo-realtime
-   qwen-omni-turbo-realtime-2025-05-08
-   qwen-omni-turbo-realtime-latest
-   qwen-plus
-   qwen-plus-0112
-   qwen-plus-0723
-   qwen-plus-0806
-   qwen-plus-0919
-   qwen-plus-1125
-   qwen-plus-1127
-   qwen-plus-1220
-   qwen-plus-2025-01-25
-   qwen-plus-2025-04-28
-   qwen-plus-2025-07-14
-   qwen-plus-2025-07-28
-   qwen-plus-2025-09-11
-   qwen-plus-2025-12-01
-   qwen-plus-latest
-   qwen-tts
-   qwen-tts-2025-04-10
-   qwen-tts-2025-05-22
-   qwen-tts-latest
-   qwen-tts-realtime
-   qwen-tts-realtime-2025-07-15
-   qwen-tts-realtime-latest
-   qwen-tts-vc-realtime-2025-08-20
-   qwen-turbo
-   qwen-turbo-0624
-   qwen-turbo-0919
-   qwen-turbo-1101
-   qwen-turbo-2025-02-11
-   qwen-turbo-2025-04-28
-   qwen-turbo-2025-07-15
-   qwen-turbo-latest
-   qwen-vl-max
-   qwen-vl-max-0809
-   qwen-vl-max-1030
-   qwen-vl-max-1119
-   qwen-vl-max-1230
-   qwen-vl-max-2025-01-25
-   qwen-vl-max-2025-04-02
-   qwen-vl-max-2025-04-08
-   qwen-vl-max-2025-08-13
-   qwen-vl-max-latest
-   qwen-vl-ocr-1028
-   qwen-vl-ocr-2025-04-13
-   qwen-vl-ocr-2025-08-28
-   qwen-vl-ocr-2025-11-20
-   qwen-vl-ocr-latest
-   qwen-vl-plus
-   qwen-vl-plus-0102
-   qwen-vl-plus-0809
-   qwen-vl-plus-2025-01-25
-   qwen-vl-plus-2025-05-07
-   qwen-vl-plus-2025-08-15
-   qwen-vl-plus-latest
-   qwen-voice-design
-   qwen1.5-110b-chat
-   qwen1.5-14b-chat
-   qwen1.5-32b-chat
-   qwen1.5-72b-chat
-   qwen1.5-7b-chat
-   qwen2-57b-a14b-instruct
-   qwen2-72b-instruct
-   qwen2-7b-instruct
-   qwen2-vl-72b-instruct
-   qwen2.5-14b-instruct
-   qwen2.5-14b-instruct-1m
-   qwen2.5-32b-instruct
-   qwen2.5-3b-instruct
-   qwen2.5-72b-instruct
-   qwen2.5-7b-instruct
-   qwen2.5-7b-instruct-1m
-   qwen2.5-coder-14b-instruct
-   qwen2.5-coder-32b-instruct
-   qwen2.5-coder-7b-instruct
-   qwen2.5-math-72b-instruct
-   qwen2.5-math-7b-instruct
-   qwen2.5-omni-7b
-   qwen2.5-vl-32b-instruct
-   qwen2.5-vl-3b-instruct
-   qwen2.5-vl-72b-instruct
-   qwen2.5-vl-7b-instruct
-   qwen2.5-vl-embedding
-   qwen3-0.6b
-   qwen3-1.7b
-   qwen3-14b
-   qwen3-235b-a22b
-   qwen3-235b-a22b-instruct-2507
-   qwen3-235b-a22b-thinking-2507
-   qwen3-30b-a3b
-   qwen3-30b-a3b-instruct-2507
-   qwen3-30b-a3b-thinking-2507
-   qwen3-32b
-   qwen3-4b
-   qwen3-8b
-   qwen3-asr-flash-2025-09-08
-   qwen3-asr-flash-filetrans-2025-11-17
-   qwen3-asr-flash-realtime-2025-10-27
-   qwen3-coder-30b-a3b-instruct
-   qwen3-coder-480b-a35b-instruct
-   qwen3-coder-flash
-   qwen3-coder-flash-2025-07-28
-   qwen3-coder-next
-   qwen3-coder-plus
-   qwen3-coder-plus-2025-07-22
-   qwen3-coder-plus-2025-09-23
-   qwen3-livetranslate-flash-2025-12-01
-   qwen3-livetranslate-flash-realtime
-   qwen3-livetranslate-flash-realtime-2025-09-22
-   qwen3-max
-   qwen3-max-2025-09-23
-   qwen3-max-2025-10-30
-   qwen3-max-2026-01-23
-   qwen3-max-preview
-   qwen3-next-80b-a3b-instruct
-   qwen3-next-80b-a3b-thinking
-   qwen3-omni-30b-a3b-captioner
-   qwen3-omni-flash
-   qwen3-omni-flash-2025-09-15
-   qwen3-omni-flash-2025-12-01
-   qwen3-omni-flash-realtime
-   qwen3-omni-flash-realtime-2025-09-15
-   qwen3-omni-flash-realtime-2025-12-01
-   qwen3-tts-flash-2025-09-18
-   qwen3-tts-flash-2025-11-27
-   qwen3-tts-flash-realtime-2025-09-18
-   qwen3-tts-flash-realtime-2025-11-27
-   qwen3-tts-vc-realtime-2025-11-27
-   qwen3-tts-vc-realtime-2026-01-15
-   qwen3-tts-vd-realtime-2025-12-16
-   qwen3-tts-vd-realtime-2026-01-15
-   qwen3-vl-235b-a22b-instruct
-   qwen3-vl-235b-a22b-thinking
-   qwen3-vl-30b-a3b-instruct
-   qwen3-vl-30b-a3b-thinking
-   qwen3-vl-32b-instruct
-   qwen3-vl-32b-thinking
-   qwen3-vl-8b-instruct
-   qwen3-vl-8b-thinking
-   qwen3-vl-flash
-   qwen3-vl-flash-2025-10-15
-   qwen3-vl-flash-2026-01-22
-   qwen3-vl-plus-2025-09-23
-   qwen3-vl-plus-2025-12-19
-   qwen3.5-122b-a10b
-   qwen3.5-27b
-   qwen3.5-35b-a3b
-   qwen3.5-397b-a17b
-   qwen3.5-flash
-   qwen3.5-flash-2026-02-23
-   qwen3.5-plus
-   qwen3.5-plus-2026-02-15
-   qwen3.5-plus-2026-04-20
-   qwen3.6-27b
-   qwen3.6-35b-a3b
-   qwen3.6-flash
-   qwen3.6-flash-2026-04-16
-   qwen3.6-max-preview
-   qwen3.6-plus
-   qwen3.6-plus-2026-04-02
-   qwen3.7-flash-2026-07-15
-   qwen3.7-max-2026-05-17
-   qwen3.7-max-2026-05-20
-   qwen3.7-max-2026-06-08
-   qwen3.7-max-preview
-   qwen3.7-plus-2026-05-26
-   qwq-32b
-   qwq-32b-preview
-   qwq-plus
-   qwq-plus-2025-03-05
-   qwq-plus-latest
-   sensevoice-v1
-   text-embedding-async-v1
-   text-embedding-v1
-   text-embedding-v2
-   text-embedding-v3
-   wan2.2-animate-mix
-   wan2.2-animate-move
-   wan2.2-i2v-flash
-   wan2.2-i2v-plus
-   wan2.2-kf2v-flash
-   wan2.2-s2v
-   wan2.2-s2v-detect
-   wan2.2-t2i-flash
-   wan2.2-t2i-plus
-   wan2.2-t2v-flash
-   wan2.2-t2v-plus
-   wan2.5-i2i-preview
-   wan2.5-i2v-preview
-   wan2.5-t2i-preview
-   wan2.5-t2v-preview
-   wan2.6-i2v
-   wan2.6-i2v-flash
-   wan2.6-image
-   wan2.6-r2v
-   wan2.6-r2v-flash
-   wan2.6-t2i
-   wan2.6-t2v
-   wanx-background-generation-v2
-   wanx-v1
-   wanx2.0-t2i-turbo
-   wanx2.1-i2v-plus
-   wanx2.1-i2v-turbo
-   wanx2.1-imageedit
-   wanx2.1-kf2v-plus
-   wanx2.1-t2i-plus
-   wanx2.1-t2i-turbo
-   wanx2.1-t2v-plus
-   wanx2.1-t2v-turbo
-   wanx2.1-vace-plus
-   wordart-semantic
-   wordart-texture
-   qwen-image-edit
-   qwen-image-edit-max
-   qwen-image-edit-plus
-   qwen-image-max
-   qwen-image-plus

## 常见问题

### 免费额度即将用完或已用完，是否有通知？

有通知。余量降至 20% 或完全耗尽时，系统通过短信、站内信、邮件发送通知。

如需开启或关闭预警、修改预警比例，请前往[我的试用](https://billing-cost.console.aliyun.com/home/myfreetier)进行设置。找到试用规格描述为**百炼大模型推理免费试用**，单击**查看试用详情**，再配置余量到期预警规则即可修改。

### 免费额度耗尽是否表示我没有购买过该模型？

不是。免费额度是您首次开通阿里云百炼时由系统自动发放的新人专属福利，无需手动领取，也无需购买任何产品，与是否购买过该模型无关。每个模型（含同一模型的不同快照版本）拥有各自独立的免费额度，因此某个模型的额度耗尽仅表示该模型的赠送 Token 已用完，并不代表您没有该模型的调用权限。

额度耗尽后能否继续调用，取决于您的账号认证状态以及是否开启了**免费额度用完即停**，详情请参见本文“免费额度用完会有什么影响？”。

### 免费额度用完会有什么影响？

**对于全新未认证用户：**免费额度用完后无法继续调用。需要[完成认证](https://myaccount.console.aliyun.com/cert-info)并[充值](https://billing-cost.console.aliyun.com/fortune/fund-management/recharge)后方可继续按量付费。

**对于已认证用户：**

-   若已开启[免费额度用完即停](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota)，免费额度用完后无法继续调用，需要关闭[免费额度用完即停](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota)方可继续按量付费。
-   若未开启[免费额度用完即停](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota)，正在进行的调用不会中断，超出额度的Token将按控制台中的输入/输出价格计费，费用以按量后付费方式从阿里云账户扣除，可能导致账户欠费。

欠费限制按商品 Code 隔离。某个商品 Code 产生欠费时，该商品 Code 对应的服务不可用，即使模型仍有免费额度也无法调用，结清欠费后恢复；其他商品 Code 对应的服务不受影响。您可以在账单中[查询商品 Code](https://help.aliyun.com/zh/model-studio/bill-query-and-cost-management#query-overdue-commodity-code)。

调用前建议查询该模型剩余额度，并配置[预算管理](https://help.aliyun.com/zh/user-center/how-to-manage-a-budget)或[账号余额预警](https://help.aliyun.com/zh/user-center/monitor-account-balances)，确保账户有充足[余额](https://billing-cost.console.aliyun.com/home)，未使用的余额支持[余额提现](https://help.aliyun.com/zh/user-center/balance-withdrawal)。

### 免费额度用完后如何充值？

阿里云支持支付宝、银联在线支付、网银等多种充值方式，具体可用方式以账号[充值界面](https://billing-cost.console.aliyun.com/fortune/fund-management/recharge)展示为准。更多信息请参考[充值方式介绍](https://help.aliyun.com/zh/user-center/use-alipay-online-banking-to-recharge-online#8e4f4cdcf42rl)。

充值完成后，账户余额可能有几分钟的更新延迟，请稍后前往[费用与成本](https://billing-cost.console.aliyun.com/home)查看可用余额。余额到账且无欠费时即可正常调用模型。

### 如何查看免费额度消耗记录或账单？

调用结束**几分钟**后即可生成消耗记录。查询步骤：

1.  在[账单详情](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail)页面，选择账单月份，**产品名称**选择**大模型服务平台百炼**，单击**搜索**。
2.  单击账单列表右上角的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1247144771/p1062109.png)图标，找到**用量信息**，勾选**用量**，单击**确定**。
3.  找到**费用类型**为**免费额度**的账单项，**用量**即为免费额度已抵扣的用量。

### 为什么产生了费用？

常见原因：

-   使用的模型已经没有免费额度。
-   免费额度不支持抵扣[OpenAI兼容-Batch（文件输入）](raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)产生的费用。
-   控制台的免费额度数据为分钟级更新且需手动刷新。若未及时刷新，页面显示仍有额度但实际已耗尽，导致产生调用费用。操作前刷新页面，以最新显示为准。
-   IDE 插件自动补全导致 Token 快速消耗。使用 Cline、CodeBuddy 等 IDE 插件调用模型时，插件会自动携带完整的代码上下文和对话历史，单次对话可能消耗数千 Token，远高于普通简短对话的消耗。

可通过[如何查看产生费用的模型？](https://help.aliyun.com/zh/model-studio/new-free-quota#3bfa8283d0tc2)和[如何查看模型调用记录？](https://help.aliyun.com/zh/model-studio/new-free-quota#ab6ba5c538rn3)确认费用详情。

大模型按实际消耗 Token 计费，无论输出是否存在幻觉或事实错误，只要发起调用即消耗额度，不支持因输出质量问题恢复已用额度或退款。免费试用结束或额度用完后产生的按量计费属于正常使用，已产生费用无法回退。建议开启**免费额度用完即停**功能防止意外扣费。

### 如何查看产生费用的模型？

调用结束**几分钟后**，在[账单详情](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail)页面，选择账单月份，**商品名称**选择**阿里云百炼大模型推理**，单击**搜索**。在资产/资源实例ID （出账粒度）列查看产生费用的模型。

### 如何查看模型调用记录？

模型调用发生后**分钟级**即可在监控图表查看。登录模型监控页面（[北京](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)或[新加坡](https://bailian.console.aliyun.com/ap-southeast-1/model/telemetry)），在左侧导航栏选择**运维管理** > **模型监控**进入监控概览页，设置查询条件（例如，选择时间范围、业务空间等），再在**模型列表**区域找到目标模型并单击**查看详情**，即可查看该模型的调用统计结果。具体请参见[监控告警](raw/model-user-guide/model-monitoring/model-telemetry.md)文档。

> 监控数据按分钟级更新，仅供参考，不作为计费依据。

### 如何避免扣费？

超出免费额度后会自动从账号余额扣费。可通过以下方式降低扣费风险：

-   删除已创建的 API-Key：进入阿里云百炼的[API-Key（北京）](https://bailian.console.aliyun.com/settings/api-key)或[API-Key（新加坡）](https://bailian.console.aliyun.com/settings/api-key)页面，删除已创建的 API-Key。删除后将无法通过API调用模型，不再产生调用费用。
    
-   设置[高额消费预警](https://billing-cost.console.aliyun.com/home/alarm-threshold)：当产品日账单超过预警阈值时，每天短信提醒一次（统计截止昨日24点）。
    
    在**预警产品**下拉框中选择具体产品（如**百炼大模型部署**、**百炼大模型推理**、**百炼大模型训练**），在**预警阈值**输入框中填写金额（如`0.01`），然后单击**增加**即可添加预警规则。
    

### 还有剩余额度，为何调用失败？

请检查[阿里云账户](https://billing-cost.console.aliyun.com/home?spm=a2c4g.11186623.nav-v2-dropdown-my-aliyun.9.f6683048dWvpGu)是否欠费。欠费限制按商品 Code 隔离，某个商品 Code 产生欠费时，该商品 Code 对应的服务不可用，即使模型仍有免费额度也无法调用，结清欠费后恢复。您可以在账单中[查询商品 Code](https://help.aliyun.com/zh/model-studio/bill-query-and-cost-management#query-overdue-commodity-code)。

### 为什么看不到免费额度与有效期？

免费额度列显示**无免费额度**或**免费额度**区域不显示，可能由以下原因之一导致：

-   **免费额度已到期或耗尽**：免费额度的有效期为 90 天，从开通阿里云百炼、模型发布或模型申请通过之日起计算（以较晚者为准），到期或耗尽后将不再显示，继续调用模型将产生计费。
-   **该模型所在地域或服务部署范围不享有免费额度**：仅华北2（北京）地域的模型享有免费额度，其他地域和部署范围无免费额度。
-   **该模型本身不提供免费额度**：部分模型不参与新人免费额度发放。判断某模型是否享有免费额度，可在控制台**模型广场**进入该模型详情页，查看免费额度区域是否有余量显示（参见本文“查看剩余额度 > 方式二：通过模型广场查看”），详情页未显示免费额度的模型即表示不享有免费额度。

### 使用哪种 API Key 才能消耗免费额度？

API Key 本身不绑定特定模型，同一个 API Key 可调用所有模型，无需为使用免费额度单独创建新的 API Key。

实时调用时，系统将自动优先使用免费额度抵扣，无需手动设置。按消耗优先级依次为：免费额度 > 资源包 > 节省计划 > 按量付费。

**Token Plan/Coding Plan 专属 API Key** 不消耗免费额度，使用专属 API Key 调用模型将直接按量付费。如需使用免费额度，请改用通用 API Key（非专属 API Key）。

### OAuth 认证的免费额度为什么在控制台不显示？

OAuth 认证提供独立的免费额度（每天 2000 次调用），与百炼控制台的 API Key 免费额度体系相互独立。

控制台的免费额度页面仅显示 API Key 的 Token 额度，不显示 OAuth 认证的调用记录与免费额度消耗，页面无相关记录并不表示 OAuth 认证的免费额度失效。

如需查看 OAuth 认证的调用记录，登录百炼控制台，在左侧导航栏选择**运维管理** > **模型监控**查看。

### 使用 Token Plan 专属 API Key 调用图像/视频生成模型报 400 错误？

图像/视频生成模型（如 wanx 系列、qwen-vl-max-latest 等多模态生成模型）不支持通过文本生成类 Base URL 直接调用。若使用 Token Plan 团队版专属 API Key 经文本 Base URL（`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）直接请求此类模型，将返回 HTTP 400 错误。

解决方法：请通过百炼应用中的 Skill（技能）或扩展机制接入多模态生成模型，而非直接以文本对话方式调用。

### 新人免费额度与节省计划是什么关系？

新人免费额度与**节省计划**相互独立，购买节省计划不会额外赠送免费额度。每个模型均有独立的免费额度（通常为 100 万 Token），不能跨模型合并或转移使用。

### 调用大模型响应慢/有延迟正常吗？

正常。响应延迟受网络状况及模型推理耗时影响，与是否使用免费额度无关。
