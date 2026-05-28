# 作文批改计费

全妙产品矩阵包含4个SaaS产品妙笔/妙策/妙搜/妙读和若干个AI Agent（场景化能力），本文档主要介绍AI Agent中作文批改应用的计费。

## **计费说明**

系统将根据您实际使用的模型所产生的输入与输出 Tokens 总量进行计费，采用后付费模式，按量结算。

## **开通产品&产品控制台**

-   开通产品：点击[作文批改开通页面](https://common-buy.aliyun.com/?commodityCode=sfm_quanmiaoAPI_public_cn)可开通作文批改产品服务；
    
-   产品控制台：点击[产品控制台](https://bailian.console.aliyun.com/?spm=5176.30275541.J_ZGek9Blx07Hclc3Ddt9dg.4.1d6c2f3deJ9i11&scm=20140722.S_card%40%40%E4%BA%A7%E5%93%81%40%402983180.S_new%7EUND%7Ecard.ID_card%40%40%E4%BA%A7%E5%93%81%40%402983180-RL_%E7%99%BE%E7%82%BC%E5%A4%A7%E6%A8%A1%E5%9E%8B-LOC_2024SPSearchCard-OR_ser-PAR1_2150420317622352750362019e6447-V_4-RE_new5-P0_0-P1_0&tab=app&productCode=p_efm&switchAgent=10680836#/app/app-market/quanmiao/homework-correction)进行产品体验。
    

## **计费详情**

模型

输入价格

输出价格

作文批改模型1

¥0.015/千tokens

¥0.015/千tokens

作文批改轻量模型

¥0.0015/千tokens

¥0.0015/千tokens

自定义批改模型

¥0.0015/千tokens

¥0.0015/千tokens

通义千问-OCR模型

¥0.01/千tokens

¥0.01/千tokens

通义千问-OCR轻量模型

¥0.0006/千tokens

¥0.0006/千tokens

## **相关文档**

接口文档：[作文批改接口](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-runessaycorrection)。

## **常见问题**

-   ### **如果任务运行到中途失败了，怎么计费？**
    
    当任务运行到中途失败时，主要是看最后一个事件消息的event，如果是task-failed，就不计费；其他运行成功部分计费，失败部分不计费。在产品客户端页面立即中断并展示状态。
