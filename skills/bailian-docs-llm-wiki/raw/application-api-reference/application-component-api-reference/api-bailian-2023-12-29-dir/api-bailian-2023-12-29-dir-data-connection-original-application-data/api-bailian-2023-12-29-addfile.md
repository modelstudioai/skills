# AddFile - 添加文件

将存储于阿里云百炼临时存储空间内的文件导入至阿里云百炼数据连接（原应用数据）。

## 接口说明

-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:AddFile 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
    
-   本接口不具备幂等性。
    

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 10 次/秒。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/AddFile)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/bailian/2023-12-29/AddFile)

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

sfm:AddFile

create

\*全部资源

`*`

无

无

## 请求语法

```
PUT /{WorkspaceId}/datacenter/file HTTP/1.1
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

业务空间 ID，即文件将上传至该业务空间中。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。

llm-3shx2gu255oqxxxx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

LeaseId

string

是

上传租约 ID，对应 **ApplyFileUploadLease** 接口返回的 `FileUploadLeaseId`。

68abd1dea7b6404d8f7d7b9f7fbd332d.17166xxxxxxxx

Parser

string

是

解析器类型。可能取值范围包括：

-   DOCMIND（智能文档解析）
    
-   DOCMIND\_DIGITAL（电子文档解析）
    
-   DOCMIND\_LLM\_VERSION（大模型文档解析）
    
-   DASH\_QWEN\_VL\_PARSER（Qwen VL 解析）
    
-   DOCMIND\_LLM\_VERSION\_MEDIA（音视频解析）
    
-   AUTO\_SELECT（自动选择解析器）
    

**说明** 当 CategoryType 为 UNSTRUCTURED 时，解析器会根据当前类目的数据解析设置，对您上传的文件进行解析。

**说明** 当 CategoryType 为 SESSION\_FILE 时，系统将使用默认方式（不支持更改）解析文件内容。

AUTO\_SELECT

CategoryId

string

是

-   当 CategoryType 为 UNSTRUCTURED 时，需传入上传文件所属类目 ID，即 **AddCategory** 接口返回的`CategoryId`。您也可以前往[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)\-文件页签，单击类目名称旁的 ID 图标获取类目 ID。此处允许传入 default，即使用系统创建的“默认类目”。
    
-   当 CategoryType 为 SESSION\_FILE 时，传入“default”即可。
    

cate\_cdd11b1b79a74e8bbd675c356a91ee35xxxxxxxx

Tags

array

否

-   文件关联的标签列表。最多传入 100 个标签，所有标签字符长度总和不能超过 700。
    
-   默认值为空，即不设置标签。
    

string

否

文件的标签。每个标签最多 32 个字符，支持 Unicode 中 letter 分类下的字符（其中包括英文、中文和数字等），下划线\_，中划线-。

产品介绍

CategoryType

string

否

类目类型，可选，默认值为 UNSTRUCTURED，取值范围：

-   UNSTRUCTURED：类目，用于构建知识库场景。
    
-   SESSION\_FILE：用于智能体应用[会话交互](https://help.aliyun.com/zh/model-studio/user-guide/file-interaction)的文件。
    
    **说明** 在使用 `SESSION_FILE` 的情况下，调用 ApplyFileUploadLease 接口时，CategoryType 参数也应传入 `SESSION_FILE`。
    
    **说明** 仅用户当前会话有效，用户关闭会话后文件过期（最长有效期为 7 天），不支持长期保存。
    

UNSTRUCTURED

OriginalFileUrl

string

否

通过此参数为文件添加一个 URL，系统将在构建[文档搜索类知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)时记录该链接。在使用阿里云百炼控制台与[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)对话时，随该文件召回结果返回（通过`docUrl`字段）。

**说明**

智能体应用必须开启**知识库**，并启用**展示回答来源**功能，否则此参数不生效。

www.test.com/111.docx

ParserConfig

object

否

解析器配置，仅当类型被设置为 Qwen VL 解析时才需要传入。

ModelName

string

否

模型名称。

qwen-vl-max

ModelPrompt

string

否

调用 Qwen VL 解析时的 Prompt。

#角色 你是一个专业的图片内容标注人员，擅长识别并描述出图片中的内容。 # 任务目标 请结合输入图片，详细描述图片中的内容。

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

Code

string

错误状态码

DataCenter.FileTooLarge

Data

object

接口业务数据字段

FileId

string

文件 ID，请妥善保管该值，它将用于后续与此文件相关的所有 API 操作

file\_9a65732555b54d5ea10796ca5742ba22\_xxxxxxxx

Parser

string

解析该文件使用的解析器类型。可能值为：

-   DASHSCOPE\_DOCMIND：阿里云文档智能解析
    

DASHSCOPE\_DOCMIND

Message

string

错误信息

User not authorized to operate on the specified resource.

RequestId

string

请求 ID

778C0B3B-xxxx-5FC1-A947-36EDD13606AB

Status

string

接口返回的状态码

200

Success

string

接口调用是否成功，可能值为：

-   true：成功
    
-   false：失败
    

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "DataCenter.FileTooLarge",
  "Data": {
    "FileId": "file_9a65732555b54d5ea10796ca5742ba22_xxxxxxxx",
    "Parser": "DASHSCOPE_DOCMIND"
  },
  "Message": "User not authorized to operate on the specified resource.",
  "RequestId": "778C0B3B-xxxx-5FC1-A947-36EDD13606AB",
  "Status": "200",
  "Success": "true"
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/AddFile#workbench-doc-change-demo)。
