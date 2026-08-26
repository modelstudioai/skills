# 新人免费额度

当您首次开通阿里云百炼时，平台会自动为您发放各模型的新人专属免费额度。

**说明**仅华北2（北京）地域模型享有免费额度，其他地域无免费额度。

## 规则说明

### 有效期

免费额度的有效期为 90 天，从开通阿里云百炼、模型发布或模型申请通过之日起计算（以较晚者为准）。额度到期或耗尽后，继续调用模型推理服务将[产生计费](https://help.aliyun.com/zh/model-studio/billing-for-model-studio)。

**重要****2025年9月8日11点**前已开通阿里云百炼的用户，免费额度有效期可能不足90天；在此之后开通的用户有效期为90天。详情参考[阿里云百炼新人免费额度有效期调整通知](https://help.aliyun.com/zh/model-studio/new-free-quota-validity-adjustment)。

免费额度过期后自动失效，不支持补发、延期或重置：

-   额度有效期内是否使用均不会暂停计时；
-   额度过期后，剩余部分自动作废，不会重新发放或延长；
-   同一实名认证主体下重新注册账号，无法再次领取新人免费额度。

### 适用范围

免费额度仅抵扣模型**实时推理**（调用）产生的费用，不支持抵扣以下场景：

-   [Batch调用](raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
-   [模型调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
-   [模型部署](raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
-   自定义模型（调优后模型、已部署模型）
-   PAI-DSW
-   OSS 存储及请求费用

### 注意事项

阿里云主账号与其RAM子账号共享免费额度。

> 例如：qwen-max的总免费额度为100万Token。主账号消耗了10万Token，RAM子账号消耗了20万Token，qwen-max的剩余免费额度为70万Token。

不同模型（含同一模型的不同快照版本）的免费额度相互独立，不互通、不共享。

-   每个模型均有独立的免费额度（通常为 100 万 Token），不能跨模型合并或转移使用。
-   带日期后缀的快照版本（如 `qwen-max-2026-05-17`）与不带日期的最新版本（如 `qwen-max`）视为两个独立模型，各自拥有独立额度。
-   当某个模型额度用完后，系统不会自动切换到其他有额度的模型。如需使用其他模型的免费额度，需在代码或工具配置中手动修改 `model` 参数。

## 获取免费额度

访问[阿里云百炼-华北2（北京）地域](https://bailian.console.aliyun.com/#/model-market)，阅读并同意协议后，系统将自动开通阿里云百炼并发放**免费推理额度**。

> 如果未弹出服务协议，表示您已经开通过阿里云百炼且获得免费额度。

首次开通阿里云百炼后由系统自动发放，无需手动领取或购买任何产品。无需**实名认证**即可获取和使用免费额度。如需在免费额度用完后按量付费继续使用，则需先完成实名认证。

开通后免费额度可能存在延迟，通常两小时内生效，若刚开通未立即显示请耐心等待。有免费额度的模型在列表中以蓝色额度条标识。

ASR 类模型需在百炼控制台业务空间逐一开通权限后方可调用并消耗免费额度。

## 查看剩余额度

可通过以下三种方式查看模型的免费额度。

免费额度剩余量为输入 Token 和输出 Token 共用的总额度，不单独区分输入或输出计算。调用时产生的输入 Token 和输出 Token 会共同扣减该总额度，控制台显示的剩余量即为扣除后的总剩余 Token 数。

#### 方式一：通过免费额度页面查看

在控制台的[免费额度](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota)页面，查看所有模型的免费额度余量及过期时间。可按模型类型筛选或搜索模型。

#### 方式二：通过模型广场查看

1.  在控制台的[**模型广场**](https://bailian.console.aliyun.com/?tab=model#/model-market/all)页面，找到目标模型系列并单击进入详情页。
    
    ![11](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9935068571/p1010357.webp)
    
2.  在**模型Code**选择模型版本，在**免费额度**区域查看余量。若无免费额度显示，可能额度已到期，具体有效期参见模型列表。
    
    **362,917/1,000,000** 表示剩余 362,917 个Token，总共 1,000,000 个Token。
    
    > 控制台显示的免费额度为分钟级更新（需手动刷新页面）。
    
    ![12](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9935068571/p1010358.webp)
    

#### 方式三：通过模型用量页面查看

-   在控制台的[**模型用量**](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/usage-statistics)页面，查看各模型的免费额度使用与剩余情况。

## 使用免费额度

实时调用大模型将自动扣除免费额度，请参考[开始使用阿里云百炼](https://help.aliyun.com/zh/model-studio/what-is-model-studio#1b7e9bceeb486)。

**重要**默认情况下，全新未认证用户免费额度耗尽后无法继续使用，需要[认证](https://myaccount.console.aliyun.com/cert-info)并[充值](https://billing-cost.console.aliyun.com/fortune/fund-management/recharge)后方能继续按量付费。已认证用户免费额度耗尽后继续调用会直接扣费，可提前开启**免费额度用完即停**功能，防止产生意外费用。

全新未认证用户免费额度耗尽后，将停止响应并返回 HTTP 403 错误，错误码为 `AllocationQuota.FreeTierOnly`，需要[认证](https://myaccount.console.aliyun.com/cert-info)并充值后方能继续按量付费。

### 免费额度用完即停

免费额度用完即停（部分用户称“安心模式”）。开启此功能后，免费额度耗尽时将停止响应并返回 HTTP 403 错误，错误码为 `AllocationQuota.FreeTierOnly`，不会继续扣费。

未完成实名认证的用户，系统默认强制开启用完即停模式，开关不可见且无法操作。完成实名认证后，可在控制台查看并自行切换该开关。

#### 如何开启

##### 方式一：在免费额度页面开启

**为单个模型开启：**

1.  在控制台的[免费额度](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota)页面。
2.  在列表中找到目标模型，在其右侧操作列开启**免费额度用完即停**开关（无免费额度的模型无法开启，开启成功后开关显示为**已开启**状态）。
3.  若目标模型的**状态**列显示为**不支持开启**，说明该模型不提供**免费额度**，无法为其开启此功能；可在页面顶部搜索框中输入模型名称，快速定位并查看目标模型的状态。

**批量开启：**

1.  在控制台的[免费额度](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota)页面。
2.  点击**批量操作免费额度用完即停**，在下拉菜单中选择**批量开启**。
3.  勾选目标模型，点击**批量开启**。如需为所有支持且未开启的模型启用，可点击**一键开启所有模型**。
4.  在确认弹窗中点击**开启免费额度用完即停**。

##### 方式二：在模型广场页面开启

以 Qwen3-Coder-Plus 为例。前往[Qwen3-Coder-Plus 模型详情页](https://bailian.console.aliyun.com/?tab=model#/model-market/detail/group-qwen3-coder-plus?modelGroup=group-qwen3-coder-plus)，开启**免费额度用完即停**开关。

若模型未显示开关，说明该模型免费额度已耗尽或过期，或模型本身不提供免费额度。

#### 如何关闭

已完成实名认证的用户，该功能默认关闭，开启后可随时关闭；未完成实名认证的用户由系统强制开启该功能，无法自行关闭。可在免费额度页面操作列关闭单个模型的**免费额度用完即停**开关，或经批量操作下拉菜单选择**批量关闭**。

百炼移动端暂不支持开启或关闭该功能，需使用电脑端访问控制台操作。

开启或关闭配置生效需要一定时间，建议等待片刻后再尝试调用。若在配置变更生效期间仍在调用，可能因生效延迟导致免费额度用完后依旧产生计费。免费额度已耗尽的模型无法开启该功能（详见本文“如何开启”说明）；此时如需停止计费，可删除 API Key（参见本文“如何避免扣费”）或购买**节省计划**。

控制台显示的**未启用**或**不支持开启**状态，是“免费额度用完即停”的保护状态提示，并非功能故障，无需额外手动启用服务。关闭该开关后状态同步存在延迟，需等待约半小时后重试方可恢复按量付费调用。生产环境不建议开启此功能，以免额度耗尽导致服务不可用。

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

-   若已开启[免费额度用完即停](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota)，免费额度用完后无法继续调用，需要关闭[免费额度用完即停](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota)方可继续按量付费。
-   若未开启[免费额度用完即停](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/free-quota)，正在进行的调用不会中断，超出额度的Token将按控制台中的输入/输出价格计费，费用以按量后付费方式从阿里云账户扣除，可能导致账户欠费。

账户欠费时，即使其他模型仍有免费额度也无法调用。

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

模型调用完**一小时后**，在模型监控（[北京](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)或[新加坡](https://modelstudio.console.aliyun.com/?tab=model#/model-telemetry)）页面设置查询条件（例如，选择时间范围、业务空间等），再在**模型列表**区域找到目标模型并单击**操作**列的**监控**，即可查看该模型的调用统计结果。具体请参见[模型监控](raw/model-user-guide/model-monitoring/model-telemetry.md)文档。

> 数据按小时更新，高峰期可能有小时级延迟，请您耐心等待。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6923304571/p992753.png)

### 如何避免扣费？

超出免费额度后会自动从账号余额扣费。可通过以下方式降低扣费风险：

-   删除已创建的 API-Key：进入阿里云百炼的[API-Key（北京）](https://bailian.console.aliyun.com/?apiKey=1&tab=globalset#/efm/api_key)或[API-Key（新加坡）](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/api_key)页面，删除已创建的 API-Key。删除后将无法通过API调用模型，不再产生调用费用。
    
-   设置[高额消费预警](https://billing-cost.console.aliyun.com/home/alarm-threshold)：当产品日账单超过预警阈值时，每天短信提醒一次（统计截止昨日24点）。
    
    在**预警产品**下拉框中选择具体产品（如**百炼大模型部署**、**百炼大模型推理**、**百炼大模型训练**），在**预警阈值**输入框中填写金额（如`0.01`），然后单击**增加**即可添加预警规则。
    

### 还有剩余额度，为何调用失败？

请检查[阿里云账户](https://billing-cost.console.aliyun.com/home?spm=a2c4g.11186623.nav-v2-dropdown-my-aliyun.9.f6683048dWvpGu)是否欠费。账户欠费时，即使模型仍有免费额度也无法调用。

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

如需查看 OAuth 认证的调用记录，登录百炼控制台，在左侧导航栏选择**模型** > **工作台** > **模型监控**查看。

### 使用 Token Plan 专属 API Key 调用图像/视频生成模型报 400 错误？

图像/视频生成模型（如 wanx 系列、qwen-vl-max-latest 等多模态生成模型）不支持通过文本生成类 Base URL 直接调用。若使用 Token Plan 团队版专属 API Key 经文本 Base URL（`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）直接请求此类模型，将返回 HTTP 400 错误。

解决方法：请通过百炼应用中的 Skill（技能）或扩展机制接入多模态生成模型，而非直接以文本对话方式调用。

### 新人免费额度与节省计划是什么关系？

新人免费额度与**节省计划**相互独立，购买节省计划不会额外赠送免费额度。每个模型均有独立的免费额度（通常为 100 万 Token），不能跨模型合并或转移使用。

### 调用大模型响应慢/有延迟正常吗？

正常。响应延迟受网络状况及模型推理耗时影响，与是否使用免费额度无关。
