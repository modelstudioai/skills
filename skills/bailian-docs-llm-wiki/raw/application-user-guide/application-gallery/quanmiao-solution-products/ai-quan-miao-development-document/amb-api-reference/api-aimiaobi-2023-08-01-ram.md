# 授权信息

访问控制（RAM）是阿里云提供的管理用户身份与资源访问权限的服务。使用 RAM 可以让您避免与其他用户共享阿里云账号密钥，并可按需为用户授予最小权限。RAM 中使用权限策略描述授权的具体内容。

本文为您介绍 _大模型服务平台百炼_ 为 RAM 权限策略定义的操作（Action）、资源（Resource）和条件（Condition）。 _大模型服务平台百炼_ 的 RAM 代码（RamCode）为 _aimiaobi_ ，支持的授权粒度为 _操作级_ 。

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

aimiaobi:AsyncUploadTenderDoc

[AsyncUploadTenderDoc](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-asyncuploadtenderdoc)

create

\*全部资源

`*****`

无

无

aimiaobi:ListHotSources

[ListHotSources](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listhotsources)

list

\*全部资源

`*****`

无

无

aimiaobi:ListDatasets

[ListDatasets](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listdatasets)

list

\*全部资源

`*****`

无

无

aimiaobi:ListSearchTaskDialogues

[ListSearchTaskDialogues](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listsearchtaskdialogues)

list

\*全部资源

`*****`

无

无

aimiaobi:SubmitEnterpriseVocAnalysisTask

[SubmitEnterpriseVocAnalysisTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitenterprisevocanalysistask)

get

\*全部资源

`*****`

无

无

aimiaobi:RunCustomHotTopicAnalysis

[RunCustomHotTopicAnalysis](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runcustomhottopicanalysis)

create

\*全部资源

`*****`

无

无

aimiaobi:RunCommentGeneration

[RunCommentGeneration](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runcommentgeneration)

get

\*全部资源

`*****`

无

无

aimiaobi:ListDataPermissions

[ListDataPermissions](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listdatapermissions)

list

\*全部资源

`*****`

无

无

aimiaobi:DeleteInterveneRule

[DeleteInterveneRule](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deleteintervenerule)

delete

\*全部资源

`*****`

无

无

aimiaobi:GetInterveneTemplateFileUrl

[GetInterveneTemplateFileUrl](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getintervenetemplatefileurl)

get

\*全部资源

`*****`

无

无

aimiaobi:GetClipsBuildInResource

[GetClipsBuildInResource](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getclipsbuildinresource)

get

\*全部资源

`*****`

无

无

aimiaobi:CreateToken

[CreateToken](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-createtoken)

create

\*全部资源

`*****`

无

无

aimiaobi:RunQuickWriting

[RunQuickWriting](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runquickwriting)

create

\*全部资源

`*****`

无

无

aimiaobi:CancelAuditTask

[CancelAuditTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-cancelaudittask)

update

\*全部资源

`*****`

无

无

aimiaobi:UpdateMaterialDocument

[UpdateMaterialDocument](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-updatematerialdocument)

update

\*全部资源

`*****`

无

无

aimiaobi:DeleteAuditTerms

[DeleteAuditTerms](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deleteauditterms)

delete

\*全部资源

`*****`

无

无

aimiaobi:AsyncCreateClipsTask

[AsyncCreateClipsTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-asynccreateclipstask)

create

\*全部资源

`*****`

无

无

aimiaobi:ListTopicRecommendEventList

[ListTopicRecommendEventList](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listtopicrecommendeventlist)

list

\*全部资源

`*****`

无

无

aimiaobi:GetCustomSourceTopicAnalysisTask

[GetCustomSourceTopicAnalysisTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getcustomsourcetopicanalysistask)

get

\*全部资源

`*****`

无

无

aimiaobi:RunSearchSimilarArticles

[RunSearchSimilarArticles](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runsearchsimilararticles)

none

\*全部资源

`*****`

无

无

aimiaobi:ListDocumentRetrieve

[ListDocumentRetrieve](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listdocumentretrieve)

list

\*全部资源

`*****`

无

无

aimiaobi:ListSearchTasks

[ListSearchTasks](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listsearchtasks)

list

