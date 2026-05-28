# 授权信息

访问控制（RAM）是阿里云提供的管理用户身份与资源访问权限的服务。使用 RAM 可以让您避免与其他用户共享阿里云账号密钥，并可按需为用户授予最小权限。RAM 中使用权限策略描述授权的具体内容。

本文为您介绍 _大模型服务平台百炼_ 为 RAM 权限策略定义的操作（Action）、资源（Resource）和条件（Condition）。 _大模型服务平台百炼_ 的 RAM 代码（RamCode）为 _dianjin_ ，支持的授权粒度为 _操作级_ 。

## 权限策略通用结构

权限策略支持 JSON 格式，其通用结构如下：

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
    
-   Resource：受操作影响的具体对象，您可以使用资源 ARN 来描述指定资源。具体信息，请参见[资源（Resource）](#title-auth-detail-3)。
    
-   Condition：指授权生效的条件。可选字段。具体信息，请参见[条件（Condition）](#title-auth-detail-4)。
    
    -   Condition\_operator：条件运算符，不同类型的条件对应不同的条件运算符。具体信息，请参见[权限策略基本元素](https://help.aliyun.com/zh/ram/policy-elements)。
        
    -   Condition\_key：条件关键字。
        
    -   Condition\_value：条件关键字对应的值。
        

## 操作（Action）

下表是_大模型服务平台百炼_定义的操作，这些操作可以在 RAM 权限策略语句的`Action`元素中使用，用来授予执行该操作的权限。下面对表中的具体项提供说明：

-   操作：是指具体的权限点。
    
-   API：是指操作对应的 API 接口。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
        
    -   对于不支持资源级授权的操作，用`全部资源`表示。
        
-   条件关键字：是指云产品自身定义的条件关键字。该列不体现适用于任何操作的[通用条件关键字](https://help.aliyun.com/zh/ram/policy-elements)。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

**操作**

**API**

**访问级别**

**资源类型**

**条件关键字**

**关联操作**

dianjin:CreatePredefinedDocument

[CreatePredefinedDocument](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-createpredefineddocument)

create

\*全部资源

`*****`

无

无

dianjin:CreateLibrary

[CreateLibrary](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-createlibrary)

create

\*全部资源

`*****`

无

无

dianjin:CreateAnnualDocSummaryTask

[CreateAnnualDocSummaryTask](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-createannualdocsummarytask)

create

\*全部资源

`*****`

无

无

dianjin:GetParseResult

[GetParseResult](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getparseresult)

none

\*全部资源

`*****`

无

无

dianjin:GetDialogLog

[GetDialogLog](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getdialoglog)

none

\*全部资源

`*****`

无

无

dianjin:CreateFinReportSummaryTask

[CreateFinReportSummaryTask](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-createfinreportsummarytask)

create

\*全部资源

`*****`

无

无

dianjin:GetFilterDocumentList

[GetFilterDocumentList](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getfilterdocumentlist)

none

\*全部资源

`*****`

无

无

dianjin:GetDocumentList

[GetDocumentList](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getdocumentlist)

get

\*全部资源

`*****`

无

无

dianjin:EndToEndRealTimeDialog

[EndToEndRealTimeDialog](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-endtoendrealtimedialog)

none

\*全部资源

`*****`

无

无

dianjin:GetChatQuestionResp

[GetChatQuestionResp](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getchatquestionresp)

none

\*全部资源

`*****`

无

无

dianjin:UpdateDocumentChunk

[UpdateDocumentChunk](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-updatedocumentchunk)

update

\*全部资源

`*****`

无

无

dianjin:GetHistoryListByBizType

[GetHistoryListByBizType](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-gethistorylistbybiztype)

get

\*全部资源

`*****`

无

无

dianjin:DeleteDocument

[DeleteDocument](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-deletedocument)

none

\*全部资源

`*****`

无

无

dianjin:RebuildTask

[RebuildTask](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-rebuildtask)

none

\*全部资源

`*****`

无

无

dianjin:RecognizeIntention

[RecognizeIntention](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-recognizeintention)

none

\*全部资源

`*****`

无

无

dianjin:RealtimeDialogAssist

[RealtimeDialogAssist](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-realtimedialogassist)

none

\*全部资源

`*****`

无

无

dianjin:RunDialogAnalysis

[RunDialogAnalysis](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-rundialoganalysis)

none

\*全部资源

`*****`

无

无

dianjin:GenDocQaResult

[GenDocQaResult](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-gendocqaresult)

create

\*全部资源

`*****`

无

无

dianjin:RunLibraryChatGeneration

[RunLibraryChatGeneration](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-runlibrarychatgeneration)

none

\*全部资源

`*****`

无

无

dianjin:CreateDocsSummaryTask

[CreateDocsSummaryTask](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-createdocssummarytask)

create

\*全部资源

`*****`

无

无

dianjin:DashscopeAsyncTaskFinishEvent

[DashscopeAsyncTaskFinishEvent](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-dashscopeasynctaskfinishevent)

none

\*全部资源

`*****`

无

无

dianjin:RecallDocument

[RecallDocument](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-recalldocument)

none

\*全部资源

`*****`

无

无

dianjin:GetSummaryTaskResult

[GetSummaryTaskResult](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getsummarytaskresult)

get

\*全部资源

`*****`

无

无

dianjin:GetAppConfig

[GetAppConfig](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getappconfig)

get

\*全部资源

`*****`

无

无

dianjin:CreateDialogAnalysisTask

[CreateDialogAnalysisTask](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-createdialoganalysistask)

create

\*全部资源

`*****`

无

无

dianjin:RunChatResultGeneration

[RunChatResultGeneration](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-runchatresultgeneration)

none

\*全部资源

`*****`

无

无

dianjin:GetTaskResult

[GetTaskResult](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-gettaskresult)

get

\*全部资源

`*****`

无

无

dianjin:CreateQualityCheckTask

[CreateQualityCheckTask](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-createqualitychecktask)

create

\*全部资源

`*****`

无

无

dianjin:RealTimeDialog

[RealTimeDialog](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-realtimedialog)

none

\*全部资源

`*****`

无

无

dianjin:UploadDocument

[UploadDocument](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-uploaddocument)

none

\*全部资源

`*****`

无

无

dianjin:ReIndex

[ReIndex](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-reindex)

none

\*全部资源

`*****`

无

无

dianjin:GetLibrary

[GetLibrary](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getlibrary)

get

\*全部资源

`*****`

无

无

dianjin:GetDialogAnalysisResult

[GetDialogAnalysisResult](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getdialoganalysisresult)

none

\*全部资源

`*****`

无

无

dianjin:CreatePdfTranslateTask

[CreatePdfTranslateTask](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-createpdftranslatetask)

create

\*全部资源

`*****`

无

无

dianjin:UpdateDocument

[UpdateDocument](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-updatedocument)

none

\*全部资源

`*****`

无

无

dianjin:GetLibraryList

[GetLibraryList](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getlibrarylist)

get

\*全部资源

`*****`

无

无

dianjin:GetDocumentUrl

[GetDocumentUrl](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getdocumenturl)

get

\*全部资源

`*****`

无

无

dianjin:GetTaskStatus

[GetTaskStatus](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-gettaskstatus)

get

\*全部资源

`*****`

无

无

dianjin:EvictTask

[EvictTask](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-evicttask)

none

\*全部资源

`*****`

无

无

dianjin:DeleteLibrary

[DeleteLibrary](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-deletelibrary)

delete

\*全部资源

`*****`

无

无

dianjin:SubmitChatQuestion

[SubmitChatQuestion](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-submitchatquestion)

none

\*全部资源

`*****`

无

无

dianjin:CreateDialog

[CreateDialog](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-createdialog)

create

\*全部资源

`*****`

无

无

dianjin:GetDialogDetail

[GetDialogDetail](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getdialogdetail)

get

\*全部资源

`*****`

无

无

dianjin:PreviewDocument

[PreviewDocument](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-previewdocument)

get

\*全部资源

`*****`

无

无

dianjin:GetDocumentChunkList

[GetDocumentChunkList](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getdocumentchunklist)

none

\*全部资源

`*****`

无

无

dianjin:RunAgent

[RunAgent](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-runagent)

none

\*全部资源

`*****`

无

无

dianjin:InvokePlugin

[InvokePlugin](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-invokeplugin)

none

\*全部资源

`*****`

无

无

dianjin:GetQualityCheckTaskResult

[GetQualityCheckTaskResult](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-getqualitychecktaskresult)

get

\*全部资源

`*****`

无

无

dianjin:UpdateLibrary

[UpdateLibrary](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-updatelibrary)

update

\*全部资源

`*****`

无

无

dianjin:UpdateQaLibrary

[UpdateQaLibrary](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-updateqalibrary)

create

\*全部资源

`*****`

无

无

## 资源（Resource）

下表是_大模型服务平台百炼_定义的资源，这些资源可以在 RAM 权限策略语句的`Resource`元素中使用，用来授予对该资源执行具体操作的权限。 其中，资源 ARN 是资源在阿里云上的唯一标识。具体说明如下：

-   `{#}`为变量标识，需要您替换为实际值。例如：`{#ramcode}`需要您替换为实际的云服务RAM代码。
    
-   `*`表示全部。例如：
    
    -   `{#resourceType}`为`*`时：表示全部资源。
        
    -   `{#regionId}`为`*`时：表示全部地域。
        
    -   `{#accountId}`为`*`时：表示全部阿里云账号。
        

资源类型

资源 ARN

## 条件（Condition）

_大模型服务平台百炼_未定义产品级别的条件关键字。如需查看适用于所有云产品的通用条件关键字，请参见[通用条件关键字](https://help.aliyun.com/zh/ram/policy-elements)。

## 相关操作

您可以创建自定义权限策略，并将权限策略授予 RAM 用户、RAM 用户组或 RAM 角色。具体操作如下：

-   [创建自定义权限策略](https://help.aliyun.com/zh/ram/create-a-custom-policy)
    
-   [为 RAM 用户授权](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-the-ram-user)
    
-   [为 RAM 用户组授权](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-a-ram-user-group)
    
-   [为 RAM 角色授权](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-a-ram-role)
