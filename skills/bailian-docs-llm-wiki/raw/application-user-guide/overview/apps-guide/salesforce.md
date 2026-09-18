# Salesforce on Alibaba Cloud

通过阿里云百炼 Connector 连接 Salesforce on Alibaba Cloud MCP 服务，将 MCP 工具接入千问办公、Qoder 等 Agent 客户端。

## 功能介绍

Salesforce on Alibaba Cloud 现支持通过阿里云百炼 Connector 连接 Salesforce on Alibaba Cloud MCP 服务，将该 MCP 服务提供的 MCP 工具接入千问办公/Qoder 等 Agent 客户端。

管理员在 Salesforce on Alibaba Cloud 中创建 External Client App，并在阿里云百炼 Connector 中完成 OAuth 2.0 身份验证配置和账号授权后，阿里云百炼 Connector 会连接 Salesforce on Alibaba Cloud MCP 服务，获取其提供的 MCP 工具。Agent 客户端可根据用户意图选择并调用这些工具，实时查询或操作 Salesforce on Alibaba Cloud 中的业务数据，用于客户信息查询、商机分析、销售协同等场景。

Salesforce on Alibaba Cloud MCP 服务不会预先复制、切片或索引 Salesforce 业务数据，而是在 MCP 工具被调用时实时访问原系统。可访问的数据范围取决于完成 OAuth 授权的 Salesforce 用户权限，不会绕过 Salesforce 的对象权限、字段权限和记录访问权限。

整体接入关系如下：

## 功能特色

### 标准 MCP 接入

阿里云百炼 Connector 通过连接 Salesforce on Alibaba Cloud MCP 服务获取 MCP 工具，并向 Agent 客户端提供统一接入方式。Agent 无需逐一对接 Salesforce 接口，即可发现和调用当前业务空间中已连接的工具。

### OAuth 2.0 安全授权

阿里云百炼 Connector 通过 External Client App 完成访问 Salesforce on Alibaba Cloud 所需的 OAuth 2.0 授权，Salesforce on Alibaba Cloud MCP 服务基于该授权提供 MCP 工具能力。用户在 Salesforce 登录并确认授权，无需向 Agent 客户端提供 Salesforce 用户名和密码。

### 权限随授权用户继承

MCP 工具调用遵循 Salesforce 原有权限体系。Agent 能够访问哪些对象、字段和记录，由授权用户在 Salesforce 中拥有的权限决定，便于企业沿用现有的数据访问控制策略。

### 实时访问业务数据

Salesforce on Alibaba Cloud MCP 服务在 MCP 工具被调用时实时访问 Salesforce，而不是定期同步数据副本。Agent 可基于组织中的最新客户、联系人、商机等业务信息完成分析和响应。

### 身份验证配置可复用

同一套身份验证配置可供多个连接复用。管理员只需统一维护 External Client App 的 Client ID 和 Client Secret，不同用户可分别完成 OAuth 授权，形成相互独立的连接。

### 支持多环境和多账号

生产组织与沙箱组织可分别创建身份验证配置和连接；同一组织也可使用不同权限的账号分别授权。建议在名称中标明环境和账号用途，避免生产与测试连接混用。

## 操作说明

### 准备工作

开始前，请确认已具备以下条件：

1.  可访问的 Salesforce on Alibaba Cloud 组织，以及创建和管理 External Client App 所需的管理员权限。
2.  已开通阿里云百炼的阿里云账号。
3.  阿里云百炼业务空间及其业务空间 ID，格式类似 `llm-xxxxxxxxxxxx`。
4.  属于该业务空间的 DashScope API Key。
5.  千问办公/Qoder 等 Agent 客户端。

### 第一步：创建 External Client App

1.  登录 Salesforce on Alibaba Cloud 组织。
    
2.  进入 **Setup**，在 **Quick Find** 中输入 `App Manager`，然后单击 **External Client App Manager**。
    
3.  单击 **New External Client App**，填写应用名称、联系人等基本信息。
    
4.  启用 OAuth 设置，并将 **Callback URL** 配置为：
    
    ```
    https://connector.aliyuncs.com/api/v1/bailian/connector/runtime/oauth/callback
    ```
    
    Callback URL 必须与上述地址完全一致。协议、域名、路径或末尾字符不一致，都可能导致 OAuth 回调校验失败。
    
