# UpdateIndex - 更新知识库

更新指定知识库的部分配置。

## 接口说明

RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。 调用本接口前，请确保您的知识库已经创建完成且未被删除（即知识库 ID`IndexId`有效）。 本接口具有幂等性。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/UpdateIndex)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/bailian/2023-12-29/UpdateIndex)

## 授权信息

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。

操作

访问级别

资源类型

条件关键字

关联操作

sfm:UpdateIndex

update

\*全部资源

`*`

无

无

## 请求语法

```
POST /{WorkspaceId}/index/update HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

WorkspaceId

string

是

业务空间 ID

llm-3shx2gu255oqxxxx

Id

string

是

知识库 ID

79c0alxxxx

Name

string

否

知识库名称

企业帮助文档库

Description

string

否

知识库描述

企业知识库

RerankMinScore

string

否

排序最低分数，取值范围\[0-1\]

0.01

DenseSimilarityTopK

integer

否

向量检索 Top K，通过生成输入文本的向量并在知识库中检索与其向量表示最相似的 K 个文本切片。K 的取值范围\[0-100\]。 `DenseSimilarityTopK`和`SparseSimilarityTopK`二者之和小于等于 200。

默认值为 100。

100

SparseSimilarityTopK

integer

否

关键词检索 TopK，即在知识库中查找与输入文本的关键词精确匹配的切片。它可以帮助您过滤掉无关的文本切片，提供更准确的结果。 取值范围\[0-100\]。 `DenseSimilarityTopK`和`SparseSimilarityTopK`二者之和小于等于 200。

默认值为：100。

100

PipelineCommercialType

string

否

知识库的规格类型。取值范围：

-   standard：标准版
    
-   enterprise：旗舰版
    

standard

PipelineCommercialCu

integer

否

指定旗舰版知识库的 RCU 数量，即仅当 pipelineCommercialType 指定 enterprise 时才需要传入。

取值范围：\[1-200\]。

3

参数 Name，Description，RerankMinScore ，至少填写一项，不能同时为空。

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

RequestId

string

请求 ID

17204B98-7734-4F9A-8464-xxx

Data

object

接口业务数据字段

Id

string

知识库 ID

79c0alxxxx

Status

string

接口返回的状态码

200

Success

boolean

接口调用是否成功，可能值为：

true：成功

false：失败

true

Message

string

错误信息

Required parameter(%s) missing or invalid, please check the request parameters.

Code

string

状态码

Success

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "17204B98-7734-4F9A-8464-xxx",
  "Data": {
    "Id": "79c0alxxxx"
  },
  "Status": 200,
  "Success": true,
  "Message": "Required parameter(%s) missing or invalid, please check the request parameters.",
  "Code": "Success"
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/bailian/2023-12-29/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2026-01-19

新增 OpenAPI

[查看变更详情](https://api.aliyun.com/document/bailian/2023-12-29/UpdateIndex?updateTime=2026-01-19#workbench-doc-change-demo)
