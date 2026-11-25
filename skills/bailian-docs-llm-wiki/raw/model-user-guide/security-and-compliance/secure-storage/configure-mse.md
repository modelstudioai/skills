# 配置MSE云原生网关

MSE（Microservices Engine）云原生网关使各服务能够互相通信。配置MSE后，可以通过MSE访问部署在私有云VPC中的资源。

<a id="适用范围"></a>

<a id="c892eac682ufq"></a>

## 适用范围

本文档适用于已经申请开通了阿里云百炼安全存储业务空间的用户。请咨询与您对接的商务人员了解如何开通阿里云百炼安全存储业务空间。

<a id="前提条件"></a>

<a id="1037f9e177yxu"></a>

## 前提条件

-   已[创建网关](configure-zone-ip.md#18a2a3bed0hua)。
-   已[配置私有网络中的资源](configure-resources-in-private-network.md)。

<a id="步骤1-创建服务"></a>

<a id="ca1b21a9a4sgx"></a>

## 步骤1：创建服务

将已有的服务添加到网关中，登记为路由备选服务，以便网关获取服务地址。

1.  登录[MSE网关管理控制台](https://mse.console.aliyun.com/#/microgw?region=cn-beijing)。
    
2.  在左侧导航栏选择**云原生网关** > **网关列表**，单击[创建网关](configure-zone-ip.md#18a2a3bed0hua)中已经创建的网关名称。
    
3.  在左侧导航栏中，选择**路由管理**。
    
4.  在**服务**页签下单击**创建服务**。
    
5.  配置以下参数。
    
    <table><thead><tr><th><p><strong>配置项</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p><strong>服务来源</strong></p></td><td><p>选择<strong>DNS域名</strong>。表示根据DNS解析的结果作为后端服务地址。</p></td></tr><tr><td><p><strong>服务名称</strong></p></td><td><p>自定义，建议规范命名，以便准确识别服务的用途。</p></td></tr><tr><td><p><strong>服务端口</strong></p></td><td rowspan="2"><p>ES实例的端口和域名。</p><p>获取方法为：</p><ol><li><p>在<a href="https://elasticsearch.console.aliyun.com/cn-beijing/instances?spm=a2c4g.11186623.0.0.28e93c2dmLN5rz">Elasticsearch实例</a>页面，单击与<a href="configure-resources-in-private-network.md#555edf87a7aid">配置ES</a>中相同的ES实例ID进入实例详情页。</p></li><li><p>在<strong>基本信息</strong>中，<strong>私网端口</strong>的值为此处需要填写的服务端口。<strong>私网地址</strong>的值为此处需要填写的域名。</p></li></ol></td></tr><tr><td><p><strong>域名列表</strong></p></td></tr><tr><td><p><strong>TLS模式</strong></p></td><td><p>选择<strong>关闭</strong>。</p></td></tr></tbody></table>
    
6.  单击**确定**，完成配置。
    
    健康检查需要一定的时间，请您耐心等待。当**健康检查状态**为**健康**时，表示服务可用。
    

<a id="步骤2-创建路由"></a>

<a id="7293892b4d8rf"></a>

## 步骤2：创建路由

将请求转发至配置的目标服务。

1.  在**路由**页签下单击**创建路由**，配置以下参数。
    
    <table><thead><tr><th><p><strong>配置项</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p><strong>路由名称</strong></p></td><td><p>自定义，建议规范命名，以便准确识别路由的用途。</p></td></tr><tr><td><p><strong>域名</strong></p></td><td><p>单击<strong>创建域名</strong>，输入ES实例的域名。</p><p>域名获取方法为：</p><ol><li><p>在阿里云百炼平台上，进入已经创建的安全存储业务空间。</p></li><li><p>在<strong>资源配置</strong>页面，复制ElasticSearch区域中domain的值。</p></li></ol></td></tr><tr><td><p><strong>路径</strong></p></td><td><p>输入<code>/</code>。</p></td></tr><tr><td><p><strong>路由指南</strong></p></td><td><p>单服务。</p></td></tr><tr><td><p><strong>后端服务</strong></p></td><td><p>选择已创建的服务和端口。</p></td></tr></tbody></table>
    
2.  单击**保存并发布**。
    

<a id="步骤3-激活安全存储业务空间"></a>

<a id="fc9063a2d8jz1"></a>

## 步骤3：激活安全存储业务空间

1.  登录[阿里云百炼大模型服务平台](https://bailian.console.aliyun.com/)。
2.  在**[业务空间管理](https://bailian.console.aliyun.com/settings/workspace)页面**，查找到已经创建的阿里云百炼安全存储业务空间，在**操作**列单击**管理阿里云百炼安全存储空间**。
3.  连续单击**下一步**，进入**资源配置**页面。
4.  确认ElasticSearch、ADB、OSS都配置无误后，单击页面下方的**激活**。
5.  等待界面上提示**激活成功**。

<a id="验证结果"></a>

<a id="15d08ad0d9gsa"></a>

## 验证结果

返回业务空间列表，查看安全存储业务空间状态。

-   激活前，阿里云百炼安全存储空间不可用。
-   激活成功后，阿里云百炼安全存储空间可用。
