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

[GetHistoryListByBizType](raw/_short/api-dianjin-2024-06-28-gethistorylistbybiztype-094e0fd700f60449.md)

get

\*全部资源

`*`

无

无

dianjin:DeleteLibrary

[DeleteLibrary](raw/_short/api-dianjin-2024-06-28-deletelibrary-1014340b912e1802.md)

delete

\*全部资源

`*`

无

无

dianjin:ReIndex

[ReIndex](raw/_short/api-dianjin-2024-06-28-reindex-b253554c9c087004.md)

none

\*全部资源

`*`

无

无

dianjin:GetTaskStatus

[GetTaskStatus](raw/_short/api-dianjin-2024-06-28-gettaskstatus-d3b9b23ec42792e0.md)

get

\*全部资源

`*`

无

无

dianjin:RealtimeDialogAssist

[RealtimeDialogAssist](raw/_short/api-dianjin-2024-06-28-realtimedialogassist-e263257cf24e3127.md)

none

\*全部资源

`*`

无

无

dianjin:GetDocumentUrl

[GetDocumentUrl](raw/_short/api-dianjin-2024-06-28-getdocumenturl-ef124c074d6ab9fa.md)

get

\*全部资源

`*`

无

无

dianjin:GetQualityCheckTaskResult

[GetQualityCheckTaskResult](raw/_short/api-dianjin-2024-06-28-getqualitychecktaskresult-6b221fa3c50b4bf2.md)

get

\*全部资源

`*`

无

无

dianjin:RunLibraryChatGeneration

[RunLibraryChatGeneration](raw/_short/api-dianjin-2024-06-28-runlibrarychatgeneration-404dfc22be5a54b0.md)

none

\*全部资源

`*`

无

无

dianjin:GetLibrary

[GetLibrary](raw/_short/api-dianjin-2024-06-28-getlibrary-fa28d970d73cf944.md)

get

\*全部资源

`*`

无

无

dianjin:InvokePlugin

[InvokePlugin](raw/_short/api-dianjin-2024-06-28-invokeplugin-1dad02a60f565377.md)

none

\*全部资源

`*`

无

无

dianjin:GetDialogLog

[GetDialogLog](raw/_short/api-dianjin-2024-06-28-getdialoglog-853687666dc3cba7.md)

none

\*全部资源

`*`

无

无

dianjin:CreateFinReportSummaryTask

[CreateFinReportSummaryTask](raw/_short/api-dianjin-2024-06-28-createfinreportsummarytas-6c944687f50f0e0d.md)

create

\*全部资源

`*`

无

无

dianjin:GetTaskResult

[GetTaskResult](raw/_short/api-dianjin-2024-06-28-gettaskresult-e502eaecf467735d.md)

get

\*全部资源

`*`

无

无

dianjin:RecognizeIntention

[RecognizeIntention](raw/_short/api-dianjin-2024-06-28-recognizeintention-cbc3739e363b12fe.md)

none

\*全部资源

`*`

无

无

dianjin:SubmitChatQuestion

[SubmitChatQuestion](raw/_short/api-dianjin-2024-06-28-submitchatquestion-33eb2d3583fa7d91.md)

none

\*全部资源

`*`

无

无

dianjin:CreateDocsSummaryTask

[CreateDocsSummaryTask](raw/_short/api-dianjin-2024-06-28-createdocssummarytask-ebf0276013590879.md)

create

\*全部资源

`*`

无

无

dianjin:RunAgent

[RunAgent](raw/_short/api-dianjin-2024-06-28-runagent-5da99dfbb5ebb6fc.md)

none

\*全部资源

`*`

无

无

dianjin:RebuildTask

[RebuildTask](raw/_short/api-dianjin-2024-06-28-rebuildtask-a8b4ee41523ac3fb.md)

none

\*全部资源

`*`

无

无

dianjin:GetParseResult

[GetParseResult](raw/_short/api-dianjin-2024-06-28-getparseresult-cee7e355a6d23912.md)

none

\*全部资源

`*`

无

无

dianjin:UpdateLibrary

[UpdateLibrary](raw/_short/api-dianjin-2024-06-28-updatelibrary-0a0d6db97e2d3487.md)

update

\*全部资源

`*`

无

无

dianjin:UpdateDocumentChunk

[UpdateDocumentChunk](raw/_short/api-dianjin-2024-06-28-updatedocumentchunk-aa1fa6c9fe4c2618.md)

update

\*全部资源

`*`

无

无

dianjin:PreviewDocument

[PreviewDocument](raw/_short/api-dianjin-2024-06-28-previewdocument-8c55690988faecdd.md)

get

\*全部资源

`*`

无

无

dianjin:CreateDialogAnalysisTask

[CreateDialogAnalysisTask](raw/_short/api-dianjin-2024-06-28-createdialoganalysistask-28fef79b887624dd.md)

create

\*全部资源

`*`

无

无

dianjin:CreateLibrary

[CreateLibrary](raw/_short/api-dianjin-2024-06-28-createlibrary-41e580c81262aa83.md)

create

\*全部资源

`*`

无

无

dianjin:GetDialogDetail

[GetDialogDetail](raw/_short/api-dianjin-2024-06-28-getdialogdetail-6dfcf43438066b60.md)

get

\*全部资源

`*`

无

无

dianjin:RealTimeDialog

