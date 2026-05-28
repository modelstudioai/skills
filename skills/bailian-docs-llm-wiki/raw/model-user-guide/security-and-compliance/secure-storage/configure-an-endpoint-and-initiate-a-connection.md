# 配置终端节点并发起连接

在私有网络环境中配置终端节点，并将其与终端节点服务（特指阿里云百炼平台的安全存储业务空间）关联，以构建通过私网访问外部服务所需的网络连接，避免通过公网访问服务带来的潜在安全风险。这样一来，部署在安全存储业务空间内的应用程序就能顺利访问位于与终端节点相同的私有网络下的云产品组件，例如 ElasticSearch、AnalyticDB（ADB）和OSS Bucket。

## 适用范围

本文档适用于已经申请开通了阿里云百炼安全存储业务空间的用户。请咨询与您对接的商务人员了解如何开通阿里云百炼安全存储业务空间。

## 前提条件

-   已经申请开通了阿里云百炼安全存储业务空间。
    
-   已存在与阿里云百炼建立私网接入的专有网络，并获取到专有网络的名称及安全组信息。
    
    -   专有网络需要满足以下条件：
        
        -   公共云：专有网络的地域为“华北2（北京）”。专有网络的可用区包括可用区G、可用区H、可用区L中的任意两个。每个可用区至少配备一个交换机。
            
    -   安全组不需要配置任何出网和入网规则，安全组不要放入其他云组件。
        

## 步骤1：创建阿里云百炼安全存储业务空间

1.  访问**[业务空间管理](https://bailian.console.aliyun.com/?admin=1#/efm/business_management)**页面。
    
2.  单击**新增业务空间**，自定义业务空间名称，选择**空间类型**为**安全存储空间**，单击**确定**进入**终端节点配置**页面。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0002853471/p935707.png)
    
    此时，安全存储空间状态为“不可用”。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6549440471/p914619.png)
    
3.  单击**立即添加**创建反向终端节点。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6549440471/p914616.png)
    

## 步骤2：创建反向终端节点（以公共云为例）

1.  登录[终端节点控制台](https://vpc.console.aliyun.com/endpoint/cn-beijing/reverseEndpoints)。
    
2.  在顶部菜单栏处，选择地域“华北2（北京）”。
    
3.  在左侧导航栏，单击**终端节点**，进入终端节点设置页面。
    
4.  选择**反向终端节点**页签。
    
5.  如果首次使用反向终端节点服务，需要单击**开通私网连接服务**，并在弹窗中单击**开通私网连接服务**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0027950671/p1015999.png)
    
6.  单击**创建终端节点**，并配置以下各项参数，其他参数保持默认即可。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6549440471/p914631.png)
    
    **参数名称**
    
    **参数取值**
    
    **所属地域**
    
    选择“华北2（北京）”。
    
    **节点名称**
    
    自定义，建议对节点名称进行规范，以便准确识别节点的用途。
    
    例如“阿里云百炼安全存储空间的私网连接”。
    
    **终端节点类型**
    
    选择“反向终端节点”。
    
    **终端节点服务**
    
    -   首次开通阿里云百炼安全存储业务空间：在成功开通阿里云百炼安全存储业务空间后，系统将自动生成终端服务名称。请您选择**其他终端节点服务**，再单击**点击验证**，验证地址正确性即可。
        
    -   其他场景：单击**选择可用服务**，选择该账号下可用的终端节点服务。
        
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1161260471/p920518.png)
    
    **专有网络**
    
    配置为[前提条件](#9f5eaa7638q38)中已经获取的专有网络、安全组、可用区与交换机。
    
    **安全组**
    
    **可用区与交换机**
    
7.  单击**确定创建**，完成创建。
    
    此时，**连接状态**为**未连接**，说明终端节点未成功连接到阿里云百炼。
    

## 步骤3：**在阿里云百炼中确认连接**

1.  访问**[业务空间管理](https://bailian.console.aliyun.com/?admin=1#/efm/business_management)**页面。
    
2.  查找到已经创建的阿里云百炼安全存储业务空间，在**操作**列单击**管理阿里云百炼安全存储空间**。
    
3.  选择已创建的终端节点，点击**连接**，开始建立私网连接。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6549440471/p920054.png)
    
4.  建立连接需要等待一定时间。当**状态**显示**已连接**时，表示成功建立私网连接。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6549440471/p920055.png)
    

## 下一步

[配置可用区IP](https://help.aliyun.com/zh/model-studio/configure-zone-ip)
