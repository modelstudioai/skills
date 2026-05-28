# SubmitCustomSourceTopicAnalysis - 提交自定义源话题选题分析任务

从自定义数据源提交选题热点分析

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitCustomSourceTopicAnalysis)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitCustomSourceTopicAnalysis)

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

aimiaobi:SubmitCustomSourceTopicAnalysis

create

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

FileUrl

string

否

文件 URL（FileUrl 与 News 二选一）（文件的结构请参考 News 字段）

http://www.example.com/xxx.json

FileType

string

否

文件类型（json: json 数组格式，jsonLine：json 行格式）

json

MaxTopicSize

integer

否

最大分析的话题数量（默认情况下 会按照聚类后的新闻数量倒排，取 TOP50 进行话题分析，最大 200 条 ）

50

News

array<object>

否

新闻列表（FileUrl 与 News 二选一）

array<object>

否

新闻对象

Title

string

否

新闻标题

新闻标题

Content

string

否

新闻正文

新闻正文

Url

string

否

新闻 URL

http://www.example.com/xxx.html

Comments

array<object>

否

评论列表

object

否

评论对象

Text

string

否

评论内容

评论内容

PubTime

string

否

发布时间(格式为： YYYY-MM-dd HH:mm:ss)

2024-01-22 10:29:00

Source

string

否

新闻来源

百度

WorkspaceId

string

是

[百炼业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xx

AnalysisTypes

array

否

选题热点要分析的类型（多选，不传默认分析全部。 传空数组，默认不做选题热点分析，仅聚类。） HotViewPoints： 热门选题视角分析 WebReviewPoints： 网友选题视角分析（需要有评论） TimedViewPoints：时效性选题视角分析 FreshViewPoints：新颖视角分析 TopicSummary：新闻摘要分析

string

否

选题热点要分析的类型

TimedViewPoints

Topics

array<object>

否

话题列表

object

否

话题对象

Topic

string

否

话题名称

话题名称

News

array

否

新闻列表

[HottopicNews](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-hottopicnews)

否

新闻对象

TopicsFileUrl

string

否

话题列表 URL(使用 json line 格式，每行是一个 json)

http://www.example.com/xxx.jsonline

支持两种分析模式

1.  传 一批文章，进行 新闻聚类 -> 然后进行 选题策划分析
    
    1.  待分析的内容为 新闻列表 对象 具体结构 请参考：News 字段。
        
    2.  News 字段与 fileUrl 字段二选一
        
    3.  支持分析的新闻数最大支持 1w 条新闻。
        
    4.  支持最大 产出的聚合话题 200 个。由参数：MaxTopicSize 控制。
        
2.  从聚类好的新闻 直接进行选题策划分析
    
    1.  待分析的内容为 话题列表 对象 具体结构 请参考：Topics 字段
        
    2.  Topics 字段与 TopicsFileUrl 字段二选一
        
3.  支持将分析结果导出为 json 或者 excel。参考[导出接口](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-exportcustomsourceanalysistask)的 ExportType 字段
    
4.  最佳实践请参考：[妙策自定义数据源最佳实践](https://help.aliyun.com/zh/model-studio/best-practices-for-miaoce-api)
    

fileUrl 示例格式为：

```
[
  {
    "Content": "这是一篇关于人工智能技术的示例文章。人工智能正在快速发展，在各个领域都有广泛应用。从自动驾驶到医疗诊断，AI 技术正在改变我们的生活方式。",
    "Title": "人工智能技术的发展趋势",
    "Source": "科技日报"
  },
  {
    "Content": "随着气候变化问题日益严重，可再生能源成为全球关注的焦点。太阳能、风能等清洁能源技术的进步，为解决环境问题提供了新的可能。",
    "Title": "可再生能源的未来",
    "Source": "环保周刊"
  },
  {
    "Content": "5G 技术的推广为物联网应用带来了新的机遇。智能家居、智慧城市等概念正在从科幻走向现实，改变着我们与世界的交互方式。",
    "Title": "5G 与物联网的融合发展",
    "Source": "通信世界"
  },
  {
    "Content": "随着人们健康意识的提高，运动健身产业迎来快速发展。从传统的健身房到新兴的在线健身平台，多样化的运动方式满足了不同人群的需求。",
    "Title": "运动健身产业的崛起",
    "Source": "健康生活"
  },
  {
    "Content": "短视频平台的兴起改变了内容消费模式。用户通过简短的视频片段获取信息和娱乐，这种碎片化的传播方式对传统媒体产生了深远影响。",
    "Title": "短视频时代的内容变革",
    "Source": "媒体观察"
  }
]
```

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

PlainResult

Code

string

状态码

NoData

Data

object

业务数据

TaskId

string

任务唯一 ID

3f7045e099474ba28ceca1b4eb6d6e21

TaskName

string

任务名称

任务名称

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

Success

boolean

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "NoData",
  "Data": {
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "TaskName": "任务名称"
  },
  "HttpStatusCode": 200,
  "Message": "success",
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

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/SubmitCustomSourceTopicAnalysis#workbench-doc-change-demo)。
