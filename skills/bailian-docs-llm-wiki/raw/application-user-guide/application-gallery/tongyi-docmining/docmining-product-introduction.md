# 通义数据挖掘产品介绍

## **产品概述**

通义数据挖掘是基于阿里云通义大模型构建的文档处理应用。核心功能涵盖信息抽取、内容审核、分类打标和摘要生成。

## **功能列表**

**功能点**

**说明**

文档管理

文档上传、文档删除

信息抽取

根据指定字段列表，在上传文档中进行搜索并抽取

内容审核

根据指定审核规则，检测内容风险，高精度输出审核结果

分类打标

根据指定分类标签，对上传文档进行分类打标

摘要生成

生成要点总结

## **计量计费**

每次调用按照输入长度进行计量计费，所有调用均按实际Token消耗计费。

**输入长度**

**输入（每千Token）**

**输出（每千Token）**

长度≤256K

0.0006元

0.001元

256K＜长度≤10M

0.0016元

0.0032元

**说明**

-   仅开通服务不收费。
    
-   计费周期从实际调用服务开始计算，当前免费体验，预计于2025年12月15日开启正式计费。
    

## **使用限制**

-   支持格式：PDF/TXT/MD/HTML/DOC/PPT/XLS/PNG/BMP/GIF/JPG/JPEG。
    
-   单文件限制：最大100MB；若为PDF文件，最多支持1000页。
    
-   文档对话：单次最多支持100个文档；控制台单次最多支持50个文档。
    
-   存储总量：免费存储1万份文件。
    

## **产品体验**

1.  在阿里云百炼控制台的应用广场中单击[通义数据挖掘](https://bailian.console.aliyun.com/?spm=a2ty02.30275987.d_app-market.1.1f0c74a1zU7JEh&tab=app#/app/app-market/zhiwen)卡片，进入**应用详情**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3500873571/p988172.png)
    
2.  首次试用时，点击右上角**免费开通**完成应用开通。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3500873571/p989913.png)
    
3.  单击**效果调试**进行功能体验。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3500873571/p988206.png)
    

## **API参考**

本应用调用接口的参数说明，请参考[API参考](https://help.aliyun.com/zh/model-studio/docmining-api-reference/)。
