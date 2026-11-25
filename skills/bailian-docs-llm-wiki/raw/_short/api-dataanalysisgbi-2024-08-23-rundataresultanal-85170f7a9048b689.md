# RunDataResultAnalysis - 执行结果分析

对结构化数据类型的执行结果进行分析、可视化信息生成。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/DataAnalysisGBI/2024-08-23/RunDataResultAnalysis)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>dataanalysisgbi:RunDataResultAnalysis</td><td>none</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /gbi/runDataResultAnalysis HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p>名称</p></th><th><p>类型</p></th><th><p>必填</p></th><th><p>描述</p></th><th><p>示例值</p></th></tr></thead><tbody><tr><td><p>workspaceId</p></td><td><p>string</p></td><td><p>是</p></td><td><p>当前请求所使用的阿里云百炼业务空间 id</p></td><td><p>llm-2v3934xtp49esw64</p></td></tr><tr><td><p>body</p></td><td><p>object</p></td><td><p>否</p></td><td><p>请求体参数</p></td><td></td></tr><tr><td><p>sqlData</p></td><td><p>object</p></td><td><p>否</p></td><td><p>sql 执行后所查询到的结构化数据内容，当前情况下此参数必传</p><a id="accordion-details"></a><section><p>Details</p><div><strong>sqlData 示例子</strong><p>{ &quot;column&quot;: [ &quot;month&quot;, &quot;total_received&quot; ], &quot;data&quot;: [ { &quot;month&quot;: &quot;2024-01&quot;, &quot;total_received&quot;: &quot;603&quot; }, { &quot;month&quot;: &quot;2024-02&quot;, &quot;total_received&quot;: &quot;749&quot; }, { &quot;month&quot;: &quot;2024-03&quot;, &quot;total_received&quot;: &quot;1311&quot; }, { &quot;month&quot;: &quot;2024-04&quot;, &quot;total_received&quot;: &quot;1003&quot; }, { &quot;month&quot;: &quot;2024-05&quot;, &quot;total_received&quot;: &quot;726&quot; }, { &quot;month&quot;: &quot;2024-06&quot;, &quot;total_received&quot;: &quot;791&quot; }, { &quot;month&quot;: &quot;2024-07&quot;, &quot;total_received&quot;: &quot;60&quot; } ] }</p></div></section></td><td></td></tr><tr><td><p>column</p></td><td><p>array</p></td><td><p>否</p></td><td><p>SQL 执行结果中，查询到的具体的字段名字列表</p></td><td></td></tr><tr><td><p>Column</p></td><td><p>string</p></td><td><p>否</p></td><td><p>SQL 执行结果中，查询到的具体的列名</p></td><td><p>month</p></td></tr><tr><td><p>data</p></td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><p>与 SQL 执行结果中的列名对应的结构化信息列表，详细结构可参考上方 sqlData 的示例</p></td><td></td></tr><tr><td><p>Data</p></td><td><p>object</p></td><td><p>否</p></td><td><p>与 SQL 执行结果中的列名对应的结构化信息，每一个代表着一行数据，其中的字段与表头列表应该为一一对应的关系</p></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><p>当前列名所对应的一条数据的具体内容</p></td><td><p>2024-01</p></td></tr><tr><td><p>analysisMode</p></td><td><p>string</p></td><td><p>否</p></td><td><p>当前希望执行的可视化类型，可以只生成图表或只生成文本分析</p><p>枚举值：</p><ul><li>all：生成图表和文字分析。</li><li>text：只生成文字分析。</li><li>chart：只生成图表。</li></ul></td><td><p>all</p></td></tr><tr><td><p>requestId</p></td><td><p>string</p></td><td><p>是</p></td><td><p>请求 id，这里的请求 id 为 RunSqlGeneration 接口中执行返回的 requestId，若传入未被 RunSqlGeneration 执行过的 requestId，执行会被拒绝</p></td><td><p>FF76AD3F-8B32-567E-819B-0D3738917006</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th>名称</th><th>类型</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td></td><td>object</td><td><div><p>Schema of Response</p></div></td><td></td></tr><tr><td>data</td><td>object</td><td><div><p>返回结果</p></div></td><td></td></tr><tr><td>errorMessage</td><td>string</td><td><div><p>错误信息</p></div></td><td>Access was denied, message: No such namespace namespaces/tech-scp-chain7.</td></tr><tr><td>event</td><td>string</td><td><div><p>事件类型</p></div><div><div>枚举值：</div><ul><li>result：结果事件。</li></ul></div></td><td>result</td></tr><tr><td>requestId</td><td>string</td><td><div><p>当前本次请求的 id</p></div></td><td>DA2578F7-88A5-5D6E-9305-33E724E97D60</td></tr><tr><td>visualization</td><td>object</td><td><div><p>用于可视化模块展示所需要的信息</p></div></td><td></td></tr><tr><td>data</td><td>object</td><td><div><p>数据列表</p></div></td><td></td></tr><tr><td>plotType</td><td>string</td><td><div><p>可视化图表展示的类型</p></div></td><td>bar</td></tr><tr><td>xAxis</td><td>array</td><td><div><p>具体某一个 x 轴所展示的字段列表</p></div></td><td></td></tr><tr><td>xAxis</td><td>string</td><td><div><p>具体某一个 x 轴所展示的字段</p></div></td><td>product_name</td></tr><tr><td>yAxis</td><td>array</td><td><div><p>具体某一个 y 轴所展示的字段列表</p></div></td><td></td></tr><tr><td>yAxis</td><td>string</td><td><div><p>具体某一个 y 轴所展示的字段</p></div></td><td>total_sales</td></tr><tr><td>text</td><td>string</td><td><div><p>对于 sql 执行结果的分析总结</p></div></td><td>查询结果显示，在过去两年中销量超过5的所有产品包括：2L大容量空气炸锅销售了109件，青春版运动手环销售了119件，2L大容量全自动豆浆机销售了106件，无线蓝牙耳机快充版销售了84件，2L大容量便携式榨汁机销售了136件，青春版智能手表销售了104件，挂壁式护眼台灯销售了102件，P30手机8+256G销售了83件，2L大容量电热水壶销售了84件，男士电动化妆刷套装销售了197件，旅行箱销售了82件，手链销售了101件，项链销售了84件，头饰发链销售了89件，腕表销售了98件，戒指销售了157件，真皮皮包销售了136件，风衣大衣销售了76件，运动旅行包销售了91件，丝巾销售了265件，1L迷你空气炸锅销售了85件，豪华款运动手环销售了132件，1L迷你全自动豆浆机销售了81件，豪华版无线蓝牙耳机（绿色）销售了122件，1L迷你便携式榨汁机销售了76件，豪华款智能手表销售了76件，粘贴式护眼台灯销售了109件，M60手机16+512G销售了109件，1L迷你电热水壶销售了63件，女士电动化妆刷套装销售了158件。</td></tr><tr><td>sql</td><td>string</td><td><div><p>当前对话生成的 SQL 语句</p></div></td><td>select p.product_id, p.product_name, sum(o.quantity) as total_sales from products p join orders o on p.product_id = o.product_id where o.order_date between '2022-10-22' and '2024-10-22' group by p.product_id, p.product_name having total_sales &gt; 5</td></tr><tr><td>rewrite</td><td>string</td><td><div><p>改写后的用户输入</p></div></td><td>过去两年中，销量超过5的产品有哪些</td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "data": {
    "errorMessage": "Access was denied, message: No such namespace namespaces/tech-scp-chain7.",
    "event": "result",
    "requestId": "DA2578F7-88A5-5D6E-9305-33E724E97D60",
    "visualization": {
      "data": {
        "plotType": "bar",
        "xAxis": [
          "product_name"
        ],
        "yAxis": [
          "total_sales"
        ]
      },
      "text": "查询结果显示，在过去两年中销量超过5的所有产品包括：2L大容量空气炸锅销售了109件，青春版运动手环销售了119件，2L大容量全自动豆浆机销售了106件，无线蓝牙耳机快充版销售了84件，2L大容量便携式榨汁机销售了136件，青春版智能手表销售了104件，挂壁式护眼台灯销售了102件，P30手机8+256G销售了83件，2L大容量电热水壶销售了84件，男士电动化妆刷套装销售了197件，旅行箱销售了82件，手链销售了101件，项链销售了84件，头饰发链销售了89件，腕表销售了98件，戒指销售了157件，真皮皮包销售了136件，风衣大衣销售了76件，运动旅行包销售了91件，丝巾销售了265件，1L迷你空气炸锅销售了85件，豪华款运动手环销售了132件，1L迷你全自动豆浆机销售了81件，豪华版无线蓝牙耳机（绿色）销售了122件，1L迷你便携式榨汁机销售了76件，豪华款智能手表销售了76件，粘贴式护眼台灯销售了109件，M60手机16+512G销售了109件，1L迷你电热水壶销售了63件，女士电动化妆刷套装销售了158件。"
    },
    "sql": "select p.product_id, p.product_name, sum(o.quantity) as total_sales from products p join orders o on p.product_id = o.product_id where o.order_date between '2022-10-22' and '2024-10-22' group by p.product_id, p.product_name having total_sales > 5",
    "rewrite": "过去两年中，销量超过5的产品有哪些"
  }
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 | 描述 |
| --- | --- | --- | --- |
| 401 | Internal.Error | Bad Request: Internal Error. | 内部错误，请联系客服人员排查 |
| 401 | NoAuth | Bad Request: Workspace.Illegal.Auth. | 当前所使用的账号无所指定业务空间的权限 |
| 401 | NoResourceAuth | Bad Request: Resource Auth Error. | 没有请求的资源的权限，请确保所请求的资源属于当前参数中的业务空间 |
| 401 | Invalid.RequestId | Bad Request: Invalid RequestId. | requestId错误或已过期 |

访问[错误中心](https://api.aliyun.com/document/DataAnalysisGBI/2024-08-23/errorCode)查看更多错误码。
