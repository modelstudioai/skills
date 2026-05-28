# 新人免费额度

当您首次开通阿里云百炼时，平台会自动为您发放各模型的新人专属免费额度。

**说明**

仅**中国内地版**模型享有免费额度，其他地域无免费额度。

## 规则说明

### 有效期

免费额度的有效期为 30～90 天，从开通阿里云百炼或模型申请通过之日起计算。额度到期或耗尽后，继续调用模型推理服务将[产生计费](https://help.aliyun.com/zh/model-studio/billing-for-model-studio)。

**重要**

自**2025年9月8日11点**起，首次开通阿里云百炼的用户，获赠的新人免费额度有效期调整为 90 天，在此之前已开通的用户不受影响，详情参考[阿里云百炼新人免费额度有效期调整通知](https://help.aliyun.com/zh/model-studio/new-free-quota-validity-adjustment)。

### 适用范围

免费额度仅抵扣模型**实时推理**（调用）产生的费用，不支持抵扣以下场景：

-   [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)
    
-   [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)
    
-   [模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)
    
-   [模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)
    
-   自定义模型（调优后模型、已部署模型）
    

### 注意事项

阿里云主账号与其RAM子账号共享免费额度。

> 例如：qwen-max的总免费额度为100万Token。主账号消耗了10万Token，RAM子账号消耗了20万Token，qwen-max的剩余免费额度为70万Token。

## 获取免费额度

访问[阿里云百炼-中国内地版](https://bailian.console.aliyun.com/#/model-market)，阅读并同意协议后，系统将自动开通阿里云百炼并发放**免费推理额度**。

> 如果未弹出服务协议，表示您已经开通过阿里云百炼且获得免费额度。

## 查看剩余额度

可通过以下两种方式查看模型的免费额度。

#### 方式一：通过模型用量查看

在控制台的[模型用量](https://bailian.console.aliyun.com/?tab=model#/model-usage/free-quota)页面，点击**免费额度**页签，查看所有模型的免费额度余量及过期时间。

#### 方式二：通过模型广场查看

1.  在控制台的\*\*[模型广场](https://bailian.console.aliyun.com/?tab=model#/model-market/all)\*\*页面，找到目标模型系列并单击进入详情页。
    
    ![11](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9935068571/p1010357.webp)
    
2.  在**模型Code**选择模型版本，在**免费额度**区域查看余量。若无免费额度显示，可能额度已到期，具体有效期参见模型列表。
    
    如下图所示，**362,917/1,000,000** 表示剩余 362,917 个Token，总共 1,000,000 个Token。
    
    > 控制台显示的免费额度为分钟级更新（需手动刷新页面）。
    
    ![12](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9935068571/p1010358.webp)
    

## 使用免费额度

实时调用大模型将自动扣除免费额度，请参考[开始使用阿里云百炼](https://help.aliyun.com/zh/model-studio/what-is-model-studio#1b7e9bceeb486)。

**重要**

默认情况下，免费额度耗尽后继续调用会直接扣费。建议提前开启**免费额度用完即停**功能，防止产生意外费用。

### 免费额度用完即停

开启此功能后，免费额度耗尽时将停止响应并返回错误码 `AllocationQuota.FreeTierOnly`，不会继续扣费。

#### 如何开启

##### 方式一：在模型用量页面开启

**为单个模型开启：**

1.  在控制台的[模型用量](https://bailian.console.aliyun.com/?tab=model#/model-usage/free-quota)页面，点击**免费额度**页签。
    
2.  在列表中找到目标模型，在其右侧操作列开启**免费额度用完即停**开关（无免费额度的模型无法开启）。
    

**批量开启：**

1.  在控制台的[模型用量](https://bailian.console.aliyun.com/?tab=model#/model-usage/free-quota)页面，点击**免费额度**页签。
    
2.  点击**批量操作免费额度用完即停**，在下拉菜单中选择**批量开启**。
    
3.  勾选目标模型，点击**批量开启**。如需为所有支持且未开启的模型启用，可点击**一键开启所有模型**。
    
4.  在确认弹窗中点击**开启免费额度用完即停**。
    
    ![2026-01-12\_15-51-25](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4644028671/p1044022.jpg)
    

##### 方式二：在模型广场页面开启

以 Qwen3-Coder-Plus 为例。前往[Qwen3-Coder-Plus 模型详情页](https://bailian.console.aliyun.com/?tab=model#/model-market/detail/group-qwen3-coder-plus?modelGroup=group-qwen3-coder-plus)，开启**免费额度用完即停**开关。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5847454571/p994732.png)

若模型未显示开关，说明该模型免费额度已耗尽或过期，或模型本身不提供免费额度。

#### 如何关闭

该功能默认关闭。若已启用**免费额度用完即停**，需等到控制台显示**免费额度用完**后才可关闭。

> 控制台显示的免费额度为分钟级更新（需手动刷新页面）。

## 常见问题

### 免费额度即将用完或已用完，是否有通知？

有通知。余量降至 20% 或完全耗尽时，系统通过短信、站内信、邮件发送通知。

如需开启或关闭预警、修改预警比例，请前往[我的试用](https://billing-cost.console.aliyun.com/home/myfreetier)进行设置。找到试用规格描述为**百炼大模型推理免费试用**，单击**查看试用详情**，再单击右上角**配置余量到期预警规则**即可修改。

### 免费额度用完会有什么影响？

若未开启[免费额度用完即停](https://bailian.console.aliyun.com/?tab=model#/model-usage/free-quota)，正在进行的调用不会中断，超出额度的Token将按控制台中的输入/输出价格计费，费用以按量后付费方式从阿里云账户扣除，可能导致账户欠费。

账户欠费时，即使其他模型仍有免费额度也无法调用。

调用前建议查询该模型剩余额度，并配置[预算管理](https://help.aliyun.com/zh/user-center/how-to-manage-a-budget)或[账号余额预警](https://help.aliyun.com/zh/user-center/monitor-account-balances)，确保账户有充足[余额](https://usercenter2.aliyun.com/home)，未使用的余额支持[余额提现](https://help.aliyun.com/zh/user-center/balance-withdrawal)。

### 免费额度用完后如何充值？

阿里云支持支付宝、银联在线支付、网银等多种充值方式，具体可用方式以账号[充值界面](https://billing-cost.console.aliyun.com/fortune/fund-management/recharge)展示为准。更多信息请参考[充值方式介绍](https://help.aliyun.com/zh/user-center/use-alipay-online-banking-to-recharge-online#8e4f4cdcf42rl)。

充值完成后，账户余额可能有几分钟的更新延迟，请稍后前往[费用与成本](https://usercenter2.aliyun.com/home)查看可用余额。余额到账且无欠费时即可正常调用模型。

### 如何查看免费额度消耗记录或账单？

调用结束**几分钟**后即可生成消耗记录。查询步骤：

1.  在[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面，选择账单月份，**产品名称**选择**大模型服务平台百炼**，单击**搜索**。
    
2.  单击账单列表右上角的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1247144771/p1062109.png)图标，找到**用量信息**，勾选**抵扣用量**，单击**确定**。
    
3.  找到**费用类型**为**免费额度**的账单项，**抵扣用量**即为免费额度已抵扣的用量。
    

### 为什么产生了费用？

常见原因：

-   使用了没有免费额度的模型（例如：qwen-max 和 qwen-max-latest 的免费额度不共享）。
    
-   免费额度不支持抵扣[OpenAI兼容-Batch（文件输入）](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)产生的费用。
    
-   控制台的免费额度数据为分钟级更新且需手动刷新。若未及时刷新，页面显示仍有额度但实际已耗尽，导致产生调用费用。操作前刷新页面，以最新显示为准。
    

可通过[如何查看产生费用的模型？](#3bfa8283d0tc2)和[如何查看模型调用记录？](#ab6ba5c538rn3)确认费用详情。

### 如何查看产生费用的模型？

调用结束**几分钟后**，在[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面，选择账单月份，**商品名称**选择**阿里云百炼大模型推理**，单击**搜索**。在资产/资源实例ID 列查看产生费用的模型。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2927326371/p898881.png)

### 如何查看模型调用记录？

模型调用完**一小时后**，在模型监控（[北京](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)或[新加坡](https://modelstudio.console.aliyun.com/?tab=model#/model-telemetry)）页面设置查询条件（例如，选择时间范围、业务空间等），再在**模型列表**区域找到目标模型并单击**操作**列的**监控**，即可查看该模型的调用统计结果。具体请参见[模型监控](https://help.aliyun.com/zh/model-studio/model-telemetry/)文档。

> 数据按小时更新，高峰期可能有小时级延迟，请您耐心等待。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6923304571/p992753.png)

### 如何避免扣费？

超出免费额度后会自动从账号余额扣费。可通过以下方式降低扣费风险：

-   删除已创建的 API-Key：进入阿里云百炼的[API-Key（北京）](https://bailian.console.aliyun.com/?apiKey=1&tab=globalset#/efm/api_key)或[API-Key（新加坡）](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/api_key)页面，删除已创建的 API-Key。删除后将无法通过API调用模型，不再产生调用费用。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4293235471/p943678.png)
    
-   设置[高额消费预警](https://usercenter2.aliyun.com/home/alarm-threshold)：当产品日账单超过预警阈值时，每天短信提醒一次（统计截止昨日24点）。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9403157371/p902681.png)
    

### 还有剩余额度，为何调用失败？

请检查[阿里云账户](https://usercenter2.aliyun.com/home?spm=a2c4g.11186623.nav-v2-dropdown-my-aliyun.9.f6683048dWvpGu)是否欠费。账户欠费时，即使模型仍有免费额度也无法调用。

### 为什么看不到免费额度与有效期？

免费额度列显示**无免费额度**或**免费额度**区域不显示，说明该账号下对应模型的免费额度已到期。

> 北京地域没有免费额度。
