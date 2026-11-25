# API概览

<a id="api标准及多语言预置sdk"></a>

<a id="api-overview-tips-wrapper"></a>

## API标准及多语言预置SDK

本产品（`BailianVoiceBot/2025-01-01`）的OpenAPI采用[RPC](https://help.aliyun.com/zh/sdk/product-overview/v3-request-structure-and-signature)签名风格。我们已经为开发者封装了常见编程语言的SDK，开发者可通过[下载SDK](https://api.aliyun.com/api-tools/sdk/BailianVoiceBot?version=2025-01-01)直接调用本产品OpenAPI而无需关心技术细节。如果现有SDK不能满足使用需求，可通过签名机制进行自签名对接。由于自签名细节非常复杂，需花费 5个工作日左右。因此建议加入我们的服务钉钉群（147535001692），在专家指导下进行签名对接。

在使用API前，您需要准备好身份账号及访问密钥（AccessKey），才能有效通过客户端工具（SDK、CLI等）访问API。细节请参见[获取AccessKey](https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair)。

<a id="自定义签名场景"></a>

<a id="827da20f55ut1"></a>

## 自定义签名场景

若您的业务场景有特殊需求，需通过自签名方式对接 API，建议优先咨询我们的技术支持团队（服务钉钉群：147535001692），获取专业指导以确保高效接入。

<a id="账号与安全准备"></a>

<a id="f43f05eefcm13"></a>

## 账号与安全准备

阿里云账号具备对所有资源的完全管理权限。一旦 AccessKey 泄露，所有相关资源都将面临未经授权访问的风险。为确保安全，建议创建一个仅具备 API 访问权限的[RAM用户](https://help.aliyun.com/zh/ram/user-guide/create-a-ram-user)并配置其 AccessKey，同时基于最小权限原则 (PoLP) 配置 RAM 策略。仅在明确需要阿里云账号权限的特定场景下，才使用阿里云账号。

<a id="api目录"></a>

<a id="api-overview-table-section-header-5631945"></a>

## API目录

| API | 标题 | API概述 |
| --- | --- | --- |
| [BridgeWebCall](api-bailianvoicebot-2025-01-01-bridgewebcall-bf1bdc82d4be852a.md) | 软电话测试通话 | 创建软电话测试通话。 |
| [GetDataChannelCredential](api-bailianvoicebot-2025-01-01-getdatachannelcre-c91633cfe2d6898e.md) | 获取数据通道凭证 | 获取数据通道凭证。 |
| [GenerateFileUploadParams](api-bailianvoicebot-2025-01-01-generatefileuploa-7b5767898dfce792.md) | 获取文件上传参数 | 获取文件上传信息 |

<a id="mq消息订阅配置"></a>

<a id="api-overview-table-section-header-mqxiaoxidingyuepeizhi"></a>

## MQ消息订阅配置

| API | 标题 | API概述 |
| --- | --- | --- |
| [UpdateSubscription](api-bailianvoicebot-2025-01-01-updatesubscriptio-60509edb5ab772d9.md) | 更新订阅信息 | 创建或更新MQ配置 |
| [GetSubscription](api-bailianvoicebot-2025-01-01-getsubscription-bc2d89609963ed9f.md) | 获取消息订阅配置信息 | 获取MQ配置 |
| [DisableSubscription](api-bailianvoicebot-2025-01-01-disablesubscripti-f22896c4b14c0b95.md) | 关闭消息订阅 | 禁用消息订阅 |

<a id="变量管理"></a>

<a id="api-overview-table-section-header-bianliangguanli"></a>

## 变量管理

| API | 标题 | API概述 |
| --- | --- | --- |
| [DeleteVariable](api-bailianvoicebot-2025-01-01-deletevariable-7c5271aa15639a44.md) | 删除变量 | 删除变量 |
| [ListVariable](api-bailianvoicebot-2025-01-01-listvariable-462f64578d59af69.md) | 获取变量列表 | 获取变量列表 |
| [UpdateVariable](api-bailianvoicebot-2025-01-01-updatevariable-b80bd228277646f3.md) | 更新变量 | 更新变量 |
| [CreateVariable](api-bailianvoicebot-2025-01-01-createvariable-d1308d6ebe89c76f.md) | 创建变量 | 创建变量 |

<a id="三方语音配置"></a>

<a id="api-overview-table-section-header-sanfangyuyinpeizhi"></a>

## 三方语音配置

| API | 标题 | API概述 |
| --- | --- | --- |
| [ListVoiceEngines](api-bailianvoicebot-2025-01-01-listvoiceengines-98d143cebd47d7e8.md) | 获取三方语音引擎列表 | 获取引擎列表 |
| [UpdateVoiceAccessProfile](api-bailianvoicebot-2025-01-01-updatevoiceaccess-275b3f4aa3b62c8f.md) | 更新三方语音配置 | 更新三方语音配置 |
| [ListVoiceAccessProfile](api-bailianvoicebot-2025-01-01-listvoiceaccesspr-b2d8f87a2cf31303.md) | 获取三方语音配置列表 | 获取三方语音配置列表 |
| [DeleteVoiceAccessProfile](api-bailianvoicebot-2025-01-01-deletevoiceaccess-0720f5024c08aaff.md) | 删除三方语音配置 | 删除三方语音配置 |
| [CreateVoiceAccessProfile](api-bailianvoicebot-2025-01-01-createvoiceaccess-15fc791559669311.md) | 创建三方语音配置 | 创建实例 |

<a id="热词管理"></a>

<a id="api-overview-table-section-header-reciguanli"></a>

## 热词管理

| API | 标题 | API概述 |
| --- | --- | --- |
| [UpdateVocabulary](api-bailianvoicebot-2025-01-01-updatevocabulary-87dfb4e4e91641d5.md) | 更新热词 | 更新实例 |
| [ListVocabulary](api-bailianvoicebot-2025-01-01-listvocabulary-01d0a1445904e554.md) | 获取热词列表 | 获取实例详情 |
| [ImportVocabulary](api-bailianvoicebot-2025-01-01-importvocabulary-3077594317ee2467.md) | 导入热词 | 导入热词 |
| [GetVocabulary](api-bailianvoicebot-2025-01-01-getvocabulary-fe02b4db6537645d.md) | 获取热词信息 | 获取实例详情 |
| [ExportVocabulary](api-bailianvoicebot-2025-01-01-exportvocabulary-b749fae412983446.md) | 导出热词 | 导出热词 |
| [DeleteVocabulary](api-bailianvoicebot-2025-01-01-deletevocabulary-997e231c7b3790ec.md) | 删除热词 | 删除场景 |
| [CreateVocabulary](api-bailianvoicebot-2025-01-01-createvocabulary-3e19496a7be85c91.md) | 创建热词 | 创建实例 |

<a id="克隆音管理"></a>

<a id="api-overview-table-section-header-kelongyinguanli"></a>

## 克隆音管理

| API | 标题 | API概述 |
| --- | --- | --- |
| [ListCloneVoiceModels](api-bailianvoicebot-2025-01-01-listclonevoicemod-266c15dd2f6bef8e.md) | 获取克隆音模型列表 | 获取克隆音色可用模型列表 |
| [DeleteCloneVoice](api-bailianvoicebot-2025-01-01-deleteclonevoice-727cffde29a328a2.md) | 删除克隆音 | 删除场景 |
| [ListCloneVoice](api-bailianvoicebot-2025-01-01-listclonevoice-b52c319e14d63ca5.md) | 获取克隆音列表 | 获取实例详情 |
| [UpdateCloneVoice](api-bailianvoicebot-2025-01-01-updateclonevoice-0e5b3e30598f9fba.md) | 更新克隆音 | 更新实例 |
| [CreateCloneVoice](api-bailianvoicebot-2025-01-01-createclonevoice-7b39a48a8f79b3b1.md) | 创建克隆音 | 创建克隆音 |

<a id="应用管理"></a>

<a id="api-overview-table-section-header-yingyongguanli"></a>

## 应用管理

| API | 标题 | API概述 |
| --- | --- | --- |
| [DeleteApplication](api-bailianvoicebot-2025-01-01-deleteapplication-9b84e9b87fd151d3.md) | 删除语音机器人应用 | 删除应用 |
| [ListNluModels](api-bailianvoicebot-2025-01-01-listnlumodels-3666b64a51e391c7.md) | 获取对话大模型列表 | 获取对话模型列表 |
| [PreviewVoice](api-bailianvoicebot-2025-01-01-previewvoice-3dde56b04f55b657.md) | TTS合成试听 | 试听 |
| [ListBackgroundMusics](api-bailianvoicebot-2025-01-01-listbackgroundmus-fe993b4c2242eae6.md) | 获取背景音列表 | 获取背景音列表 |
| [ListVoices](api-bailianvoicebot-2025-01-01-listvoices-e1924082f3684eeb.md) | 获取音色列表 | 获取音色列表 |
| [ListApplications](api-bailianvoicebot-2025-01-01-listapplications-4a71f51cfc7fc8ed.md) | 查询语音机器人应用列表 | 查询语音机器人应用列表。 |
| [CreateApplicationVersion](api-bailianvoicebot-2025-01-01-createapplication-0010e1d19b940395.md) | 创建语音机器人应用版本 | 创建语音机器人应用版本。 |
| [UpdateApplication](api-bailianvoicebot-2025-01-01-updateapplication-b5590f3e1b8177a1.md) | 修改语音机器人应用 | 修改语音机器人应用。 |
| [CreateApplication](api-bailianvoicebot-2025-01-01-createapplication-accebf2655f77566.md) | 创建语音机器人应用 | 创建语音机器人应用。 |
| [GetApplication](api-bailianvoicebot-2025-01-01-getapplication-ed15e755cb168597.md) | 获取语音机器人应用 | 获取语音机器人应用。 |
| [UpdateApplicationVersion](api-bailianvoicebot-2025-01-01-updateapplication-396d3974205b9979.md) | 修改语音机器人应用版本 | 修改场景版本。 |
| [PublishApplicationVersion](api-bailianvoicebot-2025-01-01-publishapplicatio-5650857b5047bf77.md) | 发布语音机器人 | 发布语音机器人版本 |
