# ListChunks - 查询索引下的分片列表

查看文本切片列表及信息。

## 接口说明

-   对于文档搜索或音视频搜索类知识库，本接口可查询指定文件的所有切片内容；而对于数据查询或图片问答类知识库，则可获取全部文本切片的信息。
-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:ChunkList 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
-   调用本接口前，请确保您的知识库已经创建完成且未被删除（即知识库 ID`IndexId`有效）。
-   本接口具有幂等性。

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 10 次/秒。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/ListChunks)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/bailian/2023-12-29/ListChunks)

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

sfm:ChunkList

list

\*全部资源

`*`

无

无

## 请求语法

```
POST /{WorkspaceId}/index/list_chunks HTTP/1.1
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

知识库所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。

llm-3z7uw7fwz0vxxxx

body

object

否

请求参数的主体信息。

Fields

array

否

Fields 是一个字段名数组，用于对本接口返回的 Metadata 字段中的非私有 Field（以\_下划线为前缀）进行过滤。默认 Fields 为空时，Metadata 字段中的所有非私有的 Field 都会返回。若您希望返回的 Metadata 字段只包含指定的非私有 Field，比如只包含 title，则此处传入 title 即可。

默认值为空。

string

否

字段名。

name

Filed

string

否

本字段为阿里云百炼旧版 SDK 中的文件 ID 字段。具体用法和默认值与`FileId`字段完全一致。如果您使用的阿里云百炼 SDK 是以下版本（或更新版本），推荐改用 `FileId` 字段指定文件 ID。如果您使用的是 SWIFT 语言的阿里云百炼 SDK，请继续使用本字段。

-   Java（异步）：1.0.18
-   Java：1.10.2
-   TypeScript：1.10.2
-   Go：1.10.2
-   PHP：1.10.2
-   Python：1.10.2
-   C#：1.10.2
-   C++：1.10.17

**说明** **如何查看阿里云百炼 SDK 版本**：访问[阿里云百炼 SDK 中心](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)，单击左侧导航栏中的“**安装**”，API 版本选择“**2023-12-29**”，然后选择您的开发语言，再单击“**历史版本**”即可查看。

file\_5f03dfea56da4050ab68d61871fc4cb3\_xxxxxxxx

FileId

string

否

文件 ID，即 **AddFile** 接口返回的`FileId`。数据查询/图片问答类知识库不用传入此字段；文档搜索/音视频搜索类知识库必须传入此字段。您也可以在[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)\-文件页签，单击文件名称旁的 ID 图标获取。可以通过文件 ID 筛选返回的切片。默认值为空。

file\_5f03dfea56da4050ab68d61871fc4cb3\_xxxxxxxx

IndexId

string

是

知识库 ID，即 **CreateIndex** 接口返回的`Data.Id`。

otoru9xxxx

PageNum

integer

否

指定要查询的页码。起始值为 1，默认值为 1。

1

PageSize

integer

否

指定分页查询时每页展示的文本切片数量。最大为 100。默认值为 10。

10

## 返回参数

名称

类型

描述

示例值

object

Code

string

错误状态码。

Index.InvalidParameter

Data

object

接口返回的业务字段。

Nodes

array<object>

文本切片列表。

nodes

object

文本切片对象。

Metadata

any

文本切片的元数据 Map。

**说明** 文档搜索类知识库的元数据 Map 中`file_path`字段无意义，请勿在业务代码中使用。

**说明** 检索文档搜索类识库时，若切片包含图片，将通过元数据 Map 中`image_url`字段透出，并附有过期时间。

**说明** 检索音视频搜索类知识库时，若切片包含音频，将通过元数据 Map 中`audio_url`字段透出，并附有过期时间。

**说明** 检索音视频搜索类知识库时，若切片包含视频，将通过元数据 Map 中`video_url`字段透出，并附有过期时间。

{ "file\_path": "https://bailian-\*\*\*", "parent": "阿里云百炼是一站式的大模型开发及应用构建平台。不论是开发者还是业务人员，都能深入参与大模型应用的设计和构建。您可以通过简单的界面操作，在 5分钟内开发出一款大模型应用，或在几小时内训练出一个专属模型，从而将更多精力专注于应用创新。", "is\_displayed\_chunk\_content": "true", "image\_url": \[\], "nid": "83\*\*\*", "source": "0", "\_score": 0, "title": "", "doc\_id": "file\_24e\*\*\*", "content": "阿里云百炼是一站式的大模型开发及应用构建平台。不论是开发者还是业务人员，都能深入参与大模型应用的设计和构建。您可以通过简单的界面操作，在 5分钟内开发出一款大模型应用，或在几小时内训练出一个专属模型，从而将更多精力专注于应用创新。", "\_rc\_score": 0, "workspace\_id": "llm-zna\*\*\*", "hier\_title": "", "doc\_name": "什么是阿里云百炼", "pipeline\_id": "j6b\*\*\*", "\_id": "llm-zna5\*\*\*" }

Score

double

文本切片的相似度得分。

0

Text

string

文本切片内容。

阿里云百炼是一站式的大模型开发及应用构建平台。不论是开发者还是业务人员，都能深入参与大模型应用的设计和构建。您可以通过简单的界面操作，在 5分钟内开发出一款大模型应用，或在几小时内训练出一个专属模型，从而将更多精力专注于应用创新。

Total

long

返回结果的总条数。

1

Message

string

错误信息。

Required parameter(%s) missing or invalid, please check the request parameters.

RequestId

string

请求 ID。

8F97A63B-xxxx-527F-9D6E-467B6A7E8CF1

Status

string

接口返回的状态码。

200

Success

boolean

接口调用是否成功，可能值：

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
        "Metadata": {
          "file_path": "https://bailian-***",
          "parent": "阿里云百炼是一站式的大模型开发及应用构建平台。不论是开发者还是业务人员，都能深入参与大模型应用的设计和构建。您可以通过简单的界面操作，在 5分钟内开发出一款大模型应用，或在几小时内训练出一个专属模型，从而将更多精力专注于应用创新。",
          "is_displayed_chunk_content": true,
          "image_url": [],
          "nid": "83***",
          "source": 0,
          "_score": 0,
          "title": "",
          "doc_id": "file_24e***",
          "content": "阿里云百炼是一站式的大模型开发及应用构建平台。不论是开发者还是业务人员，都能深入参与大模型应用的设计和构建。您可以通过简单的界面操作，在 5分钟内开发出一款大模型应用，或在几小时内训练出一个专属模型，从而将更多精力专注于应用创新。",
          "_rc_score": 0,
          "workspace_id": "llm-zna***",
          "hier_title": "",
          "doc_name": "什么是阿里云百炼",
          "pipeline_id": "j6b***",
          "_id": "llm-zna5***"
        },
        "Score": 0,
        "Text": "阿里云百炼是一站式的大模型开发及应用构建平台。不论是开发者还是业务人员，都能深入参与大模型应用的设计和构建。您可以通过简单的界面操作，在 5分钟内开发出一款大模型应用，或在几小时内训练出一个专属模型，从而将更多精力专注于应用创新。"
      }
    ],
    "Total": 1
  },
  "Message": "Required parameter(%s) missing or invalid, please check the request parameters.",
  "RequestId": "8F97A63B-xxxx-527F-9D6E-467B6A7E8CF1",
  "Status": 200,
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/bailian/2023-12-29/errorCode>)查看更多错误码。
