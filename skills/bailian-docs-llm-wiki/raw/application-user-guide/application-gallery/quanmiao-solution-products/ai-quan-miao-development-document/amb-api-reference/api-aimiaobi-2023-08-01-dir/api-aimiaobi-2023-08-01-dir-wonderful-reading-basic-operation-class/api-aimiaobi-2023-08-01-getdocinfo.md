# GetDocInfo - 获取文档信息

妙读获取文档信息。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetDocInfo)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetDocInfo)

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

aimiaobi:GetDocInfo

get

\*全部资源

`*`

无

无

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

WorkspaceId

string

是

阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xxx

DocId

string

是

文档 ID

12345

CategoryId

string

否

文档所在目录

default

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

Code

string

内部错误码

successful

Data

object

返回数据

DocName

string

文档名称

電視廣播2020年報

DocType

string

文档类型

pdf

FileUrl

string

文件 url

http://xxx/xxx.pdf

Status

integer

任务状态信息

1和0，当状态为1时 表示获取文档成功，用户可进行生成文档摘要、生脑图等操作

StatusMessage

string

状态消息

导入成功

VideoContents

array

视频中的语音内容文本数组

string

视频中的语音内容文本

文本内容

CategoryId

string

文档所在目录

default

PageInfo

object

Width

integer

100

Height

integer

200

HttpStatusCode

integer

http 状态码

200

Message

string

返回结果消息

successful

RequestId

string

请求 Id

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Success

boolean

是否成功

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "successful",
  "Data": {
    "DocName": "電視廣播2020年報",
    "DocType": "pdf",
    "FileUrl": "http://xxx/xxx.pdf",
    "Status": 0,
    "StatusMessage": "导入成功",
    "VideoContents": [
      "文本内容"
    ],
    "CategoryId": "default",
    "PageInfo": {
      "Width": 100,
      "Height": 200
    }
  },
  "HttpStatusCode": 200,
  "Message": "successful",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true
}
```

## 错误码

   

**HTTP status code**

**错误码**

**错误信息**

**描述**

403

NoPermission

You are not authorized to perform this action.

请检查workspaceId的赋值

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/GetDocInfo#workbench-doc-change-demo)。
