# Apps 目录

Connector 支持的全部 App、各自的接入方式与准备条件。

控制台左侧的 **Apps** 页面列出全部可连接的系统。每张卡片代表一类 App，卡片上的数字表示你已经在该 App 下创建了多少个连接。

页面顶部提供三个筛选页签和一个搜索框：

页签

含义

全部

显示所有 App，无论是否已连接

已连接

仅显示至少有一个可用连接的 App

已过期

仅显示凭证已失效、需要重新授权的 App

## 先判断要不要身份验证配置

这是连接前最关键的一个判断。单击 App 卡片的 **连接** 后，按出现的内容区分：

需要先建配置的 App，字段和获取路径见[身份验证概览](raw/application-user-guide/overview/auth-guide/overview.md)。

## 需要身份验证配置的 App

App

身份验证方法

需要准备

[Salesforce on Alibaba Cloud](raw/application-user-guide/overview/apps-guide/salesforce.md)

OAuth 2.0

组织域名、External Client App 的 Client ID 与 Client Secret

[MaxCompute](raw/application-user-guide/overview/apps-guide/maxcompute.md)

OAuth 2.0

无需凭证，仅可选的授权范围

[语雀](raw/application-user-guide/overview/apps-guide/yuque.md)

API Key

语雀 Token

## 直接连接的 App

### 平台托管

数据上传到阿里云百炼平台后由平台解析和托管，不需要外部系统的凭证。

App

用途

生成的工具

[文件连接器](raw/application-user-guide/overview/apps-guide/file.md)

托管非结构化文档，如 PDF、Word、Markdown

搜索文件、获取文件

[表格连接器](raw/application-user-guide/overview/apps-guide/table.md)

托管结构化表格数据，如 XLSX、XLS

获取表结构

连接对话框包含连接器名称、连接器描述和 **存储位置**。存储位置目前只有 **使用平台存储** 一个选项，数据存放在平台提供的有限免费存储资源内。

### 阿里云对象存储

App

用途

需要准备

[OSS](raw/application-user-guide/overview/apps-guide/oss.md)

访问对象存储中的文件

OSS Bucket，并完成授权与打标签

连接对话框包含连接器名称、连接器描述和 **存储 Bucket 选择**，旁边有 **立即授权** 入口。

### 数据库

数据保留在原数据库中实时访问，通过 DMS 导入数据源完成配置。

App

用途

需要准备

[MySQL](raw/application-user-guide/overview/apps-guide/database.md)

连接 MySQL 数据库并执行 SQL 查询

MySQL 实例与 DMS 录入

[PostgreSQL](raw/application-user-guide/overview/apps-guide/database.md)

连接 PostgreSQL 数据库并执行 SQL 查询

PostgreSQL 实例与 DMS 录入

[PolarDB-X 2.0](raw/application-user-guide/overview/apps-guide/database.md)

连接 PolarDB-X 2.0 分布式数据库

PolarDB-X 2.0 实例与 DMS 录入

连接对话框的 **选择数据来源** 提供从 DMS 导入数据源，说明是快速导入 DMS 中已经创建的数据源，通过 DMS 统一管理各类数据源。

### 钉钉系列

连接对话框里只有一个字段，填钉钉 MCP 网关签发的接入地址，不需要连接器名称。

App

用途

需要准备

[钉钉文档、钉钉表格、钉钉AI表格、钉钉待办、钉钉日历、钉钉机器人消息](raw/application-user-guide/overview/apps-guide/dingtalk.md)

钉钉办公协作

每个 App 各一个含密钥的 MCP 接入地址

这 6 个 App 的按钮是 **提交**，不是其他 App 的 **确认**。

### 邮箱

连接对话框里只有两个字段：**邮箱地址** 和 **授权码**（在邮箱设置中开启 IMAP/SMTP 服务后生成），授权码被加密存储。

App

用途

需要准备

[QQ邮箱](raw/application-user-guide/overview/apps-guide/qq-mail.md)

通过 IMAP/SMTP 访问 QQ 邮箱邮件

QQ 邮箱地址与授权码

[网易邮箱](raw/application-user-guide/overview/apps-guide/netease-mail.md)

通过 IMAP/SMTP 访问 163 邮箱邮件

163 邮箱地址与授权码

这两个 App 的按钮是 **提交**，不是需要身份验证配置的 App 的 **确认**。

## 通过授权窗口连接的 App

这类 App 不弹对话框，而是新开一个独立窗口，在对方系统里完成授权。

App

用途

需要准备

[云效](raw/application-user-guide/overview/apps-guide/yunxiao.md)

访问 Codeup 代码库、分支、提交与合并请求

浏览器已登录云效，账号在目标组织内

[腾讯文档](raw/application-user-guide/overview/apps-guide/tencent-docs.md)

读取、创建和编辑腾讯文档

浏览器能访问腾讯文档，授权时登录腾讯文档账号

**说明**Connector 处于 Beta 阶段，App 列表和各 App 的连接能力在陆续开放。控制台 **Apps** 页面可能出现本文档尚未覆盖的 App，请以页面实际显示为准。

## 通用字段

需要身份验证配置的 App、钉钉系列、邮箱系列和通过授权窗口连接的 App 之外，连接对话框都包含以下公共字段：

字段

是否必填

说明

连接器名称

是

区分同一 App 下的多个连接，最多 64 个字符

连接器描述

否

说明数据内容与用途，会影响智能体选择工具的准确度

其余字段由 App 类型决定，见各 App 的详细说明。

## 管理已有连接

在 App 详情页的 **已连接的用户** 区域可以新增、改名、查看详情和删除连接。完整说明见[连接的账户](raw/application-user-guide/overview/auth-guide/connected-accounts.md)。

**警告**连接类型在创建后不可更改。如需更换，只能新建连接。

**重要**不确定从哪个 App 开始，先用[文件连接器](raw/application-user-guide/overview/apps-guide/file.md)跑通流程，它不需要任何外部凭证，也不需要身份验证配置。
