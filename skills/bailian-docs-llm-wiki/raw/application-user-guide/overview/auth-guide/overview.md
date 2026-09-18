# 身份验证概览

理解身份验证配置的作用，判断你要连的 App 是否需要先建一个。

部分 App 在连接之前需要先有一个身份验证配置。控制台对它的定义是：身份验证配置是一个蓝图，它定义了工具包在所有用户中的身份验证方式。

换成一句话：配置一次凭证，之后这个 App 下所有人的连接都复用同一套认证方式。

## 为什么要单独一层

如果每次连接都重新填一遍 Client ID 和 Client Secret，同一个 App 连十个账号就要填十遍，凭证轮转时要改十处。身份验证配置把这部分抽出来：

创建连接时不再填凭证，只需要从下拉框里选一个已有的配置。控制台在连接对话框里的说明是：身份认证定义用户如何在当前 App 创建连接，支持认证方式和凭证选择。

## 哪些 App 需要

不是所有 App 都需要。目前需要先建身份验证配置的有 3 个：

App

身份验证方法

[Salesforce on Alibaba Cloud](raw/application-user-guide/overview/apps-guide/salesforce.md)

OAuth 2.0

[MaxCompute](raw/application-user-guide/overview/apps-guide/maxcompute.md)

OAuth 2.0

[语雀](raw/application-user-guide/overview/apps-guide/yuque.md)

API Key

其余 App 直接在连接对话框里完成配置，不经过这一层：

App

连接时填什么

[文件连接器](raw/application-user-guide/overview/apps-guide/file.md)、[表格连接器](raw/application-user-guide/overview/apps-guide/table.md)

连接器名称与存储位置

[OSS](raw/application-user-guide/overview/apps-guide/oss.md)

连接器名称与存储 Bucket，并完成授权

[MySQL、PostgreSQL、PolarDB-X 2.0](raw/application-user-guide/overview/apps-guide/database.md)

连接器名称，并从 DMS 导入数据源

**说明**判断方法很直接：单击 App 卡片上的 **连接**，如果对话框里只有一个 **选择身份验证配置** 下拉框，说明这个 App 需要先建配置。

## 两种身份验证方法

方法

控制台说明

适用

OAuth 2.0

通过 OAuth 2.0 授权流程实现安全、用户友好的登录

用户跳转到对方系统登录并授权，凭证由平台托管

API Key

使用 API Key 完成身份验证

直接填入对方系统签发的密钥

方法不由你选择，由 App 决定。进入创建流程后，**身份验证方法** 一栏直接显示该 App 支持的方法。

## 和连接的关系

三层关系是这样的：

一个身份验证配置可以支撑多个连接。反过来，一个连接只属于一个身份验证配置。

## 从哪里进入

控制台左侧导航的 **身份验证配置** 是这一层的管理入口。首次进入时页面显示请先完成身份验证配置，单击 **创建身份验证配置** 开始。

也可以从连接流程进入：在 App 的连接对话框里展开 **选择身份验证配置** 下拉框，如果显示暂无配置，单击下方的 **创建身份验证配置** 会直接跳到创建页面，并预先带上当前 App。

**重要**接下来看[创建身份验证配置](raw/application-user-guide/overview/auth-guide/create-config.md)，里面是逐字段的填写说明。
