# 特惠语音转写资源包购买及使用方法

本文 介绍如何购买特惠ASR资源包，以及配置生效的方法。

## 购买特惠语音转写资源包

[购买](https://common-buy.aliyun.com/?commodityCode=sfm_TingwuDiscountASR_dp_cn&accounttraceid=2671ba29617e48c19d2e3dd1d1b797f2xwsz)通义听悟 Agent 特价 ASR 资源包。

**说明**

-   购买后可用于抵扣汽车销售服务洞察、购车客户画像、通用服务洞察、智能纪要四个Agent的语音转写时长（注，无法抵扣工业语音指令的转写次数）。
-   资源包有效期时长为三个月，不支持退款。
-   该转写模型为Paraformer-v2和Paraformer-realtime-v2的定制版模型，可支持热词，无法进行效果调优，建议先购买350小时进行充分效果验证后，再购买更多时长。
-   离线转写通过Batch方式，24小时内返回结果。
-   该资源包的转写价格优惠，详情如下：

**资源包规格**

**资源包价格**

**单价**

350 小时

210 元

0.60000 元/小时

225,000 小时

12,600 元

0.05600 元/小时

360,000 小时

19,800 元

0.05500 元/小时

540,000 小时

28,000 元

0.05185 元/小时

750,000 小时

35,600 元

0.04747 元/小时

1,500,000 小时

52,800 元

0.03520 元/小时

2,000,000 小时

79,800 元

0.03990 元/小时

4,500,000 小时

15,1200 元

0.03360 元/小时

9,000,000 小时

25,2000 元

0.02800 元/小时

## 准备工作

[开通](https://common-buy.aliyun.com/?commodityCode=sfm_TingWuAgent_public_cn)通义听悟 Agent 服务。

**说明**开通后即可使用阿里云百炼平台全系通义听悟 Agent 服务。

## 特惠语音转写资源包使用方法

1.  购买完成后，资源包有效期内，可在[汽车销售服务洞察](https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.4ab7695bvInrXr&tab=app#/app/app-market/tingwu/tingwu-automotive-service-insights)、[购车客户画像](https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.4ab7695bvInrXr&tab=app#/app/app-market/tingwu/tingwu-automotive-customer-profile)、[通用服务洞察](https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.4ab7695bvInrXr&tab=app#/app/app-market/tingwu/tingwu-service-insights)、[智能纪要](https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.4ab7695bvInrXr&tab=app#/app/app-market/tingwu/tingwu-meeting-summary)四个Agent的控制台中，选择项目使用该转写模型。
2.  需要使用特惠转写的项目，进入“项目详情”，并勾选“使用特惠转写资源包”。如对接该项目的业务不使用特惠转写资源包，则不需要勾选。在**转写模型**下拉框中选择**fun-asr（中英）**，并勾选**使用特惠转写资源包**。
3.  在项目详情页的控制台顶部工具栏中，可看到 **调试配置** 和 **API 接入** 两个页签，以及右侧的 **版本管理**、**测试记录** 和 **发布** 按钮。单击 **发布** 按钮完成发布后，切换到 **API 接入** 页签即可查看并复制对应的接入代码。
4.  当资源包余量为零或过期失效后，将自动使“转写模型”选择的模型进行ASR，同时费用恢复到0.6元/小时，同时离线转写的耗时恢复到准实时。
5.  若需要再次使用特惠转写模型，需再次[购买](https://common-buy.aliyun.com/?commodityCode=sfm_TingwuDiscountASR_dp_cn&accounttraceid=2671ba29617e48c19d2e3dd1d1b797f2xwsz)资源包。
