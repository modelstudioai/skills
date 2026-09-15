# API概览

## API标准及多语言预置SDK

本产品（`DataAnalysisGBI/2024-08-23`）的OpenAPI采用[ROA](https://help.aliyun.com/zh/sdk/product-overview/roa-mechanism)签名风格。我们已经为开发者封装了常见编程语言的SDK，开发者可通过[下载SDK](https://api.aliyun.com/api-tools/sdk/DataAnalysisGBI?version=2024-08-23)直接调用本产品OpenAPI而无需关心技术细节。如果现有SDK不能满足使用需求，可通过签名机制进行自签名对接。由于自签名细节非常复杂，需花费 5个工作日左右。因此建议加入我们的服务钉钉群（147535001692），在专家指导下进行签名对接。

在使用API前，您需要准备好身份账号及访问密钥（AccessKey），才能有效通过客户端工具（SDK、CLI等）访问API。细节请参见[获取AccessKey](https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair)。

## 自定义签名场景

若您的业务场景有特殊需求，需通过自签名方式对接 API，建议优先咨询我们的技术支持团队（服务钉钉群：147535001692），获取专业指导以确保高效接入。

## 账号与安全准备

阿里云账号具备对所有资源的完全管理权限。一旦 AccessKey 泄露，所有相关资源都将面临未经授权访问的风险。为确保安全，建议创建一个仅具备 API 访问权限的[RAM用户](https://help.aliyun.com/zh/ram/user-guide/create-a-ram-user)并配置其 AccessKey，同时基于最小权限原则 (PoLP) 配置 RAM 策略。仅在明确需要阿里云账号权限的特定场景下，才使用阿里云账号。

## 智能问数

API

标题

API概述

云端执行SQL方式

云端执行SQL方式

[RunDataAnalysis](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-intelligent-asking-number/api-dataanalysisgbi-2024-08-23-dir-cloud-sql-execution-mode/api-dataanalysisgbi-2024-08-23-rundataanalysis.md)

Chat对话接口

析言为您提供了与官方页面对话效果相同的OpenAPI接口，只需传入workspaceId以及query等相关信息，即可对您已经创建好的业务空间进行问答和数据分析。 该接口适合以下场景： 您在析言控制台关联了数据源，即析言可以通过公网或者VPC的方式访问您的数据库并执行SQL。 具体的使用，可以参考以下最佳实践文档： [https://help.aliyun.com/zh/model-studio/gbi-best-practices](https://help.aliyun.com/zh/model-studio/gbi-best-practices)

本地执行SQL方式

本地执行SQL方式

[RunDataResultAnalysis](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-intelligent-asking-number/api-dataanalysisgbi-2024-08-23-dir-local-sql-execution-mode/api-dataanalysisgbi-2024-08-23-rundataresultanalysis.md)

执行结果分析

对结构化数据类型的执行结果进行分析、可视化信息生成。

[RunSqlGeneration](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-intelligent-asking-number/api-dataanalysisgbi-2024-08-23-dir-local-sql-execution-mode/api-dataanalysisgbi-2024-08-23-runsqlgeneration.md)

运行sql生成

运行sql生成，根据当前的query信息，结合已关联的数据表，进行sql语句的生成。 该接口适合以下场景： 您的数据库在本地，不能被析言访问。 您可以通过析言关联虚拟数据源，调用该接口生成SQL，然后自行解析和执行SQL。 具体的使用，可以参考以下最佳实践文档： [https://help.aliyun.com/zh/model-studio/xiyan-gbi-local-data-best-practices](https://help.aliyun.com/zh/model-studio/xiyan-gbi-local-data-best-practices)

## 业务逻辑解释

API

标题

API概述

[UpdateBusinessLogic](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-business-logic-explanation/api-dataanalysisgbi-2024-08-23-updatebusinesslogic.md)

修改业务逻辑解释

修改当前指定业务空间下所指定的业务逻辑解释。

[CreateBusinessLogic](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-business-logic-explanation/api-dataanalysisgbi-2024-08-23-createbusinesslogic.md)

创建业务逻辑解释

在指定的业务空间下创建新的业务逻辑解释。

[ListBusinessLogic](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-business-logic-explanation/api-dataanalysisgbi-2024-08-23-listbusinesslogic.md)

业务逻辑解释列表

获取当前指定业务空间下的企业知识名词解释列表。

[DeleteBusinessLogic](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-business-logic-explanation/api-dataanalysisgbi-2024-08-23-deletebusinesslogic.md)

删除业务逻辑解释

删除指定业务空间下所指定的业务逻辑解释。

## 同义词解释

API

标题

API概述

[CreateSynonyms](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-synonym-explanation/api-dataanalysisgbi-2024-08-23-createsynonyms.md)

创建同义词

在当前指定的业务空间下面，新建同义词。

[ListSynonyms](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-synonym-explanation/api-dataanalysisgbi-2024-08-23-listsynonyms.md)

同义词列表

获取当前指定业务空间下的同义词列表。

[UpdateSynonyms](https://help.aliyun.com/zh/model-studio/api-dataanalysisgbi-2024-08-23-updatesynonyms)

修改同义词

修改当前业务空间指定的同义词信息。

[BatchDeleteSynonyms](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-synonym-explanation/api-dataanalysisgbi-2024-08-23-batchdeletesynonyms.md)

批量删除同义词

批量删除当前指定业务空间下的同义词。

## 数据源管理

API

标题

API概述

[CreateDatasourceAuthorization](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-data-source-management/api-dataanalysisgbi-2024-08-23-createdatasourceauthorization.md)

数据源关联关系授权

创建数据库关联授权，在您指定的业务空间，对指定的数据源进行关联关系的创建，创建后可以对数据源下的表结构进行采集。

[CancelDatasourceAuthorization](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-data-source-management/api-dataanalysisgbi-2024-08-23-canceldatasourceauthorization.md)

取消数据源关联关系授权

取消关联的数据源授权。

[SyncRemoteTables](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-data-source-management/api-dataanalysisgbi-2024-08-23-syncremotetables.md)

从数据源同步数据表

更新当前业务空间所关联的数据表，从远程数据源（虚拟数据源）同步最近的表并关联到您所指定的业务空间。

[ListSelectedTables](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-data-source-management/api-dataanalysisgbi-2024-08-23-listselectedtables.md)

选择的数据表集合

获取当前业务空间处于以关联状态的数据表。

[UpdateTableInfo](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-data-source-management/api-dataanalysisgbi-2024-08-23-updatetableinfo.md)

修改数据表信息

修改当前所指定的数据表的信息。

[DeleteSelectedTable](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-data-source-management/api-dataanalysisgbi-2024-08-23-deleteselectedtable.md)

删除所选择的数据表

将当前指定数据表从指定业务空间管控中删除。

[ResyncTable](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-data-source-management/api-dataanalysisgbi-2024-08-23-resynctable.md)

刷新当前所关联的数

从远程数据库刷新当前所关联的数据表信息。

[ListColumn](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-data-source-management/api-dataanalysisgbi-2024-08-23-listcolumn.md)

数据表下的数据列集合

获取当前指定业务空间，指定表下面的列信息。

[UpdateColumn](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-data-source-management/api-dataanalysisgbi-2024-08-23-updatecolumn.md)

修改数据列信息

修改当前指定业务空间中，指定列的信息。

[RecoverColumn](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-data-source-management/api-dataanalysisgbi-2024-08-23-recovercolumn.md)

还原数据列信息

将指定数据表的数据列恢复到初始化关联时的状态。

[DeleteColumn](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-data-source-management/api-dataanalysisgbi-2024-08-23-deletecolumn.md)

删除数据表中的列

从当前所指定的业务空间中，删除所指定的列。

[ListEnumMapping](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-data-source-management/api-dataanalysisgbi-2024-08-23-listenummapping.md)

枚举值映射列表

获取当前业务空间，指定表、列下的枚举值。

[UpdateEnumMapping](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-data-source-management/api-dataanalysisgbi-2024-08-23-updateenummapping.md)

修改枚举值映射关系

修改当前指定业务空间指定列下的枚举值信息。

## 虚拟数据源

API

标题

API概述

[CreateVirtualDatasourceInstance](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-virtual-data-source/api-dataanalysisgbi-2024-08-23-createvirtualdatasourceinstance.md)

创建虚拟数据源实例

在您指定的业务空间创建虚拟数据源实例，虚拟数据源实例代表着一个虚拟的数据库，可以向虚拟数据源中添加ddl语句，来完成您构建虚拟数据库，数据表的能力。

[ListVirtualDatasourceInstance](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-virtual-data-source/api-dataanalysisgbi-2024-08-23-listvirtualdatasourceinstance.md)

虚拟数据源实例列表

获取当前业务空间下的数据源实例列表。

[UpdateVirtualDatasourceInstance](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-virtual-data-source/api-dataanalysisgbi-2024-08-23-updatevirtualdatasourceinstance.md)

修改虚拟数据源实例信息

修改指定业务空间下所指定的虚拟数据源的信息。

[DeleteVirtualDatasourceInstance](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-virtual-data-source/api-dataanalysisgbi-2024-08-23-deletevirtualdatasourceinstance.md)

删除虚拟数据源实例

删除指定业务空间下面的虚拟数据源实例。

[SaveVirtualDatasourceDdl](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-virtual-data-source/api-dataanalysisgbi-2024-08-23-savevirtualdatasourceddl.md)

向虚拟数据源中添加ddl语句

向您当前指定的业务空间下指定的虚拟数据源实例中添加ddl语句，析言GBI云服务会将您的ddl语句解析成相关的表结构信息并进行维护。
