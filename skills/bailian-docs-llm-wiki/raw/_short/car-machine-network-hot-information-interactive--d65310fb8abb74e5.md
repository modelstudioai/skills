# 车机网络热点信息互动问答计费文档

本文档主要介绍全妙产品矩阵里的AI Agent -- 车机网络热点互动问答 的计费方案。

<a id="计费说明"></a>

<a id="88ef207356m5a"></a>

## 计费说明

计费方式：**开通型后付费（按量付费）**。开通服务本身不产生费用，仅在实际调用API时根据用量计费。

-   获取播报单：按调用版本数后付费；
-   个性化内容推荐 ：按调用的次数后付费；
-   新闻问答互动：按提问的次数后付费。

<a id="计费详情"></a>

<a id="1e407d7132pxq"></a>

## 计费详情

<table><thead><tr><th><p><strong>计费项</strong></p></th><th><p><strong>计费</strong></p></th><th><p><strong>功能及计费说明</strong></p></th><th><p><strong>接口地址</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>获取播报单及聚合摘要的写作风格化</p></td><td rowspan="2"><p>1元/次</p></td><td><ul><li><p>功能说明：</p><ul><li><p>获取播报单包含官方聚合新闻播报单和自定义播报单，自定义播报单支持用户根据频道、自定义热度、话题数量等生成专属播报单。</p></li><li><p>根据客户诉求，从热榜里抽取符合其诉求的新闻信息并结构化展现。</p></li></ul></li><li><p>计费说明：</p><ul><li><p>系统以每天3次的频率，在早上7点、 中午13点和晚上19点根据当下最新的实时新闻聚类，每天产出3版带图的新闻播报单。同个版本调多次，只收费1元。</p></li><li><p>如果改过频道、热点条数或者风格，导致版本会改变，则调取时会重新收取1元。</p></li></ul></li></ul></td><td><ul><li><p><a href="api-quanmiaolightapp-2024-08-01-hotnewsrecommend-a769ef75d82638e6.md">新闻热点推荐</a></p></li><li><p><a href="api-aimiaobi-2023-08-01-gethottopicbroadcast-8bd753b9c4dd8b39.md">查询完整播报单（热榜）</a></p></li></ul></td></tr><tr><td><ul><li><p>功能说明：</p><ul><li><p>用户可以根据需求，自定义播报单的输出风格，以满足个性化体验。</p></li></ul></li></ul></td><td><p><a href="api-quanmiaolightapp-2024-08-01-runhottopicsumma-f768f0c808d06be2.md">播报单热点自定义摘要生成</a></p></td></tr><tr><td><p>个性化内容推荐</p></td><td><p>0.009元/次</p></td><td><ul><li><p>功能说明：</p><ul><li><p>通过主动发问等方式收集用户的偏好并结合当日榜单内容给用户推荐感兴趣的个性化内容。</p></li></ul></li><li><p>计费说明</p><ul><li><p>每推荐一次收费0.009元。</p></li></ul></li></ul></td><td><p>如需要测试个性化推荐效果，请加 钉钉群（群号：101930016606） ，我们会以离线形式支持您进行测试。</p></td></tr><tr><td><p>新闻问答互动</p></td><td><p>0.018元/次</p></td><td><ul><li><p>功能说明：</p><ul><li><p>支持基于生成的播报单内容进行问答；支持联网搜索问答；并支持答案配图等能力。</p></li></ul></li><li><p>计费说明：</p><ul><li><p>用户提问收费0.018元/次。</p></li></ul></li></ul></td><td><ul><li><p><a href="api-quanmiaolightapp-2024-08-01-runhottopicchat-f7b74f0dfe8703b5.md">RunHotTopicChat - 播报单（热榜）问答</a></p></li></ul></td></tr></tbody></table>

若只需用【车机网络热点信息互动问答】agent的第一步 -- 获取播报单及聚合摘要的写作风格化，开通【新闻榜单订阅】即可（commonbuy地址：[新闻榜单订阅](https://common-buy.aliyun.com/?commodityCode=sfm_newshotlist_public_cn)）；如也要使用个性化推荐及新闻互动问答能力，需同时开通商品【全妙智能检索生成应用后付费API】（commonbuy地址：[全妙智能检索生成应用后付费API](https://common-buy.aliyun.com/?commodityCode=sfm_quanmiaoAPI_public_cn)）。

此外您还可以通过MCP server的形式使用此agent，对应地址为 [全妙网络热点信息播报MCP Server](https://bailian.console.aliyun.com/?spm=5176.29619931.J__Z58Z6CX7MY__Ll8p1ZOR.1.5f3c521cV95qKK&tab=mcp#/mcp-market/detail/quanmiao-hotnews)

<a id="账单地址"></a>

<a id="5002613c90d66"></a>

## 账单地址

账单查询地址：[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail?spm=a2c4g.11186623.0.0.619355efACwmfT)。

<a id="产品地址"></a>

<a id="7b5539e694r56"></a>

## 产品地址

可点击[产品地址](https://bailian.console.aliyun.com/?spm=5176.29619931.J__Z58Z6CX7MY__Ll8p1ZOR.1.74cd521c43xzda#/app/app-market/quanmiao/news-broadcast)进行产品体验。

<a id="相关文档"></a>

<a id="03b3d4a1e8bu6"></a>

## 相关文档

[车机网络热点信息互动问答接口文档](api-quanmiaolightapp-2024-08-01-dir-car-machine--5ac049dfb43b2428.md)