\*全部资源

`*****`

无

无

aimiaobi:UpdateDataset

[UpdateDataset](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-updatedataset)

update

\*全部资源

`*****`

无

无

aimiaobi:GetBiddingRemainLimitNum

[GetBiddingRemainLimitNum](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getbiddingremainlimitnum)

get

\*全部资源

`*****`

无

无

aimiaobi:ImportInterveneFile

[ImportInterveneFile](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-importintervenefile)

create

\*全部资源

`*****`

无

无

aimiaobi:SubmitSmartClipTask

[SubmitSmartClipTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitsmartcliptask)

create

\*全部资源

`*****`

无

无

aimiaobi:RunExpandContent

[RunExpandContent](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runexpandcontent)

get

\*全部资源

`*****`

无

无

aimiaobi:SaveCustomText

[SaveCustomText](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-savecustomtext)

create

\*全部资源

`*****`

无

无

aimiaobi:RunPptOutlineGeneration

[RunPptOutlineGeneration](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runpptoutlinegeneration)

create

\*全部资源

`*****`

无

无

aimiaobi:InsertInterveneGlobalReply

[InsertInterveneGlobalReply](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-insertinterveneglobalreply)

create

\*全部资源

`*****`

无

无

aimiaobi:RunKeywordsExtractionGeneration

[RunKeywordsExtractionGeneration](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runkeywordsextractiongeneration)

create

\*全部资源

`*****`

无

无

aimiaobi:GetPptArtifactExportResult

[GetPptArtifactExportResult](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getpptartifactexportresult)

create

\*全部资源

`*****`

无

无

aimiaobi:GetDeepWriteTaskResult

[GetDeepWriteTaskResult](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getdeepwritetaskresult)

get

\*全部资源

`*****`

无

无

aimiaobi:ExportAuditContentResult

[ExportAuditContentResult](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-exportauditcontentresult)

create

\*全部资源

`*****`

无

无

aimiaobi:GetAuditNotePostProcessingStatus

[GetAuditNotePostProcessingStatus](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getauditnotepostprocessingstatus)

get

\*全部资源

`*****`

无

无

aimiaobi:GetStyleLearningResult

[GetStyleLearningResult](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getstylelearningresult)

get

\*全部资源

`*****`

无

无

aimiaobi:CreateGeneratedContent

[CreateGeneratedContent](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-creategeneratedcontent)

create

\*全部资源

`*****`

无

无

aimiaobi:RunTranslateGeneration

[RunTranslateGeneration](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runtranslategeneration)

create

\*全部资源

`*****`

无

无

aimiaobi:RunCustomHotTopicViewPointAnalysis

[RunCustomHotTopicViewPointAnalysis](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runcustomhottopicviewpointanalysis)

create

\*全部资源

`*****`

无

无

aimiaobi:RunAiHelperWriting

[RunAiHelperWriting](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runaihelperwriting)

create

\*全部资源

`*****`

无

无

aimiaobi:RunSummaryGenerate

[RunSummaryGenerate](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runsummarygenerate)

get

\*全部资源

`*****`

无

无

aimiaobi:ListFreshViewPoints

[ListFreshViewPoints](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listfreshviewpoints)

list

\*全部资源

`*****`

无

无

aimiaobi:GetPptConfig

[GetPptConfig](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getpptconfig)

create

\*全部资源

`*****`

无

无

aimiaobi:DeleteDataset

[DeleteDataset](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletedataset)

delete

\*全部资源

`*****`

无

无

aimiaobi:FetchExportTermsTask

[FetchExportTermsTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-fetchexporttermstask)

none

\*全部资源

`*****`

无

无

aimiaobi:GetTopicSelectionPerspectiveAnalysisTask

[GetTopicSelectionPerspectiveAnalysisTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-gettopicselectionperspectiveanalysistask)

get

\*全部资源

`*****`

无

无

aimiaobi:ListHotNewsWithType

[ListHotNewsWithType](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listhotnewswithtype)

list

\*全部资源

`*****`

无

无

aimiaobi:AsyncWritingBiddingDoc

[AsyncWritingBiddingDoc](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-asyncwritingbiddingdoc)

create

\*全部资源

`*****`

无

无

aimiaobi:DeleteDatasetDocument

