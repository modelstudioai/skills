# 通过Spring AI Alibaba检索阿里云百炼知识库

## **适用范围**

-   **JDK 版本：**JDK 17 或更高版本
    
-   **Spring Boot版本：**Spring Boot 3 GA或更高版本
    

## **操作步骤**

### **1\. 获取项目代码**

完整的示例代码请参见[Spring AI Alibaba项目示例](https://github.com/spring-ai-alibaba/examples/tree/main)下的**bailian-rag-knowledge**。请将整个[examples](https://github.com/spring-ai-alibaba/examples/tree/main)目录下载到本地，以确保项目结构和依赖完整。

### **2\. 环境配置**

[获取阿里云百炼的API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并配置到环境变量，环境变量名使用`AI_DASHSCOPE_API_KEY`。使用环境变量可避免硬编码带来的安全风险。

> 如需操作[子业务空间](https://help.aliyun.com/zh/model-studio/use-workspace#163e7aeb97kq8)的知识库，还需要获取[业务空间 ID](https://help.aliyun.com/zh/model-studio/use-workspace#c5222ec081sbo)，并配置到环境变量，环境变量名使用`AI_DASHSCOPE_WORKSPACE_ID`。

```
# bailian-rag-knowledge的配置文件路径：bailian-rag-knowledge/src/main/resources/application.yml
spring:
  ai:
    dashscope:
      api-key: ${AI_DASHSCOPE_API_KEY} # 阿里云百炼的 API Key
      # workspace-id: ${AI_DASHSCOPE_WORKSPACE_ID} # 业务空间 ID（可选），检索默认业务空间的知识库时无需配置
```

### **3\. 示例代码**

通过`DashScopeApi`检索阿里云百炼知识库。

**Controller示例代码**

```
import org.springframework.web.bind.annotation.*;

import com.alibaba.cloud.ai.example.rag.knowledge.service.RagService;
import reactor.core.publisher.Flux;

@RestController
@RequestMapping("/ai")
public class CloudRagController {
    
    /** 注入CloudRagService */
    private final RagService cloudRagService;
    
    public CloudRagController(RagService cloudRagService) {
        this.cloudRagService = cloudRagService;
    }
    
    @GetMapping(value="/bailian/knowledge/generate", produces="text/event-stream")
    public Flux<String> generate(@RequestParam(value = "message",
                    defaultValue = "你好，请问你的知识库文档主要是关于什么内容的?") String message) {
        return cloudRagService.retrieve(message).map(x -> x.getResult().getOutput().getContent());
    }
}
```

当用户提问时，`DashScopeDocumentRetriever`会检索与问题最相关的文本切片，并将这些上下文与原始问题一并提交给大模型（默认为`qwen-max`）生成回答。

**Service示例代码**

```
import com.alibaba.cloud.ai.advisor.DocumentRetrievalAdvisor;
import com.alibaba.cloud.ai.dashscope.api.DashScopeApi;
import com.alibaba.cloud.ai.dashscope.rag.*;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.chat.prompt.SystemPromptTemplate;
import org.springframework.ai.document.Document;
import org.springframework.ai.document.DocumentReader;
import org.springframework.ai.rag.retrieval.search.DocumentRetriever;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;

@Service()
public class CloudRagService implements RagService {
    /** 此处INDEX_NAME的值为待检索知识库的名称，知识库需要提前创建好 */
    private static final String INDEX_NAME = "测试知识库";
    
    /** 提示词模板 */
    private static final String retrievalSystemTemplate = """
        以下是上下文信息。 
        --------------------- 
        {question_answer_context} 
        --------------------- 
        请根据上下文，而不是先验知识，回复用户评论。如果答案不在上下文中，告知用户认为你不能回答这个问题。
        """; 

    private final ChatClient chatClient;
    
    private final DashScopeApi dashscopeApi;
    
    public CloudRagService(ChatClient.Builder builder, DashScopeApi dashscopeApi) {
            // 创建DocumentRetriever，用于检索知识库
            DocumentRetriever retriever = new DashScopeDocumentRetriever(dashscopeApi,
            DashScopeDocumentRetrieverOptions.builder().withIndexName(INDEX_NAME).build());
        
            this.dashscopeApi = dashscopeApi;
            // 初始化ChatClient，此处设置待检索知识库和待调用的模型
            this.chatClient = builder
                .defaultAdvisors(new DocumentRetrievalAdvisor(retriever, retrievalSystemTemplate))
                // 模型默认使用qwen-max，可通过如下代码设置不同的模型
                //.defaultOptions(DashScopeChatOptions.builder().withModel("qwen-plus").build())
                .build();
    }

    @Override
    public Flux<ChatResponse> retrieve(String message) {
        return chatClient.prompt().user(message).stream().chatResponse();
    }
}
```

## **了解更多**

-   [Spring AI Alibaba](https://java2ai.com/?spm=4347728f.638c0b20.0.0.23f87982NTcSMy)：提供文档教程、实战博客和开发者社区，帮助您快速开发 Java 生成式 AI 应用。
    
-   [创建和使用知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)：深入了解阿里云百炼知识库的核心功能与最佳实践。
