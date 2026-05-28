# 配置MSE云原生网关

MSE（Microservices Engine）云原生网关使各服务能够互相通信。配置MSE后，可以通过MSE访问部署在私有云VPC中的资源。

## 适用范围

本文档适用于已经申请开通了阿里云百炼安全存储业务空间的用户。请咨询与您对接的商务人员了解如何开通阿里云百炼安全存储业务空间。

## 前提条件

-   已[创建网关](https://help.aliyun.com/zh/model-studio/configure-zone-ip#18a2a3bed0hua)。
    
-   已[配置私有网络中的资源](https://help.aliyun.com/zh/model-studio/configure-resources-in-private-network)。
    

## 步骤1：创建服务

将已有的服务添加到网关中，登记为路由备选服务，以便网关获取服务地址。

1.  登录[MSE网关管理控制台](https://mse.console.aliyun.com/#/microgw?region=cn-beijing)。
    
2.  在左侧导航栏选择**云原生网关** > **网关列表**，单击[创建网关](https://help.aliyun.com/zh/model-studio/configure-zone-ip#18a2a3bed0hua)中已经创建的网关名称。
    
3.  在左侧导航栏中，选择**路由管理**。
    
4.  在**服务**页签下单击**创建服务**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1149440471/p907136.png)
    
5.  配置以下参数。
    
    **配置项**
    
    **说明**
    
    **服务来源**
    
    选择**DNS域名**。表示根据DNS解析的结果作为后端服务地址。
    
    **服务名称**
    
    自定义，建议规范命名，以便准确识别服务的用途。
    
    **服务端口**
    
    ES实例的端口和域名。
    
    获取方法为：
    
    1.  在[Elasticsearch实例](https://elasticsearch.console.aliyun.com/cn-beijing/instances?spm=a2c4g.11186623.0.0.28e93c2dmLN5rz)页面，单击与[配置ES](https://help.aliyun.com/zh/model-studio/configure-resources-in-private-network#555edf87a7aid)中相同的ES实例ID进入实例详情页。
        
    2.  在**基本信息**中，**私网端口**的值为此处需要填写的服务端口。**私网地址**的值为此处需要填写的域名。
        
    
    **域名列表**
    
    **TLS模式**
    
    选择**关闭**。
    
6.  单击**确定**，完成配置。
    
    健康检查需要一定的时间，请您耐心等待。当**健康检查状态**为**健康**时，表示服务可用。
    

## 步骤2：创建路由

将请求转发至配置的目标服务。

1.  在**路由**页签下单击**创建路由**，配置以下参数。
    
    **配置项**
    
    **说明**
    
    **路由名称**
    
    自定义，建议规范命名，以便准确识别路由的用途。
    
    **域名**
    
    单击**创建域名**，输入ES实例的域名。
    
    域名获取方法为：
    
    1.  在阿里云百炼平台上，进入已经创建的安全存储业务空间。
        
    2.  在**资源配置**页面，复制ElasticSearch区域中domain的值。
        
    
    **路径**
    
    输入`/`。
    
    **路由指南**
    
    单服务。
    
    **后端服务**
    
    选择已创建的服务和端口。
    
2.  单击**保存并发布**。
    

## 步骤3：激活安全存储业务空间

1.  登录[阿里云百炼大模型服务平台](https://bailian.console.aliyun.com/#/home)。
    
2.  在**[业务空间管理](https://bailian.console.aliyun.com/?admin=1#/efm/business_management)页面**，查找到已经创建的阿里云百炼安全存储业务空间，在**操作**列单击**管理阿里云百炼安全存储空间**。
    
3.  连续单击**下一步**，进入**资源配置**页面。
    
4.  确认ElasticSearch、ADB、OSS都配置无误后，单击页面下方的**激活**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1149440471/p914713.png)
    
5.  等待界面上提示**激活成功**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1149440471/p920426.png)
    

## 验证结果

返回业务空间列表，查看安全存储业务空间状态。

-   激活前，阿里云百炼安全存储空间不可用。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1149440471/p914726.png)
    
-   激活成功后，阿里云百炼安全存储空间可用。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1149440471/p920430.png)
