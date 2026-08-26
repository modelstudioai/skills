# 授权信息

访问控制（RAM）是阿里云提供的管理用户身份与资源访问权限的服务。使用 RAM 可以让您避免与其他用户共享阿里云账号密钥，并可按需为用户授予最小权限。RAM 中使用权限策略描述授权的具体内容。

本文为您介绍_大模型服务平台百炼_为 RAM 权限策略定义的操作（Action）、资源（Resource）和条件（Condition）。_大模型服务平台百炼_的 RAM 代码（RamCode）为_dianjin_，支持的授权粒度为_操作级_。

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
    
-   Action：授予允许或拒绝权限的具体操作。具体信息，请参见[操作（Action）](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-ram#title-auth-detail-2)。
    
-   Resource：受操作影响的具体对象，您可以使用资源 ARN 来描述指定资源。具体信息，请参见[资源（Resource）](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-ram#title-auth-detail-3)。
    
-   Condition：指授权生效的条件。可选字段。具体信息，请参见[条件（Condition）](https://help.aliyun.com/zh/model-studio/api-dianjin-2024-06-28-ram#title-auth-detail-4)。
    
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

dianjin:GetHistoryListByBizType

[GetHistoryListByBizType](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-gethistorylistbybiztype.md)

get

\*全部资源

`*`

无

无

dianjin:DeleteLibrary

[DeleteLibrary](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-deletelibrary.md)

delete

\*全部资源

`*`

无

无

dianjin:ReIndex

[ReIndex](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-reindex.md)

none

\*全部资源

`*`

无

无

dianjin:GetTaskStatus

[GetTaskStatus](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-gettaskstatus.md)

get

\*全部资源

`*`

无

无

dianjin:RealtimeDialogAssist

[RealtimeDialogAssist](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-realtimedialogassist.md)

none

\*全部资源

`*`

无

无

dianjin:GetDocumentUrl

[GetDocumentUrl](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-getdocumenturl.md)

get

\*全部资源

`*`

无

无

dianjin:GetQualityCheckTaskResult

[GetQualityCheckTaskResult](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-getqualitychecktaskresult.md)

get

\*全部资源

`*`

无

无

dianjin:RunLibraryChatGeneration

[RunLibraryChatGeneration](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-runlibrarychatgeneration.md)

none

\*全部资源

`*`

无

无

dianjin:GetLibrary

[GetLibrary](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-getlibrary.md)

get

\*全部资源

`*`

无

无

dianjin:InvokePlugin

[InvokePlugin](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-invokeplugin.md)

none

\*全部资源

`*`

无

无

dianjin:GetDialogLog

[GetDialogLog](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-getdialoglog.md)

none

\*全部资源

`*`

无

无

dianjin:CreateFinReportSummaryTask

[CreateFinReportSummaryTask](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-createfinreportsummarytask.md)

create

\*全部资源

`*`

无

无

dianjin:GetTaskResult

[GetTaskResult](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-gettaskresult.md)

get

\*全部资源

`*`

无

无

dianjin:RecognizeIntention

[RecognizeIntention](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-recognizeintention.md)

none

\*全部资源

`*`

无

无

dianjin:SubmitChatQuestion

[SubmitChatQuestion](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-submitchatquestion.md)

none

\*全部资源

`*`

无

无

dianjin:CreateDocsSummaryTask

[CreateDocsSummaryTask](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-createdocssummarytask.md)

create

\*全部资源

`*`

无

无

dianjin:RunAgent

[RunAgent](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-runagent.md)

none

\*全部资源

`*`

无

无

dianjin:RebuildTask

[RebuildTask](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-rebuildtask.md)

none

\*全部资源

`*`

无

无

dianjin:GetParseResult

[GetParseResult](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-getparseresult.md)

none

\*全部资源

`*`

无

无

dianjin:UpdateLibrary

[UpdateLibrary](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-updatelibrary.md)

update

\*全部资源

`*`

无

无

dianjin:UpdateDocumentChunk

[UpdateDocumentChunk](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-updatedocumentchunk.md)

update

\*全部资源

`*`

无

无

dianjin:PreviewDocument

[PreviewDocument](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-previewdocument.md)

get

\*全部资源

`*`

无

无

dianjin:CreateDialogAnalysisTask

[CreateDialogAnalysisTask](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-createdialoganalysistask.md)

create

\*全部资源

`*`

无

无

dianjin:CreateLibrary

[CreateLibrary](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-createlibrary.md)

create

\*全部资源

`*`

无

无

dianjin:GetDialogDetail

[GetDialogDetail](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-getdialogdetail.md)

get

\*全部资源

`*`

无

无

dianjin:RealTimeDialog

[RealTimeDialog](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-realtimedialog.md)

none

\*全部资源

`*`

无

无

dianjin:GetAppConfig

[GetAppConfig](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-getappconfig.md)

get

\*全部资源

`*`

无

无

dianjin:DeleteDocument

[DeleteDocument](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-deletedocument.md)

none

\*全部资源

`*`

无

无

dianjin:EvictTask

[EvictTask](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-evicttask.md)

none

\*全部资源

`*`

无

无

dianjin:UpdateDocument

[UpdateDocument](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-updatedocument.md)

none

\*全部资源

`*`

无

无

dianjin:CreatePredefinedDocument

[CreatePredefinedDocument](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-createpredefineddocument.md)

create

\*全部资源

`*`

无

无

dianjin:GetDocumentChunkList

[GetDocumentChunkList](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-getdocumentchunklist.md)

none

\*全部资源

`*`

无

无

dianjin:GetSummaryTaskResult

[GetSummaryTaskResult](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-getsummarytaskresult.md)

get

\*全部资源

`*`

无

无

dianjin:RecallDocument

[RecallDocument](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-recalldocument.md)

none

\*全部资源

`*`

无

无

dianjin:GetDialogAnalysisResult

[GetDialogAnalysisResult](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-getdialoganalysisresult.md)

none

\*全部资源

`*`

无

无

dianjin:GenDocQaResult

[GenDocQaResult](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-gendocqaresult.md)

create

\*全部资源

`*`

无

无

dianjin:GetDocumentList

[GetDocumentList](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-getdocumentlist.md)

get

\*全部资源

`*`

无

无

dianjin:EndToEndRealTimeDialog

[EndToEndRealTimeDialog](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-endtoendrealtimedialog.md)

none

\*全部资源

`*`

无

无

dianjin:CreateDialog

[CreateDialog](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-createdialog.md)

create

\*全部资源

`*`

无

无

dianjin:DashscopeAsyncTaskFinishEvent

[DashscopeAsyncTaskFinishEvent](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-other/api-dianjin-2024-06-28-dashscopeasynctaskfinishevent.md)

none

\*全部资源

`*`

无

无

dianjin:CreateQualityCheckTask

[CreateQualityCheckTask](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-createqualitychecktask.md)

create

\*全部资源

`*`

无

无

dianjin:GetLibraryList

[GetLibraryList](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-getlibrarylist.md)

get

\*全部资源

`*`

无

无

dianjin:GetFilterDocumentList

[GetFilterDocumentList](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-getfilterdocumentlist.md)

none

\*全部资源

`*`

无

无

dianjin:GetChatQuestionResp

[GetChatQuestionResp](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-getchatquestionresp.md)

none

\*全部资源

`*`

无

无

dianjin:RunDialogAnalysis

[RunDialogAnalysis](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-rundialoganalysis.md)

none

\*全部资源

`*`

无

无

dianjin:CreatePdfTranslateTask

[CreatePdfTranslateTask](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-createpdftranslatetask.md)

create

\*全部资源

`*`

无

无

dianjin:UpdateQaLibrary

[UpdateQaLibrary](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-updateqalibrary.md)

create

\*全部资源

`*`

无

无

dianjin:RunChatResultGeneration

[RunChatResultGeneration](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-runchatresultgeneration.md)

none

\*全部资源

`*`

无

无

dianjin:CreateAnnualDocSummaryTask

[CreateAnnualDocSummaryTask](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-application/api-dianjin-2024-06-28-createannualdocsummarytask.md)

create

\*全部资源

`*`

无

无

dianjin:UploadDocument

[UploadDocument](raw/application-user-guide/application-gallery/tongyi-dianjin/api-reference-3/api-dianjin-2024-06-28-dir/api-dianjin-2024-06-28-dir-platform-capabilities-document-library/api-dianjin-2024-06-28-uploaddocument.md)

none

\*全部资源

`*`

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