[DeleteDatasetDocument](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletedatasetdocument)

delete

\*全部资源

`*****`

无

无

aimiaobi:DownloadBiddingDoc

[DownloadBiddingDoc](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-downloadbiddingdoc)

get

\*全部资源

`*****`

无

无

aimiaobi:SubmitCustomTopicSelectionPerspectiveAnalysisTask

[SubmitCustomTopicSelectionPerspectiveAnalysisTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitcustomtopicselectionperspectiveanalysistask)

create

\*全部资源

`*****`

无

无

aimiaobi:ListIntervenes

[ListIntervenes](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listintervenes)

list

\*全部资源

`*****`

无

无

aimiaobi:InsertInterveneRule

[InsertInterveneRule](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-insertintervenerule)

create

\*全部资源

`*****`

无

无

aimiaobi:ClearIntervenes

[ClearIntervenes](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-clearintervenes)

delete

\*全部资源

`*****`

无

无

aimiaobi:ListBiddingDoc

[ListBiddingDoc](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listbiddingdoc)

list

\*全部资源

`*****`

无

无

aimiaobi:ListBuildConfigs

[ListBuildConfigs](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listbuildconfigs)

get

\*全部资源

`*****`

无

无

aimiaobi:BindPptArtifact

[BindPptArtifact](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-bindpptartifact)

create

\*全部资源

`*****`

无

无

aimiaobi:RunStepByStepWriting

[RunStepByStepWriting](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runstepbystepwriting)

create

\*全部资源

`*****`

无

无

aimiaobi:RunAbbreviationContent

[RunAbbreviationContent](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runabbreviationcontent)

get

\*全部资源

`*****`

无

无

aimiaobi:SaveStyleLearningResult

[SaveStyleLearningResult](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-savestylelearningresult)

create

\*全部资源

`*****`

无

无

aimiaobi:GetInterveneImportTaskInfo

[GetInterveneImportTaskInfo](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getinterveneimporttaskinfo)

get

\*全部资源

`*****`

无

无

aimiaobi:AsyncCreateClipsTimeLine

[AsyncCreateClipsTimeLine](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-asynccreateclipstimeline)

create

\*全部资源

`*****`

无

无

aimiaobi:GenerateImageTask

[GenerateImageTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-generateimagetask)

create

\*全部资源

`*****`

无

无

aimiaobi:ListWritingStyles

[ListWritingStyles](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listwritingstyles)

list

\*全部资源

`*****`

无

无

aimiaobi:CreateDataset

[CreateDataset](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-createdataset)

create

\*全部资源

`*****`

无

无

aimiaobi:GetHotTopicBroadcast

[GetHotTopicBroadcast](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-gethottopicbroadcast)

get

\*全部资源

`*****`

无

无

aimiaobi:ListCustomViewPoints

[ListCustomViewPoints](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listcustomviewpoints)

list

\*全部资源

`*****`

无

无

aimiaobi:ExportIntervenes

[ExportIntervenes](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-exportintervenes)

list

\*全部资源

`*****`

无

无

aimiaobi:ListAnalysisTagDetailByTaskId

[ListAnalysisTagDetailByTaskId](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listanalysistagdetailbytaskid)

get

\*全部资源

`*****`

无

无

aimiaobi:DeleteGeneralConfig

[DeleteGeneralConfig](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletegeneralconfig)

delete

\*全部资源

`*****`

无

无

aimiaobi:SubmitAuditTask

[SubmitAuditTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitaudittask)

create

\*全部资源

`*****`

无

无

aimiaobi:RunGenerateQuestions

[RunGenerateQuestions](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rungeneratequestions)

get

\*全部资源

`*****`

无

无

aimiaobi:DeleteMaterialById

[DeleteMaterialById](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletematerialbyid)

delete

\*全部资源

`*****`

无

无

aimiaobi:RunDocIntroduction

[RunDocIntroduction](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocintroduction)

get

\*全部资源

`*****`

无

无

aimiaobi:ExportCustomSourceAnalysisTask

[ExportCustomSourceAnalysisTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-exportcustomsourceanalysistask)

get

\*全部资源

`*****`

无

无

aimiaobi:RunDeepWriting

