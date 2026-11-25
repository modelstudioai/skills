# 三方搜索API模板

本文档提供了妙搜在接入三方企业搜索服务时所遵循的API规范。

<a id="请求规范"></a>

<a id="97103fcedcnbl"></a>

## 请求规范

<a id="端点与方法"></a>

<a id="endpoint-and-method"></a>

### 端点与方法

-   **协议：**HTTP(S)
    
-   **方法：**
    -   POST

<a id="请求头"></a>

<a id="3e5a9381d88of"></a>

### 请求头

-   Content-Type: application/json

<a id="鉴权"></a>

<a id="2500303a2dywg"></a>

### 鉴权

妙搜通过HTTP Header中的`Authorization`字段传递鉴权信息，支持以下格式：

-   `Authorization: Basic ${BasicToken}`
-   `Authorization: Bearer ${BasicToken}`

<a id="请求体"></a>

<a id="16477456a5x6u"></a>

## 请求体

请求体采用`application/json`格式，参数说明如下：

| 字段名 | 字段类型 | 是否必填 | 字段描述 | 字段示例值 |
| --- | --- | --- | --- | --- |
| query | String | 是 | 搜索关键字 | "杭州亚运会" |
| current | Integer | 否 | 当前页码<br><br>默认值：1 | 1 |
| size | Integer | 否 | 每页返回的数据条数<br><br>默认值：20 | 20 |
| includeContent | Boolean | 否 | 是否返回正文内容<br><br>默认值：true | true |

<a id="响应规范"></a>

<a id="58e58ba7b8l7z"></a>

## 响应规范

<a id="响应头"></a>

<a id="bc0e8aaa457ps"></a>

### 响应头

Content-Type: application/json

<a id="响应体"></a>

<a id="b7c73e5f40l6h"></a>

## 响应体

响应体采用`application/json`格式，结构如下：

| 字段名 | 字段类型 | 字段描述 | 字段示例值 |
| --- | --- | --- | --- |
| success | Boolean | 请求是否成功 | true |
| code | String | 错误码，请求失败时返回 | "PARAM\_ERROR" |
| message | String | 错误信息，请求失败时返回 | "参数错误" |
| data | List | 搜索结果数据列表，具体结构见下文 Article 对象 | \[\] |
| current | Integer | 当前页码 | 1 |
| size | Integer | 每页返回的数据条数 | 20 |
| total | Integer | 匹配到的总条数 | 100 |

<a id="article-对象"></a>

<a id="5b8c6039e9a1u"></a>

### Article 对象

响应体`data`字段是一个列表，列表中的每个元素都是一个 Article 对象，其结构如下：

| 字段名 | 字段类型 | 是否必填 | 字段描述 | 字段示例值 |
| --- | --- | --- | --- | --- |
| source | String | 是 | 文章来源 | "央视网" |
| title | String | 是 | 文章标题 | "杭州亚运会" |
| content | String | 是 | 文章正文。如果请求参数`includeContent`为 false，可返回空字符串。 | "无论是“大莲花”“小莲花”“大玉琮”“杭州伞”等场馆造型..." |
| url | String | 是 | 文章原文链接 | "[](http://news.cctv.com/)[http://news.cctv.com/](http://news.cctv.com/)..." |
| summary | String | 否 | 文章摘要。如果原始数据无此字段，可截取正文前N个字符作为摘要。 | "摘要内容..." |
| pubTime | String | 是 | 文章发布时间，格式：yyyy-MM-dd HH:mm:ss | "2023-01-01 12:01:01" |

<a id="示例"></a>

<a id="77c5e24661a14"></a>

## 示例

<a id="请求"></a>

<a id="2fee2795e2sfz"></a>

### 请求

<a id="code-block"></a>

```json
curl -X POST --location '{{url}}' \
-H 'Authorization: basic {{BasicToken}}' \
-H 'Content-Type: application/json' \
-d '{
      "query": "杭州亚运会"
    }'
```

<a id="响应"></a>

<a id="564464c22doka"></a>

### 响应

<a id="code-block-2"></a>

```json
{
  "success": true,
  "code": "",
  "message": "",
  "data": [{
    "source": "央视网",
    "title": "杭州亚运会",
    "content": "无论是“大莲花”“小莲花”“大玉琮”“杭州伞”等场馆造型",
    "url": "http://news.cctv.com/2023/08/29/ARTIZeHbELfOWLgviHk1IxGb230829.shtml",
    "summary": "摘要",
    "pubTime": "2023-01-01 12:01:01"
  }],
  "current": 1,
  "size": 20,
  "total": 100
}
```
