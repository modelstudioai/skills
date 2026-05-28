# 权限管理

阿里云百炼权限管理支持基于控制台页面级、模型级的多维度权限控制，满足多地域、多用户的复杂组织架构需求。

## **阿里云百炼身份管理**

单个业务空间是进行**精细化权限管理**（模型、用户）和[阿里云账单分账](#23e1b216deked)的最小管理单元。

百炼的业务空间权限管理基于三种角色：

1.  **超级管理员**：可**跨空间**统一管理用户权限、空间可用模型、空间模型限流和 API Key。
    
2.  **业务空间管理员**：只负责**某个特定业务空间**内的用户权限和资源管理。
    
3.  **普通用户**：根据分配的权限使用资源。
    

**业务空间权限**

**超级管理员**（拥有[AliyunBailianFullAccess](https://help.aliyun.com/zh/ram/developer-reference/aliyunbailianfullaccess)系统策略**）**

**业务空间管理员**

普通用户

允许特定模型调用 & 限流

支持

不支持

不支持

允许特定模型调优

支持

不支持

不支持

允许特定模型部署

支持

不支持

不支持

用户管理

支持

支持

不支持

用户可用页面管理

支持

支持

不支持

API Key 管理

支持

支持

不支持

访问/使用被授权的空间、页面、资源

支持

支持

支持

[OpenAPI 接口权限](#4adcb2854f9rv)

不支持

不支持

不支持

### **超级管理员**

包含以下两类账号：

-   阿里云主账号，可在百炼控制台右上角看到：
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7097957671/p1040205.png)
    
-   拥有[AliyunBailianFullAccess](https://help.aliyun.com/zh/ram/developer-reference/aliyunbailianfullaccess) （百炼管理员）系统策略的 [RAM 用户](https://ram.console.aliyun.com/users)（账号）。该 RAM 用户可以通过百炼的全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) | [新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management) | [弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)），为任意 RAM 用户（包括自己）授权任意**地域**、任意**空间**的几乎所有权限。（仅 [OpenAPI 接口权限](#4adcb2854f9rv) 需要阿里云主账号可以添加）
    
    > [RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)是阿里云主账号创建的子账号，用于安全地向团队内成员分配云资源和权限。
    
    可在右上角看到：
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7097957671/p1040215.png)
    

超级管理员可以使用百炼的全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) | [新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management) | [弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)），进行多业务空间管理。功能包含：

1.  新建业务空间，管理业务空间名称。
    
2.  对所有[业务空间](#dac6676deelh2)进行模型管理、模型限流。
    
3.  对所有业务空间进行账号（用户）管理。
    
4.  管理所有的 API Key。
    

**说明**

如需开通 [AI 安全护栏服务](https://help.aliyun.com/zh/document_detail/2923687.html)、[模型监控](https://help.aliyun.com/zh/model-studio/model-telemetry/#54ea9ba526ovz)、[应用观测](https://help.aliyun.com/zh/model-studio/application-observation#8b8e3a09a3wj3)等功能，建议使用**阿里云主账号**在控制台进行一次性授权和开通。

### **业务空间管理员**

指的是拥有访问某个业务空间**权限管理**页面的阿里云 [RAM 用户](https://ram.console.aliyun.com/users)。可以通过该页面管理该业务空间。

> **管理员**权限包含可访问该业务空间下所有页面的权限。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7097957671/p1040099.png)

## **业务空间权限管理**

百炼按地理区域划分资源和业务空间，**单个业务空间不能跨地域存在。即使各个地域的默认业务空间，也是不同的空间**。点击前往全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) | [新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management) | [弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)）。

同时百炼的业务空间是进行**精细化权限管理**的**最小**管理单元，它可管理：

**业务空间权限**

**超级管理员**（拥有[AliyunBailianFullAccess](https://help.aliyun.com/zh/ram/developer-reference/aliyunbailianfullaccess)系统策略**）**

**业务空间管理员**

普通用户

允许特定模型调用 & 限流

支持

不支持

不支持

允许特定模型调优

支持

不支持

不支持

允许特定模型部署

支持

不支持

不支持

用户管理

支持

支持

不支持

用户可用页面管理

支持

支持

不支持

API Key 管理

支持

支持

不支持

访问/使用被授权的空间、页面、资源

支持

支持

支持

[OpenAPI 接口权限](#4adcb2854f9rv)

不支持

不支持

不支持

-   **限制模型调用**：管理某个模型可否在该业务空间**调用**（控制台& API）并设置该模型的**请求数限流**和 **Token限流**。
    
    > 默认业务空间无法设置此限制，所有模型均可调用，且无法限流。
    
    ![PixPin\_2025-12-05\_17-10-08](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7097957671/p1032822.png)
    
-   **限制模型训练**：管理某个模型可否在该业务空间进行调优（通过控制台和API）和调优后部署**。**
    
    > 默认业务空间无法设置此限制，所有支持调优的模型均可调优以及调优完成后部署。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7097957671/p1040196.png)
    
-   **限制模型部署**：管理某个模型可否在该业务空间**直接部署。**
    
    > 默认业务空间无法设置此限制，所有支持部署的模型均可部署。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8097957671/p1040197.png)
    
-   **用户（账号）控制台权限管理**：管理某个 RAM 用户是否能使用该业务空间**控制台**的功能以及能使用该业务空间控制台的哪些功能。但无法限制归属该用户的 API Key 的调用。
    
    > 阿里云主账号无须设置，可以访问所有业务空间的所有页面。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7097957671/p1040204.png)
    

### **API-Key 权限**

单个 API Key 只能归属一个地域内的一个业务空间和一个用户，且不能转移给其他业务空间或其他用户。API Key 的可调用的功能和模型限流与**归属业务空间**的权限保持一致**，**不受**用户（账号）控制台权限管理**的影响，也无需为不同模型（如文生文、文生图、语音合成）创建不同的API Key。

API Key 的状态随归属用户（账号）操作的变化：

**说明**

自 2026年3月25日开始，**华北2（北京）**地域的所有新创建的 API Key 均归属主账号。

**触发操作**

**主账号的 API Key**

**RAM 账号的 API Key**

**主动删除 API Key**

不支持 失效，不可恢复

不支持 失效，不可恢复

**将账号移出业务空间**

—

不支持 失效

> 重新加入业务空间后 API Key 恢复生效

**在** [RAM 控制台](https://ram.console.aliyun.com/roles)**删除账号/角色**

—

不支持 失效，不可恢复

**为 API Key 设置 IP 访问白名单**

**华北2（北京）**地域的 API Key 支持设置。

**华北2（北京）**地域的 API Key 支持设置。

**管理 API-Key**：可以通过百炼控制台**左侧导航栏**中的**权限管理**页签内，为 RAM 用户添加 API-Key 权限。赋予对应 RAM 用户**创建、删除、查看该空间下所有 API-Key** 的权限。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7097957671/p1041247.png)

### **OpenAPI 接口权限**

RAM 用户默认无权调用百炼**应用**的数据、知识库、Prompt工程及长期记忆等功能的[Open API](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-dir/)。

若需调用，需要**阿里云主账号**在 [RAM 控制台](https://ram.console.aliyun.com/users)为 RAM 用户添加以下**权限之一**：

-   [AliyunBailianDataFullAccess](https://help.aliyun.com/zh/ram/developer-reference/aliyunbailiandatafullaccess)：可调用百炼应用 [API目录](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-dir/)下的所有API。
    
-   [AliyunBailianDataReadOnlyAccess](https://help.aliyun.com/zh/ram/developer-reference/aliyunbailiandatareadonlyaccess)：可调用百炼应用 [API目录](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-dir/)下的**只读类**API，例如[DescribeFile - 查询文件状态](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-describefile)、[GetIndexJobStatus - 查询知识库创建任务状态](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-getindexjobstatus)等。
    

![PixPin\_2025-12-08\_17-48-55](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7097957671/p1033176.png)

### **应用于生产环境**

-   **空间规划策略**
    
    -   **按环境划分（推荐）：**为开发、测试、预发和生产环境创建独立的业务空间，实现严格的环境隔离。
        
        -   `project-dev-workspace`
            
        -   `project-test-workspace`
            
        -   `project-prod-workspace`
            
    -   **按业务线划分：**为公司内不同的业务部门（如市场、售后、设计）创建独立的业务空间，便于权限和成本管理。
        
        -   `marketing-team-workspace`
            
        -   `customer-team-workspace`
            
-   **限流策略**
    
    -   将主账号总配额按比例分配给各业务空间，并预留一部分作为缓冲，以应对突发流量。
        
        **示例：**账号总配额为 1000 QPM，分配方案如下：
        
        -   `project-prod-workspace`: 600 QPM (60%)
            
        -   `project-test-workspace`: 200 QPM (20%)
            
        -   `project-dev-workspace`: 100 QPM (10%)
            
        -   预留缓冲：100 QPM (10%)
            

## **账单查看与预付费权限管理**

RAM 用户默认无权查看阿里云账单和购买阿里云预付费产品，如需为 RAM 用户开通相关权限，需要在 [RAM 控制台](https://ram.console.aliyun.com/users)为 RAM 用户添加**特定权限。**

**说明**

以下权限将授予 RAM 用户**查看**阿里云**所有产品**的账单或**购买**阿里云**所有预付费产品**的权限，请谨慎授权。

1.  查看阿里云账单需要为 RAM 用户添加 [AliyunBSSReadOnlyAccess 权限](https://help.aliyun.com/zh/user-center/ram-policies-for-billing-management#li-lj9-l6a-in1)。
    
2.  购买阿里云预付费产品需要为 RAM 用户添加 [AliyunBSSOrderAccess 权限](https://help.aliyun.com/zh/user-center/ram-policies-for-billing-management#li-q7v-rt1-xvi) 。
    

**细粒度页面权限**

菜单

子菜单

AliyunBSSReadOnlyAccess

AliyunBSSOrderAccess

账户总览

页面可查看，无业务操作

页面不可查看，不可发起业务操作

账户总览

充值

页面可查看，不可发起业务操作

页面不可查看，不可发起业务操作

账户总览

提现

页面可查看，可发起业务操作

页面不可查看，不可发起业务操作

账户总览

退款

页面可查看，不可发起业务操作

页面不可查看，不可发起业务操作

账户总览

申请网商贷

页面可查看，可发起业务操作

页面不可查看，不可发起业务操作

账户总览

申请支付宝首付款工具

页面可查看，可发起业务操作

页面不可查看，不可发起业务操作

账户总览

查看详情

页面可查看，无业务操作

页面不可查看，不可发起业务操作

账户总览

代金券管理

页面可查看，无业务操作

页面不可查看，不可发起业务操作

账户总览

资源包管理

页面可查看，无业务操作

页面不可查看，不可发起业务操作

账户总览

索取发票

页面可查看，无业务操作

页面不可查看，不可发起业务操作

账户总览

申请合同

页面可查看，无业务操作

页面不可查看，不可发起业务操作

收支明细

页面可查看，不可发起业务操作

页面不可查看，不可发起业务操作

消费记录

消费总览

页面可查看，可发起业务操作

页面不可查看，不可发起业务操作

消费记录

消费明细

页面可查看，可发起业务操作

页面不可查看，不可发起业务操作

消费记录

使用记录

页面可查看，可发起业务操作

页面不可查看，不可发起业务操作

消费记录

实例消费明细

页面可查看，可发起业务操作

页面不可查看，不可发起业务操作

消费记录

月度成本消耗

页面可查看，可发起业务操作

页面不可查看，不可发起业务操作

消费记录

导出记录

页面可查看，可发起业务操作

页面不可查看，不可发起业务操作

消费记录

存储到OSS

页面可查看，可发起业务操作

页面不可查看，不可发起业务操作

账单分析

产品账单分析

页面可查看，可发起业务操作

页面不可查看，不可发起业务操作

保证金管理

页面可查看，不可发起业务操作

页面不可查看，不可发起业务操作

订单管理

页面可查看，不可发起业务操作

页面可查看，可发起业务操作

代金券管理

页面可查看，无业务操作

页面不可查看，不可发起业务操作

优惠券管理

页面不可查看，不可发起业务操作

页面不可查看，不可发起业务操作

储值卡管理

页面不可查看，不可发起业务操作

页面不可查看，不可发起业务操作

提货券管理

页面不可查看，不可发起业务操作

页面不可查看，不可发起业务操作

采购单

页面不可查看，不可发起业务操作

页面不可查看，不可发起业务操作

资源包管理

资源包概览

页面可查看，无业务操作

页面不可查看，不可发起业务操作

资源包管理

使用明细

页面可查看，无业务操作

页面不可查看，不可发起业务操作

发票管理

发票索取

页面可查看，不可发起业务操作

页面不可查看，不可发起业务操作

发票管理

发票列表

页面可查看，无业务操作

页面不可查看，不可发起业务操作

发票管理

发票信息管理

页面可查看，不可发起业务操作

页面不可查看，不可发起业务操作

发票管理

发票寄送地址管理

页面可查看，不可发起业务操作

页面不可查看，不可发起业务操作

汇款底单管理

页面可查看，不可发起业务操作

页面不可查看，不可发起业务操作

退订管理

五天无理由退款

页面可查看，不可发起业务操作

页面不可查看，不可发起业务操作

退订管理

退订记录

页面可查看，无业务操作

页面不可查看，不可发起业务操作

合同管理

合同申请

页面可查看，无业务操作

页面不可查看，不可发起业务操作

合同管理

合同管理

页面可查看，无业务操作

页面不可查看，不可发起业务操作

可用性中心

页面不可查看，不可发起业务操作

页面不可查看，不可发起业务操作

续费管理

页面不可查看，不可发起业务操作

页面不可查看，不可发起业务操作

购买页

各产品购买页

页面可查看，不可发起业务操作

页面可查看，不可发起业务操作

## **常用设置**

### **设置超级管理员**

> 需要 阿里云账号（主账号）或具备[AliyunRAMFullAccess](https://help.aliyun.com/zh/ram/developer-reference/aliyunramfullaccess)系统策略的 RAM 用户操作。

1.  前往 [RAM 控制台](https://ram.console.aliyun.com/users)，为 RAM 用户添加 [AliyunBailianFullAccess](https://help.aliyun.com/zh/ram/developer-reference/aliyunbailianfullaccess) （百炼管理员）权限和 [AliyunBSSOrderAccess](https://help.aliyun.com/zh/user-center/ram-policies-for-billing-management#h3-jp4-73a-2wi)（购买阿里云预付费产品）权限。
    
2.  设置完成后即可通过百炼的全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) | [新加坡](https://modelstudio.console.aliyun.com/?tab=globalset#/efm/business_management) | [弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management)），为任意 RAM 用户（包括自己）授权任意**地域**、任意**空间**的任意权限，并购买百炼的预付费产品。
    

### **设置业务空间管理员**

> 需要超级管理员或业务空间管理员操作。

1.  在百炼控制台**左侧导航栏**中的**权限管理**页签内，为 RAM 用户添加**管理员**权限。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7097957671/p1041236.png)
    

### **设置模型调用权限**

1.  若不使用**默认业务空间**，需保证业务空间已经为特定模型开通了[模型调用](#7e5a648ddattc)权限。（需要超级管理员操作）
    
2.  **若需要通过百炼的控制台调用**，需要在百炼控制台**左侧导航栏**中的**权限管理**页签内，为 RAM 用户添加：（需要超级管理员或业务空间管理员操作）
    
    1.  **模型体验-操作** 权限，用于在控制台上调用模型。
        
    2.  **批量推理-操作** 权限，用于支持 [批量推理](https://help.aliyun.com/zh/model-studio/batch-inference)功能。
        
    3.  **模型观测-操作** 权限，用于查看模型调用、评测的 Token 消耗量。
        
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7097957671/p1040170.png)
    
3.  **若需要通过百炼的 API 调用，**需要为 RAM 用户在对应业务空间创建或分配 API Key，更多细节请参考本文的：[API-Key 权限](#f2704153a055r)。（需要超级管理员或业务空间管理员操作）
    

### **设置控制台模型调优权限**

1.  若不使用**默认业务空间**，需保证业务空间已经为特定模型开通了[模型调优（训练）](#c180b853793v3)权限。（需要超级管理员操作）
    
2.  在百炼控制台**左侧导航栏**中的**权限管理**页签内，为 RAM 用户添加几乎所有的模型权限：（需要超级管理员或业务空间管理员操作）
    
    1.  **模型体验-操作** 权限，用于在控制台上调用调优后的模型。
        
    2.  **模型调优-操作** 权限。
        
    3.  **我的模型-操作** 权限，用于管理调优完成后的模型快照。
        
    4.  **模型部署-操作** 权限，用于部署调优后的模型，模型部署后才能调用、评测。
        
    5.  **模型评测-操作** 权限。
        
    6.  **数据管理-操作** 权限，用于管理调优数据集。
        
    7.  **模型观测-操作** 权限，用于查看模型调用、评测的 Token 消耗量。
        

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7097957671/p1040160.png)

### **设置 API 模型调优权限**

1.  若不使用**默认业务空间**，需保证业务空间为特定模型开通了[模型调优（训练）](#c180b853793v3)权限。（需要超级管理员操作）
    
2.  为 RAM 用户在对应业务空间创建或分配 API Key，更多细节请参考本文的：[API-Key 权限](#f2704153a055r)。（需要超级管理员或业务空间管理员操作）
    

## **常见问题**

### **1\. 如何获取业务空间 ID 呢？**

请参考应用开发的[获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

### **2\. 如何使用子业务空间调用模型？**

无需特殊设置，使用子业务空间的 API-Key 即可。

### **3\. 如何使用特定业务空间的应用？**

使用 API 管理、调用特定业务空间的应用需要同时设置 [APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)。
