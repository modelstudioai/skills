# ListGeneratedContents - 获取文档列表

获取文档列表：用来查询妙笔中创作的文章历史列表。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListGeneratedContents)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListGeneratedContents)

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

aimiaobi:ListGeneratedContents

list

\*全部资源

`*`

无

无

## 请求参数

名称

类型

必填

描述

示例值

AgentKey

string

是

业务空间唯一标识： [AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)

xxxxx\_p\_efm

TaskId

string

否

任务唯一标识

**说明** TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。

task-03d46184ee7d8749

StartTime

string

否

开始时间

2024-01-04 11:46:07

EndTime

string

否

结束时间

2024-01-04 11:46:07

Title

string

否

标题内容

杭州亚运会

Query

string

否

搜索关键词：支持标题和正文模糊搜索

检索Query

ContentDomain

string

否

内容领域（创作类型的分类）

-   media: 传媒写作
-   government: 政府公文写作
-   office：办公写作
-   market：营销写作
-   custom: 自定义写作
-   commentGenerate: 观点生成

枚举值：

-   market：营销写作。
-   government：政务。
-   custom：自定义写作。
-   media：传媒。
-   office：办公写作。
-   commentGenerate：观点生成。

media

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

DataType

string

否

数据类型筛选

-   plainText：纯文本
-   richText：富文本
-   html：网页
-   pdf：PDF
-   word：WORD
-   excel：excel
-   csv：CSV
-   image：图片
-   video：视频
-   audio：音频

plainText

## 返回参数

名称

类型

描述

示例值

object

响应结果

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

文档列表

Data

object

文档

Content

string

正文：富文本

杭州亚运会

ContentDomain

string

内容领域（创作类型的分类）

-   media: 传媒写作
-   government: 政府公文写作
-   office：办公写作
-   market：营销写作
-   custom: 自定义写作
-   commentGenerate: 观点生成

media

ContentText

string

正文：纯文本

杭州亚运会

CreateTime

string

创建日期

2024-01-04 11:46:07

CreateUser

string

创建者

"123"

DeviceId

string

设备 ID

xxx

Id

long

文档唯一标识

10

KeywordList

array

关键词

KeywordList

string

关键词

观点

Keywords

string

关键词（string）

观点

Prompt

string

最后一次生成的提示词

创作xxx文章

TaskId

string

会话任务唯一标识

3f7045e099474ba28ceca1b4eb6d6e21

Title

string

标题

杭州亚运会

UpdateTime

string

更新日期

2024-01-04 11:46:07

UpdateUser

string

更新者

"1111"

Uuid

string

UUID 溯源唯一标识

xxx

FileKey

string

文件唯一标识

oss://default/oss-bucket-name/aimiaobi/2021/07/01/1625126400000/1.docx

FileAttr

object

文件属性

FileName

string

文件名称

homedepothp.txt

Width

integer

视频宽度

800

TmpUrl

string

视频文件临时访问 URL。1 小时过期

http://www.example.com/xxx.mp4

Height

integer

视频高度

500

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

每页记录数

10

Success

boolean

是否成功：true 成功，false 失败

true

Total

integer

总记录数

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
      "Content": "杭州亚运会",
      "ContentDomain": "media",
      "ContentText": "杭州亚运会",
      "CreateTime": "2024-01-04 11:46:07",
      "CreateUser": 123,
      "DeviceId": "xxx",
      "Id": 10,
      "KeywordList": [
        "观点"
      ],
      "Keywords": "观点",
      "Prompt": "创作xxx文章",
      "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
      "Title": "杭州亚运会",
      "UpdateTime": "2024-01-04 11:46:07",
      "UpdateUser": 1111,
      "Uuid": "xxx",
      "FileKey": "oss://default/oss-bucket-name/aimiaobi/2021/07/01/1625126400000/1.docx",
      "FileAttr": {
        "FileName": "homedepothp.txt",
        "Width": 800,
        "TmpUrl": "http://www.example.com/xxx.mp4",
        "Height": 500
      }
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

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
