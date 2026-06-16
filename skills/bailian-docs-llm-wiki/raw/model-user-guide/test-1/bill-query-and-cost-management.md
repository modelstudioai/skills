# 账单查询与成本管理

本文介绍如何查询账单明细、进行成本分摊（分账）、处理账户欠费以及停止计费。

## **查询账单**

仅在实际发生调用**结束**后生成账单：**大模型推理**分钟级出账（通常 2~10 分钟），**批量推理、模型训练、知识库**等小时级出账，业务高峰期请以系统最终出账时间为准。

### **费用概览**

登录[百炼控制台](https://bailian.console.aliyun.com/?tab=model)，单击顶部**模型**标签页，在左侧菜单选择**用量 & 费用** > [**费用概览**](https://bailian.console.aliyun.com/?tab=model#/costing-balance/overview)，选择**账期月份**：

> 该页面仅展示**大模型推理**相关费用。**模型训练**和**知识库**等费用请通过[账单详情](#29f8b9b9a4lmc)查看。

-   **查看总消费与构成**：顶部展示当月**总消费金额**，拆分为**订阅购买费用**（Token Plan、预置吞吐、模型单元、节省计划等）与**账单费用**（按量产生的模型调用与训练）；点击**订阅购买费用**或**账单费用**卡片的**查看明细**可展开分项。下方**账单趋势**仅展示后付费账单金额，不含预付费（订阅购买）金额。当月查看时，**账单费用**通常先更新，**账单趋势**出账稍有延迟。
    
-   **按模型或 API Key 查询费用**：在**账单趋势**区域，**模型**下拉选择目标模型（或按 **API Key ID** 筛选），切换至**列表**视图，累计**应付金额**列即为该项当月总费用。
    
-   **对比支出趋势**：将**分组**设为**产品分类**，按**天**或**月**对比模型部署、推理、训练的支出走势。
    
-   **设置费用告警**：在**账单费用**卡片单击**费用告警**右侧的**修改**，在**消费限额与告警**面板开启月度限额、设置阈值与邮件/短信通知，达阈值即提醒，避免欠费停服。
    

### **账单详情**

大模型推理、部署与训练账单可按 **ApiKeyID、业务空间ID、模型名称、输入/输出类型、调用渠道****、实例标签**拆分查看。

#### **1\. 下载账单**

1.  在[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面，选择账单月份，
    
2.  选择**产品名称**为**大模型服务平台百炼**，单击**搜索**。
    
3.  单击账单列表右上角的导出图标，将账单下载到本地。
    
4.  打开文件，找到 实例 ID（出账粒度）列，根据下文规则进行核对。
    

#### **2\. 解读关键字段**

**“实例 ID（出账粒度）”字段**以英文分号 `;` 分隔，完整格式为`ApiKeyID;业务空间 ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`。

-   格式 A：标准调用（包含ApiKeyID）
    
    -   示例：`12xxx;llm-xxx;qwen-max;output_token;app;0`
        
    -   依次表示`ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`。
        
-   格式 B：控制台调用（不含ApiKeyID）
    
    -   示例：`;llm-xxx;qwen-max;output_token;app;0`
        
    -   依次表示`;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`。
        
    -   若不包含`ApiKeyID`，通常表示该费用是通过阿里云百炼控制台产生的，而非通过代码调用。
        

**“实例标签”字段**：如果您使用了标签分账，该列显示格式如下：

-   示例：`key:test1 value:test1; key:test2 value:test2`
    
-   `key` 代表标签键，`value` 代表标签值。
    
-   多个标签之间用英文分号 ; 隔开。
    

#### **3\. 数据溯源与术语说明**

-   查询 API Key：复制账单中的 `ApiKeyID`，前往[百炼API Key管理](https://bailian.console.aliyun.com/?tab=model#/api-key)页面查找对应的 Key 名称。
    
-   查询业务空间：复制账单中的 `业务空间ID`，前往[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)，点击左侧菜单底部的**默认业务空间**，点击**业务空间详情**，确认具体空间ID。您也可以切换到其他业务空间。
    
-   调用渠道说明：
    
    -   `app`：通过应用程序（代码）调用模型。
        
    -   `bmp`：表示通过控制台[模型体验](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/text)调用模型。
        
    -   `assistant-api`：表示通过Assistant API调用模型。
        

## **分账管理**

给**业务空间**绑定**标签**，可按部门或项目归集费用。

1.  **获取业务空间信息**：在[**业务空间管理**](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)确定标签绑定的业务空间**Workspace ID**（示例：llm-xxx），并在[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)确定业务空间的**地域**信息。
    
2.  **绑定标签**：
    
    1.  在[**标签管理**](https://resourcemanager.console.aliyun.com/tags#/)页面选择**资源绑定标签。**
        
    2.  资源选择方式选择“**输入多个资源ID**”，在产品选项卡搜索并选择“**大模型服务平台百炼:业务空间**”并选择业务空间对应地域，资源ID输入框中填写**Workspace ID**，完成后点击绑定标签按钮执行操作。
        
    3.  在绑定标签页面中，创建标签键值或使用已创建的预置标签与业务空间绑定。当完成键值输入或选择好预置标签后，点击**确定**完成业务空间标签的绑定。
        
    4.  启用标签。进入[费用标签](https://billing-cost.console.aliyun.com/finance/tags)，在“**标签key**”中输入已绑定的标签键，单击**搜索**，找到标签，并在操作列单击**启用**。
        
3.  **验证**：配置完成后，分账账单 T+1 天后生效。可在[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面通过**实例标签**列验证业务空间的绑定标签。
    

## **欠费处理**

**账户可用额度 < 0** 视为欠费，可能导致模型调用等服务暂停。在[费用与成本首页](https://billing-cost.console.aliyun.com/home)悬停**账户可用额度**区域可查看，公式为：可用额度 =（现金余额 + 信控额度）-（当月未结清 + 历史未结清）。

-   **欠费影响**：按账单**商品名称**维度判定。
    
    -   仍有**免费额度**：可继续使用，用完后停用。
        
    -   仍有**节省计划**或**资源包**额度：可继续使用。
        
    -   已购 **Coding Plan** 或 **Token Plan**：套餐额度独立于账户余额，欠费期间可继续使用，但会导致自动续费失败，到期后无法续用。
        
    -   以上额度均无：该商品下服务将**暂停**，需结清欠费后恢复。
        
-   **结清欠费**：在[费用与成本](https://usercenter2.aliyun.com/home)页面单击**充值汇款**，输入金额并完成支付。
    
-   **预防欠费**：在[高额消费预警](https://usercenter2.aliyun.com/home/alarm-threshold)页面设置消费阈值，达阈值即提醒。
    

## **停止计费（关闭服务）**

不再使用百炼时，按以下方式关停对应服务即可停止计费。

-   **停止模型推理**：停止代码中的 API 调用、关闭控制台的模型体验，即不再产生费用。为防止意外调用，可在[**API-KEY**](https://bailian.console.aliyun.com/?apiKey=1&tab=globalset#/efm/api_key)页面删除已创建的 Key。
    
-   **停止模型训练**：没有正在进行的训练任务时即不产生费用。
    
-   **取消 Coding Plan 订阅**：Coding Plan 为包月订阅产品，到期自动停止，中途不支持取消和退款。如已开启自动续费，请在[Coding Plan](https://bailian.console.aliyun.com/?tab=model#/efm/coding_plan) 页面关闭自动续费。
    
-   **退订 Token Plan 团队版**：在[Token Plan 控制台](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/token-plan)的**我的订阅**页面按席位退订，未产生用量消耗的席位可退订，退款原路退回支付账户。如不再续费，请关闭自动续费。
    
-   **停止模型部署**：根据部署时的计费方式操作不同：
    
    -   按模型调用量计费：[下线](https://bailian.console.aliyun.com/?tab=model#/efm/model_deploy)已部署的模型，或删除[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)防止意外调用。
        
    -   按算力使用时长计费：[下线](https://bailian.console.aliyun.com/?tab=model#/efm/model_deploy)已部署的模型。
        
    -   包月预付费：[下线](https://bailian.console.aliyun.com/?tab=model#/efm/model_deploy)已部署的模型，然后在[退订管理](https://usercenter2.aliyun.com/refund/refund)页面退订实例。退订时按已消费金额扣减，退回剩余金额（详见[退订说明](https://help.aliyun.com/zh/user-center/user-guide/refund-management/)）。
        

## **常见问题**

**为什么调用模型后查不到账单？**

**原因：**

-   **出账延迟**：模型推理账单按分钟汇总，调用后通常 2~10 分钟出账；批量推理、模型训练、知识库等按小时汇总，业务高峰可能进一步延迟。
    
-   **使用了非商业化模型**：公测、邀测模型不产生账单记录。
    

**解决方案：**等待对应出账时长后再查询。

**为什么同一个模型在账单中有多行记录？**

**原因：**同一模型按计费类型（输入 Token、输出 Token、缓存命中等）和调用渠道（API 调用、控制台体验等）分别出账。例如 qwen3.6-plus 一次对话会产生“输入 Token”和“输出 Token”两行记录。

**解决方案：**通过[账单详情](#29f8b9b9a4lmc)中的`实例 ID`字段区分每行记录的具体含义。

**账单里很多行都叫“大模型文本消耗量”，怎么区分是哪个模型？**

**原因：**账单的“计费项”统一显示为“大模型文本消耗量”，未直接展示模型名称。

**解决方案：**查看[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页的**实例 ID（出账粒度）**列。字段以英文分号分隔，紧跟业务空间 ID（如 llm-xxx）之后的字段即为模型名称。例：`12xxx;llm-xxx;**qwen3.6-plus**;context_0-128k_input_token;bmp;0`表示 qwen3.6-plus 模型。

**在哪里查看模型调用次数和统计？**

进入[阿里云百炼控制台](https://bailian.console.aliyun.com/?tab=model)，右上角选择目标地域，单击顶部**模型**标签页，在左侧菜单选择**用量 & 费用** > [模型用量](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/usage-statistics)。

**按量付费是实时扣款吗？**

不是。阿里云按量付费采用“预占+月结”模式 — 系统先冻结部分额度，月账期结束后（次月初）生成最终账单并实际扣款。

**如何导出明细账单用于报销？**

参考[如何导出明细账单](https://help.aliyun.com/zh/user-center/support/billing-faqs)。

**如何充值？**

参考[如何充值缴费](https://help.aliyun.com/zh/user-center/use-alipay-online-banking-to-recharge-online)。

**为什么没怎么用却产生了欠费？**

**原因：**百炼的[联网搜索](https://help.aliyun.com/zh/model-studio/web-search)等附加功能按调用次数单独计费（后付费），与模型推理费用分开出账。即使您近期未主动操作控制台，历史创建的应用或代码中若开启了 `enable_search` 参数，每次被调用仍会产生联网搜索费用。

**解决方案：**

1.  在[账单详情](#29f8b9b9a4lmc)中筛选**大模型服务平台百炼**，查看**实例 ID（出账粒度）**列，确认产生费用的模型名称和调用渠道。
    
2.  检查应用代码或百炼应用配置中是否开启了 `enable_search`，如不再需要联网搜索，将该参数设为 `false` 或移除。
    
3.  如已停止所有调用但仍有扣费，检查是否有其他 API Key 或应用仍在运行，可在[API Key 管理](https://bailian.console.aliyun.com/?tab=model#/api-key)页面逐一排查或删除不再使用的 Key。