[RunDeepWriting](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundeepwriting)

create

\*全部资源

`*****`

无

无

aimiaobi:GetDatasetDocument

[GetDatasetDocument](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getdatasetdocument)

get

\*全部资源

`*****`

无

无

aimiaobi:RunTopicSelectionMerge

[RunTopicSelectionMerge](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runtopicselectionmerge)

create

\*全部资源

`*****`

无

无

aimiaobi:ExportAnalysisTagDetailByTaskId

[ExportAnalysisTagDetailByTaskId](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-exportanalysistagdetailbytaskid)

get

\*全部资源

`*****`

无

无

aimiaobi:SubmitDeepWriteTask

[SubmitDeepWriteTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitdeepwritetask)

create

\*全部资源

`*****`

无

无

aimiaobi:RunWriting

[RunWriting](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runwriting)

create

\*全部资源

`*****`

无

无

aimiaobi:GetAutoClipsTaskInfo

[GetAutoClipsTaskInfo](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getautoclipstaskinfo)

get

\*全部资源

`*****`

无

无

aimiaobi:GenerateFileUrlByKey

[GenerateFileUrlByKey](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-generatefileurlbykey)

get

\*全部资源

`*****`

无

无

aimiaobi:RunBookSmartCard

[RunBookSmartCard](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runbooksmartcard)

get

\*全部资源

`*****`

无

无

aimiaobi:SubmitTopicSelectionPerspectiveAnalysisTask

[SubmitTopicSelectionPerspectiveAnalysisTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submittopicselectionperspectiveanalysistask)

create

\*全部资源

`*****`

无

无

aimiaobi:GetPptTemplateSelector

[GetPptTemplateSelector](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getppttemplateselector)

create

\*全部资源

`*****`

无

无

aimiaobi:GenerateUploadConfig

[GenerateUploadConfig](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-generateuploadconfig)

create

\*全部资源

`*****`

无

无

aimiaobi:SubmitSmartAudit

[SubmitSmartAudit](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitsmartaudit)

create

\*全部资源

`*****`

无

无

aimiaobi:SubmitVideoAudit

[SubmitVideoAudit](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitvideoaudit)

create

\*全部资源

`*****`

无

无

aimiaobi:InitiatePptCreationV2

[InitiatePptCreationV2](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-initiatepptcreationv2)

create

\*全部资源

`*****`

无

无

aimiaobi:RunDocWashing

[RunDocWashing](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocwashing)

get

\*全部资源

`*****`

无

无

aimiaobi:UpdateGeneratedContent

[UpdateGeneratedContent](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-updategeneratedcontent)

update

\*全部资源

`*****`

无

无

aimiaobi:ListHotViewPoints

[ListHotViewPoints](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listhotviewpoints)

list

\*全部资源

`*****`

无

无

aimiaobi:GetMaterialById

[GetMaterialById](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getmaterialbyid)

get

\*全部资源

`*****`

无

无

aimiaobi:GenerateExportWordTask

[GenerateExportWordTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-generateexportwordtask)

get

\*全部资源

`*****`

无

无

aimiaobi:RunDocQa

[RunDocQa](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocqa)

get

\*全部资源

`*****`

无

无

aimiaobi:SaveDataSourceOrderConfig

[SaveDataSourceOrderConfig](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-savedatasourceorderconfig)

create

\*全部资源

`*****`

无

无

aimiaobi:DeleteDocs

[DeleteDocs](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletedocs)

delete

\*全部资源

`*****`

无

无

aimiaobi:ListWebReviewPoints

[ListWebReviewPoints](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listwebreviewpoints)

list

\*全部资源

`*****`

无

无

aimiaobi:DeleteStyleLearningResult

[DeleteStyleLearningResult](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletestylelearningresult)

delete

\*全部资源

`*****`

无

无

aimiaobi:CancelDeepWriteTask

[CancelDeepWriteTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-canceldeepwritetask)

update

\*全部资源

`*****`

无

无

aimiaobi:CreateGeneralConfig

[CreateGeneralConfig](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-creategeneralconfig)

create

\*全部资源

`*****`

无

无

aimiaobi:ExportGeneratedContent

[ExportGeneratedContent](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-exportgeneratedcontent)

get

