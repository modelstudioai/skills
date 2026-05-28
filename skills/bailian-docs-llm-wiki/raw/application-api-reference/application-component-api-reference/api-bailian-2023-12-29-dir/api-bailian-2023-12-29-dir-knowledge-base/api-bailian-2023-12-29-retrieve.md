# Retrieve - 检索知识库

在指定的知识库中检索信息。

## 接口说明

-   **调用方式**：可通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)（配合阿里云访问密钥 [AccessKey](https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair) ）或[Spring AI Alibaba](https://help.aliyun.com/zh/model-studio/spring-ai-alibaba-integrate-knowledge-base)（配合阿里云百炼[API-Key](https://help.aliyun.com/zh/model-studio/get-api-key)）检索知识库，两者均已封装复杂的签名计算逻辑，可简化您的调用过程。
    
-   **权限要求**：
    -   **RAM 用户（子账号）**：需先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（可使用`AliyunBailianDataFullAccess`策略，该策略已包含本接口所需的 sfm:Retrieve 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，才能调用本接口。
        
    -   **阿里云账号（主账号）**：默认拥有权限，可直接调用。
        
-   **响应延迟**：由于接口调用包含复杂的检索和匹配，响应时间可能较长，建议您合理设置请求的超时与重试策略。
    
-   **幂等性**：本接口具有幂等性。
    

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/Retrieve)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/bailian/2023-12-29/Retrieve)

## **授权信息**

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
        
    -   对于不支持资源级授权的操作，用`全部资源`表示。
        
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

**操作**

**访问级别**

**资源类型**

**条件关键字**

**关联操作**

