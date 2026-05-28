# 电商零售推广文案写作计费

全妙产品矩阵包含4个SaaS产品妙笔/妙策/妙搜/妙读和若干个AI Agent（场景化能力），本文档主要介绍AI Agent中电商零售推广文案写作应用的计费。

## **计费说明**

调用API时，系统会根据您实际选取的大模型的输出、输出token总数做计量，并采用后付费模式向您收取费用。如对费用有疑问，可参考[计费项](https://help.aliyun.com/zh/model-studio/billing-for-model-studio)文档的公示价格。

**说明**

-   该产品在“效果调试”页面供您免费体验效果。
    
-   支持基模的扩容升级，以确保您业务的持续稳定运行，并满足日益增长的算力需求。如需进行扩容，请与我们联系或加入钉钉群咨询：群号 116015001424。
    

## **计费详情**

模型

输入价格

输出价格

千问-Max-Latest

¥0.0024/千tokens

¥0.0096/千tokens

千问-Max

¥0.0024/千tokens

¥0.0096/千tokens

千问-Plus-Latest

¥0.0008/千tokens

¥0.002/千tokens

千问-Plus

¥0.0008/千tokens

¥0.002/千tokens

千问Q-Plus-Latest

¥0.0016/千tokens

¥0.004/千tokens

DeepSeek-R1

¥0.002/千tokens

¥0.008/千tokens

## **账单地址**

账单查询地址：[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail?spm=a2c4g.11186623.0.0.619355efACwmfT)。

## **产品地址**

可点击[产品地址](https://bailian.console.aliyun.com/?spm=5176.21213303.J_v8LsmxMG6alneH-O7TCPa.3.5d382f3dPKUN9O&scm=20140722.S_card%40%40&tab=app#/app/app-market/quanmiao/market-write)进行产品体验。

## **相关文档**

[电商零售推广文案写作接口文档](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-dir-e-commerce-retail-promotion-copy-writing/)

## **常见问题**

-   #### **如果任务运行到中途失败了，怎么计费？**
    
    当任务运行到中途失败时，主要是看最后一个事件消息的event，如果是task-failed，就不计费；其他运行成功部分计费，失败部分不计费。在产品客户端页面立即中断并展示状态。
