# InitiatePptCreation - 初始化用来创建PPT的会话

重要说明：这个接口涉及到扣费，请注意费用 这个接口包含两个操作： 1. 下发用于初始化“PPT生成”的前端组件的code 2. 进行计费

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/InitiatePptCreation)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/InitiatePptCreation)

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

aimiaobi:InitiatePptCreation

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

阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-3fy94b2rtadt01qa

TaskId

string

是

任务 ID

95c2fbe6-5a20-4fc2-8a93-376ed05fbe13

Outline

string

否

大纲

\# 中国传统文化艺术的魅力 ## 1. 传统文化艺术的源远流长 ### 1.1 中国古代艺术发展历程 #### 1.1.1 古代绘画艺术的演变 - 从新石器时代的彩陶绘画到东汉时期帛画的出现，绘画形式不断丰富，展现了古人对美的独特追求。唐代绘画风格多样，吴道子的《送子天王图》线条流畅，色彩绚丽，体现了唐代绘画的高超技艺。 #### 1.1.2 书法艺术的传承与创新 - 书法从甲骨文到楷书、行书、草书，历经数千年演变，承载着中华文化的深厚内涵。王羲之的《兰亭序》被誉为“天下第一行书”，其笔法精妙，结构严谨，展现了书法艺术的巅峰。

ExternalUserId

string

否

abc

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

11AC01F1-88FB-5C4D-B6F5-E8BB136CD5A3

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

返回数据

AppKey

string

AppKey

S1X5ecouBztZelaQ

Code

string

Code

7dhqd2

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "11AC01F1-88FB-5C4D-B6F5-E8BB136CD5A3",
  "Success": true,
  "Code": "DataNotExists",
  "Message": "错误消息",
  "HttpStatusCode": 400,
  "Data": {
    "AppKey": "S1X5ecouBztZelaQ",
    "Code": "7dhqd2"
  }
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/InitiatePptCreation#workbench-doc-change-demo)。
