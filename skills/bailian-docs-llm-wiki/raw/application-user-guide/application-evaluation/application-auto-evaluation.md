# 自动评测

人工评测智能体应用需要手动构建评测集，耗时费力，同时评测结果依赖领域专家的判断，虽保证了专业性，但过程难以量化且可能带入个人主观偏好。阿里云百炼提供了自动评测功能，利用大模型、基于应用的知识库自动生成评测集，评估智能体的回答并生成评测报告与调优建议。自动评测支持两种模式：

-   **单应用评测**：深度评估单个智能体应用的表现，生成包含评分、错误分析和优化建议的详细报告，用于快速发现问题并针对性优化。
    
-   **多应用横向评测**：在同一评测基准下，对比评估多个应用（或同一应用的不同版本）的各项指标，用于选型决策或版本迭代效果验证。
    

## 前提条件

1.  自动评测仅面向已发布的[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)。应用发布请参考[应用分享](https://help.aliyun.com/zh/model-studio/share-an-application)。
    
2.  自动评测将基于知识库自动生成评测集，请确保应用已配置知识库。详情可参考[创建和使用知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)。
    
3.  智能体应用评测依赖于智能体推理的过程数据，请确保已开通`应用观测`功能，并将需要评测的应用添加到观测列表中。详情可参考[用量监控与性能分析](https://help.aliyun.com/zh/model-studio/application-observation)。
    
4.  子账号（RAM用户）需获取`管理员`或`应用评测-操作`权限，才能够使用自动评测功能。详情可参考[页面权限](https://help.aliyun.com/zh/model-studio/member-management#febd776ce5lbx)。
    

## 操作流程

完成一次完整的自动评测需要经历四个阶段：创建评测任务、设置评测集、配置评测规则和执行评测。

### **创建评测任务**

1.  进入阿里云百炼控制台[自动评测](https://bailian.console.aliyun.com/?&tab=app&scm=20140722.S_%E7%99%BE%E7%82%BCprompt._.RL_%E7%99%BE%E7%82%BCprompt-LOC_aillm-OR_chat-V_3-RC_llm#/efm/app_evaluate/tabs)界面，单击**创建评测任务**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8300775671/p1034022.png)
    
    若尚未开通应用观测，请在弹出窗口单击**立即前往**完成开通。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8300775671/p1034024.png)
    

2.  选择需要评测的智能体应用。可以选择 1 个应用进行评测，或选择**最多 8 个**应用进行横向评测。
    
    **说明**
    
    -   仅支持选择**已发布**且**配置知识库**的应用。
        
    -   同一智能体的不同版本将被视为不同的、独立的应用。
        
    -   进行多应用横向评测时，所有被选应用必须都已关联了至少一个相同的知识库。
        
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8300775671/p1034025.png)
    
3.  选择用于评测的知识库。单应用评测时，可从该应用关联的所有知识库中选择一个或多个用于生成评测集；多应用横向评测时，系统会列出所有被选应用的公共知识库，选择一个或多个用于生成评测集。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8300775671/p1034035.png)
    
4.  确认选择无误后，单击**下一步**。若所选应用没有开通应用观测，请在弹出窗口单机**一键开通并进入下一步**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8300775671/p1034038.png)
    

### **设置评测集**

评测集选择支持**生成评测集**和**选择已有评测集**两种方式：

