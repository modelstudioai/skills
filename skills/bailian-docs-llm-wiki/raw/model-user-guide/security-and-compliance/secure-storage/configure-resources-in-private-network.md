# 配置私有网络中的资源

配置私有网络资源的核心目的在于为云组件（例如ElasticSearch、AnalyticDB（ADB）和OSS Bucket）创建专属的隔离环境。这样设计的目的是确保阿里云百炼平台的服务应用程序能够在安全的网络环境中顺畅地进行数据读写操作，同时避免了与平台上的其他云组件发生不必要的数据交互或资源共享，从而增强了数据的安全性和服务的稳定性。

<a id="适用范围"></a>

<a id="c892eac682ufq"></a>

## 适用范围

本文档适用于已经申请开通了阿里云百炼安全存储业务空间的用户。请咨询与您对接的商务人员了解如何开通阿里云百炼安全存储业务空间。

<a id="前提条件"></a>

<a id="f4567b7a18vgd"></a>

## 前提条件

已[配置可用区IP](configure-zone-ip.md)。

<a id="1-配置oss存储"></a>

<a id="017dd72134902"></a>

## 1\. 配置OSS存储

<a id="1-1-创建bucket"></a>

<a id="af93954a969x6"></a>

### 1.1 创建Bucket

在上传文件（Object）到OSS之前，您需要创建一个用于存储文件的存储空间（Bucket）。

1.  登录[OSS管理控制台](https://oss.console.aliyun.com/bucket)。
    
2.  在左侧导航栏，单击**Bucket 列表**，进入**Bucket 列表**页面。
    
3.  单击**创建 Bucket**。在**创建 Bucket**面板，配置以下各项参数，其余参数保持默认值即可。
    
    | 参数名称 | 参数取值 |
    | --- | --- |
    | **Bucket 名称** | 输入`bailian-safe-workspace-oss-access`。 |
    | **地域** | 选择`有地域属性`、`华北2 （北京）`。 |
    
4.  单击**完成创建**。
    

<a id="1-2-设置bucket对阿里云百炼可操作"></a>

<a id="36545c40821h2"></a>

### 1.2 设置Bucket对阿里云百炼可操作

基于安全规范要求，阿里云百炼只能访问客户授权过且设定了特定标签的Bucket。在授权阿里云百炼访问Bucket之前，需要对Bucket设置阿里云百炼可以访问的特定标签。

1.  在**Bucket 列表**页面，单击刚才创建的Bucket名称“bailian-safe-workspace-oss-access”。
    
2.  在左侧导航栏，选择**Bucket 配置Bucket 标签**。
    
3.  在**Bucket 标签**页面，单击**创建标签**。
    
4.  单击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3883543271/p832537.png)添加标签，并输入以下值配置Bucket标签。
    
    -   标签名称：输入`bailian-safe-workspace-oss-access`。
    -   标签值：输入`ReadAndWrite`。
5.  单击**保存**，完成设置。
    

<a id="1-3-创建跨域规则"></a>

<a id="08703844e5qv3"></a>

### 1.3 创建跨域规则

跨域访问是由浏览器实施的一种安全策略，核心在于遵循同源策略，这是一项旨在防范恶意脚本的重要安全机制，确保网页只能访问与其来源相同的资源。依据这一原则，未经特殊配置，浏览器会阻止页面向不同源的服务器（如阿里云对象存储OSS）发起请求，以保护用户数据和系统安全。然而，通过正确配置跨源资源共享（CORS）规则，我们可以授权特定来源的请求访问OSS跨域资源，从而规避浏览器的跨域限制，实现安全可控的数据交互。

1.  在**Bucket 列表**页面，单击刚才创建的Bucket名称“bailian-safe-workspace-oss-access”。
    
2.  在左侧导航栏，选择**数据安全跨域设置**。
    
3.  单击**创建规则**，配置以下参数，其它参数保持默认即可。
    
    | 参数名称 | 参数取值 |
    | --- | --- |
    | 来源 | 输入`*bailian.console.aliyun.com`。 |
    | 允许Methods | 选择`GET`、`POST`、`PUT`、`DELETE`。 |
    
4.  单击**确定**，完成创建。
    

<a id="1-4-配置oss"></a>

<a id="45d87ace097xs"></a>

