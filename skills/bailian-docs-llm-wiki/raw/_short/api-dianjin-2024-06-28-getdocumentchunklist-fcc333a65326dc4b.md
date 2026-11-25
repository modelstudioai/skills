# GetDocumentChunkList - 获取文档块列表

获取文档块列表，可根据查询条件过滤。

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

[调试](https://api.aliyun.com/api/DianJin/2024-06-28/GetDocumentChunkList)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>dianjin:GetDocumentChunkList</td><td>none</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{workspaceId}/api/library/getDocumentChunk HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| workspaceId | string | 是 | 路径参数，业务空间 id | llm-xxxxx |
| body | object | 否 | 请求体参数。 |  |
| chunkIdList | array | 否 | 文档块 id 列表 |  |
| chunkIdList | string | 否 | 文档块 id | 83648326438746 |
| docId | string | 是 | 文档 id | 182364872346 |
| libraryId | string | 是 | 文档库 id | dsjgfdjgfxxx |
| order | string | 否 | 排序方式 | desc |
| orderBy | string | 否 | 排序字段 | gmtCreate |
| page | integer | 否 | 页码 | 1 |
| pageSize | integer | 否 | 每页大小 | 10 |
| searchQuery | string | 否 | 搜索查询关键词 | test |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th>名称</th><th>类型</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td></td><td>object</td><td><div><p>ResultCode&lt;PageVO</p><div>&gt;</div></div></td><td></td></tr><tr><td>cost</td><td>long</td><td><div><p>耗时</p></div></td><td>null</td></tr><tr><td>data</td><td>object</td><td><div><p>响应数据</p></div></td><td></td></tr><tr><td>currentPage</td><td>long</td><td><div><p>当前页</p></div></td><td>1</td></tr><tr><td>pageSize</td><td>long</td><td><div><p>每页记录数</p></div></td><td>10</td></tr><tr><td>records</td><td>array&lt;object&gt;</td><td><div><p>记录</p></div></td><td></td></tr><tr><td>record</td><td>object</td><td></td><td></td></tr><tr><td>chunkId</td><td>string</td><td><div><p>文档块 id</p></div></td><td>28377468263482764</td></tr><tr><td>chunkMeta</td><td>object</td><td><div><p>文档块元数据</p></div></td><td>{&quot;a&quot;:&quot;1&quot;}</td></tr><tr><td>chunkOssUrl</td><td>string</td><td><div><p>文档块 oss 地址</p></div></td><td>oss-xxxx-hangzhou.com/test.pdf</td></tr><tr><td>chunkText</td><td>string</td><td><div><p>文档块文本</p></div></td><td>这是一段测试文本</td></tr><tr><td>chunkType</td><td>string</td><td><div><p>文档块类型</p></div><div><div>枚举值：</div><ul><li>faq：faq。</li><li>text：text。</li><li>graph：graph。</li><li>table：table。</li><li>structure：structure。</li></ul></div></td><td>text</td></tr><tr><td>docId</td><td>string</td><td><div><p>文档 id</p></div></td><td>8947387648356</td></tr><tr><td>fileType</td><td>string</td><td><div><p>文档类型</p></div></td><td>pdf</td></tr><tr><td>libraryId</td><td>string</td><td><div><p>文档库 id</p></div></td><td>jhsdvne</td></tr><tr><td>libraryName</td><td>string</td><td><div><p>文档库名称</p></div></td><td>测试文档库</td></tr><tr><td>nextChunkId</td><td>string</td><td><div><p>后一个文档块 id</p></div></td><td>947538465</td></tr><tr><td>pos</td><td>array&lt;object&gt;</td><td><div><p>文档块位置</p></div></td><td></td></tr><tr><td>po</td><td>object</td><td><div><p>版面的位置信息</p></div></td><td></td></tr><tr><td>axisArray</td><td>array</td><td><div><p>坐标</p></div></td><td></td></tr><tr><td>axisArray</td><td>double</td><td><div><p>坐标</p></div></td><td>394.3</td></tr><tr><td>page</td><td>integer</td><td><div><p>页码</p></div></td><td>1</td></tr><tr><td>textHighlightArea</td><td>array</td><td><div><p>文本高亮区域，用于文本类型的文件高亮</p></div></td><td></td></tr><tr><td>textHighlightArea</td><td>integer</td><td><div><p>文本高亮区域</p></div></td><td>38</td></tr><tr><td>preChunkId</td><td>string</td><td><div><p>前一个文档块 id</p></div></td><td>9848346548365</td></tr><tr><td>score</td><td>float</td><td><div><p>文档块分数</p></div></td><td>0.5</td></tr><tr><td>title</td><td>string</td><td><div><p>文档标题</p></div></td><td>test</td></tr><tr><td>totalPages</td><td>long</td><td><div><p>总页数</p></div></td><td>10</td></tr><tr><td>totalRecords</td><td>long</td><td><div><p>总记录数</p></div></td><td>100</td></tr><tr><td>dataType</td><td>string</td><td><div><p>数据类型</p></div></td><td>null</td></tr><tr><td>errCode</td><td>string</td><td><div><p>错误码</p></div></td><td>0</td></tr><tr><td>message</td><td>string</td><td><div><p>错误信息</p></div></td><td>ok</td></tr><tr><td>requestId</td><td>string</td><td><div><p>请求 id</p></div></td><td>2B8F6DC9-6FAF-576F-9095-CCD90FB2BDDF</td></tr><tr><td>success</td><td>boolean</td><td><div><p>是否成功</p></div></td><td>true</td></tr><tr><td>time</td><td>string</td><td><div><p>时间戳</p></div></td><td>2024-04-24 11:54:34</td></tr></tbody></table>

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
    "currentPage": 1,
    "pageSize": 10,
    "records": [
      {
        "chunkId": 28377468263482764,
        "chunkMeta": {
          "a": 1
        },
        "chunkOssUrl": "oss-xxxx-hangzhou.com/test.pdf",
        "chunkText": "这是一段测试文本",
        "chunkType": "text",
        "docId": 8947387648356,
        "fileType": "pdf",
        "libraryId": "jhsdvne",
        "libraryName": "测试文档库",
        "nextChunkId": 947538465,
        "pos": [
          {
            "axisArray": [
              394.3
            ],
            "page": 1,
            "textHighlightArea": [
              38
            ]
          }
        ],
        "preChunkId": 9848346548365,
        "score": 0.5,
        "title": "test"
      }
    ],
    "totalPages": 10,
    "totalRecords": 100
  },
  "dataType": null,
  "errCode": 0,
  "message": "ok",
  "requestId": "2B8F6DC9-6FAF-576F-9095-CCD90FB2BDDF",
  "success": true,
  "time": "2024-04-24 11:54:34"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/DianJin/2024-06-28/errorCode)查看更多错误码。
