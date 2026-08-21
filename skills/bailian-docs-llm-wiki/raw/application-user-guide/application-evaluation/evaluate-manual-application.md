# 手动评测

大模型应用手动评测是一种基于应用维度评估应用效果的方法，通过针对特定业务场景来人工构建评测集，并对应用的回答进行人工分析与评分，产出评测报告。

## **效果展示**

手动评测通过人工构建评测集，并对应用回答进行人工分析与评分，最终产出评测报告。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0439694571/p996097.png)

## **第一步：准备评测集**

需先下载评测集模板，按照模板内容进行补充内容。示例评测集文件[应用评测-评测集-EfmApplicationdata.xlsx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240123/lfrxah/应用评测-评测集-EfmApplicationdata.xlsx)

**说明**

Prompt：即提示词，简单的理解为它是给大模型的指令。它可以是一个问题、一段文字描述，甚至可以是带有一堆参数的文字描述。

Completion：Prompt对应的内容。可以是答案、一段文字描述。

SessionId：会话ID，可以自定义编写。

## **第二步：上传评测集**

1.  访问**应用评测**的[评测集](https://bailian.console.aliyun.com/tab=app&scm=20140722.S_%E7%99%BE%E7%82%BCprompt._.RL_%E7%99%BE%E7%82%BCprompt-LOC_aillm-OR_chat-V_3-RC_llm?tab=app#/efm/app_evaluate/tabs?tab=group)页面。
    
2.  单击**创建评测集**，自定义评测集名称，上传准备好的评测集文件。
    
    **说明**
    
    支持扩展名：xls、xlsx，文件最大20M，单次最多上传10个文件。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0439694571/p996082.png)
    
3.  单击**确认**后，将在[评测集](https://bailian.console.aliyun.com/tab=app&scm=20140722.S_%E7%99%BE%E7%82%BCprompt._.RL_%E7%99%BE%E7%82%BCprompt-LOC_aillm-OR_chat-V_3-RC_llm?tab=app#/efm/app_evaluate/tabs?tab=group)页面显示上传的文件。
    
4.  等待**导入状态**为**导入成功**时，单击**操作**列的**发布**，发布当前评测集。
    
    > 草稿状态的评测集不能用于应用评测，必须发布后再使用。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0439694571/p996087.png)
    

## **第三步：创建评测任务**

1.  访问**[手动评测](https://bailian.console.aliyun.com/tab=app&scm=20140722.S_%E7%99%BE%E7%82%BCprompt._.RL_%E7%99%BE%E7%82%BCprompt-LOC_aillm-OR_chat-V_3-RC_llm?spm=0.0.0.i1&tab=app#/efm/app_evaluate/tabs?field=gmtCreate&order=descend&pageNum=1&tab=eval&z_type_=%7B%22pageNum%22%3A%22num%22%7D)**页面，单击**创建评测任务**。在**应用批量评测**的下拉列表中选择已发布的智能体应用，单击**下一步**。
    
    > 当前仅支持选择已发布的**智能体应用**。
    
    **说明**
    
    **应用批量评测**：应用批量评测需要选择评测集进行评测，适用于应用上线前端到端效果验证。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8229463471/p937409.png)

2.  选择已经完成上传并**发布**的评测集，单击**下一步**。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8229463471/p937413.png)

3.  选择评测维度，单击**下一步**。
    
    如果未配置[自定义评测维度](https://help.aliyun.com/zh/model-studio/evaluation-metrics#46a5d1d06dd8u)模板，可以选择内置模板。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8229463471/p937416.png)

4.  自定义修改**任务名称**，查看评测任务的完整信息、单击**计算详情**查看预估费用。
    
    确认无误后单击**开始评测**。
    

**说明**

**预估费用**：应用批量评测将基于评测集进行推理获取模型结果，使用公共资源部署模型，可能产生Tokens调用费用或消耗Tokens流量包，使用独占资源部署模型，不收费，请确认后开始评测，费用说明如下

评测费用=评测产生的Tokens \* 模型调用单价

评测产生的Tokens总量包括评测集Tokens总量及推理结果Tokens总量，最终以实际产生的费用为准。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8229463471/p937417.png)

5.  等待评测状态为**标注中**时，单击**操作**列的**标注**按钮，针对应用生成结果进行**打标**。
    
    > “打标”是指对应用生成的结果和评测集中的标准答案进行对比，并对应用生成的结果进行评价（如“较差”“一般”“较好”）或者打分（如1-5分）。通过打标，可以识别应用在不同场景下的表现优劣。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0439694571/p996092.png)
    
    对比评测集结果和应用A生成的结果，给出综合评价【较差、一般、较好】，单击**保存并下一个**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0439694571/p954478.png)
    

6.  对评测集中的每条数据打标后，单击**完成评测并提交**，完成应用评测。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8229463471/p937463.png)

## **查看评测结果**

评测完成后，**评测状态**显示**已完成**。单击**操作**列的**结果**查看评测结果详情。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0439694571/p996094.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0439694571/p996097.png)
