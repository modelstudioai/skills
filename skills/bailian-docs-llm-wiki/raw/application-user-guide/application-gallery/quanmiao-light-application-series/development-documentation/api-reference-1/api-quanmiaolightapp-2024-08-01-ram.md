# 授权信息

访问控制（RAM）是阿里云提供的管理用户身份与资源访问权限的服务。使用RAM可以让您避免与其他用户共享阿里云账号密钥，并可按需为用户授予最小权限。RAM中使用权限策略描述授权的具体内容。

本文为您介绍大模型服务平台百炼（QuanMiaoLightApp）为RAM权限策略定义的操作（Action）、资源（Resource）和条件（Condition）。大模型服务平台百炼（QuanMiaoLightApp）的RAM代码（RamCode）为 quanmiaolightapp，支持的授权粒度为操作级。

## 权限策略通用结构

权限策略支持JSON格式，其通用结构如下：

```
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "<Effect>",
      "Action": "<Action>",
      "Resource": "<Resource>",
      "Condition": {
        "<Condition_operator>": {
          "<Condition_key>": [
            "<Condition_value>"
          ]
        }
      }
    }
  ]
}
```

各字段含义如下：

-   Effect：权限策略效果。取值：Allow（允许）、Deny（拒绝）。
-   Action：授予允许或拒绝权限的具体操作。具体信息，请参见[操作（Action）](#title-auth-detail-2)。
-   Resource：受操作影响的具体对象，您可以使用资源ARN来描述指定资源。具体信息，请参见[资源（Resource）](#title-auth-detail-3)。
-   Condition：指授权生效的条件。可选字段。具体信息，请参见[条件（Condition）](#title-auth-detail-4)。
    -   Condition\_operator：条件运算符，不同类型的条件对应不同的条件运算符。具体信息，请参见[权限策略基本元素](https://help.aliyun.com/zh/ram/policy-elements)。
    -   Condition\_key：条件关键字。
    -   Condition\_value：条件关键字对应的值。

## 操作（Action）

下表是大模型服务平台百炼（QuanMiaoLightApp）定义的操作，这些操作可以在RAM权限策略语句的`Action`元素中使用，用来授予执行该操作的权限。下面对表中的具体项提供说明：

-   操作：是指具体的权限点。
-   API：是指操作对应的API接口。
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。该列不体现适用于任何操作的[通用条件关键字](https://help.aliyun.com/zh/ram/policy-elements)。
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。

操作

API

访问级别

资源类型

条件关键字

关联操作

quanmiaolightapp:CancelAsyncTask

[CancelAsyncTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-cancelasynctask)

create

\*全部资源

`*`

无

无

quanmiaolightapp:ExportAnalysisTagDetailByTaskId

[ExportAnalysisTagDetailByTaskId](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-exportanalysistagdetailbytaskid)

none

\*全部资源

`*`

无

无

quanmiaolightapp:GenerateBroadcastNews

[GenerateBroadcastNews](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-generatebroadcastnews)

none

\*全部资源

`*`

无

无

quanmiaolightapp:GenerateOutputFormat

[GenerateOutputFormat](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-generateoutputformat)

none

\*全部资源

`*`

无

无

quanmiaolightapp:GetEnterpriseVocAnalysisTask

[GetEnterpriseVocAnalysisTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-getenterprisevocanalysistask)

get

\*全部资源

`*`

无

无

quanmiaolightapp:GetEssayCorrectionTask

[GetEssayCorrectionTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-getessaycorrectiontask)

get

\*全部资源

`*`

无

无

quanmiaolightapp:GetFileContent

[GetFileContent](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-getfilecontent)

get

\*全部资源

`*`

无

无

quanmiaolightapp:GetTagMiningAnalysisTask

[GetTagMiningAnalysisTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-gettagmininganalysistask)

get

\*全部资源

`*`

无

无

quanmiaolightapp:GetVideoAnalysisConfig

[GetVideoAnalysisConfig](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-getvideoanalysisconfig)

get

\*全部资源

`*`

无

无

quanmiaolightapp:GetVideoAnalysisTask

[GetVideoAnalysisTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-getvideoanalysistask)

get

\*全部资源

`*`

无

无

quanmiaolightapp:GetVideoDetectShotConfig

[GetVideoDetectShotConfig](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-getvideodetectshotconfig)

get

\*全部资源

`*`

无

无

quanmiaolightapp:GetVideoDetectShotTask

[GetVideoDetectShotTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-getvideodetectshottask)

get

\*全部资源

`*`

无

无

quanmiaolightapp:HotNewsRecommend

[HotNewsRecommend](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-hotnewsrecommend)

create

\*全部资源

`*`

无

无

quanmiaolightapp:ListAnalysisTagDetailByTaskId

[ListAnalysisTagDetailByTaskId](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-listanalysistagdetailbytaskid)

list

\*全部资源

`*`

无

无

quanmiaolightapp:ListHotTopicSummaries

[ListHotTopicSummaries](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-listhottopicsummaries)

list

\*全部资源

`*`

无

无

quanmiaolightapp:RunEnterpriseVocAnalysis

[RunEnterpriseVocAnalysis](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runenterprisevocanalysis)

none

\*全部资源

`*`

无

无

quanmiaolightapp:RunEssayCorrection

[RunEssayCorrection](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runessaycorrection)

create

\*全部资源

`*`

无

无

quanmiaolightapp:RunHotTopicChat

[RunHotTopicChat](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runhottopicchat)

none

\*全部资源

`*`

无

无

quanmiaolightapp:RunHotTopicSummary

[RunHotTopicSummary](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runhottopicsummary)

none

\*全部资源

`*`

无

无

quanmiaolightapp:RunMarketingInformationExtract

[RunMarketingInformationExtract](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runmarketinginformationextract)

none

\*全部资源

`*`

无

无

quanmiaolightapp:RunMarketingInformationWriting

[RunMarketingInformationWriting](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runmarketinginformationwriting)

none

\*全部资源

`*`

无

无

quanmiaolightapp:RunNetworkContentAudit

[RunNetworkContentAudit](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runnetworkcontentaudit)

create

\*全部资源

`*`

无

无

quanmiaolightapp:RunOcrParse

[RunOcrParse](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runocrparse)

create

\*全部资源

`*`

无

无

quanmiaolightapp:RunScriptChat

[RunScriptChat](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runscriptchat)

none

\*全部资源

`*`

无

无

quanmiaolightapp:RunScriptContinue

[RunScriptContinue](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runscriptcontinue)

none

\*全部资源

`*`

无

无

quanmiaolightapp:RunScriptPlanning

[RunScriptPlanning](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runscriptplanning)

none

\*全部资源

`*`

无

无

quanmiaolightapp:RunScriptRefine

[RunScriptRefine](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runscriptrefine)

none

\*全部资源

`*`

无

无

quanmiaolightapp:RunStyleWriting

[RunStyleWriting](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runstylewriting)

none

\*全部资源

`*`

无

无

quanmiaolightapp:RunTagMiningAnalysis

[RunTagMiningAnalysis](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runtagmininganalysis)

create

\*全部资源

`*`

无

无

quanmiaolightapp:RunVideoAnalysis

[RunVideoAnalysis](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runvideoanalysis)

none

\*全部资源

`*`

无

无

quanmiaolightapp:RunVideoDetectShot

[RunVideoDetectShot](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runvideodetectshot)

none

\*全部资源

`*`

无

无

quanmiaolightapp:SubmitEnterpriseVocAnalysisTask

[SubmitEnterpriseVocAnalysisTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-submitenterprisevocanalysistask)

create

\*全部资源

`*`

无

无

quanmiaolightapp:SubmitEssayCorrectionTask

[SubmitEssayCorrectionTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-submitessaycorrectiontask)

create

\*全部资源

`*`

无

无

quanmiaolightapp:SubmitTagMiningAnalysisTask

[SubmitTagMiningAnalysisTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-submittagmininganalysistask)

create

\*全部资源

`*`

无

无

quanmiaolightapp:SubmitVideoAnalysisTask

[SubmitVideoAnalysisTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-submitvideoanalysistask)

create

\*全部资源

`*`

无

无

quanmiaolightapp:SubmitVideoDetectShotTask

[SubmitVideoDetectShotTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-submitvideodetectshottask)

create

\*全部资源

`*`

无

无

quanmiaolightapp:UpdateVideoAnalysisConfig

[UpdateVideoAnalysisConfig](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-updatevideoanalysisconfig)

update

\*全部资源

`*`

无

无

quanmiaolightapp:UpdateVideoAnalysisTask

[UpdateVideoAnalysisTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-updatevideoanalysistask)

update

\*全部资源

`*`

无

无

quanmiaolightapp:UpdateVideoAnalysisTasks

[UpdateVideoAnalysisTasks](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-updatevideoanalysistasks)

update

\*全部资源

`*`

无

无

quanmiaolightapp:UpdateVideoDetectShotConfig

[UpdateVideoDetectShotConfig](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-updatevideodetectshotconfig)

update

\*全部资源

`*`

无

无

quanmiaolightapp:UpdateVideoDetectShotTask

[UpdateVideoDetectShotTask](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-updatevideodetectshottask)

update

\*全部资源

`*`

无

无

## 资源（Resource）

大模型服务平台百炼（QuanMiaoLightApp）不支持在RAM权限策略语句的`Resource`中指定资源ARN。如果要允许对大模型服务平台百炼（QuanMiaoLightApp）的访问权限，请在策略语句中指定`"Resource": "*"`。

## 条件（Condition）

大模型服务平台百炼（QuanMiaoLightApp）未定义产品级别的条件关键字。如需查看适用于所有云产品的通用条件关键字，请参见[通用条件关键字](https://help.aliyun.com/zh/ram/policy-elements)。

## 相关操作

您可以创建自定义权限策略，并将权限策略授予RAM用户、RAM用户组或RAM角色。具体操作如下：

-   [创建自定义权限策略](https://help.aliyun.com/zh/ram/create-a-custom-policy)
-   [为RAM用户授权](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-the-ram-user)
-   [为RAM用户组授权](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-a-ram-user-group)
-   [为RAM角色授权](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-a-ram-role)
