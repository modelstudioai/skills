# Connector

阿里云百炼 Connector 是把企业系统与数据接入智能体的统一连接层，在控制台完成一次授权后，即可将外部系统的能力封装为 MCP 工具供智能体调用。

智能体要回答企业内部的问题，前提是能读到企业的数据。这些数据分散在钉钉文档、语雀、OSS、数据库和各类 SaaS 系统里，逐个对接既费时又难维护。

Connector 把这些系统收敛成一个统一的连接层：在控制台完成一次授权，Connector 就把对应系统的能力封装成标准工具，通过 MCP 协议暴露给智能体。智能体不需要关心数据存在哪里，直接调用工具即可。

**说明**Connector 目前处于 Beta 阶段，功能与支持的 App 列表仍在持续扩充。

## 功能特性

-   **连接 20 类系统**：钉钉、语雀、Salesforce on Alibaba Cloud、数据库、OSS 等，开箱可连，见[Apps 目录](raw/application-user-guide/overview/apps-guide/overview.md)。
-   **自动生成工具**：连接完成后自动生成可调用的工具，不需要自己写接口封装，见[核心概念](raw/application-user-guide/overview/concepts.md)。
-   **凭证配置一次复用**：同一个 App 下的所有连接共用一套身份验证配置，轮转凭证只改一处，见[身份验证概览](raw/application-user-guide/overview/auth-guide/overview.md)。
-   **托管文件与表格**：上传的文档与表格由平台托管解析，供智能体检索引用，见[文件连接器](raw/application-user-guide/overview/apps-guide/file.md)。

## 从这里开始

-   [快速开始](raw/application-user-guide/overview/quickstart.md)：连接第一个 App，并在你的智能体里调用它的工具，全程约 10 分钟。
-   [核心概念](raw/application-user-guide/overview/concepts.md)：弄清 App、连接器、工具与 MCP 之间的关系。
-   [Apps 目录](raw/application-user-guide/overview/apps-guide/overview.md)：查看全部可连接的 App 以及各自的准备条件。
-   [身份验证](raw/application-user-guide/overview/auth-guide/overview.md)：配置一次凭证，同一个 App 下的所有连接复用。

## 旧版数据连接迁移

如果此前在阿里云百炼控制台创建过数据连接，这些连接器需要迁移到新版 Connector 后才能在新版控制台中管理。

**警告**旧版数据连接的一键迁移入口开放至 **2026 年 9 月 30 日**，请在此之前完成迁移。详见[数据连接迁移](raw/application-user-guide/overview/overview/migration.md)。
