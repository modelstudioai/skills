# 授权信息

访问控制（RAM）是阿里云提供的管理用户身份与资源访问权限的服务。使用 RAM 可以让您避免与其他用户共享阿里云账号密钥，并可按需为用户授予最小权限。RAM 中使用权限策略描述授权的具体内容。

本文为您介绍_大模型服务平台百炼_为 RAM 权限策略定义的操作（Action）、资源（Resource）和条件（Condition）。_大模型服务平台百炼_的 RAM 代码（RamCode）为_aimiaobi_，支持的授权粒度为_操作级_。

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
    
-   Action：授予允许或拒绝权限的具体操作。具体信息，请参见[操作（Action）](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-ram#title-auth-detail-2)。
    
-   Resource：受操作影响的具体对象，您可以使用资源 ARN 来描述指定资源。具体信息，请参见[资源（Resource）](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-ram#title-auth-detail-3)。
    
-   Condition：指授权生效的条件。可选字段。具体信息，请参见[条件（Condition）](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-ram#title-auth-detail-4)。
    
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

aimiaobi:RunDocTranslation

[RunDocTranslation](raw/_short/api-aimiaobi-2023-08-01-rundoctranslation-0f3a1feddae9d305.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunWriting

[RunWriting](raw/_short/api-aimiaobi-2023-08-01-runwriting-9d6e099473aae89e.md)

create

\*全部资源

`*`

无

无

aimiaobi:InitiatePptCreationV2

[InitiatePptCreationV2](raw/_short/api-aimiaobi-2023-08-01-initiatepptcreationv2-4062493b702b42ec.md)

create

\*全部资源

`*`

无

无

aimiaobi:DocumentExtraction

[DocumentExtraction](raw/_short/api-aimiaobi-2023-08-01-documentextraction-879dcd16a978286b.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListTopicViewPointRecommendEventList

[ListTopicViewPointRecommendEventList](raw/_short/api-aimiaobi-2023-08-01-listtopicviewpointrecomm-ebe93014b2db3119.md)

list

\*全部资源

`*`

无

无

aimiaobi:SubmitImportTermsTask

[SubmitImportTermsTask](raw/_short/api-aimiaobi-2023-08-01-submitimporttermstask-9a94f483ca7bc550.md)

none

\*全部资源

`*`

无

无

aimiaobi:RunGenerateQuestions

[RunGenerateQuestions](raw/_short/api-aimiaobi-2023-08-01-rungeneratequestions-f55f369366c49818.md)

get

\*全部资源

`*`

无

无

aimiaobi:DeleteCustomTopicByTopic

[DeleteCustomTopicByTopic](raw/_short/api-aimiaobi-2023-08-01-deletecustomtopicbytopic-66df35e4f3a7ae25.md)

delete

\*全部资源

`*`

无

无

aimiaobi:RunStyleFeatureAnalysis

[RunStyleFeatureAnalysis](raw/_short/api-aimiaobi-2023-08-01-runstylefeatureanalysis-160e341164f4c588.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetAutoClipsTaskInfo

[GetAutoClipsTaskInfo](raw/_short/api-aimiaobi-2023-08-01-getautoclipstaskinfo-50f6650b8f3c65c5.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunCustomHotTopicViewPointAnalysis

[RunCustomHotTopicViewPointAnalysis](raw/_short/api-aimiaobi-2023-08-01-runcustomhottopicviewpoi-b4cbf10013f689d2.md)

create

\*全部资源

`*`

无

无

aimiaobi:AsyncUploadVideo

[AsyncUploadVideo](raw/_short/api-aimiaobi-2023-08-01-asyncuploadvideo-d0e99ebcb110c597.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeleteGeneratedContent

[DeleteGeneratedContent](raw/_short/api-aimiaobi-2023-08-01-deletegeneratedcontent-1df6fa814ba5cf1f.md)

delete

\*全部资源

`*`

无

无

aimiaobi:SaveMaterialDocument

[SaveMaterialDocument](raw/_short/api-aimiaobi-2023-08-01-savematerialdocument-2ed89ecadfabe906.md)

create

\*全部资源

`*`

无

无

aimiaobi:AsyncCreateClipsTimeLine

[AsyncCreateClipsTimeLine](raw/_short/api-aimiaobi-2023-08-01-asynccreateclipstimeline-14877300ad7c1050.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListMaterialDocuments

[ListMaterialDocuments](raw/_short/api-aimiaobi-2023-08-01-listmaterialdocuments-a02fb69f2708de2b.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetCustomSourceTopicAnalysisTask

[GetCustomSourceTopicAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-getcustomsourcetopicanal-3f63cd5d0eb9099a.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListFreshViewPoints

[ListFreshViewPoints](raw/_short/api-aimiaobi-2023-08-01-listfreshviewpoints-bb696a988a17c02b.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetInterveneGlobalReply

[GetInterveneGlobalReply](raw/_short/api-aimiaobi-2023-08-01-getinterveneglobalreply-cb707e0863d06e20.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListDocs

[ListDocs](raw/_short/api-aimiaobi-2023-08-01-listdocs-ad0fdf3af98a7522.md)

list

\*全部资源

`*`

无

无

aimiaobi:AddAuditTerms

[AddAuditTerms](raw/_short/api-aimiaobi-2023-08-01-addauditterms-2421387c4f814ba2.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeleteDataset

[DeleteDataset](raw/_short/api-aimiaobi-2023-08-01-deletedataset-1ea96ab7e4a8eed5.md)

delete

\*全部资源

`*`

无

无

aimiaobi:ListAuditContentErrorTypes

[ListAuditContentErrorTypes](raw/_short/api-aimiaobi-2023-08-01-listauditcontenterrortyp-ae99f744060b0271.md)

list

\*全部资源

`*`

无

无

aimiaobi:DeleteInterveneRule

[DeleteInterveneRule](raw/_short/api-aimiaobi-2023-08-01-deleteintervenerule-cd1c8557749e6f23.md)

delete

\*全部资源

`*`

无

无

aimiaobi:UpdateMaterialDocument

[UpdateMaterialDocument](raw/_short/api-aimiaobi-2023-08-01-updatematerialdocument-21039974b5d50370.md)

update

\*全部资源

`*`

无

无

aimiaobi:ListDatasetDocuments

[ListDatasetDocuments](raw/_short/api-aimiaobi-2023-08-01-listdatasetdocuments-e5d9a8f76f09beb3.md)

list

\*全部资源

`*`

无

无

aimiaobi:GenerateViewPoint

[GenerateViewPoint](raw/_short/api-aimiaobi-2023-08-01-generateviewpoint-e5f80eb517621506.md)

list

\*全部资源

`*`

无

无

aimiaobi:CreateDataset

[CreateDataset](raw/_short/api-aimiaobi-2023-08-01-createdataset-9cf2fa0cba66e0a0.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetClipsBuildInResource

[GetClipsBuildInResource](raw/_short/api-aimiaobi-2023-08-01-getclipsbuildinresource-14ccf9f66f82db80.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetSmartAuditResult

[GetSmartAuditResult](raw/_short/api-aimiaobi-2023-08-01-getsmartauditresult-7103e3facc2406a5.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunCommentGeneration

[RunCommentGeneration](raw/_short/api-aimiaobi-2023-08-01-runcommentgeneration-aaa80fae0d17b5d7.md)

get

\*全部资源

`*`

无

无

aimiaobi:InsertInterveneRule

[InsertInterveneRule](raw/_short/api-aimiaobi-2023-08-01-insertintervenerule-839c4bd6eb0087cb.md)

create

\*全部资源

`*`

无

无

aimiaobi:CreateGeneralConfig

[CreateGeneralConfig](raw/_short/api-aimiaobi-2023-08-01-creategeneralconfig-5fd6ad7a5aceecc5.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetDatasetDocument

[GetDatasetDocument](raw/_short/api-aimiaobi-2023-08-01-getdatasetdocument-288cb4bd87c944f5.md)

get

\*全部资源

`*`

无

无

aimiaobi:ClearIntervenes

[ClearIntervenes](raw/_short/api-aimiaobi-2023-08-01-clearintervenes-6f2779628a8415e0.md)

delete

\*全部资源

`*`

无

无

aimiaobi:ListDataPermissions

[ListDataPermissions](raw/_short/api-aimiaobi-2023-08-01-listdatapermissions-6a463276f7a9b04b.md)

list

\*全部资源

`*`

无

无

aimiaobi:ListCustomText

[ListCustomText](raw/_short/api-aimiaobi-2023-08-01-listcustomtext-5c8b74495701eb8c.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunDocSmartCard

[RunDocSmartCard](raw/_short/api-aimiaobi-2023-08-01-rundocsmartcard-af6c27edb34673b0.md)

get

\*全部资源

`*`

无

无

aimiaobi:UpdateGeneratedContent

[UpdateGeneratedContent](raw/_short/api-aimiaobi-2023-08-01-updategeneratedcontent-2e8dd063dcd14c64.md)

update

\*全部资源

`*`

无

无

aimiaobi:GetDataSourceOrderConfig

[GetDataSourceOrderConfig](raw/_short/api-aimiaobi-2023-08-01-getdatasourceorderconfig-e2d6ff83ddbb8c7a.md)

get

\*全部资源

`*`

无

无

aimiaobi:SubmitTopicSelectionPerspectiveAnalysisTask

[SubmitTopicSelectionPerspectiveAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-submittopicselectionpers-b46d6db50c29c545.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListInterveneRules

[ListInterveneRules](raw/_short/api-aimiaobi-2023-08-01-listintervenerules-be029c7a7c1dd9a1.md)

list

\*全部资源

`*`

无

无

aimiaobi:ListHotTopics

[ListHotTopics](raw/_short/api-aimiaobi-2023-08-01-listhottopics-be1206a872d0fc62.md)

list

\*全部资源

`*`

无

无

aimiaobi:SubmitCustomTopicSelectionPerspectiveAnalysisTask

[SubmitCustomTopicSelectionPerspectiveAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-submitcustomtopicselecti-f43c96bd9199b0b0.md)

create

\*全部资源

`*`

无

无

aimiaobi:CreateToken

[CreateToken](raw/_short/api-aimiaobi-2023-08-01-createtoken-31d0f72627ed1e95.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunDocIntroduction

[RunDocIntroduction](raw/_short/api-aimiaobi-2023-08-01-rundocintroduction-b3dff35f3fe6ef41.md)

get

\*全部资源

`*`

无

无

aimiaobi:CancelDeepWriteTask

[CancelDeepWriteTask](raw/_short/api-aimiaobi-2023-08-01-canceldeepwritetask-f1d2e18084b53a79.md)

update

\*全部资源

`*`

无

无

aimiaobi:DeleteAuditTerms

[DeleteAuditTerms](raw/_short/api-aimiaobi-2023-08-01-deleteauditterms-5bec31d0945e0f6e.md)

delete

\*全部资源

`*`

无

无

aimiaobi:FeedbackDialogue

[FeedbackDialogue](raw/_short/api-aimiaobi-2023-08-01-feedbackdialogue-7e2be294b274b693.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListWebReviewPoints

[ListWebReviewPoints](raw/_short/api-aimiaobi-2023-08-01-listwebreviewpoints-ed2b4a25f4ee1fcd.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunDocWashing

[RunDocWashing](raw/_short/api-aimiaobi-2023-08-01-rundocwashing-3dfdb3e3dbc3bf19.md)

get

\*全部资源

`*`

无

无

aimiaobi:DeleteAuditNote

[DeleteAuditNote](raw/_short/api-aimiaobi-2023-08-01-deleteauditnote-295374bda0cc78a8.md)

delete

\*全部资源

`*`

无

无

aimiaobi:ImportInterveneFileAsync

[ImportInterveneFileAsync](raw/_short/api-aimiaobi-2023-08-01-importintervenefileasync-e2549c89026ee3b1.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeletePptArtifact

[DeletePptArtifact](raw/_short/api-aimiaobi-2023-08-01-deletepptartifact-9553eeced05220b3.md)

delete

\*全部资源

`*`

无

无

aimiaobi:SearchDatasetDocuments

[SearchDatasetDocuments](raw/_short/api-aimiaobi-2023-08-01-searchdatasetdocuments-dc8b0ab1d58aa26c.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunPptOutlineGeneration

[RunPptOutlineGeneration](raw/_short/api-aimiaobi-2023-08-01-runpptoutlinegeneration-9b5a71de31898ea6.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetCategoriesByTaskId

[GetCategoriesByTaskId](raw/_short/api-aimiaobi-2023-08-01-getcategoriesbytaskid-694c03be06cc2d35.md)

get

\*全部资源

`*`

无

无

aimiaobi:GenerateExportWordTask

[GenerateExportWordTask](raw/_short/api-aimiaobi-2023-08-01-generateexportwordtask-95985f758c2f1e70.md)

get

\*全部资源

`*`

无

无

aimiaobi:QueryAuditTask

[QueryAuditTask](raw/_short/api-aimiaobi-2023-08-01-queryaudittask-e02e1f1166a11563.md)

get

\*全部资源

`*`

无

无

aimiaobi:AsyncEditTimeline

[AsyncEditTimeline](raw/_short/api-aimiaobi-2023-08-01-asyncedittimeline-d0c7f457f2d113b3.md)

update

\*全部资源

`*`

无

无

aimiaobi:ListWritingStyles

[ListWritingStyles](raw/_short/api-aimiaobi-2023-08-01-listwritingstyles-52bccb929c9fee6e.md)

list

\*全部资源

`*`

无

无

aimiaobi:CreateGeneratedContent

[CreateGeneratedContent](raw/_short/api-aimiaobi-2023-08-01-creategeneratedcontent-ab73761b0df9b458.md)

create

\*全部资源

`*`

无

无

aimiaobi:SubmitCustomHotTopicBroadcastJob

[SubmitCustomHotTopicBroadcastJob](raw/_short/api-aimiaobi-2023-08-01-submitcustomhottopicbroa-696f6e7806399ac7.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetDeepWriteTask

[GetDeepWriteTask](raw/_short/api-aimiaobi-2023-08-01-getdeepwritetask-c6c54c4400f43c73.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetGeneratedContent

[GetGeneratedContent](raw/_short/api-aimiaobi-2023-08-01-getgeneratedcontent-1909d9ce44a08b0b.md)

get

\*全部资源

`*`

无

无

aimiaobi:SubmitCustomSourceTopicAnalysis

[SubmitCustomSourceTopicAnalysis](raw/_short/api-aimiaobi-2023-08-01-submitcustomsourcetopica-1588b67464848f92.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetEnterpriseVocAnalysisTask

[GetEnterpriseVocAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-getenterprisevocanalysis-210c72887adca821.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunDeepWriting

[RunDeepWriting](raw/_short/api-aimiaobi-2023-08-01-rundeepwriting-ff148f017931e795.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunBookBrainmap

[RunBookBrainmap](raw/_short/api-aimiaobi-2023-08-01-runbookbrainmap-495cdb43a5e90c9a.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListSearchTasks

[ListSearchTasks](raw/_short/api-aimiaobi-2023-08-01-listsearchtasks-16cba5cd29273c99.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetPptConfig

[GetPptConfig](raw/_short/api-aimiaobi-2023-08-01-getpptconfig-52f53c774cb5add0.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunHotword

[RunHotword](raw/_short/api-aimiaobi-2023-08-01-runhotword-750e7a4a7db2266b.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListBiddingDoc

[ListBiddingDoc](raw/_short/api-aimiaobi-2023-08-01-listbiddingdoc-d296bfd7208fb3a9.md)

list

\*全部资源

`*`

无

无

aimiaobi:ListGeneratedContents

[ListGeneratedContents](raw/_short/api-aimiaobi-2023-08-01-listgeneratedcontents-80a3d80c1c5380c1.md)

list

\*全部资源

`*`

无

无

aimiaobi:ExportAnalysisTagDetailByTaskId

[ExportAnalysisTagDetailByTaskId](raw/_short/api-aimiaobi-2023-08-01-exportanalysistagdetailb-3fd7221595c0d2b0.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListStyleLearningResult

[ListStyleLearningResult](raw/_short/api-aimiaobi-2023-08-01-liststylelearningresult-39f16039f72598b1.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunSearchSimilarArticles

[RunSearchSimilarArticles](raw/_short/api-aimiaobi-2023-08-01-runsearchsimilararticles-bcda6f0ee4f20779.md)

none

\*全部资源

`*`

无

无

aimiaobi:GetSmartClipTask

[GetSmartClipTask](raw/_short/api-aimiaobi-2023-08-01-getsmartcliptask-37342952edacb40e.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetInterveneImportTaskInfo

[GetInterveneImportTaskInfo](raw/_short/api-aimiaobi-2023-08-01-getinterveneimporttaskin-7f7c6f974abcd47b.md)

get

\*全部资源

`*`

无

无

aimiaobi:CancelAsyncTask

[CancelAsyncTask](raw/_short/api-aimiaobi-2023-08-01-cancelasynctask-58375d56808add96.md)

update

\*全部资源

`*`

无

无

aimiaobi:AsyncUploadTenderDoc

[AsyncUploadTenderDoc](raw/_short/api-aimiaobi-2023-08-01-asyncuploadtenderdoc-7785704010a85310.md)

create

\*全部资源

`*`

无

无

aimiaobi:UpdateCustomText

[UpdateCustomText](raw/_short/api-aimiaobi-2023-08-01-updatecustomtext-1b28fa3c526a111e.md)

update

\*全部资源

`*`

无

无

aimiaobi:ListHotViewPoints

[ListHotViewPoints](raw/_short/api-aimiaobi-2023-08-01-listhotviewpoints-4e7aa5f65b1c8418.md)

list

\*全部资源

`*`

无

无

aimiaobi:QueryAsyncTask

[QueryAsyncTask](raw/_short/api-aimiaobi-2023-08-01-queryasynctask-8aa4356039580ce4.md)

get

\*全部资源

`*`

无

无

aimiaobi:DownloadAuditNote

[DownloadAuditNote](raw/_short/api-aimiaobi-2023-08-01-downloadauditnote-b2b15d4831e61bf7.md)

get

\*全部资源

`*`

无

无

aimiaobi:ImportInterveneFile

[ImportInterveneFile](raw/_short/api-aimiaobi-2023-08-01-importintervenefile-793880acb61b1871.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeleteCustomText

[DeleteCustomText](raw/_short/api-aimiaobi-2023-08-01-deletecustomtext-df47fb16e3e3db78.md)

delete

\*全部资源

`*`

无

无

aimiaobi:ExportHotTopicPlanningProposals

[ExportHotTopicPlanningProposals](raw/_short/api-aimiaobi-2023-08-01-exporthottopicplanningpr-4c72d53eedb8d622.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunDocSummary

[RunDocSummary](raw/_short/api-aimiaobi-2023-08-01-rundocsummary-93fed1072d326095.md)

get

\*全部资源

`*`

无

无

aimiaobi:SubmitEnterpriseVocAnalysisTask

[SubmitEnterpriseVocAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-submitenterprisevocanaly-d287f2bd7de3d396.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListDialogues

[ListDialogues](raw/_short/api-aimiaobi-2023-08-01-listdialogues-633f18a2791021db.md)

list

\*全部资源

`*`

无

无

aimiaobi:GenerateImageTask

[GenerateImageTask](raw/_short/api-aimiaobi-2023-08-01-generateimagetask-96a6665068d7d7a4.md)

create

\*全部资源

`*`

无

无

aimiaobi:SaveOrUpdateOssConfig

[SaveOrUpdateOssConfig](raw/_short/api-aimiaobi-2023-08-01-saveorupdateossconfig-1e5b39d94b913c47.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeleteDocs

[DeleteDocs](raw/_short/api-aimiaobi-2023-08-01-deletedocs-cb552930413a9a4f.md)

delete

\*全部资源

`*`

无

无

aimiaobi:ListHotNewsWithType

[ListHotNewsWithType](raw/_short/api-aimiaobi-2023-08-01-listhotnewswithtype-5ee22bfbb19de172.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunKeywordsExtractionGeneration

[RunKeywordsExtractionGeneration](raw/_short/api-aimiaobi-2023-08-01-runkeywordsextractiongen-a558548b4828a2a6.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunTranslateGeneration

[RunTranslateGeneration](raw/_short/api-aimiaobi-2023-08-01-runtranslategeneration-b780b5a3f4af697b.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunCustomHotTopicAnalysis

[RunCustomHotTopicAnalysis](raw/_short/api-aimiaobi-2023-08-01-runcustomhottopicanalysi-eee1c995bd24b8a9.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetTopicById

[GetTopicById](raw/_short/api-aimiaobi-2023-08-01-gettopicbyid-e2940091d7b12bdf.md)

get

\*全部资源

`*`

无

无

aimiaobi:DeleteCustomTopicViewPointById

[DeleteCustomTopicViewPointById](raw/_short/api-aimiaobi-2023-08-01-deletecustomtopicviewpoi-8d7a39d5cb24a64f.md)

delete

\*全部资源

`*`

无

无

aimiaobi:BindPptArtifact

[BindPptArtifact](raw/_short/api-aimiaobi-2023-08-01-bindpptartifact-4a67476f37b3d367.md)

create

\*全部资源

`*`

无

无

aimiaobi:InsertInterveneGlobalReply

[InsertInterveneGlobalReply](raw/_short/api-aimiaobi-2023-08-01-insertinterveneglobalrep-f0e6cc945d8afcb7.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeleteDatasetDocument

[DeleteDatasetDocument](raw/_short/api-aimiaobi-2023-08-01-deletedatasetdocument-9e9a8e3a4e6a76c3.md)

delete

\*全部资源

`*`

无

无

aimiaobi:ListSearchTaskDialogues

[ListSearchTaskDialogues](raw/_short/api-aimiaobi-2023-08-01-listsearchtaskdialogues-3d8d4525ce15ac3c.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetPptArtifactExportResult

[GetPptArtifactExportResult](raw/_short/api-aimiaobi-2023-08-01-getpptartifactexportresu-37a0f7509007c9b8.md)

create

\*全部资源

`*`

无

无

aimiaobi:AddDatasetDocument

[AddDatasetDocument](raw/_short/api-aimiaobi-2023-08-01-adddatasetdocument-d634038ff7246468.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListAuditTerms

[ListAuditTerms](raw/_short/api-aimiaobi-2023-08-01-listauditterms-0cdf6342a3c1ba2c.md)

list

\*全部资源

`*`

无

无

aimiaobi:SubmitVideoAudit

[SubmitVideoAudit](raw/_short/api-aimiaobi-2023-08-01-submitvideoaudit-f1daecd67484be9a.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListInterveneCnt

[ListInterveneCnt](raw/_short/api-aimiaobi-2023-08-01-listintervenecnt-ddf7e96fccd1cbaf.md)

list

\*全部资源

`*`

无

无

aimiaobi:ListCustomViewPoints

[ListCustomViewPoints](raw/_short/api-aimiaobi-2023-08-01-listcustomviewpoints-3e0955032d94655e.md)

list

\*全部资源

`*`

无

无

aimiaobi:SaveStyleLearningResult

[SaveStyleLearningResult](raw/_short/api-aimiaobi-2023-08-01-savestylelearningresult-56dac23f73924d93.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunSearchGeneration

[RunSearchGeneration](raw/_short/api-aimiaobi-2023-08-01-runsearchgeneration-008d7da322c502e5.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListEnterprisePptTemplates

[ListEnterprisePptTemplates](raw/_short/api-aimiaobi-2023-08-01-listenterpriseppttemplat-11fb38dc423d3cdc.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetTopicSelectionPerspectiveAnalysisTask

[GetTopicSelectionPerspectiveAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-gettopicselectionperspec-b259efa3e95830ee.md)

get

\*全部资源

`*`

无

无

aimiaobi:SaveDataSourceOrderConfig

[SaveDataSourceOrderConfig](raw/_short/api-aimiaobi-2023-08-01-savedatasourceorderconfi-11a35e9d66ef9dfb.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetBiddingRemainLimitNum

[GetBiddingRemainLimitNum](raw/_short/api-aimiaobi-2023-08-01-getbiddingremainlimitnum-e93ae2f1850d3bb1.md)

get

\*全部资源

`*`

无

无

aimiaobi:UploadBook

[UploadBook](raw/_short/api-aimiaobi-2023-08-01-uploadbook-50ae98ab14ff4412.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListPptArtifacts

[ListPptArtifacts](raw/_short/api-aimiaobi-2023-08-01-listpptartifacts-86ceeb78e8675d61.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetProperties

[GetProperties](raw/_short/api-aimiaobi-2023-08-01-getproperties-b79eceec87432e84.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListHotSources

[ListHotSources](raw/_short/api-aimiaobi-2023-08-01-listhotsources-2977aa404a278eec.md)

list

\*全部资源

`*`

无

无

aimiaobi:GenerateFileUrlByKey

[GenerateFileUrlByKey](raw/_short/api-aimiaobi-2023-08-01-generatefileurlbykey-43a4fbecc2395492.md)

get

\*全部资源

`*`

无

无

aimiaobi:EditAuditTerms

[EditAuditTerms](raw/_short/api-aimiaobi-2023-08-01-editauditterms-19833e85ab21ee1f.md)

update

\*全部资源

`*`

无

无

aimiaobi:ListAutoClipsTask

[ListAutoClipsTask](raw/_short/api-aimiaobi-2023-08-01-listautoclipstask-91cab23de98380bf.md)

list

\*全部资源

`*`

无

无

aimiaobi:ListBuildConfigs

[ListBuildConfigs](raw/_short/api-aimiaobi-2023-08-01-listbuildconfigs-3cc338f62bb472ca.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunWriteToneGeneration

[RunWriteToneGeneration](raw/_short/api-aimiaobi-2023-08-01-runwritetonegeneration-52d5e2eb7aceaffc.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetDataset

[GetDataset](raw/_short/api-aimiaobi-2023-08-01-getdataset-afa789c817f35796.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunBookSmartCard

[RunBookSmartCard](raw/_short/api-aimiaobi-2023-08-01-runbooksmartcard-fffc7fbdcf026ae2.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetPptInfo

[GetPptInfo](raw/_short/api-aimiaobi-2023-08-01-getpptinfo-7884360e080c1512.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeleteMaterialById

[DeleteMaterialById](raw/_short/api-aimiaobi-2023-08-01-deletematerialbyid-e1160cc591477f8c.md)

delete

\*全部资源

`*`

无

无

aimiaobi:ListIntervenes

[ListIntervenes](raw/_short/api-aimiaobi-2023-08-01-listintervenes-872b29b2fdaa31b7.md)

list

\*全部资源

`*`

无

无

aimiaobi:InitiatePptCreation

[InitiatePptCreation](raw/_short/api-aimiaobi-2023-08-01-initiatepptcreation-fb43bbeadaa03b4e.md)

create

\*全部资源

`*`

无

无

aimiaobi:SubmitSmartClipTask

[SubmitSmartClipTask](raw/_short/api-aimiaobi-2023-08-01-submitsmartcliptask-692691c843acd7e6.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunStepByStepWriting

[RunStepByStepWriting](raw/_short/api-aimiaobi-2023-08-01-runstepbystepwriting-334d441c5a2388c5.md)

create

\*全部资源

`*`

无

无

aimiaobi:FetchImageTask

[FetchImageTask](raw/_short/api-aimiaobi-2023-08-01-fetchimagetask-955891bc23019c34.md)

get

\*全部资源

`*`

无

无

aimiaobi:ExportPptArtifact

[ExportPptArtifact](raw/_short/api-aimiaobi-2023-08-01-exportpptartifact-3ab2c360f21119c8.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetCustomText

[GetCustomText](raw/_short/api-aimiaobi-2023-08-01-getcustomtext-f0aa71879c4ce9d6.md)

get

\*全部资源

`*`

无

无

aimiaobi:UploadDoc

[UploadDoc](raw/_short/api-aimiaobi-2023-08-01-uploaddoc-fc9dfbba774d5eb3.md)

create

\*全部资源

`*`

无

无

aimiaobi:QueryVideoAuditResult

[QueryVideoAuditResult](raw/_short/api-aimiaobi-2023-08-01-queryvideoauditresult-d063c7e865ff6788.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetStyleLearningResult

[GetStyleLearningResult](raw/_short/api-aimiaobi-2023-08-01-getstylelearningresult-456707d84adbf341.md)

get

\*全部资源

`*`

无

无

aimiaobi:UpdateGeneralConfig

[UpdateGeneralConfig](raw/_short/api-aimiaobi-2023-08-01-updategeneralconfig-a6333a8d0884350c.md)

update

\*全部资源

`*`

无

无

aimiaobi:AsyncCreateClipsTask

[AsyncCreateClipsTask](raw/_short/api-aimiaobi-2023-08-01-asynccreateclipstask-12435f3b2efae2e3.md)

create

\*全部资源

`*`

无

无

aimiaobi:CreateDataPermissions

[CreateDataPermissions](raw/_short/api-aimiaobi-2023-08-01-createdatapermissions-f2c3b1411dc813f2.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunQuickWriting

[RunQuickWriting](raw/_short/api-aimiaobi-2023-08-01-runquickwriting-0913fdae211015fe.md)

create

\*全部资源

`*`

无

无

aimiaobi:SubmitSmartAudit

[SubmitSmartAudit](raw/_short/api-aimiaobi-2023-08-01-submitsmartaudit-c9bb41d30ae288c1.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListVersions

[ListVersions](raw/_short/api-aimiaobi-2023-08-01-listversions-7e06722f5d06863e.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetInterveneRuleDetail

[GetInterveneRuleDetail](raw/_short/api-aimiaobi-2023-08-01-getinterveneruledetail-852eecc9a22c6a88.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunTopicSelectionMerge

[RunTopicSelectionMerge](raw/_short/api-aimiaobi-2023-08-01-runtopicselectionmerge-958f3d415ff349d3.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetFactAuditUrl

[GetFactAuditUrl](raw/_short/api-aimiaobi-2023-08-01-getfactauditurl-b88dfd44ccf55f6b.md)

delete

\*全部资源

`*`

无

无

aimiaobi:SaveCustomText

[SaveCustomText](raw/_short/api-aimiaobi-2023-08-01-savecustomtext-45514e1e2c987f11.md)

create

\*全部资源

`*`

无

无

aimiaobi:ExportIntervenes

[ExportIntervenes](raw/_short/api-aimiaobi-2023-08-01-exportintervenes-3684439a1506d245.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetHotTopicBroadcast

[GetHotTopicBroadcast](raw/_short/api-aimiaobi-2023-08-01-gethottopicbroadcast-d602ac9dc08f3c2e.md)

get

\*全部资源

`*`

无

无

aimiaobi:SubmitDeepWriteTask

[SubmitDeepWriteTask](raw/_short/api-aimiaobi-2023-08-01-submitdeepwritetask-d0829118e2b72254.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListSearchTaskDialogueDatas

[ListSearchTaskDialogueDatas](raw/_short/api-aimiaobi-2023-08-01-listsearchtaskdialogueda-40b8e7ed38a3461c.md)

list

\*全部资源

`*`

无

无

aimiaobi:ValidateUploadTemplate

[ValidateUploadTemplate](raw/_short/api-aimiaobi-2023-08-01-validateuploadtemplate-e42a1128a9b137bd.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunAiHelperWriting

[RunAiHelperWriting](raw/_short/api-aimiaobi-2023-08-01-runaihelperwriting-1492711ad2fd2716.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetDocClusterTask

[GetDocClusterTask](raw/_short/api-aimiaobi-2023-08-01-getdocclustertask-4888868ba4ccadaa.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunWritingV2

[RunWritingV2](raw/_short/api-aimiaobi-2023-08-01-runwritingv2-29d0abaf2738f46a.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListDatasets

[ListDatasets](raw/_short/api-aimiaobi-2023-08-01-listdatasets-2313cd6272804496.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunTextPolishing

[RunTextPolishing](raw/_short/api-aimiaobi-2023-08-01-runtextpolishing-9673d4832b2a38ee.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListDocumentRetrieve

[ListDocumentRetrieve](raw/_short/api-aimiaobi-2023-08-01-listdocumentretrieve-36263f723f8bc86b.md)

list

\*全部资源

`*`

无

无

aimiaobi:SubmitAuditNote

[SubmitAuditNote](raw/_short/api-aimiaobi-2023-08-01-submitauditnote-d429bd0fa8ba411a.md)

none

\*全部资源

`*`

无

无

aimiaobi:ExportCustomSourceAnalysisTask

[ExportCustomSourceAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-exportcustomsourceanalys-67d4a70d158d53c4.md)

get

\*全部资源

`*`

无

无

aimiaobi:FetchExportWordTask

[FetchExportWordTask](raw/_short/api-aimiaobi-2023-08-01-fetchexportwordtask-bb378dad8224a696.md)

get

\*全部资源

`*`

无

无

aimiaobi:DownloadBiddingDoc

[DownloadBiddingDoc](raw/_short/api-aimiaobi-2023-08-01-downloadbiddingdoc-96709e9db4f8d2de.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunVideoScriptGenerate

[RunVideoScriptGenerate](raw/_short/api-aimiaobi-2023-08-01-runvideoscriptgenerate-184c90127ca3e802.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListAnalysisTagDetailByTaskId

[ListAnalysisTagDetailByTaskId](raw/_short/api-aimiaobi-2023-08-01-listanalysistagdetailbyt-6d37c9bfa9675c69.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListTopicRecommendEventList

[ListTopicRecommendEventList](raw/_short/api-aimiaobi-2023-08-01-listtopicrecommendeventl-571464d0d7dbac01.md)

list

\*全部资源

`*`

无

无

aimiaobi:AsyncWritingBiddingDoc

[AsyncWritingBiddingDoc](raw/_short/api-aimiaobi-2023-08-01-asyncwritingbiddingdoc-82200a3e98741182.md)

create

\*全部资源

`*`

无

无

aimiaobi:SubmitExportTermsTask

[SubmitExportTermsTask](raw/_short/api-aimiaobi-2023-08-01-submitexporttermstask-4713f23ec141d82e.md)

none

\*全部资源

`*`

无

无

aimiaobi:GetCustomTopicSelectionPerspectiveAnalysisTask

[GetCustomTopicSelectionPerspectiveAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-getcustomtopicselectionp-9d02679b5ad8c643.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetCustomHotTopicBroadcastJob

[GetCustomHotTopicBroadcastJob](raw/_short/api-aimiaobi-2023-08-01-getcustomhottopicbroadca-7518d2dff5cab560.md)

get

\*全部资源

`*`

无

无

aimiaobi:DeleteStyleLearningResult

[DeleteStyleLearningResult](raw/_short/api-aimiaobi-2023-08-01-deletestylelearningresul-c94fd4b7dfe5101b.md)

delete

\*全部资源

`*`

无

无

aimiaobi:UpdateDataset

[UpdateDataset](raw/_short/api-aimiaobi-2023-08-01-updatedataset-4e703cba19f41d7d.md)

update

\*全部资源

`*`

无

无

aimiaobi:ListPptTemplates

[ListPptTemplates](raw/_short/api-aimiaobi-2023-08-01-listppttemplates-49fdbe4a26736e15.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetPptArtifact

[GetPptArtifact](raw/_short/api-aimiaobi-2023-08-01-getpptartifact-05d70ce3defd7029.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetDeepWriteTaskResult

[GetDeepWriteTaskResult](raw/_short/api-aimiaobi-2023-08-01-getdeepwritetaskresult-c4aa5ce1a27de345.md)

get

\*全部资源

`*`

无

无

aimiaobi:FetchExportTermsTask

[FetchExportTermsTask](raw/_short/api-aimiaobi-2023-08-01-fetchexporttermstask-a316ab339965da1d.md)

none

\*全部资源

`*`

无

无

aimiaobi:GetAvailableAuditNotes

[GetAvailableAuditNotes](raw/_short/api-aimiaobi-2023-08-01-getavailableauditnotes-17f54efd8b06c91c.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunAbbreviationContent

[RunAbbreviationContent](raw/_short/api-aimiaobi-2023-08-01-runabbreviationcontent-9d4883501cf8bfb9.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetInterveneTemplateFileUrl

[GetInterveneTemplateFileUrl](raw/_short/api-aimiaobi-2023-08-01-getintervenetemplatefile-f8fabdf8a7a17100.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunContinueContent

[RunContinueContent](raw/_short/api-aimiaobi-2023-08-01-runcontinuecontent-2253fd16575800be.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetGeneralConfig

[GetGeneralConfig](raw/_short/api-aimiaobi-2023-08-01-getgeneralconfig-122f3097253cebd4.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListPlanningProposal

[ListPlanningProposal](raw/_short/api-aimiaobi-2023-08-01-listplanningproposal-1a619658c92c5fbf.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetAuditNoteProcessingStatus

[GetAuditNoteProcessingStatus](raw/_short/api-aimiaobi-2023-08-01-getauditnoteprocessingst-42f3952de60d4eaf.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetAuditNotePostProcessingStatus

[GetAuditNotePostProcessingStatus](raw/_short/api-aimiaobi-2023-08-01-getauditnotepostprocessi-10b0d630c7d4777f.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListTimedViewAttitude

[ListTimedViewAttitude](raw/_short/api-aimiaobi-2023-08-01-listtimedviewattitude-a66456e6ac87d8c2.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunSummaryGenerate

[RunSummaryGenerate](raw/_short/api-aimiaobi-2023-08-01-runsummarygenerate-6d8d20235b9716a2.md)

get

\*全部资源

`*`

无

无

aimiaobi:FetchImportTermsTask

[FetchImportTermsTask](raw/_short/api-aimiaobi-2023-08-01-fetchimporttermstask-3e325a59df01c370.md)

none

\*全部资源

`*`

无

无

aimiaobi:RunDocBrainmap

[RunDocBrainmap](raw/_short/api-aimiaobi-2023-08-01-rundocbrainmap-c4b3bc56029576ba.md)

get

\*全部资源

`*`

无

无

aimiaobi:DeleteDataPermissions

[DeleteDataPermissions](raw/_short/api-aimiaobi-2023-08-01-deletedatapermissions-f908866cf49c5d10.md)

delete

\*全部资源

`*`

无

无

aimiaobi:RunBookIntroduction

[RunBookIntroduction](raw/_short/api-aimiaobi-2023-08-01-runbookintroduction-932b09ce0ede16e1.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetBiddingDocInfo

[GetBiddingDocInfo](raw/_short/api-aimiaobi-2023-08-01-getbiddingdocinfo-25fab3d029976395.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListGeneralConfigs

[ListGeneralConfigs](raw/_short/api-aimiaobi-2023-08-01-listgeneralconfigs-a889bc46882e86e6.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunMultiDocIntroduction

[RunMultiDocIntroduction](raw/_short/api-aimiaobi-2023-08-01-runmultidocintroduction-bc4c44fecdb736c9.md)

get

\*全部资源

`*`

无

无

aimiaobi:SubmitAsyncTask

[SubmitAsyncTask](raw/_short/api-aimiaobi-2023-08-01-submitasynctask-b8e07c70487ee1e2.md)

create

\*全部资源

`*`

无

无

aimiaobi:UpdateDatasetDocument

[UpdateDatasetDocument](raw/_short/api-aimiaobi-2023-08-01-updatedatasetdocument-18ab686c5f35fc8b.md)

update

\*全部资源

`*`

无

无

aimiaobi:RunExpandContent

[RunExpandContent](raw/_short/api-aimiaobi-2023-08-01-runexpandcontent-a2bbe2a2a1bf2f84.md)

get

\*全部资源

`*`

无

无

aimiaobi:GenerateUploadConfig

[GenerateUploadConfig](raw/_short/api-aimiaobi-2023-08-01-generateuploadconfig-6bb22e9b8a3c683c.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunTitleGeneration

[RunTitleGeneration](raw/_short/api-aimiaobi-2023-08-01-runtitlegeneration-dce82a814e9d2d49.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListAsyncTasks

[ListAsyncTasks](raw/_short/api-aimiaobi-2023-08-01-listasynctasks-b4270d078065c3ba.md)

list

\*全部资源

`*`

无

无

aimiaobi:ExportGeneratedContent

[ExportGeneratedContent](raw/_short/api-aimiaobi-2023-08-01-exportgeneratedcontent-16c0c93e55633e9f.md)

get

\*全部资源

`*`

无

无

aimiaobi:ConfirmAndPostProcessAuditNote

[ConfirmAndPostProcessAuditNote](raw/_short/api-aimiaobi-2023-08-01-confirmandpostprocessaud-02f771c9a5326671.md)

none

\*全部资源

`*`

无

无

aimiaobi:GetMaterialById

[GetMaterialById](raw/_short/api-aimiaobi-2023-08-01-getmaterialbyid-a41e3f081d3b690f.md)

get

\*全部资源

`*`

无

无

aimiaobi:DeleteGeneralConfig

[DeleteGeneralConfig](raw/_short/api-aimiaobi-2023-08-01-deletegeneralconfig-e2d486a6149dc804.md)

delete

\*全部资源

`*`

无

无

aimiaobi:GetFileContentLength

[GetFileContentLength](raw/_short/api-aimiaobi-2023-08-01-getfilecontentlength-1f70516ba56bd5fd.md)

get

\*全部资源

`*`

无

无

aimiaobi:CancelAuditTask

[CancelAuditTask](raw/_short/api-aimiaobi-2023-08-01-cancelaudittask-954a245fd407b59f.md)

update

\*全部资源

`*`

无

无

aimiaobi:SubmitDocClusterTask

[SubmitDocClusterTask](raw/_short/api-aimiaobi-2023-08-01-submitdocclustertask-997ad9822426e716.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeleteFactAuditUrl

[DeleteFactAuditUrl](raw/_short/api-aimiaobi-2023-08-01-deletefactauditurl-7c2603d348156de8.md)

delete

\*全部资源

`*`

无

无

aimiaobi:EditBiddingDoc

[EditBiddingDoc](raw/_short/api-aimiaobi-2023-08-01-editbiddingdoc-f0c191cc201bd6cf.md)

update

\*全部资源

`*`

无

无

aimiaobi:SubmitAuditTask

[SubmitAuditTask](raw/_short/api-aimiaobi-2023-08-01-submitaudittask-aa18a0881f0d21ab.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetDocInfo

[GetDocInfo](raw/_short/api-aimiaobi-2023-08-01-getdocinfo-1792f23538478a5f.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetPptTemplateSelector

[GetPptTemplateSelector](raw/_short/api-aimiaobi-2023-08-01-getppttemplateselector-1a17a431df471928.md)

create

\*全部资源

`*`

无

无

aimiaobi:SearchNews

[SearchNews](raw/_short/api-aimiaobi-2023-08-01-searchnews-a4ff1a25537b0ca8.md)

list

\*全部资源

`*`

无

无

aimiaobi:ExportAuditContentResult

[ExportAuditContentResult](raw/_short/api-aimiaobi-2023-08-01-exportauditcontentresult-5d43ee5b856f6e26.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunDocQa

[RunDocQa](raw/_short/api-aimiaobi-2023-08-01-rundocqa-dd1ebcfbe739f1b9.md)

get

\*全部资源

`*`

无

无

aimiaobi:SubmitFactAuditUrl

[SubmitFactAuditUrl](raw/_short/api-aimiaobi-2023-08-01-submitfactauditurl-50ef7c2f7fbcdd5a.md)

create

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
