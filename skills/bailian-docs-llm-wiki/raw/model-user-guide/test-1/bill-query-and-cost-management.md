# 账单查询与成本管理

本文介绍如何查询账单明细、进行成本分摊（分账）、处理账户欠费以及停止计费。

## **查询账单**

**说明**

Coding Plan 不产生按量账单，可在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)查看套餐用量。

### **出账周期**

仅在实际发生调用后，系统才会生成账单。

-   **大模型推理**：分钟级出账。
    
-   **其他服务（批量推理/模型训练/知识库等）**：小时级出账。
    

系统出账存在延迟（如大模型推理账单通常在调用后2～10分钟左右生成），业务高峰期请以系统最终出账时间为准。

### **1\. 查询具体模型的推理费用**

如果您想知道某个特定模型（如 qwen-plus）的推理费用，请按以下步骤操作：

1.  在[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面，选择账单月份。
    
2.  选择**商品名称**为**百炼大模型推理**，单击**搜索**。
    
3.  在实例 ID（出账粒度）列找到所有与qwen-plus相关的实例。
    
4.  将这些实例对应的**应付金额**相加，即为该模型在选定月份的推理总费用。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6506545671/p1030802.png)

### **2\. 查询百炼服务的总费用**

如果您想查看百炼平台整体或某类服务的总支出趋势，可通过成本分析功能查看。

**查看“模型推理”服务的总费用**

1.  在[成本分析](https://usercenter2.aliyun.com/expense-manage/expense-analyze)页面，**成本类型**选择**应付金额**。
    
2.  **时间粒度**选择**月**，选择时间范围，例如2025年05月～10月。
    
3.  **产品明细**选择百炼大模型推理，即可查看所选时间范围内模型推理总花费。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6506545671/p1030807.png)

**查看“阿里云百炼平台”所有服务的总费用**

1.  在[成本分析](https://usercenter2.aliyun.com/expense-manage/expense-analyze)页面，**成本类型**选择**应付金额**。
    
2.  **时间粒度**选择**月**，选择时间范围，例如2025年10月。
    
3.  **产品**选择**大模型服务平台百炼**，即可查看所选时间范围内百炼的成本支出。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6506545671/p1030808.png)

### **3\. 查询明细账单的Token消耗量**

在[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面中导出，可在账单中查看到Token用量。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3694117471/p952403.png)

## 分析账单明细

自2024年9月7日起，阿里云百炼的大模型推理、部署与训练账单支持更细维度的核对。您可以通过 **ApiKeyID、业务空间ID、模型名称、输入/输出类型、调用渠道****、实例标签**来查看费用。

#### **1\.** 下载账单

1.  在[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面，选择账单月份，
    
2.  选择**产品名称**为**大模型服务平台百炼**，单击**搜索**。
    
3.  单击账单列表右上角的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6506545671/p995237.png)图标，将账单下载到本地。
    
4.  打开文件，找到 实例 ID（出账粒度）列，根据下文规则进行核对。
    

#### **2\. 解读关键字段**

**“实例 ID（出账粒度）”字段**：此字段包含多段信息，通常以英文分号 ; 分隔。完整格式为`ApiKeyID;业务空间 ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`。

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
        

## 分账管理

如果您需要将费用归属到不同的部门或项目，可以使用“标签”功能对**业务空间**进行标记。

**步骤一：获取业务空间信息**

在[**业务空间管理**](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)确定标签绑定的业务空间**Workspace ID**（示例：llm-xxx），并在[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)确定业务空间的**地域**信息。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3694117471/p952142.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3694117471/p952383.png)

**步骤二：绑定标签**

1.  在[**标签管理**](https://resourcemanager.console.aliyun.com/tags#/)页面选择**资源绑定标签。**
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3694117471/p952146.png)
    
2.  资源选择方式选择“**输入多个资源ID**”，在产品选项卡搜索并选择“**大模型服务平台百炼:业务空间**”并选择业务空间对应地域，资源ID输入框中填写**Workspace ID**，完成后点击绑定标签按钮执行操作。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3694117471/p952362.png)
    
3.  在绑定标签页面中，创建标签键值或使用已创建的预置标签与业务空间绑定。当完成键值输入或选择好预置标签后，点击**确定**完成业务空间标签的绑定。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3694117471/p951040.png)
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3694117471/p952461.png)
    