\*全部资源

`*****`

无

无

aimiaobi:GetProperties

[GetProperties](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getproperties)

get

\*全部资源

`*****`

无

无

aimiaobi:GetGeneralConfig

[GetGeneralConfig](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getgeneralconfig)

get

\*全部资源

`*****`

无

无

aimiaobi:UpdateCustomText

[UpdateCustomText](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-updatecustomtext)

update

\*全部资源

`*****`

无

无

aimiaobi:UpdateDatasetDocument

[UpdateDatasetDocument](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-updatedatasetdocument)

update

\*全部资源

`*****`

无

无

aimiaobi:GetTopicById

[GetTopicById](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-gettopicbyid)

get

\*全部资源

`*****`

无

无

aimiaobi:ListInterveneCnt

[ListInterveneCnt](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listintervenecnt)

list

\*全部资源

`*****`

无

无

aimiaobi:ListMaterialDocuments

[ListMaterialDocuments](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listmaterialdocuments)

list

\*全部资源

`*****`

无

无

aimiaobi:UpdateGeneralConfig

[UpdateGeneralConfig](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-updategeneralconfig)

update

\*全部资源

`*****`

无

无

aimiaobi:GenerateViewPoint

[GenerateViewPoint](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-generateviewpoint)

list

\*全部资源

`*****`

无

无

aimiaobi:GetCustomHotTopicBroadcastJob

[GetCustomHotTopicBroadcastJob](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getcustomhottopicbroadcastjob)

get

\*全部资源

`*****`

无

无

aimiaobi:ListStyleLearningResult

[ListStyleLearningResult](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-liststylelearningresult)

list

\*全部资源

`*****`

无

无

aimiaobi:GetInterveneGlobalReply

[GetInterveneGlobalReply](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getinterveneglobalreply)

get

\*全部资源

`*****`

无

无

aimiaobi:RunSearchGeneration

[RunSearchGeneration](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runsearchgeneration)

create

\*全部资源

`*****`

无

无

aimiaobi:DownloadAuditNote

[DownloadAuditNote](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-downloadauditnote)

get

\*全部资源

`*****`

无

无

aimiaobi:GetCategoriesByTaskId

[GetCategoriesByTaskId](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getcategoriesbytaskid)

get

\*全部资源

`*****`

无

无

aimiaobi:EditBiddingDoc

[EditBiddingDoc](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-editbiddingdoc)

update

\*全部资源

`*****`

无

无

aimiaobi:FetchImageTask

[FetchImageTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-fetchimagetask)

get

\*全部资源

`*****`

无

无

aimiaobi:ListDialogues

[ListDialogues](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listdialogues)

list

\*全部资源

`*****`

无

无

aimiaobi:SaveOrUpdateOssConfig

[SaveOrUpdateOssConfig](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-saveorupdateossconfig)

create

\*全部资源

`*****`

无

无

aimiaobi:ListEnterprisePptTemplates

[ListEnterprisePptTemplates](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listenterpriseppttemplates)

list

\*全部资源

`*****`

无

无

aimiaobi:RunWriteToneGeneration

[RunWriteToneGeneration](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runwritetonegeneration)

create

\*全部资源

`*****`

无

无

aimiaobi:GetFileContentLength

[GetFileContentLength](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getfilecontentlength)

get

\*全部资源

`*****`

无

无

aimiaobi:SubmitCustomHotTopicBroadcastJob

[SubmitCustomHotTopicBroadcastJob](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitcustomhottopicbroadcastjob)

create

\*全部资源

`*****`

无

无

aimiaobi:SubmitImportTermsTask

[SubmitImportTermsTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitimporttermstask)

none

\*全部资源

`*****`

无

无

aimiaobi:ListGeneratedContents

[ListGeneratedContents](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listgeneratedcontents)

list

\*全部资源

`*****`

无

无

aimiaobi:RunDocSummary

[RunDocSummary](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocsummary)

get

\*全部资源

`*****`

无

无

aimiaobi:GetDataSourceOrderConfig

[GetDataSourceOrderConfig](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getdatasourceorderconfig)

get

\*全部资源

`*****`

无

无

aimiaobi:GetAuditNoteProcessingStatus

