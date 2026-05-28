# InitiatePptCreationV2 - 初始化PPT创建操作

初始化PPT创建操作V2

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/InitiatePptCreationV2)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/InitiatePptCreationV2)

## **授权信息**

当前API暂无授权信息透出。

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

llm-2setzb9x4ewsd

TaskId

string

是

任务 ID

8a7dfece-f204-4380-a7d0-a13d37de3924

ProcessType

integer

否

处理类型  
0：只生成签名，用于初始化前端 SDK，完成整个制作流程  
1：生成和签名和处理流程 ID，用于自行开发‘模版’前端页面，然后初始化前端 SDK  
2：生成作品 ID，可以直接进行作品的编辑  
3：生成导出任务 ID，可以轮询导出任务 ID 获取导出结果

1

PptTemplateType

integer

否

模板类型，默认为 1，1：系统模板，2: 企业模板

1

PptTemplateId

integer

否

PPT 模板 ID

500

PptTitle

string

否

中国传统文化艺术的魅力

Outline

string

否

PPT 大纲

\# 中国传统文化艺术的魅力 ## 1. 传统文化艺术的源远流长 ### 1.1 中国古代艺术发展历程 #### 1.1.1 古代绘画艺术的演变 - 从新石器时代的彩陶绘画到东汉时期帛画的出现，绘画形式不断丰富，展现了古人对美的独特追求。唐代绘画风格多样，吴道子的《送子天王图》线条流畅，色彩绚丽，体现了唐代绘画的高超技艺。 #### 1.1.2 书法艺术的传承与创新 - 书法从甲骨文到楷书、行书、草书，历经数千年演变，承载着中华文化的深厚内涵。王羲之的《兰亭序》被誉为“天下第一行书”，其笔法精妙，结构严谨，展现了书法艺术的巅峰。

ExternalUserId

string

否

第三方传入的用户 ID

abc

IsMobile

boolean

否

是否是移动端场景

true

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

业务数据

AppKey

string

用于初始化前端组件的 AppKey

S1X5ecouBztZelaQ

Signature

string

用于初始化前端组件的 Signature

dBBGvT0Toje5887Qw+/IwwMNYfk=

PptProcessId

string

处理流程 ID，用于初始化前端组件-创建 PPT 作品

8485143

PptArtifactId

string

作品 ID，用于作品的编辑

53059801

PptArtifactCover

string

作品封面图

http://a.com/xxx.png

ExportTaskId

string

导出任务 ID

66b25058-d735-47e5-a534-5da93453d3df

Alert

string

本月版本内的配送额度已经用尽，超额使用将走按量后付费，下个月配送额度将重新下发；请知晓

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
    "AppKey": "S1X5ecouBztZelaQ",
    "Signature": "dBBGvT0Toje5887Qw+/IwwMNYfk=",
    "PptProcessId": "8485143",
    "PptArtifactId": "53059801",
    "PptArtifactCover": "http://a.com/xxx.png",
    "ExportTaskId": "66b25058-d735-47e5-a534-5da93453d3df",
    "Alert": "本月版本内的配送额度已经用尽，超额使用将走按量后付费，下个月配送额度将重新下发；请知晓"
  }
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/InitiatePptCreationV2#workbench-doc-change-demo)。
