# ListStyleLearningResult - 获取文体学习分析结果列表

获取文体学习分析结果列表。

## 接口说明

全妙产品支持 iframe 嵌入 具体请参考文档： [客户对接\_全妙公有云 iframe 定制方案](https://help.aliyun.com/zh/model-studio/iframe-embedding-scheme)

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListStyleLearningResult)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListStyleLearningResult)

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

aimiaobi:ListStyleLearningResult

list

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

AgentKey

string

是

业务空间唯一标识： [AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)

xxxxx\_p\_efm

Current

integer

否

当前页码

1

Size

integer

否

每页条数：默认 10

10

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

PageResult

Code

string

状态码

NoData

Current

integer

当前页码

1

Data

array<object>

文体学习分析结果集合

object

业务数据

AigcResult

string

AIGC 生成的内容

AIGC 生成的内容

Id

integer

文体学习分析结果 ID

70

RewriteResult

string

用户修订后内容

用户修订后内容

StyleName

string

文体风格名称

文体风格名称

TaskId

string

文体分析时的任务 ID

3f7045e099474ba28ceca1b4eb6d6e21

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

success

RequestId

string

请求唯一标识

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Size

integer

每页记录条数

10

Success

boolean

是否成功：true 成功，false 失败

true

Total

integer

总记录条数

100

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "NoData",
  "Current": 1,
  "Data": [
    {
      "AigcResult": "AIGC 生成的内容",
      "Id": 70,
      "RewriteResult": "用户修订后内容",
      "StyleName": "文体风格名称",
      "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21"
    }
  ],
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Size": 10,
  "Success": true,
  "Total": 100
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/ListStyleLearningResult#workbench-doc-change-demo)。
