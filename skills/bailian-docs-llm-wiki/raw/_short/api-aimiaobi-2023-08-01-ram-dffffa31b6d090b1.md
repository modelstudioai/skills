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

[RunDocTranslation](raw/_short/api-aimiaobi-2023-08-01-rundoctranslation-31e4461fd87a5ffb.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunWriting

[RunWriting](raw/_short/api-aimiaobi-2023-08-01-runwriting-5e97e8ba3ea2e785.md)

create

\*全部资源

`*`

无

无

aimiaobi:InitiatePptCreationV2

[InitiatePptCreationV2](raw/_short/api-aimiaobi-2023-08-01-initiatepptcreationv2-89f1190e9dc82ba3.md)

create

\*全部资源

`*`

无

无

aimiaobi:DocumentExtraction

[DocumentExtraction](raw/_short/api-aimiaobi-2023-08-01-documentextraction-aa864d298372391a.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListTopicViewPointRecommendEventList

[ListTopicViewPointRecommendEventList](raw/_short/api-aimiaobi-2023-08-01-listtopicviewpointrecomm-71836941fef7f644.md)

list

\*全部资源

`*`

无

无

aimiaobi:SubmitImportTermsTask

[SubmitImportTermsTask](raw/_short/api-aimiaobi-2023-08-01-submitimporttermstask-a5e8e8627cfa2b43.md)

none

\*全部资源

`*`

无

无

aimiaobi:RunGenerateQuestions

[RunGenerateQuestions](raw/_short/api-aimiaobi-2023-08-01-rungeneratequestions-7cf400348adb2544.md)

get

\*全部资源

`*`

无

无

aimiaobi:DeleteCustomTopicByTopic

[DeleteCustomTopicByTopic](raw/_short/api-aimiaobi-2023-08-01-deletecustomtopicbytopic-0b9cd39aeb957af4.md)

delete

\*全部资源

`*`

无

无

aimiaobi:RunStyleFeatureAnalysis

[RunStyleFeatureAnalysis](raw/_short/api-aimiaobi-2023-08-01-runstylefeatureanalysis-9944b2eede7623b9.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetAutoClipsTaskInfo

[GetAutoClipsTaskInfo](raw/_short/api-aimiaobi-2023-08-01-getautoclipstaskinfo-a6fc5ba7dfd32888.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunCustomHotTopicViewPointAnalysis

[RunCustomHotTopicViewPointAnalysis](raw/_short/api-aimiaobi-2023-08-01-runcustomhottopicviewpoi-ed90e405982fea66.md)

create

\*全部资源

`*`

无

无

aimiaobi:AsyncUploadVideo

[AsyncUploadVideo](raw/_short/api-aimiaobi-2023-08-01-asyncuploadvideo-9f3f37ee9ab819ca.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeleteGeneratedContent

[DeleteGeneratedContent](raw/_short/api-aimiaobi-2023-08-01-deletegeneratedcontent-34f0916fae2b2468.md)

delete

\*全部资源

`*`

无

无

aimiaobi:SaveMaterialDocument

[SaveMaterialDocument](raw/_short/api-aimiaobi-2023-08-01-savematerialdocument-c9fe1c0e21a3e01f.md)

create

\*全部资源

`*`

无

无

aimiaobi:AsyncCreateClipsTimeLine

[AsyncCreateClipsTimeLine](raw/_short/api-aimiaobi-2023-08-01-asynccreateclipstimeline-2a7e2aa5dfe9623f.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListMaterialDocuments

[ListMaterialDocuments](raw/_short/api-aimiaobi-2023-08-01-listmaterialdocuments-d2cab230af7fc017.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetCustomSourceTopicAnalysisTask

[GetCustomSourceTopicAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-getcustomsourcetopicanal-eb47231ec72f7dad.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListFreshViewPoints

[ListFreshViewPoints](raw/_short/api-aimiaobi-2023-08-01-listfreshviewpoints-5ac76a5b6c3f4436.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetInterveneGlobalReply

[GetInterveneGlobalReply](raw/_short/api-aimiaobi-2023-08-01-getinterveneglobalreply-cea7cb5dcdfaf5ab.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListDocs

[ListDocs](raw/_short/api-aimiaobi-2023-08-01-listdocs-726e0c28b9af37d5.md)

list

\*全部资源

`*`

无

无

aimiaobi:AddAuditTerms

[AddAuditTerms](raw/_short/api-aimiaobi-2023-08-01-addauditterms-c2e7e65e3718af44.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeleteDataset

[DeleteDataset](raw/_short/api-aimiaobi-2023-08-01-deletedataset-0ec7388963806422.md)

delete

\*全部资源

`*`

无

无

aimiaobi:ListAuditContentErrorTypes

[ListAuditContentErrorTypes](raw/_short/api-aimiaobi-2023-08-01-listauditcontenterrortyp-dc8a1e855346739b.md)

list

\*全部资源

`*`

无

无

aimiaobi:DeleteInterveneRule

[DeleteInterveneRule](raw/_short/api-aimiaobi-2023-08-01-deleteintervenerule-85d7c16bea7a6615.md)

delete

\*全部资源

`*`

无

无

aimiaobi:UpdateMaterialDocument

[UpdateMaterialDocument](raw/_short/api-aimiaobi-2023-08-01-updatematerialdocument-a325206d60bcfb13.md)

update

\*全部资源

`*`

无

无

aimiaobi:ListDatasetDocuments

[ListDatasetDocuments](raw/_short/api-aimiaobi-2023-08-01-listdatasetdocuments-ceeb17246b42816b.md)

list

\*全部资源

`*`

无

无

aimiaobi:GenerateViewPoint

[GenerateViewPoint](raw/_short/api-aimiaobi-2023-08-01-generateviewpoint-2bad7e470e8c9975.md)

list

\*全部资源

`*`

无

无

aimiaobi:CreateDataset

[CreateDataset](raw/_short/api-aimiaobi-2023-08-01-createdataset-1f6c6af171e2174b.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetClipsBuildInResource

[GetClipsBuildInResource](raw/_short/api-aimiaobi-2023-08-01-getclipsbuildinresource-d1ab0d82b9ba11de.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetSmartAuditResult

[GetSmartAuditResult](raw/_short/api-aimiaobi-2023-08-01-getsmartauditresult-d5d51df64c9a539b.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunCommentGeneration

[RunCommentGeneration](raw/_short/api-aimiaobi-2023-08-01-runcommentgeneration-14291096fd211b29.md)

get

\*全部资源

`*`

无

无

aimiaobi:InsertInterveneRule

[InsertInterveneRule](raw/_short/api-aimiaobi-2023-08-01-insertintervenerule-5f3a709565c0df27.md)

create

\*全部资源

`*`

无

无

aimiaobi:CreateGeneralConfig

[CreateGeneralConfig](raw/_short/api-aimiaobi-2023-08-01-creategeneralconfig-86f4dc453b9743a3.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetDatasetDocument

[GetDatasetDocument](raw/_short/api-aimiaobi-2023-08-01-getdatasetdocument-53e494d1732896c8.md)

get

\*全部资源

`*`

无

无

aimiaobi:ClearIntervenes

[ClearIntervenes](raw/_short/api-aimiaobi-2023-08-01-clearintervenes-aa9df2177225ab48.md)

delete

\*全部资源

`*`

无

无

aimiaobi:ListDataPermissions

[ListDataPermissions](raw/_short/api-aimiaobi-2023-08-01-listdatapermissions-221440708fc649f4.md)

list

\*全部资源

`*`

无

无

aimiaobi:ListCustomText

[ListCustomText](raw/_short/api-aimiaobi-2023-08-01-listcustomtext-b5954f5a136d9fb9.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunDocSmartCard

[RunDocSmartCard](raw/_short/api-aimiaobi-2023-08-01-rundocsmartcard-0237f0e317daae40.md)

get

\*全部资源

`*`

无

无

aimiaobi:UpdateGeneratedContent

[UpdateGeneratedContent](raw/_short/api-aimiaobi-2023-08-01-updategeneratedcontent-408a790e4f35aba5.md)

update

\*全部资源

`*`

无

无

aimiaobi:GetDataSourceOrderConfig

[GetDataSourceOrderConfig](raw/_short/api-aimiaobi-2023-08-01-getdatasourceorderconfig-02dd0b2876015623.md)

get

\*全部资源

`*`

无

无

aimiaobi:SubmitTopicSelectionPerspectiveAnalysisTask

[SubmitTopicSelectionPerspectiveAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-submittopicselectionpers-122ab8b66568eb05.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListInterveneRules

[ListInterveneRules](raw/_short/api-aimiaobi-2023-08-01-listintervenerules-b783831749be3506.md)

list

\*全部资源

`*`

无

无

aimiaobi:ListHotTopics

[ListHotTopics](raw/_short/api-aimiaobi-2023-08-01-listhottopics-c4f5349d89ca55f4.md)

list

\*全部资源

`*`

无

无

aimiaobi:SubmitCustomTopicSelectionPerspectiveAnalysisTask

[SubmitCustomTopicSelectionPerspectiveAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-submitcustomtopicselecti-e062bab5658516ce.md)

create

\*全部资源

`*`

无

无

aimiaobi:CreateToken

[CreateToken](raw/_short/api-aimiaobi-2023-08-01-createtoken-981cf209302c80d5.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunDocIntroduction

[RunDocIntroduction](raw/_short/api-aimiaobi-2023-08-01-rundocintroduction-10faef44b834783f.md)

get

\*全部资源

`*`

无

无

aimiaobi:CancelDeepWriteTask

[CancelDeepWriteTask](raw/_short/api-aimiaobi-2023-08-01-canceldeepwritetask-6fbb6df1c9f568b7.md)

update

\*全部资源

`*`

无

无

aimiaobi:DeleteAuditTerms

[DeleteAuditTerms](raw/_short/api-aimiaobi-2023-08-01-deleteauditterms-dcec0441ef3384b0.md)

delete

\*全部资源

`*`

无

无

aimiaobi:FeedbackDialogue

[FeedbackDialogue](raw/_short/api-aimiaobi-2023-08-01-feedbackdialogue-924bdb6696987000.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListWebReviewPoints

[ListWebReviewPoints](raw/_short/api-aimiaobi-2023-08-01-listwebreviewpoints-3943abfd6701e5cd.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunDocWashing

[RunDocWashing](raw/_short/api-aimiaobi-2023-08-01-rundocwashing-c04c4d4024297e9e.md)

get

\*全部资源

`*`

无

无

aimiaobi:DeleteAuditNote

[DeleteAuditNote](raw/_short/api-aimiaobi-2023-08-01-deleteauditnote-7c2265362fc1e2b7.md)

delete

\*全部资源

`*`

无

无

aimiaobi:ImportInterveneFileAsync

[ImportInterveneFileAsync](raw/_short/api-aimiaobi-2023-08-01-importintervenefileasync-34c43150e55a6512.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeletePptArtifact

[DeletePptArtifact](raw/_short/api-aimiaobi-2023-08-01-deletepptartifact-2c9c2c6cefcc45cd.md)

delete

\*全部资源

`*`

无

无

aimiaobi:SearchDatasetDocuments

[SearchDatasetDocuments](raw/_short/api-aimiaobi-2023-08-01-searchdatasetdocuments-a4c30deb56fbfd19.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunPptOutlineGeneration

[RunPptOutlineGeneration](raw/_short/api-aimiaobi-2023-08-01-runpptoutlinegeneration-7bb578387e9124a4.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetCategoriesByTaskId

[GetCategoriesByTaskId](raw/_short/api-aimiaobi-2023-08-01-getcategoriesbytaskid-29e8a5a3ec522b51.md)

get

\*全部资源

`*`

无

无

aimiaobi:GenerateExportWordTask

[GenerateExportWordTask](raw/_short/api-aimiaobi-2023-08-01-generateexportwordtask-4ded5df79af1a93e.md)

get

\*全部资源

`*`

无

无

aimiaobi:QueryAuditTask

[QueryAuditTask](raw/_short/api-aimiaobi-2023-08-01-queryaudittask-4649ac6969ac59fc.md)

get

\*全部资源

`*`

无

无

aimiaobi:AsyncEditTimeline

[AsyncEditTimeline](raw/_short/api-aimiaobi-2023-08-01-asyncedittimeline-420f22884628bd96.md)

update

\*全部资源

`*`

无

无

aimiaobi:ListWritingStyles

[ListWritingStyles](raw/_short/api-aimiaobi-2023-08-01-listwritingstyles-00ef4732c20d15a3.md)

list

\*全部资源

`*`

无

无

aimiaobi:CreateGeneratedContent

[CreateGeneratedContent](raw/_short/api-aimiaobi-2023-08-01-creategeneratedcontent-7d826fa65c957a57.md)

create

\*全部资源

`*`

无

无

aimiaobi:SubmitCustomHotTopicBroadcastJob

[SubmitCustomHotTopicBroadcastJob](raw/_short/api-aimiaobi-2023-08-01-submitcustomhottopicbroa-ef63e50230f3647a.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetDeepWriteTask

[GetDeepWriteTask](raw/_short/api-aimiaobi-2023-08-01-getdeepwritetask-2445f319d2d961c8.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetGeneratedContent

[GetGeneratedContent](raw/_short/api-aimiaobi-2023-08-01-getgeneratedcontent-2b1bcf044ca9bcc2.md)

get

\*全部资源

`*`

无

无

aimiaobi:SubmitCustomSourceTopicAnalysis

[SubmitCustomSourceTopicAnalysis](raw/_short/api-aimiaobi-2023-08-01-submitcustomsourcetopica-205245308ab89fe9.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetEnterpriseVocAnalysisTask

[GetEnterpriseVocAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-getenterprisevocanalysis-007980209765d6cc.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunDeepWriting

[RunDeepWriting](raw/_short/api-aimiaobi-2023-08-01-rundeepwriting-5745e4d86a24743c.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunBookBrainmap

[RunBookBrainmap](raw/_short/api-aimiaobi-2023-08-01-runbookbrainmap-6df4d57ebb0aa70e.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListSearchTasks

[ListSearchTasks](raw/_short/api-aimiaobi-2023-08-01-listsearchtasks-3ff96b450681db57.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetPptConfig

[GetPptConfig](raw/_short/api-aimiaobi-2023-08-01-getpptconfig-f664f98d565e54f9.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunHotword

[RunHotword](raw/_short/api-aimiaobi-2023-08-01-runhotword-027ef76322241544.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListBiddingDoc

[ListBiddingDoc](raw/_short/api-aimiaobi-2023-08-01-listbiddingdoc-ca714519e77804be.md)

list

\*全部资源

`*`

无

无

aimiaobi:ListGeneratedContents

[ListGeneratedContents](raw/_short/api-aimiaobi-2023-08-01-listgeneratedcontents-88d7de02c6ba070f.md)

list

\*全部资源

`*`

无

无

aimiaobi:ExportAnalysisTagDetailByTaskId

[ExportAnalysisTagDetailByTaskId](raw/_short/api-aimiaobi-2023-08-01-exportanalysistagdetailb-b8456d8de7d22dff.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListStyleLearningResult

[ListStyleLearningResult](raw/_short/api-aimiaobi-2023-08-01-liststylelearningresult-6c5e1f83a5872222.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunSearchSimilarArticles

[RunSearchSimilarArticles](raw/_short/api-aimiaobi-2023-08-01-runsearchsimilararticles-0ba6542b93a5e56d.md)

none

\*全部资源

`*`

无

无

aimiaobi:GetSmartClipTask

[GetSmartClipTask](raw/_short/api-aimiaobi-2023-08-01-getsmartcliptask-c9166cfc941760b9.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetInterveneImportTaskInfo

[GetInterveneImportTaskInfo](raw/_short/api-aimiaobi-2023-08-01-getinterveneimporttaskin-3a75bb78582f514b.md)

get

\*全部资源

`*`

无

无

aimiaobi:CancelAsyncTask

[CancelAsyncTask](raw/_short/api-aimiaobi-2023-08-01-cancelasynctask-cff6e72978ed6068.md)

update

\*全部资源

`*`

无

无

aimiaobi:AsyncUploadTenderDoc

[AsyncUploadTenderDoc](raw/_short/api-aimiaobi-2023-08-01-asyncuploadtenderdoc-c44972bda9d77b18.md)

create

\*全部资源

`*`

无

无

aimiaobi:UpdateCustomText

[UpdateCustomText](raw/_short/api-aimiaobi-2023-08-01-updatecustomtext-8c266521c9515813.md)

update

\*全部资源

`*`

无

无

aimiaobi:ListHotViewPoints

[ListHotViewPoints](raw/_short/api-aimiaobi-2023-08-01-listhotviewpoints-f5b56834fe3de5e8.md)

list

\*全部资源

`*`

无

无

aimiaobi:QueryAsyncTask

[QueryAsyncTask](raw/_short/api-aimiaobi-2023-08-01-queryasynctask-882ed78b81e346f5.md)

get

\*全部资源

`*`

无

无

aimiaobi:DownloadAuditNote

[DownloadAuditNote](raw/_short/api-aimiaobi-2023-08-01-downloadauditnote-02e275cb53c50d03.md)

get

\*全部资源

`*`

无

无

aimiaobi:ImportInterveneFile

[ImportInterveneFile](raw/_short/api-aimiaobi-2023-08-01-importintervenefile-a4d65125f35c2f6b.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeleteCustomText

[DeleteCustomText](raw/_short/api-aimiaobi-2023-08-01-deletecustomtext-49ecdbe276c7d043.md)

delete

\*全部资源

`*`

无

无

aimiaobi:ExportHotTopicPlanningProposals

[ExportHotTopicPlanningProposals](raw/_short/api-aimiaobi-2023-08-01-exporthottopicplanningpr-87a00d2165ad9bf3.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunDocSummary

[RunDocSummary](raw/_short/api-aimiaobi-2023-08-01-rundocsummary-747d3826b5a072aa.md)

get

\*全部资源

`*`

无

无

aimiaobi:SubmitEnterpriseVocAnalysisTask

[SubmitEnterpriseVocAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-submitenterprisevocanaly-3dc1a2175631556e.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListDialogues

[ListDialogues](raw/_short/api-aimiaobi-2023-08-01-listdialogues-61cfb60e703e2024.md)

list

\*全部资源

`*`

无

无

aimiaobi:GenerateImageTask

[GenerateImageTask](raw/_short/api-aimiaobi-2023-08-01-generateimagetask-081ae48bd13db383.md)

create

\*全部资源

`*`

无

无

aimiaobi:SaveOrUpdateOssConfig

[SaveOrUpdateOssConfig](raw/_short/api-aimiaobi-2023-08-01-saveorupdateossconfig-90d3b00a842fbe4f.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeleteDocs

[DeleteDocs](raw/_short/api-aimiaobi-2023-08-01-deletedocs-cde7906f2c831321.md)

delete

\*全部资源

`*`

无

无

aimiaobi:ListHotNewsWithType

[ListHotNewsWithType](raw/_short/api-aimiaobi-2023-08-01-listhotnewswithtype-65411800b9013884.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunKeywordsExtractionGeneration

[RunKeywordsExtractionGeneration](raw/_short/api-aimiaobi-2023-08-01-runkeywordsextractiongen-5ec2ef5a48d0ee19.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunTranslateGeneration

[RunTranslateGeneration](raw/_short/api-aimiaobi-2023-08-01-runtranslategeneration-2f8d19c9f2356b75.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunCustomHotTopicAnalysis

[RunCustomHotTopicAnalysis](raw/_short/api-aimiaobi-2023-08-01-runcustomhottopicanalysi-8bd7a8fe36026851.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetTopicById

[GetTopicById](raw/_short/api-aimiaobi-2023-08-01-gettopicbyid-cec5b365c1dfb4bf.md)

get

\*全部资源

`*`

无

无

aimiaobi:DeleteCustomTopicViewPointById

[DeleteCustomTopicViewPointById](raw/_short/api-aimiaobi-2023-08-01-deletecustomtopicviewpoi-1b44cc137249a490.md)

delete

\*全部资源

`*`

无

无

aimiaobi:BindPptArtifact

[BindPptArtifact](raw/_short/api-aimiaobi-2023-08-01-bindpptartifact-9ab377fb301d3f3f.md)

create

\*全部资源

`*`

无

无

aimiaobi:InsertInterveneGlobalReply

[InsertInterveneGlobalReply](raw/_short/api-aimiaobi-2023-08-01-insertinterveneglobalrep-298cfcee20646204.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeleteDatasetDocument

[DeleteDatasetDocument](raw/_short/api-aimiaobi-2023-08-01-deletedatasetdocument-c2d21ec292e79729.md)

delete

\*全部资源

`*`

无

无

aimiaobi:ListSearchTaskDialogues

[ListSearchTaskDialogues](raw/_short/api-aimiaobi-2023-08-01-listsearchtaskdialogues-f99b815c8643ed2b.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetPptArtifactExportResult

[GetPptArtifactExportResult](raw/_short/api-aimiaobi-2023-08-01-getpptartifactexportresu-16475c338abc9043.md)

create

\*全部资源

`*`

无

无

aimiaobi:AddDatasetDocument

[AddDatasetDocument](raw/_short/api-aimiaobi-2023-08-01-adddatasetdocument-9b751b0f9ec6b91e.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListAuditTerms

[ListAuditTerms](raw/_short/api-aimiaobi-2023-08-01-listauditterms-1cf5da35bc82f01e.md)

list

\*全部资源

`*`

无

无

aimiaobi:SubmitVideoAudit

[SubmitVideoAudit](raw/_short/api-aimiaobi-2023-08-01-submitvideoaudit-b7445c8adb8a8d2a.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListInterveneCnt

[ListInterveneCnt](raw/_short/api-aimiaobi-2023-08-01-listintervenecnt-2d93b76026d1ed5f.md)

list

\*全部资源

`*`

无

无

aimiaobi:ListCustomViewPoints

[ListCustomViewPoints](raw/_short/api-aimiaobi-2023-08-01-listcustomviewpoints-2498b20aeb2e3417.md)

list

\*全部资源

`*`

无

无

aimiaobi:SaveStyleLearningResult

[SaveStyleLearningResult](raw/_short/api-aimiaobi-2023-08-01-savestylelearningresult-da5242a6d765f766.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunSearchGeneration

[RunSearchGeneration](raw/_short/api-aimiaobi-2023-08-01-runsearchgeneration-9f952fe3b300d756.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListEnterprisePptTemplates

[ListEnterprisePptTemplates](raw/_short/api-aimiaobi-2023-08-01-listenterpriseppttemplat-0f6af38d590d2725.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetTopicSelectionPerspectiveAnalysisTask

[GetTopicSelectionPerspectiveAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-gettopicselectionperspec-ef7ec32a61ba11fd.md)

get

\*全部资源

`*`

无

无

aimiaobi:SaveDataSourceOrderConfig

[SaveDataSourceOrderConfig](raw/_short/api-aimiaobi-2023-08-01-savedatasourceorderconfi-da7481b7bb79267c.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetBiddingRemainLimitNum

[GetBiddingRemainLimitNum](raw/_short/api-aimiaobi-2023-08-01-getbiddingremainlimitnum-3d1bd6af4806959d.md)

get

\*全部资源

`*`

无

无

aimiaobi:UploadBook

[UploadBook](raw/_short/api-aimiaobi-2023-08-01-uploadbook-70a69960e8a10bde.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListPptArtifacts

[ListPptArtifacts](raw/_short/api-aimiaobi-2023-08-01-listpptartifacts-f05d5c55d265b07f.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetProperties

[GetProperties](raw/_short/api-aimiaobi-2023-08-01-getproperties-227db200efb65951.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListHotSources

[ListHotSources](raw/_short/api-aimiaobi-2023-08-01-listhotsources-0d21da74b7aa0b35.md)

list

\*全部资源

`*`

无

无

aimiaobi:GenerateFileUrlByKey

[GenerateFileUrlByKey](raw/_short/api-aimiaobi-2023-08-01-generatefileurlbykey-9259e036b36e906e.md)

get

\*全部资源

`*`

无

无

aimiaobi:EditAuditTerms

[EditAuditTerms](raw/_short/api-aimiaobi-2023-08-01-editauditterms-ce093d7e95e2db64.md)

update

\*全部资源

`*`

无

无

aimiaobi:ListAutoClipsTask

[ListAutoClipsTask](raw/_short/api-aimiaobi-2023-08-01-listautoclipstask-3fc611032bbe6624.md)

list

\*全部资源

`*`

无

无

aimiaobi:ListBuildConfigs

[ListBuildConfigs](raw/_short/api-aimiaobi-2023-08-01-listbuildconfigs-a6bef156747baddc.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunWriteToneGeneration

[RunWriteToneGeneration](raw/_short/api-aimiaobi-2023-08-01-runwritetonegeneration-4e42ab315d97d32e.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetDataset

[GetDataset](raw/_short/api-aimiaobi-2023-08-01-getdataset-22149b3781cffd5d.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunBookSmartCard

[RunBookSmartCard](raw/_short/api-aimiaobi-2023-08-01-runbooksmartcard-35cbe00c12792058.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetPptInfo

[GetPptInfo](raw/_short/api-aimiaobi-2023-08-01-getpptinfo-204afb4585337757.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeleteMaterialById

[DeleteMaterialById](raw/_short/api-aimiaobi-2023-08-01-deletematerialbyid-ce963e1d0cf3a2f3.md)

delete

\*全部资源

`*`

无

无

aimiaobi:ListIntervenes

[ListIntervenes](raw/_short/api-aimiaobi-2023-08-01-listintervenes-aeda2abf29c49a64.md)

list

\*全部资源

`*`

无

无

aimiaobi:InitiatePptCreation

[InitiatePptCreation](raw/_short/api-aimiaobi-2023-08-01-initiatepptcreation-5737c5ef27fa268d.md)

create

\*全部资源

`*`

无

无

aimiaobi:SubmitSmartClipTask

[SubmitSmartClipTask](raw/_short/api-aimiaobi-2023-08-01-submitsmartcliptask-f428eaea1e0c51a0.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunStepByStepWriting

[RunStepByStepWriting](raw/_short/api-aimiaobi-2023-08-01-runstepbystepwriting-4ff99b2db5069654.md)

create

\*全部资源

`*`

无

无

aimiaobi:FetchImageTask

[FetchImageTask](raw/_short/api-aimiaobi-2023-08-01-fetchimagetask-31305890a48151ef.md)

get

\*全部资源

`*`

无

无

aimiaobi:ExportPptArtifact

[ExportPptArtifact](raw/_short/api-aimiaobi-2023-08-01-exportpptartifact-fdb00f37b4c36d44.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetCustomText

[GetCustomText](raw/_short/api-aimiaobi-2023-08-01-getcustomtext-8157bfb9335a59f8.md)

get

\*全部资源

`*`

无

无

aimiaobi:UploadDoc

[UploadDoc](raw/_short/api-aimiaobi-2023-08-01-uploaddoc-65330797e2012078.md)

create

\*全部资源

`*`

无

无

aimiaobi:QueryVideoAuditResult

[QueryVideoAuditResult](raw/_short/api-aimiaobi-2023-08-01-queryvideoauditresult-3b8b4811530192fa.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetStyleLearningResult

[GetStyleLearningResult](raw/_short/api-aimiaobi-2023-08-01-getstylelearningresult-5360d3dde2c4474f.md)

get

\*全部资源

`*`

无

无

aimiaobi:UpdateGeneralConfig

[UpdateGeneralConfig](raw/_short/api-aimiaobi-2023-08-01-updategeneralconfig-045ba8737985ed17.md)

update

\*全部资源

`*`

无

无

aimiaobi:AsyncCreateClipsTask

[AsyncCreateClipsTask](raw/_short/api-aimiaobi-2023-08-01-asynccreateclipstask-f0727c5910f93f6f.md)

create

\*全部资源

`*`

无

无

aimiaobi:CreateDataPermissions

[CreateDataPermissions](raw/_short/api-aimiaobi-2023-08-01-createdatapermissions-92bb8122d208ea90.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunQuickWriting

[RunQuickWriting](raw/_short/api-aimiaobi-2023-08-01-runquickwriting-0e3b4ffec0852cef.md)

create

\*全部资源

`*`

无

无

aimiaobi:SubmitSmartAudit

[SubmitSmartAudit](raw/_short/api-aimiaobi-2023-08-01-submitsmartaudit-1b12b5a3618bb1cf.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListVersions

[ListVersions](raw/_short/api-aimiaobi-2023-08-01-listversions-e13aeb5fb9759776.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetInterveneRuleDetail

[GetInterveneRuleDetail](raw/_short/api-aimiaobi-2023-08-01-getinterveneruledetail-2a38c8e60d5f6b9b.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunTopicSelectionMerge

[RunTopicSelectionMerge](raw/_short/api-aimiaobi-2023-08-01-runtopicselectionmerge-3593266936554a26.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetFactAuditUrl

[GetFactAuditUrl](raw/_short/api-aimiaobi-2023-08-01-getfactauditurl-99a00a3a6ceaa9b7.md)

delete

\*全部资源

`*`

无

无

aimiaobi:SaveCustomText

[SaveCustomText](raw/_short/api-aimiaobi-2023-08-01-savecustomtext-3e5e75cf554b196d.md)

create

\*全部资源

`*`

无

无

aimiaobi:ExportIntervenes

[ExportIntervenes](raw/_short/api-aimiaobi-2023-08-01-exportintervenes-665adb0369561931.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetHotTopicBroadcast

[GetHotTopicBroadcast](raw/_short/api-aimiaobi-2023-08-01-gethottopicbroadcast-8bd753b9c4dd8b39.md)

get

\*全部资源

`*`

无

无

aimiaobi:SubmitDeepWriteTask

[SubmitDeepWriteTask](raw/_short/api-aimiaobi-2023-08-01-submitdeepwritetask-eef9df189279c77b.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListSearchTaskDialogueDatas

[ListSearchTaskDialogueDatas](raw/_short/api-aimiaobi-2023-08-01-listsearchtaskdialogueda-b9ade5026d8c596c.md)

list

\*全部资源

`*`

无

无

aimiaobi:ValidateUploadTemplate

[ValidateUploadTemplate](raw/_short/api-aimiaobi-2023-08-01-validateuploadtemplate-66737360c2dfa698.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunAiHelperWriting

[RunAiHelperWriting](raw/_short/api-aimiaobi-2023-08-01-runaihelperwriting-9e965c7e9fdbd13a.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetDocClusterTask

[GetDocClusterTask](raw/_short/api-aimiaobi-2023-08-01-getdocclustertask-8b6e25a105e3999f.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunWritingV2

[RunWritingV2](raw/_short/api-aimiaobi-2023-08-01-runwritingv2-c908f14d478d0459.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListDatasets

[ListDatasets](raw/_short/api-aimiaobi-2023-08-01-listdatasets-0f50aee17fb84ace.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunTextPolishing

[RunTextPolishing](raw/_short/api-aimiaobi-2023-08-01-runtextpolishing-d2237dfca46f820a.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListDocumentRetrieve

[ListDocumentRetrieve](raw/_short/api-aimiaobi-2023-08-01-listdocumentretrieve-4c7d5716896386e5.md)

list

\*全部资源

`*`

无

无

aimiaobi:SubmitAuditNote

[SubmitAuditNote](raw/_short/api-aimiaobi-2023-08-01-submitauditnote-4dd821cdf8013394.md)

none

\*全部资源

`*`

无

无

aimiaobi:ExportCustomSourceAnalysisTask

[ExportCustomSourceAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-exportcustomsourceanalys-dde5bfb67e895c5b.md)

get

\*全部资源

`*`

无

无

aimiaobi:FetchExportWordTask

[FetchExportWordTask](raw/_short/api-aimiaobi-2023-08-01-fetchexportwordtask-07e6992c68761aec.md)

get

\*全部资源

`*`

无

无

aimiaobi:DownloadBiddingDoc

[DownloadBiddingDoc](raw/_short/api-aimiaobi-2023-08-01-downloadbiddingdoc-635cd728381c2cbb.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunVideoScriptGenerate

[RunVideoScriptGenerate](raw/_short/api-aimiaobi-2023-08-01-runvideoscriptgenerate-3bc899c41f140c1f.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListAnalysisTagDetailByTaskId

[ListAnalysisTagDetailByTaskId](raw/_short/api-aimiaobi-2023-08-01-listanalysistagdetailbyt-e0dcf88e65760df1.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListTopicRecommendEventList

[ListTopicRecommendEventList](raw/_short/api-aimiaobi-2023-08-01-listtopicrecommendeventl-6b169c8697e358f3.md)

list

\*全部资源

`*`

无

无

aimiaobi:AsyncWritingBiddingDoc

[AsyncWritingBiddingDoc](raw/_short/api-aimiaobi-2023-08-01-asyncwritingbiddingdoc-2448bdba888d3b83.md)

create

\*全部资源

`*`

无

无

aimiaobi:SubmitExportTermsTask

[SubmitExportTermsTask](raw/_short/api-aimiaobi-2023-08-01-submitexporttermstask-ded711ad9a7779f9.md)

none

\*全部资源

`*`

无

无

aimiaobi:GetCustomTopicSelectionPerspectiveAnalysisTask

[GetCustomTopicSelectionPerspectiveAnalysisTask](raw/_short/api-aimiaobi-2023-08-01-getcustomtopicselectionp-9fc38ab6a2f293a9.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetCustomHotTopicBroadcastJob

[GetCustomHotTopicBroadcastJob](raw/_short/api-aimiaobi-2023-08-01-getcustomhottopicbroadca-d81006ae3cdf61d0.md)

get

\*全部资源

`*`

无

无

aimiaobi:DeleteStyleLearningResult

[DeleteStyleLearningResult](raw/_short/api-aimiaobi-2023-08-01-deletestylelearningresul-6b84f0160aafcb9d.md)

delete

\*全部资源

`*`

无

无

aimiaobi:UpdateDataset

[UpdateDataset](raw/_short/api-aimiaobi-2023-08-01-updatedataset-84bb97dbcac8c8eb.md)

update

\*全部资源

`*`

无

无

aimiaobi:ListPptTemplates

[ListPptTemplates](raw/_short/api-aimiaobi-2023-08-01-listppttemplates-88c8fe161f29a68f.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetPptArtifact

[GetPptArtifact](raw/_short/api-aimiaobi-2023-08-01-getpptartifact-0f24541bb6f0fb00.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetDeepWriteTaskResult

[GetDeepWriteTaskResult](raw/_short/api-aimiaobi-2023-08-01-getdeepwritetaskresult-a48c5d1c3eb0da71.md)

get

\*全部资源

`*`

无

无

aimiaobi:FetchExportTermsTask

[FetchExportTermsTask](raw/_short/api-aimiaobi-2023-08-01-fetchexporttermstask-029fa7b5f8e826dd.md)

none

\*全部资源

`*`

无

无

aimiaobi:GetAvailableAuditNotes

[GetAvailableAuditNotes](raw/_short/api-aimiaobi-2023-08-01-getavailableauditnotes-ed16fde575f68a31.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunAbbreviationContent

[RunAbbreviationContent](raw/_short/api-aimiaobi-2023-08-01-runabbreviationcontent-16382e8e5c8d6a6a.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetInterveneTemplateFileUrl

[GetInterveneTemplateFileUrl](raw/_short/api-aimiaobi-2023-08-01-getintervenetemplatefile-fe147f4cb14c0790.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunContinueContent

[RunContinueContent](raw/_short/api-aimiaobi-2023-08-01-runcontinuecontent-ab23bb7881b05f49.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetGeneralConfig

[GetGeneralConfig](raw/_short/api-aimiaobi-2023-08-01-getgeneralconfig-f2ee935b25738158.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListPlanningProposal

[ListPlanningProposal](raw/_short/api-aimiaobi-2023-08-01-listplanningproposal-7fadcb3c2ad047a5.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetAuditNoteProcessingStatus

[GetAuditNoteProcessingStatus](raw/_short/api-aimiaobi-2023-08-01-getauditnoteprocessingst-d90bc8538711a38c.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetAuditNotePostProcessingStatus

[GetAuditNotePostProcessingStatus](raw/_short/api-aimiaobi-2023-08-01-getauditnotepostprocessi-0aa9857194b67f71.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListTimedViewAttitude

[ListTimedViewAttitude](raw/_short/api-aimiaobi-2023-08-01-listtimedviewattitude-87c50823d6877c36.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunSummaryGenerate

[RunSummaryGenerate](raw/_short/api-aimiaobi-2023-08-01-runsummarygenerate-4842711c2c69d073.md)

get

\*全部资源

`*`

无

无

aimiaobi:FetchImportTermsTask

[FetchImportTermsTask](raw/_short/api-aimiaobi-2023-08-01-fetchimporttermstask-12ad325ce266ad04.md)

none

\*全部资源

`*`

无

无

aimiaobi:RunDocBrainmap

[RunDocBrainmap](raw/_short/api-aimiaobi-2023-08-01-rundocbrainmap-dc8e5bb64d710c98.md)

get

\*全部资源

`*`

无

无

aimiaobi:DeleteDataPermissions

[DeleteDataPermissions](raw/_short/api-aimiaobi-2023-08-01-deletedatapermissions-ea275f3378d861c1.md)

delete

\*全部资源

`*`

无

无

aimiaobi:RunBookIntroduction

[RunBookIntroduction](raw/_short/api-aimiaobi-2023-08-01-runbookintroduction-187585ee56810a9d.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetBiddingDocInfo

[GetBiddingDocInfo](raw/_short/api-aimiaobi-2023-08-01-getbiddingdocinfo-2fba9aa02ef96557.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListGeneralConfigs

[ListGeneralConfigs](raw/_short/api-aimiaobi-2023-08-01-listgeneralconfigs-630d0961286433c3.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunMultiDocIntroduction

[RunMultiDocIntroduction](raw/_short/api-aimiaobi-2023-08-01-runmultidocintroduction-1aa5a5e92698ff45.md)

get

\*全部资源

`*`

无

无

aimiaobi:SubmitAsyncTask

[SubmitAsyncTask](raw/_short/api-aimiaobi-2023-08-01-submitasynctask-07564d84da416279.md)

create

\*全部资源

`*`

无

无

aimiaobi:UpdateDatasetDocument

[UpdateDatasetDocument](raw/_short/api-aimiaobi-2023-08-01-updatedatasetdocument-20a215b97bba17aa.md)

update

\*全部资源

`*`

无

无

aimiaobi:RunExpandContent

[RunExpandContent](raw/_short/api-aimiaobi-2023-08-01-runexpandcontent-9ef545004396e6b9.md)

get

\*全部资源

`*`

无

无

aimiaobi:GenerateUploadConfig

[GenerateUploadConfig](raw/_short/api-aimiaobi-2023-08-01-generateuploadconfig-b7fff5389b2cbb66.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunTitleGeneration

[RunTitleGeneration](raw/_short/api-aimiaobi-2023-08-01-runtitlegeneration-a6c45cae66bbca21.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListAsyncTasks

[ListAsyncTasks](raw/_short/api-aimiaobi-2023-08-01-listasynctasks-76b88ff5435ad197.md)

list

\*全部资源

`*`

无

无

aimiaobi:ExportGeneratedContent

[ExportGeneratedContent](raw/_short/api-aimiaobi-2023-08-01-exportgeneratedcontent-4f19c9aa87904422.md)

get

\*全部资源

`*`

无

无

aimiaobi:ConfirmAndPostProcessAuditNote

[ConfirmAndPostProcessAuditNote](raw/_short/api-aimiaobi-2023-08-01-confirmandpostprocessaud-84319a0fa03a0d5f.md)

none

\*全部资源

`*`

无

无

aimiaobi:GetMaterialById

[GetMaterialById](raw/_short/api-aimiaobi-2023-08-01-getmaterialbyid-22e7878700a6f08e.md)

get

\*全部资源

`*`

无

无

aimiaobi:DeleteGeneralConfig

[DeleteGeneralConfig](raw/_short/api-aimiaobi-2023-08-01-deletegeneralconfig-fd8c5615923b9ff2.md)

delete

\*全部资源

`*`

无

无

aimiaobi:GetFileContentLength

[GetFileContentLength](raw/_short/api-aimiaobi-2023-08-01-getfilecontentlength-7895970d20b8a70d.md)

get

\*全部资源

`*`

无

无

aimiaobi:CancelAuditTask

[CancelAuditTask](raw/_short/api-aimiaobi-2023-08-01-cancelaudittask-2c8ab9606eeda99c.md)

update

\*全部资源

`*`

无

无

aimiaobi:SubmitDocClusterTask

[SubmitDocClusterTask](raw/_short/api-aimiaobi-2023-08-01-submitdocclustertask-54ca4a8668e488bc.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeleteFactAuditUrl

[DeleteFactAuditUrl](raw/_short/api-aimiaobi-2023-08-01-deletefactauditurl-b6796061bd36bd1d.md)

delete

\*全部资源

`*`

无

无

aimiaobi:EditBiddingDoc

[EditBiddingDoc](raw/_short/api-aimiaobi-2023-08-01-editbiddingdoc-8f9a8217921fd807.md)

update

\*全部资源

`*`

无

无

aimiaobi:SubmitAuditTask

[SubmitAuditTask](raw/_short/api-aimiaobi-2023-08-01-submitaudittask-c89e9e79c8c2943f.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetDocInfo

[GetDocInfo](raw/_short/api-aimiaobi-2023-08-01-getdocinfo-e63b147cceaff4cb.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetPptTemplateSelector

[GetPptTemplateSelector](raw/_short/api-aimiaobi-2023-08-01-getppttemplateselector-5b8157ba87d36c80.md)

create

\*全部资源

`*`

无

无

aimiaobi:SearchNews

[SearchNews](raw/_short/api-aimiaobi-2023-08-01-searchnews-2c347c0bb8002e65.md)

list

\*全部资源

`*`

无

无

aimiaobi:ExportAuditContentResult

[ExportAuditContentResult](raw/_short/api-aimiaobi-2023-08-01-exportauditcontentresult-12ec62cdb9103ee9.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunDocQa

[RunDocQa](raw/_short/api-aimiaobi-2023-08-01-rundocqa-45115fa76b5c8329.md)

get

\*全部资源

`*`

无

无

aimiaobi:SubmitFactAuditUrl

[SubmitFactAuditUrl](raw/_short/api-aimiaobi-2023-08-01-submitfactauditurl-7ea215332c708901.md)

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
