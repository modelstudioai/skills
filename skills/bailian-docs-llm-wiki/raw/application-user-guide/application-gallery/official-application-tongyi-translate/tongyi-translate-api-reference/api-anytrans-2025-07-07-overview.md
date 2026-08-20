# API概览

## API标准及多语言预置SDK

本产品（`AnyTrans/2025-07-07`）的OpenAPI采用ROA签名风格。我们已经为开发者封装了常见编程语言的SDK，开发者可通过[下载SDK](https://api.aliyun.com/api-tools/sdk/AnyTrans?version=2025-07-07)直接调用本产品OpenAPI而无需关心技术细节。如果现有SDK不能满足使用需求，可通过签名机制进行自签名对接。由于自签名细节非常复杂，需花费 5个工作日左右。因此建议加入我们的服务钉钉群（147535001692），在专家指导下进行签名对接。

在使用API前，您需要准备好身份账号及访问密钥（AccessKey），才能有效通过客户端工具（SDK、CLI等）访问API。细节请参见获取AccessKey。

## 自定义签名场景

若您的业务场景有特殊需求，需通过自签名方式对接 API，建议优先咨询我们的技术支持团队（服务钉钉群：147535001692），获取专业指导以确保高效接入。

## 账号与安全准备

阿里云账号具备对所有资源的完全管理权限。一旦 AccessKey 泄露，所有相关资源都将面临未经授权访问的风险。为确保安全，建议创建一个仅具备 API 访问权限的RAM用户并配置其 AccessKey，同时基于最小权限原则 (PoLP) 配置 RAM 策略。仅在明确需要阿里云账号权限的特定场景下，才使用阿里云账号。

## 文本翻译

API

标题

API概述

[TextTranslate](raw/application-user-guide/application-gallery/official-application-tongyi-translate/tongyi-translate-api-reference/api-anytrans-2025-07-07-dir/api-anytrans-2025-07-07-dir-text-translation/api-anytrans-2025-07-07-texttranslate.md)

文本翻译接口

通义多模态翻译文本翻译

[BatchTranslate](raw/application-user-guide/application-gallery/official-application-tongyi-translate/tongyi-translate-api-reference/api-anytrans-2025-07-07-dir/api-anytrans-2025-07-07-dir-text-translation/api-anytrans-2025-07-07-batchtranslate.md)

批量文本翻译

通义多模态翻译批量翻译

[SubmitLongTextTranslateTask](raw/application-user-guide/application-gallery/official-application-tongyi-translate/tongyi-translate-api-reference/api-anytrans-2025-07-07-dir/api-anytrans-2025-07-07-dir-text-translation/api-anytrans-2025-07-07-submitlongtexttranslatetask.md)

提交长文本翻译任务

通义多模态翻译提交长文翻译任务

[GetLongTextTranslateTask](raw/application-user-guide/application-gallery/official-application-tongyi-translate/tongyi-translate-api-reference/api-anytrans-2025-07-07-dir/api-anytrans-2025-07-07-dir-text-translation/api-anytrans-2025-07-07-getlongtexttranslatetask.md)

获取长文本翻译任务结果

通义多模态翻译获取长文翻译结果

[SubmitHtmlTranslateTask](raw/application-user-guide/application-gallery/official-application-tongyi-translate/tongyi-translate-api-reference/api-anytrans-2025-07-07-dir/api-anytrans-2025-07-07-dir-text-translation/api-anytrans-2025-07-07-submithtmltranslatetask.md)

提交html翻译任务

通义多模态翻译提交html翻译任务

[GetHtmlTranslateTask](raw/application-user-guide/application-gallery/official-application-tongyi-translate/tongyi-translate-api-reference/api-anytrans-2025-07-07-dir/api-anytrans-2025-07-07-dir-text-translation/api-anytrans-2025-07-07-gethtmltranslatetask.md)

获取html翻译任务结果

通义多模态翻译获取html翻译结果

[TermEdit](raw/application-user-guide/application-gallery/official-application-tongyi-translate/tongyi-translate-api-reference/api-anytrans-2025-07-07-dir/api-anytrans-2025-07-07-dir-text-translation/api-anytrans-2025-07-07-termedit.md)

术语库编辑

通义多模态翻译术语库编辑

[TermQuery](raw/application-user-guide/application-gallery/official-application-tongyi-translate/tongyi-translate-api-reference/api-anytrans-2025-07-07-dir/api-anytrans-2025-07-07-dir-text-translation/api-anytrans-2025-07-07-termquery.md)

术语库查询

通义多模态翻译术语库查询

## 图片翻译

API

标题

API概述

[GetImageTranslateTask](raw/application-user-guide/application-gallery/official-application-tongyi-translate/tongyi-translate-api-reference/api-anytrans-2025-07-07-dir/api-anytrans-2025-07-07-dir-image-translation/api-anytrans-2025-07-07-getimagetranslatetask.md)

获取图片翻译任务结果

通义多模态翻译获取图片翻译结果

[SubmitImageTranslateTask](raw/application-user-guide/application-gallery/official-application-tongyi-translate/tongyi-translate-api-reference/api-anytrans-2025-07-07-dir/api-anytrans-2025-07-07-dir-image-translation/api-anytrans-2025-07-07-submitimagetranslatetask.md)

提交图片翻译任务

通义多模态翻译提交图片翻译任务

## 文档翻译

API

标题

API概述

[SubmitDocTranslateTask](raw/application-user-guide/application-gallery/official-application-tongyi-translate/tongyi-translate-api-reference/api-anytrans-2025-07-07-dir/api-anytrans-2025-07-07-dir-document-translation/api-anytrans-2025-07-07-submitdoctranslatetask.md)

文档翻译任务提交

通义多模态翻译提交文档翻译任务。

[GetDocTranslateTask](raw/application-user-guide/application-gallery/official-application-tongyi-translate/tongyi-translate-api-reference/api-anytrans-2025-07-07-dir/api-anytrans-2025-07-07-dir-document-translation/api-anytrans-2025-07-07-getdoctranslatetask.md)

文档翻译结果获取

通义多模态翻译获取文档翻译结果
