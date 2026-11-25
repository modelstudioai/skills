# RunHotTopicChat - 播报单（热榜）问答

阿里云百炼轻应用-车机/内容平台新闻热榜互动-播报单（热榜）问答：可以对播报单、新闻、开放域内容问答。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

<a id="当前接口-runhottopicchat-说明"></a>

## 当前接口 RunHotTopicChat 说明

通过此接口，可以对播报单（热榜）、热榜新闻、开放域内容做问答，包括频道推荐、热点推荐、热点内容问答等。

欢迎前往[控制台](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/news-broadcast)体验。

**通过 SDK 方式调用 API，请可参考[控制台](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/news-broadcast)“API”页签下的 java、python 示例！** **通过 SDK 方式调用 API，请可参考[控制台](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/news-broadcast)“API”页签下的 java、python 示例！** **通过 SDK 方式调用 API，请可参考[控制台](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/news-broadcast)“API”页签下的 java、python 示例！**

<a id="新闻热榜互动全量-api-说明"></a>

## 新闻热榜互动全量 API 说明

<a id="api-明细"></a>

### API 明细

<a id="ai-妙笔-sdk-下-对应-alibabacloud-aimiaobi20230801"></a>

#### AI 妙笔 SDK 下：对应 alibabacloud-aimiaobi20230801

-   **GetHotTopicBroadcast** - 查询完整播报单（热榜） --常用
-   SubmitCustomHotTopicBroadcastJob - 提交自定义播报单任务
-   GetCustomHotTopicBroadcastJob - 获取自定义播报单任务结果

<a id="阿里云百炼全妙轻应用-sdk-下-对应-alibabacloud-quanmiaolightapp20240801"></a>

#### 阿里云百炼全妙轻应用 SDK 下：对应 alibabacloud-quanmiaolightapp20240801

-   RunHotTopicChat - 播报单（热榜）问答 --常用
-   RunHotTopicSummary - 播报单热点自定义摘要生成

<a id="场景说明"></a>

### 场景说明

<a id="场景-1-获取完整播报单-热榜-全量或者部分频道热点"></a>

#### 场景 1：获取完整播报单（热榜）全量或者部分频道热点：

-   GetHotTopicBroadcast：查询播报单

<a id="场景-2-针对播报单或通用领域问题做问答"></a>

#### 场景 2：针对播报单或通用领域问题做问答：

-   RunHotTopicChat：问答

<a id="场景-3-内置播报单-热榜-不满足要求-需要个性化定制-频道-个性化摘要等"></a>

#### 场景 3：内置播报单（热榜）不满足要求，需要个性化定制（频道、个性化摘要等）：

