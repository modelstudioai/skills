# 知识库配额与限制

## **用量配额**

**类别**

**描述**

**上限**

**知识库数量**

每个[阿里云账号（主账号）](https://help.aliyun.com/zh/model-studio/permission-management-overview#24ca2dad7djzs)可创建的知识库数量。

-   使用RDS数据源：100
    
-   其它数据源：无限制
    

**知识库存储容量（平台存储）**

每个知识库独享的免费向量存储空间。

-   旗舰版：9,999 GB
    
-   标准版：100 GB
    

**类目数量**

每个[业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)可创建的类目数量（父级+子级）。

500

**文件数量**

每个业务空间可上传的文件数量。

100,000

**数据表数量**

每个业务空间可创建的数据表数量。

1,000

## **文件上传**

### **支持的格式**

**文档搜索类知识库**

**支持格式**

**限制**

pdf、docx、doc、wps、pptx、ppt

-   最大100MB
    
-   页数不超过1,000
    

txt、markdown、html

最大10MB

xlsx、xls

最大10MB，10万行以内

png、jpg / jpeg、bmp、gif

-   最大20MB
    
-   图片短边 > 15 像素，长边 < 8,192像素，最长边与最短边的比例 < 50
    

**数据查询、图片问答类知识库**

**支持格式**

**限制**

xlsx、xls

-   最大100,000行
    
-   列数不超过100
    

**音视频搜索类知识库**

**支持格式**

**限制**

aac、amr、flac、flv、m4a、mp3、mpeg、ogg、opus、wav、webm、wma、mp4、mkv、avi、mov、wmv

最大512MB

### **上传操作**

**类别**

**描述**

**上限**

**单次导入文件数量**

在控制台单次操作可同时导入的文件数量。

> 通过API进行批量导入时不受此限制，但建议单次导入不超过 10,000 个文件。

50

**标签数量**

单个文件可附加的标签数量。

32

## **数据处理**

### **切片**

**类别**

**描述**

**上限**

**文本切片数量**

单个文件的文本切片数量。

无限制

**文本切片长度**

单个文本切片的Token数量。

6,000

### **向量化**

> 更多信息，请参见[文本与多模态向量化](https://help.aliyun.com/zh/model-studio/embedding)。

**类别**

**说明**

**向量模型**

-   **文档搜索类、数据查询、音视频搜索类知识库：**支持text-embedding-v4、text-embedding-v3模型。
    
-   **图片问答类知识库：**目前只支持multimodal-embedding-v1模型。
    

**向量维度**

-   text-embedding-v4：512维
    
-   text-embedding-v3：512维
    
-   multimodal-embedding-v1：1024维
    

> 以上向量维度不支持更改。

## **检索**

**类别**

**描述**

**上限**

**检索并发**

指知识库自身的核心[检索](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve)性能（不含依赖链路，例如调用排序模型）**。**

> 创建知识库（旗舰版）时，可预设依赖链路[限流](https://help.aliyun.com/zh/model-studio/rate-limit)后的处理策略。

-   旗舰版：50-10,000 QPS（可调，对应 1-200 RCU）
    
-   标准版：1 QPS（固定值，无法调整）
    

**召回文本切片数量**

单次查询可召回的文本切片数量。

20
