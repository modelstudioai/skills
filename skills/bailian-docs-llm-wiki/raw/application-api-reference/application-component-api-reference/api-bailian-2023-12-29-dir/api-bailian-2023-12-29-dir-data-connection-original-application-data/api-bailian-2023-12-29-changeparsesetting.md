# ChangeParseSetting - 修改类目解析设置

配置特定文件类型的解析方式。例如，为 .pdf 文件指定使用大模型文档解析，为 .jpg 文件指定使用Qwen VL解析。

## 接口说明

-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:ChangeParseSetting 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
    
-   本接口不具有幂等性。
    

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 10 次/秒。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/ChangeParseSetting)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/bailian/2023-12-29/ChangeParseSetting)

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

sfm:ChangeParseSetting

update

\*全部资源

`*`

无

无

## 请求语法

```
PUT /{WorkspaceId}/datacenter/parser/settings HTTP/1.1
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

类目所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。

llm-3z7uw7fwz0vxxxx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

CategoryId

string

是

类目 ID，即 **AddCategory** 接口返回的`CategoryId`，或者在[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)\-文件页签，单击类目名称旁的 ID 图标获取。

cate\_cdd11b1b79a74e8bbd675c356a91ee35xxxxxxxx

FileType

string

是

文件类型，扩展名，可能值为：

-   doc
    
-   docx
    
-   ppt
    
-   pptx
    
-   xls
    
-   xlsx
    
-   md
    
-   txt
    
-   pdf
    
-   png
    
-   jpg
    
-   jpeg
    
-   bmp
    
-   gif
    
-   html
    

pdf

Parser

string

是

解析器标识 code。不同解析器适用于不同场景，具体参见“知识库”。可能值为：

-   DOCMIND（智能文档解析）
    
-   DOCMIND\_DIGITAL （电子文档解析）
    
-   DOCMIND\_LLM\_VERSION （大模型文档解析）
    
-   DASH\_QWEN\_VL\_PARSER （Qwen VL 解析）
    

**枚举值：**

-   DOCMIND :
    
    智能文档解析
    
-   DOCMIND\_LLM\_VERSION :
    
    大模型文档解析
    
-   DOCMIND\_DIGITAL :
    
    电子文档解析
    
-   DASH\_QWEN\_VL\_PARSER :
    
    QWEN VL 解析
    

DOCMIND

ParserConfig

object

否

解析器配置，仅当类型被设置为 Qwen VL 解析时才需要传入。

modelName

string

否

模型名称。

**枚举值：**

-   qwen-vl-max :
    
    qwen-vl-max
    
-   qwen-vl-plus :
    
    qwen-vl-plus
    

qwen-vl-max

modelPrompt

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

RequestId

string

请求 ID。

7BA8ADD9-53D6-53F0-918F-A1E776AD230E

Data

object

请求成功返回的业务数据。

ChangeResult

boolean

配置是否发生变更。

-   true：配置已更新。
    
-   false：配置未发生变更，修改失败。
    

true

Status

string

接口返回的状态码。

200

Success

boolean

接口调用是否成功，可能值为：

-   true：成功 。
    
-   false：失败。
    

true

Message

string

错误信息。

User not authorized to operate on the specified resource.

Code

string

错误状态码。

InvalidParameter

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "7BA8ADD9-53D6-53F0-918F-A1E776AD230E",
  "Data": {
    "ChangeResult": true
  },
  "Status": "200",
  "Success": true,
  "Message": "User not authorized to operate on the specified resource.",
  "Code": "InvalidParameter"
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/ChangeParseSetting#workbench-doc-change-demo)。
