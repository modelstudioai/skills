# API概览

## API标准及多语言预置SDK

本产品（`BailianVoiceBot/2025-01-01`）的OpenAPI采用[RPC](https://help.aliyun.com/zh/sdk/product-overview/v3-request-structure-and-signature)签名风格。我们已经为开发者封装了常见编程语言的SDK，开发者可通过[下载SDK](https://api.aliyun.com/api-tools/sdk/BailianVoiceBot?version=2025-01-01)直接调用本产品OpenAPI而无需关心技术细节。如果现有SDK不能满足使用需求，可通过签名机制进行自签名对接。由于自签名细节非常复杂，需花费 5个工作日左右。因此建议加入我们的服务钉钉群（147535001692），在专家指导下进行签名对接。

在使用API前，您需要准备好身份账号及访问密钥（AccessKey），才能有效通过客户端工具（SDK、CLI等）访问API。细节请参见[获取AccessKey](https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair)。

## 自定义签名场景

若您的业务场景有特殊需求，需通过自签名方式对接 API，建议优先咨询我们的技术支持团队（服务钉钉群：147535001692），获取专业指导以确保高效接入。

## 账号与安全准备

阿里云账号具备对所有资源的完全管理权限。一旦 AccessKey 泄露，所有相关资源都将面临未经授权访问的风险。为确保安全，建议创建一个仅具备 API 访问权限的[RAM用户](https://help.aliyun.com/zh/ram/user-guide/create-a-ram-user)并配置其 AccessKey，同时基于最小权限原则 (PoLP) 配置 RAM 策略。仅在明确需要阿里云账号权限的特定场景下，才使用阿里云账号。

## API目录

API

标题

API概述

[BridgeWebCall](raw/_short/api-bailianvoicebot-2025-01-01-bridgewebcall-37795e5ee7bec833.md)

软电话测试通话

创建软电话测试通话。

[GetDataChannelCredential](raw/_short/api-bailianvoicebot-2025-01-01-getdatachannelcre-3f8c5776277d7a23.md)

获取数据通道凭证

获取数据通道凭证。

[GenerateFileUploadParams](raw/_short/api-bailianvoicebot-2025-01-01-generatefileuploa-d5a33e5cb5280c76.md)

获取文件上传参数

获取文件上传信息

## MQ消息订阅配置

API

标题

API概述

[UpdateSubscription](raw/_short/api-bailianvoicebot-2025-01-01-updatesubscriptio-8e9caba4c721685c.md)

更新订阅信息

创建或更新MQ配置

[GetSubscription](raw/_short/api-bailianvoicebot-2025-01-01-getsubscription-a1c9e3358d612ee8.md)

获取消息订阅配置信息

获取MQ配置

[DisableSubscription](raw/_short/api-bailianvoicebot-2025-01-01-disablesubscripti-cac218cb10a616a1.md)

关闭消息订阅

禁用消息订阅

## 变量管理

API

标题

API概述

[DeleteVariable](raw/_short/api-bailianvoicebot-2025-01-01-deletevariable-7935f31cfa0085ad.md)

删除变量

删除变量

[ListVariable](raw/_short/api-bailianvoicebot-2025-01-01-listvariable-f0acbe83a3843d1c.md)

获取变量列表

获取变量列表

[UpdateVariable](raw/_short/api-bailianvoicebot-2025-01-01-updatevariable-bb35cf02f586f180.md)

更新变量

更新变量

[CreateVariable](raw/_short/api-bailianvoicebot-2025-01-01-createvariable-d3e3faf7f33ea6fb.md)

创建变量

创建变量

## 三方语音配置

API

标题

API概述

[ListVoiceEngines](raw/_short/api-bailianvoicebot-2025-01-01-listvoiceengines-3f15e9416fbdfc0f.md)

获取三方语音引擎列表

获取引擎列表

[UpdateVoiceAccessProfile](raw/_short/api-bailianvoicebot-2025-01-01-updatevoiceaccess-0c7fea2cfb2ad5e1.md)

更新三方语音配置

更新三方语音配置

[ListVoiceAccessProfile](raw/_short/api-bailianvoicebot-2025-01-01-listvoiceaccesspr-67ad6f3da20a802e.md)

获取三方语音配置列表

获取三方语音配置列表

[DeleteVoiceAccessProfile](raw/_short/api-bailianvoicebot-2025-01-01-deletevoiceaccess-9f083f89c756abc6.md)

删除三方语音配置

删除三方语音配置

[CreateVoiceAccessProfile](raw/_short/api-bailianvoicebot-2025-01-01-createvoiceaccess-c94d6e41368829a6.md)

创建三方语音配置

创建实例

## 热词管理

API

标题

API概述

[UpdateVocabulary](raw/_short/api-bailianvoicebot-2025-01-01-updatevocabulary-567d8cc1d56b0794.md)

更新热词

更新实例

[ListVocabulary](raw/_short/api-bailianvoicebot-2025-01-01-listvocabulary-a3b521e2a1a6af4d.md)

获取热词列表

获取实例详情

[ImportVocabulary](raw/_short/api-bailianvoicebot-2025-01-01-importvocabulary-39521d337359c277.md)

导入热词

导入热词

[GetVocabulary](raw/_short/api-bailianvoicebot-2025-01-01-getvocabulary-0a73462fa0907877.md)

获取热词信息

获取实例详情

[ExportVocabulary](raw/_short/api-bailianvoicebot-2025-01-01-exportvocabulary-a2ce6962b9cdaef0.md)

导出热词

导出热词

[DeleteVocabulary](raw/_short/api-bailianvoicebot-2025-01-01-deletevocabulary-73a9701e954438eb.md)

删除热词

删除场景

[CreateVocabulary](raw/_short/api-bailianvoicebot-2025-01-01-createvocabulary-f95a19ec03f73ae7.md)

创建热词

创建实例

## 克隆音管理

API

标题

API概述

[ListCloneVoiceModels](raw/_short/api-bailianvoicebot-2025-01-01-listclonevoicemod-992e6101ea18c859.md)

获取克隆音模型列表

获取克隆音色可用模型列表

[DeleteCloneVoice](raw/_short/api-bailianvoicebot-2025-01-01-deleteclonevoice-29fa811f10617d02.md)

删除克隆音

删除场景

[ListCloneVoice](raw/_short/api-bailianvoicebot-2025-01-01-listclonevoice-4a7f3a48e1e10e35.md)

获取克隆音列表

获取实例详情

[UpdateCloneVoice](raw/_short/api-bailianvoicebot-2025-01-01-updateclonevoice-a2604a4c84f78d58.md)

更新克隆音

更新实例

[CreateCloneVoice](raw/_short/api-bailianvoicebot-2025-01-01-createclonevoice-db8172ecb0209b4e.md)

创建克隆音

创建克隆音

## 应用管理

API

标题

API概述

[DeleteApplication](raw/_short/api-bailianvoicebot-2025-01-01-deleteapplication-32f15b15b4a87a3b.md)

删除语音机器人应用

删除应用

[ListNluModels](raw/_short/api-bailianvoicebot-2025-01-01-listnlumodels-cd00d62fde6d669f.md)

获取对话大模型列表

获取对话模型列表

[PreviewVoice](raw/_short/api-bailianvoicebot-2025-01-01-previewvoice-3f71cb671c8b280c.md)

TTS合成试听

试听

[ListBackgroundMusics](raw/_short/api-bailianvoicebot-2025-01-01-listbackgroundmus-ab3c945580a2d37c.md)

获取背景音列表

获取背景音列表

[ListVoices](raw/_short/api-bailianvoicebot-2025-01-01-listvoices-ed2b447066119e81.md)

获取音色列表

获取音色列表

[ListApplications](raw/_short/api-bailianvoicebot-2025-01-01-listapplications-96bf2b50f1086252.md)

查询语音机器人应用列表

查询语音机器人应用列表。

[CreateApplicationVersion](raw/_short/api-bailianvoicebot-2025-01-01-createapplication-7e3434b6ca481e25.md)

创建语音机器人应用版本

创建语音机器人应用版本。

[UpdateApplication](raw/_short/api-bailianvoicebot-2025-01-01-updateapplication-ff4f8f81036d8d71.md)

修改语音机器人应用

修改语音机器人应用。

[CreateApplication](raw/_short/api-bailianvoicebot-2025-01-01-createapplication-b08fef6abd22de35.md)

创建语音机器人应用

创建语音机器人应用。

[GetApplication](raw/_short/api-bailianvoicebot-2025-01-01-getapplication-a1a2f16d9168ee0f.md)

获取语音机器人应用

获取语音机器人应用。

[UpdateApplicationVersion](raw/_short/api-bailianvoicebot-2025-01-01-updateapplication-1da727b68ddf9d5a.md)

修改语音机器人应用版本

修改场景版本。

[PublishApplicationVersion](raw/_short/api-bailianvoicebot-2025-01-01-publishapplicatio-16edd467e4affffa.md)

发布语音机器人

发布语音机器人版本