-   SubmitCustomHotTopicBroadcastJob：提交自定义播报单任务
-   GetCustomHotTopicBroadcastJob：轮训自定义播报单任务状态
-   GetHotTopicBroadcast：获取自定义播报单信息

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunHotTopicChat)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>quanmiaolightapp:RunHotTopicChat</td><td>none</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{workspaceId}/quanmiao/lightapp/runHotTopicChat HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td>workspaceId</td><td>string</td><td>是</td><td><div><p>阿里云百炼业务空间唯一标识：<a href="https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id">获取 workspaceId</a></p></div></td><td>llm-xx</td></tr><tr><td>modelId</td><td>string</td><td>否</td><td><div><p>数据模型 ID。默认：qwen-max-latest</p></div></td><td>qwen-max-latest</td></tr><tr><td>modelCustomPromptTemplate</td><td>string</td><td>否</td><td><div><p>prompt 模版</p></div></td><td>xx</td></tr><tr><td>generateOptions</td><td>array</td><td>否</td><td><div><p>生成模式列表：默认 textChatGenerate</p></div></td><td></td></tr><tr><td></td><td>string</td><td>否</td><td><div><p>生成模式：summaryChatGenerate、newsChatGenerate 和控制台第三步两个选项对应，可以直接使用，其他场景可以按需要组合：</p><ul><li>能力组合：内置好的，原子能力+搜索源的组合<ul><li>summaryChatGenerate：对应轻应用控制台“仅针对聚合新闻播报单内已包含的信息进行回答”，包括 categoryRecommend, hotTopicSummarySearch, textChatGenerate</li><li>newsChatGenerate：对应轻应用控制台“允许针对新闻的原始素材和互联网开放域进行搜索后回答“，包括 hotTopicNewsSearch, internetSearch, textChatGenerate</li></ul></li><li>原子能力：<ul><li>categoryRecommend：频道热点推荐，比如“推荐下体育新闻”</li><li>textChatGenerate：问答，仅次选项时，必须明确指定源 internetSearch、hotTopicSummarySearch、hotTopicNewsSearch，比如“xxx 事件哪天发生的”</li><li>queryRecommend：开启 query 推荐，单独结构返回</li></ul></li><li>搜索源：<ul><li>hotTopicSummarySearch：热榜摘要搜索源</li><li>hotTopicNewsSearch：热榜新闻详情搜索源</li><li>internetSearch：互联网通用领域搜索源</li></ul></li></ul></div></td><td>newsChatGenerate</td></tr><tr><td>taskId</td><td>string</td><td>否</td><td><div><p>对话任务唯一标识：多轮时，这个值保持不变</p></div></td><td>a3d1c2ac-f086-4a21-9069-f5631542f5a2</td></tr><tr><td>originalSessionId</td><td>string</td><td>否</td><td><div><p>原始会话唯一标识：重试场景</p></div></td><td>a3d1c2ac-f086-4a21-9069-f5631542f5ax</td></tr><tr><td>prompt</td><td>string</td><td>否</td><td><div><p>用户问题</p></div></td><td>帮我播报体育热点</td></tr><tr><td>hotTopicVersion</td><td>string</td><td>否</td><td><div><p>热榜版本</p></div></td><td>2024-09-13_12</td></tr><tr><td>category</td><td>string</td><td>否</td><td><div><p>热榜频道</p></div></td><td>体育</td></tr><tr><td>hotTopics</td><td>array</td><td>否</td><td><div><p>热点名称列表</p></div></td><td></td></tr><tr><td></td><td>string</td><td>否</td><td><div><p>热点标题名称</p></div></td><td>xxx</td></tr><tr><td>imageCount</td><td>integer</td><td>否</td><td><div><p>配图张数：不一定都有图，取值[1-3]</p></div></td><td>1</td></tr><tr><td>stepForBroadcastContentConfig</td><td>object</td><td>否</td><td><div><p>新闻播报内容配置：仅 Saas 用，Paas 调用建议走 hotTopicVersion</p></div></td><td></td></tr><tr><td>categories</td><td>array</td><td>否</td><td><div><p>选择的频道列表</p></div></td><td></td></tr><tr><td></td><td>string</td><td>否</td><td><div><p>频道</p></div></td><td>体育</td></tr><tr><td>customHotValueWeights</td><td>array&lt;object&gt;</td><td>否</td><td><div><p>热度计算维度，不传，则走默认</p></div></td><td></td></tr><tr><td></td><td>object</td><td>否</td><td><div><p>热度计算维度列表</p></div></td><td></td></tr><tr><td>dimension</td><td>string</td><td>否</td><td><div><p>权重维度唯一标识：</p><ul><li>views(&quot;阅读量&quot;)</li><li>comments(&quot;发表观点量&quot;)</li><li>ups(&quot;点赞数&quot;)</li><li>downs(&quot;点踩数&quot;)</li><li>publishTime(&quot;发布时间&quot;)</li></ul></div></td><td>comments</td></tr><tr><td>weight</td><td>integer</td><td>否</td><td><div><p>权重，0-10 之间</p></div></td><td>1</td></tr><tr><td>topicCount</td><td>integer</td><td>否</td><td><div><p>话题数量</p></div></td><td>20</td></tr><tr><td>messages</td><td>array&lt;object&gt;</td><td>否</td><td><div><p>上下文</p></div></td><td></td></tr><tr><td></td><td>object</td><td>否</td><td><div><p>角色：user、assistant、system</p></div></td><td></td></tr><tr><td>role</td><td>string</td><td>否</td><td><div><p>内容</p></div></td><td>user</td></tr><tr><td>content</td><td>string</td><td>否</td><td><div><p>发生时间</p></div></td><td>xxx</td></tr><tr><td>createTime</td><td>string</td><td>否</td><td><div><p>时间</p></div></td><td>2024-12-10 18:51:29</td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th>名称</th><th>类型</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td></td><td>object</td><td><div><p>Schema of Response</p></div></td><td></td></tr><tr><td>header</td><td>object</td><td><div><p>消息头</p></div></td><td></td></tr><tr><td>errorCode</td><td>string</td><td><div><p>错误码 code</p></div></td><td>InvalidParam</td></tr><tr><td>errorMessage</td><td>string</td><td><div><p>错误描述</p></div></td><td>xx</td></tr><tr><td>event</td><td>string</td><td><div><p>事件</p></div></td><td>task-finished</td></tr><tr><td>eventInfo</td><td>string</td><td><div><p>事件描述信息</p></div></td><td>xx</td></tr><tr><td>sessionId</td><td>string</td><td><div><p>会话唯一标识</p></div></td><td>xxx</td></tr><tr><td>taskId</td><td>string</td><td><div><p>任务唯一标识</p></div></td><td>d3be9981-ca2d-4e17-bf31-1c0a628e9f99</td></tr><tr><td>traceId</td><td>string</td><td><div><p>全链路唯一标识</p></div></td><td>2150451a17191950923411783e2927</td></tr><tr><td>payload</td><td>object</td><td><div><p>消息体</p></div></td><td></td></tr><tr><td>output</td><td>object</td><td><div><p>输出结果</p></div></td><td></td></tr><tr><td>articles</td><td>array&lt;object&gt;</td><td><div><p>参照内容列表</p></div></td><td></td></tr><tr><td>articles</td><td>object</td><td><div><p>内容列表</p></div></td><td></td></tr><tr><td>content</td><td>string</td><td><div><p>正文</p></div></td><td>xxx</td></tr><tr><td>pubTime</td><td>string</td><td><div><p>发布时间</p></div></td><td>2024-09-22 16:45:06</td></tr><tr><td>score</td><td>double</td><td><div><p>相关度</p></div></td><td>0.8</td></tr><tr><td>searchSourceName</td><td>string</td><td><div><p>文章来源名称</p></div></td><td>互联网</td></tr><tr><td>select</td><td>boolean</td><td><div><p>是否参照</p></div></td><td>true</td></tr><tr><td>summary</td><td>string</td><td><div><p>摘要</p></div></td><td>xx</td></tr><tr><td>title</td><td>string</td><td><div><p>标题</p></div></td><td>test</td></tr><tr><td>url</td><td>string</td><td><div><p>链接</p></div></td><td>http://xxx</td></tr><tr><td>hotTopicSummaries</td><td>array&lt;object&gt;</td><td><div><p>热点列表</p></div></td><td></td></tr><tr><td>hotTopicSummaries</td><td>object</td><td><div><p>热点</p></div></td><td></td></tr><tr><td>customHotValue</td><td>double</td><td><div><p>自定义热度值</p></div></td><td>100000</td></tr><tr><td>hotTopic</td><td>string</td><td><div><p>热点话题名称</p></div></td><td>xx</td></tr><tr><td>hotTopicVersion</td><td>string</td><td><div><p>热点话题摘要版本</p></div></td><td>2024-09-13_08</td></tr><tr><td>hotValue</td><td>double</td><td><div><p>热度值</p></div></td><td>100000</td></tr><tr><td>textSummary</td><td>string</td><td><div><p>热点话题文本摘要</p></div></td><td>xxx</td></tr><tr><td>customTextSummary</td><td>string</td><td><div><p>自定义热点话题文本摘要</p></div></td><td>xxx</td></tr><tr><td>news</td><td>array&lt;object&gt;</td><td><div><p>新闻列表</p></div></td><td></td></tr><tr><td>news</td><td>object</td><td><div><p>新闻</p></div></td><td></td></tr><tr><td>title</td><td>string</td><td><div><p>标题</p></div></td><td>xxx</td></tr><tr><td>url</td><td>string</td><td><div><p>url</p></div></td><td>http://xxx</td></tr><tr><td>images</td><td>array&lt;object&gt;</td><td><div><p>图片列表</p></div></td><td></td></tr><tr><td>images</td><td>object</td><td><div><p>图片</p></div></td><td></td></tr><tr><td>url</td><td>string</td><td><div><p>图片</p></div></td><td><a href="http://www.example.com/xxx.png">http://www.example.com/xxx.png</a></td></tr><tr><td>url</td><td>string</td><td><div><p>热点话题的 URL</p></div></td><td><a href="http://www.example.com/xxx.html">http://www.example.com/xxx.html</a></td></tr><tr><td>pubTime</td><td>string</td><td><div><p>热点话题发布时间</p></div></td><td>2025-05-20 12:00:00</td></tr><tr><td>multimodalMedias</td><td>array&lt;object&gt;</td><td><div><p>配图</p></div></td><td></td></tr><tr><td>multimodalMedias</td><td>object</td><td><div><p>配图</p></div></td><td></td></tr><tr><td>fileUrl</td><td>string</td><td><div><p>链接</p></div></td><td>http://xxxx</td></tr><tr><td>mediaType</td><td>string</td><td><div><p>类型：</p><ul><li>image：图片</li></ul></div></td><td>image</td></tr><tr><td>sortScore</td><td>double</td><td><div><p>相关度</p></div></td><td>0.8</td></tr><tr><td>recommendQueries</td><td>array</td><td><div><p>推荐 query 列表</p></div></td><td></td></tr><tr><td>recommendQueries</td><td>string</td><td><div><p>推荐 query</p></div></td><td>关于xx你有什么看法？</td></tr><tr><td>searchQuery</td><td>string</td><td><div><p>改写后 query</p></div></td><td>xxx</td></tr><tr><td>text</td><td>string</td><td><div><p>生成正文：答案等</p></div></td><td>xx</td></tr><tr><td>category</td><td>string</td><td><div><p>新闻播报场景的领域识别（时政、社会、国际等频道识别）</p></div></td><td>国际</td></tr><tr><td>keyword</td><td>string</td><td><div><p>新闻播报场景的关键字识别</p></div></td><td>AI</td></tr><tr><td>location</td><td>string</td><td><div><p>新闻播报场景的地点名识别</p></div></td><td>杭州</td></tr><tr><td>usage</td><td>object</td><td><div><p>token 消耗</p></div></td><td></td></tr><tr><td>inputTokens</td><td>long</td><td><div><p>输入 token</p></div></td><td>100</td></tr><tr><td>outputTokens</td><td>long</td><td><div><p>输出 token</p></div></td><td>100</td></tr><tr><td>totalTokens</td><td>long</td><td><div><p>总 token</p></div></td><td>200</td></tr><tr><td>requestId</td><td>string</td><td><div><p>请求唯一标识</p></div></td><td>04DA1A52-4E51-56CB-BA64-FDDA0B53BAE8</td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "header": {
    "errorCode": "InvalidParam",
    "errorMessage": "xx",
    "event": "task-finished",
    "eventInfo": "xx",
    "sessionId": "xxx",
    "taskId": "d3be9981-ca2d-4e17-bf31-1c0a628e9f99",
    "traceId": "2150451a17191950923411783e2927"
  },
  "payload": {
    "output": {
      "articles": [
        {
          "content": "xxx",
          "pubTime": "2024-09-22 16:45:06",
          "score": 0.8,
          "searchSourceName": "互联网",
          "select": true,
          "summary": "xx",
          "title": "test",
          "url": "http://xxx"
        }
      ],
      "hotTopicSummaries": [
        {
          "customHotValue": 100000,
          "hotTopic": "xx",
          "hotTopicVersion": "2024-09-13_08",
          "hotValue": 100000,
          "textSummary": "xxx",
          "customTextSummary": "xxx",
          "news": [
            {
              "title": "xxx",
              "url": "http://xxx"
            }
          ],
          "images": [
            {
              "url": "http://www.example.com/xxx.png"
            }
          ],
          "url": "http://www.example.com/xxx.html",
          "pubTime": "2025-05-20 12:00:00"
        }
      ],
      "multimodalMedias": [
        {
          "fileUrl": "http://xxxx",
          "mediaType": "image",
          "sortScore": 0.8
        }
      ],
      "recommendQueries": [
        "关于xx你有什么看法？"
      ],
      "searchQuery": "xxx",
      "text": "xx",
      "category": "国际",
      "keyword": "AI",
      "location": "杭州"
    },
    "usage": {
      "inputTokens": 100,
      "outputTokens": 100,
      "totalTokens": 200
    }
  },
  "requestId": "04DA1A52-4E51-56CB-BA64-FDDA0B53BAE8"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 | 描述 |
| --- | --- | --- | --- |
| 403 | NoPermission | You are not authorized to perform this action , Please check the assignment of the workspaceId. | 请检查workspaceId的赋值 |

访问[错误中心](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

| 变更时间 | 变更内容概要 | 操作 |
| --- | --- | --- |

暂无变更历史
