# 配置可用区IP

本文档以公共云为例介绍如何配置可用区IP。

## 适用范围

本文档适用于已经申请开通了百炼安全存储业务空间的用户。请咨询与您对接的商务人员了解如何开通百炼安全存储业务空间。

## 前提条件

已配置终端节点并发起连接。具体操作，请参见[配置终端节点并发起连接](https://help.aliyun.com/zh/model-studio/configure-an-endpoint-and-initiate-a-connection)。

## 步骤1：创建网关

> 若您在私有云VPC所在的地域已有满足以下配置的云原生网关实例，则可跳过此步骤。

1.  登录[MSE网关管理控制台](https://mse.console.aliyun.com/#/microgw?region=cn-beijing)。
    
2.  在左侧导航栏选择**云原生网关** > **网关列表**。
    
3.  顶部菜单栏选择地域“华北2（北京）”。
    
4.  在**网关列表**页面左上角单击**创建网关**。
    
5.  在云原生网关购买页面中配置以下网关信息，其他参数保持默认值即可。
    
    **配置项**
    
    **说明**
    
    **商品类型**
    
    支持**包年包月**和**按量付费**方式。具体价格，请参见[普通实例计费概述](https://help.aliyun.com/zh/mse/product-overview/billing-overview-2#concept-2081040)。
    
    **地域**
    
    选择阿里云百炼服务所在地域“华北2（北京）”。
    
    **网关名称**
    
    自定义，建议规范命名，以便准确识别网关的用途。
    
    **网关实例规格**
    
    选择**2核4G**。
    
    ****网关节点数****
    
    选择**2**。
    
    **硬件加速**
    
    选中**启用 TLS 硬件加速**。
    
    **资源组**
    
    选择资源组。
    
    **专有网络**
    
    选择与反向终端节点相同的专有网络。
    
    **可用区位置**
    
    **手动选择**。
    
    **可用区与交换机**
    
    选择与专有网络一致的可用区及交换机。至少选择两个可用区。
    
    **网络访问类型**
    
    选择**私网**。
    
    > 关于云原生网关的更多信息，请参见[创建MSE云原生网关](https://help.aliyun.com/zh/mse/user-guide/create-a-cloud-native-gateway)。
    
6.  单击**立即购买** >**立即开通**创建网关。
    
    网关创建过程可能需要2~3分钟，请您耐心等待。当状态为**运行中**时，表示网关可用。
    

## 步骤2：获取可用区VIP及交换机网段

1.  返回控制台的**网关列表**页面，单击刚才创建的网关名称。
    
2.  在页面下方的**网关入口**页签，单击**NLB**类型的实例ID。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8001540471/p907082.png)
    
3.  获取可用区的VIP。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8001540471/p920407.png)
    
4.  单击交换机ID，获取所有交换机的网段。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8001540471/p920409.png)
    

## 步骤3：配置可用区IP

1.  访问**[业务空间管理](https://bailian.console.aliyun.com/?admin=1#/efm/business_management)**页面。
    
2.  找到已经创建的阿里云百炼安全存储业务空间，在**操作**列单击**管理阿里云百炼安全存储空间**。
    
3.  在**终端节点配置**页面单击**下一步**，进入**可用区IP配置**页面。
    
    选择与[步骤1：创建网关](#18a2a3bed0hua)中一致的可用区，如果仅有一个可用区一致，则只选择该可用区。可用区IP地址为[步骤2：获取可用区VIP及交换机网段](#24a6fbbdc0hkn)中已获取的可用区的VIP。
    
4.  配置完成后，单击**保存**。
    

## 步骤4：将MSE的NLB的IP添加到反向终端节点的安全组中

1.  在[安全组](https://ecs.console.aliyun.com/securityGroup/region/cn-beijing)中，找到反向终端节点关联的安全组。
    
2.  单击安全组名称，进入**安全组详情**页。
    
3.  在**入方向**页签中，单击**手动添加**，配置以下参数。
    
    -   **端口范围 > 目的**：选择**全部（1/65535）**。
        
    -   **源**：[步骤2：获取可用区VIP及交换机网段](#24a6fbbdc0hkn)中已经获取的VIP，多个VIP之间用逗号分隔。
        
4.  单击当前行最右侧的**保存**。
    

## 下一步

进入**资源配置**页面[配置私有网络中的资源](https://help.aliyun.com/zh/model-studio/configure-resources-in-private-network)（例如，ElasticSearch、ADB、OSS），便于阿里云百炼将数据存储到相应资源中。
