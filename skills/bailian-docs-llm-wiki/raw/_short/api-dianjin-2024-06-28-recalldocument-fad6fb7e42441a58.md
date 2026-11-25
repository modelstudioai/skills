# RecallDocument - 文档召回

文档召回，可根据文本从文档库中召回文档块。并可设置召回文档块数量、也可根据元信息条件进行过滤，同时可选择是否进行文档块的补全。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

**前提条件**

-   已开通阿里云百炼服务和通义点金服务。
-   获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/DianJin/2024-06-28/RecallDocument)

<a id="授权信息"></a>

<a id="api-detail-32"></a>

## 授权信息

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>dianjin:RecallDocument</td><td>none</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{workspaceId}/api/library/recallDocument HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td>workspaceId</td><td>string</td><td>是</td><td><div><p>路径参数，业务空间 id。</p></div></td><td>llm-xxxxx</td></tr><tr><td>body</td><td>object</td><td>否</td><td><div><p>请求体参数。</p></div></td><td></td></tr><tr><td>filters</td><td>array&lt;object&gt;</td><td>否</td><td><div><p>元信息过滤条件</p></div></td><td></td></tr><tr><td>filter</td><td>object</td><td>否</td><td><div><p>过滤</p></div></td><td></td></tr><tr><td>and</td><td>array&lt;object&gt;</td><td>否</td><td><div><p>and 表达式，用于筛选文档/文档块</p></div></td><td></td></tr><tr><td>and</td><td>object</td><td>否</td><td><div><p>and 表达式</p></div></td><td></td></tr><tr><td>boost</td><td>float</td><td>否</td><td><div><p>关键词权重</p></div></td><td>20</td></tr><tr><td>key</td><td>string</td><td>否</td><td><div><p>文档库中，元信息的 key</p></div></td><td>docType</td></tr><tr><td>operator</td><td>string</td><td>否</td><td><div><p>文档库元信息 key 存储的 value 和您输入的 value 之间的关系</p><ul><li>eq: 文档库元信息 key 存储的 value = 您输入的 value</li><li>lte：文档库元信息 key 存储的 value &lt;= 您输入的 value</li><li>gte：文档库元信息 key 存储的 value &gt;= 您输入的 value</li><li>lt：文档库元信息 key 存储的 value &lt; 您输入的 value</li><li>gt：文档库元信息 key 存储的 value &gt; 您输入的 value</li><li>contains: 文档库元信息 key 存储的 value 列表 &quot;包含&quot; 您输入的 value</li></ul></div></td><td>contains</td></tr><tr><td>value</td><td>string</td><td>否</td><td><div><p>输入的元信息的值</p></div></td><td>策略报告</td></tr><tr><td>chunkType</td><td>string</td><td>否</td><td><div><p>文档块类型，用于筛选文档块，包括：Text、Graph、Table、FAQ</p></div></td><td>Text</td></tr><tr><td>docIdList</td><td>array</td><td>否</td><td><div><p>文档 id 列表，用于筛选文档/文档块</p></div></td><td></td></tr><tr><td>docIdList</td><td>string</td><td>否</td><td><div><p>文档 id</p></div></td><td>8372458573692819933</td></tr><tr><td>libraryId</td><td>string</td><td>是</td><td><div><p>文档库 id 用于筛选文档/文档块</p></div></td><td>sdbjhvs</td></tr><tr><td>or</td><td>array&lt;object&gt;</td><td>否</td><td><div><p>or 表达式，用于筛选文档/文档块</p></div></td><td></td></tr><tr><td>or</td><td>object</td><td>否</td><td><div><p>or 表达式</p></div></td><td></td></tr><tr><td>boost</td><td>float</td><td>否</td><td><div><p>关键词权重</p></div></td><td>30</td></tr><tr><td>key</td><td>string</td><td>否</td><td><div><p>文档库中，元信息的 key</p></div></td><td>researcher</td></tr><tr><td>operator</td><td>string</td><td>否</td><td><div><p>文档库元信息 key 存储的 value 和您输入的 value 之间的关系</p><ul><li>eq: 文档库元信息 key 存储的 value = 您输入的 value</li><li>lte：文档库元信息 key 存储的 value &lt;= 您输入的 value</li><li>gte：文档库元信息 key 存储的 value &gt;= 您输入的 value</li><li>lt：文档库元信息 key 存储的 value &lt; 您输入的 value</li><li>gt：文档库元信息 key 存储的 value &gt; 您输入的 value</li><li>contains: 文档库元信息 key 存储的 value 列表 &quot;包含&quot; 您输入的 value</li></ul></div></td><td>eq</td></tr><tr><td>value</td><td>string</td><td>否</td><td><div><p>输入的元信息的值</p></div></td><td>zhangsan</td></tr><tr><td>status</td><td>array</td><td>否</td><td><div><p>文档状态列表，用于筛选文档</p></div></td><td></td></tr><tr><td>statu</td><td>string</td><td>否</td><td><div><p>文档状态</p></div></td><td>WaitRefresh</td></tr><tr><td>query</td><td>string</td><td>是</td><td><div><p>文本</p></div></td><td>欧洲杯历史上有哪些球队因为球员的适应新文化而受益</td></tr><tr><td>rearrangement</td><td>boolean</td><td>否</td><td><div><p>是否开启父子文档块召回。</p><ul><li>父子文档块：文档解析过程中，一个完整的语义块，比如一个自然段，一个小节，可能会被切分成多个文档块，这取决于您配置的切分策略。开启父子文档召回之后，系统会尝试补全召回文档块所属的语义块，这样在构造 prompt 时，可以使得语料的语义更加完整，进而提升答案的完整性和准确性。</li></ul></div></td><td>false</td></tr><tr><td>topK</td><td>integer</td><td>否</td><td><div><p>为召回文档块的数量</p></div></td><td>10</td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | 返回数据 |  |
| cost | long | 耗时 | 0 |
| data | object | 响应数据 |  |
| chunkList | array<object> | chunk 列表 |  |
| chunkList | object | chunk |  |
| chunkId | string | 文档块 id | 823746762354 |
| chunkMeta | object | 文档块元数据 | {"a":"1"} |
| chunkOssUrl | string | 文档块 oss 地址 | [http://oss-xxx-hangzhou.com/xxx](http://oss-xxx-hangzhou.com/xxx) |
| chunkText | string | 文档块文本 | 测试文档块 |
| chunkType | string | 文档块类型 | text |
| docId | string | 文档 id | 839468263472 |
| fileType | string | 文档类型 | pdf |
| libraryId | string | 文档库 id | dscsbdsk |
| libraryName | string | 文档库名称 | 测试文档库 |
| nextChunkId | string | 后一个文档块 id | 982374872364 |
| pos | array<object> | 文档块位置 |  |
| po | object | 文档块位置坐标 |  |
| axisArray | array | 坐标 |  |
| axisArray | double | 坐标值 | 20.8 |
| page | integer | 页码 | 1 |
| textHighlightArea | array | 文本高亮区域，用于文本类型的文件高亮 |  |
| textHighlightArea | integer | 文本高亮区域数据 | 1 |
| preChunkId | string | 前一个文档块 id | 827364827364832 |
| score | float | 文档块分数 | 0.5 |
| title | string | 文档标题 | test |
| chunkPartList | array<object> | chunk part（版面识别结果）列表 |  |
| chunkPartList | object | chunk part（版面识别结果） |  |
| chunkId | string | 文档块 id | 98327482364 |
| chunkMeta | object | 文档块元数据 | {"a":"1"} |
| chunkOssUrl | string | 文档块 oss 地址 | [http://oss-xxx-hangzhou.com/xxx](http://oss-xxx-hangzhou.com/xxx) |
| chunkText | string | 文档块文本 | 测试文档块 |
| chunkType | string | 文档块类型 | text |
| docId | string | 文档 id | 92837482364 |
| fileType | string | 文档类型 | pdf |
| libraryId | string | 文档库 id | sjdhgjsd |
| libraryName | string | 文档库名称 | 测试文档库 |
| nextChunkId | string | 后一个文档块 id | 2387648263542 |
| pos | array<object> | 文档块位置 |  |
| po | object | 文档块位置数据 |  |
| axisArray | array | 坐标 |  |
| axisArray | double | 坐标数值 | 1 |
| page | integer | 页码 | 1 |
| textHighlightArea | array | 文本高亮区域，用于文本类型的文件高亮 |  |
| textHighlightArea | integer | 文本高亮区域位置数据 | 1 |
| preChunkId | string | 前一个文档块 id | 32874682764 |
| score | float | 文档块分数 | 0.5 |
| title | string | 文档标题 | 测试文档标题 |
| chunkTextList | array | chunk text 列表 |  |
| chunkTextList | string | 文档块 | 这是一段测试文档块 |
| documents | array<object> | 文档列表 |  |
| document | object | 文档信息 |  |
| docId | string | 文档 id | 92837482364 |
| documentMeta | object | 文档元数据 | {"a":"1"} |
| fileType | string | 文档类型 | pdf |
| gmtCreate | string | 创建时间 | 2024-01-01 00:00:00 |
| libraryId | string | 文档库 id | sjdhgjsd |
| title | string | 文档标题 | test |
| url | string | 文档链接 | [http://oss-xxx-hangzhou.com/test.pdf](http://oss-xxx-hangzhou.com/test.pdf) |
| embeddingElapsedMs | long | 向量计算耗时 | 100 |
| textChunkList | array<object> | 从文本索引召回的 chunk 列表 |  |
| textChunkList | object | 从文本索引召回的 chunk |  |
| chunkId | string | 文档块 id | 32874682364 |
| chunkMeta | object | 文档块元数据 | {"a":"1"} |
| chunkOssUrl | string | 文档块 oss 地址 | [http://oss-xxx-hangzhou.com/xxx](http://oss-xxx-hangzhou.com/xxx) |
| chunkText | string | 文档块文本 | 这是一段测试文档块 |
| chunkType | string | 文档块类型 | text |
| docId | string | 文档 id | 8372467263542 |
| fileType | string | 文档类型 | pdf |
| libraryId | string | 文档库 id | djsgfsjd |
| libraryName | string | 文档库名称 | 测试文档库 |
| nextChunkId | string | 后一个文档块 id | 23874682432 |
| pos | array<object> | 文档块位置 |  |
| po | object | 文档块位置 |  |
| axisArray | array | 坐标 |  |
| axisArray | double | 坐标值 | 10 |
| page | integer | 页码 | 1 |
| textHighlightArea | array | 文本高亮区域，用于文本类型的文件高亮 |  |
| textHighlightArea | integer | 文本高亮区域数据 | 1 |
| preChunkId | string | 前一个文档块 id | 89473868346 |
| score | float | 文档块分数 | 0.5 |
| title | string | 文档标题 | 测试文档标题 |
| textSearchElapsedMs | long | 文本搜索耗时 | 100 |
| totalElapsedMs | long | 总耗时 包括向量计算耗时、向量搜索耗时、文本搜索耗时等（取决于召回参数） | 400 |
| vectorChunkList | array<object> | 从向量索引召回的 chunk 列表 |  |
| vectorChunkList | object | 从向量索引召回的 chunk |  |
| chunkId | string | 文档块 id | 8723642345276 |
| chunkMeta | object | 文档块元数据 | {"a":"1"} |
| chunkOssUrl | string | 文档块 oss 地址 | [https://oss-xxxx-hangzhou.com/test.pdf](https://oss-xxxx-hangzhou.com/test.pdf) |
| chunkText | string | 文档块文本 | 这是一段测试文本 |
| chunkType | string | 文档块类型 | text |
| docId | string | 文档 id | 78326476235675372 |
| fileType | string | 文档类型 | pdf |
| libraryId | string | 文档库 id | djsgfsjd |
| libraryName | string | 文档库名称 | 测试文档库 |
| nextChunkId | string | 后一个文档块 id | 293846872343 |
| pos | array<object> | 文档块位置 |  |
| po | object | 文档块位置坐标 |  |
| axisArray | array | 坐标 |  |
| axisArray | double | 坐标值 | 48.8 |
| page | integer | 页码 | 1 |
| textHighlightArea | array | 文本高亮区域，用于文本类型的文件高亮 |  |
| textHighlightArea | integer | 文本高亮区域 | 10 |
| preChunkId | string | 前一个文档块 id | 873647326542 |
| score | float | 文档块分数 | 0.5 |
| title | string | 文档标题 | test |
| vectorSearchElapsedMs | long | 向量搜索耗时 | 100 |
| dataType | string | 数据类型 | null |
| errCode | string | 错误码 | 0 |
| message | string | 错误信息 | ok |
| requestId | string | 请求 id | 0bc13a9517168617617186457e401f |
| success | boolean | 是否成功 | true |
| time | string | 时间戳 | 2024-04-24 11:54:34 |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "cost": 0,
  "data": {
    "chunkList": [
      {
        "chunkId": 823746762354,
        "chunkMeta": {
          "a": 1
        },
        "chunkOssUrl": "http://oss-xxx-hangzhou.com/xxx",
        "chunkText": "测试文档块",
        "chunkType": "text",
        "docId": 839468263472,
        "fileType": "pdf",
        "libraryId": "dscsbdsk",
        "libraryName": "测试文档库",
        "nextChunkId": 982374872364,
        "pos": [
          {
            "axisArray": [
              20.8
            ],
            "page": 1,
            "textHighlightArea": [
              1
            ]
          }
        ],
        "preChunkId": 827364827364832,
        "score": 0.5,
        "title": "test"
      }
    ],
    "chunkPartList": [
      {
        "chunkId": 98327482364,
        "chunkMeta": {
          "a": 1
        },
        "chunkOssUrl": "http://oss-xxx-hangzhou.com/xxx\n",
        "chunkText": "测试文档块\n",
        "chunkType": "text",
        "docId": 92837482364,
        "fileType": "pdf",
        "libraryId": "sjdhgjsd",
        "libraryName": "测试文档库",
        "nextChunkId": 2387648263542,
        "pos": [
          {
            "axisArray": [
              1
            ],
            "page": 1,
            "textHighlightArea": [
              1
            ]
          }
        ],
        "preChunkId": 32874682764,
        "score": 0.5,
        "title": "测试文档标题"
      }
    ],
    "chunkTextList": [
      "这是一段测试文档块"
    ],
    "documents": [
      {
        "docId": 92837482364,
        "documentMeta": {
          "a": 1
        },
        "fileType": "pdf",
        "gmtCreate": "2024-01-01 00:00:00",
        "libraryId": "sjdhgjsd\n",
        "title": "test",
        "url": "http://oss-xxx-hangzhou.com/test.pdf"
      }
    ],
    "embeddingElapsedMs": 100,
    "textChunkList": [
      {
        "chunkId": 32874682364,
        "chunkMeta": {
          "a": 1
        },
        "chunkOssUrl": "http://oss-xxx-hangzhou.com/xxx\n",
        "chunkText": "这是一段测试文档块\n",
        "chunkType": "text",
        "docId": 8372467263542,
        "fileType": "pdf",
        "libraryId": "djsgfsjd",
        "libraryName": "测试文档库",
        "nextChunkId": 23874682432,
        "pos": [
          {
            "axisArray": [
              10
            ],
            "page": 1,
            "textHighlightArea": [
              1
            ]
          }
        ],
        "preChunkId": 89473868346,
        "score": 0.5,
        "title": "测试文档标题"
      }
    ],
    "textSearchElapsedMs": 100,
    "totalElapsedMs": 400,
    "vectorChunkList": [
      {
        "chunkId": 8723642345276,
        "chunkMeta": {
          "a": 1
        },
        "chunkOssUrl": "https://oss-xxxx-hangzhou.com/test.pdf",
        "chunkText": "这是一段测试文本",
        "chunkType": "text",
        "docId": 78326476235675380,
        "fileType": "pdf",
        "libraryId": "djsgfsjd",
        "libraryName": "测试文档库",
        "nextChunkId": 293846872343,
        "pos": [
          {
            "axisArray": [
              48.8
            ],
            "page": 1,
            "textHighlightArea": [
              10
            ]
          }
        ],
        "preChunkId": 873647326542,
        "score": 0.5,
        "title": "test"
      }
    ],
    "vectorSearchElapsedMs": 100
  },
  "dataType": null,
  "errCode": 0,
  "message": "ok",
  "requestId": "0bc13a9517168617617186457e401f",
  "success": true,
  "time": "2024-04-24 11:54:34"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/DianJin/2024-06-28/errorCode)查看更多错误码。
