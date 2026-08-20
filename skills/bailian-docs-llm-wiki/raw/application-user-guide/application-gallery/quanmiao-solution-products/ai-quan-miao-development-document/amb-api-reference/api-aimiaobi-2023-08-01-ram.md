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
    
    -   Condition\_operator：条件运算符，不同类型的条件对应不同的条件运算符。具体信息，请参见权限策略基本元素。
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
-   条件关键字：是指云产品自身定义的条件关键字。该列不体现适用于任何操作的通用条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

**操作**

**API**

**访问级别**

**资源类型**

**条件关键字**

**关联操作**

aimiaobi:RunDocTranslation

[RunDocTranslation](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-other/api-aimiaobi-2023-08-01-rundoctranslation.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunWriting

[RunWriting](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runwriting.md)

create

\*全部资源

`*`

无

无

aimiaobi:InitiatePptCreationV2

[InitiatePptCreationV2](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-initiatepptcreationv2.md)

create

\*全部资源

`*`

无

无

aimiaobi:DocumentExtraction

[DocumentExtraction](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library-custom-text/api-aimiaobi-2023-08-01-documentextraction.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListTopicViewPointRecommendEventList

[ListTopicViewPointRecommendEventList](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-policy-custom-topic/api-aimiaobi-2023-08-01-listtopicviewpointrecommendeventlist.md)

list

\*全部资源

`*`

无

无

aimiaobi:SubmitImportTermsTask

[SubmitImportTermsTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-thesaurus-management/api-aimiaobi-2023-08-01-submitimporttermstask.md)

none

\*全部资源

`*`

无

无

aimiaobi:RunGenerateQuestions

[RunGenerateQuestions](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-question-and-answer-class/api-aimiaobi-2023-08-01-rungeneratequestions.md)

get

\*全部资源

`*`

无

无

aimiaobi:DeleteCustomTopicByTopic

[DeleteCustomTopicByTopic](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-policy-custom-topic/api-aimiaobi-2023-08-01-deletecustomtopicbytopic.md)

delete

\*全部资源

`*`

无

无

aimiaobi:RunStyleFeatureAnalysis

[RunStyleFeatureAnalysis](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-style-imitation-writing/api-aimiaobi-2023-08-01-runstylefeatureanalysis.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetAutoClipsTaskInfo

[GetAutoClipsTaskInfo](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-video-mixed-cut/api-aimiaobi-2023-08-01-getautoclipstaskinfo.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunCustomHotTopicViewPointAnalysis

[RunCustomHotTopicViewPointAnalysis](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-policy-custom-topic/api-aimiaobi-2023-08-01-runcustomhottopicviewpointanalysis.md)

create

\*全部资源

`*`

无

无

aimiaobi:AsyncUploadVideo

[AsyncUploadVideo](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-video-mixed-cut/api-aimiaobi-2023-08-01-asyncuploadvideo.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeleteGeneratedContent

[DeleteGeneratedContent](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-document-management/api-aimiaobi-2023-08-01-deletegeneratedcontent.md)

delete

\*全部资源

`*`

无

无

aimiaobi:SaveMaterialDocument

[SaveMaterialDocument](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library/api-aimiaobi-2023-08-01-savematerialdocument.md)

create

\*全部资源

`*`

无

无

aimiaobi:AsyncCreateClipsTimeLine

[AsyncCreateClipsTimeLine](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-video-mixed-cut/api-aimiaobi-2023-08-01-asynccreateclipstimeline.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListMaterialDocuments

[ListMaterialDocuments](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library/api-aimiaobi-2023-08-01-listmaterialdocuments.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetCustomSourceTopicAnalysisTask

[GetCustomSourceTopicAnalysisTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tips-custom-data-source/api-aimiaobi-2023-08-01-getcustomsourcetopicanalysistask.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListFreshViewPoints

[ListFreshViewPoints](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-listfreshviewpoints.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetInterveneGlobalReply

[GetInterveneGlobalReply](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-getinterveneglobalreply.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListDocs

[ListDocs](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-basic-operation-class/api-aimiaobi-2023-08-01-listdocs.md)

list

\*全部资源

`*`

无

无

aimiaobi:AddAuditTerms

[AddAuditTerms](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-thesaurus-management/api-aimiaobi-2023-08-01-addauditterms.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeleteDataset

[DeleteDataset](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-deletedataset.md)

delete

\*全部资源

`*`

无

无

aimiaobi:ListAuditContentErrorTypes

[ListAuditContentErrorTypes](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-article-reviser/api-aimiaobi-2023-08-01-listauditcontenterrortypes.md)

list

\*全部资源

`*`

无

无

aimiaobi:DeleteInterveneRule

[DeleteInterveneRule](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-deleteintervenerule.md)

delete

\*全部资源

`*`

无

无

aimiaobi:UpdateMaterialDocument

[UpdateMaterialDocument](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library/api-aimiaobi-2023-08-01-updatematerialdocument.md)

update

\*全部资源

`*`

无

无

aimiaobi:ListDatasetDocuments

[ListDatasetDocuments](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-listdatasetdocuments.md)

list

\*全部资源

`*`

无

无

aimiaobi:GenerateViewPoint

[GenerateViewPoint](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-generateviewpoint.md)

list

\*全部资源

`*`

无

无

aimiaobi:CreateDataset

[CreateDataset](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-createdataset.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetClipsBuildInResource

[GetClipsBuildInResource](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-video-mixed-cut/api-aimiaobi-2023-08-01-getclipsbuildinresource.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetSmartAuditResult

[GetSmartAuditResult](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-article-reviser/api-aimiaobi-2023-08-01-getsmartauditresult.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunCommentGeneration

[RunCommentGeneration](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-generate-class/api-aimiaobi-2023-08-01-runcommentgeneration.md)

get

\*全部资源

`*`

无

无

aimiaobi:InsertInterveneRule

[InsertInterveneRule](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-insertintervenerule.md)

create

\*全部资源

`*`

无

无

aimiaobi:CreateGeneralConfig

[CreateGeneralConfig](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-common-configuration/api-aimiaobi-2023-08-01-creategeneralconfig.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetDatasetDocument

[GetDatasetDocument](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-getdatasetdocument.md)

get

\*全部资源

`*`

无

无

aimiaobi:ClearIntervenes

[ClearIntervenes](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-clearintervenes.md)

delete

\*全部资源

`*`

无

无

aimiaobi:ListDataPermissions

[ListDataPermissions](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-listdatapermissions.md)

list

\*全部资源

`*`

无

无

aimiaobi:ListCustomText

[ListCustomText](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library-custom-text/api-aimiaobi-2023-08-01-listcustomtext.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunDocSmartCard

[RunDocSmartCard](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-other/api-aimiaobi-2023-08-01-rundocsmartcard.md)

get

\*全部资源

`*`

无

无

aimiaobi:UpdateGeneratedContent

[UpdateGeneratedContent](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-document-management/api-aimiaobi-2023-08-01-updategeneratedcontent.md)

update

\*全部资源

`*`

无

无

aimiaobi:GetDataSourceOrderConfig

[GetDataSourceOrderConfig](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-source-management/api-aimiaobi-2023-08-01-getdatasourceorderconfig.md)

get

\*全部资源

`*`

无

无

aimiaobi:SubmitTopicSelectionPerspectiveAnalysisTask

[SubmitTopicSelectionPerspectiveAnalysisTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tips-openapi/api-aimiaobi-2023-08-01-submittopicselectionperspectiveanalysistask.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListInterveneRules

[ListInterveneRules](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-listintervenerules.md)

list

\*全部资源

`*`

无

无

aimiaobi:ListHotTopics

[ListHotTopics](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-listhottopics.md)

list

\*全部资源

`*`

无

无

aimiaobi:SubmitCustomTopicSelectionPerspectiveAnalysisTask

[SubmitCustomTopicSelectionPerspectiveAnalysisTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tips-openapi/api-aimiaobi-2023-08-01-submitcustomtopicselectionperspectiveanalysistask.md)

create

\*全部资源

`*`

无

无

aimiaobi:CreateToken

[CreateToken](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-universal-interface/api-aimiaobi-2023-08-01-createtoken.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunDocIntroduction

[RunDocIntroduction](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-generate-class/api-aimiaobi-2023-08-01-rundocintroduction.md)

get

\*全部资源

`*`

无

无

aimiaobi:CancelDeepWriteTask

[CancelDeepWriteTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-deep-writing/api-aimiaobi-2023-08-01-canceldeepwritetask.md)

update

\*全部资源

`*`

无

无

aimiaobi:DeleteAuditTerms

[DeleteAuditTerms](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-thesaurus-management/api-aimiaobi-2023-08-01-deleteauditterms.md)

delete

\*全部资源

`*`

无

无

aimiaobi:FeedbackDialogue

[FeedbackDialogue](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-feedbackdialogue.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListWebReviewPoints

[ListWebReviewPoints](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-listwebreviewpoints.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunDocWashing

[RunDocWashing](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-generate-class/api-aimiaobi-2023-08-01-rundocwashing.md)

get

\*全部资源

`*`

无

无

aimiaobi:DeleteAuditNote

[DeleteAuditNote](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-proofreading-rule-library-management/api-aimiaobi-2023-08-01-deleteauditnote.md)

delete

\*全部资源

`*`

无

无

aimiaobi:ImportInterveneFileAsync

[ImportInterveneFileAsync](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-importintervenefileasync.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeletePptArtifact

[DeletePptArtifact](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-deletepptartifact.md)

delete

\*全部资源

`*`

无

无

aimiaobi:SearchDatasetDocuments

[SearchDatasetDocuments](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-searchdatasetdocuments.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunPptOutlineGeneration

[RunPptOutlineGeneration](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-runpptoutlinegeneration.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetCategoriesByTaskId

[GetCategoriesByTaskId](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaoce-enterprise-voc-mining/api-aimiaobi-2023-08-01-getcategoriesbytaskid.md)

get

\*全部资源

`*`

无

无

aimiaobi:GenerateExportWordTask

[GenerateExportWordTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-document-management/api-aimiaobi-2023-08-01-generateexportwordtask.md)

get

\*全部资源

`*`

无

无

aimiaobi:QueryAuditTask

[QueryAuditTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-queryaudittask.md)

get

\*全部资源

`*`

无

无

aimiaobi:AsyncEditTimeline

[AsyncEditTimeline](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-video-mixed-cut/api-aimiaobi-2023-08-01-asyncedittimeline.md)

update

\*全部资源

`*`

无

无

aimiaobi:ListWritingStyles

[ListWritingStyles](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-style-imitation-writing/api-aimiaobi-2023-08-01-listwritingstyles.md)

list

\*全部资源

`*`

无

无

aimiaobi:CreateGeneratedContent

[CreateGeneratedContent](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-document-management/api-aimiaobi-2023-08-01-creategeneratedcontent.md)

create

\*全部资源

`*`

无

无

aimiaobi:SubmitCustomHotTopicBroadcastJob

[SubmitCustomHotTopicBroadcastJob](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-policy-news-broadcast/api-aimiaobi-2023-08-01-submitcustomhottopicbroadcastjob.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetDeepWriteTask

[GetDeepWriteTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-deep-writing/api-aimiaobi-2023-08-01-getdeepwritetask.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetGeneratedContent

[GetGeneratedContent](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-document-management/api-aimiaobi-2023-08-01-getgeneratedcontent.md)

get

\*全部资源

`*`

无

无

aimiaobi:SubmitCustomSourceTopicAnalysis

[SubmitCustomSourceTopicAnalysis](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tips-custom-data-source/api-aimiaobi-2023-08-01-submitcustomsourcetopicanalysis.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetEnterpriseVocAnalysisTask

[GetEnterpriseVocAnalysisTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaoce-enterprise-voc-mining/api-aimiaobi-2023-08-01-getenterprisevocanalysistask.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunDeepWriting

[RunDeepWriting](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-deep-writing/api-aimiaobi-2023-08-01-rundeepwriting.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunBookBrainmap

[RunBookBrainmap](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-generate-class/api-aimiaobi-2023-08-01-runbookbrainmap.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListSearchTasks

[ListSearchTasks](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-smart-search/api-aimiaobi-2023-08-01-listsearchtasks.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetPptConfig

[GetPptConfig](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-getpptconfig.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunHotword

[RunHotword](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-extraction-class/api-aimiaobi-2023-08-01-runhotword.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListBiddingDoc

[ListBiddingDoc](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tender-generation/api-aimiaobi-2023-08-01-listbiddingdoc.md)

list

\*全部资源

`*`

无

无

aimiaobi:ListGeneratedContents

[ListGeneratedContents](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-document-management/api-aimiaobi-2023-08-01-listgeneratedcontents.md)

list

\*全部资源

`*`

无

无

aimiaobi:ExportAnalysisTagDetailByTaskId

[ExportAnalysisTagDetailByTaskId](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaoce-enterprise-voc-mining/api-aimiaobi-2023-08-01-exportanalysistagdetailbytaskid.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListStyleLearningResult

[ListStyleLearningResult](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-style-imitation-writing/api-aimiaobi-2023-08-01-liststylelearningresult.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunSearchSimilarArticles

[RunSearchSimilarArticles](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-smart-search/api-aimiaobi-2023-08-01-runsearchsimilararticles.md)

none

\*全部资源

`*`

无

无

aimiaobi:GetSmartClipTask

[GetSmartClipTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-getsmartcliptask.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetInterveneImportTaskInfo

[GetInterveneImportTaskInfo](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-getinterveneimporttaskinfo.md)

get

\*全部资源

`*`

无

无

aimiaobi:CancelAsyncTask

[CancelAsyncTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-asynchronous-task-management/api-aimiaobi-2023-08-01-cancelasynctask.md)

update

\*全部资源

`*`

无

无

aimiaobi:AsyncUploadTenderDoc

[AsyncUploadTenderDoc](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tender-generation/api-aimiaobi-2023-08-01-asyncuploadtenderdoc.md)

create

\*全部资源

`*`

无

无

aimiaobi:UpdateCustomText

[UpdateCustomText](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library-custom-text/api-aimiaobi-2023-08-01-updatecustomtext.md)

update

\*全部资源

`*`

无

无

aimiaobi:ListHotViewPoints

[ListHotViewPoints](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-listhotviewpoints.md)

list

\*全部资源

`*`

无

无

aimiaobi:QueryAsyncTask

[QueryAsyncTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-asynchronous-task-management/api-aimiaobi-2023-08-01-queryasynctask.md)

get

\*全部资源

`*`

无

无

aimiaobi:DownloadAuditNote

[DownloadAuditNote](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-proofreading-rule-library-management/api-aimiaobi-2023-08-01-downloadauditnote.md)

get

\*全部资源

`*`

无

无

aimiaobi:ImportInterveneFile

[ImportInterveneFile](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-importintervenefile.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeleteCustomText

[DeleteCustomText](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library-custom-text/api-aimiaobi-2023-08-01-deletecustomtext.md)

delete

\*全部资源

`*`

无

无

aimiaobi:ExportHotTopicPlanningProposals

[ExportHotTopicPlanningProposals](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-exporthottopicplanningproposals.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunDocSummary

[RunDocSummary](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-generate-class/api-aimiaobi-2023-08-01-rundocsummary.md)

get

\*全部资源

`*`

无

无

aimiaobi:SubmitEnterpriseVocAnalysisTask

[SubmitEnterpriseVocAnalysisTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaoce-enterprise-voc-mining/api-aimiaobi-2023-08-01-submitenterprisevocanalysistask.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListDialogues

[ListDialogues](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-universal-interface/api-aimiaobi-2023-08-01-listdialogues.md)

list

\*全部资源

`*`

无

无

aimiaobi:GenerateImageTask

[GenerateImageTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-generateimagetask.md)

create

\*全部资源

`*`

无

无

aimiaobi:SaveOrUpdateOssConfig

[SaveOrUpdateOssConfig](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-saveorupdateossconfig.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeleteDocs

[DeleteDocs](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-basic-operation-class/api-aimiaobi-2023-08-01-deletedocs.md)

delete

\*全部资源

`*`

无

无

aimiaobi:ListHotNewsWithType

[ListHotNewsWithType](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-listhotnewswithtype.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunKeywordsExtractionGeneration

[RunKeywordsExtractionGeneration](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runkeywordsextractiongeneration.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunTranslateGeneration

[RunTranslateGeneration](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runtranslategeneration.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunCustomHotTopicAnalysis

[RunCustomHotTopicAnalysis](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-policy-custom-topic/api-aimiaobi-2023-08-01-runcustomhottopicanalysis.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetTopicById

[GetTopicById](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-gettopicbyid.md)

get

\*全部资源

`*`

无

无

aimiaobi:DeleteCustomTopicViewPointById

[DeleteCustomTopicViewPointById](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-policy-custom-topic/api-aimiaobi-2023-08-01-deletecustomtopicviewpointbyid.md)

delete

\*全部资源

`*`

无

无

aimiaobi:BindPptArtifact

[BindPptArtifact](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-bindpptartifact.md)

create

\*全部资源

`*`

无

无

aimiaobi:InsertInterveneGlobalReply

[InsertInterveneGlobalReply](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-insertinterveneglobalreply.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeleteDatasetDocument

[DeleteDatasetDocument](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-deletedatasetdocument.md)

delete

\*全部资源

`*`

无

无

aimiaobi:ListSearchTaskDialogues

[ListSearchTaskDialogues](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-smart-search/api-aimiaobi-2023-08-01-listsearchtaskdialogues.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetPptArtifactExportResult

[GetPptArtifactExportResult](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-getpptartifactexportresult.md)

create

\*全部资源

`*`

无

无

aimiaobi:AddDatasetDocument

[AddDatasetDocument](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-adddatasetdocument.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListAuditTerms

[ListAuditTerms](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-thesaurus-management/api-aimiaobi-2023-08-01-listauditterms.md)

list

\*全部资源

`*`

无

无

aimiaobi:SubmitVideoAudit

[SubmitVideoAudit](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-video-review/api-aimiaobi-2023-08-01-submitvideoaudit.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListInterveneCnt

[ListInterveneCnt](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-listintervenecnt.md)

list

\*全部资源

`*`

无

无

aimiaobi:ListCustomViewPoints

[ListCustomViewPoints](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-policy-custom-topic/api-aimiaobi-2023-08-01-listcustomviewpoints.md)

list

\*全部资源

`*`

无

无

aimiaobi:SaveStyleLearningResult

[SaveStyleLearningResult](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-style-imitation-writing/api-aimiaobi-2023-08-01-savestylelearningresult.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunSearchGeneration

[RunSearchGeneration](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-smart-search/api-aimiaobi-2023-08-01-runsearchgeneration.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListEnterprisePptTemplates

[ListEnterprisePptTemplates](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-listenterpriseppttemplates.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetTopicSelectionPerspectiveAnalysisTask

[GetTopicSelectionPerspectiveAnalysisTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tips-openapi/api-aimiaobi-2023-08-01-gettopicselectionperspectiveanalysistask.md)

get

\*全部资源

`*`

无

无

aimiaobi:SaveDataSourceOrderConfig

[SaveDataSourceOrderConfig](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-source-management/api-aimiaobi-2023-08-01-savedatasourceorderconfig.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetBiddingRemainLimitNum

[GetBiddingRemainLimitNum](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tender-generation/api-aimiaobi-2023-08-01-getbiddingremainlimitnum.md)

get

\*全部资源

`*`

无

无

aimiaobi:UploadBook

[UploadBook](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-basic-operation-class/api-aimiaobi-2023-08-01-uploadbook.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListPptArtifacts

[ListPptArtifacts](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-listpptartifacts.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetProperties

[GetProperties](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-universal-interface/api-aimiaobi-2023-08-01-getproperties.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListHotSources

[ListHotSources](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-listhotsources.md)

list

\*全部资源

`*`

无

无

aimiaobi:GenerateFileUrlByKey

[GenerateFileUrlByKey](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-file-upload-and-download/api-aimiaobi-2023-08-01-generatefileurlbykey.md)

get

\*全部资源

`*`

无

无

aimiaobi:EditAuditTerms

[EditAuditTerms](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-thesaurus-management/api-aimiaobi-2023-08-01-editauditterms.md)

update

\*全部资源

`*`

无

无

aimiaobi:ListAutoClipsTask

[ListAutoClipsTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-video-mixed-cut/api-aimiaobi-2023-08-01-listautoclipstask.md)

list

\*全部资源

`*`

无

无

aimiaobi:ListBuildConfigs

[ListBuildConfigs](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-listbuildconfigs.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunWriteToneGeneration

[RunWriteToneGeneration](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runwritetonegeneration.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetDataset

[GetDataset](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-getdataset.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunBookSmartCard

[RunBookSmartCard](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-other/api-aimiaobi-2023-08-01-runbooksmartcard.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetPptInfo

[GetPptInfo](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-getpptinfo.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeleteMaterialById

[DeleteMaterialById](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library/api-aimiaobi-2023-08-01-deletematerialbyid.md)

delete

\*全部资源

`*`

无

无

aimiaobi:ListIntervenes

[ListIntervenes](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-listintervenes.md)

list

\*全部资源

`*`

无

无

aimiaobi:InitiatePptCreation

[InitiatePptCreation](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-initiatepptcreation.md)

create

\*全部资源

`*`

无

无

aimiaobi:SubmitSmartClipTask

[SubmitSmartClipTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-submitsmartcliptask.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunStepByStepWriting

[RunStepByStepWriting](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runstepbystepwriting.md)

create

\*全部资源

`*`

无

无

aimiaobi:FetchImageTask

[FetchImageTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-fetchimagetask.md)

get

\*全部资源

`*`

无

无

aimiaobi:ExportPptArtifact

[ExportPptArtifact](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-exportpptartifact.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetCustomText

[GetCustomText](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library-custom-text/api-aimiaobi-2023-08-01-getcustomtext.md)

get

\*全部资源

`*`

无

无

aimiaobi:UploadDoc

[UploadDoc](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-basic-operation-class/api-aimiaobi-2023-08-01-uploaddoc.md)

create

\*全部资源

`*`

无

无

aimiaobi:QueryVideoAuditResult

[QueryVideoAuditResult](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-video-review/api-aimiaobi-2023-08-01-queryvideoauditresult.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetStyleLearningResult

[GetStyleLearningResult](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-style-imitation-writing/api-aimiaobi-2023-08-01-getstylelearningresult.md)

get

\*全部资源

`*`

无

无

aimiaobi:UpdateGeneralConfig

[UpdateGeneralConfig](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-common-configuration/api-aimiaobi-2023-08-01-updategeneralconfig.md)

update

\*全部资源

`*`

无

无

aimiaobi:AsyncCreateClipsTask

[AsyncCreateClipsTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-video-mixed-cut/api-aimiaobi-2023-08-01-asynccreateclipstask.md)

create

\*全部资源

`*`

无

无

aimiaobi:CreateDataPermissions

[CreateDataPermissions](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-createdatapermissions.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunQuickWriting

[RunQuickWriting](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runquickwriting.md)

create

\*全部资源

`*`

无

无

aimiaobi:SubmitSmartAudit

[SubmitSmartAudit](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-article-reviser/api-aimiaobi-2023-08-01-submitsmartaudit.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListVersions

[ListVersions](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-universal-interface/api-aimiaobi-2023-08-01-listversions.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetInterveneRuleDetail

[GetInterveneRuleDetail](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-getinterveneruledetail.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunTopicSelectionMerge

[RunTopicSelectionMerge](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-runtopicselectionmerge.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetFactAuditUrl

[GetFactAuditUrl](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-factual-review/api-aimiaobi-2023-08-01-getfactauditurl.md)

delete

\*全部资源

`*`

无

无

aimiaobi:SaveCustomText

[SaveCustomText](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library-custom-text/api-aimiaobi-2023-08-01-savecustomtext.md)

create

\*全部资源

`*`

无

无

aimiaobi:ExportIntervenes

[ExportIntervenes](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-exportintervenes.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetHotTopicBroadcast

[GetHotTopicBroadcast](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-policy-news-broadcast/api-aimiaobi-2023-08-01-gethottopicbroadcast.md)

get

\*全部资源

`*`

无

无

aimiaobi:SubmitDeepWriteTask

[SubmitDeepWriteTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-deep-writing/api-aimiaobi-2023-08-01-submitdeepwritetask.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListSearchTaskDialogueDatas

[ListSearchTaskDialogueDatas](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-smart-search/api-aimiaobi-2023-08-01-listsearchtaskdialoguedatas.md)

list

\*全部资源

`*`

无

无

aimiaobi:ValidateUploadTemplate

[ValidateUploadTemplate](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaoce-enterprise-voc-mining/api-aimiaobi-2023-08-01-validateuploadtemplate.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunAiHelperWriting

[RunAiHelperWriting](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runaihelperwriting.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetDocClusterTask

[GetDocClusterTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tips-openapi/api-aimiaobi-2023-08-01-getdocclustertask.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunWritingV2

[RunWritingV2](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runwritingv2.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListDatasets

[ListDatasets](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-listdatasets.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunTextPolishing

[RunTextPolishing](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runtextpolishing.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListDocumentRetrieve

[ListDocumentRetrieve](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-public-library-retrieval/api-aimiaobi-2023-08-01-listdocumentretrieve.md)

list

\*全部资源

`*`

无

无

aimiaobi:SubmitAuditNote

[SubmitAuditNote](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-proofreading-rule-library-management/api-aimiaobi-2023-08-01-submitauditnote.md)

none

\*全部资源

`*`

无

无

aimiaobi:ExportCustomSourceAnalysisTask

[ExportCustomSourceAnalysisTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tips-custom-data-source/api-aimiaobi-2023-08-01-exportcustomsourceanalysistask.md)

get

\*全部资源

`*`

无

无

aimiaobi:FetchExportWordTask

[FetchExportWordTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-document-management/api-aimiaobi-2023-08-01-fetchexportwordtask.md)

get

\*全部资源

`*`

无

无

aimiaobi:DownloadBiddingDoc

[DownloadBiddingDoc](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tender-generation/api-aimiaobi-2023-08-01-downloadbiddingdoc.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunVideoScriptGenerate

[RunVideoScriptGenerate](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-runvideoscriptgenerate.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListAnalysisTagDetailByTaskId

[ListAnalysisTagDetailByTaskId](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaoce-enterprise-voc-mining/api-aimiaobi-2023-08-01-listanalysistagdetailbytaskid.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListTopicRecommendEventList

[ListTopicRecommendEventList](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-policy-custom-topic/api-aimiaobi-2023-08-01-listtopicrecommendeventlist.md)

list

\*全部资源

`*`

无

无

aimiaobi:AsyncWritingBiddingDoc

[AsyncWritingBiddingDoc](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tender-generation/api-aimiaobi-2023-08-01-asyncwritingbiddingdoc.md)

create

\*全部资源

`*`

无

无

aimiaobi:SubmitExportTermsTask

[SubmitExportTermsTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-thesaurus-management/api-aimiaobi-2023-08-01-submitexporttermstask.md)

none

\*全部资源

`*`

无

无

aimiaobi:GetCustomTopicSelectionPerspectiveAnalysisTask

[GetCustomTopicSelectionPerspectiveAnalysisTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tips-openapi/api-aimiaobi-2023-08-01-getcustomtopicselectionperspectiveanalysistask.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetCustomHotTopicBroadcastJob

[GetCustomHotTopicBroadcastJob](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-policy-news-broadcast/api-aimiaobi-2023-08-01-getcustomhottopicbroadcastjob.md)

get

\*全部资源

`*`

无

无

aimiaobi:DeleteStyleLearningResult

[DeleteStyleLearningResult](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-style-imitation-writing/api-aimiaobi-2023-08-01-deletestylelearningresult.md)

delete

\*全部资源

`*`

无

无

aimiaobi:UpdateDataset

[UpdateDataset](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-updatedataset.md)

update

\*全部资源

`*`

无

无

aimiaobi:ListPptTemplates

[ListPptTemplates](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-listppttemplates.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetPptArtifact

[GetPptArtifact](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-getpptartifact.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetDeepWriteTaskResult

[GetDeepWriteTaskResult](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-deep-writing/api-aimiaobi-2023-08-01-getdeepwritetaskresult.md)

get

\*全部资源

`*`

无

无

aimiaobi:FetchExportTermsTask

[FetchExportTermsTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-thesaurus-management/api-aimiaobi-2023-08-01-fetchexporttermstask.md)

none

\*全部资源

`*`

无

无

aimiaobi:GetAvailableAuditNotes

[GetAvailableAuditNotes](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-proofreading-rule-library-management/api-aimiaobi-2023-08-01-getavailableauditnotes.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunAbbreviationContent

[RunAbbreviationContent](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runabbreviationcontent.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetInterveneTemplateFileUrl

[GetInterveneTemplateFileUrl](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-system-configuration-intervention-configuration/api-aimiaobi-2023-08-01-getintervenetemplatefileurl.md)

get

\*全部资源

`*`

无

无

aimiaobi:RunContinueContent

[RunContinueContent](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runcontinuecontent.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetGeneralConfig

[GetGeneralConfig](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-common-configuration/api-aimiaobi-2023-08-01-getgeneralconfig.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListPlanningProposal

[ListPlanningProposal](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-listplanningproposal.md)

list

\*全部资源

`*`

无

无

aimiaobi:GetAuditNoteProcessingStatus

[GetAuditNoteProcessingStatus](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-proofreading-rule-library-management/api-aimiaobi-2023-08-01-getauditnoteprocessingstatus.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetAuditNotePostProcessingStatus

[GetAuditNotePostProcessingStatus](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-proofreading-rule-library-management/api-aimiaobi-2023-08-01-getauditnotepostprocessingstatus.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListTimedViewAttitude

[ListTimedViewAttitude](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaozi-hot-topics/api-aimiaobi-2023-08-01-listtimedviewattitude.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunSummaryGenerate

[RunSummaryGenerate](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runsummarygenerate.md)

get

\*全部资源

`*`

无

无

aimiaobi:FetchImportTermsTask

[FetchImportTermsTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-thesaurus-management/api-aimiaobi-2023-08-01-fetchimporttermstask.md)

none

\*全部资源

`*`

无

无

aimiaobi:RunDocBrainmap

[RunDocBrainmap](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-generate-class/api-aimiaobi-2023-08-01-rundocbrainmap.md)

get

\*全部资源

`*`

无

无

aimiaobi:DeleteDataPermissions

[DeleteDataPermissions](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-deletedatapermissions.md)

delete

\*全部资源

`*`

无

无

aimiaobi:RunBookIntroduction

[RunBookIntroduction](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-generate-class/api-aimiaobi-2023-08-01-runbookintroduction.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetBiddingDocInfo

[GetBiddingDocInfo](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tender-generation/api-aimiaobi-2023-08-01-getbiddingdocinfo.md)

get

\*全部资源

`*`

无

无

aimiaobi:ListGeneralConfigs

[ListGeneralConfigs](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-common-configuration/api-aimiaobi-2023-08-01-listgeneralconfigs.md)

list

\*全部资源

`*`

无

无

aimiaobi:RunMultiDocIntroduction

[RunMultiDocIntroduction](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-generate-class/api-aimiaobi-2023-08-01-runmultidocintroduction.md)

get

\*全部资源

`*`

无

无

aimiaobi:SubmitAsyncTask

[SubmitAsyncTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-asynchronous-task-management/api-aimiaobi-2023-08-01-submitasynctask.md)

create

\*全部资源

`*`

无

无

aimiaobi:UpdateDatasetDocument

[UpdateDatasetDocument](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-search-data-source/api-aimiaobi-2023-08-01-updatedatasetdocument.md)

update

\*全部资源

`*`

无

无

aimiaobi:RunExpandContent

[RunExpandContent](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runexpandcontent.md)

get

\*全部资源

`*`

无

无

aimiaobi:GenerateUploadConfig

[GenerateUploadConfig](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-file-upload-and-download/api-aimiaobi-2023-08-01-generateuploadconfig.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunTitleGeneration

[RunTitleGeneration](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-runtitlegeneration.md)

create

\*全部资源

`*`

无

无

aimiaobi:ListAsyncTasks

[ListAsyncTasks](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-asynchronous-task-management/api-aimiaobi-2023-08-01-listasynctasks.md)

list

\*全部资源

`*`

无

无

aimiaobi:ExportGeneratedContent

[ExportGeneratedContent](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-document-management/api-aimiaobi-2023-08-01-exportgeneratedcontent.md)

get

\*全部资源

`*`

无

无

aimiaobi:ConfirmAndPostProcessAuditNote

[ConfirmAndPostProcessAuditNote](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-proofreading-rule-library-management/api-aimiaobi-2023-08-01-confirmandpostprocessauditnote.md)

none

\*全部资源

`*`

无

无

aimiaobi:GetMaterialById

[GetMaterialById](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-material-library/api-aimiaobi-2023-08-01-getmaterialbyid.md)

get

\*全部资源

`*`

无

无

aimiaobi:DeleteGeneralConfig

[DeleteGeneralConfig](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-common-interface-common-configuration/api-aimiaobi-2023-08-01-deletegeneralconfig.md)

delete

\*全部资源

`*`

无

无

aimiaobi:GetFileContentLength

[GetFileContentLength](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-basic-operation-class/api-aimiaobi-2023-08-01-getfilecontentlength.md)

get

\*全部资源

`*`

无

无

aimiaobi:CancelAuditTask

[CancelAuditTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-cancelaudittask.md)

update

\*全部资源

`*`

无

无

aimiaobi:SubmitDocClusterTask

[SubmitDocClusterTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tips-openapi/api-aimiaobi-2023-08-01-submitdocclustertask.md)

create

\*全部资源

`*`

无

无

aimiaobi:DeleteFactAuditUrl

[DeleteFactAuditUrl](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-factual-review/api-aimiaobi-2023-08-01-deletefactauditurl.md)

delete

\*全部资源

`*`

无

无

aimiaobi:EditBiddingDoc

[EditBiddingDoc](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-tender-generation/api-aimiaobi-2023-08-01-editbiddingdoc.md)

update

\*全部资源

`*`

无

无

aimiaobi:SubmitAuditTask

[SubmitAuditTask](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-other/api-aimiaobi-2023-08-01-submitaudittask.md)

create

\*全部资源

`*`

无

无

aimiaobi:GetDocInfo

[GetDocInfo](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-basic-operation-class/api-aimiaobi-2023-08-01-getdocinfo.md)

get

\*全部资源

`*`

无

无

aimiaobi:GetPptTemplateSelector

[GetPptTemplateSelector](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-ppt-generation/api-aimiaobi-2023-08-01-getppttemplateselector.md)

create

\*全部资源

`*`

无

无

aimiaobi:SearchNews

[SearchNews](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-creative-articles/api-aimiaobi-2023-08-01-searchnews.md)

list

\*全部资源

`*`

无

无

aimiaobi:ExportAuditContentResult

[ExportAuditContentResult](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-pen-article-reviser/api-aimiaobi-2023-08-01-exportauditcontentresult.md)

create

\*全部资源

`*`

无

无

aimiaobi:RunDocQa

[RunDocQa](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-wonderful-reading-question-and-answer-class/api-aimiaobi-2023-08-01-rundocqa.md)

get

\*全部资源

`*`

无

无

aimiaobi:SubmitFactAuditUrl

[SubmitFactAuditUrl](raw/application-user-guide/application-gallery/quanmiao-solution-products/ai-quan-miao-development-document/amb-api-reference/api-aimiaobi-2023-08-01-dir/api-aimiaobi-2023-08-01-dir-miaobi-article-review-factual-review/api-aimiaobi-2023-08-01-submitfactauditurl.md)

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

_大模型服务平台百炼_未定义产品级别的条件关键字。如需查看适用于所有云产品的通用条件关键字，请参见通用条件关键字。

## 相关操作

您可以创建自定义权限策略，并将权限策略授予 RAM 用户、RAM 用户组或 RAM 角色。具体操作如下：

-   创建自定义权限策略
-   为 RAM 用户授权
-   为 RAM 用户组授权
-   为 RAM 角色授权
