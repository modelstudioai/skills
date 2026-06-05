# FetchParseDocumentLayoutTask - 获取排版任务结果

获取排版任务结果

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/FetchParseDocumentLayoutTask)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/FetchParseDocumentLayoutTask)

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

是

阿里云百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xxxx

TaskId

string

是

待排版内容

29ae0ba84c1c4cc694d0f4f1aead8005

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

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Success

boolean

调用是否成功。

true

Code

string

状态码

successful

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

successful

Data

object

业务数据

TaskStats

string

任务状态

PENDING-待执行、RUNNING-执行中、SUCCESSED-成功、SUSPENDED-暂停、FAILED-失败、CANCELLED-取消

LayoutResult

object

排版后的结构化内容

Elements

array<object>

返回元素数据

object

数组对象

Index

number

各个元素的索引顺序

1

Type

string

type 类型

支持的类型如下 HEADING("标题"), H1("一级标题"), H2("二级标题"), H3("三级标题"), H4("四级标题"), H5("五级标题"), H6("六级标题"), PARAGRAPH("段落"), SIGNATURE("落款"), FOOTNOTE("脚注"), TABLE("表格"), CODE\_BLOCK("代码块"), ATTACHMENT("附件"), BLOCKQUOTE("引用");

Content

string

内容

一、本月主要工作进展\\n

FormatContent

string

针对标题，去除标题数字标好后的内容

本月主要工作进展

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true,
  "Code": "successful",
  "HttpStatusCode": 200,
  "Message": "successful",
  "Data": {
    "TaskStats": "PENDING-待执行、RUNNING-执行中、SUCCESSED-成功、SUSPENDED-暂停、FAILED-失败、CANCELLED-取消",
    "LayoutResult": {
      "Elements": [
        {
          "Index": 1,
          "Type": "支持的类型如下\n    HEADING(\"标题\"),\n    H1(\"一级标题\"),\n    H2(\"二级标题\"),\n    H3(\"三级标题\"),\n    H4(\"四级标题\"),\n    H5(\"五级标题\"),\n    H6(\"六级标题\"),\n    PARAGRAPH(\"段落\"),\n    SIGNATURE(\"落款\"),\n    FOOTNOTE(\"脚注\"),\n    TABLE(\"表格\"),\n    CODE_BLOCK(\"代码块\"),\n    ATTACHMENT(\"附件\"),\n    BLOCKQUOTE(\"引用\");",
          "Content": "一、本月主要工作进展\\n",
          "FormatContent": "本月主要工作进展"
        }
      ]
    }
  }
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/FetchParseDocumentLayoutTask#workbench-doc-change-demo)。