sfm:Retrieve

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{WorkspaceId}/index/retrieve HTTP/1.1
```

## 路径参数

**名称**

**类型**

**必填**

**描述**

**示例值**

WorkspaceId

string

是

知识库所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。

llm-3shx2gu255oqxxxx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

Query

string

否

输入文本（原始输入 prompt）。Query 的长度和字符没有限制。

阿里云百炼平台介绍

DenseSimilarityTopK

integer

否

向量检索 Top K，通过生成输入文本的向量并在知识库中检索与其向量表示最相似的 K 个文本切片。K 的取值范围\[0-100\]。 `DenseSimilarityTopK`和`SparseSimilarityTopK`二者之和小于等于 200。

默认值为 100。

100

EnableReranking

boolean

否

是否开启重排序。更多信息，请参见[知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)。取值范围：

-   true：开启。
    
-   false：不开启。
    

默认值为 true。

**枚举值：**

-   true :
    
    开启
    
-   false :
    
    不开启
    

true

EnableRewrite

boolean

否

是否开启[多轮对话改写](https://help.aliyun.com/model-studio/use-cases/rag-optimization#b7031e2ad6cji)。 取值范围：

-   true：开启。
    
-   false：不开启。
    

默认值为 false。

**枚举值：**

-   true :
    
    开启
    
-   false :
    
    不开启
    

false

Rerank

array<object>

否

重排序配置。

object

否

重排序配置对象。

ModelName

string

否

使用指定的排序模型。此处指定值将覆盖创建知识库时所选择的排序模型。取值范围：

-   qwen3-rerank-hybrid：qwen3-rerank(hybrid)排序。
    
-   qwen3-rerank：qwen3-rerank 排序。
    
-   gte-rerank-hybrid：gte-rerank(hybrid)排序。
    
-   gte-rerank：gte-rerank 排序。
    

默认值为空，使用创建知识库时选择的排序模型。

**说明**

如仅需语义排序，可使用`qwen3-rerank`；若同时需要语义排序和文本匹配特征以确保相关性，建议使用`qwen3-rerank-hybrid`。

**说明**

`gte-rerank-hybrid`与`gte-rerank`后续停止更新，不建议使用。

**枚举值：**

-   gte-rerank-hybrid :
    
    gte-rerank(hybrid)排序
    
-   gte-rerank :
    
    gte-rerank 排序
    

gte-rerank-hybrid

RerankMode

string

否

指定重排序模型的指令干预模式，以决定其评分偏好。

**可选值：**

-   **qa**:（默认值） 问答模式。模型倾向于为能直接回答查询（Query）的候选项赋予更高分。建议在问答场景使用。
    
-   **similar**: 相似模式。模型倾向于为与查询内容一致性高的候选项赋予更高分。建议在匹配检索场景使用。
    
-   **custom**: 自定义模式。模型的排序行为由 rerank\_instruct 参数中的指令决定。
    

**枚举值：**

-   similar: 相似模式。 :
    
    similar: 相似模式。
    
-   custom: 自定义模式。 :
    
    custom: 自定义模式。
    
-   qa:（默认值） 问答模式。 :
    
    qa:（默认值） 问答模式。
    

qa

RerankInstruct

string

否

提供一个自然语言指令，用于精细化控制重排序模型的行为。

**重要** 此参数仅在 rerank\_mode 设置为 "custom" 时生效。

RerankMinScore

number

否

相似度阈值。该阈值表示允许召回的文本切片的最低相似度分数，用于筛选 Rank 模型返回的文本切片，即只有分数超过此数值的文本切片才会被召回。取值范围\[0.01-1.00\]。此参数的优先级大于知识库相似度阈值配置。

当未指定具体值时，默认采用该知识库配置的相似度阈值。

0.20

RerankTopN

integer

否

重排序后的 Top N 返回数据。取值范围\[1-20\]，默认值为 5。

5

Rewrite

array<object>

否

多轮对话改写配置。

object

否

多轮对话改写配置对象。

ModelName

string

否

多轮对话改写模型名称。它会基于会话上下文自动调整原始输入 prompt（用户问题）以提升检索效果。取值范围：

-   conv-rewrite-qwen-1.8b：conv-rewrite-qwen-1.8b 模型（目前只支持该模型）
    

默认值为空，采用 conv-rewrite-qwen-1.8b 模型。

**枚举值：**

-   conv-rewrite-qwen-1.8b :
    
    conv-rewrite-qwen-1.8b 模型
    

conv-rewrite-qwen-1.8b

SparseSimilarityTopK

integer

否

关键词检索 TopK，即在知识库中查找与输入文本的关键词精确匹配的切片。它可以帮助您过滤掉无关的文本切片，提供更准确的结果。 取值范围\[0-100\]。 `DenseSimilarityTopK`和`SparseSimilarityTopK`二者之和小于等于 200。

默认值为：100。

100

IndexId

string

是

知识库 ID，即 **CreateIndex** 接口返回的`Data.Id`。

**说明**

-   请确保对应知识库已成功创建且未被删除。
    

5pwe0mxxxx

SaveRetrieverHistory

boolean

否

是否保存历史文本切片召回测试数据。取值范围：

-   true：保存。
    
-   false：不保存。
    

默认值为：false。

false

SearchFilters

array<object>

否

支持通过 SearchFilter 设置个性化的检索条件（比如标签），对语义检索结果进行过滤，以排除与查询 Query 无关的信息。 设置 is\_displayed\_chunk\_content 参数为 true 生效筛选逻辑，具体内容请参见[知识库 SearchFilters](https://help.aliyun.com/zh/model-studio/how-to-use-search-filters)。

object

否

检索条件对象。

string

否

Images

array

否

支持在提问时传入图片 URL 地址。

string

否

检索图片问答类知识库时您可传入图片 URL 地址。当该知识库中存在图片索引时，系统会将输入图片转为向量并检索到相关记录；如果不存在图片索引，则输入的图片不会用于检索。

**说明**

本字段不支持文档搜索/数据查询/音视频搜索类知识库（即使传入也不生效）

**说明**

请确保链接公开可访问且指向一个有效的图片文件。格式示例：https://example.com/downloads/pic.jpg

https://example.com/downloads/pic.jpg

QueryHistory

array<object>

否

[多轮对话改写](https://help.aliyun.com/model-studio/use-cases/rag-optimization#b7031e2ad6cji)支持您传入自己管理的对话历史。仅在 EnableRewrite=**true** 时生效（否则即使传入也不生效）。

object

否

role

string

否

角色。

取值范围：

-   user：传入此角色，此时 content 表示您输入给阿里云百炼应用的文本。
    
-   assistant：传入此角色，此时 content 表示阿里云百炼应用的回复。
    

user

content

string

否

对应角色的问题或者回答内容。

代表一段文本。

Extra

object

否

uniqueId

string

否

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Code

string

错误状态码。

Index.InvalidParameter

Data

object

接口业务数据字段。

Nodes

array<object>

命中的文本切片列表。

object

文本切片对象。

Metadata

any

文本切片的元数据 Map。

**说明**

文档搜索类知识库的元数据 Map 中`file_path`字段无意义，请勿在业务代码中使用。

**说明**

检索文档搜索类识库时，若切片包含图片，将通过元数据 Map 中`image_url`字段透出，并附有过期时间。

**说明**

检索音视频搜索类知识库时，若切片包含音频，将通过元数据 Map 中`audio_url`字段透出，并附有过期时间。

**说明**

检索音视频搜索类知识库时，若切片包含视频，将通过元数据 Map 中`video_url`字段透出，并附有过期时间。

{ "parent": "", "file\_path": "https://\*\*\*", "image\_url": \[ "http://\*\*\*" \], "nid": "\*\*\*", "title": "阿里云百炼文档", "doc\_id": "doc\_\*\*\*", "content": "阿里云百炼是基于通义大模型、行业大模型以及三方大模型的一站式大模型开发平台。面向企业客户和个人开发者，提供完整的模型服务工具和全链路应用开发套件，预置丰富的能力插件，提供API及SDK等便捷的集成方式，高效完成大模型应用构建", "workspace\_id": "ws\_\*\*\*", "hier\_title": "阿里云百炼文档", "doc\_name": "阿里云百炼文档介绍.pdpf", "pipeline\_id": "rhd\*\*\*", "\_id": "ws\_\*\*\*" }

Score

number

文本切片的相似度得分，可能值范围：\[0-1\]。

0.3

Text

string

文本切片内容。

阿里云百炼是基于通义大模型、行业大模型以及三方大模型的一站式大模型开发平台。面向企业客户和个人开发者，提供完整的模型服务工具和全链路应用开发套件，预置丰富的能力插件，提供API及SDK等便捷的集成方式，高效完成大模型应用构建。

Message

string

错误信息。

Required parameter(%s) missing or invalid, please check the request parameters.

RequestId

string

请求 ID。

17204B98-7734-4F9A-8464-2446A84821CA

Status

string

接口返回的状态码。

200

Success

boolean

接口调用是否成功，可能值为：

-   true：成功。
    
-   false：失败。
    

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "Index.InvalidParameter",
  "Data": {
    "Nodes": [
      {
        "Metadata": "{\n  \"parent\": \"\",\n  \"file_path\": \"https://***\",\n  \"image_url\": [\n    \"http://***\"\n  ],\n  \"nid\": \"***\",\n  \"title\": \"阿里云百炼文档\",\n  \"doc_id\": \"doc_***\",\n  \"content\": \"阿里云百炼是基于通义大模型、行业大模型以及三方大模型的一站式大模型开发平台。面向企业客户和个人开发者，提供完整的模型服务工具和全链路应用开发套件，预置丰富的能力插件，提供API及SDK等便捷的集成方式，高效完成大模型应用构建\",\n  \"workspace_id\": \"ws_***\",\n  \"hier_title\": \"阿里云百炼文档\",\n  \"doc_name\": \"阿里云百炼文档介绍.pdpf\",\n  \"pipeline_id\": \"rhd***\",\n  \"_id\": \"ws_***\"\n}",
        "Score": 0.3,
        "Text": "阿里云百炼是基于通义大模型、行业大模型以及三方大模型的一站式大模型开发平台。面向企业客户和个人开发者，提供完整的模型服务工具和全链路应用开发套件，预置丰富的能力插件，提供API及SDK等便捷的集成方式，高效完成大模型应用构建。"
      }
    ]
  },
  "Message": "Required parameter(%s) missing or invalid, please check the request parameters.",
  "RequestId": "17204B98-7734-4F9A-8464-2446A84821CA",
  "Status": "200",
  "Success": true
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/Retrieve#workbench-doc-change-demo)。