4.  启用标签。进入[费用标签](https://billing-cost.console.aliyun.com/finance/tags)，在“**标签key**”中输入已绑定的标签键，单击**搜索**，找到标签，并在操作列单击**启用**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6049720771/p1052873.png)
    

**第三步：验证**

配置完成后，分账账单T+1天后生效 。您可在[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面通过**实例标签**列验证与查询业务空间的绑定标签。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3694117471/p952391.png)

## **欠费说明与处理**

当您的 **账户可用额度 < 0** 时，即视为欠费。欠费可能导致服务暂停（如模型无法调用），建议您保持余额充足并开启预警。

### 1\. 如何查看是否欠费

将鼠标悬停在[费用与成本首页](https://billing-cost.console.aliyun.com/home)的 **账户可用额度** 区域。

-   计算公式：可用额度 = （现金余额 + 信控额度）-（当月未结清 + 历史未结清）。
    
-   如果计算结果小于 0，请立即充值。
    

### **2\. 欠费影响**

欠费影响按**商品名称**维度判定（对应账单中的"商品名称"字段）。当某一商品的使用导致账户欠费时，其他商品下的服务是否可用取决于以下条件：

-   若该商品下的模型仍有**免费额度**，可继续使用。免费额度用完后将无法使用。
    
-   若已购买**节省计划**或**资源包**且仍有额度，可继续使用。
    
-   若既无免费额度，也无节省计划或资源包额度，则**无法使用**。
    

Coding Plan 和 Token Plan 套餐额度独立于账户余额，欠费不影响使用。但账户欠费会导致自动续费失败，套餐到期后将无法继续使用。

### **3\. 结清欠费账单**

-   余额核查：登录[费用与成本](https://usercenter2.aliyun.com/home)页面，查看账户余额。
    
-   充值操作：点击**充值汇款**按钮，输入所需金额并完成支付。
    

### **4\. 如何避免欠费停服**

设置消费预警：您可以在[高额消费预警](https://usercenter2.aliyun.com/home/alarm-threshold)设置消费阈值，系统将在触达该金额时发送提醒。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3957386371/p902494.png)

## 停止计费（关闭服务）

如果您不再需要使用百炼服务，可以通过以下方式停止计费，避免产生额外费用。

### 1\. 取消 Coding Plan 订阅

Coding Plan 为包月订阅产品，到期自动停止，无需手动取消。如需关闭自动续费，请[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)关闭自动续费。

### 2\. 停止模型推理

-   操作：停止使用相关功能后将不再产生费用，如不再使用阿里云百炼控制台进行模型体验、停止所有代码中的 API 调用等。
    
-   建议：为了避免意外调用，您可以访问[阿里云百炼控制台](https://modelstudio.console.alibabacloud.com/)，在页面右上角选择目标地域，进入[**API-KEY**](https://bailian.console.aliyun.com/?apiKey=1&tab=globalset#/efm/api_key)页面删除已创建的 API-Key。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1493235471/p943518.png)
    

### **3\.** 停止模型训练

-   操作：只要没有正在进行的训练任务，就不会产生费用。
    

### 4\. 停止模型部署

根据部署时的计费方式，操作略有不同：

-   按模型调用量计费：[下线](https://bailian.console.aliyun.com/?tab=model#/efm/model_deploy)已部署的模型，或删除阿里云百炼的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)防止意外调用产生费用。
    
-   按算力使用时长计费：[下线](https://bailian.console.aliyun.com/?tab=model#/efm/model_deploy)已部署的模型。
    
-   包月预付费：
    
    -   [下线](https://bailian.console.aliyun.com/?tab=model#/efm/model_deploy)已部署的模型，然后在[退订管理](https://usercenter2.aliyun.com/refund/refund)页面，退订已购买的资源实例。
        
    -   退订时，将从实付金额中扣除已消费金额，退回剩余金额。具体说明请参考[退订说明](https://help.aliyun.com/zh/user-center/user-guide/refund-management/)。
        

## **常见问题**

#### **Q：为什么我刚刚调用了模型，却查不到账单？**

A：可能原因如下：

1.  **出账延迟**：大模型推理账单**按分钟**汇总生成，调用完成后通常会在2～10分钟左右出账；其他（批量推理、模型训练、知识库等）则按**小时**汇总生成账单。如遇业务高峰期，实际出账可能会有延迟，具体以系统实际出账时间为准。
    
2.  **使用了公测/邀测等非商业化的模型**：不会产生账单记录。
    

#### **Q：为什么同一个模型在账单中有多行记录？**

A：同一个模型的费用会按计费类型（输入 Token、输出 Token、缓存命中等）和调用渠道（API 调用、控制台体验等）分别出账。

例如，使用 qwen3.6-plus 模型进行一次对话，会产生“输入 Token”和“输出 Token”两行账单记录。您可以通过[分析账单明细](#29f8b9b9a4lmc)中的`实例 ID` 字段来区分每行记录的具体含义。

#### **Q：账单里有很多行都叫“大模型文本消耗量”，怎么知道每行是哪个模型产生的？**

A：您可以通过查看[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面的 **实例 ID（出账粒度）** 列来确认。

-   字段使用英文分号;分隔。通常情况下，紧跟在业务空间 ID（如 llm-xxx）之后的字段，即为实际调用的模型名称。
    
-   示例：`12xxx;llm-xxx;**qwen3.6-plus**;context_0-128k_input_token;bmp;0`，这表明该行记录对应的是`qwen3.6-plus` 模型的费用。
    

#### **Q：在哪里看模型的调用次数和统计？**

A： 您可以访问[阿里云百炼控制台](https://modelstudio.console.alibabacloud.com/)，在页面右上角选择目标地域，进入[模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)页面查询模型调用统计。

#### **Q：按量付费是实时扣款吗？**

A： 不是。阿里云按量付费通常采用“预占+月结”模式。系统会先冻结一部分额度，每个月账期结束后（次月初），才会生成最终账单并统一进行实际扣款。

#### **Q：如何导出明细账单用于报销？**

A：请参考[如何导出明细账单](https://help.aliyun.com/zh/user-center/support/billing-faqs)进行操作。

#### **Q：如何充值？**

A：请参考[如何充值缴费](https://help.aliyun.com/zh/user-center/use-alipay-online-banking-to-recharge-online)进行操作。