-   生成评测集：基于上一步选中的知识库，由大模型自动生成评测集。所有生成的评测集均可在[评测集](https://bailian.console.aliyun.com/?&tab=app&scm=20140722.S_%E7%99%BE%E7%82%BCprompt._.RL_%E7%99%BE%E7%82%BCprompt-LOC_aillm-OR_chat-V_3-RC_llm#/efm/app_evaluate/tabs?tab=group)页面查看。
    
-   选择已有评测集：复用已有评测集，需确保所选评测集内各问题的参考答案，均能在当前指定的知识库中找到。否则将导致评测结果不准确。评测集格式请参考[评测集](https://help.aliyun.com/zh/model-studio/application-evaluation-dataset)。
    

以下以生成评测集为例。

1.  输入评测集名称。
    
2.  选择任务类型。生成评测集时，需选择 2 至 8 种任务类型。系统默认提供“事实型”、“分析型”、“比较型”、“教程型”四种任务类型。此外也支持自定义新类型，单击**增加任务类型**，输入任务类型、描述和示例即可。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8300775671/p1034046.png)
    
3.  选择用于生成评测任务的模型。为确保生成质量，目前仅支持使用`qwen-max`和`qwen-plus`模型。各模型能力请参考[选择模型](https://help.aliyun.com/zh/model-studio/models)，计费规则请参考[模型调用计费](https://help.aliyun.com/zh/model-studio/model-pricing)。
    
4.  模型选择完毕后，页面下方将显示模型 Token 的预估平均消耗和预估最大消耗。评测完成后，可以在[自动评测](https://bailian.console.aliyun.com/tab=app&scm=20140722.S_%E7%99%BE%E7%82%BCprompt._.RL_%E7%99%BE%E7%82%BCprompt-LOC_aillm-OR_chat-V_3-RC_llm#/efm/app_evaluate/tabs)页面查看实际 Token 消耗明细。
    
    **说明**
    
    -   **预估平均消耗**是**参考值**，最终用量请以实际账单为准。
        
    -   **预估最大消耗**是为防止意外的超长输出而设置的成本硬性上限，实际消耗通常远低于此值。
        
    
5.  单击**生成评测集**，在弹出页面确认配置信息，然后单击**继续生成**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8300775671/p1034054.png)
    
6.  等待评测集生成，生成状态可在[评测集](https://bailian.console.aliyun.com/?&tab=app&scm=20140722.S_%E7%99%BE%E7%82%BCprompt._.RL_%E7%99%BE%E7%82%BCprompt-LOC_aillm-OR_chat-V_3-RC_llm#/efm/app_evaluate/tabs?tab=group)管理页面查看。评测集生成的时间开销，主要取决于所选知识库的数量与文档总量。生成完毕后，单击**下一步**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8300775671/p1034070.png)
    

### **配置评测规则**

1.  选择分类采样数。用于设置每个任务类型需要采样的问题数量。系统将从每个类型下随机抽取指定数量的问题用于最终评测。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8300775671/p1034086.png)
    
2.  选择评测模型。为确保结果准确，目前仅支持使用`qwen-max`和`qwen-plus`模型，模型能力和计费规则请参考[选择模型](https://help.aliyun.com/zh/model-studio/models)和[模型调用计费](https://help.aliyun.com/zh/model-studio/model-pricing)。
    
3.  模型选择完毕后，下方将显示预估平均消耗和预估最大消耗。采样的评测数据越多，消耗的 Token 数量越大。评测完成后，可在[自动评测](https://bailian.console.aliyun.com/tab=app&scm=20140722.S_%E7%99%BE%E7%82%BCprompt._.RL_%E7%99%BE%E7%82%BCprompt-LOC_aillm-OR_chat-V_3-RC_llm#/efm/app_evaluate/tabs)页面查看实际 Token 消耗明细。
    
    **说明**
    
    -   **预估平均消耗**是**参考值**，最终用量请以实际账单为准。
        
    -   **预估最大消耗**是为防止意外的超长输出而设置的成本硬性上限，实际消耗通常远低于此值。
        
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8300775671/p1034090.png)
    
4.  在正式评测之前，可以选择试运行以预览评测效果，**试运行仅支持单个应用的评测结果预览**。试运行将随机抽取一道题执行完整评测，此过程会消耗少量 Token。单击**试运行**，在弹窗中选择需要试运行评测的应用，再次单击**试运行**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8300775671/p1034097.png)
    
    查看试运行结果。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8300775671/p1034100.png)
    

### **执行评测**

1.  确认评测集与评测规则配置无误后，单击**发起评测任务**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8300775671/p1034104.png)
    
2.  在弹出窗口确认评测配置和预计消耗后，单击**开始评测**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8300775671/p1034250.png)
    
    等待评测完成。自动评测的时间开销，主要取决于评测样本的总规模。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8300775671/p1034253.png)
    
3.  评测完成后，可在任务列表中单击**追加评测**，为本次任务加入新的应用进行对比。此操作适用于单应用评测和多应用评测。追加后的应用总数不能超过 8 个。
    
    ![20251211114058](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8300775671/p1034255.jpg)
    

## 评测报告分析

### 评分机制

系统使用大模型对每个回答进行评分（1-5 分），评分时会对比智能体的输出和评测集中的参考答案，评估答案的准确性、完整性和相关性。评分规则如下：

-   **5 分：**答案正确，质量优秀**。**
    
-   **4 分**：答案正确，质量良好。
    
-   **4 分以下**：答案错误，系统将自动进行归因分析。
    

### 结果分析