[GetAuditNoteProcessingStatus](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getauditnoteprocessingstatus)

get

\*全部资源

`*****`

无

无

aimiaobi:RunContinueContent

[RunContinueContent](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runcontinuecontent)

get

\*全部资源

`*****`

无

无

aimiaobi:FeedbackDialogue

[FeedbackDialogue](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-feedbackdialogue)

create

\*全部资源

`*****`

无

无

aimiaobi:FetchImportTermsTask

[FetchImportTermsTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-fetchimporttermstask)

none

\*全部资源

`*****`

无

无

aimiaobi:RunDocTranslation

[RunDocTranslation](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundoctranslation)

get

\*全部资源

`*****`

无

无

aimiaobi:AddDatasetDocument

[AddDatasetDocument](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-adddatasetdocument)

create

\*全部资源

`*****`

无

无

aimiaobi:SubmitFactAuditUrl

[SubmitFactAuditUrl](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitfactauditurl)

create

\*全部资源

`*****`

无

无

aimiaobi:GetFactAuditUrl

[GetFactAuditUrl](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getfactauditurl)

delete

\*全部资源

`*****`

无

无

aimiaobi:ListInterveneRules

[ListInterveneRules](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listintervenerules)

list

\*全部资源

`*****`

无

无

aimiaobi:SubmitExportTermsTask

[SubmitExportTermsTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitexporttermstask)

none

\*全部资源

`*****`

无

无

aimiaobi:RunDocBrainmap

[RunDocBrainmap](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocbrainmap)

get

\*全部资源

`*****`

无

无

aimiaobi:ImportInterveneFileAsync

[ImportInterveneFileAsync](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-importintervenefileasync)

create

\*全部资源

`*****`

无

无

aimiaobi:ExportPptArtifact

[ExportPptArtifact](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-exportpptartifact)

create

\*全部资源

`*****`

无

无

aimiaobi:GetSmartClipTask

[GetSmartClipTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getsmartcliptask)

create

\*全部资源

`*****`

无

无

aimiaobi:ExportHotTopicPlanningProposals

[ExportHotTopicPlanningProposals](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-exporthottopicplanningproposals)

get

\*全部资源

`*****`

无

无

aimiaobi:CreateDataPermissions

[CreateDataPermissions](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-createdatapermissions)

create

\*全部资源

`*****`

无

无

aimiaobi:DeleteGeneratedContent

[DeleteGeneratedContent](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletegeneratedcontent)

delete

\*全部资源

`*****`

无

无

aimiaobi:EditAuditTerms

[EditAuditTerms](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-editauditterms)

update

\*全部资源

`*****`

无

无

aimiaobi:GetInterveneRuleDetail

[GetInterveneRuleDetail](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getinterveneruledetail)

get

\*全部资源

`*****`

无

无

aimiaobi:SubmitCustomSourceTopicAnalysis

[SubmitCustomSourceTopicAnalysis](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitcustomsourcetopicanalysis)

create

\*全部资源

`*****`

无

无

aimiaobi:RunTitleGeneration

[RunTitleGeneration](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runtitlegeneration)

create

\*全部资源

`*****`

无

无

aimiaobi:RunHotword

[RunHotword](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runhotword)

get

\*全部资源

`*****`

无

无

aimiaobi:GetAvailableAuditNotes

[GetAvailableAuditNotes](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getavailableauditnotes)

get

\*全部资源

`*****`

无

无

aimiaobi:ListTopicViewPointRecommendEventList

[ListTopicViewPointRecommendEventList](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listtopicviewpointrecommendeventlist)

list

\*全部资源

`*****`

无

无

aimiaobi:GetDocClusterTask

[GetDocClusterTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getdocclustertask)

get

\*全部资源

`*****`

无

无

aimiaobi:AddAuditTerms

[AddAuditTerms](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-addauditterms)

create

\*全部资源

`*****`

无

无

aimiaobi:GetPptArtifact

[GetPptArtifact](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getpptartifact)

get

\*全部资源

`*****`

无

无

aimiaobi:SubmitAsyncTask

[SubmitAsyncTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitasynctask)

create

\*全部资源

`*****`

无

无

aimiaobi:ListSearchTaskDialogueDatas

