# 使用Prompt样例库优化模型输出

当通用大语言模型在处理特定领域的专业任务时，可能难以生成精准或符合预设格式的回答。采用少样本学习（Few-shot learning）的思路，从预定义的高质量问答对中检索相关样例作为模型参考，引导其生成更准确、风格更一致的回复。该功能尤其适用于需要严格遵循既有知识或固定风格的场景，例如智能客服、特定领域知识问答以及格式化内容生成。

**说明**

Prompt样例库功能已不再维护，推荐您将样例库数据迁移到 RAG 表格库中，参见[Prompt 样例库迁移到 RAG 表格库](https://help.aliyun.com/zh/model-studio/migrate-sample-library-prompt-to-rag-table-library)。

## **效果展示**

以下表格展示了样例库中包含的样例内容。

**用户输入**

**模型输出**

解释术语：API (Application Programming Interface)

解释：API是一种定义了软件组件之间如何交互的接口规范，它允许不同的应用程序通过预设的规则和协议进行数据交换和功能调用。 类比：想象你点餐的菜单，菜单（API）列出了你可以点的菜品（功能）以及如何点（请求格式），厨房（服务）会根据菜单的要求准备好食物（响应），你不必知道厨房内部如何运作。

解释术语：区块链 (Blockchain)

解释：区块链是一种分布式、去中心化的数字账本技术，它将交易数据记录在一个不断增长的、由加密链接起来的“区块”链中，使得数据难以被篡改，提高了透明度和安全性。 类比：就像一个由许多人共同维护的、大家都看得见的银行流水账本，每个新交易都被记录在一个新的条目里，并用密码锁住，而且这个账本一旦写好，就很难再被一个人悄悄修改。

解释术语：量子纠缠 (Quantum Entanglement)

解释：量子纠缠是一种奇特的量子力学现象，当两个或多个粒子之间存在某种关联时，它们的状态是相互依赖的，无论它们相距多远，测量其中一个粒子的状态会瞬间影响到另一个粒子的状态。 类比：想象你有一双神奇的手套，你戴上左手手套，另一只手套（无论在哪里）立刻就变成了右手手套。它们的状态是瞬间关联的。

使用该Prompt样例库后，模型严格遵循了样例中的术语解释结构和类比风格。效果对比如下：

**未使用Prompt样例库**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1806201671/p1005929.png)

**使用Prompt样例库**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1806201671/p1007424.png)

## **创建并使用**Prompt样例库

### **1\. 创建Prompt样例库**

1.  访问[样例库](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt-case)页面，单击**创建样例库**（首次创建时显示）或单击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6604462571/p975472.png)图标新建样例库。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6604462571/p975479.png)
    
2.  输入样例库名称，并选择导入方式，支持**手动输入**和**批量导入**两种。
    
    #### **手动输入**
    
    直接在页面上输入样例信息（用户输入和模型输出），可单击**新增样例**添加多条。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3269174671/p899538.png)
    
    #### **批量导入**
    
    下载模板文件，按格式填写后上传。支持小于 20MB 的 Excel 文件，单次最多导入 100 条样例。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5423376371/p899543.png)
    

### **2\. 在智能体应用中使用样例库**

将Prompt样例库与位于相同的业务空间里的智能体应用关联，使其生效。

1.  确保你已有一个[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)。
    
2.  前往[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面，找到目标智能体应用，单击应用卡片上的**配置**。
    
3.  找到并打开**样例库**开关。添加样例库，选择上一步创建的样例库（一个应用最多可关联5个样例库，采用多路召回策略）。
    
    > 多路召回策略：系统会从所有关联的库中检索相关样例，并通过排序模型选出最相关的K条（召回片段数，可配置）加入到大模型的输入Token中用于其回答时参考。
    
    **说明**
    
    目前尚不支持用户手动设置检索顺序。
    
4.  **可选**：单击**配置**，调整召回片段数（默认为5，最多10）。
    
5.  **发布**应用，使配置生效。
    

### **3\. 测试验证**

#### **控制台调试**

在应用调试界面输入一个与样例相关的查询。例如，**解释术语：神经网络 (Neural Network)**。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1806201671/p1007424.png)

单击**prompt样例检索**，可查看样例检索的输入输出。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1806201671/p1005919.png)

#### **API调用**

在调用应用 API 时，将请求参数 `has_thoughts` 设置为 `true`，响应中的 `thoughts` 字段将包含详细的检索过程信息，便于调试和验证。调用示例可参考[应用调用](https://help.aliyun.com/zh/model-studio/application-calling-guide#a52e24a20c60u)。

## **管理样例库与样例**

在 Prompt样例库页面，可以对已创建的库和库中的样例进行维护。

### **管理样例库**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5423376371/p899512.png)

-   新增：单击**样例库管理**右侧的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5423376371/p899513.png)图标创建新的样例库。
    
-   删除：鼠标悬停在目标样例库上，单击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5423376371/p899514.png)图标删除样例库。
    
    > 正在被应用引用的样例库无法直接删除。请先前往**应用管理**页面，在相关应用的配置中解除引用关系，然后再执行删除操作。
    
-   重命名：鼠标悬停在需要重命名的样例库上，单击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5423376371/p899515.png)图标对样例库重命名。
    

### **管理样例**

选择样例库，在当前样例库中执行以下操作：

-   增加：单击**丰富样例**或**导入数据**增加相似样例。
    
-   删除：在目标样例的**操作**列，单击**删除**。
    
-   修改：在待修改样例的**操作**列，单击**编辑**，修改**用户输入**或**模型输出**内容，并**保存**。
    

## **使用限制**

-   **样例库容量**：每个样例库最多包含 300 条样例。
    
    **说明**
    
    此限制旨在平衡检索性能与召回准确率。过大的单库规模可能导致检索延迟增加。若样例超过 300 条，建议根据业务主题将其拆分为多个独立的样例库（如“产品功能库”、“售后策略库”）。
    
-   **应用关联数量**：每个智能体应用最多可关联 5 个样例库。
    
    **说明**
    
    系统采用多路召回策略，会从所有关联的库中并行检索。
    
-   **召回片段数**：单次请求最多召回 10 个样例片段注入上下文。
    
    **说明**
    
    此参数可在应用配置中调整，用于控制注入上下文的长度，以平衡效果和 Token 成本。
    
-   **文件导入限制**：批量导入时，支持 20MB 以内的 Excel 文件，单次最多导入 100 条样例。
    

## 计费说明

Prompt 样例库功能本身**不收取**存储或管理费用。

但是，启用此功能会**增加大模型调用的 Token 消耗**，从而影响你的总体费用。增加的 Token 主要来自被召回并注入到上下文中的样例内容。

**成本预估公式**： 总输入 Token ≈ 用户查询 Token + 所有召回样例的总 Token + 系统指令 Token

## **常见问题**

-   **样例库和样例的关系？**
    
    包含关系。每个样例库最多包含300个相似的样例。每个样例包括用户输入和模型输出。
    
    样例通过样例库进行组织和管理，可以增加多个不同名称的样例库进行应用配置。