1.  **总正确率**：展示应用的整体表现评估，计算公式：总正确率 = 得分不低于4分的回答数量 / 总回答数量 × 100%。多应用评测会以图表形式展示各应用的对比。
    
    单应用：
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3639694571/p994661.png)
    
    多应用：
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3639694571/p993712.png)
    
2.  **BadCase 分析**：BadCase 列表默认按分数从低到高展示 Top-5 的错误评测条目，点击**查看全部数据**可以查看全部错误评测条目。
    
    > 若无 BadCase，BadCase 分析列表将为空。如需查看全部结果，可单击页面右上角**下载评测结果**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3639694571/p994664.png)
    
3.  **调优建议**：系统会根据归因分析结果，提供针对Prompt、检索配置或知识库切片的具体优化建议。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3639694571/p994666.png)
    
4.  **RAG 智能体评价**：展示各问题类型（如事实型、分析型）的单项得分。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3639694571/p994670.png)
    

### 归因分析

对于得分低于 4 分的 BadCase，系统会自动进行归因分析，定位问题出在 RAG 流程的哪个环节。各项归因类型的含义及优化建议如下：

1.  **模型理解有误**：已获取正确知识，但应用配置的提示词不明确或模型推理能力不足，导致答案错误。需补充更清晰的回答要求或切换更强的模型。
    
2.  **重排不佳**：正确切片已被召回，但排序靠后未被包含在最终传递给大模型的上下文中。需调整重排配置或增加传递给模型的切片数量。
    
3.  **检索无效**：通常是由于设置的检索策略不合适，导致召回了过多或过少的切片。需根据数据特点调整检索方式。
    
4.  **切片不完整**：通常是由于创建知识库时，切分粒度过细导致一个完整的语义单元被分割到多个不同的切片中。需增大切片长度或启用语义切分。
    
5.  **未获取知识**：可能是由于知识库召回无结果或缺失与问题相关的内容。需向知识库中补充相应知识。
    

## 最佳实践

单次评测只能反映应用在特定时间点的表现。要持续保障智能体应用的质量，需要将自动评测融入日常的开发和运维流程。

### 建立持续评测机制

以下场景建议触发一次评测：

-   **知识库更新后**：新增、修改或删除知识内容可能影响检索和回答质量。
    
-   **调整 Prompt 后**：提示词的变化直接影响模型的输出行为。
    
-   **更换或升级模型后**：不同模型的理解和生成能力存在差异。
    
-   **调整检索/重排策略后**：这些配置直接影响 RAG 流程的召回质量。
    
-   **定期回归（每周或每月）**：即使没有主动变更，也建议定期评测以监控潜在的质量波动。
    

### 建立优化闭环

建议按以下流程进行迭代：

1.  **识别 BadCase**：在评测报告中，重点关注得分低于 4 分的回答。
    
2.  **分析归因，定位问题**：根据系统给出的归因类型，参考[归因分析](#c686b552abp3n)中的说明，快速定位每个 BadCase 的产生原因。
    
3.  **实施针对性优化**：根据归因结果，修改对应的配置。
    
4.  **发布新版本，再次评测**：将优化后的应用发布为新版本，使用同一评测集进行评测。
    
5.  **对比结果，确认改进**：对比新旧版本的评测报告，验证优化效果。若优化效果未达预期或发现新问题，则返回第一步，开始新一轮优化循环。
    

## 常见问题

### **模型 Token 的预估平均消耗和预估最大消耗有什么区别？为什么实际消耗与预估消耗不符？**

1.  **预估平均消耗**是**参考值**，最终用量请以实际账单为准。
    
2.  **预估最大消耗**是**理论上限**，基于模型最大输入输出 Token 长度计算，实际消耗不会超过这个值。
    

### **为什么评测集生成和应用评测的进度长时间保持在0%？**

评测集生成和应用评测均为离线任务，需在后台排队执行，排队期间进度将保持0%。任务开始执行后，进度会自动更新。

### **评测任务运行时，关闭应用观测会有什么影响？**

为确保评测任务正常运行，请勿在评测期间关闭应用观测，否则可能导致评测任务失败、数据丢失或最终评测报告不准确。

### 为什么评测报告中显示的用例数量与设置的不符？

自动评测可能会失败。评测报告只显示成功完成评测的任务用例，失败的任务不计入最终正确率的计算。

### **为什么评测任务失败了，还会消耗 Token？**

评测任务是分步执行的。每个成功完成的步骤都会消耗 Token 并计费。如果任务在后续步骤失败，此前已消耗的 Token 仍然会计入用量。
