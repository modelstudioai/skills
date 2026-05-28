# GetPptInfo - 查询PPT任务信息

查询PPT任务信息

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetPptInfo)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetPptInfo)

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

aimiaobi:GetPptInfo

create

\*全部资源

`*`

无

无

## 请求语法

```
POST  HTTP/1.1
```

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

WorkspaceId

string

否

业务空间 ID

llm-2setzb9xb8mx6vss

ExternalUserId

string

否

abc

TaskId

string

否

PPT 任务的 ID

1f178f22-ec52-467d-8489-eef4468x0240

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

RequestId

string

Id of the request

xxxxx

Success

boolean

此次请求是否成功

true

Code

string

错误码

DataNotExists

Message

string

错误消息

错误消息

HttpStatusCode

integer

http 错误码

400

Data

object

数据对象

TaskId

string

PPT 任务的 ID

xxx-xxx-xx

Query

string

PPT 任务的输入信息

关于班会主题的PPT

PptProcessId

string

PPT 流程 ID

11231232

PptArtifactId

string

PPT 作品 ID

5423431

PptArtifactCover

string

http://a.com/xxx.jpeg

ExportTaskId

string

导出任务的 key

xxx-xxx-xx

ExportFileLink

array

导出文件链接

string

文件链接

http://xxx.com/a.pptx

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "xxxxx",
  "Success": true,
  "Code": "DataNotExists",
  "Message": "错误消息",
  "HttpStatusCode": 400,
  "Data": {
    "TaskId": "xxx-xxx-xx",
    "Query": "关于班会主题的PPT",
    "PptProcessId": "11231232",
    "PptArtifactId": "5423431",
    "PptArtifactCover": "http://a.com/xxx.jpeg",
    "ExportTaskId": "xxx-xxx-xx",
    "ExportFileLink": [
      "http://xxx.com/a.pptx"
    ]
  }
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/GetPptInfo#workbench-doc-change-demo)。
