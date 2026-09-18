# MaxCompute

连接 MaxCompute，让智能体访问项目中的数据。无需填写凭证。

MaxCompute 连接器让智能体访问 MaxCompute 项目中的数据。

它是所有需要身份验证配置的 App 中最简单的一个：身份验证方法是 OAuth 2.0，但不需要填任何凭证，只有一个可选的授权范围。

## 前置条件

-   有一个可访问的 MaxCompute 项目。
-   已建好 MaxCompute 的[身份验证配置](raw/application-user-guide/overview/auth-guide/oauth.md)。

## 连接步骤

1.  **创建身份验证配置**：在[创建身份验证配置](raw/application-user-guide/overview/auth-guide/create-config.md)的第一步选择 **MAX\_COMPUTE**，第二步页面提示请输入授权范围（可选）。
    
    字段
    
    是否必填
    
    说明
    
    配置名称
    
    否
    
    区分多个配置
    
    Scope
    
    否
    
    权限范围，不填则使用默认值
    
    两个字段都可以留空，直接单击 **完成**。
    
2.  **打开连接对话框**：在 **Apps** 页面找到 **MAX\_COMPUTE** 卡片，单击 **连接**，在 **选择身份验证配置** 中选中刚建的配置。
    
3.  **完成授权**：单击 **确定** 完成 OAuth 2.0 授权流程。
    

## 自动生成的工具

连接成功后，Connector 会自动生成访问 MaxCompute 数据的工具，在 App 详情页的 **可用的工具** 区域查看。

## 和数据库连接器的区别

MaxCompute

[MySQL、PostgreSQL、PolarDB-X 2.0](raw/application-user-guide/overview/apps-guide/database.md)

是否需要身份验证配置

需要

不需要

连接方式

OAuth 2.0 授权

从 DMS 导入数据源

适合的数据量

大数据离线分析

在线业务查询