### 1.4 配置OSS

1.  访问**[业务空间管理](https://bailian.console.aliyun.com/settings/workspace)**页面。
    
2.  查找到已经创建的阿里云百炼安全存储业务空间，在**操作**列单击**管理阿里云百炼安全存储空间**。
    
3.  连续单击**下一步**，进入**资源配置**页面。
    
4.  首次配置OSS，需要授权阿里云百炼访问您的OSS对象存储资源。
    
    在**资源配置**页面的**OSS配置**区域，单击**去授权**，再单击**确定授权**。
    
5.  选择刚才创建的Bucket“bailian-safe-workspace-oss-access”。
    
6.  单击**保存**，完成配置。
    
    > **重要**
    >
    > -   如果OSS的Bucket停止服务，将导致阿里云百炼安全存储空间、知识库、审计日志、历史记录等模块不可用，需要恢复OSS的Bucket才能恢复服务。
    > -   如果OSS的Bucket被释放，将造成阿里云百炼安全存储空间不可用，且无法恢复，需要重新创建一个新的阿里云百炼安全存储空间。
    

<a id="2-配置adb存储"></a>

<a id="uyWNn"></a>

## 2\. 配置ADB存储

<a id="2-1-购买adb资源"></a>

<a id="ef5eaa365b5g5"></a>

### 2.1 购买ADB资源

1.  登录[云原生数据仓库AnalyticDB PostgreSQL版控制台](https://gpdbnext.console.aliyun.com/gpdb/overview)。
    
2.  单击页面右上角的**购买实例**，配置以下各项参数，其余参数保持默认值即可。
    
    <table><thead><tr><th><p><strong>参数名称</strong></p></th><th><p><strong>参数取值</strong></p></th></tr></thead><tbody><tr><td><p><strong>商品类型</strong></p></td><td><p>请按实际业务需求选择。</p></td></tr><tr><td><p><strong>地域和可用区</strong></p></td><td><p>地域：选择“华北2（北京）”。</p><p>可用区：请在“华北2可用区G”、“华北2可用区H”、“华北2可用区I”中任选其一。</p></td></tr><tr><td><p><strong>引擎版本</strong></p></td><td><p>选择“6.0 标准版”。</p></td></tr><tr><td><p><strong>实例系列</strong></p></td><td><p>建议选择“高可用版”。</p></td></tr><tr><td><p><strong>向量引擎优化</strong></p></td><td><p>选择“开启”。</p></td></tr><tr><td><p><strong>专有网络（VPC）</strong></p></td><td rowspan="2"><p>选择与<a href="configure-an-endpoint-and-initiate-a-connection.md">配置终端节点并发起连接</a>中相同的专有网络和交换机。</p></td></tr><tr><td><p><strong>专有网络交换机</strong></p></td></tr></tbody></table>
    
3.  单击**立即购买** > **立即开通**创建ADB。
    
    创建过程可能需要几分钟，请您耐心等待。当运行状态为**运行中**时，表示ADB可用。
    

<a id="2-2-配置adb"></a>

<a id="c3d4051bd36ux"></a>

### 2.2 配置ADB

1.  访问**[业务空间管理](https://bailian.console.aliyun.com/settings/workspace)**页面。
    
2.  查找到已经创建的阿里云百炼安全存储业务空间，在**操作**列单击**管理阿里云百炼安全存储空间**。
    
3.  连续单击**下一步**，进入**资源配置**页面。
    
4.  首次配置ADB，需要授权阿里云百炼平台访问您的ADB对象存储资源、使用该权限访问、读取、写入和调用对象存储的数据和服务。
    
    在**资源配置**页面的**ADB配置**区域，单击**去授权**，再单击**确定授权**。
    
    授权的角色名称为 `AliyunServiceRoleForSFMAccessADB`，角色权限策略为 `AliyunServiceRolePolicyForSFMAccessADB`。
    
5.  选择刚才购买的ADB实例ID。
    
6.  单击**保存**，完成配置。
    

<a id="3-配置es存储"></a>

<a id="a86adabb34yv7"></a>

## 3\. 配置ES存储

<a id="3-1-购买elasticsearch存储"></a>

<a id="8c5f3fad16udn"></a>

### 3.1 购买ElasticSearch存储

1.  登录[阿里云Elasticsearch控制台](https://elasticsearch.console.aliyun.com/cn-beijing/instances)。
    
2.  在左侧导航栏，单击**Elasticsearch实例**。
    
3.  单击**创建**，配置以下参数，其余参数保持默认即可。
    
    <table><thead><tr><th><p><strong>参数名称</strong></p></th><th><p><strong>参数取值</strong></p></th></tr></thead><tbody><tr><td><p><strong>商品类型</strong></p></td><td><p>按实际业务需求选择。</p></td></tr><tr><td><p><strong>地域和可用区</strong></p></td><td><p>地域：选择“华北2（北京）”。</p><p>可用区：请在“北京可用区H”、“北京可用区G”或“北京可用区L”中任选其一。</p></td></tr><tr><td><p><strong>可用区数量</strong></p></td><td><p>选择“两个可用区”。</p></td></tr><tr><td><p><strong>专有网络</strong></p></td><td rowspan="2"><p>选择与<a href="configure-an-endpoint-and-initiate-a-connection.md">配置终端节点并发起连接</a>中相同的专有网络和交换机。</p></td></tr><tr><td><p><strong>虚拟交换机</strong></p></td></tr><tr><td><p><strong>实例类型</strong></p></td><td><p>选择“内核增强版”。</p></td></tr><tr><td><p><strong>Elasticsearch版本</strong></p></td><td><p>选择“7.10”。</p></td></tr><tr><td><p><strong>登录名</strong></p></td><td><p>默认值“elastic”。</p></td></tr><tr><td><p><strong>登录密码</strong></p></td><td><p>自定义设置。</p><p>请将密码记录到安全的地方，后续“配置ES”时会用到。</p></td></tr></tbody></table>
    
4.  单击**立即购买** > **立即开通**创建ES。
    
5.  在**Elasticsearch实例**页面查看已创建的ES实例。
    
    实例创建后，需要一段时间才能生效。时间长短与您的集群规格、数据结构和大小等相关，一般在小时级别。ES实例**状态**为**正常**时，表示实例可用。
    

<a id="3-2-将交换机的网段添加到es的白名单中"></a>

<a id="0747dbb943tq3"></a>

### 3.2 将交换机的网段添加到ES的白名单中

1.  在**Elasticsearch实例**页面单击已创建的ES实例名称进入ES实例详情页。
    
2.  在左侧导航栏中选择**安全配置**，再单击**VPC私网访问白名单**后的**修改**。
    
3.  单击**新增IP白名单分组**，将[获取可用区IP及交换机网段](configure-zone-ip.md#24a6fbbdc0hkn)中获取的交换机网段添加到白名单分组中。
    
    在弹出的对话框中，设置 **IP白名单分组名称**（例如 `mse_switch_iplist`），并在 **白名单内IP地址** 中填写交换机网段（例如 `192.168.0.0/24,172.16.1.0/24`），然后单击 **确认**。
    

<a id="3-3-配置es"></a>

<a id="555edf87a7aid"></a>

### 3.3 配置ES

1.  访问**[业务空间管理](https://bailian.console.aliyun.com/settings/workspace)**页面。
    
2.  查找到已经创建的阿里云百炼安全存储业务空间，在**操作**列单击**管理阿里云百炼安全存储空间**。
    
3.  连续单击**下一步**进入**资源配置**页面。
    
4.  在ElasticSearch区域配置以下参数。
    
    | 参数名称 | 参数取值 |
    | --- | --- |
    | **实例ID** | 输入刚才创建的ES实例ID。 |
    | **账号** | 输入`elastic`。 |
    | **密码** | 输入刚才创建ES实例时设置的登录密码。 |
    
5.  单击**保存**
    
    > **重要**
    >
    > -   如果ES停止计费，将导致阿里云百炼安全存储空间、知识库、审计日志、历史记录等模块不可用。需要给ES续费才能恢复服务。
    > -   如果ES被释放，将造成阿里云百炼安全存储空间不可用，且无法恢复。需要重新创建一个新的阿里云百炼安全存储空间。
    

<a id="下一步"></a>

<a id="b8a9adc49c0zr"></a>

## 下一步

[配置MSE云原生网关](configure-mse.md)
