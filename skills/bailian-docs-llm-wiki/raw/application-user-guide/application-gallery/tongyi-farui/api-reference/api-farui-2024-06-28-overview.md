# API概览

## API标准及多语言预置SDK

本产品（`FaRui/2024-06-28`）的OpenAPI采用[ROA](https://help.aliyun.com/zh/sdk/product-overview/roa-mechanism)签名风格。我们已经为开发者封装了常见编程语言的SDK，开发者可通过[下载SDK](https://api.aliyun.com/api-tools/sdk/FaRui?version=2024-06-28)直接调用本产品OpenAPI而无需关心技术细节。如果现有SDK不能满足使用需求，可通过签名机制进行自签名对接。由于自签名细节非常复杂，需花费 5个工作日左右。因此建议加入我们的服务钉钉群（147535001692），在专家指导下进行签名对接。

在使用API前，您需要准备好身份账号及访问密钥（AccessKey），才能有效通过客户端工具（SDK、CLI等）访问API。细节请参见[获取AccessKey](https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair)。

## 自定义签名场景

若您的业务场景有特殊需求，需通过自签名方式对接 API，建议优先咨询我们的技术支持团队（服务钉钉群：147535001692），获取专业指导以确保高效接入。

## 账号与安全准备

阿里云账号具备对所有资源的完全管理权限。一旦 AccessKey 泄露，所有相关资源都将面临未经授权访问的风险。为确保安全，建议创建一个仅具备 API 访问权限的[RAM用户](https://help.aliyun.com/zh/ram/user-guide/create-a-ram-user)并配置其 AccessKey，同时基于最小权限原则 (PoLP) 配置 RAM 策略。仅在明确需要阿里云账号权限的特定场景下，才使用阿里云账号。

## 法律咨询

API

标题

API概述

[RunLegalAdviceConsultation](raw/application-user-guide/application-gallery/tongyi-farui/api-reference/api-farui-2024-06-28-dir/api-farui-2024-06-28-dir-legal-advice/api-farui-2024-06-28-runlegaladviceconsultation.md)

法律咨询

法律咨询。

## 合同审查

API

标题

API概述

[CreateTextFile](raw/application-user-guide/application-gallery/tongyi-farui/api-reference/api-farui-2024-06-28-dir/api-farui-2024-06-28-dir-contract-review/api-farui-2024-06-28-createtextfile.md)

上传合同审查文件

该接口用于将文档上传到合同审查模块中，添加成功之后，系统会自动启动文件的解析，并返回对应的文件ID用于后续生成审查规则和审查结果。文件解析有排队机制，如果队列较长，文件可能需要等待一段时间才能解析完成。

[RunContractRuleGeneration](raw/application-user-guide/application-gallery/tongyi-farui/api-reference/api-farui-2024-06-28-dir/api-farui-2024-06-28-dir-contract-review/api-farui-2024-06-28-runcontractrulegeneration.md)

生成合同审查规则

该接口用于合同审查模块的智能规则生成，调用大模型返回合同的审查规则和对应风险。传入合同审查文件的ID、审查立场，会通过sse的方式增量式返回模型生成的审查规则。

[RunContractResultGeneration](raw/application-user-guide/application-gallery/tongyi-farui/api-reference/api-farui-2024-06-28-dir/api-farui-2024-06-28-dir-contract-review/api-farui-2024-06-28-runcontractresultgeneration.md)

生成合同审查结果

该接口用于合同审查模块的审查结果生成，调用大模型返回合同的审查结果、审查风险项、建议修改内容等。传入合同审查文件的ID、审查立场、审查规则，会通过sse的方式增量式返回模型生成的审查结果。

## 搜索服务

API

标题

API概述

[RunSearchLawQuery](raw/application-user-guide/application-gallery/tongyi-farui/api-reference/api-farui-2024-06-28-dir/api-farui-2024-06-28-dir-search-services/api-farui-2024-06-28-runsearchlawquery.md)

法规检索

该接口用于检索用户描述的问题对应的相关法规。用户输入问题后，会调用大模型分析并检索对应的法规法条。

[RunSearchCaseFullText](raw/application-user-guide/application-gallery/tongyi-farui/api-reference/api-farui-2024-06-28-dir/api-farui-2024-06-28-dir-search-services/api-farui-2024-06-28-runsearchcasefulltext.md)

案例检索

该接口用于检索用户描述的问题对应的相关案例。用户输入问题后，会调用大模型解析用户问题生成对应的检索条件，并根据检索条件检索对应的案例。

## 合同抽取

API

标题

API概述

[RunContractExtract](raw/application-user-guide/application-gallery/tongyi-farui/api-reference/api-farui-2024-06-28-dir/api-farui-2024-06-28-dir-contract-extraction/api-farui-2024-06-28-runcontractextract.md)

合同抽取

该接口用于根据合同内容抽取相应的字段。用户输入合同链接和抽取字段信息后会进行对应字段抽取
