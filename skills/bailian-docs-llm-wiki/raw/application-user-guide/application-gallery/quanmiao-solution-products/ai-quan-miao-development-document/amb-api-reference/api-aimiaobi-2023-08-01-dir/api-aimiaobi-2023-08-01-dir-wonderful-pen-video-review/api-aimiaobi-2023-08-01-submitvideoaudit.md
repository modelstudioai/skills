# SubmitVideoAudit - 提交视频审校任务

提交视频审校

## 接口说明

全妙产品支持 iframe 嵌入 具体请参考文档： [客户对接\_全妙公有云 iframe 定制方案](https://alidocs.dingtalk.com/i/nodes/m9bN7RYPWdyrPBREcyM6jDQ2VZd1wyK0?cid=116617178%3A898142682&utm_source=im&utm_scene=team_space&iframeQuery=utm_medium%3Dim_card%26utm_source%3Dim&utm_medium=im_card&corpId=dingd8e1123006514592)

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitVideoAudit)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitVideoAudit)

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

aimiaobi:SubmitVideoAudit

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /quanmiao/aimiaobi/pop/videoAudit/submitVideoAudit HTTP/1.1
```

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

WorkspaceId

string

是

业务空间 ID

llm-xxxxx

FileKey

string

否

妙笔系统内部文件唯一标识（FileKey 与 Url 二选一）

oss://default/xxx/video/test.mp4

Url

string

否

视频 URL（FileKey 与 Url 二选一）

https://example.com/video.mp4

SnapshotInterval

number

否

抽帧间隔

1.0

Ext

string

否

扩展参数

{}

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

提交任务响应

RequestId

string

请求 ID

1813ceee-7fe5-41b4-87e5-982a4d18cca5

HttpStatusCode

integer

HTTP 状态码

200

Code

string

业务状态码

success

Message

string

返回信息

任务提交成功

Success

boolean

是否成功

true

Data

object

提交任务结果数据

TaskId

string

任务 ID

xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "HttpStatusCode": 200,
  "Code": "success",
  "Message": "任务提交成功",
  "Success": true,
  "Data": {
    "TaskId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  }
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/SubmitVideoAudit#workbench-doc-change-demo)。
