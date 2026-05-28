# 影视互娱剧本创作计费

全妙产品矩阵包含4个SaaS产品妙笔/妙策/妙搜/妙读和若干个AI Agent（场景化能力），本文档主要介绍AI Agent中影视互娱剧本创作应用的计费。

## **计费说明**

系统会根据您实际选取的大模型的输出、输出token总数做计量，并采用后付费模式向您收取费用。

## **计费详情**

模型

输入价格

输出价格

全妙-Max

¥0.06/千tokens

¥0.06/千tokens

## **账单地址**

账单查询地址：[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail?spm=a2c4g.11186623.0.0.619355efACwmfT)。

## **产品地址**

可点击[产品地址](https://bailian.console.aliyun.com/?spm=5176.21213303.J_v8LsmxMG6alneH-O7TCPa.3.5d382f3dPKUN9O&scm=20140722.S_card%40%40&tab=app#/app/app-market/quanmiao/script-create)进行产品体验。

## **相关文档**

[影视互娱剧本创作接口文档](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-dir-film-and-television-mutual-entertainment-script-creation/)

## **常见问题**

-   ### **如果任务运行到中途失败了，怎么计费？**
    
    当任务运行到中途失败时，主要是看最后一个事件消息的event，如果是task-failed，就不计费；其他运行成功部分计费，失败部分不计费。在产品客户端页面立即中断并展示状态。