5.  在 **OAuth Scopes** 中至少选择以下三项：
    
    OAuth Scope
    
    Scope 值
    
    用途
    
    Manage user data via APIs
    
    `api`
    
    允许 Connector 通过 API 访问授权用户可访问的 Salesforce 数据
    
    Manage user data via Web browsers
    
    `web`
    
    支持基于 Web 的 OAuth 授权流程
    
    Perform requests at any time
    
    `refresh_token, offline_access`
    
    允许 Connector 在授权有效期内刷新访问令牌
    
6.  保存 External Client App。
    

### 第二步：获取 Consumer Key 和 Consumer Secret

1.  在 **Setup** 的 **Quick Find** 中输入 `App Manager`，然后单击 **External Client App Manager**。
2.  单击已创建的 External Client App。
3.  打开 **Settings** 页签。
4.  展开 **OAuth Settings**，单击 **Consumer Key and Secret**。
5.  Salesforce 会打开 **Verify Your Identity** 页面，并向当前用户的邮箱发送验证码。
6.  将邮件中的验证码填写到验证页面，然后单击 **Verify**。
7.  复制 **Consumer Key**。Consumer Key 对应阿里云百炼 Connector 中的 **Client ID**。
8.  复制 **Consumer Secret**。Consumer Secret 对应阿里云百炼 Connector 中的 **Client Secret**。

### 第三步：创建阿里云百炼身份验证配置

1.  进入[阿里云百炼 Connector 控制台](https://bailian.console.aliyun.com/cn-beijing/connector/home)。
    
2.  在左侧导航中单击 **身份验证配置**，然后单击 **创建身份验证配置**。
    
3.  在 **选择 App** 页面选择 **Salesforce on Alibaba Cloud**。
    
4.  单击 **下一步**，填写以下信息：
    
    字段
    
    填写说明
    
    配置名称
    
    用于区分组织和环境，建议采用“组织简称-环境”格式，例如 `CXG-生产环境`
    
    组织域名
    
    Salesforce on Alibaba Cloud 组织域名，例如 `xxx.my.salesforce.com`；不要填写 `login.salesforce.com`
    
    Client ID
    
    External Client App 的 Consumer Key
    
    Client Secret
    
    External Client App 的 Consumer Secret
    
5.  单击 **完成**。保存后，该配置将显示在身份验证配置列表中。
    

生产组织和沙箱组织的域名不同。请分别创建身份验证配置，不要使用同一配置连接两个环境。

### 第四步：连接 Salesforce on Alibaba Cloud

1.  在阿里云百炼 Connector 控制台左侧导航中单击 **Apps**。
2.  找到 **Salesforce on Alibaba Cloud** App，单击 **连接**。
3.  在 **选择身份验证配置** 下拉框中选择上一步创建的配置。
4.  单击 **确定**，浏览器将跳转到 Salesforce on Alibaba Cloud 登录和授权页面。
5.  使用计划供 Agent 访问数据的 Salesforce 用户登录，并确认授权。
6.  授权完成后返回阿里云百炼控制台。在 Salesforce App 详情页的 **已连接的用户** 区域确认连接状态为 **已连接**。
7.  在 **可用的工具** 区域查看阿里云百炼 Connector 从 Salesforce on Alibaba Cloud MCP Server 获取的 MCP 工具及其输入、输出参数。具体工具范围以控制台实际展示为准。

同一个身份验证配置可以创建多个用户连接。不同连接继承各自授权用户的 Salesforce 权限。

### 第五步：连接千问办公/Qoder 等 Agent 客户端

进入阿里云百炼控制台的 **支持的客户端** 页面，选择需要连接的 Agent 客户端，并按照页面展示的接入说明完成配置。不同 Agent 客户端的配置方式可能不同，请以所选客户端页面中的说明为准。

### 第六步：验证连接

可在千问办公/Qoder 等 Agent 客户端中输入与 Salesforce 数据相关的请求，例如：查询本周新创建的商机，并按阶段汇总。

Agent 将根据请求选择阿里云百炼 Connector 从 Salesforce on Alibaba Cloud MCP 服务获取的 MCP 工具。最终可访问的数据和可执行的操作，由当前工具能力以及授权用户的 Salesforce 权限共同决定。

## 相关文档

-   [Connector 概述](raw/application-user-guide/overview.md)
-   [Salesforce：Create an External Client App](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_auth_eca.htm)