[RealTimeDialog](raw/_short/api-dianjin-2024-06-28-realtimedialog-1724ffb10bd69761.md)

none

\*全部资源

`*`

无

无

dianjin:GetAppConfig

[GetAppConfig](raw/_short/api-dianjin-2024-06-28-getappconfig-493fe5a694a1cdc0.md)

get

\*全部资源

`*`

无

无

dianjin:DeleteDocument

[DeleteDocument](raw/_short/api-dianjin-2024-06-28-deletedocument-53502bae8139481f.md)

none

\*全部资源

`*`

无

无

dianjin:EvictTask

[EvictTask](raw/_short/api-dianjin-2024-06-28-evicttask-11939924bb8c12d1.md)

none

\*全部资源

`*`

无

无

dianjin:UpdateDocument

[UpdateDocument](raw/_short/api-dianjin-2024-06-28-updatedocument-62af14b3aafbd006.md)

none

\*全部资源

`*`

无

无

dianjin:CreatePredefinedDocument

[CreatePredefinedDocument](raw/_short/api-dianjin-2024-06-28-createpredefineddocument-a6dc0f48fd9f94f3.md)

create

\*全部资源

`*`

无

无

dianjin:GetDocumentChunkList

[GetDocumentChunkList](raw/_short/api-dianjin-2024-06-28-getdocumentchunklist-d16101f8854a50e4.md)

none

\*全部资源

`*`

无

无

dianjin:GetSummaryTaskResult

[GetSummaryTaskResult](raw/_short/api-dianjin-2024-06-28-getsummarytaskresult-baf9b62231f3fc7d.md)

get

\*全部资源

`*`

无

无

dianjin:RecallDocument

[RecallDocument](raw/_short/api-dianjin-2024-06-28-recalldocument-1ab8ab89e9dcd579.md)

none

\*全部资源

`*`

无

无

dianjin:GetDialogAnalysisResult

[GetDialogAnalysisResult](raw/_short/api-dianjin-2024-06-28-getdialoganalysisresult-af77b60dab70f1db.md)

none

\*全部资源

`*`

无

无

dianjin:GenDocQaResult

[GenDocQaResult](raw/_short/api-dianjin-2024-06-28-gendocqaresult-ea4e4da85dcec9b7.md)

create

\*全部资源

`*`

无

无

dianjin:GetDocumentList

[GetDocumentList](raw/_short/api-dianjin-2024-06-28-getdocumentlist-8c64b5f73a3d397d.md)

get

\*全部资源

`*`

无

无

dianjin:EndToEndRealTimeDialog

[EndToEndRealTimeDialog](raw/_short/api-dianjin-2024-06-28-endtoendrealtimedialog-cf7033bc8e9b66ad.md)

none

\*全部资源

`*`

无

无

dianjin:CreateDialog

[CreateDialog](raw/_short/api-dianjin-2024-06-28-createdialog-3eacc140f2ccfd23.md)

create

\*全部资源

`*`

无

无

dianjin:DashscopeAsyncTaskFinishEvent

[DashscopeAsyncTaskFinishEvent](raw/_short/api-dianjin-2024-06-28-dashscopeasynctaskfinishe-cf84eae8f5382c7a.md)

none

\*全部资源

`*`

无

无

dianjin:CreateQualityCheckTask

[CreateQualityCheckTask](raw/_short/api-dianjin-2024-06-28-createqualitychecktask-a97404112319d946.md)

create

\*全部资源

`*`

无

无

dianjin:GetLibraryList

[GetLibraryList](raw/_short/api-dianjin-2024-06-28-getlibrarylist-7f15dede0f988ab0.md)

get

\*全部资源

`*`

无

无

dianjin:GetFilterDocumentList

[GetFilterDocumentList](raw/_short/api-dianjin-2024-06-28-getfilterdocumentlist-bd6838be9decd0b7.md)

none

\*全部资源

`*`

无

无

dianjin:GetChatQuestionResp

[GetChatQuestionResp](raw/_short/api-dianjin-2024-06-28-getchatquestionresp-582ec2d8484e6216.md)

none

\*全部资源

`*`

无

无

dianjin:RunDialogAnalysis

[RunDialogAnalysis](raw/_short/api-dianjin-2024-06-28-rundialoganalysis-a9e9c74f75b4c904.md)

none

\*全部资源

`*`

无

无

dianjin:CreatePdfTranslateTask

[CreatePdfTranslateTask](raw/_short/api-dianjin-2024-06-28-createpdftranslatetask-44b47ee418a0abd2.md)

create

\*全部资源

`*`

无

无

dianjin:UpdateQaLibrary

[UpdateQaLibrary](raw/_short/api-dianjin-2024-06-28-updateqalibrary-f59478ca344e0602.md)

create

\*全部资源

`*`

无

无

dianjin:RunChatResultGeneration

[RunChatResultGeneration](raw/_short/api-dianjin-2024-06-28-runchatresultgeneration-7ffa922f4f82a17c.md)

none

\*全部资源

`*`

无

无

dianjin:CreateAnnualDocSummaryTask

[CreateAnnualDocSummaryTask](raw/_short/api-dianjin-2024-06-28-createannualdocsummarytas-351fd85aa94ffbaa.md)

create

\*全部资源

`*`

无

无

dianjin:UploadDocument

[UploadDocument](raw/_short/api-dianjin-2024-06-28-uploaddocument-a87b051dc9961d86.md)

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