[ListSearchTaskDialogueDatas](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listsearchtaskdialoguedatas)

list

\*全部资源

`*****`

无

无

aimiaobi:AsyncUploadVideo

[AsyncUploadVideo](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-asyncuploadvideo)

create

\*全部资源

`*****`

无

无

aimiaobi:GetPptInfo

[GetPptInfo](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getpptinfo)

create

\*全部资源

`*****`

无

无

aimiaobi:UploadBook

[UploadBook](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-uploadbook)

create

\*全部资源

`*****`

无

无

aimiaobi:CancelAsyncTask

[CancelAsyncTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-cancelasynctask)

update

\*全部资源

`*****`

无

无

aimiaobi:QueryVideoAuditResult

[QueryVideoAuditResult](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-queryvideoauditresult)

get

\*全部资源

`*****`

无

无

aimiaobi:GetSmartAuditResult

[GetSmartAuditResult](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getsmartauditresult)

get

\*全部资源

`*****`

无

无

aimiaobi:DeleteAuditNote

[DeleteAuditNote](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deleteauditnote)

delete

\*全部资源

`*****`

无

无

aimiaobi:RunMultiDocIntroduction

[RunMultiDocIntroduction](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runmultidocintroduction)

get

\*全部资源

`*****`

无

无

aimiaobi:SubmitAuditNote

[SubmitAuditNote](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitauditnote)

none

\*全部资源

`*****`

无

无

aimiaobi:GetEnterpriseVocAnalysisTask

[GetEnterpriseVocAnalysisTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getenterprisevocanalysistask)

get

\*全部资源

`*****`

无

无

aimiaobi:ConfirmAndPostProcessAuditNote

[ConfirmAndPostProcessAuditNote](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-confirmandpostprocessauditnote)

none

\*全部资源

`*****`

无

无

aimiaobi:ValidateUploadTemplate

[ValidateUploadTemplate](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-validateuploadtemplate)

get

\*全部资源

`*****`

无

无

aimiaobi:ListAutoClipsTask

[ListAutoClipsTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listautoclipstask)

list

\*全部资源

`*****`

无

无

aimiaobi:DeleteCustomTopicByTopic

[DeleteCustomTopicByTopic](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletecustomtopicbytopic)

delete

\*全部资源

`*****`

无

无

aimiaobi:DeleteDataPermissions

[DeleteDataPermissions](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletedatapermissions)

delete

\*全部资源

`*****`

无

无

aimiaobi:RunDocSmartCard

[RunDocSmartCard](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocsmartcard)

get

\*全部资源

`*****`

无

无

aimiaobi:RunStyleFeatureAnalysis

[RunStyleFeatureAnalysis](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runstylefeatureanalysis)

get

\*全部资源

`*****`

无

无

aimiaobi:ListCustomText

[ListCustomText](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listcustomtext)

list

\*全部资源

`*****`

无

无

aimiaobi:ListPptArtifacts

[ListPptArtifacts](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listpptartifacts)

list

\*全部资源

`*****`

无

无

aimiaobi:RunBookIntroduction

[RunBookIntroduction](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runbookintroduction)

get

\*全部资源

`*****`

无

无

aimiaobi:ListGeneralConfigs

[ListGeneralConfigs](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listgeneralconfigs)

list

\*全部资源

`*****`

无

无

aimiaobi:QueryAuditTask

[QueryAuditTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-queryaudittask)

get

\*全部资源

`*****`

无

无

aimiaobi:DeleteFactAuditUrl

[DeleteFactAuditUrl](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletefactauditurl)

delete

\*全部资源

`*****`

无

无

aimiaobi:RunTextPolishing

[RunTextPolishing](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runtextpolishing)

create

\*全部资源

`*****`

无

无

aimiaobi:DocumentExtraction

[DocumentExtraction](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-documentextraction)

get

\*全部资源

`*****`

无

无

aimiaobi:GetDocInfo

[GetDocInfo](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getdocinfo)

get

\*全部资源

`*****`

无

无

aimiaobi:ListAsyncTasks

[ListAsyncTasks](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listasynctasks)

list

\*全部资源

`*****`

无

无

aimiaobi:GetCustomTopicSelectionPerspectiveAnalysisTask

