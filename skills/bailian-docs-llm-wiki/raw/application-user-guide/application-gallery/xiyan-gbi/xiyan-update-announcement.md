# 析言GBI更新公告

本文介绍了析言GBI的产品功能及其相应的文档变更记录。

## 2024年11月

**日期**

**功能模块**

**变更点**

**功能说明**

11月28日

权限管理

新增数据权限自设置功能

析言提供精细的数据访问权限控制，您可以精确控制用户能够查询哪些数据表、哪些列以及哪些特定值范围。这使得您能够灵活地管理数据访问权限，确保数据的安全性和合规性。具体配置方法请参考“[权限管理](raw/application-user-guide/application-gallery/xiyan-gbi/xiyan-gbi-permission-management.md)”文档。

11月28日

问答设置

新增SQL智能校验功能

析言提供 SQL 智能校验功能，可以自动检查问答过程中生成的 SQL 语句的语法正确性，并尝试修复错误的 SQL 语句，从而显著提高 SQL 执行的成功率。启用此功能后，如果初次生成的 SQL 未通过校验，系统会在首页步骤 4 展示详细的校验记录，帮助您了解问题所在。[首页](https://bailian.console.aliyun.com/xiyan?spm=a2c4g.11186623.0.0.6e316709xwHjvq#/home)步骤4才会显示**SQL智能校验记录**。

设置的执行次数越多，析言回答问题的响应时长越长，最多可执行3次。

## 2024年10月

**日期**

**功能模块**

**变更点**

**功能说明**

10月21日

计费

大幅下调析言GBI标准版的价格

-   **标准版TURBO**：原价格为15000元/月/RPM，现调整为299元/月，默认包含5 RPM（Request Per Minute，即5并发）。如果您需要提高RPM，请点击[购买](https://common-buy.aliyun.com/?&msctype=email&mscareaid=cn&mscsiteid=cn&mscmsgid=3800124102101018568&yunge_info=email___3800124102101018568&commodityCode=sfm_DataAnalysisGBI_public_cn)进入购买页面自行增购。
    
-   **标准版MIX**​​：原价格为37500元/月/RPM，现调整为499元/月，默认包含5 RPM（Request Per Minute，即5并发）。如果您需要提高RPM，请点击[购买](https://common-buy.aliyun.com/?&msctype=email&mscareaid=cn&mscsiteid=cn&mscmsgid=3800124102101018568&yunge_info=email___3800124102101018568&commodityCode=sfm_DataAnalysisGBI_public_cn)进入购买页面自行增购。
    

购买**标准版TURBO**或**标准版MIX**​​后，每月额外赠送500次免费调用。免费额度消耗完毕后，调用产生的费用将以后付费的方式从您的阿里云账户中扣除。（使用一条自然语言对析言GBI进行提问即产生一次调用，若在模型生成结果返回前中断请求，调用依然被消耗。）

您可以在[首页](https://bailian.console.aliyun.com/xiyan?spm=a2c4g.11186623.0.0.6e316709xwHjvq#/home)左下角点击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2805379271/p861924.png)查看已购买及赠送资源的消耗进度。

## 2024年8月

**日期**

**功能模块**

**变更点**

**功能说明**

8月29日

首页 > 数据文件

标准版MIX支持上传Excel数据文件

上传Excel数据文件后，可针对Excel进行提问，析言GBI会根据提问进行数据分析、绘制可视化图表。请点击[使用指南](raw/application-user-guide/application-gallery/xiyan-gbi/xiyan-gbi-user-guide.md)查看完整信息。

8月29日

首页 > 数据库

新增官方预置数据库及样例问题

当您在测试阶段，没有可用的数据库可关联时，可以直接使用官方预置的数据库进行测试。请点击[使用指南](raw/application-user-guide/application-gallery/xiyan-gbi/xiyan-gbi-user-guide.md)查看完整信息。

8月29日

首页

问答交互优化

支持结果重新生成，支持图表（柱状图、折线图、饼图）切换，分析结果可下载导出。请点击[使用指南](raw/application-user-guide/application-gallery/xiyan-gbi/xiyan-gbi-user-guide.md)查看完整信息。

## 2024年7月

**日期**

**功能模块**

**变更点**

**功能说明**

7月11日

数据表管理

新增：VPC访问数据库

“VPC访问数据库”功能使析言GBI可以连接阿里云VPC内的数据库（包括AnalyticDB PostgreSQL版、Hologres、MySQL、PostgreSQL），扩大了析言GBI可连接的数据库范围 。请点击[使用指南](raw/application-user-guide/application-gallery/xiyan-gbi/xiyan-gbi-user-guide.md)查看完整信息。