[GetCustomTopicSelectionPerspectiveAnalysisTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getcustomtopicselectionperspectiveanalysistask)

get

\*全部资源

`*****`

无

无

aimiaobi:SearchNews

[SearchNews](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-searchnews)

list

\*全部资源

`*****`

无

无

aimiaobi:ListAuditContentErrorTypes

[ListAuditContentErrorTypes](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listauditcontenterrortypes)

list

\*全部资源

`*****`

无

无

aimiaobi:ListTimedViewAttitude

[ListTimedViewAttitude](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listtimedviewattitude)

list

\*全部资源

`*****`

无

无

aimiaobi:ListDocs

[ListDocs](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listdocs)

list

\*全部资源

`*****`

无

无

aimiaobi:ListHotTopics

[ListHotTopics](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listhottopics)

list

\*全部资源

`*****`

无

无

aimiaobi:DeleteCustomTopicViewPointById

[DeleteCustomTopicViewPointById](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletecustomtopicviewpointbyid)

delete

\*全部资源

`*****`

无

无

aimiaobi:SearchDatasetDocuments

[SearchDatasetDocuments](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-searchdatasetdocuments)

list

\*全部资源

`*****`

无

无

aimiaobi:ListPptTemplates

[ListPptTemplates](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listppttemplates)

list

\*全部资源

`*****`

无

无

aimiaobi:DeleteCustomText

[DeleteCustomText](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletecustomtext)

delete

\*全部资源

`*****`

无

无

aimiaobi:GetGeneratedContent

[GetGeneratedContent](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getgeneratedcontent)

get

\*全部资源

`*****`

无

无

aimiaobi:DeletePptArtifact

[DeletePptArtifact](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-deletepptartifact)

delete

\*全部资源

`*****`

无

无

aimiaobi:RunWritingV2

[RunWritingV2](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runwritingv2)

create

\*全部资源

`*****`

无

无

aimiaobi:UploadDoc

[UploadDoc](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-uploaddoc)

create

\*全部资源

`*****`

无

无

aimiaobi:ListAuditTerms

[ListAuditTerms](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listauditterms)

list

\*全部资源

`*****`

无

无

aimiaobi:ListVersions

[ListVersions](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listversions)

list

\*全部资源

`*****`

无

无

aimiaobi:GetDataset

[GetDataset](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getdataset)

get

\*全部资源

`*****`

无

无

aimiaobi:GetCustomText

[GetCustomText](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getcustomtext)

get

\*全部资源

`*****`

无

无

aimiaobi:QueryAsyncTask

[QueryAsyncTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-queryasynctask)

get

\*全部资源

`*****`

无

无

aimiaobi:FetchExportWordTask

[FetchExportWordTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-fetchexportwordtask)

get

\*全部资源

`*****`

无

无

aimiaobi:ListPlanningProposal

[ListPlanningProposal](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listplanningproposal)

list

\*全部资源

`*****`

无

无

aimiaobi:ListDatasetDocuments

[ListDatasetDocuments](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listdatasetdocuments)

list

\*全部资源

`*****`

无

无

aimiaobi:InitiatePptCreation

[InitiatePptCreation](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-initiatepptcreation)

create

\*全部资源

`*****`

无

无

aimiaobi:RunBookBrainmap

[RunBookBrainmap](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runbookbrainmap)

get

\*全部资源

`*****`

无

无

aimiaobi:GetDeepWriteTask

[GetDeepWriteTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getdeepwritetask)

get

\*全部资源

`*****`

无

无

aimiaobi:SaveMaterialDocument

[SaveMaterialDocument](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-savematerialdocument)

create

\*全部资源

`*****`

无

无

aimiaobi:RunVideoScriptGenerate

[RunVideoScriptGenerate](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runvideoscriptgenerate)

create

\*全部资源

`*****`

无

无

aimiaobi:GetBiddingDocInfo

[GetBiddingDocInfo](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getbiddingdocinfo)

get

\*全部资源

`*****`

无

无

aimiaobi:SubmitDocClusterTask

[SubmitDocClusterTask](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitdocclustertask)

create

\*全部资源

`*****`

无

无

aimiaobi:AsyncEditTimeline

[AsyncEditTimeline](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-asyncedittimeline)

update

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
