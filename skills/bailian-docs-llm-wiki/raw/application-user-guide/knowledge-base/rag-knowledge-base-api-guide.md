# 知识库API指南

阿里云百炼知识库提供开放的API接口，便于您快速接入现有业务系统，实现自动化操作，并应对复杂的检索需求。

**重要**

本文档仅适用于文档搜索类知识库。

## **前置步骤**

1.  [子账号](https://help.aliyun.com/zh/model-studio/application-permission-management-overview#24ca2dad7djzs)（主账号不需要）需获取[API权限](https://help.aliyun.com/zh/model-studio/member-management#a2e8c1d6246s2)（AliyunBailianDataFullAccess策略），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)，然后才能通过阿里云API操作知识库。
    
    > 子账号只能操作已加入业务空间中的知识库；主账号可操作所有业务空间下的知识库。
    
2.  安装最新版[阿里云百炼SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29&language=python-tea&tab=primer-doc)，以调用知识库相关的阿里云API。如何安装请参考[阿里云SDK开发参考](https://help.aliyun.com/zh/sdk/developer-reference/)目录下文档。
    
    > 如果SDK不能满足需求，可以通过[签名机制](https://help.aliyun.com/zh/sdk/product-overview/v3-request-structure-and-signature)（较为复杂）HTTP请求知识库的相关接口。具体对接方式请参见[API概览](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-overview)。
    
3.  [获取AccessKey和AccessKey Secret](https://help.aliyun.com/zh/sdk/developer-reference/configure-the-alibaba-cloud-accesskey-environment-variable-on-linux-macos-and-windows-systems)以及[业务空间 ID](https://help.aliyun.com/zh/model-studio/use-workspace#3d584de2733bp)，并将它们配置到系统环境变量，以运行示例代码。以Linux操作系统为例：
    
    > 如果您使用了 IDE 或其他辅助开发插件，需自行将ALIBABA\_CLOUD\_ACCESS\_KEY\_ID、ALIBABA\_CLOUD\_ACCESS\_KEY\_SECRET和WORKSPACE\_ID变量配置到相应的开发环境中。
    
    ```
    export ALIBABA_CLOUD_ACCESS_KEY_ID='您的阿里云访问密钥ID'
    export ALIBABA_CLOUD_ACCESS_KEY_SECRET='您的阿里云访问密钥密码'
    export WORKSPACE_ID='您的阿里云百炼业务空间ID'
    ```
    
4.  准备好示例知识文档[阿里云百炼系列手机产品介绍.docx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250428/tfewui/%E9%98%BF%E9%87%8C%E4%BA%91%E7%99%BE%E7%82%BC%E7%B3%BB%E5%88%97%E6%89%8B%E6%9C%BA%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D.docx)，用于创建知识库。
    

## **完整示例代码**

## 创建知识库

**重要**

-   在调用本示例之前，请务必完成上述所有[前置步骤](#a4a15bd543can)。子账号调用本示例前需[获取AliyunBailianDataFullAccess策略](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)。
    
-   若您使用了 IDE 或其他辅助开发插件，需将`ALIBABA_CLOUD_ACCESS_KEY_ID`、`ALIBABA_CLOUD_ACCESS_KEY_SECRET`和`WORKSPACE_ID`变量配置到相应的开发环境中。
    

## Python

```
# 示例代码仅供参考，请勿在生产环境中直接使用
import hashlib
import os
import time

import requests
from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

def check_environment_variables():
    """检查并提示设置必要的环境变量"""
    required_vars = {
        'ALIBABA_CLOUD_ACCESS_KEY_ID': '阿里云访问密钥ID',
        'ALIBABA_CLOUD_ACCESS_KEY_SECRET': '阿里云访问密钥密码',
        'WORKSPACE_ID': '阿里云百炼业务空间ID'
    }
    missing_vars = []
    for var, description in required_vars.items():
        if not os.environ.get(var):
            missing_vars.append(var)
            print(f"错误：请设置 {var} 环境变量 ({description})")
    
    return len(missing_vars) == 0

def calculate_md5(file_path: str) -> str:
    """
    计算文件的MD5值。

    参数:
        file_path (str): 文件本地路径。

    返回:
        str: 文件的MD5值。
    """
    md5_hash = hashlib.md5()

    # 以二进制形式读取文件
    with open(file_path, "rb") as f:
        # 按块读取文件，避免大文件占用过多内存
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)

    return md5_hash.hexdigest()

def get_file_size(file_path: str) -> int:
    """
    获取文件大小（以字节为单位）。
    参数:
        file_path (str): 文件本地路径。
    返回:
        int: 文件大小（以字节为单位）。
    """
    return os.path.getsize(file_path)

# 初始化客户端（Client）
def create_client() -> bailian20231229Client:
    """
    创建并配置客户端（Client）。

    返回:
        bailian20231229Client: 配置好的客户端（Client）。
    """
    config = open_api_models.Config(
        access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    )
    # 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
    config.endpoint = 'bailian.cn-beijing.aliyuncs.com'
    return bailian20231229Client(config)

# 申请文件上传租约
def apply_lease(client, category_id, file_name, file_md5, file_size, workspace_id):
    """
    从阿里云百炼服务申请文件上传租约。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        category_id (str): 类目ID。
        file_name (str): 文件名称。
        file_md5 (str): 文件的MD5值。
        file_size (int): 文件大小（以字节为单位）。
        workspace_id (str): 业务空间ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    request = bailian_20231229_models.ApplyFileUploadLeaseRequest(
        file_name=file_name,
        md_5=file_md5,
        size_in_bytes=file_size,
    )
    runtime = util_models.RuntimeOptions()
    return client.apply_file_upload_lease_with_options(category_id, workspace_id, request, headers, runtime)

# 上传文件到临时存储
def upload_file(pre_signed_url, headers, file_path):
    """
    将文件上传到阿里云百炼服务。
    参数:
        pre_signed_url (str): 上传租约中的 URL。
        headers (dict): 上传请求的头部。
        file_path (str): 文件本地路径。
    """
    with open(file_path, 'rb') as f:
        file_content = f.read()
    upload_headers = {
        "X-bailian-extra": headers["X-bailian-extra"],
        "Content-Type": headers["Content-Type"]
    }
    response = requests.put(pre_signed_url, data=file_content, headers=upload_headers)
    response.raise_for_status()

# 添加文件到类目中
def add_file(client: bailian20231229Client, lease_id: str, parser: str, category_id: str, workspace_id: str):
    """
    将文件添加到阿里云百炼服务的指定类目中。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        lease_id (str): 租约ID。
        parser (str): 用于文件的解析器。
        category_id (str): 类目ID。
        workspace_id (str): 业务空间ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    request = bailian_20231229_models.AddFileRequest(
        lease_id=lease_id,
        parser=parser,
        category_id=category_id,
    )
    runtime = util_models.RuntimeOptions()
    return client.add_file_with_options(workspace_id, request, headers, runtime)

# 查询文件的解析状态
def describe_file(client, workspace_id, file_id):
    """
    获取文件的基本信息。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        file_id (str): 文件ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    runtime = util_models.RuntimeOptions()
    return client.describe_file_with_options(workspace_id, file_id, headers, runtime)

# 初始化知识库（索引）
def create_index(client, workspace_id, file_id, name, structure_type, source_type, sink_type):
    """
    在阿里云百炼服务中创建知识库（初始化）。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        file_id (str): 文件ID。
        name (str): 知识库名称。
        structure_type (str): 知识库的数据类型。
        source_type (str): 应用数据的数据类型，支持类目类型和文件类型。
        sink_type (str): 知识库的向量存储类型。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    request = bailian_20231229_models.CreateIndexRequest(
        structure_type=structure_type,
        name=name,
        source_type=source_type,
        sink_type=sink_type,
        document_ids=[file_id]
    )
    runtime = util_models.RuntimeOptions()
    return client.create_index_with_options(workspace_id, request, headers, runtime)

# 提交索引任务
def submit_index(client, workspace_id, index_id):
    """
    向阿里云百炼服务提交索引任务。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    submit_index_job_request = bailian_20231229_models.SubmitIndexJobRequest(
        index_id=index_id
    )
    runtime = util_models.RuntimeOptions()
    return client.submit_index_job_with_options(workspace_id, submit_index_job_request, headers, runtime)

# 等待索引任务完成
def get_index_job_status(client, workspace_id, job_id, index_id):
    """
    查询索引任务状态。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        job_id (str): 任务ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    get_index_job_status_request = bailian_20231229_models.GetIndexJobStatusRequest(
        index_id=index_id,
        job_id=job_id
    )
    runtime = util_models.RuntimeOptions()
    return client.get_index_job_status_with_options(workspace_id, get_index_job_status_request, headers, runtime)

def create_knowledge_base(
        file_path: str,
        workspace_id: str,
        name: str
):
    """
    使用阿里云百炼服务创建知识库。
    参数:
        file_path (str): 文件本地路径。
        workspace_id (str): 业务空间ID。
        name (str): 知识库名称。
    返回:
        str or None: 如果成功，返回知识库ID；否则返回None。
    """
    # 设置默认值
    category_id = 'default'
    parser = 'DASHSCOPE_DOCMIND'
    source_type = 'DATA_CENTER_FILE'
    structure_type = 'unstructured'
    sink_type = 'DEFAULT'
    try:
        # 步骤1：初始化客户端（Client）
        print("步骤1：初始化Client")
        client = create_client()
        # 步骤2：准备文件信息
        print("步骤2：准备文件信息")
        file_name = os.path.basename(file_path)
        file_md5 = calculate_md5(file_path)
        file_size = get_file_size(file_path)
        # 步骤3：申请上传租约
        print("步骤3：向阿里云百炼申请上传租约")
        lease_response = apply_lease(client, category_id, file_name, file_md5, file_size, workspace_id)
        lease_id = lease_response.body.data.file_upload_lease_id
        upload_url = lease_response.body.data.param.url
        upload_headers = lease_response.body.data.param.headers
        # 步骤4：上传文件
        print("步骤4：上传文件到阿里云百炼")
        upload_file(upload_url, upload_headers, file_path)
        # 步骤5：将文件添加到服务器
        print("步骤5：将文件添加到阿里云百炼服务器")
        add_response = add_file(client, lease_id, parser, category_id, workspace_id)
        file_id = add_response.body.data.file_id
        # 步骤6：检查文件状态
        print("步骤6：检查阿里云百炼中的文件状态")
        while True:
            describe_response = describe_file(client, workspace_id, file_id)
            status = describe_response.body.data.status
            print(f"当前文件状态：{status}")
            if status == 'INIT':
                print("文件待解析，请稍候...")
            elif status == 'PARSING':
                print("文件解析中，请稍候...")
            elif status == 'PARSE_SUCCESS':
                print("文件解析完成！")
                break
            else:
                print(f"未知的文件状态：{status}，请联系技术支持。")
                return None
            time.sleep(5)
        # 步骤7：初始化知识库
        print("步骤7：在阿里云百炼中初始化知识库")
        index_response = create_index(client, workspace_id, file_id, name, structure_type, source_type, sink_type)
        index_id = index_response.body.data.id
        # 步骤8：提交索引任务
        print("步骤8：向阿里云百炼提交索引任务")
        submit_response = submit_index(client, workspace_id, index_id)
        job_id = submit_response.body.data.id
        # 步骤9：获取索引任务状态
        print("步骤9：获取阿里云百炼索引任务状态")
        while True:
            get_index_job_status_response = get_index_job_status(client, workspace_id, job_id, index_id)
            status = get_index_job_status_response.body.data.status
            print(f"当前索引任务状态：{status}")
            if status == 'COMPLETED':
                break
            time.sleep(5)
        print("阿里云百炼知识库创建成功！")
        return index_id
    except Exception as e:
        print(f"发生错误：{e}")
        return None

def main():
    if not check_environment_variables():
        print("环境变量校验未通过。")
        return
    file_path = input("请输入您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：")
    kb_name = input("请为您的知识库输入一个名称：")
    workspace_id = os.environ.get('WORKSPACE_ID')
    create_knowledge_base(file_path, workspace_id, kb_name)

if __name__ == '__main__':
    main()
```

## Java

```
// 示例代码仅供参考，请勿在生产环境中直接使用
import com.aliyun.bailian20231229.models.*;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.io.FileInputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.security.MessageDigest;
import java.util.*;
import java.util.concurrent.TimeUnit;

public class KnowledgeBaseCreate {

    /**
     * 检查并提示设置必要的环境变量。
     *
     * @return true 如果所有必需的环境变量都已设置，否则 false
     */
    public static boolean checkEnvironmentVariables() {
        Map<String, String> requiredVars = new HashMap<>();
        requiredVars.put("ALIBABA_CLOUD_ACCESS_KEY_ID", "阿里云访问密钥ID");
        requiredVars.put("ALIBABA_CLOUD_ACCESS_KEY_SECRET", "阿里云访问密钥密码");
        requiredVars.put("WORKSPACE_ID", "阿里云百炼业务空间ID");

        List<String> missingVars = new ArrayList<>();
        for (Map.Entry<String, String> entry : requiredVars.entrySet()) {
            String value = System.getenv(entry.getKey());
            if (value == null || value.isEmpty()) {
                missingVars.add(entry.getKey());
                System.out.println("错误：请设置 " + entry.getKey() + " 环境变量 (" + entry.getValue() + ")");
            }
        }

        return missingVars.isEmpty();
    }

    /**
     * 计算文件的MD5值。
     *
     * @param filePath 文件本地路径
     * @return 文件的MD5值
     * @throws Exception 如果计算过程中发生错误
     */
    public static String calculateMD5(String filePath) throws Exception {
        MessageDigest md = MessageDigest.getInstance("MD5");
        try (FileInputStream fis = new FileInputStream(filePath)) {
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                md.update(buffer, 0, bytesRead);
            }
        }
        StringBuilder sb = new StringBuilder();
        for (byte b : md.digest()) {
            sb.append(String.format("%02x", b & 0xff));
        }
        return sb.toString();
    }

    /**
     * 获取文件大小（以字节为单位）。
     *
     * @param filePath 文件本地路径
     * @return 文件大小（以字节为单位）
     */
    public static String getFileSize(String filePath) {
        File file = new File(filePath);
        long fileSize = file.length();
        return String.valueOf(fileSize);
    }

    /**
     * 初始化客户端（Client）。
     *
     * @return 配置好的客户端对象
     */
    public static com.aliyun.bailian20231229.Client createClient() throws Exception {
        com.aliyun.teaopenapi.models.Config config = new com.aliyun.teaopenapi.models.Config()
                .setAccessKeyId(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"))
                .setAccessKeySecret(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"));
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
        config.endpoint = "bailian.cn-beijing.aliyuncs.com";
        return new com.aliyun.bailian20231229.Client(config);
    }

    /**
     * 申请文件上传租约。
     *
     * @param client      客户端对象
     * @param categoryId  类目ID
     * @param fileName    文件名称
     * @param fileMd5     文件的MD5值
     * @param fileSize    文件大小（以字节为单位）
     * @param workspaceId 业务空间ID
     * @return 阿里云百炼服务的响应对象
     */
    public static ApplyFileUploadLeaseResponse applyLease(com.aliyun.bailian20231229.Client client, String categoryId, String fileName, String fileMd5, String fileSize, String workspaceId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.bailian20231229.models.ApplyFileUploadLeaseRequest applyFileUploadLeaseRequest = new com.aliyun.bailian20231229.models.ApplyFileUploadLeaseRequest();
        applyFileUploadLeaseRequest.setFileName(fileName);
        applyFileUploadLeaseRequest.setMd5(fileMd5);
        applyFileUploadLeaseRequest.setSizeInBytes(fileSize);
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        ApplyFileUploadLeaseResponse applyFileUploadLeaseResponse = null;
        applyFileUploadLeaseResponse = client.applyFileUploadLeaseWithOptions(categoryId, workspaceId, applyFileUploadLeaseRequest, headers, runtime);
        return applyFileUploadLeaseResponse;
    }

    /**
     * 上传文件到临时存储。
     *
     * @param preSignedUrl 上传租约中的 URL
     * @param headers      上传请求的头部
     * @param filePath     文件本地路径
     * @throws Exception 如果上传过程中发生错误
     */
    public static void uploadFile(String preSignedUrl, Map<String, String> headers, String filePath) throws Exception {
        File file = new File(filePath);
        if (!file.exists() || !file.isFile()) {
            throw new IllegalArgumentException("文件不存在或不是普通文件: " + filePath);
        }

        try (FileInputStream fis = new FileInputStream(file)) {
            URL url = new URL(preSignedUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("PUT");
            conn.setDoOutput(true);

            // 设置上传请求头
            conn.setRequestProperty("X-bailian-extra", headers.get("X-bailian-extra"));
            conn.setRequestProperty("Content-Type", headers.get("Content-Type"));

            // 分块读取并上传文件
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                conn.getOutputStream().write(buffer, 0, bytesRead);
            }

            int responseCode = conn.getResponseCode();
            if (responseCode != 200) {
                throw new RuntimeException("上传失败: " + responseCode);
            }
        }
    }

    /**
     * 将文件添加到类目中。
     *
     * @param client      客户端对象
     * @param leaseId     租约ID
     * @param parser      用于文件的解析器
     * @param categoryId  类目ID
     * @param workspaceId 业务空间ID
     * @return 阿里云百炼服务的响应对象
     */
    public static AddFileResponse addFile(com.aliyun.bailian20231229.Client client, String leaseId, String parser, String categoryId, String workspaceId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.bailian20231229.models.AddFileRequest addFileRequest = new com.aliyun.bailian20231229.models.AddFileRequest();
        addFileRequest.setLeaseId(leaseId);
        addFileRequest.setParser(parser);
        addFileRequest.setCategoryId(categoryId);
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return client.addFileWithOptions(workspaceId, addFileRequest, headers, runtime);
    }

    /**
     * 查询文件的基本信息。
     *
     * @param client      客户端对象
     * @param workspaceId 业务空间ID
     * @param fileId      文件ID
     * @return 阿里云百炼服务的响应对象
     */
    public static DescribeFileResponse describeFile(com.aliyun.bailian20231229.Client client, String workspaceId, String fileId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return client.describeFileWithOptions(workspaceId, fileId, headers, runtime);
    }

    /**
     * 在阿里云百炼服务中创建知识库（初始化）。
     *
     * @param client        客户端对象
     * @param workspaceId   业务空间ID
     * @param fileId        文件ID
     * @param name          知识库名称
     * @param structureType 知识库的数据类型
     * @param sourceType    应用数据的数据类型，支持类目类型和文件类型
     * @param sinkType      知识库的向量存储类型
     * @return 阿里云百炼服务的响应对象
     */
    public static CreateIndexResponse createIndex(com.aliyun.bailian20231229.Client client, String workspaceId, String fileId, String name, String structureType, String sourceType, String sinkType) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.bailian20231229.models.CreateIndexRequest createIndexRequest = new com.aliyun.bailian20231229.models.CreateIndexRequest();
        createIndexRequest.setStructureType(structureType);
        createIndexRequest.setName(name);
        createIndexRequest.setSourceType(sourceType);
        createIndexRequest.setSinkType(sinkType);
        createIndexRequest.setDocumentIds(Collections.singletonList(fileId));
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return client.createIndexWithOptions(workspaceId, createIndexRequest, headers, runtime);
    }

    /**
     * 向阿里云百炼服务提交索引任务。
     *
     * @param client      客户端对象
     * @param workspaceId 业务空间ID
     * @param indexId     知识库ID
     * @return 阿里云百炼服务的响应对象
     */
    public static SubmitIndexJobResponse submitIndex(com.aliyun.bailian20231229.Client client, String workspaceId, String indexId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.bailian20231229.models.SubmitIndexJobRequest submitIndexJobRequest = new com.aliyun.bailian20231229.models.SubmitIndexJobRequest();
        submitIndexJobRequest.setIndexId(indexId);
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return client.submitIndexJobWithOptions(workspaceId, submitIndexJobRequest, headers, runtime);
    }

    /**
     * 查询索引任务状态。
     *
     * @param client      客户端对象
     * @param workspaceId 业务空间ID
     * @param jobId       任务ID
     * @param indexId     知识库ID
     * @return 阿里云百炼服务的响应对象
     */
    public static GetIndexJobStatusResponse getIndexJobStatus(com.aliyun.bailian20231229.Client client, String workspaceId, String jobId, String indexId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.bailian20231229.models.GetIndexJobStatusRequest getIndexJobStatusRequest = new com.aliyun.bailian20231229.models.GetIndexJobStatusRequest();
        getIndexJobStatusRequest.setIndexId(indexId);
        getIndexJobStatusRequest.setJobId(jobId);
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        GetIndexJobStatusResponse getIndexJobStatusResponse = null;
        getIndexJobStatusResponse = client.getIndexJobStatusWithOptions(workspaceId, getIndexJobStatusRequest, headers, runtime);
        return getIndexJobStatusResponse;
    }

    /**
     * 使用阿里云百炼服务创建知识库。
     *
     * @param filePath    文件本地路径
     * @param workspaceId 业务空间ID
     * @param name        知识库名称
     * @return 如果成功，返回知识库ID；否则返回 null
     */
    public static String createKnowledgeBase(String filePath, String workspaceId, String name) {
        // 设置默认值
        String categoryId = "default";
        String parser = "DASHSCOPE_DOCMIND";
        String sourceType = "DATA_CENTER_FILE";
        String structureType = "unstructured";
        String sinkType = "DEFAULT";
        try {
            // 步骤1：初始化客户端（Client）
            System.out.println("步骤1：初始化Client");
            com.aliyun.bailian20231229.Client client = createClient();

            // 步骤2：准备文件信息
            System.out.println("步骤2：准备文件信息");
            String fileName = new File(filePath).getName();
            String fileMd5 = calculateMD5(filePath);
            String fileSize = getFileSize(filePath);

            // 步骤3：申请上传租约
            System.out.println("步骤3：向阿里云百炼申请上传租约");
            ApplyFileUploadLeaseResponse leaseResponse = applyLease(client, categoryId, fileName, fileMd5, fileSize, workspaceId);
            String leaseId = leaseResponse.getBody().getData().getFileUploadLeaseId();
            String uploadUrl = leaseResponse.getBody().getData().getParam().getUrl();
            Object uploadHeaders = leaseResponse.getBody().getData().getParam().getHeaders();

            // 步骤4：上传文件
            System.out.println("步骤4：上传文件到阿里云百炼");
            // 请自行安装jackson-databind
            // 将上一步的uploadHeaders转换为Map(Key-Value形式)
            ObjectMapper mapper = new ObjectMapper();
            Map<String, String> uploadHeadersMap = (Map<String, String>) mapper.readValue(mapper.writeValueAsString(uploadHeaders), Map.class);
            uploadFile(uploadUrl, uploadHeadersMap, filePath);

            // 步骤5：将文件添加到服务器
            System.out.println("步骤5：将文件添加到阿里云百炼服务器");
            AddFileResponse addResponse = addFile(client, leaseId, parser, categoryId, workspaceId);
            String fileId = addResponse.getBody().getData().getFileId();

            // 步骤6：检查文件状态
            System.out.println("步骤6：检查阿里云百炼中的文件状态");
            while (true) {
                DescribeFileResponse describeResponse = describeFile(client, workspaceId, fileId);
                String status = describeResponse.getBody().getData().getStatus();
                System.out.println("当前文件状态：" + status);

                if (status.equals("INIT")) {
                    System.out.println("文件待解析，请稍候...");
                } else if (status.equals("PARSING")) {
                    System.out.println("文件解析中，请稍候...");
                } else if (status.equals("PARSE_SUCCESS")) {
                    System.out.println("文件解析完成！");
                    break;
                } else {
                    System.out.println("未知的文件状态：" + status + "，请联系技术支持。");
                    return null;
                }
                TimeUnit.SECONDS.sleep(5);
            }

            // 步骤7：初始化知识库
            System.out.println("步骤7：在阿里云百炼中创建知识库");
            CreateIndexResponse indexResponse = createIndex(client, workspaceId, fileId, name, structureType, sourceType, sinkType);
            String indexId = indexResponse.getBody().getData().getId();

            // 步骤8：提交索引任务
            System.out.println("步骤8：向阿里云百炼提交索引任务");
            SubmitIndexJobResponse submitResponse = submitIndex(client, workspaceId, indexId);
            String jobId = submitResponse.getBody().getData().getId();

            // 步骤9：获取索引任务状态
            System.out.println("步骤9：获取阿里云百炼索引任务状态");
            while (true) {
                GetIndexJobStatusResponse getStatusResponse = getIndexJobStatus(client, workspaceId, jobId, indexId);
                String status = getStatusResponse.getBody().getData().getStatus();
                System.out.println("当前索引任务状态：" + status);

                if (status.equals("COMPLETED")) {
                    break;
                }
                TimeUnit.SECONDS.sleep(5);
            }

            System.out.println("阿里云百炼知识库创建成功！");
            return indexId;

        } catch (Exception e) {
            System.out.println("发生错误：" + e.getMessage());
            e.printStackTrace();
            return null;
        }
    }

    /**
     * 主函数。
     */
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        if (!checkEnvironmentVariables()) {
            return;
        }

        System.out.print("请输入您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：");
        String filePath = scanner.nextLine();

        System.out.print("请为您的知识库输入一个名称：");
        String kbName = scanner.nextLine();

        String workspaceId = System.getenv("WORKSPACE_ID");
        String result = createKnowledgeBase(filePath, workspaceId, kbName);
        if (result != null) {
            System.out.println("知识库ID: " + result);
        }
    }
}
```

## PHP

```
<?php
// 示例代码仅供参考，请勿在生产环境中直接使用
namespace AlibabaCloud\SDK\Sample;

use AlibabaCloud\Dara\Models\RuntimeOptions;
use AlibabaCloud\SDK\Bailian\V20231229\Bailian;
use AlibabaCloud\SDK\Bailian\V20231229\Models\AddFileRequest;
use \Exception;

use Darabonba\OpenApi\Models\Config;
use AlibabaCloud\SDK\Bailian\V20231229\Models\ApplyFileUploadLeaseRequest;
use AlibabaCloud\SDK\Bailian\V20231229\Models\CreateIndexRequest;
use AlibabaCloud\SDK\Bailian\V20231229\Models\SubmitIndexJobRequest;
use AlibabaCloud\SDK\Bailian\V20231229\Models\GetIndexJobStatusRequest;

class KnowledgeBaseCreate {

    /**
    * 检查并提示设置必要的环境变量。
    *
    * @return bool 返回 true 如果所有必需的环境变量都已设置，否则 false。
    */
    public static function checkEnvironmentVariables() {
        $requiredVars = [
            'ALIBABA_CLOUD_ACCESS_KEY_ID' => '阿里云访问密钥ID',
            'ALIBABA_CLOUD_ACCESS_KEY_SECRET' => '阿里云访问密钥密码',
            'WORKSPACE_ID' => '阿里云百炼业务空间ID'
        ];
        $missingVars = [];
        foreach ($requiredVars as $var => $description) {
            if (!getenv($var)) {
                $missingVars[] = $var;
                echo "错误：请设置 $var 环境变量 ($description)\n";
            }
        }
        return count($missingVars) === 0;
    }

    /**
     * 计算文件的MD5值。
     *
     * @param string $filePath 文件本地路径。
     * @return string 文件的MD5值。
     */
    public static function calculateMd5($filePath) {
        $md5Hash = hash_init("md5");
        $handle = fopen($filePath, "rb");
        while (!feof($handle)) {
            $chunk = fread($handle, 4096);
            hash_update($md5Hash, $chunk);
        }
        fclose($handle);
        return hash_final($md5Hash);
    }

    /**
     * 获取文件大小（以字节为单位）。
     *
     * @param string $filePath 文件本地路径。
     * @return int 文件大小（以字节为单位）。
     */
    public static function getFileSize($filePath) {
        return (string)filesize($filePath);
    }

    /**
     * 初始化客户端（Client）。
     *
     * @return Bailian 配置好的客户端对象（Client）。
     */
    public static function createClient(){
        $config = new Config([
            "accessKeyId" => getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"), 
            "accessKeySecret" => getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        ]);
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
        $config->endpoint = 'bailian.cn-beijing.aliyuncs.com';
        return new Bailian($config);
    }

    /**
     * 申请文件上传租约。
     *
     * @param Bailian $client 客户端（Client）。
     * @param string $categoryId 类目ID。
     * @param string $fileName 文件名称。
     * @param string $fileMd5 文件的MD5值。
     * @param int $fileSize 文件大小（以字节为单位）。
     * @param string $workspaceId 业务空间ID。
     * @return ApplyFileUploadLeaseResponse 阿里云百炼服务的响应。
     */
    public static function applyLease($client, $categoryId, $fileName, $fileMd5, $fileSize, $workspaceId) {
        $headers = [];
        $applyFileUploadLeaseRequest = new ApplyFileUploadLeaseRequest([
            "fileName" => $fileName,
            "md5" => $fileMd5,
            "sizeInBytes" => $fileSize
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->applyFileUploadLeaseWithOptions($categoryId, $workspaceId, $applyFileUploadLeaseRequest, $headers, $runtime);
    }

    /**
     * 上传文件到临时存储。
    *
    * @param string $preSignedUrl 上传租约中的 URL。
    * @param array $headers 上传请求的头部。
    * @param string $filePath 文件本地路径。
    */
    public static function uploadFile($preSignedUrl, $headers, $filePath) {
        $fileContent = file_get_contents($filePath);
        // 设置上传请求头
        $uploadHeaders = [
            "X-bailian-extra" => $headers["X-bailian-extra"],
            "Content-Type" => $headers["Content-Type"]
        ];
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $preSignedUrl);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PUT");
        curl_setopt($ch, CURLOPT_POSTFIELDS, $fileContent);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array_map(function($key, $value) {
            return "$key: $value";
        }, array_keys($uploadHeaders), $uploadHeaders));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        if ($httpCode != 200) {
            throw new Exception("上传失败: " . curl_error($ch));
        }
        curl_close($ch);
    }

    /**
     * 将文件添加到类目中。
     *
     * @param Bailian $client 客户端（Client）。
     * @param string $leaseId 租约ID。
     * @param string $parser 用于文件的解析器。
     * @param string $categoryId 类目ID。
     * @param string $workspaceId 业务空间ID。
     * @return AddFileResponse 阿里云百炼服务的响应。
     */
    public static function addFile($client, $leaseId, $parser, $categoryId, $workspaceId) {
        $headers = [];
        $addFileRequest = new AddFileRequest([
            "leaseId" => $leaseId,
            "parser" => $parser,
            "categoryId" => $categoryId
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->addFileWithOptions($workspaceId, $addFileRequest, $headers, $runtime);
    }

    /**
     * 查询文件的基本信息。
     *
     * @param Bailian $client 客户端（Client）。
     * @param string $workspaceId 业务空间ID。
     * @param string $fileId 文件ID。
     * @return DescribeFileResponse 阿里云百炼服务的响应。
     */
    public static function describeFile($client, $workspaceId, $fileId) {
        $headers = [];
        $runtime = new RuntimeOptions([]);
        return $client->describeFileWithOptions($workspaceId, $fileId, $headers, $runtime);
    }

    /**
     * 在阿里云百炼服务中创建知识库（初始化）。
     *
     * @param Bailian $client 客户端（Client）。
     * @param string $workspaceId 业务空间ID。
     * @param string $fileId 文件ID。
     * @param string $name 知识库名称。
     * @param string $structureType 知识库的数据类型。
     * @param string $sourceType 应用数据的数据类型，支持类目类型和文件类型。
     * @param string $sinkType 知识库的向量存储类型。
     * @return CreateIndexResponse 阿里云百炼服务的响应。
     */
    public static function createIndex($client, $workspaceId, $fileId, $name, $structureType, $sourceType, $sinkType) {
        $headers = [];
        $createIndexRequest = new CreateIndexRequest([
            "structureType" => $structureType,
            "name" => $name,
            "sourceType" => $sourceType,
            "documentIds" => [
                $fileId
            ],
            "sinkType" => $sinkType
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->createIndexWithOptions($workspaceId, $createIndexRequest, $headers, $runtime);
    }

    /**
     * 向阿里云百炼服务提交索引任务。
     *
     * @param Bailian $client 客户端（Client）。
     * @param string $workspaceId 业务空间ID。
     * @param string $indexId 知识库ID。
     * @return SubmitIndexJobResponse 阿里云百炼服务的响应。
     */
    public static function submitIndex($client, $workspaceId, $indexId) {
        $headers = [];
        $submitIndexJobRequest = new SubmitIndexJobRequest([
            'indexId' => $indexId
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->submitIndexJobWithOptions($workspaceId, $submitIndexJobRequest, $headers, $runtime);
    }

    /**
     * 查询索引任务状态。
     *
     * @param Bailian $client 客户端（Client）。
     * @param string $workspaceId 业务空间ID。
     * @param string $indexId 知识库ID。
     * @param string $jobId 任务ID。
     * @return GetIndexJobStatusResponse 阿里云百炼服务的响应。
     */
    public static function getIndexJobStatus($client, $workspaceId, $jobId, $indexId) {
        $headers = [];
        $getIndexJobStatusRequest = new GetIndexJobStatusRequest([
            'indexId' => $indexId,
            'jobId' => $jobId
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->getIndexJobStatusWithOptions($workspaceId, $getIndexJobStatusRequest, $headers, $runtime);
    }

    /**
     * 使用阿里云百炼服务创建知识库。
     *
     * @param string $filePath 文件本地路径。
     * @param string $workspaceId 业务空间ID。
     * @param string $name 知识库名称。
     * @return string|null 如果成功，返回知识库ID；否则返回null。
     */
    public static function createKnowledgeBase($filePath, $workspaceId, $name) {
        // 设置默认值
        $categoryId = 'default';
        $parser = 'DASHSCOPE_DOCMIND';
        $sourceType = 'DATA_CENTER_FILE';
        $structureType = 'unstructured';
        $sinkType = 'DEFAULT';
        try {
            // 步骤1：初始化客户端（Client）
            echo "步骤1：初始化Client\n";
            $client = self::createClient();

            // 步骤2：准备文件信息
            echo "步骤2：准备文件信息\n";
            $fileName = basename($filePath);
            echo("this is filename : $fileName");
            $fileMd5 = self::calculateMd5($filePath);
            $fileSize = self::getFileSize($filePath);

            // 步骤3：申请上传租约
            echo "步骤3：向阿里云百炼申请上传租约\n";
            $leaseResponse = self::applyLease($client, $categoryId, $fileName, $fileMd5, $fileSize, $workspaceId);
            $leaseId = $leaseResponse->body->data->fileUploadLeaseId;
            $uploadUrl = $leaseResponse->body->data->param->url;
            $uploadHeaders = $leaseResponse->body->data->param->headers;
            $uploadHeadersMap = json_decode(json_encode($uploadHeaders), true);

            // 步骤4：上传文件
            echo "步骤4：上传文件到阿里云百炼\n";
            self::uploadFile($uploadUrl, $uploadHeadersMap, $filePath);

            // 步骤5：将文件添加到服务器
            echo "步骤5：将文件添加到阿里云百炼服务器\n";
            $addResponse = self::addFile($client, $leaseId, $parser, $categoryId, $workspaceId);
            $fileId = $addResponse->body->data->fileId;
            echo("fileid: $fileId\n");
            // 步骤6：检查文件状态
            echo "步骤6：检查阿里云百炼中的文件状态\n";
            while (true) {
                $describeResponse = self::describeFile($client, $workspaceId, $fileId);
                $status = $describeResponse->body->data->status;
                echo "当前文件状态：$status\n";
                if ($status == 'INIT') {
                    echo "文件待解析，请稍候...\n";
                } elseif ($status == 'PARSING') {
                    echo "文件解析中，请稍候...\n";
                } elseif ($status == 'PARSE_SUCCESS') {
                    echo "文件解析完成！\n";
                    break;
                } else {
                    echo "未知的文件状态：$status, 请联系技术支持。\n";
                    return null;
                }
                sleep(5);
            }

            // 步骤7：初始化知识库
            echo "步骤7：在阿里云百炼中初始化知识库\n";
            $indexResponse = self::createIndex($client, $workspaceId, $fileId, $name, $structureType, $sourceType, $sinkType);
            $indexId = $indexResponse->body->data->id;

            // 步骤8：提交索引任务
            echo "步骤8：向阿里云百炼提交索引任务\n";
            $submitResponse = self::submitIndex($client, $workspaceId, $indexId);
            $jobId = $submitResponse->body->data->id;

            // 步骤9：获取索引任务状态
            echo "步骤9：获取阿里云百炼索引任务状态\n";
            while (true) {
                $getIndexJobStatusResponse = self::getIndexJobStatus($client, $workspaceId, $jobId, $indexId);
                $status = $getIndexJobStatusResponse->body->data->status;
                echo "当前索引任务状态：$status\n";
                if ($status == 'COMPLETED') {
                    break;
                }
                sleep(5);
            }
            echo "阿里云百炼知识库创建成功！\n";
            return $indexId;
        } catch (Exception $e) {
            echo "发生错误：{$e->getMessage()}\n";
            return null;
        }
    }

    /**
     * 主函数。
     */
    public static function main($args){
        if (!self::checkEnvironmentVariables()) {
            echo "环境变量校验未通过。\n";
            return;
        }
        $filePath = readline("请输入您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：");
        $kbName = readline("请为您的知识库输入一个名称：");
        $workspaceId = getenv('WORKSPACE_ID');
        $result = self::createKnowledgeBase($filePath, $workspaceId, $kbName);
       if ($result) {
           echo "知识库ID: $result\n";
       } else {
           echo "知识库创建失败。\n";
       }
    }
}
// 假定autoload.php位于当前代码文件所在目录的上一级目录中，请根据您的项目实际结构调整。
$path = __DIR__ . \DIRECTORY_SEPARATOR . '..' . \DIRECTORY_SEPARATOR . 'vendor' . \DIRECTORY_SEPARATOR . 'autoload.php';
if (file_exists($path)) {
    require_once $path;
}
KnowledgeBaseCreate::main(array_slice($argv, 1));
```

## Node.js

```
// 示例代码仅供参考，请勿在生产环境中直接使用
'use strict';

const fs = require('fs');
const path = require('path');
const axios = require('axios');
const crypto = require('crypto');

const bailian20231229 = require('@alicloud/bailian20231229');
const OpenApi = require('@alicloud/openapi-client');
const Util = require('@alicloud/tea-util');
const Tea = require('@alicloud/tea-typescript');

class KbCreate {

  /**
   * 检查并提示设置必要的环境变量
   * @returns {boolean} - 如果所有必需的环境变量都已设置，返回 true；否则返回 false
   */
  static checkEnvironmentVariables() {
    const requiredVars = {
      'ALIBABA_CLOUD_ACCESS_KEY_ID': '阿里云访问密钥ID',
      'ALIBABA_CLOUD_ACCESS_KEY_SECRET': '阿里云访问密钥密码',
      'WORKSPACE_ID': '阿里云百炼业务空间ID'
    };

    const missing = [];
    for (const [varName, desc] of Object.entries(requiredVars)) {
      if (!process.env[varName]) {
        console.error(`错误：请设置 ${varName} 环境变量 (${desc})`);
        missing.push(varName);
      }
    }
    return missing.length === 0;
  }

  /**
   * 计算文件的MD5值
   * @param {string} filePath - 文件本地路径
   * @returns {Promise<string>} - 文件的MD5值
   */
  static async calculateMD5(filePath) {
    const hash = crypto.createHash('md5');
    const stream = fs.createReadStream(filePath);

    return new Promise((resolve, reject) => {
      stream.on('data', chunk => hash.update(chunk));
      stream.on('end', () => resolve(hash.digest('hex')));
      stream.on('error', reject);
    });
  }

  /**
   * 获取文件大小（以字节为单位），返回字符串格式
   * @param {string} filePath - 文件本地路径
   * @returns {string} - 文件大小（如 "123456"）
   */
  static getFileSize(filePath) {
    try {
      const stats = fs.statSync(filePath);
      return stats.size.toString();
    } catch (err) {
      console.error(`获取文件大小失败: ${err.message}`);
      throw err;
    }
  }

  /**
   * 创建并配置客户端（Client）
   * @return Client
   * @throws Exception
   */
  static createClient() {
    const config = new OpenApi.Config({
      accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
      accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET
    });
    // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址
    config.endpoint = `bailian.cn-beijing.aliyuncs.com`;
    return new bailian20231229.default(config);
  }

  /**
   * 申请文件上传租约
   * @param {Bailian20231229Client} client - 客户端（Client）
   * @param {string} categoryId - 类目ID
   * @param {string} fileName - 文件名称
   * @param {string} fileMd5 - 文件的MD5值
   * @param {string} fileSize - 文件大小（以字节为单位）
   * @param {string} workspaceId - 业务空间ID
   * @returns {Promise<bailian20231229.ApplyFileUploadLeaseResponse>} - 阿里云百炼服务的响应
   */
  static async applyLease(client, categoryId, fileName, fileMd5, fileSize, workspaceId) {
    const headers = {};
    const req = new bailian20231229.ApplyFileUploadLeaseRequest({
      md5: fileMd5,
      fileName,
      sizeInBytes: fileSize
    });
    const runtime = new Util.RuntimeOptions({});
    return await client.applyFileUploadLeaseWithOptions(
      categoryId,
      workspaceId,
      req,
      headers,
      runtime
    );
  }

  /**
   * 上传文件到临时存储
   * @param {string} preSignedUrl - 上传租约中的URL
   * @param {Object} headers - 上传请求的头部
   * @param {string} filePath - 文件本地路径
   */
  static async uploadFile(preSignedUrl, headers, filePath) {
    const uploadHeaders = {
      "X-bailian-extra": headers["X-bailian-extra"],
      "Content-Type": headers["Content-Type"]
    };
    const stream = fs.createReadStream(filePath);
    try {
      await axios.put(preSignedUrl, stream, { headers: uploadHeaders });
    } catch (e) {
      throw new Error(`上传失败: ${e.message}`);
    }
  }

  /**
   * 添加文件到类目中
   * @param {Bailian20231229Client} client - 客户端（Client）
   * @param {string} leaseId - 租约ID
   * @param {string} parser - 用于文件的解析器
   * @param {string} categoryId - 类目ID
   * @param {string} workspaceId - 业务空间ID
   * @returns {Promise<bailian20231229.AddFileResponse>} - 阿里云百炼服务的响应
   */
  static async addFile(client, leaseId, parser, categoryId, workspaceId) {
    const headers = {};
    const req = new bailian20231229.AddFileRequest({
      leaseId,
      parser,
      categoryId
    });
    const runtime = new Util.RuntimeOptions({});
    return await client.addFileWithOptions(workspaceId, req, headers, runtime);
  }

  /**
   * 查询文件的解析状态
   * @param {Bailian20231229Client} client - 客户端（Client）
   * @param {string} workspaceId - 业务空间ID
   * @param {string} fileId - 文件ID
   * @returns {Promise<bailian20231229.DescribeFileResponse>} - 阿里云百炼服务的响应
   */
  static async describeFile(client, workspaceId, fileId) {
    const headers = {};
    const runtime = new Util.RuntimeOptions({});
    return await client.describeFileWithOptions(workspaceId, fileId, headers, runtime);
  }

  /**
   * 初始化知识库（索引）
   * @param {Bailian20231229Client} client - 客户端（Client）
   * @param {string} workspaceId - 业务空间ID
   * @param {string} fileId - 文件ID
   * @param {string} name - 知识库名称
   * @param {string} structureType - 知识库的数据类型
   * @param {string} sourceType - 应用数据的数据类型，支持类目类型和文件类型
   * @param {string} sinkType - 知识库的向量存储类型
   * @returns {Promise<bailian20231229.CreateIndexResponse>} - 阿里云百炼服务的响应
   */
  static async createIndex(client, workspaceId, fileId, name, structureType, sourceType, sinkType) {
    const headers = {};
    const req = new bailian20231229.CreateIndexRequest({
      name,
      structureType,
      documentIds: [fileId],
      sourceType,
      sinkType
    });
    const runtime = new Util.RuntimeOptions({});
    return await client.createIndexWithOptions(workspaceId, req, headers, runtime);
  }

  /**
   * 提交索引任务
   * @param {Bailian20231229Client} client - 客户端（Client）
   * @param {string} workspaceId - 业务空间ID
   * @param {string} indexId - 知识库ID
   * @returns {Promise<bailian20231229.SubmitIndexJobResponse>} - 阿里云百炼服务的响应
   */
  static async submitIndex(client, workspaceId, indexId) {
    const headers = {};
    const req = new bailian20231229.SubmitIndexJobRequest({ indexId });
    const runtime = new Util.RuntimeOptions({});
    return await client.submitIndexJobWithOptions(workspaceId, req, headers, runtime);
  }

  /**
   * 查询索引任务状态
   * @param {Bailian20231229Client} client - 客户端（Client）
   * @param {string} workspaceId - 业务空间ID
   * @param {string} jobId - 任务ID
   * @param {string} indexId - 知识库ID
   * @returns {Promise<bailian20231229.GetIndexJobStatusResponse>} - 阿里云百炼服务的响应
   */
  static async getIndexJobStatus(client, workspaceId, jobId, indexId) {
    const headers = {};
    const req = new bailian20231229.GetIndexJobStatusRequest({ jobId, indexId });
    const runtime = new Util.RuntimeOptions({});
    return await client.getIndexJobStatusWithOptions(workspaceId, req, headers, runtime);
  }

  /**
   * 创建知识库
   * @param {string} filePath - 文件本地路径
   * @param {string} workspaceId - 业务空间ID
   * @param {string} name - 知识库名称
   * @returns {Promise<string | null>} - 如果成功，返回知识库ID；否则返回null
   */
  static async createKnowledgeBase(filePath, workspaceId, name) {
    const categoryId = 'default';
    const parser = 'DASHSCOPE_DOCMIND';
    const sourceType = 'DATA_CENTER_FILE';
    const structureType = 'unstructured';
    const sinkType = 'DEFAULT';

    try {
      console.log("步骤1：初始化Client");
      const client = this.createClient();

      console.log("步骤2：准备文件信息");
      const fileName = path.basename(filePath);
      const fileMd5 = await this.calculateMD5(filePath);
      const fileSize = this.getFileSize(filePath);

      console.log("步骤3：向阿里云百炼申请上传租约")
      const leaseRes = await this.applyLease(client, categoryId, fileName, fileMd5, fileSize, workspaceId);
      const leaseId = leaseRes.body.data.fileUploadLeaseId;
      const uploadUrl = leaseRes.body.data.param.url;
      const uploadHeaders = leaseRes.body.data.param.headers;

      console.log("步骤4：上传文件到阿里云百炼")
      await this.uploadFile(uploadUrl, uploadHeaders, filePath);

      console.log("步骤5：将文件添加到阿里云百炼服务器")
      const addRes = await this.addFile(client, leaseId, parser, categoryId, workspaceId);
      const fileId = addRes.body.data.fileId;

      console.log("步骤6：检查阿里云百炼中的文件状态")
      while (true) {
        const descRes = await this.describeFile(client, workspaceId, fileId);
        const status = descRes.body.data.status;
        console.log(`当前文件状态：${status}`);

        if (status === 'INIT') console.log("文件待解析，请稍候...");
        else if (status === 'PARSING') console.log("文件解析中，请稍候...");
        else if (status === 'PARSE_SUCCESS') break;
        else {
          console.error(`未知的文件状态：${status}，请联系技术支持。`);
          return null;
        }
        await this.sleep(5);
      }

      console.log("步骤7：在阿里云百炼中初始化知识库")
      const indexRes = await this.createIndex(client, workspaceId, fileId, name, structureType, sourceType, sinkType);
      const indexId = indexRes.body.data.id;

      console.log("步骤8：向阿里云百炼提交索引任务")
      const submitRes = await this.submitIndex(client, workspaceId, indexId);
      const jobId = submitRes.body.data.id;

      console.log("步骤9：获取阿里云百炼索引任务状态")
      while (true) {
        const jobRes = await this.getIndexJobStatus(client, workspaceId, jobId, indexId);
        const status = jobRes.body.data.status;
        console.log(`当前索引任务状态：${status}`);
        if (status === 'COMPLETED') break;
        await this.sleep(5);
      }
      console.log("阿里云百炼知识库创建成功！");
      return indexId;
    } catch (e) {
      console.error(`发生错误：${e.message}`);
      return null;
    }
  }

  /**
   * 等待指定时间（秒）
   * @param {number} seconds - 等待时间（秒）
   * @returns {Promise<void>}
   */
  static sleep(seconds) {
    return new Promise(resolve => setTimeout(resolve, seconds * 1000));
  }

  static async main(args) {
    if (!this.checkEnvironmentVariables()) {
      console.log("环境变量校验未通过。");
      return;
    }

    const readline = require('readline').createInterface({
      input: process.stdin,
      output: process.stdout
    });

    try {
      const filePath = await new Promise((resolve, reject) => {
        readline.question("请输入您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：", (ans) => {
          ans.trim() ? resolve(ans) : reject(new Error("路径不能为空"));
        });
      });
      const kbName = await new Promise((resolve, reject) => {
        readline.question("请为您的知识库输入一个名称：", (ans) => {
          ans.trim() ? resolve(ans) : reject(new Error("知识库名称不能为空"));
        });
      });
      const workspaceId = process.env.WORKSPACE_ID;

      const result = await KbCreate.createKnowledgeBase(filePath, workspaceId, kbName);
      if (result) console.log(`知识库ID: ${result}`);
      else console.log("知识库创建失败。");
    } catch (err) {
      console.error(err.message);
    } finally {
      readline.close();
    }
  }
}

exports.KbCreate = KbCreate;
KbCreate.main(process.argv.slice(2));
```

## C#

```
// 示例代码仅供参考，请勿在生产环境中直接使用
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

using Newtonsoft.Json;
using Tea;
using Tea.Utils;

namespace AlibabaCloud.SDK.KnowledgeBase
{
    public class KnowledgeBaseCreate
    {
        /// <summary>
        /// 检查并提示设置必要的环境变量。
        /// </summary>
        /// <returns>如果所有必需的环境变量都已设置，返回 true；否则返回 false。</returns>
        public static bool CheckEnvironmentVariables()
        {
            var requiredVars = new Dictionary<string, string>
            {
                { "ALIBABA_CLOUD_ACCESS_KEY_ID", "阿里云访问密钥ID" },
                { "ALIBABA_CLOUD_ACCESS_KEY_SECRET", "阿里云访问密钥密码" },
                { "WORKSPACE_ID", "阿里云百炼业务空间ID" }
            };

            var missingVars = new List<string>();
            foreach (var entry in requiredVars)
            {
                string value = Environment.GetEnvironmentVariable(entry.Key);
                if (string.IsNullOrEmpty(value))
                {
                    missingVars.Add(entry.Key);
                    Console.WriteLine($"错误：请设置 {entry.Key} 环境变量（{entry.Value}）");
                }
            }

            return missingVars.Count == 0;
        }

        /// <summary>
        /// 计算文件的MD5值。
        /// </summary>
        /// <param name="filePath">文件本地路径</param>
        /// <returns>文件的MD5值</returns>
        /// <exception cref="Exception">计算过程中发生错误时抛出异常</exception>
        public static string CalculateMD5(string filePath)
        {
            using (var md5 = MD5.Create())
            {
                using (var stream = new FileStream(filePath, FileMode.Open, FileAccess.Read))
                {
                    byte[] hashBytes = md5.ComputeHash(stream);
                    StringBuilder sb = new StringBuilder();
                    foreach (byte b in hashBytes)
                    {
                        sb.Append(b.ToString("x2"));
                    }
                    return sb.ToString();
                }
            }
        }

        /// <summary>
        /// 获取文件大小（以字节为单位）。
        /// </summary>
        /// <param name="filePath">文件本地路径</param>
        /// <returns>文件大小（以字节为单位）</returns>
        public static string GetFileSize(string filePath)
        {
            var file = new FileInfo(filePath);
            return file.Length.ToString();
        }

        /// <summary>
        /// 初始化客户端（Client）。
        /// </summary>
        /// <returns>配置好的客户端对象</returns>
        /// <exception cref="Exception">初始化过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Client CreateClient()
        {
            var config = new AlibabaCloud.OpenApiClient.Models.Config
            {
                AccessKeyId = Environment.GetEnvironmentVariable("ALIBABA_CLOUD_ACCESS_KEY_ID"),
                AccessKeySecret = Environment.GetEnvironmentVariable("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
            };
            // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址.
            config.Endpoint = "bailian.cn-beijing.aliyuncs.com";
            return new AlibabaCloud.SDK.Bailian20231229.Client(config);
        }

        /// <summary>
        /// 申请文件上传租约。
        /// </summary>
        /// <param name="client">客户端对象</param>
        /// <param name="categoryId">类目ID</param>
        /// <param name="fileName">文件名称</param>
        /// <param name="fileMd5">文件的MD5值</param>
        /// <param name="fileSize">文件大小（以字节为单位）</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <returns>阿里云百炼服务的响应对象</returns>
        /// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.ApplyFileUploadLeaseResponse ApplyLease(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string categoryId,
            string fileName,
            string fileMd5,
            string fileSize,
            string workspaceId)
        {
            var headers = new Dictionary<string, string>() { };
            var applyFileUploadLeaseRequest = new AlibabaCloud.SDK.Bailian20231229.Models.ApplyFileUploadLeaseRequest
            {
                FileName = fileName,
                Md5 = fileMd5,
                SizeInBytes = fileSize
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.ApplyFileUploadLeaseWithOptions(categoryId, workspaceId, applyFileUploadLeaseRequest, headers, runtime);
        }

        /// <summary>
        /// 上传文件到临时存储。
        /// </summary>
        /// <param name="preSignedUrl">上传租约中的 URL</param>
        /// <param name="headers">上传请求的头部</param>
        /// <param name="filePath">文件本地路径</param>
        /// <exception cref="Exception">上传过程中发生错误时抛出异常</exception>
        public static void UploadFile(string preSignedUrl, Dictionary<string, string> headers, string filePath)
        {
            var file = new FileInfo(filePath);
            if (!File.Exists(filePath))
            {
                throw new ArgumentException($"文件不存在或不是普通文件: {filePath}");
            }

            using (var fs = new FileStream(filePath, FileMode.Open, FileAccess.Read))
            {
                var url = new Uri(preSignedUrl);
                var conn = (HttpWebRequest)WebRequest.Create(url);
                conn.Method = "PUT";
                conn.ContentType = headers["Content-Type"];
                conn.Headers.Add("X-bailian-extra", headers["X-bailian-extra"]);

                byte[] buffer = new byte[4096];
                int bytesRead;
                while ((bytesRead = fs.Read(buffer, 0, buffer.Length)) > 0)
                {
                    conn.GetRequestStream().Write(buffer, 0, bytesRead);
                }

                using (var response = (HttpWebResponse)conn.GetResponse())
                {
                    if (response.StatusCode != HttpStatusCode.OK)
                    {
                        throw new Exception($"上传失败: {response.StatusCode}");
                    }
                }
            }
        }

        /// <summary>
        /// 将文件添加到类目中。
        /// </summary>
        /// <param name="client">客户端对象</param>
        /// <param name="leaseId">租约ID</param>
        /// <param name="parser">用于文件的解析器</param>
        /// <param name="categoryId">类目ID</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <returns>阿里云百炼服务的响应对象</returns>
        /// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.AddFileResponse AddFile(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string leaseId,
            string parser,
            string categoryId,
            string workspaceId)
        {
            var headers = new Dictionary<string, string>() { };
            var addFileRequest = new AlibabaCloud.SDK.Bailian20231229.Models.AddFileRequest
            {
                LeaseId = leaseId,
                Parser = parser,
                CategoryId = categoryId
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.AddFileWithOptions(workspaceId, addFileRequest, headers, runtime);
        }

        /// <summary>
        /// 查询文件的基本信息。
        /// </summary>
        /// <param name="client">客户端对象</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="fileId">文件ID</param>
        /// <returns>阿里云百炼服务的响应对象</returns>
        /// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.DescribeFileResponse DescribeFile(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string workspaceId,
            string fileId)
        {
            var headers = new Dictionary<string, string>() { };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.DescribeFileWithOptions(workspaceId, fileId, headers, runtime);
        }

        /// <summary>
        /// 在阿里云百炼服务中创建知识库（初始化）。
        /// </summary>
        /// <param name="client">客户端对象</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="fileId">文件ID</param>
        /// <param name="name">知识库名称</param>
        /// <param name="structureType">知识库的数据类型</param>
        /// <param name="sourceType">应用数据的数据类型，支持类目类型和文件类型</param>
        /// <param name="sinkType">知识库的向量存储类型</param>
        /// <returns>阿里云百炼服务的响应对象</returns>
        /// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.CreateIndexResponse CreateIndex(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string workspaceId,
            string fileId,
            string name,
            string structureType,
            string sourceType,
            string sinkType)
        {
            var headers = new Dictionary<string, string>() { };
            var createIndexRequest = new AlibabaCloud.SDK.Bailian20231229.Models.CreateIndexRequest
            {
                StructureType = structureType,
                Name = name,
                SourceType = sourceType,
                SinkType = sinkType,
                DocumentIds = new List<string> { fileId }
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.CreateIndexWithOptions(workspaceId, createIndexRequest, headers, runtime);
        }

        /// <summary>
        /// 向阿里云百炼服务提交索引任务。
        /// </summary>
        /// <param name="client">客户端对象</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="indexId">知识库ID</param>
        /// <returns>阿里云百炼服务的响应对象</returns>
        /// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.SubmitIndexJobResponse SubmitIndex(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string workspaceId,
            string indexId)
        {
            var headers = new Dictionary<string, string>() { };
            var submitIndexJobRequest = new AlibabaCloud.SDK.Bailian20231229.Models.SubmitIndexJobRequest
            {
                IndexId = indexId
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.SubmitIndexJobWithOptions(workspaceId, submitIndexJobRequest, headers, runtime);
        }

        /// <summary>
        /// 查询索引任务状态。
        /// </summary>
        /// <param name="client">客户端对象</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="jobId">任务ID</param>
        /// <param name="indexId">知识库ID</param>
        /// <returns>阿里云百炼服务的响应对象</returns>
        /// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.GetIndexJobStatusResponse GetIndexJobStatus(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string workspaceId,
            string jobId,
            string indexId)
        {
            var headers = new Dictionary<string, string>() { };
            var getIndexJobStatusRequest = new AlibabaCloud.SDK.Bailian20231229.Models.GetIndexJobStatusRequest
            {
                IndexId = indexId,
                JobId = jobId
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.GetIndexJobStatusWithOptions(workspaceId, getIndexJobStatusRequest, headers, runtime);
        }

        /// <summary>
        /// 使用阿里云百炼服务创建知识库。
        /// </summary>
        /// <param name="filePath">文件本地路径</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="name">知识库名称</param>
        /// <returns>如果成功，返回知识库ID；否则返回 null</returns>
        public static string CreateKnowledgeBase(string filePath, string workspaceId, string name)
        {
            // 设置默认值
            string categoryId = "default";
            string parser = "DASHSCOPE_DOCMIND";
            string sourceType = "DATA_CENTER_FILE";
            string structureType = "unstructured";
            string sinkType = "DEFAULT";

            try
            {
                Console.WriteLine("步骤1：初始化Client");
                AlibabaCloud.SDK.Bailian20231229.Client client = CreateClient();

                Console.WriteLine("步骤2：准备文件信息");
                var fileInfo = new FileInfo(filePath);
                string fileName = fileInfo.Name;
                string fileMd5 = CalculateMD5(filePath);
                string fileSize = GetFileSize(filePath);

                Console.WriteLine("步骤3：向阿里云百炼申请上传租约");
                Bailian20231229.Models.ApplyFileUploadLeaseResponse leaseResponse = ApplyLease(client, categoryId, fileName, fileMd5, fileSize, workspaceId);
                string leaseId = leaseResponse.Body.Data.FileUploadLeaseId;
                string uploadUrl = leaseResponse.Body.Data.Param.Url;
                var uploadHeaders = leaseResponse.Body.Data.Param.Headers;

                Console.WriteLine("步骤4：上传文件到阿里云百炼");
                // 请自行安装Newtonsoft.Json
                var uploadHeadersMap = JsonConvert.DeserializeObject<Dictionary<string, string>>(JsonConvert.SerializeObject(uploadHeaders));
                UploadFile(uploadUrl, uploadHeadersMap, filePath);

                Console.WriteLine("步骤5：将文件添加到阿里云百炼服务器");
                Bailian20231229.Models.AddFileResponse addResponse = AddFile(client, leaseId, parser, categoryId, workspaceId);
                string fileId = addResponse.Body.Data.FileId;

                Console.WriteLine("步骤6：检查阿里云百炼中的文件状态");
                while (true)
                {
                    Bailian20231229.Models.DescribeFileResponse describeResponse = DescribeFile(client, workspaceId, fileId);
                    string status = describeResponse.Body.Data.Status;
                    Console.WriteLine($"当前文件状态：{status}");

                    if (status == "INIT")
                    {
                        Console.WriteLine("文件待解析，请稍候...");
                    }
                    else if (status == "PARSING")
                    {
                        Console.WriteLine("文件解析中，请稍候...");
                    }
                    else if (status == "PARSE_SUCCESS")
                    {
                        Console.WriteLine("文件解析完成！");
                        break;
                    }
                    else
                    {
                        Console.WriteLine($"未知的文件状态：{status}，请联系技术支持。");
                        return null;
                    }
                    Thread.Sleep(5000);
                }

                Console.WriteLine("步骤7：在阿里云百炼中创建知识库");
                Bailian20231229.Models.CreateIndexResponse indexResponse = CreateIndex(client, workspaceId, fileId, name, structureType, sourceType, sinkType);
                string indexId = indexResponse.Body.Data.Id;

                Console.WriteLine("步骤8：向阿里云百炼提交索引任务");
                Bailian20231229.Models.SubmitIndexJobResponse submitResponse = SubmitIndex(client, workspaceId, indexId);
                string jobId = submitResponse.Body.Data.Id;

                Console.WriteLine("步骤9：获取阿里云百炼索引任务状态");
                while (true)
                {
                    Bailian20231229.Models.GetIndexJobStatusResponse getStatusResponse = GetIndexJobStatus(client, workspaceId, jobId, indexId);
                    string status = getStatusResponse.Body.Data.Status;
                    Console.WriteLine($"当前索引任务状态：{status}");

                    if (status == "COMPLETED")
                    {
                        break;
                    }
                    Thread.Sleep(5000);
                }

                Console.WriteLine("阿里云百炼知识库创建成功！");
                return indexId;

            }
            catch (Exception ex)
            {
                Console.WriteLine($"发生错误：{ex.Message}");
                Console.WriteLine("错误详情: " + ex.StackTrace);
                return null;
            }
        }

        /// <summary>
        /// 主函数。
        /// </summary>
        public static void Main(string[] args)
        {
            if (!CheckEnvironmentVariables())
            {
                return;
            }

            Console.Write("请输入您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：");
            string filePath = Console.ReadLine();

            Console.Write("请为您的知识库输入一个名称：");
            string kbName = Console.ReadLine();

            string workspaceId = Environment.GetEnvironmentVariable("WORKSPACE_ID");
            string result = CreateKnowledgeBase(filePath, workspaceId, kbName);
            if (result != null)
            {
                Console.WriteLine($"知识库ID: {result}");
            }
        }
    }
}
```

## Go

```
// 示例代码仅供参考，请勿在生产环境中直接使用
package main

import (
	"bufio"
	"crypto/md5"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"time"

	bailian20231229 "github.com/alibabacloud-go/bailian-20231229/v2/client"
	openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client"
	util "github.com/alibabacloud-go/tea-utils/v2/service"
	"github.com/alibabacloud-go/tea/tea"
	"github.com/go-resty/resty/v2"
)

// CheckEnvironmentVariables 检查并提示设置必要的环境变量。
func CheckEnvironmentVariables() bool {
	// 必要的环境变量及其描述.
	requiredVars := map[string]string{
		"ALIBABA_CLOUD_ACCESS_KEY_ID":     "阿里云访问密钥ID",
		"ALIBABA_CLOUD_ACCESS_KEY_SECRET": "阿里云访问密钥密码",
		"WORKSPACE_ID":                    "阿里云百炼业务空间ID",
	}

	var missingVars []string
	for varName, desc := range requiredVars {
		if os.Getenv(varName) == "" {
			fmt.Printf("错误：请设置 %s 环境变量 (%s)\n", varName, desc)
			missingVars = append(missingVars, varName)
		}
	}

	return len(missingVars) == 0
}

// CalculateMD5 计算文件的MD5值。
//
// 参数:
//   - filePath (string): 文件本地路径。
//
// 返回:
//   - string: 文件的MD5值。
//   - error: 错误信息.
func CalculateMD5(filePath string) (_result string, _err error) {
	file, err := os.Open(filePath)
	if err != nil {
		return "", err
	}
	defer file.Close()

	md5Hash := md5.New()
	_, err = io.Copy(md5Hash, file)
	if err != nil {
		return "", err
	}

	return fmt.Sprintf("%x", md5Hash.Sum(nil)), nil
}

// GetFileSize 获取文件大小（以字节为单位）。
//
// 参数:
//   - filePath (string): 文件本地路径。
//
// 返回:
//   - string: 文件大小（以字节为单位）。
//   - error: 错误信息。
func GetFileSize(filePath string) (_result string, _err error) {
	info, err := os.Stat(filePath)
	if err != nil {
		return "", err
	}
	return fmt.Sprintf("%d", info.Size()), nil
}

// CreateClient 创建并配置客户端（Client）。
//
// 返回:
//   - *client.Bailian20231229Client: 配置好的客户端（Client）。
//   - error: 错误信息。
func CreateClient() (_result *bailian20231229.Client, _err error) {
	config := &openapi.Config{
		AccessKeyId:     tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")),
		AccessKeySecret: tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")),
	}
	// 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
	config.Endpoint = tea.String("bailian.cn-beijing.aliyuncs.com")
	_result = &bailian20231229.Client{}
	_result, _err = bailian20231229.NewClient(config)
	return _result, _err
}

// ApplyLease 从阿里云百炼服务申请文件上传租约。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - categoryId (string): 类目ID。
//   - fileName (string): 文件名称。
//   - fileMD5 (string): 文件的MD5值。
//   - fileSize (string): 文件大小（以字节为单位）。
//   - workspaceId (string): 业务空间ID。
//
// 返回:
//   - *bailian20231229.ApplyFileUploadLeaseResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func ApplyLease(client *bailian20231229.Client, categoryId, fileName, fileMD5 string, fileSize string, workspaceId string) (_result *bailian20231229.ApplyFileUploadLeaseResponse, _err error) {
	headers := make(map[string]*string)
	applyFileUploadLeaseRequest := &bailian20231229.ApplyFileUploadLeaseRequest{
		FileName:    tea.String(fileName),
		Md5:         tea.String(fileMD5),
		SizeInBytes: tea.String(fileSize),
	}
	runtime := &util.RuntimeOptions{}
	return client.ApplyFileUploadLeaseWithOptions(tea.String(categoryId), tea.String(workspaceId), applyFileUploadLeaseRequest, headers, runtime)
}

// UploadFile 将文件上传到阿里云百炼服务。
//
// 参数:
//   - preSignedUrl (string): 上传租约中的 URL。
//   - headers (map[string]string): 上传请求的头部。
//   - filePath (string): 文件本地路径。
func UploadFile(preSignedUrl string, headers map[string]string, filePath string) error {
	file, err := os.Open(filePath)
	if err != nil {
		return err
	}
	defer file.Close()

	body, err := io.ReadAll(file)
	if err != nil {
		return err
	}

	client := resty.New()
	uploadHeaders := map[string]string{
		"X-bailian-extra": headers["X-bailian-extra"],
		"Content-Type":    headers["Content-Type"],
	}

	resp, err := client.R().
		SetHeaders(uploadHeaders).
		SetBody(body).
		Put(preSignedUrl)

	if err != nil {
		return err
	}

	if resp.IsError() {
		return fmt.Errorf("HTTP 错误: %d", resp.StatusCode())
	}

	return nil
}

// AddFile 将文件添加到阿里云百炼服务的指定类目中。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - leaseId (string): 租约ID。
//   - parser (string): 用于文件的解析器。
//   - categoryId (string): 类目ID。
//   - workspaceId (string): 业务空间ID。
//
// 返回:
//   - *bailian20231229.AddFileResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func AddFile(client *bailian20231229.Client, leaseId, parser, categoryId, workspaceId string) (_result *bailian20231229.AddFileResponse, _err error) {
	headers := make(map[string]*string)
	addFileRequest := &bailian20231229.AddFileRequest{
		LeaseId:    tea.String(leaseId),
		Parser:     tea.String(parser),
		CategoryId: tea.String(categoryId),
	}
	runtime := &util.RuntimeOptions{}
	return client.AddFileWithOptions(tea.String(workspaceId), addFileRequest, headers, runtime)
}

// DescribeFile 获取文件的基本信息。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - fileId (string): 文件ID。
//
// 返回:
//   - any: 阿里云百炼服务的响应。
//   - error: 错误信息。
func DescribeFile(client *bailian20231229.Client, workspaceId, fileId string) (_result *bailian20231229.DescribeFileResponse, _err error) {
	headers := make(map[string]*string)
	runtime := &util.RuntimeOptions{}
	return client.DescribeFileWithOptions(tea.String(workspaceId), tea.String(fileId), headers, runtime)
}

// CreateIndex 在阿里云百炼服务中创建知识库（初始化）。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - fileId (string): 文件ID。
//   - name (string): 知识库名称。
//   - structureType (string): 知识库的数据类型。
//   - sourceType (string): 应用数据的数据类型，支持类目类型和文件类型。
//   - sinkType (string): 知识库的向量存储类型。
//
// 返回:
//   - *bailian20231229.CreateIndexResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func CreateIndex(client *bailian20231229.Client, workspaceId, fileId, name, structureType, sourceType, sinkType string) (_result *bailian20231229.CreateIndexResponse, _err error) {
	headers := make(map[string]*string)
	createIndexRequest := &bailian20231229.CreateIndexRequest{
		StructureType: tea.String(structureType),
		Name:          tea.String(name),
		SourceType:    tea.String(sourceType),
		SinkType:      tea.String(sinkType),
		DocumentIds:   []*string{tea.String(fileId)},
	}
	runtime := &util.RuntimeOptions{}
	return client.CreateIndexWithOptions(tea.String(workspaceId), createIndexRequest, headers, runtime)
}

// SubmitIndex 提交索引任务。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - indexId (string): 知识库ID。
//
// 返回:
//   - *bailian20231229.SubmitIndexJobResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func SubmitIndex(client *bailian20231229.Client, workspaceId, indexId string) (_result *bailian20231229.SubmitIndexJobResponse, _err error) {
	headers := make(map[string]*string)
	submitIndexJobRequest := &bailian20231229.SubmitIndexJobRequest{
		IndexId: tea.String(indexId),
	}
	runtime := &util.RuntimeOptions{}
	return client.SubmitIndexJobWithOptions(tea.String(workspaceId), submitIndexJobRequest, headers, runtime)
}

// GetIndexJobStatus 查询索引任务状态。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - jobId (string): 任务ID。
//   - indexId (string): 知识库ID。
//
// 返回:
//   - *bailian20231229.GetIndexJobStatusResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func GetIndexJobStatus(client *bailian20231229.Client, workspaceId, jobId, indexId string) (_result *bailian20231229.GetIndexJobStatusResponse, _err error) {
	headers := make(map[string]*string)
	getIndexJobStatusRequest := &bailian20231229.GetIndexJobStatusRequest{
		JobId:   tea.String(jobId),
		IndexId: tea.String(indexId),
	}
	runtime := &util.RuntimeOptions{}
	return client.GetIndexJobStatusWithOptions(tea.String(workspaceId), getIndexJobStatusRequest, headers, runtime)
}

// CreateKnowledgeBase 使用阿里云百炼服务创建知识库。
//
// 参数:
//   - filePath (string): 文件本地路径。
//   - workspaceId (string): 业务空间ID。
//   - name (string): 知识库名称。
//
// 返回:
//   - string or nil: 如果成功，返回知识库ID；否则返回nil。
//   - error: 错误信息。
func CreateKnowledgeBase(filePath, workspaceId, name string) (_result string, _err error) {
	categoryId := "default"
	parser := "DASHSCOPE_DOCMIND"
	sourceType := "DATA_CENTER_FILE"
	structureType := "unstructured"
	sinkType := "DEFAULT"

	fmt.Println("步骤1：初始化Client")
	client, err := CreateClient()
	if err != nil {
		return "", err
	}

	fmt.Println("步骤2：准备文件信息")
	fileName := filepath.Base(filePath)
	fileMD5, err := CalculateMD5(filePath)
	if err != nil {
		return "", err
	}
	fileSizeStr, err := GetFileSize(filePath)
	if err != nil {
		return "", err
	}

	fmt.Println("步骤3：向阿里云百炼申请上传租约")
	leaseResponse, err := ApplyLease(client, categoryId, fileName, fileMD5, fileSizeStr, workspaceId)
	if err != nil {
		return "", err
	}

	leaseId := tea.StringValue(leaseResponse.Body.Data.FileUploadLeaseId)
	uploadURL := tea.StringValue(leaseResponse.Body.Data.Param.Url)
	uploadHeaders := leaseResponse.Body.Data.Param.Headers

	jsonData, err := json.Marshal(uploadHeaders)
	if err != nil {
		return "", err
	}

	var uploadHeadersMap map[string]string
	err = json.Unmarshal(jsonData, &uploadHeadersMap)
	if err != nil {
		return "", err
	}

	fmt.Println("步骤4：上传文件到阿里云百炼")
	err = UploadFile(uploadURL, uploadHeadersMap, filePath)
	if err != nil {
		return "", err
	}

	fmt.Println("步骤5：将文件添加到阿里云百炼服务器")
	addResponse, err := AddFile(client, leaseId, parser, categoryId, workspaceId)
	if err != nil {
		return "", err
	}
	fileID := tea.StringValue(addResponse.Body.Data.FileId)

	fmt.Println("步骤6：检查阿里云百炼中的文件状态")
	for {
		describeResponse, err := DescribeFile(client, workspaceId, fileID)
		if err != nil {
			return "", err
		}

		status := tea.StringValue(describeResponse.Body.Data.Status)
		fmt.Printf("当前文件状态：%s\n", status)

		if status == "INIT" {
			fmt.Println("文件待解析，请稍候...")
		} else if status == "PARSING" {
			fmt.Println("文件解析中，请稍候...")
		} else if status == "PARSE_SUCCESS" {
			fmt.Println("文件解析完成！")
			break
		} else {
			fmt.Printf("未知的文件状态：%s，请联系技术支持。\n", status)
			return "", fmt.Errorf("unknown document status: %s", status)
		}
		time.Sleep(5 * time.Second)
	}

	fmt.Println("步骤7：在阿里云百炼中初始化知识库")
	indexResponse, err := CreateIndex(client, workspaceId, fileID, name, structureType, sourceType, sinkType)
	if err != nil {
		return "", err
	}
	indexID := tea.StringValue(indexResponse.Body.Data.Id)

	fmt.Println("步骤8：向阿里云百炼提交索引任务")
	submitResponse, err := SubmitIndex(client, workspaceId, indexID)
	if err != nil {
		return "", err
	}
	jobID := tea.StringValue(submitResponse.Body.Data.Id)

	fmt.Println("步骤9：获取阿里云百炼索引任务状态")
	for {
		getIndexJobStatusResponse, err := GetIndexJobStatus(client, workspaceId, jobID, indexID)
		if err != nil {
			return "", err
		}

		status := tea.StringValue(getIndexJobStatusResponse.Body.Data.Status)
		fmt.Printf("当前索引任务状态：%s\n", status)

		if status == "COMPLETED" {
			break
		}
		time.Sleep(5 * time.Second)
	}

	fmt.Println("阿里云百炼知识库创建成功！")
	return indexID, nil
}

// 主函数。
func main() {
	if !CheckEnvironmentVariables() {
		fmt.Println("环境变量校验未通过。")
		return
	}
	// 创建 scanner 用于读取输入
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("请输入您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：")
	filePath, _ := reader.ReadString('\n')
	filePath = strings.TrimSpace(filePath)
	fmt.Print("请为您的知识库输入一个名称：")
	kbName, _ := reader.ReadString('\n')
	kbName = strings.TrimSpace(kbName)
	workspaceID := os.Getenv("WORKSPACE_ID")
	indexID, err := CreateKnowledgeBase(filePath, workspaceID, kbName)
	if err != nil {
		fmt.Printf("发生错误：%v\n", err)
		return
	}
	fmt.Printf("知识库创建成功，ID为：%s\n", indexID)
}
```

## 检索知识库

**重要**

-   在调用本示例之前，请务必完成上述所有[前置步骤](#a4a15bd543can)。子账号调用本示例前需[获取AliyunBailianDataFullAccess策略](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)。
    
-   若您使用了 IDE 或其他辅助开发插件，需将`ALIBABA_CLOUD_ACCESS_KEY_ID`、`ALIBABA_CLOUD_ACCESS_KEY_SECRET`和`WORKSPACE_ID`变量配置到相应的开发环境中。
    

## Python

```
# 示例代码仅供参考，请勿在生产环境中直接使用
import os

from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

def check_environment_variables():
    """检查并提示设置必要的环境变量"""
    required_vars = {
        'ALIBABA_CLOUD_ACCESS_KEY_ID': '阿里云访问密钥ID',
        'ALIBABA_CLOUD_ACCESS_KEY_SECRET': '阿里云访问密钥密码',
        'WORKSPACE_ID': '阿里云百炼业务空间ID'
    }
    missing_vars = []
    for var, description in required_vars.items():
        if not os.environ.get(var):
            missing_vars.append(var)
            print(f"错误：请设置 {var} 环境变量 ({description})")
    
    return len(missing_vars) == 0

# 创建客户端（Client）
def create_client() -> bailian20231229Client:
    """
    创建并配置客户端（Client）。

    返回:
        bailian20231229Client: 配置好的客户端（Client）。
    """
    config = open_api_models.Config(
        access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    )
        # 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
    config.endpoint = 'bailian.cn-beijing.aliyuncs.com'
    return bailian20231229Client(config)

# 检索知识库
def retrieve_index(client, workspace_id, index_id, query):
    """
    在指定的知识库中检索信息。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        query (str): 检索query。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    retrieve_request = bailian_20231229_models.RetrieveRequest(
        index_id=index_id,
        query=query
    )
    runtime = util_models.RuntimeOptions()
    return client.retrieve_with_options(workspace_id, retrieve_request, headers, runtime)

def main():
    """
    使用阿里云百炼服务检索知识库。

    返回:
        str or None: 如果成功，返回检索召回的文本切片；否则返回 None。
    """
    if not check_environment_variables():
        print("环境变量校验未通过。")
        return
    try:
        print("步骤1：创建Client")
        client = create_client()
        print("步骤2：检索知识库")
        index_id = input("请输入知识库ID：")  # 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
        query = input("请输入检索query：")
        workspace_id = os.environ.get('WORKSPACE_ID')
        resp = retrieve_index(client, workspace_id, index_id, query)
        result = UtilClient.to_jsonstring(resp.body)
        print(result)
    except Exception as e:
        print(f"发生错误：{e}")
        return None

if __name__ == '__main__':
    main()
```

## Java

```
// 示例代码仅供参考，请勿在生产环境中直接使用
import com.aliyun.bailian20231229.models.RetrieveRequest;
import com.aliyun.bailian20231229.models.RetrieveResponse;
import com.aliyun.teautil.models.RuntimeOptions;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.*;

public class KnowledgeBaseRetrieve {

    /**
     * 检查并提示设置必要的环境变量。
     *
     * @return true 如果所有必需的环境变量都已设置，否则 false
     */
    public static boolean checkEnvironmentVariables() {
        Map<String, String> requiredVars = new HashMap<>();
        requiredVars.put("ALIBABA_CLOUD_ACCESS_KEY_ID", "阿里云访问密钥ID");
        requiredVars.put("ALIBABA_CLOUD_ACCESS_KEY_SECRET", "阿里云访问密钥密码");
        requiredVars.put("WORKSPACE_ID", "阿里云百炼业务空间ID");

        List<String> missingVars = new ArrayList<>();
        for (Map.Entry<String, String> entry : requiredVars.entrySet()) {
            String value = System.getenv(entry.getKey());
            if (value == null || value.isEmpty()) {
                missingVars.add(entry.getKey());
                System.out.println("错误：请设置 " + entry.getKey() + " 环境变量 (" + entry.getValue() + ")");
            }
        }

        return missingVars.isEmpty();
    }

    /**
     * 初始化客户端（Client）。
     *
     * @return 配置好的客户端对象
     */
    public static com.aliyun.bailian20231229.Client createClient() throws Exception {
        com.aliyun.teaopenapi.models.Config config = new com.aliyun.teaopenapi.models.Config()
                .setAccessKeyId(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"))
                .setAccessKeySecret(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"));
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
        config.endpoint = "bailian.cn-beijing.aliyuncs.com";
        return new com.aliyun.bailian20231229.Client(config);
    }

    /**
     * 在指定的知识库中检索信息。
     *
     * @param client         客户端对象（bailian20231229Client）
     * @param workspaceId    业务空间ID
     * @param indexId        知识库ID
     * @param query          检索查询语句
     * @return               阿里云百炼服务的响应
     */
    public static RetrieveResponse retrieveIndex(com.aliyun.bailian20231229.Client client, String workspaceId, String indexId, String query) throws Exception {
        RetrieveRequest retrieveRequest = new RetrieveRequest();
        retrieveRequest.setIndexId(indexId);
        retrieveRequest.setQuery(query);
        RuntimeOptions runtime = new RuntimeOptions();
        return client.retrieveWithOptions(workspaceId, retrieveRequest, null, runtime);
    }

    /**
     * 使用阿里云百炼服务检索知识库。
     */
    public static void main(String[] args) {
        if (!checkEnvironmentVariables()) {
            System.out.println("环境变量校验未通过。");
            return;
        }

        try {
            // 步骤1：初始化客户端（Client）
            System.out.println("步骤1：创建Client");
            com.aliyun.bailian20231229.Client client = createClient();

            // 步骤2：检索知识库
            System.out.println("步骤2：检索知识库");
            Scanner scanner = new Scanner(System.in);
            System.out.print("请输入知识库ID："); // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
            String indexId = scanner.nextLine();
            System.out.print("请输入检索query：");
            String query = scanner.nextLine();
            String workspaceId = System.getenv("WORKSPACE_ID");
            RetrieveResponse resp = retrieveIndex(client, workspaceId, indexId, query);

            // 请自行安装jackson-databind。将响应体responsebody转换为 JSON 字符串
            ObjectMapper mapper = new ObjectMapper();
            String result = mapper.writeValueAsString(resp.getBody());
            System.out.println(result);
        } catch (Exception e) {
            System.out.println("发生错误：" + e.getMessage());
        }
    }
}
```

## PHP

```
<?php
// 示例代码仅供参考，请勿在生产环境中直接使用
namespace AlibabaCloud\SDK\Sample;

use AlibabaCloud\Dara\Models\RuntimeOptions;
use AlibabaCloud\SDK\Bailian\V20231229\Bailian;
use \Exception;

use Darabonba\OpenApi\Models\Config;
use AlibabaCloud\SDK\Bailian\V20231229\Models\RetrieveRequest;

class KnowledgeBaseRetrieve {

    /**
    * 检查并提示设置必要的环境变量。
    *
    * @return bool 返回 true 如果所有必需的环境变量都已设置，否则 false。
    */
    public static function checkEnvironmentVariables() {
        $requiredVars = [
            'ALIBABA_CLOUD_ACCESS_KEY_ID' => '阿里云访问密钥ID',
            'ALIBABA_CLOUD_ACCESS_KEY_SECRET' => '阿里云访问密钥密码',
            'WORKSPACE_ID' => '阿里云百炼业务空间ID'
        ];
        $missingVars = [];
        foreach ($requiredVars as $var => $description) {
            if (!getenv($var)) {
                $missingVars[] = $var;
                echo "错误：请设置 $var 环境变量 ($description)\n";
            }
        }
        return count($missingVars) === 0;
    }

    /**
     * 初始化客户端（Client）。
     *
     * @return Bailian 配置好的客户端对象（Client）。
     */
    public static function createClient(){
        $config = new Config([
            "accessKeyId" => getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"), 
            "accessKeySecret" => getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        ]);
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
        $config->endpoint = 'bailian.cn-beijing.aliyuncs.com';
        return new Bailian($config);
    }

     /**
     * 在指定的知识库中检索信息。
     *
     * @param Bailian $client 客户端对象（Client）。
     * @param string $workspaceId 业务空间ID
     * @param string $indexId 知识库ID
     * @param string $query 检索查询语句
     * @return RetrieveResponse 阿里云百炼服务的响应
     * @throws Exception
     */
    public static function retrieveIndex($client, $workspaceId, $indexId, $query) {
        $headers = [];
        $retrieveRequest = new RetrieveRequest([
            "query" => $query,
            "indexId" => $indexId
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->retrieveWithOptions($workspaceId, $retrieveRequest, $headers, $runtime);
    }

    /**
     * 使用阿里云百炼服务检索知识库。
     */
    public static function main($args){
        if (!self::checkEnvironmentVariables()) {
            echo "环境变量校验未通过。\n";
            return;
        }

        try {
            // 步骤1：创建Client
            echo "步骤1：创建Client\n";
            $client = self::createClient();

            // 步骤2：检索知识库
            echo "步骤2：检索知识库\n";
            $indexId = readline("请输入知识库ID："); // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
            $query = readline("请输入检索query："); 
            $workspaceId = getenv("WORKSPACE_ID");
            // 调用检索方法
            $resp = self::retrieveIndex($client, $workspaceId, $indexId, $query);
            // 将响应体responsebody转换为 JSON 字符串
            $result = json_encode($resp->body, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
            echo $result . "\n";
        } catch (Exception $e) {
            echo "发生错误：" . $e->getMessage() . "\n";
        }
    }
}
// 假定autoload.php位于当前代码文件所在目录的上一级目录中，请根据您的项目实际结构调整。
$path = __DIR__ . \DIRECTORY_SEPARATOR . '..' . \DIRECTORY_SEPARATOR . 'vendor' . \DIRECTORY_SEPARATOR . 'autoload.php';
if (file_exists($path)) {
    require_once $path;
}
KnowledgeBaseRetrieve::main(array_slice($argv, 1));
```

## Node.js

```
// 示例代码仅供参考，请勿在生产环境中直接使用
'use strict';

const bailian20231229 = require('@alicloud/bailian20231229');
const OpenApi = require('@alicloud/openapi-client');
const Util = require('@alicloud/tea-util');
const Tea = require('@alicloud/tea-typescript');

class KbRetrieve {

    /**
     * 检查并提示设置必要的环境变量
     * @returns {boolean} - 如果所有必需的环境变量都已设置，返回 true；否则返回 false
     */
    static checkEnvironmentVariables() {
        const requiredVars = {
            'ALIBABA_CLOUD_ACCESS_KEY_ID': '阿里云访问密钥ID',
            'ALIBABA_CLOUD_ACCESS_KEY_SECRET': '阿里云访问密钥密码',
            'WORKSPACE_ID': '阿里云百炼业务空间ID'
        };

        const missing = [];
        for (const [varName, desc] of Object.entries(requiredVars)) {
            if (!process.env[varName]) {
                console.error(`错误：请设置 ${varName} 环境变量 (${desc})`);
                missing.push(varName);
            }
        }
        return missing.length === 0;
    }

    /**
     * 创建并配置客户端（Client）
     * @return Client
     * @throws Exception
     */
    static createClient() {
        const config = new OpenApi.Config({
            accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
            accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET
        });
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址
        config.endpoint = 'bailian.cn-beijing.aliyuncs.com';
        return new bailian20231229.default(config);
    }

    /**
     * 在指定的知识库中检索信息
     * @param {bailian20231229.Client} client 客户端（Client）
     * @param {string} workspaceId 业务空间ID
     * @param {string} indexId 知识库ID
     * @param {string} query 检索query
     * @returns {Promise<bailian20231229.RetrieveResponse>} 阿里云百炼服务的响应
     */
    static async retrieveIndex(client, workspaceId, indexId, query) {
        const headers = {};
        const req = new bailian20231229.RetrieveRequest({
            indexId,
            query
        });
        const runtime = new Util.RuntimeOptions({});
        return await client.retrieveWithOptions(workspaceId, req, headers, runtime);
    }

    /**
     * 使用阿里云百炼服务检索知识库
     */
    static async main(args) {
        if (!this.checkEnvironmentVariables()) {
            console.log("环境变量校验未通过。");
            return;
        }

        const readline = require('readline').createInterface({
            input: process.stdin,
            output: process.stdout
        });

        try {
            console.log("步骤1：创建Client")
            const client = this.createClient();
            
            console.log("步骤2：检索知识库")
            const indexId = await new Promise((resolve, reject) => {
                // 知识库ID即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取
                readline.question("请输入知识库ID：", (ans) => {
                    ans.trim() ? resolve(ans) : reject(new Error("知识库ID不能为空"));
                });
            });
            const query = await new Promise((resolve, reject) => {
                readline.question("请输入检索query：", (ans) => {
                    ans.trim() ? resolve(ans) : reject(new Error("检索query不能为空"));
                });
            });
            const workspaceId = process.env.WORKSPACE_ID;
            const resp = await this.retrieveIndex(client, workspaceId, indexId, query);
            const result = JSON.stringify(resp.body);
            console.log(result);
        } catch (err) {
            console.error(`发生错误：${err.message}`);
            return;
        } finally {
            readline.close();
        }
    }
}

exports.KbRetrieve = KbRetrieve;
KbRetrieve.main(process.argv.slice(2));
```

## C#

```
// 示例代码仅供参考，请勿在生产环境中直接使用
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Text;

using Newtonsoft.Json;
using Tea;
using Tea.Utils;

namespace AlibabaCloud.SDK.KnowledgeBase
{
    public class KnowledgeBaseRetrieve
    {
        /// <summary>
        /// 检查并提示设置必要的环境变量。
        /// </summary>
        /// <returns>如果所有必需的环境变量都已设置，返回 true；否则返回 false。</returns>
        public static bool CheckEnvironmentVariables()
        {
            var requiredVars = new Dictionary<string, string>
            {
                { "ALIBABA_CLOUD_ACCESS_KEY_ID", "阿里云访问密钥ID" },
                { "ALIBABA_CLOUD_ACCESS_KEY_SECRET", "阿里云访问密钥密码" },
                { "WORKSPACE_ID", "阿里云百炼业务空间ID" }
            };

            var missingVars = new List<string>();
            foreach (var entry in requiredVars)
            {
                string value = Environment.GetEnvironmentVariable(entry.Key);
                if (string.IsNullOrEmpty(value))
                {
                    missingVars.Add(entry.Key);
                    Console.WriteLine($"错误：请设置 {entry.Key} 环境变量（{entry.Value}）");
                }
            }

            return missingVars.Count == 0;
        }

        /// <summary>
        /// 初始化客户端（Client）。
        /// </summary>
        /// <returns>配置好的客户端对象</returns>
        /// <exception cref="Exception">初始化过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Client CreateClient()
        {
            var config = new AlibabaCloud.OpenApiClient.Models.Config
            {
                AccessKeyId = Environment.GetEnvironmentVariable("ALIBABA_CLOUD_ACCESS_KEY_ID"),
                AccessKeySecret = Environment.GetEnvironmentVariable("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
            };
            // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
            config.Endpoint = "bailian.cn-beijing.aliyuncs.com";
            return new AlibabaCloud.SDK.Bailian20231229.Client(config);
        }

        /// <summary>
        /// 在指定的知识库中检索信息。
        /// </summary>
        /// <param name="client">客户端对象（bailian20231229Client）</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="indexId">知识库ID</param>
        /// <param name="query">检索查询语句</param>
        /// <returns>阿里云百炼服务的响应</returns>
        /// <exception cref="Exception">如果调用失败</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.RetrieveResponse RetrieveIndex(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string workspaceId,
            string indexId,
            string query)
        {
            var headers = new Dictionary<string, string>() { };
            var retrieveRequest = new AlibabaCloud.SDK.Bailian20231229.Models.RetrieveRequest
            {
                IndexId = indexId,
                Query = query
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.RetrieveWithOptions(workspaceId, retrieveRequest, headers, runtime);
        }

        /// <summary>
        /// 使用阿里云百炼服务检索知识库。
        /// </summary>
        public static void Main(string[] args)
        {
            if (!CheckEnvironmentVariables())
            {
                Console.WriteLine("环境变量校验未通过。");
                return;
            }

            try
            {
                // 步骤1：初始化客户端（Client）
                Console.WriteLine("步骤1：创建Client");
                Bailian20231229.Client client = CreateClient();

                // 步骤2：检索知识库
                Console.WriteLine("步骤2：检索知识库");
                Console.Write("请输入知识库ID："); // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
                string indexId = Console.ReadLine();
                Console.Write("请输入检索query：");
                string query = Console.ReadLine();
                string workspaceId = Environment.GetEnvironmentVariable("WORKSPACE_ID");
                Bailian20231229.Models.RetrieveResponse resp = RetrieveIndex(client, workspaceId, indexId, query);

                // 请自行安装Newtonsoft.Json。将响应体responsebody转换为 JSON 字符串
                var mapper = new JsonSerializerSettings { Formatting = Formatting.Indented };
                string result = JsonConvert.SerializeObject(resp.Body, mapper);
                Console.WriteLine(result);
            }
            catch (Exception e)
            {
                Console.WriteLine("发生错误：" + e.Message);
            }
        }
    }
}
```

## Go

```
// 示例代码仅供参考，请勿在生产环境中直接使用
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	bailian20231229 "github.com/alibabacloud-go/bailian-20231229/v2/client"
	openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client"
	util "github.com/alibabacloud-go/tea-utils/v2/service"
	"github.com/alibabacloud-go/tea/tea"
)

// checkEnvironmentVariables 检查并提示设置必要的环境变量。
func checkEnvironmentVariables() bool {
	// 必要的环境变量及其描述。
	requiredVars := map[string]string{
		"ALIBABA_CLOUD_ACCESS_KEY_ID":     "阿里云访问密钥ID",
		"ALIBABA_CLOUD_ACCESS_KEY_SECRET": "阿里云访问密钥密码",
		"WORKSPACE_ID":                    "阿里云百炼业务空间ID",
	}

	var missingVars []string
	for varName, desc := range requiredVars {
		if os.Getenv(varName) == "" {
			fmt.Printf("错误：请设置 %s 环境变量 (%s)\n", varName, desc)
			missingVars = append(missingVars, varName)
		}
	}

	return len(missingVars) == 0
}

// createClient 创建并配置客户端（Client）。
//
// 返回:
//   - *client.Bailian20231229Client: 配置好的客户端（Client）。
//   - error: 错误信息。
func createClient() (_result *bailian20231229.Client, _err error) {
	config := &openapi.Config{
		AccessKeyId:     tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")),
		AccessKeySecret: tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")),
	}
	// 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
	config.Endpoint = tea.String("bailian.cn-beijing.aliyuncs.com")
	_result = &bailian20231229.Client{}
	_result, _err = bailian20231229.NewClient(config)
	return _result, _err
}

// retrieveIndex 在指定的知识库中检索信息。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - indexId（string）: 知识库ID。
//   - query（string）: 检索查询语句
//
// 返回:
//   - *bailian20231229.RetrieveResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func retrieveIndex(client *bailian20231229.Client, workspaceId, indexId, query string) (*bailian20231229.RetrieveResponse, error) {
	headers := make(map[string]*string)
	request := &bailian20231229.RetrieveRequest{
		IndexId: tea.String(indexId),
		Query:   tea.String(query),
	}
	runtime := &util.RuntimeOptions{}
	return client.RetrieveWithOptions(tea.String(workspaceId), request, headers, runtime)
}

// 主函数。
func main() {
	if !checkEnvironmentVariables() {
		fmt.Println("环境变量校验未通过。")
		return
	}

	// 步骤1：初始化客户端（Client）
	fmt.Println("步骤1：创建Client")
	client, err := createClient()
	if err != nil {
		fmt.Println("创建客户端失败:", err)
		return
	}

	// 步骤2：检索知识库
	fmt.Println("步骤2：检索知识库")
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("请输入知识库ID：") // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
	indexId, _ := reader.ReadString('\n')
	indexId = strings.TrimSpace(indexId)
	fmt.Print("请输入检索query：")
	query, _ := reader.ReadString('\n')
	query = strings.TrimSpace(query)
	workspaceId := os.Getenv("WORKSPACE_ID")
	resp, err := retrieveIndex(client, workspaceId, indexId, query)
	if err != nil {
		fmt.Printf("检索失败：%v\n", err)
		return
	}
        fmt.Println(resp.Body)
}
```

## 更新知识库

**重要**

-   在调用本示例之前，请务必完成上述所有[前置步骤](#a4a15bd543can)。子账号调用本示例前需[获取AliyunBailianDataFullAccess策略](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)。
    
-   若您使用了 IDE 或其他辅助开发插件，需将`ALIBABA_CLOUD_ACCESS_KEY_ID`、`ALIBABA_CLOUD_ACCESS_KEY_SECRET`和`WORKSPACE_ID`变量配置到相应的开发环境中。
    

## Python

```
# 示例代码仅供参考，请勿在生产环境中直接使用
import hashlib
import os
import time

import requests
from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

def check_environment_variables():
    """检查并提示设置必要的环境变量"""
    required_vars = {
        'ALIBABA_CLOUD_ACCESS_KEY_ID': '阿里云访问密钥ID',
        'ALIBABA_CLOUD_ACCESS_KEY_SECRET': '阿里云访问密钥密码',
        'WORKSPACE_ID': '阿里云百炼业务空间ID'
    }
    missing_vars = []
    for var, description in required_vars.items():
        if not os.environ.get(var):
            missing_vars.append(var)
            print(f"错误：请设置 {var} 环境变量 ({description})")
    
    return len(missing_vars) == 0

# 创建客户端（Client）
def create_client() -> bailian20231229Client:
    """
    创建并配置客户端（Client）。

    返回:
        bailian20231229Client: 配置好的客户端（Client）。
    """
    config = open_api_models.Config(
        access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    )
    # 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
    config.endpoint = 'bailian.cn-beijing.aliyuncs.com'
    return bailian20231229Client(config)

def calculate_md5(file_path: str) -> str:
    """
    计算文件的MD5值。

    参数:
        file_path (str): 文件本地路径。

    返回:
        str: 文件的MD5值。
    """
    md5_hash = hashlib.md5()

    # 以二进制形式读取文件
    with open(file_path, "rb") as f:
        # 按块读取文件，避免大文件占用过多内存
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)

    return md5_hash.hexdigest()

def get_file_size(file_path: str) -> int:
    """
    获取文件大小（以字节为单位）。
    参数:
        file_path (str): 文件本地路径。
    返回:
        int: 文件大小（以字节为单位）。
    """
    return os.path.getsize(file_path)

# 申请文件上传租约
def apply_lease(client, category_id, file_name, file_md5, file_size, workspace_id):
    """
    从阿里云百炼服务申请文件上传租约。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        category_id (str): 类目ID。
        file_name (str): 文件名称。
        file_md5 (str): 文件的MD5值。
        file_size (int): 文件大小（以字节为单位）。
        workspace_id (str): 业务空间ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    request = bailian_20231229_models.ApplyFileUploadLeaseRequest(
        file_name=file_name,
        md_5=file_md5,
        size_in_bytes=file_size,
    )
    runtime = util_models.RuntimeOptions()
    return client.apply_file_upload_lease_with_options(category_id, workspace_id, request, headers, runtime)

# 上传文件到临时存储
def upload_file(pre_signed_url, headers, file_path):
    """
    将文件上传到阿里云百炼服务。
    参数:
        pre_signed_url (str): 上传租约中的 URL。
        headers (dict): 上传请求的头部。
        file_path (str): 文件本地路径。
    """
    with open(file_path, 'rb') as f:
        file_content = f.read()
    upload_headers = {
        "X-bailian-extra": headers["X-bailian-extra"],
        "Content-Type": headers["Content-Type"]
    }
    response = requests.put(pre_signed_url, data=file_content, headers=upload_headers)
    response.raise_for_status()

# 添加文件到类目中
def add_file(client: bailian20231229Client, lease_id: str, parser: str, category_id: str, workspace_id: str):
    """
    将文件添加到阿里云百炼服务的指定类目中。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        lease_id (str): 租约ID。
        parser (str): 用于文件的解析器。
        category_id (str): 类目ID。
        workspace_id (str): 业务空间ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    request = bailian_20231229_models.AddFileRequest(
        lease_id=lease_id,
        parser=parser,
        category_id=category_id,
    )
    runtime = util_models.RuntimeOptions()
    return client.add_file_with_options(workspace_id, request, headers, runtime)

# 查询文件的解析状态
def describe_file(client, workspace_id, file_id):
    """
    获取文件的基本信息。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        file_id (str): 文件ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    runtime = util_models.RuntimeOptions()
    return client.describe_file_with_options(workspace_id, file_id, headers, runtime)

# 提交追加文件任务
def submit_index_add_documents_job(client, workspace_id, index_id, file_id, source_type):
    """
    向一个文档搜索类知识库追加导入已解析的文件。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        file_id (str): 文件ID。
        source_type(str): 数据类型。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    submit_index_add_documents_job_request = bailian_20231229_models.SubmitIndexAddDocumentsJobRequest(
        index_id=index_id,
        document_ids=[file_id],
        source_type=source_type
    )
    runtime = util_models.RuntimeOptions()
    return client.submit_index_add_documents_job_with_options(workspace_id, submit_index_add_documents_job_request,
                                                              headers, runtime)

# 等待追加任务完成
def get_index_job_status(client, workspace_id, job_id, index_id):
    """
    查询索引任务状态。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        job_id (str): 任务ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    get_index_job_status_request = bailian_20231229_models.GetIndexJobStatusRequest(
        index_id=index_id,
        job_id=job_id
    )
    runtime = util_models.RuntimeOptions()
    return client.get_index_job_status_with_options(workspace_id, get_index_job_status_request, headers, runtime)

# 删除旧文件
def delete_index_document(client, workspace_id, index_id, file_id):
    """
    从指定的文档搜索类知识库中永久删除一个或多个文件。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        file_id (str): 文件ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    delete_index_document_request = bailian_20231229_models.DeleteIndexDocumentRequest(
        index_id=index_id,
        document_ids=[file_id]
    )
    runtime = util_models.RuntimeOptions()
    return client.delete_index_document_with_options(workspace_id, delete_index_document_request, headers, runtime)

def update_knowledge_base(
        file_path: str,
        workspace_id: str,
        index_id: str,
        old_file_id: str
):
    """
    使用阿里云百炼服务更新知识库。
    参数:
        file_path (str): 文件（更新后的）的实际本地路径。
        workspace_id (str): 业务空间ID。
        index_id (str): 需要更新的知识库ID。
        old_file_id (str): 需要更新的文件的FileID。
    返回:
        str or None: 如果成功，返回知识库ID；否则返回None。
    """
    # 设置默认值
    category_id = 'default'
    parser = 'DASHSCOPE_DOCMIND'
    source_type = 'DATA_CENTER_FILE'
    try:
        # 步骤1：创建客户端（Client）
        print("步骤1：创建Client")
        client = create_client()
        # 步骤2：准备文件信息
        print("步骤2：准备文件信息")
        file_name = os.path.basename(file_path)
        file_md5 = calculate_md5(file_path)
        file_size = get_file_size(file_path)
        # 步骤3：申请上传租约
        print("步骤3：向阿里云百炼申请上传租约")
        lease_response = apply_lease(client, category_id, file_name, file_md5, file_size, workspace_id)
        lease_id = lease_response.body.data.file_upload_lease_id
        upload_url = lease_response.body.data.param.url
        upload_headers = lease_response.body.data.param.headers
        # 步骤4：上传文件到临时存储
        print("步骤4：上传文件到临时存储")
        upload_file(upload_url, upload_headers, file_path)
        # 步骤5：添加文件到类目中
        print("步骤5：添加文件到类目中")
        add_response = add_file(client, lease_id, parser, category_id, workspace_id)
        file_id = add_response.body.data.file_id
        # 步骤6：检查文件状态
        print("步骤6：检查阿里云百炼中的文件状态")
        while True:
            describe_response = describe_file(client, workspace_id, file_id)
            status = describe_response.body.data.status
            print(f"当前文件状态：{status}")
            if status == 'INIT':
                print("文件待解析，请稍候...")
            elif status == 'PARSING':
                print("文件解析中，请稍候...")
            elif status == 'PARSE_SUCCESS':
                print("文件解析完成！")
                break
            else:
                print(f"未知的文件状态：{status}，请联系技术支持。")
                return None
            time.sleep(5)
        # 步骤7：提交追加文件任务
        print("步骤7：提交追加文件任务")
        index_add_response = submit_index_add_documents_job(client, workspace_id, index_id, file_id, source_type)
        job_id = index_add_response.body.data.id
        # 步骤8：获取索引任务状态
        print("步骤8：等待追加任务完成")
        while True:
            get_index_job_status_response = get_index_job_status(client, workspace_id, job_id, index_id)
            status = get_index_job_status_response.body.data.status
            print(f"当前索引任务状态：{status}")
            if status == 'COMPLETED':
                break
            time.sleep(5)
        print("步骤9：删除旧文件")
        delete_index_document(client, workspace_id, index_id, old_file_id)
        print("阿里云百炼知识库更新成功！")
        return index_id
    except Exception as e:
        print(f"发生错误：{e}")
        return None

def main():
    if not check_environment_variables():
        print("环境变量校验未通过。")
        return
    file_path = input("请输入您需要上传文件（更新后的）的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：")
    index_id = input("请输入需要更新的知识库ID：")  # 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
    old_file_id = input("请输入需要更新的文件的 FileID：")  # 即 AddFile 接口返回的 FileId。您也可以在阿里云百炼控制台的应用数据页面，单击文件名称旁的 ID 图标获取。
    workspace_id = os.environ.get('WORKSPACE_ID')
    update_knowledge_base(file_path, workspace_id, index_id, old_file_id)

if __name__ == '__main__':
    main()
```

## Java

```
// 示例代码仅供参考，请勿在生产环境中直接使用
import com.aliyun.bailian20231229.models.*;
import com.aliyun.teautil.models.RuntimeOptions;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.io.FileInputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.file.Paths;
import java.security.MessageDigest;
import java.util.*;

public class KnowledgeBaseUpdate {

    /**
     * 检查并提示设置必要的环境变量。
     *
     * @return true 如果所有必需的环境变量都已设置，否则 false
     */
    public static boolean checkEnvironmentVariables() {
        Map<String, String> requiredVars = new HashMap<>();
        requiredVars.put("ALIBABA_CLOUD_ACCESS_KEY_ID", "阿里云访问密钥ID");
        requiredVars.put("ALIBABA_CLOUD_ACCESS_KEY_SECRET", "阿里云访问密钥密码");
        requiredVars.put("WORKSPACE_ID", "阿里云百炼业务空间ID");

        List<String> missingVars = new ArrayList<>();
        for (Map.Entry<String, String> entry : requiredVars.entrySet()) {
            String value = System.getenv(entry.getKey());
            if (value == null || value.isEmpty()) {
                missingVars.add(entry.getKey());
                System.out.println("错误：请设置 " + entry.getKey() + " 环境变量 (" + entry.getValue() + ")");
            }
        }

        return missingVars.isEmpty();
    }

    /**
     * 创建并配置客户端（Client）
     *
     * @return 配置好的客户端（Client）
     */
    public static com.aliyun.bailian20231229.Client createClient() throws Exception {
        com.aliyun.teaopenapi.models.Config config = new com.aliyun.teaopenapi.models.Config()
                .setAccessKeyId(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"))
                .setAccessKeySecret(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"));
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
        config.endpoint = "bailian.cn-beijing.aliyuncs.com";
        return new com.aliyun.bailian20231229.Client(config);
    }

    /**
     * 计算文件的MD5值
     *
     * @param filePath 文件本地路径
     * @return 文件的MD5值
     */
    public static String calculateMD5(String filePath) throws Exception {
        MessageDigest md = MessageDigest.getInstance("MD5");
        try (FileInputStream fis = new FileInputStream(filePath)) {
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                md.update(buffer, 0, bytesRead);
            }
        }
        StringBuilder sb = new StringBuilder();
        for (byte b : md.digest()) {
            sb.append(String.format("%02x", b & 0xff));
        }
        return sb.toString();
    }

    /**
     * 获取文件大小（以字节为单位）
     *
     * @param filePath 文件本地路径
     * @return 文件大小（以字节为单位）
     */
    public static String getFileSize(String filePath) {
        File file = new File(filePath);
        long fileSize = file.length();
        return String.valueOf(fileSize);
    }

    /**
     * 申请文件上传租约。
     *
     * @param client      客户端对象
     * @param categoryId  类目ID
     * @param fileName    文件名称
     * @param fileMd5     文件的MD5值
     * @param fileSize    文件大小（以字节为单位）
     * @param workspaceId 业务空间ID
     * @return 阿里云百炼服务的响应对象
     */
    public static ApplyFileUploadLeaseResponse applyLease(com.aliyun.bailian20231229.Client client, String categoryId, String fileName, String fileMd5, String fileSize, String workspaceId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.bailian20231229.models.ApplyFileUploadLeaseRequest applyFileUploadLeaseRequest = new com.aliyun.bailian20231229.models.ApplyFileUploadLeaseRequest();
        applyFileUploadLeaseRequest.setFileName(fileName);
        applyFileUploadLeaseRequest.setMd5(fileMd5);
        applyFileUploadLeaseRequest.setSizeInBytes(fileSize);
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        ApplyFileUploadLeaseResponse applyFileUploadLeaseResponse = null;
        applyFileUploadLeaseResponse = client.applyFileUploadLeaseWithOptions(categoryId, workspaceId, applyFileUploadLeaseRequest, headers, runtime);
        return applyFileUploadLeaseResponse;
    }

    /**
     * 上传文件到临时存储。
     *
     * @param preSignedUrl 上传租约中的 URL
     * @param headers      上传请求的头部
     * @param filePath     文件本地路径
     * @throws Exception 如果上传过程中发生错误
     */
    public static void uploadFile(String preSignedUrl, Map<String, String> headers, String filePath) throws Exception {
        File file = new File(filePath);
        if (!file.exists() || !file.isFile()) {
            throw new IllegalArgumentException("文件不存在或不是普通文件: " + filePath);
        }

        try (FileInputStream fis = new FileInputStream(file)) {
            URL url = new URL(preSignedUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("PUT");
            conn.setDoOutput(true);

            // 设置上传请求头
            conn.setRequestProperty("X-bailian-extra", headers.get("X-bailian-extra"));
            conn.setRequestProperty("Content-Type", headers.get("Content-Type"));

            // 分块读取并上传文件
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                conn.getOutputStream().write(buffer, 0, bytesRead);
            }

            int responseCode = conn.getResponseCode();
            if (responseCode != 200) {
                throw new RuntimeException("上传失败: " + responseCode);
            }
        }
    }

    /**
     * 将文件添加到类目中。
     *
     * @param client      客户端对象
     * @param leaseId     租约ID
     * @param parser      用于文件的解析器
     * @param categoryId  类目ID
     * @param workspaceId 业务空间ID
     * @return 阿里云百炼服务的响应对象
     */
    public static AddFileResponse addFile(com.aliyun.bailian20231229.Client client, String leaseId, String parser, String categoryId, String workspaceId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.bailian20231229.models.AddFileRequest addFileRequest = new com.aliyun.bailian20231229.models.AddFileRequest();
        addFileRequest.setLeaseId(leaseId);
        addFileRequest.setParser(parser);
        addFileRequest.setCategoryId(categoryId);
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return client.addFileWithOptions(workspaceId, addFileRequest, headers, runtime);
    }

    /**
     * 查询文件的基本信息。
     *
     * @param client      客户端对象
     * @param workspaceId 业务空间ID
     * @param fileId      文件ID
     * @return 阿里云百炼服务的响应对象
     */
    public static DescribeFileResponse describeFile(com.aliyun.bailian20231229.Client client, String workspaceId, String fileId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return client.describeFileWithOptions(workspaceId, fileId, headers, runtime);
    }

    /**
     * 向一个文档搜索类知识库追加导入已解析的文件
     *
     * @param client      客户端（Client）
     * @param workspaceId 业务空间ID
     * @param indexId     知识库ID
     * @param fileId      文件ID
     * @param sourceType  数据类型
     * @return 阿里云百炼服务的响应
     */
    public static SubmitIndexAddDocumentsJobResponse submitIndexAddDocumentsJob(com.aliyun.bailian20231229.Client client, String workspaceId, String indexId, String fileId, String sourceType) throws Exception {
        Map<String, String> headers = new HashMap<>();
        SubmitIndexAddDocumentsJobRequest submitIndexAddDocumentsJobRequest = new SubmitIndexAddDocumentsJobRequest();
        submitIndexAddDocumentsJobRequest.setIndexId(indexId);
        submitIndexAddDocumentsJobRequest.setDocumentIds(Collections.singletonList(fileId));
        submitIndexAddDocumentsJobRequest.setSourceType(sourceType);
        RuntimeOptions runtime = new RuntimeOptions();
        return client.submitIndexAddDocumentsJobWithOptions(workspaceId, submitIndexAddDocumentsJobRequest, headers, runtime);
    }

    /**
     * 查询索引任务状态。
     *
     * @param client      客户端对象
     * @param workspaceId 业务空间ID
     * @param jobId       任务ID
     * @param indexId     知识库ID
     * @return 阿里云百炼服务的响应对象
     */
    public static GetIndexJobStatusResponse getIndexJobStatus(com.aliyun.bailian20231229.Client client, String workspaceId, String jobId, String indexId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.bailian20231229.models.GetIndexJobStatusRequest getIndexJobStatusRequest = new com.aliyun.bailian20231229.models.GetIndexJobStatusRequest();
        getIndexJobStatusRequest.setIndexId(indexId);
        getIndexJobStatusRequest.setJobId(jobId);
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        GetIndexJobStatusResponse getIndexJobStatusResponse = null;
        getIndexJobStatusResponse = client.getIndexJobStatusWithOptions(workspaceId, getIndexJobStatusRequest, headers, runtime);
        return getIndexJobStatusResponse;
    }

    /**
     * 从指定的文档搜索类知识库中永久删除一个或多个文件
     *
     * @param client      客户端（Client）
     * @param workspaceId 业务空间ID
     * @param indexId     知识库ID
     * @param fileId      文件ID
     * @return 阿里云百炼服务的响应
     */
    public static DeleteIndexDocumentResponse deleteIndexDocument(com.aliyun.bailian20231229.Client client, String workspaceId, String indexId, String fileId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        DeleteIndexDocumentRequest deleteIndexDocumentRequest = new DeleteIndexDocumentRequest();
        deleteIndexDocumentRequest.setIndexId(indexId);
        deleteIndexDocumentRequest.setDocumentIds(Collections.singletonList(fileId));
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return client.deleteIndexDocumentWithOptions(workspaceId, deleteIndexDocumentRequest, headers, runtime);
    }

    /**
     * 使用阿里云百炼服务更新知识库
     *
     * @param filePath    文件（更新后的）的实际本地路径
     * @param workspaceId 业务空间ID
     * @param indexId     需要更新的知识库ID
     * @param oldFileId   需要更新的文件的FileID
     * @return 如果成功，返回知识库ID；否则返回 null
     */
    public static String updateKnowledgeBase(String filePath, String workspaceId, String indexId, String oldFileId) {
        // 设置默认值
        String categoryId = "default";
        String parser = "DASHSCOPE_DOCMIND";
        String sourceType = "DATA_CENTER_FILE";
        try {
            // 步骤1：初始化客户端（Client）
            System.out.println("步骤1：创建Client");
            com.aliyun.bailian20231229.Client client = createClient();

            // 步骤2：准备文件信息（更新后的文件）
            System.out.println("步骤2：准备文件信息");
            String fileName = Paths.get(filePath).getFileName().toString();
            String fileMd5 = calculateMD5(filePath);
            String fileSize = getFileSize(filePath);

            // 步骤3：申请上传租约
            System.out.println("步骤3：向阿里云百炼申请上传租约");
            ApplyFileUploadLeaseResponse leaseResponse = applyLease(client, categoryId, fileName, fileMd5, fileSize, workspaceId);
            String leaseId = leaseResponse.getBody().getData().getFileUploadLeaseId();
            String uploadUrl = leaseResponse.getBody().getData().getParam().getUrl();
            Object uploadHeaders = leaseResponse.getBody().getData().getParam().getHeaders();

            // 步骤4：上传文件到临时存储
            System.out.println("步骤4：上传文件到临时存储");
            // 请自行安装jackson-databind
            // 将上一步的uploadHeaders转换为Map(Key-Value形式)
            ObjectMapper mapper = new ObjectMapper();
            Map<String, String> uploadHeadersMap = (Map<String, String>) mapper.readValue(mapper.writeValueAsString(uploadHeaders), Map.class);
            uploadFile(uploadUrl, uploadHeadersMap, filePath);

            // 步骤5：添加文件到类目中
            System.out.println("步骤5：添加文件到类目中");
            AddFileResponse addResponse = addFile(client, leaseId, parser, categoryId, workspaceId);
            String fileId = addResponse.getBody().getData().getFileId();

            // 步骤6：检查更新后的文件状态
            System.out.println("步骤6：检查阿里云百炼中的文件状态");
            while (true) {
                DescribeFileResponse describeResponse = describeFile(client, workspaceId, fileId);
                String status = describeResponse.getBody().getData().getStatus();
                System.out.println("当前文件状态：" + status);
                if ("INIT".equals(status)) {
                    System.out.println("文件待解析，请稍候...");
                } else if ("PARSING".equals(status)) {
                    System.out.println("文件解析中，请稍候...");
                } else if ("PARSE_SUCCESS".equals(status)) {
                    System.out.println("文件解析完成！");
                    break;
                } else {
                    System.out.println("未知的文件状态：" + status + "，请联系技术支持。");
                    return null;
                }
                Thread.sleep(5000);
            }

            // 步骤7：提交追加文件任务
            System.out.println("步骤7：提交追加文件任务");
            SubmitIndexAddDocumentsJobResponse indexAddResponse = submitIndexAddDocumentsJob(client, workspaceId, indexId, fileId, sourceType);
            String jobId = indexAddResponse.getBody().getData().getId();

            // 步骤8：等待追加任务完成
            System.out.println("步骤8：等待追加任务完成");
            while (true) {
                GetIndexJobStatusResponse jobStatusResponse = getIndexJobStatus(client, workspaceId, jobId, indexId);
                String status = jobStatusResponse.getBody().getData().getStatus();
                System.out.println("当前索引任务状态：" + status);
                if ("COMPLETED".equals(status)) {
                    break;
                }
                Thread.sleep(5000);
            }

            // 步骤9：删除旧文件
            System.out.println("步骤9：删除旧文件");
            deleteIndexDocument(client, workspaceId, indexId, oldFileId);

            System.out.println("阿里云百炼知识库更新成功！");
            return indexId;
        } catch (Exception e) {
            System.out.println("发生错误：" + e.getMessage());
            return null;
        }
    }

    /**
     * 主函数。
     */
    public static void main(String[] args) {
        if (!checkEnvironmentVariables()) {
            System.out.println("环境变量校验未通过。");
            return;
        }

        Scanner scanner = new Scanner(System.in);
        System.out.print("请输入您需要上传文件（更新后的）的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：");
        String filePath = scanner.nextLine();

        System.out.print("请输入需要更新的知识库ID："); // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
        String indexId = scanner.nextLine(); // 即 AddFile 接口返回的 FileId。您也可以在阿里云百炼控制台的应用数据页面，单击文件名称旁的 ID 图标获取。

        System.out.print("请输入需要更新的文件的 FileID：");
        String oldFileId = scanner.nextLine();

        String workspaceId = System.getenv("WORKSPACE_ID");
        String result = updateKnowledgeBase(filePath, workspaceId, indexId, oldFileId);
        if (result != null) {
            System.out.println("知识库更新成功，返回知识库ID: " + result);
        } else {
            System.out.println("知识库更新失败。");
        }
    }
}
```

## PHP

```
<?php
// 示例代码仅供参考，请勿在生产环境中直接使用
namespace AlibabaCloud\SDK\Sample;

use AlibabaCloud\Dara\Models\RuntimeOptions;
use AlibabaCloud\SDK\Bailian\V20231229\Bailian;
use AlibabaCloud\SDK\Bailian\V20231229\Models\AddFileRequest;
use \Exception;

use Darabonba\OpenApi\Models\Config;
use AlibabaCloud\SDK\Bailian\V20231229\Models\ApplyFileUploadLeaseRequest;
use AlibabaCloud\SDK\Bailian\V20231229\Models\DeleteIndexDocumentRequest;
use AlibabaCloud\SDK\Bailian\V20231229\Models\GetIndexJobStatusRequest;
use AlibabaCloud\SDK\Bailian\V20231229\Models\SubmitIndexAddDocumentsJobRequest;

class KnowledgeBaseUpdate {

    /**
    * 检查并提示设置必要的环境变量。
    *
    * @return bool 返回 true 如果所有必需的环境变量都已设置，否则 false。
    */
    public static function checkEnvironmentVariables() {
        $requiredVars = [
            'ALIBABA_CLOUD_ACCESS_KEY_ID' => '阿里云访问密钥ID',
            'ALIBABA_CLOUD_ACCESS_KEY_SECRET' => '阿里云访问密钥密码',
            'WORKSPACE_ID' => '阿里云百炼业务空间ID'
        ];
        $missingVars = [];
        foreach ($requiredVars as $var => $description) {
            if (!getenv($var)) {
                $missingVars[] = $var;
                echo "错误：请设置 $var 环境变量 ($description)\n";
            }
        }
        return count($missingVars) === 0;
    }

    /**
     * 计算文件的MD5值。
     *
     * @param string $filePath 文件本地路径。
     * @return string 文件的MD5值。
     */
    public static function calculateMd5($filePath) {
        $md5Hash = hash_init("md5");
        $handle = fopen($filePath, "rb");
        while (!feof($handle)) {
            $chunk = fread($handle, 4096);
            hash_update($md5Hash, $chunk);
        }
        fclose($handle);
        return hash_final($md5Hash);
    }

    /**
     * 获取文件大小（以字节为单位）。
     *
     * @param string $filePath 文件本地路径。
     * @return int 文件大小（以字节为单位）。
     */
    public static function getFileSize($filePath) {
        return (string)filesize($filePath);
    }

    /**
     * 初始化客户端（Client）。
     *
     * @return Bailian 配置好的客户端对象（Client）。
     */
    public static function createClient(){
        $config = new Config([
            "accessKeyId" => getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"), 
            "accessKeySecret" => getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        ]);
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
        $config->endpoint = 'bailian.cn-beijing.aliyuncs.com';
        return new Bailian($config);
    }

    /**
     * 申请文件上传租约。
     *
     * @param Bailian $client 客户端（Client）。
     * @param string $categoryId 类目ID。
     * @param string $fileName 文件名称。
     * @param string $fileMd5 文件的MD5值。
     * @param int $fileSize 文件大小（以字节为单位）。
     * @param string $workspaceId 业务空间ID。
     * @return ApplyFileUploadLeaseResponse 阿里云百炼服务的响应。
     */
    public static function applyLease($client, $categoryId, $fileName, $fileMd5, $fileSize, $workspaceId) {
        $headers = [];
        $applyFileUploadLeaseRequest = new ApplyFileUploadLeaseRequest([
            "fileName" => $fileName,
            "md5" => $fileMd5,
            "sizeInBytes" => $fileSize
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->applyFileUploadLeaseWithOptions($categoryId, $workspaceId, $applyFileUploadLeaseRequest, $headers, $runtime);
    }

    /**
     * 上传文件到临时存储。
    *
    * @param string $preSignedUrl 上传租约中的 URL。
    * @param array $headers 上传请求的头部。
    * @param string $filePath 文件本地路径。
    */
    public static function uploadFile($preSignedUrl, $headers, $filePath) {
        $fileContent = file_get_contents($filePath);
        // 设置上传请求头
        $uploadHeaders = [
            "X-bailian-extra" => $headers["X-bailian-extra"],
            "Content-Type" => $headers["Content-Type"]
        ];
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $preSignedUrl);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PUT");
        curl_setopt($ch, CURLOPT_POSTFIELDS, $fileContent);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array_map(function($key, $value) {
            return "$key: $value";
        }, array_keys($uploadHeaders), $uploadHeaders));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        if ($httpCode != 200) {
            throw new Exception("上传失败: " . curl_error($ch));
        }
        curl_close($ch);
    }

    /**
     * 将文件添加到类目中。
     *
     * @param Bailian $client 客户端（Client）。
     * @param string $leaseId 租约ID。
     * @param string $parser 用于文件的解析器。
     * @param string $categoryId 类目ID。
     * @param string $workspaceId 业务空间ID。
     * @return AddFileResponse 阿里云百炼服务的响应。
     */
    public static function addFile($client, $leaseId, $parser, $categoryId, $workspaceId) {
        $headers = [];
        $addFileRequest = new AddFileRequest([
            "leaseId" => $leaseId,
            "parser" => $parser,
            "categoryId" => $categoryId
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->addFileWithOptions($workspaceId, $addFileRequest, $headers, $runtime);
    }

    /**
     * 查询文件的基本信息。
     *
     * @param Bailian $client 客户端（Client）。
     * @param string $workspaceId 业务空间ID。
     * @param string $fileId 文件ID。
     * @return DescribeFileResponse 阿里云百炼服务的响应。
     */
    public static function describeFile($client, $workspaceId, $fileId) {
        $headers = [];
        $runtime = new RuntimeOptions([]);
        return $client->describeFileWithOptions($workspaceId, $fileId, $headers, $runtime);
    }

    /**
     * 向一个文档搜索类知识库追加导入已解析的文件
     *
     * @param Bailian $client 客户端对象
     * @param string $workspaceId 业务空间ID
     * @param string $indexId 知识库ID
     * @param string $fileId 文件ID
     * @param string $sourceType 数据类型
     * @return SubmitIndexAddDocumentsJobResponse 阿里云百炼服务的响应
     * @throws Exception
     */
    public static function submitIndexAddDocumentsJob($client, $workspaceId, $indexId, $fileId, $sourceType) {
        $headers = [];
        $submitIndexAddDocumentsJobRequest = new SubmitIndexAddDocumentsJobRequest([
            "indexId" =>$indexId,
            "sourceType" => $sourceType,
            "documentIds" => [
                $fileId
            ]
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->submitIndexAddDocumentsJobWithOptions($workspaceId, $submitIndexAddDocumentsJobRequest, $headers, $runtime);
    }

    /**
     * 查询索引任务状态。
     *
     * @param Bailian $client 客户端（Client）。
     * @param string $workspaceId 业务空间ID。
     * @param string $indexId 知识库ID。
     * @param string $jobId 任务ID。
     * @return GetIndexJobStatusResponse 阿里云百炼服务的响应。
     */
    public static function getIndexJobStatus($client, $workspaceId, $jobId, $indexId) {
        $headers = [];
        $getIndexJobStatusRequest = new GetIndexJobStatusRequest([
            'indexId' => $indexId,
            'jobId' => $jobId
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->getIndexJobStatusWithOptions($workspaceId, $getIndexJobStatusRequest, $headers, $runtime);
    }

    /**
     * 从指定的文档搜索类知识库中永久删除文件
     *
     * @param Bailian $client 客户端对象
     * @param string $workspaceId 业务空间ID
     * @param string $indexId 知识库ID
     * @param string $fileId 文件ID
     * @return mixed 阿里云百炼服务的响应
     * @throws Exception
     */
    public static function deleteIndexDocument($client, $workspaceId, $indexId, $fileId) {
        $headers = [];
        $deleteIndexDocumentRequest = new DeleteIndexDocumentRequest([
            "indexId" => $indexId,
            "documentIds" => [
                $fileId
            ]
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->deleteIndexDocumentWithOptions($workspaceId, $deleteIndexDocumentRequest, $headers, $runtime);
    }

    /**
     * 使用阿里云百炼服务更新知识库
     *
     * @param string $filePath 文件（更新后的）的实际本地路径
     * @param string $workspaceId 业务空间ID
     * @param string $indexId 需要更新的知识库ID
     * @param string $oldFileId 需要更新的文件的FileID
     * @return string| null 如果成功，返回知识库ID；否则返回 null
     */
    public static function updateKnowledgeBase($filePath, $workspaceId, $indexId, $oldFileId) {
        $categoryId = "default";
        $parser = "DASHSCOPE_DOCMIND";
        $sourceType = "DATA_CENTER_FILE";

        try {
            // 步骤1：创建Client
            echo "步骤1：创建Client\n";
            $client = self::createClient();

            // 步骤2：准备文件信息
            echo "步骤2：准备文件信息\n";
            $fileName = basename($filePath);
            $fileMd5 = self::calculateMD5($filePath);
            $fileSize = self::getFileSize($filePath);

            // 步骤3：申请上传租约
            echo "步骤3：向阿里云百炼申请上传租约\n";
            $leaseResponse = self::applyLease($client, $categoryId, $fileName, $fileMd5, $fileSize, $workspaceId);
            $leaseId = $leaseResponse->body->data->fileUploadLeaseId;
            $uploadUrl = $leaseResponse->body->data->param->url;
            $uploadHeaders = $leaseResponse->body->data->param->headers;
            $uploadHeadersMap = json_decode(json_encode($uploadHeaders), true);

            // 步骤4：上传文件到临时存储
            echo "步骤4：上传文件到临时存储\n";
            self::uploadFile($uploadUrl, $uploadHeadersMap, $filePath);

            // 步骤5：添加文件到类目中
            echo "步骤5：添加文件到类目中\n";
            $addResponse = self::addFile($client, $leaseId, $parser, $categoryId, $workspaceId);
            $fileId = $addResponse->body->data->fileId;

            // 步骤6：检查文件状态
            echo "步骤6：检查阿里云百炼中的文件状态\n";
            while (true) {
                $describeResponse = self::describeFile($client, $workspaceId, $fileId);
                $status = $describeResponse->body->data->status;
                echo "当前文件状态：" . $status . "\n";

                if ($status === "INIT") {
                    echo "文件待解析，请稍候...\n";
                } elseif ($status === "PARSING") {
                    echo "文件解析中，请稍候...\n";
                } elseif ($status === "PARSE_SUCCESS") {
                    echo "文件解析完成！\n";
                    break;
                } else {
                    echo "未知的文件状态：" . $status . "，请联系技术支持。\n";
                    return null;
                }
                sleep(5);
            }

            // 步骤7：提交追加文件任务
            echo "步骤7：提交追加文件任务\n";
            $indexAddResponse = self::submitIndexAddDocumentsJob($client, $workspaceId, $indexId, $fileId, $sourceType);
            $jobId = $indexAddResponse->body->data->id;

            // 步骤8：等待任务完成
            echo "步骤8：等待追加任务完成\n";
            while (true) {
                $jobStatusResponse = self::getIndexJobStatus($client, $workspaceId, $jobId, $indexId);
                $status = $jobStatusResponse->body->data->status;
                echo "当前索引任务状态：" . $status . "\n";

                if ($status === "COMPLETED") {
                    break;
                }
                sleep(5);
            }

            // 步骤9：删除旧文件
            echo "步骤9：删除旧文件\n";
            self::deleteIndexDocument($client, $workspaceId, $indexId, $oldFileId);

            echo "阿里云百炼知识库更新成功！\n";
            return $indexId;

        } catch (Exception $e) {
            echo "发生错误：" . $e->getMessage() . "\n";
            return null;
        }
    }

    /**
     * 主函数。
     */
    public static function main($args){
        if (!self::checkEnvironmentVariables()) {
            echo "环境变量校验未通过。\n";
            return;
        }
        $filePath = readline("请输入您需要上传文件（更新后的）的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：");
        $indexId = readline("请输入需要更新的知识库ID："); // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
        $oldFileId = readline("请输入需要更新的文件的 FileID："); // 即 AddFile 接口返回的 FileId。您也可以在阿里云百炼控制台的应用数据页面，单击文件名称旁的 ID 图标获取。
        $workspaceId = getenv('WORKSPACE_ID');
        $result = self::updateKnowledgeBase($filePath, $workspaceId, $indexId, $oldFileId);

        if ($result !== null) {
            echo "知识库更新成功，返回知识库ID: " . $result . "\n";
        } else {
            echo "知识库更新失败。\n";
        }
    }
}
// 假定autoload.php位于当前代码文件所在目录的上一级目录中，请根据您的项目实际结构调整。
$path = __DIR__ . \DIRECTORY_SEPARATOR . '..' . \DIRECTORY_SEPARATOR . 'vendor' . \DIRECTORY_SEPARATOR . 'autoload.php';
if (file_exists($path)) {
    require_once $path;
}
KnowledgeBaseUpdate::main(array_slice($argv, 1));
```

## Node.js

```
// 示例代码仅供参考，请勿在生产环境中直接使用
'use strict';

const fs = require('fs');
const path = require('path');
const axios = require('axios');
const crypto = require('crypto');

const bailian20231229 = require('@alicloud/bailian20231229');
const OpenApi = require('@alicloud/openapi-client');
const Util = require('@alicloud/tea-util');
const Tea = require('@alicloud/tea-typescript');

class KbUpdate {

    /**
     * 检查并提示设置必要的环境变量
     * @returns {boolean} - 如果所有必需的环境变量都已设置，返回 true；否则返回 false
     */
    static checkEnvironmentVariables() {
        const requiredVars = {
            'ALIBABA_CLOUD_ACCESS_KEY_ID': '阿里云访问密钥ID',
            'ALIBABA_CLOUD_ACCESS_KEY_SECRET': '阿里云访问密钥密码',
            'WORKSPACE_ID': '阿里云百炼业务空间ID'
        };

        const missing = [];
        for (const [varName, desc] of Object.entries(requiredVars)) {
            if (!process.env[varName]) {
                console.error(`错误：请设置 ${varName} 环境变量 (${desc})`);
                missing.push(varName);
            }
        }
        return missing.length === 0;
    }

    /**
     * 计算文件的MD5值
     * @param {string} filePath - 文件本地路径
     * @returns {Promise<string>} - 文件的MD5值
     */
    static async calculateMD5(filePath) {
        const hash = crypto.createHash('md5');
        const stream = fs.createReadStream(filePath);

        return new Promise((resolve, reject) => {
            stream.on('data', chunk => hash.update(chunk));
            stream.on('end', () => resolve(hash.digest('hex')));
            stream.on('error', reject);
        });
    }

    /**
     * 获取文件大小（以字节为单位），返回字符串格式
     * @param {string} filePath - 文件本地路径
     * @returns {string} - 文件大小（如 "123456"）
     */
    static getFileSize(filePath) {
        try {
            const stats = fs.statSync(filePath);
            return stats.size.toString();
        } catch (err) {
            console.error(`获取文件大小失败: ${err.message}`);
            throw err;
        }
    }

    /**
     * 创建并配置客户端（Client）
     * @return Client
     * @throws Exception
     */
    static createClient() {
        const config = new OpenApi.Config({
            accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
            accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET
        });
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址
        config.endpoint = `bailian.cn-beijing.aliyuncs.com`;
        return new bailian20231229.default(config);
    }

    /**
     * 申请文件上传租约
     * @param {Bailian20231229Client} client - 客户端（Client）
     * @param {string} categoryId - 类目ID
     * @param {string} fileName - 文件名称
     * @param {string} fileMd5 - 文件的MD5值
     * @param {string} fileSize - 文件大小（以字节为单位）
     * @param {string} workspaceId - 业务空间ID
     * @returns {Promise<bailian20231229.ApplyFileUploadLeaseResponse>} - 阿里云百炼服务的响应
     */
    static async applyLease(client, categoryId, fileName, fileMd5, fileSize, workspaceId) {
        const headers = {};
        const req = new bailian20231229.ApplyFileUploadLeaseRequest({
            md5: fileMd5,
            fileName,
            sizeInBytes: fileSize
        });
        const runtime = new Util.RuntimeOptions({});
        return await client.applyFileUploadLeaseWithOptions(
            categoryId,
            workspaceId,
            req,
            headers,
            runtime
        );
    }

    /**
     * 上传文件到临时存储
     * @param {string} preSignedUrl - 上传租约中的URL
     * @param {Object} headers - 上传请求的头部
     * @param {string} filePath - 文件本地路径
     */
    static async uploadFile(preSignedUrl, headers, filePath) {
        const uploadHeaders = {
            "X-bailian-extra": headers["X-bailian-extra"],
            "Content-Type": headers["Content-Type"]
        };
        const stream = fs.createReadStream(filePath);
        try {
            await axios.put(preSignedUrl, stream, { headers: uploadHeaders });
        } catch (e) {
            throw new Error(`上传失败: ${e.message}`);
        }
    }

    /**
     * 添加文件到类目中
     * @param {Bailian20231229Client} client - 客户端（Client）
     * @param {string} leaseId - 租约ID
     * @param {string} parser - 用于文件的解析器
     * @param {string} categoryId - 类目ID
     * @param {string} workspaceId - 业务空间ID
     * @returns {Promise<bailian20231229.AddFileResponse>} - 阿里云百炼服务的响应
     */
    static async addFile(client, leaseId, parser, categoryId, workspaceId) {
        const headers = {};
        const req = new bailian20231229.AddFileRequest({
            leaseId,
            parser,
            categoryId
        });
        const runtime = new Util.RuntimeOptions({});
        return await client.addFileWithOptions(workspaceId, req, headers, runtime);
    }

    /**
     * 查询文件的解析状态
     * @param {Bailian20231229Client} client - 客户端（Client）
     * @param {string} workspaceId - 业务空间ID
     * @param {string} fileId - 文件ID
     * @returns {Promise<bailian20231229.DescribeFileResponse>} - 阿里云百炼服务的响应
     */
    static async describeFile(client, workspaceId, fileId) {
        const headers = {};
        const runtime = new Util.RuntimeOptions({});
        return await client.describeFileWithOptions(workspaceId, fileId, headers, runtime);
    }

    /**
     * 提交追加文件任务
     * @param {Bailian20231229Client} client - 客户端（Client）
     * @param {string} workspaceId - 业务空间ID
     * @param {string} indexId - 知识库ID
     * @param {string} fileId - 文件ID
     * @param {string} sourceType - 数据类型
     * @returns {Promise<bailian20231229.SubmitIndexAddDocumentsJobResponse>} - 阿里云百炼服务的响应
     */
    static async submitIndexAddDocumentsJob(client, workspaceId, indexId, fileId, sourceType) {
        const headers = {};
        const req = new bailian20231229.SubmitIndexAddDocumentsJobRequest({
            indexId,
            documentIds: [fileId],
            sourceType,
        });
        const runtime = new Util.RuntimeOptions({});
        return await client.submitIndexAddDocumentsJobWithOptions(workspaceId, req, headers, runtime);
    }

    /**
     * 查询索引任务状态
     * @param {Bailian20231229Client} client - 客户端（Client）
     * @param {string} workspaceId - 业务空间ID
     * @param {string} jobId - 任务ID
     * @param {string} indexId - 知识库ID
     * @returns {Promise<bailian20231229.GetIndexJobStatusResponse>} - 阿里云百炼服务的响应
     */
    static async getIndexJobStatus(client, workspaceId, jobId, indexId) {
        const headers = {};
        const req = new bailian20231229.GetIndexJobStatusRequest({ jobId, indexId });
        const runtime = new Util.RuntimeOptions({});
        return await client.getIndexJobStatusWithOptions(workspaceId, req, headers, runtime);
    }

    /**
     * 删除旧文件
     * @param {Bailian20231229Client} client - 客户端（Client）
     * @param {string} workspaceId - 业务空间ID
     * @param {string} indexId - 知识库ID
     * @param {string} fileId - 文件ID
     * @returns {Promise<bailian20231229.DeleteIndexDocumentResponse>} - 阿里云百炼服务的响应
     */
    static async deleteIndexDocument(client, workspaceId, indexId, fileId) {
        const headers = {};
        const req = new bailian20231229.DeleteIndexDocumentRequest({
            indexId,
            documentIds: [fileId],
        });
        const runtime = new Util.RuntimeOptions({});
        return await client.deleteIndexDocumentWithOptions(workspaceId, req, headers, runtime);
    }

    /**
     * 使用阿里云百炼服务更新知识库
     * @param {string} filePath - 文件（更新后的）的实际本地路径
     * @param {string} workspaceId - 业务空间ID
     * @param {string} indexId - 需要更新的知识库ID
     * @param {string} oldFileId - 需要更新的文件的FileID
     * @returns {Promise<string | null>} - 如果成功，返回知识库ID；否则返回null
     */
    static async updateKnowledgeBase(filePath, workspaceId, indexId, oldFileId) {
        const categoryId = 'default';
        const parser = 'DASHSCOPE_DOCMIND';
        const sourceType = 'DATA_CENTER_FILE';

        try {
            console.log("步骤1：创建Client");
            const client = this.createClient();

            console.log("步骤2：准备文件信息");
            const fileName = path.basename(filePath);
            const fileMd5 = await this.calculateMD5(filePath);
            const fileSize = this.getFileSize(filePath);

            console.log("步骤3：向阿里云百炼申请上传租约");
            const leaseRes = await this.applyLease(client, categoryId, fileName, fileMd5, fileSize, workspaceId);
            const leaseId = leaseRes.body.data.fileUploadLeaseId;
            const uploadUrl = leaseRes.body.data.param.url;
            const uploadHeaders = leaseRes.body.data.param.headers;

            console.log("步骤4：上传文件到临时存储");
            await this.uploadFile(uploadUrl, uploadHeaders, filePath);

            console.log("步骤5：添加文件到类目中");
            const addRes = await this.addFile(client, leaseId, parser, categoryId, workspaceId);
            const fileId = addRes.body.data.fileId;

            console.log("步骤6：检查阿里云百炼中的文件状态");
            while (true) {
                const descRes = await this.describeFile(client, workspaceId, fileId);
                const status = descRes.body.data.status;
                console.log(`当前文件状态：${status}`);

                if (status === 'INIT') {
                    console.log("文件待解析，请稍候...");
                } else if (status === 'PARSING') {
                    console.log("文件解析中，请稍候...");
                } else if (status === 'PARSE_SUCCESS') {
                    console.log("文件解析完成！");
                    break;
                } else {
                    console.error(`未知的文件状态：${status}，请联系技术支持。`);
                    return null;
                }
                await this.sleep(5);
            }

            console.log("步骤7：提交追加文件任务");
            const indexAddResponse = await this.submitIndexAddDocumentsJob(client, workspaceId, indexId, fileId, sourceType);
            const jobId = indexAddResponse.body.data.id;

            console.log("步骤8：等待追加任务完成");
            while (true) {
                const getJobStatusResponse = await this.getIndexJobStatus(client, workspaceId, jobId, indexId);
                const status = getJobStatusResponse.body.data.status;
                console.log(`当前索引任务状态：${status}`);
                if (status === 'COMPLETED') {
                    break;
                }
                await this.sleep(5);
            }

            console.log("步骤9：删除旧文件");
            await this.deleteIndexDocument(client, workspaceId, indexId, oldFileId);

            console.log("阿里云百炼知识库更新成功！");
            return indexId;
        } catch (e) {
            console.error(`发生错误：${e.message}`);
            return null;
        }
    }

    /**
     * 等待指定时间（秒）
     * @param {number} seconds - 等待时间（秒）
     * @returns {Promise<void>}
     */
    static sleep(seconds) {
        return new Promise(resolve => setTimeout(resolve, seconds * 1000));
    }

    static async main(args) {
        if (!this.checkEnvironmentVariables()) {
            console.log("环境变量校验未通过。");
            return;
        }

        const readline = require('readline').createInterface({
            input: process.stdin,
            output: process.stdout
        });

        try {
            const filePath = await new Promise((resolve, reject) => {
                readline.question("请输入您需要上传文件（更新后的）的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：", (ans) => {
                    ans.trim() ? resolve(ans) : reject(new Error("路径不能为空"));
                });
            });
            const indexId = await new Promise((resolve, reject) => {
                // 知识库ID即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
                readline.question("请输入需要更新的知识库ID：", (ans) => {
                    ans.trim() ? resolve(ans) : reject(new Error("知识库ID不能为空"));
                });
            });
            const oldFileId = await new Promise((resolve, reject) => {
                // FileId即 AddFile 接口返回的 FileId。您也可以在阿里云百炼控制台的应用数据页面，单击文件名称旁的 ID 图标获取。
                readline.question("请输入需要更新的文件的 FileID：", (ans) => {
                    ans.trim() ? resolve(ans) : reject(new Error("FileID不能为空"));
                });
            });
            const workspaceId = process.env.WORKSPACE_ID;

            const result = await this.updateKnowledgeBase(filePath, workspaceId, indexId, oldFileId);
            if (result) console.log(`知识库ID: ${result}`);
            else console.log("知识库更新失败。");
        } catch (err) {
            console.error(err.message);
        } finally {
            readline.close();
        }
    }
}

exports.KbUpdate = KbUpdate;
KbUpdate.main(process.argv.slice(2));
```

## C#

```
// 示例代码仅供参考，请勿在生产环境中直接使用
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

using Tea;
using Tea.Utils;

namespace AlibabaCloud.SDK.KnowledgeBase
{
    public class KnowledgeBaseUpdate
    {
        /// <summary>
        /// 检查并提示设置必要的环境变量。
        /// </summary>
        /// <returns>如果所有必需的环境变量都已设置，返回 true；否则返回 false。</returns>
        public static bool CheckEnvironmentVariables()
        {
            var requiredVars = new Dictionary<string, string>
            {
                { "ALIBABA_CLOUD_ACCESS_KEY_ID", "阿里云访问密钥ID" },
                { "ALIBABA_CLOUD_ACCESS_KEY_SECRET", "阿里云访问密钥密码" },
                { "WORKSPACE_ID", "阿里云百炼业务空间ID" }
            };

            var missingVars = new List<string>();
            foreach (var entry in requiredVars)
            {
                string value = Environment.GetEnvironmentVariable(entry.Key);
                if (string.IsNullOrEmpty(value))
                {
                    missingVars.Add(entry.Key);
                    Console.WriteLine($"错误：请设置 {entry.Key} 环境变量（{entry.Value}）");
                }
            }

            return missingVars.Count == 0;
        }

        /// <summary>
        /// 计算文件的MD5值。
        /// </summary>
        /// <param name="filePath">文件本地路径</param>
        /// <returns>文件的MD5值</returns>
        /// <exception cref="Exception">计算过程中发生错误时抛出异常</exception>
        public static string CalculateMD5(string filePath)
        {
            using (var md5 = MD5.Create())
            {
                using (var stream = new FileStream(filePath, FileMode.Open, FileAccess.Read))
                {
                    byte[] hashBytes = md5.ComputeHash(stream);
                    StringBuilder sb = new StringBuilder();
                    foreach (byte b in hashBytes)
                    {
                        sb.Append(b.ToString("x2"));
                    }
                    return sb.ToString();
                }
            }
        }

        /// <summary>
        /// 获取文件大小（以字节为单位）。
        /// </summary>
        /// <param name="filePath">文件本地路径</param>
        /// <returns>文件大小（以字节为单位）</returns>
        public static string GetFileSize(string filePath)
        {
            var file = new FileInfo(filePath);
            return file.Length.ToString();
        }

        /// <summary>
        /// 初始化客户端（Client）。
        /// </summary>
        /// <returns>配置好的客户端对象</returns>
        /// <exception cref="Exception">初始化过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Client CreateClient()
        {
            var config = new AlibabaCloud.OpenApiClient.Models.Config
            {
                AccessKeyId = Environment.GetEnvironmentVariable("ALIBABA_CLOUD_ACCESS_KEY_ID"),
                AccessKeySecret = Environment.GetEnvironmentVariable("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
            };
            // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
            config.Endpoint = "bailian.cn-beijing.aliyuncs.com";
            return new AlibabaCloud.SDK.Bailian20231229.Client(config);
        }

        /// <summary>
        /// 申请文件上传租约。
        /// </summary>
        /// <param name="client">客户端对象</param>
        /// <param name="categoryId">类目ID</param>
        /// <param name="fileName">文件名称</param>
        /// <param name="fileMd5">文件的MD5值</param>
        /// <param name="fileSize">文件大小（以字节为单位）</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <returns>阿里云百炼服务的响应对象</returns>
        /// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.ApplyFileUploadLeaseResponse ApplyLease(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string categoryId,
            string fileName,
            string fileMd5,
            string fileSize,
            string workspaceId)
        {
            var headers = new Dictionary<string, string>() { };
            var applyFileUploadLeaseRequest = new AlibabaCloud.SDK.Bailian20231229.Models.ApplyFileUploadLeaseRequest
            {
                FileName = fileName,
                Md5 = fileMd5,
                SizeInBytes = fileSize
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.ApplyFileUploadLeaseWithOptions(categoryId, workspaceId, applyFileUploadLeaseRequest, headers, runtime);
        }

        /// <summary>
        /// 上传文件到临时存储。
        /// </summary>
        /// <param name="preSignedUrl">上传租约中的 URL</param>
        /// <param name="headers">上传请求的头部</param>
        /// <param name="filePath">文件本地路径</param>
        /// <exception cref="Exception">上传过程中发生错误时抛出异常</exception>
        public static void UploadFile(string preSignedUrl, Dictionary<string, string> headers, string filePath)
        {
            var file = new FileInfo(filePath);
            if (!File.Exists(filePath))
            {
                throw new ArgumentException($"文件不存在或不是普通文件: {filePath}");
            }

            using (var fs = new FileStream(filePath, FileMode.Open, FileAccess.Read))
            {
                var url = new Uri(preSignedUrl);
                var conn = (HttpWebRequest)WebRequest.Create(url);
                conn.Method = "PUT";
                conn.ContentType = headers["Content-Type"];
                conn.Headers.Add("X-bailian-extra", headers["X-bailian-extra"]);

                byte[] buffer = new byte[4096];
                int bytesRead;
                while ((bytesRead = fs.Read(buffer, 0, buffer.Length)) > 0)
                {
                    conn.GetRequestStream().Write(buffer, 0, bytesRead);
                }

                using (var response = (HttpWebResponse)conn.GetResponse())
                {
                    if (response.StatusCode != HttpStatusCode.OK)
                    {
                        throw new Exception($"上传失败: {response.StatusCode}");
                    }
                }
            }
        }

        /// <summary>
        /// 将文件添加到类目中。
        /// </summary>
        /// <param name="client">客户端对象</param>
        /// <param name="leaseId">租约ID</param>
        /// <param name="parser">用于文件的解析器</param>
        /// <param name="categoryId">类目ID</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <returns>阿里云百炼服务的响应对象</returns>
        /// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.AddFileResponse AddFile(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string leaseId,
            string parser,
            string categoryId,
            string workspaceId)
        {
            var headers = new Dictionary<string, string>() { };
            var addFileRequest = new AlibabaCloud.SDK.Bailian20231229.Models.AddFileRequest
            {
                LeaseId = leaseId,
                Parser = parser,
                CategoryId = categoryId
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.AddFileWithOptions(workspaceId, addFileRequest, headers, runtime);
        }

        /// <summary>
        /// 查询文件的基本信息。
        /// </summary>
        /// <param name="client">客户端对象</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="fileId">文件ID</param>
        /// <returns>阿里云百炼服务的响应对象</returns>
        /// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.DescribeFileResponse DescribeFile(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string workspaceId,
            string fileId)
        {
            var headers = new Dictionary<string, string>() { };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.DescribeFileWithOptions(workspaceId, fileId, headers, runtime);
        }

        /// <summary>
        /// 向一个文档搜索类知识库追加导入已解析的文件
        /// </summary>
        /// <param name="client">客户端（Client）</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="indexId">知识库ID</param>
        /// <param name="fileId">文件ID</param>
        /// <param name="sourceType">数据类型</param>
        /// <returns>阿里云百炼服务的响应</returns>
        public static AlibabaCloud.SDK.Bailian20231229.Models.SubmitIndexAddDocumentsJobResponse SubmitIndexAddDocumentsJob(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string workspaceId,
            string indexId,
            string fileId,
            string sourceType)
        {
            var headers = new Dictionary<string, string>() { };
            var submitIndexAddDocumentsJobRequest = new AlibabaCloud.SDK.Bailian20231229.Models.SubmitIndexAddDocumentsJobRequest
            {
                IndexId = indexId,
                DocumentIds = new List<string> { fileId },
                SourceType = sourceType
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.SubmitIndexAddDocumentsJobWithOptions(workspaceId, submitIndexAddDocumentsJobRequest, headers, runtime);
        }

        /// <summary>
        /// 查询索引任务状态。
        /// </summary>
        /// <param name="client">客户端对象</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="jobId">任务ID</param>
        /// <param name="indexId">知识库ID</param>
        /// <returns>阿里云百炼服务的响应对象</returns>
        /// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Models.GetIndexJobStatusResponse GetIndexJobStatus(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string workspaceId,
            string jobId,
            string indexId)
        {
            var headers = new Dictionary<string, string>() { };
            var getIndexJobStatusRequest = new AlibabaCloud.SDK.Bailian20231229.Models.GetIndexJobStatusRequest
            {
                IndexId = indexId,
                JobId = jobId
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.GetIndexJobStatusWithOptions(workspaceId, getIndexJobStatusRequest, headers, runtime);
        }

        /// <summary>
        /// 从指定的文档搜索类知识库中永久删除一个或多个文件
        /// </summary>
        /// <param name="client">客户端（Client）</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="indexId">知识库ID</param>
        /// <param name="fileId">文件ID</param>
        /// <returns>阿里云百炼服务的响应</returns>
        public static AlibabaCloud.SDK.Bailian20231229.Models.DeleteIndexDocumentResponse DeleteIndexDocument(
            AlibabaCloud.SDK.Bailian20231229.Client client,
            string workspaceId,
            string indexId,
            string fileId)
        {
            var headers = new Dictionary<string, string>() { };
            var deleteIndexDocumentRequest = new AlibabaCloud.SDK.Bailian20231229.Models.DeleteIndexDocumentRequest
            {
                IndexId = indexId,
                DocumentIds = new List<string> { fileId }
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.DeleteIndexDocumentWithOptions(workspaceId, deleteIndexDocumentRequest, headers, runtime);
        }

        /// <summary>
        /// 使用阿里云百炼服务更新知识库
        /// </summary>
        /// <param name="filePath">文件（更新后的）的实际本地路径</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="indexId">需要更新的知识库ID</param>
        /// <param name="oldFileId">需要更新的文件的FileID</param>
        /// <returns>如果成功，返回知识库ID；否则返回 null</returns>
        public static string UpdateKnowledgeBase(string filePath, string workspaceId, string indexId, string oldFileId)
        {
            // 设置默认值
            string categoryId = "default";
            string parser = "DASHSCOPE_DOCMIND";
            string sourceType = "DATA_CENTER_FILE";

            try
            {
                Console.WriteLine("步骤1：创建Client");
                var client = CreateClient();

                Console.WriteLine("步骤2：准备文件信息");
                string fileName = Path.GetFileName(filePath);
                string fileMd5 = CalculateMD5(filePath);
                string fileSize = GetFileSize(filePath);

                Console.WriteLine("步骤3：向阿里云百炼申请上传租约");
                Bailian20231229.Models.ApplyFileUploadLeaseResponse leaseResponse = ApplyLease(client, categoryId, fileName, fileMd5, fileSize, workspaceId);
                string leaseId = leaseResponse.Body.Data.FileUploadLeaseId;
                string uploadUrl = leaseResponse.Body.Data.Param.Url;
                var uploadHeaders = leaseResponse.Body.Data.Param.Headers;

                Console.WriteLine("步骤4：上传文件到临时存储");
                // 请自行安装Newtonsoft.Json
                var uploadHeadersMap = JsonConvert.DeserializeObject<Dictionary<string, string>>(JsonConvert.SerializeObject(uploadHeaders));
                UploadFile(uploadUrl, uploadHeadersMap, filePath);

                Console.WriteLine("步骤5：添加文件到类目中");
                Bailian20231229.Models.AddFileResponse addResponse = AddFile(client, leaseId, parser, categoryId, workspaceId);
                string fileId = addResponse.Body.Data.FileId;

                Console.WriteLine("步骤6：检查阿里云百炼中的文件状态");
                while (true)
                {
                    Bailian20231229.Models.DescribeFileResponse describeResponse = DescribeFile(client, workspaceId, fileId);
                    string status = describeResponse.Body.Data.Status;
                    Console.WriteLine("当前文件状态：" + status);
                    if ("INIT".Equals(status))
                    {
                        Console.WriteLine("文件待解析，请稍候...");
                    }
                    else if ("PARSING".Equals(status))
                    {
                        Console.WriteLine("文件解析中，请稍候...");
                    }
                    else if ("PARSE_SUCCESS".Equals(status))
                    {
                        Console.WriteLine("文件解析完成！");
                        break;
                    }
                    else
                    {
                        Console.WriteLine("未知的文件状态：" + status + "，请联系技术支持。");
                        return null;
                    }
                    Thread.Sleep(5000);
                }

                Console.WriteLine("步骤7：提交追加文件任务");
                Bailian20231229.Models.SubmitIndexAddDocumentsJobResponse indexAddResponse = SubmitIndexAddDocumentsJob(client, workspaceId, indexId, fileId, sourceType);
                string jobId = indexAddResponse.Body.Data.Id;

                Console.WriteLine("步骤8：等待追加任务完成");
                while (true)
                {
                    Bailian20231229.Models.GetIndexJobStatusResponse jobStatusResponse = GetIndexJobStatus(client, workspaceId, jobId, indexId);
                    string status = jobStatusResponse.Body.Data.Status;
                    Console.WriteLine("当前索引任务状态：" + status);
                    if ("COMPLETED".Equals(status))
                    {
                        break;
                    }
                    Thread.Sleep(5000);
                }

                Console.WriteLine("步骤9：删除旧文件");
                DeleteIndexDocument(client, workspaceId, indexId, oldFileId);

                Console.WriteLine("阿里云百炼知识库更新成功！");
                return indexId;
            }
            catch (Exception e)
            {
                Console.WriteLine("发生错误：" + e.Message);
                return null;
            }
        }

        /// <summary>
        /// 主函数。
        /// </summary>
        public static void Main(string[] args)
        {
            if (!CheckEnvironmentVariables())
            {
                Console.WriteLine("环境变量校验未通过。");
                return;
            }

            Console.Write("请输入您需要上传文件（更新后的）的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：");
            string filePath = Console.ReadLine();

            Console.Write("请输入需要更新的知识库ID："); // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
            string indexId = Console.ReadLine();

            Console.Write("请输入需要更新的文件的 FileID："); // 即 AddFile 接口返回的 FileId。您也可以在阿里云百炼控制台的应用数据页面，单击文件名称旁的 ID 图标获取。
            string oldFileId = Console.ReadLine();

            string workspaceId = Environment.GetEnvironmentVariable("WORKSPACE_ID");
            string result = UpdateKnowledgeBase(filePath, workspaceId, indexId, oldFileId);
            if (result != null)
            {
                Console.WriteLine("知识库更新成功，返回知识库ID: " + result);
            }
            else
            {
                Console.WriteLine("知识库更新失败。");
            }
        }
    }
}
```

## Go

```
// 示例代码仅供参考，请勿在生产环境中直接使用
package main

import (
	"bufio"
	"crypto/md5"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"time"

	bailian20231229 "github.com/alibabacloud-go/bailian-20231229/v2/client"
	openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client"
	util "github.com/alibabacloud-go/tea-utils/v2/service"
	"github.com/alibabacloud-go/tea/tea"
	"github.com/go-resty/resty/v2"
)

// CheckEnvironmentVariables 检查并提示设置必要的环境变量。
func CheckEnvironmentVariables() bool {
	// 必要的环境变量及其描述。
	requiredVars := map[string]string{
		"ALIBABA_CLOUD_ACCESS_KEY_ID":     "阿里云访问密钥ID",
		"ALIBABA_CLOUD_ACCESS_KEY_SECRET": "阿里云访问密钥密码",
		"WORKSPACE_ID":                    "阿里云百炼业务空间ID",
	}

	var missingVars []string
	for varName, desc := range requiredVars {
		if os.Getenv(varName) == "" {
			fmt.Printf("错误：请设置 %s 环境变量 (%s)\n", varName, desc)
			missingVars = append(missingVars, varName)
		}
	}

	return len(missingVars) == 0
}

// CalculateMD5 计算文件的MD5值。
//
// 参数:
//   - filePath (string): 文件本地路径。
//
// 返回:
//   - string: 文件的MD5值。
//   - error: 错误信息。
func CalculateMD5(filePath string) (_result string, _err error) {
	file, err := os.Open(filePath)
	if err != nil {
		return "", err
	}
	defer file.Close()

	md5Hash := md5.New()
	_, err = io.Copy(md5Hash, file)
	if err != nil {
		return "", err
	}

	return fmt.Sprintf("%x", md5Hash.Sum(nil)), nil
}

// GetFileSize 获取文件大小（以字节为单位）。
//
// 参数:
//   - filePath (string): 文件本地路径。
//
// 返回:
//   - string: 文件大小（以字节为单位）。
//   - error: 错误信息。
func GetFileSize(filePath string) (_result string, _err error) {
	info, err := os.Stat(filePath)
	if err != nil {
		return "", err
	}
	return fmt.Sprintf("%d", info.Size()), nil
}

// CreateClient 创建并配置客户端（Client）。
//
// 返回:
//   - *client.Bailian20231229Client: 配置好的客户端（Client）。
//   - error: 错误信息。
func CreateClient() (_result *bailian20231229.Client, _err error) {
	config := &openapi.Config{
		AccessKeyId:     tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")),
		AccessKeySecret: tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")),
	}
	// 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
	config.Endpoint = tea.String("bailian.cn-beijing.aliyuncs.com")
	_result = &bailian20231229.Client{}
	_result, _err = bailian20231229.NewClient(config)
	return _result, _err
}

// ApplyLease 从阿里云百炼服务申请文件上传租约。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - categoryId (string): 类目ID。
//   - fileName (string): 文件名称。
//   - fileMD5 (string): 文件的MD5值。
//   - fileSize (string): 文件大小（以字节为单位）。
//   - workspaceId (string): 业务空间ID。
//
// 返回:
//   - *bailian20231229.ApplyFileUploadLeaseResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func ApplyLease(client *bailian20231229.Client, categoryId, fileName, fileMD5 string, fileSize string, workspaceId string) (_result *bailian20231229.ApplyFileUploadLeaseResponse, _err error) {
	headers := make(map[string]*string)
	applyFileUploadLeaseRequest := &bailian20231229.ApplyFileUploadLeaseRequest{
		FileName:    tea.String(fileName),
		Md5:         tea.String(fileMD5),
		SizeInBytes: tea.String(fileSize),
	}
	runtime := &util.RuntimeOptions{}
	return client.ApplyFileUploadLeaseWithOptions(tea.String(categoryId), tea.String(workspaceId), applyFileUploadLeaseRequest, headers, runtime)
}

// UploadFile 将文件上传到阿里云百炼服务。
//
// 参数:
//   - preSignedUrl (string): 上传租约中的 URL。
//   - headers (map[string]string): 上传请求的头部。
//   - filePath (string): 文件本地路径。
func UploadFile(preSignedUrl string, headers map[string]string, filePath string) error {
	file, err := os.Open(filePath)
	if err != nil {
		return err
	}
	defer file.Close()

	body, err := io.ReadAll(file)
	if err != nil {
		return err
	}

	client := resty.New()
	uploadHeaders := map[string]string{
		"X-bailian-extra": headers["X-bailian-extra"],
		"Content-Type":    headers["Content-Type"],
	}

	resp, err := client.R().
		SetHeaders(uploadHeaders).
		SetBody(body).
		Put(preSignedUrl)

	if err != nil {
		return err
	}

	if resp.IsError() {
		return fmt.Errorf("HTTP 错误: %d", resp.StatusCode())
	}

	return nil
}

// AddFile 将文件添加到阿里云百炼服务的指定类目中。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - leaseId (string): 租约ID。
//   - parser (string): 用于文件的解析器。
//   - categoryId (string): 类目ID。
//   - workspaceId (string): 业务空间ID。
//
// 返回:
//   - *bailian20231229.AddFileResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func AddFile(client *bailian20231229.Client, leaseId, parser, categoryId, workspaceId string) (_result *bailian20231229.AddFileResponse, _err error) {
	headers := make(map[string]*string)
	addFileRequest := &bailian20231229.AddFileRequest{
		LeaseId:    tea.String(leaseId),
		Parser:     tea.String(parser),
		CategoryId: tea.String(categoryId),
	}
	runtime := &util.RuntimeOptions{}
	return client.AddFileWithOptions(tea.String(workspaceId), addFileRequest, headers, runtime)
}

// DescribeFile 获取文件的基本信息。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - fileId (string): 文件ID。
//
// 返回:
//   - *bailian20231229.DescribeFileResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func DescribeFile(client *bailian20231229.Client, workspaceId, fileId string) (_result *bailian20231229.DescribeFileResponse, _err error) {
	headers := make(map[string]*string)
	runtime := &util.RuntimeOptions{}
	return client.DescribeFileWithOptions(tea.String(workspaceId), tea.String(fileId), headers, runtime)
}

// SubmitIndexAddDocumentsJob 向一个文档搜索类知识库追加导入已解析的文件。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - indexId（string）: 知识库ID。
//   - fileId(string): 文件ID。
//   - sourceType(string): 数据类型。
//
// 返回:
//   - *bailian20231229.SubmitIndexAddDocumentsJobResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func SubmitIndexAddDocumentsJob(client *bailian20231229.Client, workspaceId, indexId, fileId, sourceType string) (_result *bailian20231229.SubmitIndexAddDocumentsJobResponse, _err error) {
	headers := make(map[string]*string)
	submitIndexAddDocumentsJobRequest := &bailian20231229.SubmitIndexAddDocumentsJobRequest{
		IndexId:     tea.String(indexId),
		SourceType:  tea.String(sourceType),
		DocumentIds: []*string{tea.String(fileId)},
	}
	runtime := &util.RuntimeOptions{}
	return client.SubmitIndexAddDocumentsJobWithOptions(tea.String(workspaceId), submitIndexAddDocumentsJobRequest, headers, runtime)
}

// GetIndexJobStatus 查询索引任务状态。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - jobId (string): 任务ID。
//   - indexId (string): 知识库ID。
//
// 返回:
//   - *bailian20231229.GetIndexJobStatusResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func GetIndexJobStatus(client *bailian20231229.Client, workspaceId, jobId, indexId string) (_result *bailian20231229.GetIndexJobStatusResponse, _err error) {
	headers := make(map[string]*string)
	getIndexJobStatusRequest := &bailian20231229.GetIndexJobStatusRequest{
		JobId:   tea.String(jobId),
		IndexId: tea.String(indexId),
	}
	runtime := &util.RuntimeOptions{}
	return client.GetIndexJobStatusWithOptions(tea.String(workspaceId), getIndexJobStatusRequest, headers, runtime)
}

// DeleteIndexDocument 从指定的文档搜索类知识库中永久删除一个或多个文件。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - indexId (string): 知识库ID。
//   - fileId (string): 文件ID。
//
// 返回:
//   - *bailian20231229.DeleteIndexDocumentResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func DeleteIndexDocument(client *bailian20231229.Client, workspaceId, indexId, fileId string) (*bailian20231229.DeleteIndexDocumentResponse, error) {
	headers := make(map[string]*string)
	deleteIndexDocumentRequest := &bailian20231229.DeleteIndexDocumentRequest{
		IndexId:     tea.String(indexId),
		DocumentIds: []*string{tea.String(fileId)},
	}
	runtime := &util.RuntimeOptions{}
	return client.DeleteIndexDocumentWithOptions(tea.String(workspaceId), deleteIndexDocumentRequest, headers, runtime)
}

// UpdateKnowledgeBase 使用阿里云百炼服务更新知识库。
//
// 参数:
//   - filePath (string): 文件（更新后的）的实际本地路径。
//   - workspaceId (string): 业务空间ID。
//   - indexId (string): 需要更新的知识库ID。
//   - oldFileId (string): 需要更新的文件的FileID。
//
// 返回:
//   - string: 如果成功，返回知识库ID；否则返回空字符串。
//   - error: 错误信息。
func UpdateKnowledgeBase(filePath, workspaceId, indexId, oldFileId string) (_result string, _err error) {
	// 设置默认值
	categoryId := "default"
	parser := "DASHSCOPE_DOCMIND"
	sourceType := "DATA_CENTER_FILE"

	fmt.Println("步骤1：创建Client")
	client, err := CreateClient()
	if err != nil {
		return "", err
	}

	fmt.Println("步骤2：准备文件信息")
	fileName := filepath.Base(filePath)
	fileMD5, err := CalculateMD5(filePath)
	if err != nil {
		return "", err
	}
	fileSizeStr, err := GetFileSize(filePath)
	if err != nil {
		return "", err
	}

	fmt.Println("步骤3：向阿里云百炼申请上传租约")
	leaseResponse, err := ApplyLease(client, categoryId, fileName, fileMD5, fileSizeStr, workspaceId)
	if err != nil {
		return "", err
	}

	leaseId := tea.StringValue(leaseResponse.Body.Data.FileUploadLeaseId)
	uploadURL := tea.StringValue(leaseResponse.Body.Data.Param.Url)
	uploadHeaders := leaseResponse.Body.Data.Param.Headers

	jsonData, err := json.Marshal(uploadHeaders)
	if err != nil {
		return "", err
	}

	var uploadHeadersMap map[string]string
	err = json.Unmarshal(jsonData, &uploadHeadersMap)
	if err != nil {
		return "", err
	}

	fmt.Println("步骤4：上传文件到临时存储")
	err = UploadFile(uploadURL, uploadHeadersMap, filePath)
	if err != nil {
		return "", err
	}

	fmt.Println("步骤5：添加文件到类目中")
	addResponse, err := AddFile(client, leaseId, parser, categoryId, workspaceId)
	if err != nil {
		return "", err
	}
	fileId := tea.StringValue(addResponse.Body.Data.FileId)

	fmt.Println("步骤6：检查阿里云百炼中的文件状态")
	for {
		describeResponse, err := DescribeFile(client, workspaceId, fileId)
		if err != nil {
			return "", err
		}

		status := tea.StringValue(describeResponse.Body.Data.Status)
		fmt.Printf("当前文件状态：%s\n", status)

		if status == "INIT" {
			fmt.Println("文件待解析，请稍候...")
		} else if status == "PARSING" {
			fmt.Println("文件解析中，请稍候...")
		} else if status == "PARSE_SUCCESS" {
			fmt.Println("文件解析完成！")
			break
		} else {
			fmt.Printf("未知的文件状态：%s，请联系技术支持。\n", status)
			return "", fmt.Errorf("unknown document status: %s", status)
		}
		time.Sleep(5 * time.Second)
	}

	// 提交追加文件任务
	fmt.Println("步骤7：提交追加文件任务")
	indexAddResponse, err := SubmitIndexAddDocumentsJob(client, workspaceId, indexId, fileId, sourceType)
	if err != nil {
		return "", err
	}
	jobId := tea.StringValue(indexAddResponse.Body.Data.Id)

	// 等待任务完成
	fmt.Println("步骤8：等待追加任务完成")
	for {
		getIndexJobStatusResponse, err := GetIndexJobStatus(client, workspaceId, jobId, indexId)
		if err != nil {
			return "", err
		}

		status := tea.StringValue(getIndexJobStatusResponse.Body.Data.Status)
		fmt.Printf("当前索引任务状态：%s\n", status)

		if status == "COMPLETED" {
			break
		}
		time.Sleep(5 * time.Second)
	}

	// 删除旧文件
	fmt.Println("步骤9：删除旧文件")
	_, err = DeleteIndexDocument(client, workspaceId, indexId, oldFileId)
	if err != nil {
		return "", err
	}

	fmt.Println("阿里云百炼知识库更新成功！")
	return indexId, nil
}

// 主函数。
func main() {
	if !CheckEnvironmentVariables() {
		fmt.Println("环境变量校验未通过。")
		return
	}
	// 创建 scanner 用于读取输入
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("请输入您需要上传文件（更新后的）的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：")
	filePath, _ := reader.ReadString('\n')
	filePath = strings.TrimSpace(filePath)

	fmt.Print("请输入需要更新的知识库ID：") // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
	indexId, _ := reader.ReadString('\n')
	indexId = strings.TrimSpace(indexId)

	fmt.Print("请输入需要更新的文件的 FileID：") // 即 AddFile 接口返回的 FileId。您也可以在阿里云百炼控制台的应用数据页面，单击文件名称旁的 ID 图标获取。
	oldFileId, _ := reader.ReadString('\n')
	oldFileId = strings.TrimSpace(oldFileId)

	workspaceId := os.Getenv("WORKSPACE_ID")
	result, err := UpdateKnowledgeBase(filePath, workspaceId, indexId, oldFileId)
	if err != nil {
		fmt.Printf("发生错误：%v\n", err)
		return
	}

	if result != "" {
		fmt.Printf("知识库更新成功，返回知识库ID: %s\n", result)
	} else {
		fmt.Println("知识库更新失败。")
	}
}
```

## 管理知识库

**重要**

-   在调用本示例之前，请务必完成上述所有[前置步骤](#a4a15bd543can)。子账号调用本示例前需[获取AliyunBailianDataFullAccess策略](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)。
    
-   若您使用了 IDE 或其他辅助开发插件，需将`ALIBABA_CLOUD_ACCESS_KEY_ID`、`ALIBABA_CLOUD_ACCESS_KEY_SECRET`和`WORKSPACE_ID`变量配置到相应的开发环境中。
    

## Python

```
# 示例代码仅供参考，请勿在生产环境中直接使用
import os

from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

def check_environment_variables():
    """检查并提示设置必要的环境变量"""
    required_vars = {
        'ALIBABA_CLOUD_ACCESS_KEY_ID': '阿里云访问密钥ID',
        'ALIBABA_CLOUD_ACCESS_KEY_SECRET': '阿里云访问密钥密码',
        'WORKSPACE_ID': '阿里云百炼业务空间ID'
    }
    missing_vars = []
    for var, description in required_vars.items():
        if not os.environ.get(var):
            missing_vars.append(var)
            print(f"错误：请设置 {var} 环境变量 ({description})")

    return len(missing_vars) == 0

# 创建客户端（Client）
def create_client() -> bailian20231229Client:
    """
    创建并配置客户端（Client）。

    返回:
        bailian20231229Client: 配置好的客户端（Client）。
    """
    config = open_api_models.Config(
        access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    )
    # 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
    config.endpoint = 'bailian.cn-beijing.aliyuncs.com'
    return bailian20231229Client(config)

# 查看知识库
def list_indices(client, workspace_id):
    """
    获取指定业务空间下一个或多个知识库的详细信息。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    list_indices_request = bailian_20231229_models.ListIndicesRequest()
    runtime = util_models.RuntimeOptions()
    return client.list_indices_with_options(workspace_id, list_indices_request, headers, runtime)

# 删除知识库
def delete_index(client, workspace_id, index_id):
    """
    永久性删除指定的知识库。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    delete_index_request = bailian_20231229_models.DeleteIndexRequest(
        index_id=index_id
    )
    runtime = util_models.RuntimeOptions()
    return client.delete_index_with_options(workspace_id, delete_index_request, headers, runtime)

def main():
    if not check_environment_variables():
        print("环境变量校验未通过。")
        return
    try:
        start_option = input(
            "请选择要执行的操作：\n1. 查看知识库\n2. 删除知识库\n请输入选项（1或2）：")
        if start_option == '1':
            # 查看知识库
            print("\n执行查看知识库")
            workspace_id = os.environ.get('WORKSPACE_ID')
            client = create_client()
            list_indices_response = list_indices(client, workspace_id)
            print(UtilClient.to_jsonstring(list_indices_response.body.data))
        elif start_option == '2':
            print("\n执行删除知识库")
            workspace_id = os.environ.get('WORKSPACE_ID')
            index_id = input("请输入知识库ID：")  # 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
            # 删除前二次确认
            while True:
                confirm = input(f"您确定要永久性删除该知识库 {index_id} 吗？(y/n): ").strip().lower()
                if confirm == 'y':
                    break
                elif confirm == 'n':
                    print("已取消删除操作。")
                    return
                else:
                    print("无效输入，请输入 y 或 n。")
            client = create_client()
            resp = delete_index(client, workspace_id, index_id)
            if resp.body.status == 200:
                print(f"知识库{index_id}删除成功！")
            else:
                err_info = UtilClient.to_jsonstring(resp.body)
                print(f"发生错误：{err_info}")
        else:
            print("无效的选项，程序退出。")
            return
    except Exception as e:
        print(f"发生错误：{e}")
        return

if __name__ == '__main__':
    main()
```

## Java

```
// 示例代码仅供参考，请勿在生产环境中直接使用
import com.aliyun.bailian20231229.models.DeleteIndexResponse;
import com.aliyun.bailian20231229.models.ListIndicesResponse;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.*;

public class KnowledgeBaseManage {

    /**
     * 检查并提示设置必要的环境变量。
     *
     * @return true 如果所有必需的环境变量都已设置，否则 false
     */
    public static boolean checkEnvironmentVariables() {
        Map<String, String> requiredVars = new HashMap<>();
        requiredVars.put("ALIBABA_CLOUD_ACCESS_KEY_ID", "阿里云访问密钥ID");
        requiredVars.put("ALIBABA_CLOUD_ACCESS_KEY_SECRET", "阿里云访问密钥密码");
        requiredVars.put("WORKSPACE_ID", "阿里云百炼业务空间ID");

        List<String> missingVars = new ArrayList<>();
        for (Map.Entry<String, String> entry : requiredVars.entrySet()) {
            String value = System.getenv(entry.getKey());
            if (value == null || value.isEmpty()) {
                missingVars.add(entry.getKey());
                System.out.println("错误：请设置 " + entry.getKey() + " 环境变量 (" + entry.getValue() + ")");
            }
        }

        return missingVars.isEmpty();
    }

    /**
     * 创建并配置客户端（Client）
     *
     * @return 配置好的客户端（Client）
     */
    public static com.aliyun.bailian20231229.Client createClient() throws Exception {
        com.aliyun.credentials.Client credential = new com.aliyun.credentials.Client();
        com.aliyun.teaopenapi.models.Config config = new com.aliyun.teaopenapi.models.Config()
                .setCredential(credential);
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
        config.endpoint = "bailian.cn-beijing.aliyuncs.com";
        return new com.aliyun.bailian20231229.Client(config);
    }

    /**
     * 获取指定业务空间下一个或多个知识库的详细信息
     *
     * @param client      客户端（Client）
     * @param workspaceId 业务空间ID
     * @return 阿里云百炼服务的响应
     */
    public static ListIndicesResponse listIndices(com.aliyun.bailian20231229.Client client, String workspaceId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.bailian20231229.models.ListIndicesRequest listIndicesRequest = new com.aliyun.bailian20231229.models.ListIndicesRequest();
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return client.listIndicesWithOptions(workspaceId, listIndicesRequest, headers, runtime);
    }

    /**
     * 永久性删除指定的知识库
     *
     * @param client      客户端（Client）
     * @param workspaceId 业务空间ID
     * @param indexId     知识库ID
     * @return 阿里云百炼服务的响应
     */
    public static DeleteIndexResponse deleteIndex(com.aliyun.bailian20231229.Client client, String workspaceId, String indexId) throws Exception {
        Map<String, String> headers = new HashMap<>();
        com.aliyun.bailian20231229.models.DeleteIndexRequest deleteIndexRequest = new com.aliyun.bailian20231229.models.DeleteIndexRequest();
        deleteIndexRequest.setIndexId(indexId);
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return client.deleteIndexWithOptions(workspaceId, deleteIndexRequest, headers, runtime);
    }

    /**
     * 主函数
     */
    public static void main(String[] args) {
        if (!checkEnvironmentVariables()) {
            System.out.println("环境变量校验未通过。");
            return;
        }

        try {
            Scanner scanner = new Scanner(System.in);
            System.out.print("请选择要执行的操作：\n1. 查看知识库\n2. 删除知识库\n请输入选项（1或2）：");
            String startOption = scanner.nextLine();
            com.aliyun.bailian20231229.Client client = createClient();
            if (startOption.equals("1")) {
                // 查看知识库
                System.out.println("\n执行查看知识库");
                String workspaceId = System.getenv("WORKSPACE_ID");
                ListIndicesResponse response = listIndices(client, workspaceId);
                // 请自行安装jackson-databind。将响应转换为 JSON 字符串
                ObjectMapper mapper = new ObjectMapper();
                String result = mapper.writeValueAsString(response.getBody().getData());
                System.out.println(result);
            } else if (startOption.equals("2")) {
                System.out.println("\n执行删除知识库");
                String workspaceId = System.getenv("WORKSPACE_ID");
                System.out.print("请输入知识库ID："); // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
                String indexId = scanner.nextLine();
                // 删除前二次确认
                boolean confirm = false;
                while (!confirm) {
                    System.out.print("您确定要永久性删除该知识库 " + indexId + " 吗？(y/n): ");
                    String input = scanner.nextLine().trim().toLowerCase();
                    if (input.equals("y")) {
                        confirm = true;
                    } else if (input.equals("n")) {
                        System.out.println("已取消删除操作。");
                        return;
                    } else {
                        System.out.println("无效输入，请输入 y 或 n。");
                    }
                }
                DeleteIndexResponse resp = deleteIndex(client, workspaceId, indexId);
                if (resp.getBody().getStatus().equals("200")) {
                    System.out.println("知识库" + indexId + "删除成功！");
                } else {
                    ObjectMapper mapper = new ObjectMapper();
                    System.out.println("发生错误：" + mapper.writeValueAsString(resp.getBody()));
                }
            } else {
                System.out.println("无效的选项，程序退出。");
            }
        } catch (Exception e) {
            System.out.println("发生错误：" + e.getMessage());
        }
    }
}
```

## PHP

```
<?php
// 示例代码仅供参考，请勿在生产环境中直接使用
namespace AlibabaCloud\SDK\Sample;

use AlibabaCloud\Dara\Models\RuntimeOptions;
use AlibabaCloud\SDK\Bailian\V20231229\Bailian;
use AlibabaCloud\SDK\Bailian\V20231229\Models\DeleteIndexRequest;
use AlibabaCloud\SDK\Bailian\V20231229\Models\ListIndexDocumentsRequest;
use \Exception;

use Darabonba\OpenApi\Models\Config;

class KnowledgeBaseManage {

    /**
    * 检查并提示设置必要的环境变量。
    *
    * @return bool 返回 true 如果所有必需的环境变量都已设置，否则 false。
    */
    public static function checkEnvironmentVariables() {
        $requiredVars = [
            'ALIBABA_CLOUD_ACCESS_KEY_ID' => '阿里云访问密钥ID',
            'ALIBABA_CLOUD_ACCESS_KEY_SECRET' => '阿里云访问密钥密码',
            'WORKSPACE_ID' => '阿里云百炼业务空间ID'
        ];
        $missingVars = [];
        foreach ($requiredVars as $var => $description) {
            if (!getenv($var)) {
                $missingVars[] = $var;
                echo "错误：请设置 $var 环境变量 ($description)\n";
            }
        }
        return count($missingVars) === 0;
    }

    /**
     * 初始化客户端（Client）。
     *
     * @return Bailian 配置好的客户端对象（Client）。
     */
    public static function createClient(){
        $config = new Config([
            "accessKeyId" => getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"), 
            "accessKeySecret" => getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        ]);
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
        $config->endpoint = 'bailian.cn-beijing.aliyuncs.com';
        return new Bailian($config);
    }

     /**
     * 获取指定业务空间下一个或多个知识库的详细信息
     *
     * @param Bailian $client 客户端对象（Client）
     * @param string $workspaceId 业务空间ID
     * @return ListIndicesResponse 阿里云百炼服务的响应
     * @throws Exception
     */
    public static function listIndices($client, $workspaceId) {
        $headers = [];
        $listIndexDocumentsRequest = new ListIndexDocumentsRequest([]);
        $runtime = new RuntimeOptions([]);
        // 调用客户端方法
        return $client->listIndicesWithOptions($workspaceId, $listIndexDocumentsRequest, $headers, $runtime);
    }

    /**
     * 永久性删除指定的知识库
     *
     * @param Bailian $client 客户端对象（Client）
     * @param string $workspaceId 业务空间ID
     * @param string $indexId 知识库ID
     * @return mixed 阿里云百炼服务的响应
     * @throws Exception
     */
    public static function deleteIndex($client, $workspaceId, $indexId) {
        $headers = [];
        $deleteIndexRequest = new DeleteIndexRequest([
            "indexId" => $indexId
        ]);
        $runtime = new RuntimeOptions([]);
        return $client->deleteIndexWithOptions($workspaceId, $deleteIndexRequest, $headers, $runtime);
    }

    /**
     * 主函数
     */
    public static function main($args) {
        if (!self::checkEnvironmentVariables()) {
            echo "环境变量校验未通过。\n";
            return;
        }

        try {
            echo "请选择要执行的操作：\n1. 查看知识库\n2. 删除知识库\n请输入选项（1或2）：";
            $startOption = trim(fgets(STDIN));
            $client = self::createClient();
            if ($startOption === "1") {
                // 查看知识库
                echo "\n执行查看知识库\n";
                $workspaceId = getenv("WORKSPACE_ID");
                $response = self::listIndices($client, $workspaceId);
                // 将响应转换为 JSON 字符串
                $result = json_encode($response->body->data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
                echo $result . "\n";
            } elseif ($startOption === "2") {
                echo "\n执行删除知识库\n";
                $workspaceId = getenv("WORKSPACE_ID");
                $indexId = readline("请输入知识库ID："); // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
                // 删除前二次确认
                while (true) {
                    $confirm = strtolower(trim(readline("您确定要永久性删除该知识库 $indexId 吗？(y/n): ")));
                    if ($confirm === 'y') {
                        break;
                    } elseif ($confirm === 'n') {
                        echo "已取消删除操作。\n";
                        return;
                    } else {
                        echo "无效输入，请输入 y 或 n。\n";
                    }
                }
                $response = self::deleteIndex($client, $workspaceId, $indexId);
                if ($response->body->status == "200")
                    echo "知识库" . $indexId . "删除成功！\n";
                else 
                    echo "发生错误：" . json_encode($response->body) . "\n";
            } else {
                echo "无效的选项，程序退出。\n";
            }
        } catch (Exception $e) {
            echo "发生错误：" . $e->getMessage() . "\n";
        }
    }
}
// 假定autoload.php位于当前代码文件所在目录的上一级目录中，请根据您的项目实际结构调整。
$path = __DIR__ . \DIRECTORY_SEPARATOR . '..' . \DIRECTORY_SEPARATOR . 'vendor' . \DIRECTORY_SEPARATOR . 'autoload.php';
if (file_exists($path)) {
    require_once $path;
}
KnowledgeBaseManage::main(array_slice($argv, 1));
```

## Node.js

```
// 示例代码仅供参考，请勿在生产环境中直接使用
'use strict';

const bailian20231229 = require('@alicloud/bailian20231229');
const OpenApi = require('@alicloud/openapi-client');
const Util = require('@alicloud/tea-util');
const Tea = require('@alicloud/tea-typescript');

class KbManage {

    /**
     * 检查并提示设置必要的环境变量
     * @returns {boolean} - 如果所有必需的环境变量都已设置，返回 true；否则返回 false
     */
    static checkEnvironmentVariables() {
        const requiredVars = {
            'ALIBABA_CLOUD_ACCESS_KEY_ID': '阿里云访问密钥ID',
            'ALIBABA_CLOUD_ACCESS_KEY_SECRET': '阿里云访问密钥密码',
            'WORKSPACE_ID': '阿里云百炼业务空间ID'
        };

        const missing = [];
        for (const [varName, desc] of Object.entries(requiredVars)) {
            if (!process.env[varName]) {
                console.error(`错误：请设置 ${varName} 环境变量 (${desc})`);
                missing.push(varName);
            }
        }

        return missing.length === 0;
    }

    /**
     * 创建并配置客户端（Client）
     * @return Client
     * @throws Exception
     */
    static createClient() {
        const config = new OpenApi.Config({
            accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
            accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET
        });
        // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址
        config.endpoint = 'bailian.cn-beijing.aliyuncs.com';
        return new bailian20231229.default(config);
    }

    /**
     * 获取指定业务空间下一个或多个知识库的详细信息
     * @param {bailian20231229.Client} client 客户端（Client）
     * @param {string} workspaceId 业务空间ID
     * @returns {Promise<bailian20231229.ListIndicesResponse>} 阿里云百炼服务的响应
     */
    static async listIndices(client, workspaceId) {
        const headers = {};
        const listIndicesRequest = new bailian20231229.ListIndicesRequest();
        const runtime = new Util.RuntimeOptions({});
        return await client.listIndicesWithOptions(workspaceId, listIndicesRequest, headers, runtime);
    }

    /**
     * 永久性删除指定的知识库
     * @param {bailian20231229.Client} client 客户端（Client）
     * @param {string} workspaceId 业务空间ID
     * @param {string} indexId 知识库ID
     * @returns {Promise<bailian20231229.DeleteIndexResponse>} 阿里云百炼服务的响应
     */
    static async deleteIndex(client, workspaceId, indexId) {
        const headers = {};
        const deleteIndexRequest = new bailian20231229.DeleteIndexRequest({
            indexId
        });
        const runtime = new Util.RuntimeOptions({});
        return await client.deleteIndexWithOptions(workspaceId, deleteIndexRequest, headers, runtime);
    }

    /**
     * 使用阿里云百炼服务执行操作（查看或删除知识库）
     */
    static async main(args) {
        if (!this.checkEnvironmentVariables()) {
            console.log("环境变量校验未通过。");
            return;
        }

        const readline = require('readline').createInterface({
            input: process.stdin,
            output: process.stdout
        });

        try {
            const startOption = await new Promise((resolve) => {
                readline.question("请选择要执行的操作：\n1. 查看知识库\n2. 删除知识库\n请输入选项（1或2）：", (ans) => {
                    resolve(ans.trim());
                });
            });

            if (startOption === '1') {
                console.log("\n执行查看知识库");
                const workspaceId = process.env.WORKSPACE_ID;
                const client = this.createClient();
                const response = await this.listIndices(client, workspaceId);
                console.log(JSON.stringify(response.body.data));
            } else if (startOption === '2') {
                console.log("\n执行删除知识库");
                const workspaceId = process.env.WORKSPACE_ID;
                const indexId = await new Promise((resolve) => {
                    readline.question("请输入知识库ID：", (ans) => { // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
                        resolve(ans.trim());
                    });
                });
                // 删除前二次确认
                let confirm = '';
                while (confirm !== 'y' && confirm !== 'n') {
                    confirm = (await new Promise((resolve) => {
                        readline.question(`您确定要永久性删除该知识库 ${indexId} 吗？(y/n): `, (ans) => {
                            resolve(ans.trim().toLowerCase());
                        });
                    })).toLowerCase();
                    if (confirm === 'n') {
                        console.log("已取消删除操作。");
                        return;
                    } else if (confirm !== 'y') {
                        console.log("无效输入，请输入 y 或 n。");
                    }
                }
                const client = this.createClient();
                const resp = await this.deleteIndex(client, workspaceId, indexId);
                if (resp.body.status == '200')
                    console.log(`知识库${indexId}删除成功！`);
                else {
                    const errInfo = JSON.stringify(resp.body);
                    console.error(`发生错误：${errInfo}`)
                }
            } else {
                console.log("无效的选项，程序退出。");
            }
        } catch (err) {
            console.error(`发生错误：${err.message}`);
        } finally {
            readline.close();
        }
    }
}

exports.KbManage = KbManage;
KbManage.main(process.argv.slice(2));
```

## C#

```
// 示例代码仅供参考，请勿在生产环境中直接使用
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Text;

using Newtonsoft.Json;
using Tea;
using Tea.Utils;

namespace AlibabaCloud.SDK.KnowledgeBase
{
    public class KnowledgeBaseManage
    {
        /// <summary>
        /// 检查并提示设置必要的环境变量。
        /// </summary>
        /// <returns>如果所有必需的环境变量都已设置，返回 true；否则返回 false。</returns>
        public static bool CheckEnvironmentVariables()
        {
            var requiredVars = new Dictionary<string, string>
            {
                { "ALIBABA_CLOUD_ACCESS_KEY_ID", "阿里云访问密钥ID" },
                { "ALIBABA_CLOUD_ACCESS_KEY_SECRET", "阿里云访问密钥密码" },
                { "WORKSPACE_ID", "阿里云百炼业务空间ID" }
            };

            var missingVars = new List<string>();
            foreach (var entry in requiredVars)
            {
                string value = Environment.GetEnvironmentVariable(entry.Key);
                if (string.IsNullOrEmpty(value))
                {
                    missingVars.Add(entry.Key);
                    Console.WriteLine($"错误：请设置 {entry.Key} 环境变量（{entry.Value}）");
                }
            }

            return missingVars.Count == 0;
        }

        /// <summary>
        /// 初始化客户端（Client）。
        /// </summary>
        /// <returns>配置好的客户端对象</returns>
        /// <exception cref="Exception">初始化过程中发生错误时抛出异常</exception>
        public static AlibabaCloud.SDK.Bailian20231229.Client CreateClient()
        {
            var config = new AlibabaCloud.OpenApiClient.Models.Config
            {
                AccessKeyId = Environment.GetEnvironmentVariable("ALIBABA_CLOUD_ACCESS_KEY_ID"),
                AccessKeySecret = Environment.GetEnvironmentVariable("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
            };
            // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
            config.Endpoint = "bailian.cn-beijing.aliyuncs.com";
            return new AlibabaCloud.SDK.Bailian20231229.Client(config);
        }

        /// <summary>
        /// 获取指定业务空间下一个或多个知识库的详细信息。
        /// </summary>
        /// <param name="client">客户端（Client）</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <returns>阿里云百炼服务的响应</returns>
        public static AlibabaCloud.SDK.Bailian20231229.Models.ListIndicesResponse ListIndices(AlibabaCloud.SDK.Bailian20231229.Client client, string workspaceId)
        {
            var headers = new Dictionary<string, string>() { };
            var listIndicesRequest = new Bailian20231229.Models.ListIndicesRequest();
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.ListIndicesWithOptions(workspaceId, listIndicesRequest, headers, runtime);
        }

        /// <summary>
        /// 永久性删除指定的知识库。
        /// </summary>
        /// <param name="client">客户端（Client）</param>
        /// <param name="workspaceId">业务空间ID</param>
        /// <param name="indexId">知识库ID</param>
        /// <returns>阿里云百炼服务的响应</returns>
        public static AlibabaCloud.SDK.Bailian20231229.Models.DeleteIndexResponse DeleteIndex(AlibabaCloud.SDK.Bailian20231229.Client client, string workspaceId, string indexId)
        {
            var headers = new Dictionary<string, string>() { };
            var deleteIndexRequest = new Bailian20231229.Models.DeleteIndexRequest
            {
                IndexId = indexId
            };
            var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
            return client.DeleteIndexWithOptions(workspaceId, deleteIndexRequest, headers, runtime);
        }

        /// <summary>
        /// 主函数
        /// </summary>
        public static void Main(string[] args)
        {
            if (!CheckEnvironmentVariables())
            {
                Console.WriteLine("环境变量校验未通过。");
                return;
            }
            try
            {
                Console.Write("请选择要执行的操作：\n1. 查看知识库\n2. 删除知识库\n请输入选项（1或2）：");
                string startOption = Console.ReadLine();
                if (startOption == "1")
                {
                    Console.WriteLine("\n执行查看知识库");
                    string workspaceId = Environment.GetEnvironmentVariable("WORKSPACE_ID");
                    Bailian20231229.Client client = CreateClient();
                    Bailian20231229.Models.ListIndicesResponse listIndicesResponse = ListIndices(client, workspaceId);
                    // 请自行安装Newtonsoft.Json。将响应对象转为 JSON 字符串输出
                    var json = JsonConvert.SerializeObject(listIndicesResponse.Body.Data, Formatting.Indented);
                    Console.WriteLine(json);
                }
                else if (startOption == "2")
                {
                    Console.WriteLine("\n执行删除知识库");
                    string workspaceId = Environment.GetEnvironmentVariable("WORKSPACE_ID");
                    Console.Write("请输入知识库ID："); // 即 CreateIndex 接口返回的 Data.Id，您也可以在阿里云百炼控制台的知识库页面获取。
                    string indexId = Console.ReadLine();
                    // 删除前二次确认
                    while (true)
                    {
                        Console.Write($"您确定要永久性删除该知识库 {indexId} 吗？(y/n): ");
                        string confirm = Console.ReadLine()?.ToLower();
                        if (confirm == "y")
                        {
                            break;
                        }
                        else if (confirm == "n")
                        {
                            Console.WriteLine("已取消删除操作。");
                            return;
                        }
                        else
                        {
                            Console.WriteLine("无效输入，请输入 y 或 n。");
                        }
                    }
                    Bailian20231229.Client client = CreateClient();
                    Bailian20231229.Models.DeleteIndexResponse resp = DeleteIndex(client, workspaceId, indexId);
                    if (resp.Body.Status == "200")
                    {
                        Console.WriteLine($"知识库{indexId}删除成功！");
                    }
                    else
                    {
                        var mapper = new JsonSerializerSettings { Formatting = Formatting.Indented };
                        string errInfo = JsonConvert.SerializeObject(resp.Body, mapper);
                        Console.WriteLine($"发生错误：{errInfo}");
                    }
                }
                else
                {
                    Console.WriteLine("无效的选项，程序退出。");
                    return;
                }
            }
            catch (Exception e)
            {
                Console.WriteLine("发生错误：" + e.Message);
            }
        }
    }
}
```

## Go

```
// 示例代码仅供参考，请勿在生产环境中直接使用
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	bailian20231229 "github.com/alibabacloud-go/bailian-20231229/v2/client"
	openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client"
	util "github.com/alibabacloud-go/tea-utils/v2/service"
	"github.com/alibabacloud-go/tea/tea"
)

// checkEnvironmentVariables 检查并提示设置必要的环境变量。
func checkEnvironmentVariables() bool {
	// 必要的环境变量及其描述
	requiredVars := map[string]string{
		"ALIBABA_CLOUD_ACCESS_KEY_ID":     "阿里云访问密钥ID",
		"ALIBABA_CLOUD_ACCESS_KEY_SECRET": "阿里云访问密钥密码",
		"WORKSPACE_ID":                    "阿里云百炼业务空间ID",
	}

	var missingVars []string
	for varName, desc := range requiredVars {
		if os.Getenv(varName) == "" {
			fmt.Printf("错误：请设置 %s 环境变量 (%s)\n", varName, desc)
			missingVars = append(missingVars, varName)
		}
	}

	return len(missingVars) == 0
}

// createClient 创建并配置客户端（Client）。
//
// 返回:
//   - *client.Bailian20231229Client: 配置好的客户端（Client）。
func createClient() (_result *bailian20231229.Client, _err error) {
	config := &openapi.Config{
		AccessKeyId:     tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")),
		AccessKeySecret: tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")),
	}
	// 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
	config.Endpoint = tea.String("bailian.cn-beijing.aliyuncs.com")
	_result = &bailian20231229.Client{}
	_result, _err = bailian20231229.NewClient(config)
	return _result, _err
}

// listIndices 获取指定业务空间下一个或多个知识库的详细信息。
//
// 参数:
//   - client      *bailian20231229.Client: 客户端（Client）。
//   - workspaceId string: 业务空间ID。
//
// 返回:
//   - *bailian20231229.ListIndicesResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func listIndices(client *bailian20231229.Client, workspaceId string) (_result *bailian20231229.ListIndicesResponse, _err error) {
	headers := make(map[string]*string)
	listIndicesRequest := &bailian20231229.ListIndicesRequest{}
	runtime := &util.RuntimeOptions{}
	return client.ListIndicesWithOptions(tea.String(workspaceId), listIndicesRequest, headers, runtime)
}

// deleteIndex 永久性删除指定的知识库。
//
// 参数:
//   - client      *bailian20231229.Client: 客户端（Client）。
//   - workspaceId string: 业务空间ID。
//   - indexId     string: 知识库ID。
//
// 返回:
//   - *bailian20231229.DeleteIndexResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func deleteIndex(client *bailian20231229.Client, workspaceId, indexId string) (_result *bailian20231229.DeleteIndexResponse, _err error) {
	headers := make(map[string]*string)
	deleteIndexRequest := &bailian20231229.DeleteIndexRequest{
		IndexId: tea.String(indexId),
	}
	runtime := &util.RuntimeOptions{}
	return client.DeleteIndexWithOptions(tea.String(workspaceId), deleteIndexRequest, headers, runtime)

}

// 主函数。
func main() {
	if !checkEnvironmentVariables() {
		fmt.Println("环境变量校验未通过。")
		return
	}

	scanner := bufio.NewScanner(os.Stdin)
	fmt.Print("请选择要执行的操作：\n1. 查看知识库\n2. 删除知识库\n请输入选项（1或2）：")

	// 确保读取输入
	if !scanner.Scan() {
		fmt.Println("无法读取输入。")
		return
	}
	startOption := scanner.Text()

	client, err := createClient()
	if err != nil {
		fmt.Println("创建客户端失败:", err)
		return
	}

	if strings.TrimSpace(startOption) == "1" {
		fmt.Println("\n执行查看知识库")
		workspaceId := os.Getenv("WORKSPACE_ID")
		resp, err := listIndices(client, workspaceId)
		if err != nil {
			fmt.Println("获取知识库列表失败:", err)
			return
		}
		fmt.Printf("知识库列表:\n%+v\n", resp.Body.Data)
	} else if strings.TrimSpace(startOption) == "2" {
		fmt.Println("\n执行删除知识库")
		workspaceId := os.Getenv("WORKSPACE_ID")
		fmt.Print("请输入知识库ID：")
		if !scanner.Scan() {
			fmt.Println("无法读取知识库ID。")
			return
		}
		indexId := scanner.Text()
		for {
			fmt.Printf("您确定要永久性删除该知识库 %s 吗？(y/n): ", indexId)
			if !scanner.Scan() {
				fmt.Println("无法读取确认输入。")
				return
			}
			confirm := strings.ToLower(strings.TrimSpace(scanner.Text()))

			if confirm == "y" {
				break
			} else if confirm == "n" {
				fmt.Println("已取消删除操作。")
				return
			} else {
				fmt.Println("无效输入，请输入 y 或 n。")
			}
		}
		resp, err := deleteIndex(client, workspaceId, indexId)
		if err != nil {
			fmt.Println("删除知识库失败:", err)
		} else {
			if tea.StringValue(resp.Body.Status) == "200" {
				fmt.Printf("知识库 %s 删除成功！\n", indexId)
			} else {
				fmt.Println(resp.Body)
			}
		}
	} else {
		fmt.Println("无效的选项，程序退出。")
	}
}
```

## **创建知识库**

接下来通过示例，引导您在给定的业务空间下创建一个文档搜索类知识库。

### **1\. 初始化客户端**

在开始上传文件和创建知识库之前，您需要使用[配置好的AccessKey和AccessKey Secret](#a4a15bd543can)初始化客户端（Client），以完成身份验证和接入点`endpoint`配置。

-   **公网接入地址：**
    
    > 请确保您的客户端可以访问公网。
    
    -   公有云：`bailian.cn-beijing.aliyuncs.com`
        
-   **VPC接入地址：**
    
    > 若您的客户端部署在阿里云北京地域`cn-beijing`（公有云），且处于[VPC](https://help.aliyun.com/zh/vpc/what-is-vpc)网络环境中，可以使用以下VPC接入地址（不支持跨地域访问）。
    
    -   公有云：`bailian-vpc.cn-beijing.aliyuncs.com`
        

创建完成后，您将得到一个Client对象，用于后续的 API 调用。

## Python

```
def create_client() -> bailian20231229Client:
    """
    创建并配置客户端（Client）。

    返回:
        bailian20231229Client: 配置好的客户端（Client）。
    """
    config = open_api_models.Config(
        access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    )
    # 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
    config.endpoint = 'bailian.cn-beijing.aliyuncs.com'
    return bailian20231229Client(config)
```

## Java

```
/**
 * 初始化客户端（Client）。
 *
 * @return 配置好的客户端对象
 */
public com.aliyun.bailian20231229.Client createClient() throws Exception {
    com.aliyun.teaopenapi.models.Config config = new com.aliyun.teaopenapi.models.Config()
            .setAccessKeyId(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"))
            .setAccessKeySecret(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"));
    // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
    config.endpoint = "bailian.cn-beijing.aliyuncs.com";
    return new com.aliyun.bailian20231229.Client(config);
}
```

## PHP

```
/**
 * 初始化客户端（Client）。
 *
 * @return Bailian 配置好的客户端对象（Client）。
 */
public function createClient(){
    $config = new Config([
        "accessKeyId" => getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"), 
        "accessKeySecret" => getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    ]);
    // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
    $config->endpoint = 'bailian.cn-beijing.aliyuncs.com';
    return new Bailian($config);
}
```

## Node.js

```
/**
 * 创建并配置客户端（Client）
 * @return Client
 * @throws Exception
 */
function createClient() {
  const config = new OpenApi.Config({
    accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID,
    accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET
  });
  // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址
  config.endpoint = `bailian.cn-beijing.aliyuncs.com`;
  return new bailian20231229.default(config);
}
```

## C#

```
/// <summary>
/// 初始化客户端（Client）。
/// </summary>
/// <returns>配置好的客户端对象</returns>
/// <exception cref="Exception">初始化过程中发生错误时抛出异常</exception>
public AlibabaCloud.SDK.Bailian20231229.Client CreateClient()
{
    var config = new AlibabaCloud.OpenApiClient.Models.Config
    {
        AccessKeyId = Environment.GetEnvironmentVariable("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        AccessKeySecret = Environment.GetEnvironmentVariable("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    };
    // 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址.
    config.Endpoint = "bailian.cn-beijing.aliyuncs.com";
    return new AlibabaCloud.SDK.Bailian20231229.Client(config);
}
```

## Go

```
// CreateClient 创建并配置客户端（Client）。
//
// 返回:
//   - *client.Bailian20231229Client: 配置好的客户端（Client）。
//   - error: 错误信息。
func CreateClient() (_result *bailian20231229.Client, _err error) {
	config := &openapi.Config{
		AccessKeyId:     tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")),
		AccessKeySecret: tea.String(os.Getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")),
	}
	// 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
	config.Endpoint = tea.String("bailian.cn-beijing.aliyuncs.com")
	_result = &bailian20231229.Client{}
	_result, _err = bailian20231229.NewClient(config)
	return _result, _err
}
```

### **2\. 上传知识库文件**

#### **2.1. 申请文件上传租约**

在创建知识库前，您需先将文件上传至**同一业务空间**，作为知识库的知识来源。上传文件前，需调用[ApplyFileUploadLease接口](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-applyfileuploadlease)申请一个文件上传租约。该租约是一个临时的授权，允许您在限定时间内（有效期为分钟级）上传文件。

-   **workspace\_id：**[如何获取业务空间ID](https://help.aliyun.com/zh/model-studio/use-workspace#c5222ec081sbo)
    
-   **category\_id：**本示例中，请传入`default`。阿里云百炼使用类目管理您上传的文件，系统会自动创建一个默认类目。您亦可调用[AddCategory接口](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-addcategory)创建新类目，并获取对应的`category_id`。
    
-   **file\_name：**请传入上传文件的名称（包括后缀）。其值必须与实际文件名一致。例如，上传图中的文件时，请传入`阿里云百炼系列手机产品介绍.docx`。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5825785471/p904944.png)
    
-   **file\_md5：**请传入上传文件的MD5值（但当前阿里云不对该值进行校验，便于您使用URL地址上传文件）。
    
    > 以Python为例，MD5值可使用hashlib模块获取。其他语言请参见[完整示例代码](#17d78ffbdafbj)。
    
    **代码示例**
    
    ```
    import hashlib
    
    
    def calculate_md5(file_path):
        """
        计算文件的MD5值。
    
        参数:
            file_path (str): 文件本地路径。
    
        返回:
            str: 文件的MD5值。
        """
        md5_hash = hashlib.md5()
    
        # 以二进制形式读取文件
        with open(file_path, "rb") as f:
            # 按块读取文件，避免大文件占用过多内存
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
    
        return md5_hash.hexdigest()
    
    
    # 使用示例
    file_path = "请替换为您需要上传文件的实际本地路径，例如/xxx/xxx/xxx/阿里云百炼系列手机产品介绍.docx"
    md5_value = calculate_md5(file_path)
    print(f"文件的MD5值为: {md5_value}")
    ```
    
    将代码中的`file_path`变量替换为文件的实际本地路径后运行，即可获取目标文件的MD5值（下方为示例值）：
    
    ```
    文件的MD5值为: 2ef7361ea907f3a1b91e3b9936f5643a
    ```
    
-   **file\_size：**请传入上传文件的字节大小。
    
    > 以Python为例，该值可使用os模块获取。其他语言请参见[完整示例代码](#17d78ffbdafbj)。
    
    **代码示例**
    
    ```
    import os
    
    
    def get_file_size(file_path: str) -> int:
        """
        获取文件的字节大小（以字节为单位）。
    
        参数:
            file_path (str): 文件的实际本地路径。
    
        返回:
            int: 文件大小（以字节为单位）。
        """
        return os.path.getsize(file_path)
    
    
    # 使用示例
    file_path = "请替换为您需要上传文件的实际本地路径，例如/xxx/xxx/xxx/阿里云百炼系列手机产品介绍.docx"
    file_size = get_file_size(file_path)
    print(f"文件的字节大小为: {file_size}")
    ```
    
    将代码中的`file_path`变量替换为文件的实际本地路径后运行，即可获取目标文件的字节大小（下方为示例值）：
    
    ```
    文件的字节大小为: 14015
    ```
    

申请临时上传租约成功后，您将获得：

-   **一组临时上传参数：**
    
    -   `Data.FileUploadLeaseId`
        
    -   `Data.Param.Method`
        
    -   `Data.Param.Headers`中的`X-bailian-extra`
        
    -   `Data.Param.Headers`中的`Content-Type`
        
-   **一个临时上传URL：**`Data.Param.Url`
    

您将在下一步中用到它们。

**重要**

-   子账号调用本示例前需获取[API权限](https://help.aliyun.com/zh/model-studio/member-management#a2e8c1d6246s2)（AliyunBailianDataFullAccess策略）。
    
-   本示例支持[在线调试](https://api.aliyun.com/api/bailian/2023-12-29/ApplyFileUploadLease)及多语言[代码示例生成](https://api.aliyun.com/api/bailian/2023-12-29/ApplyFileUploadLease?lang=JAVA&tab=DEMO)。
    

## Python

```
def apply_lease(client, category_id, file_name, file_md5, file_size, workspace_id):
    """
    从阿里云百炼服务申请文件上传租约。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        category_id (str): 类目ID。
        file_name (str): 文件名称。
        file_md5 (str): 文件的MD5值。
        file_size (int): 文件大小（以字节为单位）。
        workspace_id (str): 业务空间ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    request = bailian_20231229_models.ApplyFileUploadLeaseRequest(
        file_name=file_name,
        md_5=file_md5,
        size_in_bytes=file_size,
    )
    runtime = util_models.RuntimeOptions()
    return client.apply_file_upload_lease_with_options(category_id, workspace_id, request, headers, runtime)
```

## Java

```
/**
 * 申请文件上传租约。
 *
 * @param client      客户端对象
 * @param categoryId  类目ID
 * @param fileName    文件名称
 * @param fileMd5     文件的MD5值
 * @param fileSize    文件大小（以字节为单位）
 * @param workspaceId 业务空间ID
 * @return 阿里云百炼服务的响应对象
 */
public ApplyFileUploadLeaseResponse applyLease(com.aliyun.bailian20231229.Client client, String categoryId, String fileName, String fileMd5, String fileSize, String workspaceId) throws Exception {
    Map<String, String> headers = new HashMap<>();
    com.aliyun.bailian20231229.models.ApplyFileUploadLeaseRequest applyFileUploadLeaseRequest = new com.aliyun.bailian20231229.models.ApplyFileUploadLeaseRequest();
    applyFileUploadLeaseRequest.setFileName(fileName);
    applyFileUploadLeaseRequest.setMd5(fileMd5);
    applyFileUploadLeaseRequest.setSizeInBytes(fileSize);
    com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
    ApplyFileUploadLeaseResponse applyFileUploadLeaseResponse = null;
    applyFileUploadLeaseResponse = client.applyFileUploadLeaseWithOptions(categoryId, workspaceId, applyFileUploadLeaseRequest, headers, runtime);
    return applyFileUploadLeaseResponse;
}
```

## PHP

```
/**
 * 申请文件上传租约。
 *
 * @param Bailian $client 客户端（Client）。
 * @param string $categoryId 类目ID。
 * @param string $fileName 文件名称。
 * @param string $fileMd5 文件的MD5值。
 * @param int $fileSize 文件大小（以字节为单位）。
 * @param string $workspaceId 业务空间ID。
 * @return ApplyFileUploadLeaseResponse 阿里云百炼服务的响应。
 */
public function applyLease($client, $categoryId, $fileName, $fileMd5, $fileSize, $workspaceId) {
    $headers = [];
    $applyFileUploadLeaseRequest = new ApplyFileUploadLeaseRequest([
        "fileName" => $fileName,
        "md5" => $fileMd5,
        "sizeInBytes" => $fileSize
    ]);
    $runtime = new RuntimeOptions([]);
    return $client->applyFileUploadLeaseWithOptions($categoryId, $workspaceId, $applyFileUploadLeaseRequest, $headers, $runtime);
}
```

## Node.js

```
/**
 * 申请文件上传租约
 * @param {Bailian20231229Client} client - 客户端（Client）
 * @param {string} categoryId - 类目ID
 * @param {string} fileName - 文件名称
 * @param {string} fileMd5 - 文件的MD5值
 * @param {string} fileSize - 文件大小（以字节为单位）
 * @param {string} workspaceId - 业务空间ID
 * @returns {Promise<bailian20231229.ApplyFileUploadLeaseResponse>} - 阿里云百炼服务的响应
 */
async function applyLease(client, categoryId, fileName, fileMd5, fileSize, workspaceId) {
  const headers = {};
  const req = new bailian20231229.ApplyFileUploadLeaseRequest({
    md5: fileMd5,
    fileName,
    sizeInBytes: fileSize
 });
 const runtime = new Util.RuntimeOptions({});
 return await client.applyFileUploadLeaseWithOptions(
    categoryId,
    workspaceId,
    req,
    headers,
    runtime
  );
}
```

## C#

```
/// <summary>
/// 申请文件上传租约。
/// </summary>
/// <param name="client">客户端对象</param>
/// <param name="categoryId">类目ID</param>
/// <param name="fileName">文件名称</param>
/// <param name="fileMd5">文件的MD5值</param>
/// <param name="fileSize">文件大小（以字节为单位）</param>
/// <param name="workspaceId">业务空间ID</param>
/// <returns>阿里云百炼服务的响应对象</returns>
/// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
public AlibabaCloud.SDK.Bailian20231229.Models.ApplyFileUploadLeaseResponse ApplyLease(
    AlibabaCloud.SDK.Bailian20231229.Client client,
    string categoryId,
    string fileName,
    string fileMd5,
    string fileSize,
    string workspaceId)
{
    var headers = new Dictionary<string, string>() { };
    var applyFileUploadLeaseRequest = new AlibabaCloud.SDK.Bailian20231229.Models.ApplyFileUploadLeaseRequest
    {
        FileName = fileName,
        Md5 = fileMd5,
        SizeInBytes = fileSize
    };
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.ApplyFileUploadLeaseWithOptions(categoryId, workspaceId, applyFileUploadLeaseRequest, headers, runtime);
}
```

## Go

```
// ApplyLease 从阿里云百炼服务申请文件上传租约。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - categoryId (string): 类目ID。
//   - fileName (string): 文件名称。
//   - fileMD5 (string): 文件的MD5值。
//   - fileSize (string): 文件大小（以字节为单位）。
//   - workspaceId (string): 业务空间ID。
//
// 返回:
//   - *bailian20231229.ApplyFileUploadLeaseResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func ApplyLease(client *bailian20231229.Client, categoryId, fileName, fileMD5 string, fileSize string, workspaceId string) (_result *bailian20231229.ApplyFileUploadLeaseResponse, _err error) {
	headers := make(map[string]*string)
	applyFileUploadLeaseRequest := &bailian20231229.ApplyFileUploadLeaseRequest{
		FileName:    tea.String(fileName),
		Md5:         tea.String(fileMD5),
		SizeInBytes: tea.String(fileSize),
	}
	runtime := &util.RuntimeOptions{}
	return client.ApplyFileUploadLeaseWithOptions(tea.String(categoryId), tea.String(workspaceId), applyFileUploadLeaseRequest, headers, runtime)
}
```

**请求示例**

```
{
  "CategoryId": "default",
  "FileName": "阿里云百炼系列手机产品介绍.docx",
  "Md5": "2ef7361ea907f3a1b91e3b9936f5643a",
  "SizeInBytes": "14015",
  "WorkspaceId": "llm-4u5xpd1xdjqpxxxx"
}
```

**响应示例**

```
{
  "RequestId": "778C0B3B-59C2-5FC1-A947-36EDD1XXXXXX",
  "Success": true,
  "Message": "",
  "Code": "success",
  "Status": "200",
  "Data": {
    "FileUploadLeaseId": "1e6a159107384782be5e45ac4759b247.1719325231035",
    "Type": "HTTP",
    "Param": {
      "Method": "PUT",
      "Url": "https://bailian-datahub-data-origin-prod.oss-cn-hangzhou.aliyuncs.com/1005426495169178/10024405/68abd1dea7b6404d8f7d7b9f7fbd332d.1716698936847.pdf?Expires=1716699536&OSSAccessKeyId=TestID&Signature=HfwPUZo4pR6DatSDym0zFKVh9Wg%3D",
      "Headers": "        \"X-bailian-extra\": \"MTAwNTQyNjQ5NTE2OTE3OA==\",\n        \"Content-Type\": \"application/pdf\""
    }
  }
}
```

#### **2.2. 上传文件到临时存储**

取得上传租约后，您即可使用租约中的临时上传参数和临时上传URL，将本地存储或可通过公网访问的文件上传至阿里云百炼服务器。请注意，每个业务空间最多支持10万个文件。目前支持上传的格式包括：PDF、DOCX、DOC、TXT、Markdown、PPTX、PPT、XLSX、XLS、HTML、PNG、JPG、JPEG、BMP 和 GIF。

-   **pre\_signed\_url：**请传入[申请文件上传租约](#9eb81df79bvkg)时接口返回的`Data.Param.Url`。
    
    > 该 URL 为预签名 URL，不支持 FormData 方式上传，需使用二进制方式上传（详见示例代码）。
    

**重要**

本示例不支持在线调试和多语言示例代码生成。

## 本地上传

## Python

```
import requests
from urllib.parse import urlparse

def upload_file(pre_signed_url, file_path):
    """
    将本地文件上传至临时存储。

    参数:
        pre_signed_url (str): 上传租约中的URL。
        file_path (str): 文件本地路径。
    
    返回:
        阿里云百炼服务的响应。
    """
    try:
        # 设置请求头
        headers = {
            "X-bailian-extra": "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值",
            "Content-Type": "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值（返回空值时，传空值即可）"
        }

        # 读取文件并上传
        with open(file_path, 'rb') as file:
            # 下方设置请求方法用于文件上传，需与您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Method字段的值一致
            response = requests.put(pre_signed_url, data=file, headers=headers)

        # 检查响应状态码
        if response.status_code == 200:
            print("File uploaded successfully.")
        else:
            print(f"Failed to upload the file. ResponseCode: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":

    pre_signed_url_or_http_url = "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值"

    # 将本地文件上传至临时存储
    file_path = "请替换为您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）"
    upload_file(pre_signed_url_or_http_url, file_path)
```

## Java

```
import java.io.DataOutputStream;
import java.io.FileInputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class UploadFile {
    public static void uploadFile(String preSignedUrl, String filePath) {
        HttpURLConnection connection = null;
        try {
            // 创建URL对象
            URL url = new URL(preSignedUrl);
            connection = (HttpURLConnection) url.openConnection();
            // 设置请求方法用于文件上传，需与您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Method字段的值一致
            connection.setRequestMethod("PUT");
            // 允许向connection输出，因为这个连接是用于上传文件的
            connection.setDoOutput(true);
            connection.setRequestProperty("X-bailian-extra", "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值");
            connection.setRequestProperty("Content-Type", "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值（返回空值时，传空值即可）");
            // 读取文件并通过连接上传
            try (DataOutputStream outStream = new DataOutputStream(connection.getOutputStream());
                 FileInputStream fileInputStream = new FileInputStream(filePath)) {
                byte[] buffer = new byte[4096];
                int bytesRead;
                while ((bytesRead = fileInputStream.read(buffer)) != -1) {
                    outStream.write(buffer, 0, bytesRead);
                }
                outStream.flush();
            }
            // 检查响应
            int responseCode = connection.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                // 文件上传成功处理
                System.out.println("File uploaded successfully.");
            } else {
                // 文件上传失败处理
                System.out.println("Failed to upload the file. ResponseCode: " + responseCode);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
    }

    public static void main(String[] args) {
        String preSignedUrlOrHttpUrl = "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值";
        // 将本地文件上传至临时存储
        String filePath = "请替换为您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）";
        uploadFile(preSignedUrlOrHttpUrl, filePath);
    }
}
```

## PHP

```
<?php

/**
 * 将本地文件上传至临时存储
 *
 * @param string $preSignedUrl 从 ApplyFileUploadLease 接口获取的预签名 URL 或 HTTP 地址
 * @param array $headers 包含 "X-bailian-extra" 和 "Content-Type" 的请求头数组
 * @param string $filePath 本地文件路径
 * @throws Exception 如果上传失败
 */
function uploadFile($preSignedUrl, $headers, $filePath) {
    // 读取文件内容
    $fileContent = file_get_contents($filePath);
    if ($fileContent === false) {
        throw new Exception("无法读取文件: " . $filePath);
    }

    // 初始化 cURL 会话
    $ch = curl_init();

    // 设置 cURL 选项
    curl_setopt($ch, CURLOPT_URL, $preSignedUrl);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PUT"); // 使用 PUT 方法
    curl_setopt($ch, CURLOPT_POSTFIELDS, $fileContent); // 设置请求体为文件内容
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true); // 返回响应结果而不是直接输出

    // 构建请求头
    $uploadHeaders = [
        "X-bailian-extra: " . $headers["X-bailian-extra"],
        "Content-Type: " . $headers["Content-Type"]
    ];
    curl_setopt($ch, CURLOPT_HTTPHEADER, $uploadHeaders);

    // 执行请求
    $response = curl_exec($ch);

    // 获取 HTTP 响应码
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

    // 关闭 cURL 会话
    curl_close($ch);

    // 检查响应码
    if ($httpCode != 200) {
        throw new Exception("上传失败，HTTP 状态码: " . $httpCode . "，错误信息: " . $response);
    }

    // 上传成功
    echo "File uploaded successfully.\n";
}

/**
 * 主函数：本地文件上传
 */
function main() {
    // 请替换为您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param 中 Url 字段的值
    $preSignedUrl = "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值";

    // 请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中的 X-bailian-extra 和 Content-Type
    $headers = [
        "X-bailian-extra" => "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值",
        "Content-Type" => "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值（返回空值时，传空值即可）"
    ];

    // 将本地文件上传至临时存储
    $filePath = "请替换为您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）";

    try {
        uploadFile($preSignedUrl, $headers, $filePath);
    } catch (Exception $e) {
        echo "Error: " . $e->getMessage() . "\n";
    }
}

// 调用主函数
main();

?>
```

## Node.js

```
const fs = require('fs');
const axios = require('axios');

/**
 * 将本地文件上传至临时存储
 *
 * @param {string} preSignedUrl - 上传租约中的URL
 * @param {Object} headers - 上传请求的头部
 * @param {string} filePath - 文件本地路径
 * @throws {Error} 如果上传失败
 */
async function uploadFile(preSignedUrl, headers, filePath) {
    // 构建上传所需的请求头
    const uploadHeaders = {
        "X-bailian-extra": headers["X-bailian-extra"],
        "Content-Type": headers["Content-Type"]
    };

    // 创建文件读取流
    const fileStream = fs.createReadStream(filePath);

    try {
        // 使用 axios 发送 PUT 请求
        const response = await axios.put(preSignedUrl, fileStream, {
            headers: uploadHeaders
        });

        // 检查响应状态码
        if (response.status === 200) {
            console.log("File uploaded successfully.");
        } else {
            console.error(`Failed to upload the file. ResponseCode: ${response.status}`);
            throw new Error(`Upload failed with status code: ${response.status}`);
        }
    } catch (error) {
        // 处理错误
        console.error("Error during upload:", error.message);
        throw new Error(`上传失败: ${error.message}`);
    }
}

/**
 * 主函数：本地文件上传
 */
function main() {
    const preSignedUrl = "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值";

    const headers = {
        "X-bailian-extra": "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值",
        "Content-Type": "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值（返回空值时，传空值即可）"
    };

    // 将本地文件上传至临时存储
    const filePath = "请替换为您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）";

    uploadFile(preSignedUrl, headers, filePath)
        .then(() => {
            console.log("Upload completed.");
        })
        .catch((err) => {
            console.error("Upload failed:", err.message);
        });
}

// 调用主函数
main();
```

## C#

```
using System;
using System.IO;
using System.Net;

public class UploadFilExample
{
    public static void UploadFile(string preSignedUrl, string filePath)
    {
        HttpWebRequest connection = null;
        try
        {
            // 创建 URL 对象
            Uri url = new Uri(preSignedUrl);
            connection = (HttpWebRequest)WebRequest.Create(url);
            // 设置请求方法用于文件上传，需与您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param 中 Method 字段的值一致
            connection.Method = "PUT";
            // 允许向 connection 输出，因为这个连接是用于上传文件的
            connection.AllowWriteStreamBuffering = false;
            connection.SendChunked = false;
            // 设置请求头，需与您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param.Headers 中的字段值一致
            connection.Headers["X-bailian-extra"] = "请替换为您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param.Headers 中 X-bailian-extra 字段的值";
            connection.ContentType = "请替换为您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param.Headers 中 Content-Type 字段的值（返回空值时，传空值即可）";
            // 读取文件并通过连接上传
            using (var fileStream = new FileStream(filePath, FileMode.Open, FileAccess.Read))
            using (var requestStream = connection.GetRequestStream())
            {
                byte[] buffer = new byte[4096];
                int bytesRead;
                while ((bytesRead = fileStream.Read(buffer, 0, buffer.Length)) != 0)
                {
                    requestStream.Write(buffer, 0, bytesRead);
                }
                requestStream.Flush();
            }
            // 检查响应
            using (HttpWebResponse response = (HttpWebResponse)connection.GetResponse())
            {
                if (response.StatusCode == HttpStatusCode.OK)
                {
                    // 文件上传成功处理
                    Console.WriteLine("File uploaded successfully.");
                }
                else
                {
                    // 文件上传失败处理
                    Console.WriteLine($"Failed to upload the file. ResponseCode: {response.StatusCode}");
                }
            }
        }
        catch (Exception e)
        {
            Console.WriteLine(e.Message);
            e.StackTrace.ToString();
        }
        finally
        {
            if (connection != null)
            {
                connection.Abort();
            }
        }
    }

    public static void Main(string[] args)
    {
        string preSignedUrlOrHttpUrl = "请替换为您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param 中 Url 字段的值";
        // 将本地文件上传至临时存储
        string filePath = "请替换为您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）";
        UploadFile(preSignedUrlOrHttpUrl, filePath);
    }
}
```

## Go

```
package main

import (
    "fmt"
    "io"
    "os"

    "github.com/go-resty/resty/v2"
)

// UploadFile 将本地文件上传至临时存储。
//
// 参数:
//   - preSignedUrl (string): 上传租约中的 URL。
//   - headers (map[string]string): 上传请求的头部。
//   - filePath (string): 文件本地路径。
//
// 返回:
//   - error: 如果上传失败返回错误信息，否则返回 nil
func UploadFile(preSignedUrl string, headers map[string]string, filePath string) error {
    // 打开本地文件
    file, err := os.Open(filePath)
    if err != nil {
        return fmt.Errorf("打开文件失败: %w", err)
    }
    defer file.Close()

    // 读取内容
    body, err := io.ReadAll(file)
    if err != nil {
        return fmt.Errorf("读取文件失败: %w", err)
    }

    // 创建 REST 客户端
    client := resty.New()

    // 构建上传所需的请求头
    uploadHeaders := map[string]string{
        "X-bailian-extra": headers["X-bailian-extra"],
        "Content-Type":    headers["Content-Type"],
    }

    // 发送 PUT 请求
    resp, err := client.R().
        SetHeaders(uploadHeaders).
        SetBody(body).
        Put(preSignedUrl)

    if err != nil {
        return fmt.Errorf("发送请求失败: %w", err)
    }

    // 检查 HTTP 响应状态码
    if resp.IsError() {
        return fmt.Errorf("HTTP 错误: %d", resp.StatusCode())
    }

    fmt.Println("File uploaded successfully.")
    return nil
}

// main 主函数
func main() {
    // 请替换为您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param 中 Url 字段的值
    preSignedUrl := "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值"

    // 请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中的 X-bailian-extra 和 Content-Type
    headers := map[string]string{
        "X-bailian-extra": "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值",
        "Content-Type":    "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值（返回空值时，传空值即可）",
    }

    // 将本地文件上传至临时存储
    filePath := "请替换为您需要上传文件的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）"

    // 调用上传函数
    err := UploadFile(preSignedUrl, headers, filePath)
    if err != nil {
        fmt.Printf("上传失败: %v\n", err)
    }
}
```

## URL地址上传

> 请确保URL公开可访问且指向一个有效的文件。

## Python

```
import requests
from urllib.parse import urlparse

def upload_file_link(pre_signed_url, source_url_string):
    """
    将可通过公网访问的文件上传至临时存储。

    参数:
        pre_signed_url (str): 上传租约中的 URL。
        source_url_string (str): 文件的URL地址。
    
    返回:
        阿里云百炼服务的响应。
    """
    try:
        # 设置请求头
        headers = {
            "X-bailian-extra": "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值",
            "Content-Type": "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值（返回空值时，传空值即可）"
        }

        # 设置访问文件URL地址的请求方法为GET
        source_response = requests.get(source_url_string)
        if source_response.status_code != 200:
            raise RuntimeError("Failed to get source file.")

        # 下方设置请求方法用于文件上传，需与您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Method字段的值一致
        response = requests.put(pre_signed_url, data=source_response.content, headers=headers)

        # 检查响应状态码
        if response.status_code == 200:
            print("File uploaded successfully.")
        else:
            print(f"Failed to upload the file. ResponseCode: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":

    pre_signed_url_or_http_url = "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值（返回空值时，传空值即可）"

    # 文件的URL地址
    source_url = "请替换为您需要上传文件的URL地址"
    upload_file_link(pre_signed_url_or_http_url, source_url)
```

## Java

```
import java.io.BufferedInputStream;
import java.io.DataOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class UploadFile {
    public static void uploadFileLink(String preSignedUrl, String sourceUrlString) {
        HttpURLConnection connection = null;
        try {
            // 创建URL对象
            URL url = new URL(preSignedUrl);
            connection = (HttpURLConnection) url.openConnection();
            // 设置请求方法用于文件上传，需与您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Method字段的值一致
            connection.setRequestMethod("PUT");
            // 允许向connection输出，因为这个连接是用于上传文件的
            connection.setDoOutput(true);
            connection.setRequestProperty("X-bailian-extra", "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值");
            connection.setRequestProperty("Content-Type", "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值（返回空值时，传空值即可）");
            URL sourceUrl = new URL(sourceUrlString);
            HttpURLConnection sourceConnection = (HttpURLConnection) sourceUrl.openConnection();
            // 设置访问文件URL地址的请求方法为GET
            sourceConnection.setRequestMethod("GET");
            // 获取响应码，200表示请求成功
            int sourceFileResponseCode = sourceConnection.getResponseCode();
            // 从URL地址读取文件并通过连接上传
            if (sourceFileResponseCode != HttpURLConnection.HTTP_OK) {
                throw new RuntimeException("Failed to get source file.");
            }
            try (DataOutputStream outStream = new DataOutputStream(connection.getOutputStream());
                 InputStream in = new BufferedInputStream(sourceConnection.getInputStream())) {
                byte[] buffer = new byte[4096];
                int bytesRead;
                while ((bytesRead = in.read(buffer)) != -1) {
                    outStream.write(buffer, 0, bytesRead);
                }
                outStream.flush();
            }
            // 检查响应
            int responseCode = connection.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                // 文件上传成功
                System.out.println("File uploaded successfully.");
            } else {
                // 文件上传失败
                System.out.println("Failed to upload the file. ResponseCode: " + responseCode);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
    }

    public static void main(String[] args) {
        String preSignedUrlOrHttpUrl = "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值";
        
        String sourceUrl = "请替换为您需要上传文件的URL地址";
        uploadFileLink(preSignedUrlOrHttpUrl, sourceUrl);
    }
}
```

## PHP

```
<?php

/**
 * 将可通过公网访问的文件上传至临时存储
 *
 * @param string $preSignedUrl 从 ApplyFileUploadLease 接口获取的预签名 URL 或 HTTP 地址
 * @param array $headers 包含 "X-bailian-extra" 和 "Content-Type" 的请求头数组
 * @param string $sourceUrl 文件的URL地址
 * @throws Exception 如果上传失败
 */
function uploadFile($preSignedUrl, $headers, $sourceUrl) {

    $fileContent = file_get_contents($sourceUrl);
    if ($fileContent === false) {
        throw new Exception("无法从给定的URL地址下载文件: " . $sourceUrl);
    }
    // 初始化 cURL 会话
    $ch = curl_init();

    // 设置 cURL 选项
    curl_setopt($ch, CURLOPT_URL, $preSignedUrl);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PUT"); // 使用 PUT 方法
    curl_setopt($ch, CURLOPT_POSTFIELDS, $fileContent); // 设置请求体为文件内容
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true); // 返回响应结果而不是直接输出

    // 构建请求头
    $uploadHeaders = [
        "X-bailian-extra: " . $headers["X-bailian-extra"],
        "Content-Type: " . $headers["Content-Type"]
    ];
    curl_setopt($ch, CURLOPT_HTTPHEADER, $uploadHeaders);

    // 执行请求
    $response = curl_exec($ch);

    // 获取 HTTP 响应码
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

    // 关闭 cURL 会话
    curl_close($ch);

    // 检查响应码
    if ($httpCode != 200) {
        throw new Exception("上传失败，HTTP 状态码: " . $httpCode . "，错误信息: " . $response);
    }

    // 上传成功
    echo "File uploaded successfully.\n";
}

/**
 * 主函数：将可通过公网访问的文件上传至临时存储
 */
function main() {
    // 请替换为您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param 中 Url 字段的值
    $preSignedUrl = "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值";

    // 请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中的 X-bailian-extra 和 Content-Type
    $headers = [
        "X-bailian-extra" => "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值",
        "Content-Type" => "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值（返回空值时，传空值即可）"
    ];

    $sourceUrl = "请替换为您需要上传文件的URL地址";

    try {
        uploadFile($preSignedUrl, $headers, $sourceUrl);
    } catch (Exception $e) {
        echo "Error: " . $e->getMessage() . "\n";
    }
}

// 调用主函数
main();

?>
```

## Node.js

```
const axios = require('axios');

/**
 * 将可通过公网访问的文件上传至临时存储
 *
 * @param {string} preSignedUrl - 上传租约中的URL
 * @param {Object} headers - 上传请求的头部
 * @param {string} sourceUrl - 文件的URL地址
 * @throws {Error} 如果上传失败
 */
async function uploadFileFromUrl(preSignedUrl, headers, sourceUrl) {
    // 构建上传所需的请求头
    const uploadHeaders = {
        "X-bailian-extra": headers["X-bailian-extra"],
        "Content-Type": headers["Content-Type"]
    };

    try {
        // 从给定的URL地址下载文件
        const response = await axios.get(sourceUrl, {
            responseType: 'stream'
        });

        // 使用 axios 发送 PUT 请求
        const uploadResponse = await axios.put(preSignedUrl, response.data, {
            headers: uploadHeaders
        });

        // 检查响应状态码
        if (uploadResponse.status === 200) {
            console.log("File uploaded successfully from URL.");
        } else {
            console.error(`Failed to upload the file. ResponseCode: ${uploadResponse.status}`);
            throw new Error(`Upload failed with status code: ${uploadResponse.status}`);
        }
    } catch (error) {
        // 处理错误
        console.error("Error during upload:", error.message);
        throw new Error(`上传失败: ${error.message}`);
    }
}

/**
 * 主函数：将一个可公开直接下载的文件上传到临时存储
 */
function main() {
    const preSignedUrl = "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值";

    const headers = {
        "X-bailian-extra": "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值",
        "Content-Type": "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值（返回空值时，传空值即可）"
    };

    const sourceUrl = "请替换为您需要上传文件的URL地址";

    uploadFileFromUrl(preSignedUrl, headers, sourceUrl)
        .then(() => {
            console.log("Upload completed.");
        })
        .catch((err) => {
            console.error("Upload failed:", err.message);
        });
}

// 调用主函数
main();
```

## C#

```
using System;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;

public class UploadFileExample
{
    public static async Task UploadFileFromUrl(string preSignedUrl, string url)
    {
        try
        {
            // 创建 HTTP 客户端从给定的URL地址下载文件
            using (HttpClient httpClient = new HttpClient())
            {
                HttpResponseMessage response = await httpClient.GetAsync(url, HttpCompletionOption.ResponseHeadersRead);
                response.EnsureSuccessStatusCode();

                // 获取文件流
                using (Stream fileStream = await response.Content.ReadAsStreamAsync())
                {
                    // 创建 URL 对象
                    Uri urlObj = new Uri(preSignedUrl);
                    HttpWebRequest connection = (HttpWebRequest)WebRequest.Create(urlObj);

                    // 设置请求方法用于文件上传
                    connection.Method = "PUT";
                    connection.AllowWriteStreamBuffering = false;
                    connection.SendChunked = false;

                    // 设置请求头（请替换为实际值）
                    connection.Headers["X-bailian-extra"] = "请替换为您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param.Headers 中 X-bailian-extra 字段的值";
                    connection.ContentType = "请替换为您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param.Headers 中 Content-Type 字段的值（返回空值时，传空值即可）";

                    // 获取请求流并写入文件流
                    using (Stream requestStream = connection.GetRequestStream())
                    {
                        byte[] buffer = new byte[4096];
                        int bytesRead;
                        while ((bytesRead = await fileStream.ReadAsync(buffer, 0, buffer.Length)) > 0)
                        {
                            await requestStream.WriteAsync(buffer, 0, bytesRead);
                        }
                        await requestStream.FlushAsync();
                    }

                    // 检查响应
                    using (HttpWebResponse responseResult = (HttpWebResponse)connection.GetResponse())
                    {
                        if (responseResult.StatusCode == HttpStatusCode.OK)
                        {
                            Console.WriteLine("File uploaded successfully from URL.");
                        }
                        else
                        {
                            Console.WriteLine($"Failed to upload the file. ResponseCode: {responseResult.StatusCode}");
                        }
                    }
                }
            }
        }
        catch (Exception e)
        {
            Console.WriteLine(e.Message);
            Console.WriteLine(e.StackTrace);
        }
    }

    public static async Task Main(string[] args)
    {
        string preSignedUrlOrHttpUrl = "请替换为您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param 中 Url 字段的值";
        string url = "请替换为您需要上传文件的URL地址";   

        await UploadFileFromUrl(preSignedUrlOrHttpUrl, url);
    }
}
```

## Go

```
package main
 
import (
    "fmt"
    "net/http"
 
    "github.com/go-resty/resty/v2"
)
 
// UploadFileFromUrl 将可通过公网访问的文件上传至临时存储。
//
// 参数:
//   - preSignedUrl (string): 上传租约中的 URL。
//   - headers (map[string]string): 上传请求的头部。
//   - sourceUrl (string): 文件的URL地址。
//
// 返回:
//   - error: 如果上传失败返回错误信息，否则返回 nil
func UploadFileFromUrl(preSignedUrl string, headers map[string]string, sourceUrl string) error {
    // 从给定的URL地址下载文件
    resp, err := http.Get(sourceUrl)
    if err != nil {
        return fmt.Errorf("获取文件失败: %w", err)
    }
    defer resp.Body.Close()
 
    if resp.StatusCode != http.StatusOK {
        return fmt.Errorf("获取文件失败，状态码: %d", resp.StatusCode)
    }
 
    // 创建 REST 客户端
    client := resty.New()
 
    // 构建上传所需的请求头
    uploadHeaders := map[string]string{
        "X-bailian-extra": headers["X-bailian-extra"],
        "Content-Type":    headers["Content-Type"],
    }
 
    // 发送 PUT 请求
    response, err := client.R().
        SetHeaders(uploadHeaders).
        SetBody(resp.Body).
        Put(preSignedUrl)
 
    if err != nil {
        return fmt.Errorf("发送请求失败: %w", err)
    }
 
    if err != nil {
        return fmt.Errorf("发送请求失败: %w", err)
    }
 
    // 检查 HTTP 响应状态码
    if response.IsError() {
        return fmt.Errorf("HTTP 错误: %d", response.StatusCode())
    }
 
    fmt.Println("File uploaded successfully from URL.")
    return nil
}
 
// main 主函数
func main() {
    // 请替换为您在上一步中调用 ApplyFileUploadLease 接口实际返回的 Data.Param 中 Url 字段的值
    preSignedUrl := "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Url字段的值"
 
    // 请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中的 X-bailian-extra 和 Content-Type
    headers := map[string]string{
        "X-bailian-extra": "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中X-bailian-extra字段的值",
        "Content-Type":    "请替换为您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param.Headers中Content-Type字段的值（返回空值时，传空值即可）",
    }
 
    sourceUrl := "请替换为您需要上传文件的URL地址"
 
    // 调用上传函数
    err := UploadFileFromUrl(preSignedUrl, headers, sourceUrl)
    if err != nil {
        fmt.Printf("上传失败: %v\n", err)
    }
}
```

#### **2.3. 添加文件到类目中**

阿里云百炼使用类目管理您上传的文件。因此，接下来您需要调用[AddFile接口](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-addfile)将已上传的文件添加到同一业务空间下的类目中。

-   **parser：**请传入`DASHSCOPE_DOCMIND`。
    
-   **lease\_id：**请传入[申请文件上传租约](#9eb81df79bvkg)时接口返回的`Data.FileUploadLeaseId`。
    
-   **category\_id：**本示例中，请传入`default`。若您使用了自建类目上传，则需传入对应的`category_id`。
    
    **重要**
    
    请确保此处传入的`CategoryId`与[申请文件上传租约](#9eb81df79bvkg)步骤中使用的`CategoryId`保持一致，否则会出现`Category is mismatched`错误。
    

完成添加后，阿里云百炼将返回该文件的`FileId`，并自动开始解析您的文件。同时`lease_id`（租约ID）随即失效，**请勿再使用相同的租约ID重复提交**。

**重要**

-   子账号调用本示例前需获取[API权限](https://help.aliyun.com/zh/model-studio/member-management#a2e8c1d6246s2)（AliyunBailianDataFullAccess策略）。
    
-   本示例支持[在线调试](https://api.aliyun.com/api/bailian/2023-12-29/AddFile)及多语言[代码示例生成](https://api.aliyun.com/api/bailian/2023-12-29/AddFile?lang=JAVA&tab=DEMO)。
    

## Python

```
def add_file(client: bailian20231229Client, lease_id: str, parser: str, category_id: str, workspace_id: str):
    """
    将文件添加到阿里云百炼服务的指定类目中。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        lease_id (str): 租约ID。
        parser (str): 用于文件的解析器。
        category_id (str): 类目ID。
        workspace_id (str): 业务空间ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    request = bailian_20231229_models.AddFileRequest(
        lease_id=lease_id,
        parser=parser,
        category_id=category_id,
    )
    runtime = util_models.RuntimeOptions()
    return client.add_file_with_options(workspace_id, request, headers, runtime)
```

## Java

```
/**
 * 将文件添加到类目中。
 *
 * @param client      客户端对象
 * @param leaseId     租约ID
 * @param parser      用于文件的解析器
 * @param categoryId  类目ID
 * @param workspaceId 业务空间ID
 * @return 阿里云百炼服务的响应对象
 */
public AddFileResponse addFile(com.aliyun.bailian20231229.Client client, String leaseId, String parser, String categoryId, String workspaceId) throws Exception {
    Map<String, String> headers = new HashMap<>();
    com.aliyun.bailian20231229.models.AddFileRequest addFileRequest = new com.aliyun.bailian20231229.models.AddFileRequest();
    addFileRequest.setLeaseId(leaseId);
    addFileRequest.setParser(parser);
    addFileRequest.setCategoryId(categoryId);
    com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
    return client.addFileWithOptions(workspaceId, addFileRequest, headers, runtime);
}
```

## PHP

```
/**
 * 将文件添加到类目中。
 *
 * @param Bailian $client 客户端（Client）。
 * @param string $leaseId 租约ID。
 * @param string $parser 用于文件的解析器。
 * @param string $categoryId 类目ID。
 * @param string $workspaceId 业务空间ID。
 * @return AddFileResponse 阿里云百炼服务的响应。
 */
public function addFile($client, $leaseId, $parser, $categoryId, $workspaceId) {
    $headers = [];
    $addFileRequest = new AddFileRequest([
        "leaseId" => $leaseId,
        "parser" => $parser,
        "categoryId" => $categoryId
    ]);
    $runtime = new RuntimeOptions([]);
    return $client->addFileWithOptions($workspaceId, $addFileRequest, $headers, $runtime);
}
```

## Node.js

```
/**
 * 添加文件到类目中
 * @param {Bailian20231229Client} client - 客户端（Client）
 * @param {string} leaseId - 租约ID
 * @param {string} parser - 用于文件的解析器
 * @param {string} categoryId - 类目ID
 * @param {string} workspaceId - 业务空间ID
 * @returns {Promise<bailian20231229.AddFileResponse>} - 阿里云百炼服务的响应
 */
async function addFile(client, leaseId, parser, categoryId, workspaceId) {
 const headers = {};
 const req = new bailian20231229.AddFileRequest({
  leaseId,
  parser,
  categoryId
});
 const runtime = new Util.RuntimeOptions({});
 return await client.addFileWithOptions(workspaceId, req, headers, runtime);
}
```

## C#

```
/// <summary>
/// 将文件添加到类目中。
/// </summary>
/// <param name="client">客户端对象</param>
/// <param name="leaseId">租约ID</param>
/// <param name="parser">用于文件的解析器</param>
/// <param name="categoryId">类目ID</param>
/// <param name="workspaceId">业务空间ID</param>
/// <returns>阿里云百炼服务的响应对象</returns>
/// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
public AlibabaCloud.SDK.Bailian20231229.Models.AddFileResponse AddFile(
    AlibabaCloud.SDK.Bailian20231229.Client client,
    string leaseId,
    string parser,
    string categoryId,
    string workspaceId)
{
    var headers = new Dictionary<string, string>() { };
    var addFileRequest = new AlibabaCloud.SDK.Bailian20231229.Models.AddFileRequest
    {
        LeaseId = leaseId,
        Parser = parser,
        CategoryId = categoryId
    };
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.AddFileWithOptions(workspaceId, addFileRequest, headers, runtime);
}
```

## Go

```
// AddFile 将文件添加到阿里云百炼服务的指定类目中。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - leaseId (string): 租约ID。
//   - parser (string): 用于文件的解析器。
//   - categoryId (string): 类目ID。
//   - workspaceId (string): 业务空间ID。
//
// 返回:
//   - *bailian20231229.AddFileResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func AddFile(client *bailian20231229.Client, leaseId, parser, categoryId, workspaceId string) (_result *bailian20231229.AddFileResponse, _err error) {
	headers := make(map[string]*string)
	addFileRequest := &bailian20231229.AddFileRequest{
		LeaseId:    tea.String(leaseId),
		Parser:     tea.String(parser),
		CategoryId: tea.String(categoryId),
	}
	runtime := &util.RuntimeOptions{}
	return client.AddFileWithOptions(tea.String(workspaceId), addFileRequest, headers, runtime)
}
```

**请求示例**

```
{
  "CategoryId": "default",
  "LeaseId": "d92bd94fa9b54326a2547415e100c9e2.1742195250069",
  "Parser": "DASHSCOPE_DOCMIND",
  "WorkspaceId": "llm-4u5xpd1xdjqpxxxx"
}
```

**响应示例**

```
{
  "Status": "200",
  "Message": "",
  "RequestId": "5832A1F4-AF91-5242-8B75-35BDC9XXXXXX",
  "Data": {
    "FileId": "file_0b21e0a852cd40cd9741c54fefbb61cd_10xxxxxx",
    "Parser": "DASHSCOPE_DOCMIND"
  },
  "Code": "Success",
  "Success": "true"
}
```

#### **2.4. 查询文件的解析状态**

未解析完成的文件无法用于知识库，在请求高峰时段，该过程可能需要数小时。您可以调用[DescribeFile接口](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-describefile)查询文件的解析状态。

-   **file\_id：**请传入[添加文件到类目中](#494345d4b1hx2)时接口返回的`FileId`。
    

当本接口返回的`Data.Status`字段值为`PARSE_SUCCESS`时，表示文件已解析完成，可以将其导入知识库。

**重要**

-   子账号调用本示例前需获取[API权限](https://help.aliyun.com/zh/model-studio/member-management#a2e8c1d6246s2)（AliyunBailianDataFullAccess或AliyunBailianDataReadOnlyAccess策略）。
    
-   本示例支持[在线调试](https://api.aliyun.com/api/bailian/2023-12-29/DescribeFile)及多语言[代码示例生成](https://api.aliyun.com/api/bailian/2023-12-29/DescribeFile?lang=JAVA&tab=DEMO)。
    

## Python

```
def describe_file(client, workspace_id, file_id):
    """
    获取文件的基本信息。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        file_id (str): 文件ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    runtime = util_models.RuntimeOptions()
    return client.describe_file_with_options(workspace_id, file_id, headers, runtime)
```

## Java

```
/**
 * 查询文件的基本信息。
 *
 * @param client      客户端对象
 * @param workspaceId 业务空间ID
 * @param fileId      文件ID
 * @return 阿里云百炼服务的响应对象
 */
public DescribeFileResponse describeFile(com.aliyun.bailian20231229.Client client, String workspaceId, String fileId) throws Exception {
    Map<String, String> headers = new HashMap<>();
    com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
    return client.describeFileWithOptions(workspaceId, fileId, headers, runtime);
}
```

## PHP

```
/**
 * 查询文件的基本信息。
 *
 * @param Bailian $client 客户端（Client）。
 * @param string $workspaceId 业务空间ID。
 * @param string $fileId 文件ID。
 * @return DescribeFileResponse 阿里云百炼服务的响应。
 */
public function describeFile($client, $workspaceId, $fileId) {
    $headers = [];
    $runtime = new RuntimeOptions([]);
    return $client->describeFileWithOptions($workspaceId, $fileId, $headers, $runtime);
}
```

## Node.js

```
/**
 * 查询文件的解析状态
 * @param {Bailian20231229Client} client - 客户端（Client）
 * @param {string} workspaceId - 业务空间ID
 * @param {string} fileId - 文件ID
 * @returns {Promise<bailian20231229.DescribeFileResponse>} - 阿里云百炼服务的响应
 */
async function describeFile(client, workspaceId, fileId) {
 const headers = {};
 const runtime = new Util.RuntimeOptions({});
 return await client.describeFileWithOptions(workspaceId, fileId, headers, runtime);
}
```

## C#

```
/// <summary>
/// 查询文件的基本信息。
/// </summary>
/// <param name="client">客户端对象</param>
/// <param name="workspaceId">业务空间ID</param>
/// <param name="fileId">文件ID</param>
/// <returns>阿里云百炼服务的响应对象</returns>
/// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
public AlibabaCloud.SDK.Bailian20231229.Models.DescribeFileResponse DescribeFile(
    AlibabaCloud.SDK.Bailian20231229.Client client,
    string workspaceId,
    string fileId)
{
    var headers = new Dictionary<string, string>() { };
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.DescribeFileWithOptions(workspaceId, fileId, headers, runtime);
}
```

## Go

```
// DescribeFile 获取文件的基本信息。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - fileId (string): 文件ID。
//
// 返回:
//   - any: 阿里云百炼服务的响应。
//   - error: 错误信息。
func DescribeFile(client *bailian20231229.Client, workspaceId, fileId string) (_result *bailian20231229.DescribeFileResponse, _err error) {
	headers := make(map[string]*string)
	runtime := &util.RuntimeOptions{}
	return client.DescribeFileWithOptions(tea.String(workspaceId), tea.String(fileId), headers, runtime)
}
```

**请求示例**

```
{
  "FileId": "file_0b21e0a852cd40cd9741c54fefbb61cd_10xxxxxx",
  "WorkspaceId": "llm-4u5xpd1xdjqpxxxx"
}
```

**响应示例**

```
{
  "Status": "200",
  "Message": "",
  "RequestId": "B9246251-987A-5628-8E1E-17BB39XXXXXX",
  "Data": {
    "CategoryId": "cate_206ea350f0014ea4a324adff1ca13011_10xxxxxx",
    "Status": "PARSE_SUCCESS",
    "FileType": "docx",
    "CreateTime": "2025-03-17 15:47:13",
    "FileName": "阿里云百炼系列手机产品介绍.docx",
    "FileId": "file_0b21e0a852cd40cd9741c54fefbb61cd_10xxxxxx",
    "SizeInBytes": "14015",
    "Parser": "DASHSCOPE_DOCMIND"
  },
  "Code": "Success",
  "Success": "true"
}
```

### **3\. 创建知识库**

#### **3.1. 初始化知识库**

文件解析完成后，您即可将其导入同一业务空间下的知识库。初始化（非最终提交）一个文档搜索类知识库，可以调用[CreateIndex接口](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-createindex)。

-   **workspace\_id：**[如何获取业务空间ID](https://help.aliyun.com/zh/model-studio/use-workspace#c5222ec081sbo)
    
-   **file\_id：**请传入[添加文件到类目中](#494345d4b1hx2)时接口返回的`FileId`。
    
    > 若source\_type为`DATA_CENTER_FILE`，则该参数为必传，否则接口将报错。
    
-   **structure\_type：**本示例中，请传入`unstructured`。
    
-   **source\_type：**本示例中，请传入`DATA_CENTER_FILE`。
    
-   **sink\_type：**本示例中，请传入`BUILT_IN`。
    

本接口返回的`Data.Id`字段值即为知识库ID，用于后续的索引构建。

> 请您妥善保管知识库ID，后续该知识库所有相关API操作都将用到它。

**重要**

-   子账号调用本示例前需获取[API权限](https://help.aliyun.com/zh/model-studio/member-management#a2e8c1d6246s2)（AliyunBailianDataFullAccess策略）。
    
-   本示例支持[在线调试](https://api.aliyun.com/api/bailian/2023-12-29/CreateIndex)及多语言[代码示例生成](https://api.aliyun.com/api/bailian/2023-12-29/CreateIndex?lang=JAVA&tab=DEMO)。
    

## Python

```
def create_index(client, workspace_id, file_id, name, structure_type, source_type, sink_type):
    """
    在阿里云百炼服务中创建知识库（初始化）。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        file_id (str): 文件ID。
        name (str): 知识库名称。
        structure_type (str): 知识库的数据类型。
        source_type (str): 应用数据的数据类型，支持类目类型和文件类型。
        sink_type (str): 知识库的向量存储类型。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    request = bailian_20231229_models.CreateIndexRequest(
        structure_type=structure_type,
        name=name,
        source_type=source_type,
        sink_type=sink_type,
        document_ids=[file_id]
    )
    runtime = util_models.RuntimeOptions()
    return client.create_index_with_options(workspace_id, request, headers, runtime)
```

## Java

```
/**
 * 在阿里云百炼服务中创建知识库（初始化）。
 *
 * @param client        客户端对象
 * @param workspaceId   业务空间ID
 * @param fileId        文件ID
 * @param name          知识库名称
 * @param structureType 知识库的数据类型
 * @param sourceType    应用数据的数据类型，支持类目类型和文件类型
 * @param sinkType      知识库的向量存储类型
 * @return 阿里云百炼服务的响应对象
 */
public CreateIndexResponse createIndex(com.aliyun.bailian20231229.Client client, String workspaceId, String fileId, String name, String structureType, String sourceType, String sinkType) throws Exception {
    Map<String, String> headers = new HashMap<>();
    com.aliyun.bailian20231229.models.CreateIndexRequest createIndexRequest = new com.aliyun.bailian20231229.models.CreateIndexRequest();
    createIndexRequest.setStructureType(structureType);
    createIndexRequest.setName(name);
    createIndexRequest.setSourceType(sourceType);
    createIndexRequest.setSinkType(sinkType);
    createIndexRequest.setDocumentIds(Collections.singletonList(fileId));
    com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
    return client.createIndexWithOptions(workspaceId, createIndexRequest, headers, runtime);
}
```

## PHP

```
/**
 * 在阿里云百炼服务中创建知识库（初始化）。
 *
 * @param Bailian $client 客户端（Client）。
 * @param string $workspaceId 业务空间ID。
 * @param string $fileId 文件ID。
 * @param string $name 知识库名称。
 * @param string $structureType 知识库的数据类型。
 * @param string $sourceType 应用数据的数据类型，支持类目类型和文件类型。
 * @param string $sinkType 知识库的向量存储类型。
 * @return CreateIndexResponse 阿里云百炼服务的响应。
 */
public function createIndex($client, $workspaceId, $fileId, $name, $structureType, $sourceType, $sinkType) {
    $headers = [];
    $createIndexRequest = new CreateIndexRequest([
        "structureType" => $structureType,
        "name" => $name,
        "sourceType" => $sourceType,
        "documentIds" => [
            $fileId
        ],
        "sinkType" => $sinkType
    ]);
    $runtime = new RuntimeOptions([]);
    return $client->createIndexWithOptions($workspaceId, $createIndexRequest, $headers, $runtime);
}
```

## Node.js

```
/**
 * 初始化知识库（索引）
 * @param {Bailian20231229Client} client - 客户端（Client）
 * @param {string} workspaceId - 业务空间ID
 * @param {string} fileId - 文件ID
 * @param {string} name - 知识库名称
 * @param {string} structureType - 知识库的数据类型
 * @param {string} sourceType - 应用数据的数据类型，支持类目类型和文件类型
 * @param {string} sinkType - 知识库的向量存储类型
 * @returns {Promise<bailian20231229.CreateIndexResponse>} - 阿里云百炼服务的响应
 */
async function createIndex(client, workspaceId, fileId, name, structureType, sourceType, sinkType) {
 const headers = {};
 const req = new bailian20231229.CreateIndexRequest({
   name,
   structureType,
   documentIds: [fileId],
   sourceType,
   sinkType
 });
 const runtime = new Util.RuntimeOptions({});
 return await client.createIndexWithOptions(workspaceId, req, headers, runtime);
}
```

## C#

```
/// <summary>
/// 在阿里云百炼服务中创建知识库（初始化）。
/// </summary>
/// <param name="client">客户端对象</param>
/// <param name="workspaceId">业务空间ID</param>
/// <param name="fileId">文件ID</param>
/// <param name="name">知识库名称</param>
/// <param name="structureType">知识库的数据类型</param>
/// <param name="sourceType">应用数据的数据类型，支持类目类型和文件类型</param>
/// <param name="sinkType">知识库的向量存储类型</param>
/// <returns>阿里云百炼服务的响应对象</returns>
/// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
public AlibabaCloud.SDK.Bailian20231229.Models.CreateIndexResponse CreateIndex(
    AlibabaCloud.SDK.Bailian20231229.Client client,
    string workspaceId,
    string fileId,
    string name,
    string structureType,
    string sourceType,
    string sinkType)
{
    var headers = new Dictionary<string, string>() { };
    var createIndexRequest = new AlibabaCloud.SDK.Bailian20231229.Models.CreateIndexRequest
    {
        StructureType = structureType,
        Name = name,
        SourceType = sourceType,
        SinkType = sinkType,
        DocumentIds = new List<string> { fileId }
    };
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.CreateIndexWithOptions(workspaceId, createIndexRequest, headers, runtime);
}
```

## Go

```
// CreateIndex 在阿里云百炼服务中创建知识库（初始化）。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - fileId (string): 文件ID。
//   - name (string): 知识库名称。
//   - structureType (string): 知识库的数据类型。
//   - sourceType (string): 应用数据的数据类型，支持类目类型和文件类型。
//   - sinkType (string): 知识库的向量存储类型。
//
// 返回:
//   - *bailian20231229.CreateIndexResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func CreateIndex(client *bailian20231229.Client, workspaceId, fileId, name, structureType, sourceType, sinkType string) (_result *bailian20231229.CreateIndexResponse, _err error) {
	headers := make(map[string]*string)
	createIndexRequest := &bailian20231229.CreateIndexRequest{
		StructureType: tea.String(structureType),
		Name:          tea.String(name),
		SourceType:    tea.String(sourceType),
		SinkType:      tea.String(sinkType),
		DocumentIds:   []*string{tea.String(fileId)},
	}
	runtime := &util.RuntimeOptions{}
	return client.CreateIndexWithOptions(tea.String(workspaceId), createIndexRequest, headers, runtime)
}
```

**请求示例**

```
{
  "Name": "阿里云百炼手机知识库",
  "SinkType": "BUILT_IN",
  "SourceType": "DATA_CENTER_FILE",
  "StructureType": "unstructured",
  "WorkspaceId": "llm-4u5xpd1xdjqpxxxx",
  "DocumentIds": [
    "file_0b21e0a852cd40cd9741c54fefbb61cd_10xxxxxx"
  ]
}
```

**响应示例**

```
{
  "Status": "200",
  "Message": "success",
  "RequestId": "87CB0999-F1BB-5290-8C79-A875B2XXXXXX",
  "Data": {
    "Id": "mymxbdxxxx"
  },
  "Code": "Success",
  "Success": "true"
}
```

#### **3.2. 提交索引任务**

初始化知识库后，您需要调用[SubmitIndexJob接口](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-submitindexjob)提交索引任务，以启动知识库的索引构建。

-   **index\_id：**请传入[初始化知识库](#00ded5ee90ffx)时接口返回的`Data.Id`。
    

完成提交后，阿里云百炼随即以异步任务方式开始构建索引。本接口返回的`Data.Id`为对应的任务ID。下一步中，您将用到此ID查询任务的最新状态。

**重要**

-   子账号调用本示例前需获取[API权限](https://help.aliyun.com/zh/model-studio/member-management#a2e8c1d6246s2)（AliyunBailianDataFullAccess策略）。
    
-   本示例支持[在线调试](https://api.aliyun.com/api/bailian/2023-12-29/SubmitIndexJob)及多语言[代码示例生成](https://api.aliyun.com/api/bailian/2023-12-29/SubmitIndexJob?lang=JAVA&tab=DEMO)。
    

## Python

```
def submit_index(client, workspace_id, index_id):
    """
    向阿里云百炼服务提交索引任务。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    submit_index_job_request = bailian_20231229_models.SubmitIndexJobRequest(
        index_id=index_id
    )
    runtime = util_models.RuntimeOptions()
    return client.submit_index_job_with_options(workspace_id, submit_index_job_request, headers, runtime)
```

## Java

```
/**
 * 向阿里云百炼服务提交索引任务。
 *
 * @param client      客户端对象
 * @param workspaceId 业务空间ID
 * @param indexId     知识库ID
 * @return 阿里云百炼服务的响应对象
 */
public SubmitIndexJobResponse submitIndex(com.aliyun.bailian20231229.Client client, String workspaceId, String indexId) throws Exception {
    Map<String, String> headers = new HashMap<>();
    com.aliyun.bailian20231229.models.SubmitIndexJobRequest submitIndexJobRequest = new com.aliyun.bailian20231229.models.SubmitIndexJobRequest();
    submitIndexJobRequest.setIndexId(indexId);
    com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
    return client.submitIndexJobWithOptions(workspaceId, submitIndexJobRequest, headers, runtime);
}
```

## PHP

```
/**
 * 向阿里云百炼服务提交索引任务。
 *
 * @param Bailian $client 客户端（Client）。
 * @param string $workspaceId 业务空间ID。
 * @param string $indexId 知识库ID。
 * @return SubmitIndexJobResponse 阿里云百炼服务的响应。
 */
public static function submitIndex($client, $workspaceId, $indexId) {
    $headers = [];
    $submitIndexJobRequest = new SubmitIndexJobRequest([
        'indexId' => $indexId
    ]);
    $runtime = new RuntimeOptions([]);
    return $client->submitIndexJobWithOptions($workspaceId, $submitIndexJobRequest, $headers, $runtime);
}
```

## Node.js

```
/**
 * 提交索引任务
 * @param {Bailian20231229Client} client - 客户端（Client）
 * @param {string} workspaceId - 业务空间ID
 * @param {string} indexId - 知识库ID
 * @returns {Promise<bailian20231229.SubmitIndexJobResponse>} - 阿里云百炼服务的响应
 */
async function submitIndex(client, workspaceId, indexId) {
  const headers = {};
  const req = new bailian20231229.SubmitIndexJobRequest({ indexId });
  const runtime = new Util.RuntimeOptions({});
  return await client.submitIndexJobWithOptions(workspaceId, req, headers, runtime);
}
```

## C#

```
/// <summary>
/// 向阿里云百炼服务提交索引任务。
/// </summary>
/// <param name="client">客户端对象</param>
/// <param name="workspaceId">业务空间ID</param>
/// <param name="indexId">知识库ID</param>
/// <returns>阿里云百炼服务的响应对象</returns>
/// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
public AlibabaCloud.SDK.Bailian20231229.Models.SubmitIndexJobResponse SubmitIndex(
    AlibabaCloud.SDK.Bailian20231229.Client client,
    string workspaceId,
    string indexId)
{
    var headers = new Dictionary<string, string>() { };
    var submitIndexJobRequest = new AlibabaCloud.SDK.Bailian20231229.Models.SubmitIndexJobRequest
    {
           IndexId = indexId
    };
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.SubmitIndexJobWithOptions(workspaceId, submitIndexJobRequest, headers, runtime);
}
```

## Go

```
// SubmitIndex 提交索引任务。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - indexId (string): 知识库ID。
//
// 返回:
//   - *bailian20231229.SubmitIndexJobResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func SubmitIndex(client *bailian20231229.Client, workspaceId, indexId string) (_result *bailian20231229.SubmitIndexJobResponse, _err error) {
	headers := make(map[string]*string)
	submitIndexJobRequest := &bailian20231229.SubmitIndexJobRequest{
		IndexId: tea.String(indexId),
	}
	runtime := &util.RuntimeOptions{}
	return client.SubmitIndexJobWithOptions(tea.String(workspaceId), submitIndexJobRequest, headers, runtime)
}
```

**请求示例**

```
{
  "IndexId": "mymxbdxxxx",
  "WorkspaceId": "llm-4u5xpd1xdjqpxxxx"
}
```

**响应示例**

```
{
  "Status": "200",
  "Message": "success",
  "RequestId": "7774575F-571D-5854-82C2-634AB8XXXXXX",
  "Data": {
    "IndexId": "mymxbdxxxx",
    "Id": "3cd6fb57aaf44cd0b4dd2ca584xxxxxx"
  },
  "Code": "Success",
  "Success": "true"
}
```

#### **3.3. 等待索引任务完成**

索引任务的执行需要一定时间，在请求高峰时段，该过程可能需要数小时。查询其执行状态可以调用[GetIndexJobStatus接口](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-getindexjobstatus)。

-   **job\_id：**请传入[提交索引任务](#bf14fb34a58vy)时接口返回的`Data.Id`。
    

当本接口返回的`Data.Status`字段值为`COMPLETED`时，表示知识库已创建完成。

**重要**

-   子账号调用本示例前需获取[API权限](https://help.aliyun.com/zh/model-studio/member-management#a2e8c1d6246s2)（AliyunBailianDataFullAccess策略）。
    
-   本示例支持[在线调试](https://api.aliyun.com/api/bailian/2023-12-29/SubmitIndexJob)及多语言[代码示例生成](https://api.aliyun.com/api/bailian/2023-12-29/SubmitIndexJob?lang=JAVA&tab=DEMO)。
    

## Python

```
def get_index_job_status(client, workspace_id, index_id, job_id):
    """
    查询索引任务状态。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        job_id (str): 任务ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    get_index_job_status_request = bailian_20231229_models.GetIndexJobStatusRequest(
        index_id=index_id,
        job_id=job_id
    )
    runtime = util_models.RuntimeOptions()
    return client.get_index_job_status_with_options(workspace_id, get_index_job_status_request, headers, runtime)
```

## Java

```
/**
 * 查询索引任务状态。
 *
 * @param client      客户端对象
 * @param workspaceId 业务空间ID
 * @param jobId       任务ID
 * @param indexId     知识库ID
 * @return 阿里云百炼服务的响应对象
 */
public GetIndexJobStatusResponse getIndexJobStatus(com.aliyun.bailian20231229.Client client, String workspaceId, String jobId, String indexId) throws Exception {
    Map<String, String> headers = new HashMap<>();
    com.aliyun.bailian20231229.models.GetIndexJobStatusRequest getIndexJobStatusRequest = new com.aliyun.bailian20231229.models.GetIndexJobStatusRequest();
    getIndexJobStatusRequest.setIndexId(indexId);
    getIndexJobStatusRequest.setJobId(jobId);
    com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
    GetIndexJobStatusResponse getIndexJobStatusResponse = null;
    getIndexJobStatusResponse = client.getIndexJobStatusWithOptions(workspaceId, getIndexJobStatusRequest, headers, runtime);
    return getIndexJobStatusResponse;
}
```

## PHP

```
/**
 * 查询索引任务状态。
 *
 * @param Bailian $client 客户端（Client）。
 * @param string $workspaceId 业务空间ID。
 * @param string $indexId 知识库ID。
 * @param string $jobId 任务ID。
 * @return GetIndexJobStatusResponse 阿里云百炼服务的响应。
 */
public function getIndexJobStatus($client, $workspaceId, $jobId, $indexId) {
    $headers = [];
    $getIndexJobStatusRequest = new GetIndexJobStatusRequest([
        'indexId' => $indexId,
        'jobId' => $jobId
    ]);
    $runtime = new RuntimeOptions([]);
    return $client->getIndexJobStatusWithOptions($workspaceId, $getIndexJobStatusRequest, $headers, $runtime);
}
```

## Node.js

```
/**
 * 查询索引任务状态
 * @param {Bailian20231229Client} client - 客户端（Client）
 * @param {string} workspaceId - 业务空间ID
 * @param {string} jobId - 任务ID
 * @param {string} indexId - 知识库ID
 * @returns {Promise<bailian20231229.GetIndexJobStatusResponse>} - 阿里云百炼服务的响应
 */
async function getIndexJobStatus(client, workspaceId, jobId, indexId) {
  const headers = {};
  const req = new bailian20231229.GetIndexJobStatusRequest({ jobId, indexId });
  const runtime = new Util.RuntimeOptions({});
  return await client.getIndexJobStatusWithOptions(workspaceId, req, headers, runtime);
}
```

## C#

```
/// <summary>
/// 查询索引任务状态。
/// </summary>
/// <param name="client">客户端对象</param>
/// <param name="workspaceId">业务空间ID</param>
/// <param name="jobId">任务ID</param>
/// <param name="indexId">知识库ID</param>
/// <returns>阿里云百炼服务的响应对象</returns>
/// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
public AlibabaCloud.SDK.Bailian20231229.Models.GetIndexJobStatusResponse GetIndexJobStatus(
    AlibabaCloud.SDK.Bailian20231229.Client client,
    string workspaceId,
    string jobId,
    string indexId)
{
    var headers = new Dictionary<string, string>() { };
    var getIndexJobStatusRequest = new AlibabaCloud.SDK.Bailian20231229.Models.GetIndexJobStatusRequest
    {
        IndexId = indexId,
        JobId = jobId
    };
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.GetIndexJobStatusWithOptions(workspaceId, getIndexJobStatusRequest, headers, runtime);
}
```

## Go

```
// GetIndexJobStatus 查询索引任务状态。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - jobId (string): 任务ID。
//   - indexId (string): 知识库ID。
//
// 返回:
//   - *bailian20231229.GetIndexJobStatusResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func GetIndexJobStatus(client *bailian20231229.Client, workspaceId, jobId, indexId string) (_result *bailian20231229.GetIndexJobStatusResponse, _err error) {
	headers := make(map[string]*string)
	getIndexJobStatusRequest := &bailian20231229.GetIndexJobStatusRequest{
		JobId:   tea.String(jobId),
		IndexId: tea.String(indexId),
	}
	runtime := &util.RuntimeOptions{}
	return client.GetIndexJobStatusWithOptions(tea.String(workspaceId), getIndexJobStatusRequest, headers, runtime)
}
```

**请求示例**

```
{
  "IndexId": "mymxbdxxxx",
  "JobId": "3cd6fb57aaf44cd0b4dd2ca584xxxxxx",
  "WorkspaceId": "llm-4u5xpd1xdjqpxxxx"
}
```

**响应示例**

```
{
  "Status": "200",
  "Message": "success",
  "RequestId": "E83423B9-7D6D-5283-836B-CF7EAEXXXXXX",
  "Data": {
    "Status": "COMPLETED",
    "Documents": [
      {
        "Status": "FINISH",
        "DocId": "file_0b21e0a852cd40cd9741c54fefbb61cd_10xxxxxx",
        "Message": "导入成功",
        "DocName": "阿里云百炼系列手机产品介绍",
        "Code": "FINISH"
      }
    ],
    "JobId": "3cd6fb57aaf44cd0b4dd2ca584xxxxxx"
  },
  "Code": "Success",
  "Success": "true"
}
```

通过以上步骤，您已成功创建了一个知识库，并包含了需要上传的文件。

## **检索知识库**

目前，检索知识库支持两种方式：

-   **使用阿里云百炼应用：**[调用应用](https://help.aliyun.com/zh/model-studio/application-calling-guide#4100253b7chc3)时，通过`rag_options`传入知识库ID`index_id`，为您的大模型应用补充私有知识和提供最新信息。
    
-   **使用阿里云API：**调用[Retrieve接口](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve)在指定的知识库中检索信息并返回原始文本切片。
    

二者的区别在于：前者先将检索到的相关文本切片传给您配置的大模型，模型再结合这些切片与用户的原始查询生成最终回答并返回；后者则是直接返回文本切片。

接下来为您介绍**使用阿里云API**的方式。

在指定的知识库中检索信息，并返回文本切片，可以通过调用[Retrieve接口](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve)。

-   **client：**[如何获取client](#52ff2774f0pq9)
    
-   **workspace\_id：**知识库所在的业务空间。[如何获取业务空间ID](https://help.aliyun.com/zh/model-studio/use-workspace#c5222ec081sbo)
    
    > 子账号只能检索自己[已加入的业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)中的知识库。
    

若本接口返回的结果包含较多干扰信息，您可以在请求时传入[SearchFilters](https://help.aliyun.com/zh/model-studio/how-to-use-search-filters)设置检索条件（比如设置[标签](https://help.aliyun.com/zh/model-studio/rag-knowledge-base#0a4efa5d7dta6)筛选），以排除干扰信息。

**重要**

-   子账号调用本示例前需获取[API权限](https://help.aliyun.com/zh/model-studio/member-management#a2e8c1d6246s2)（AliyunBailianDataFullAccess策略）。
    
-   本示例支持[在线调试](https://api.aliyun.com/api/bailian/2023-12-29/Retrieve)及多语言[代码示例生成](https://api.aliyun.com/api/bailian/2023-12-29/Retrieve?lang=JAVA&tab=DEMO)。
    

## Python

```
def retrieve_index(client, workspace_id, index_id, query):
    """
    在指定的知识库中检索信息。
        
    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        query (str): 原始输入prompt。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    retrieve_request = bailian_20231229_models.RetrieveRequest(
        index_id=index_id,
        query=query
    )
    runtime = util_models.RuntimeOptions()
    return client.retrieve_with_options(workspace_id, retrieve_request, headers, runtime)
```

## Java

```
/**
 * 在指定的知识库中检索信息。
 *
 * @param client         客户端对象（bailian20231229Client）
 * @param workspaceId    业务空间ID
 * @param indexId        知识库ID
 * @param query          检索查询语句
 * @return               阿里云百炼服务的响应
 */
public RetrieveResponse retrieveIndex(com.aliyun.bailian20231229.Client client, String workspaceId, String indexId, String query) throws Exception {
    RetrieveRequest retrieveRequest = new RetrieveRequest();
    retrieveRequest.setIndexId(indexId);
    retrieveRequest.setQuery(query);
    RuntimeOptions runtime = new RuntimeOptions();
    return client.retrieveWithOptions(workspaceId, retrieveRequest, null, runtime);
}
```

## PHP

```
/**
 * 在指定的知识库中检索信息。
 *
 * @param Bailian $client 客户端对象（Client）。
 * @param string $workspaceId 业务空间ID
 * @param string $indexId 知识库ID
 * @param string $query 检索查询语句
 * @return RetrieveResponse 阿里云百炼服务的响应
 * @throws Exception
 */
public function retrieveIndex($client, $workspaceId, $indexId, $query) {
    $headers = [];
    $retrieveRequest = new RetrieveRequest([
        "query" => $query,
        "indexId" => $indexId
    ]);
    $runtime = new RuntimeOptions([]);
    return $client->retrieveWithOptions($workspaceId, $retrieveRequest, $headers, $runtime);
}
```

## Node.js

```
/**
 * 在指定的知识库中检索信息
 * @param {bailian20231229.Client} client 客户端（Client）
 * @param {string} workspaceId 业务空间ID
 * @param {string} indexId 知识库ID
 * @param {string} query 检索query
 * @returns {Promise<bailian20231229.RetrieveResponse>} 阿里云百炼服务的响应
 */
async function retrieveIndex(client, workspaceId, indexId, query) {
    const headers = {};
    const req = new bailian20231229.RetrieveRequest({
        indexId,
        query
    });
    const runtime = new Util.RuntimeOptions({});
    return await client.retrieveWithOptions(workspaceId, req, headers, runtime);
}
```

## C#

```
/// <summary>
/// 在指定的知识库中检索信息。
/// </summary>
/// <param name="client">客户端对象（bailian20231229Client）</param>
/// <param name="workspaceId">业务空间ID</param>
/// <param name="indexId">知识库ID</param>
/// <param name="query">检索查询语句</param>
/// <returns>阿里云百炼服务的响应</returns>
/// <exception cref="Exception">如果调用失败</exception>
public AlibabaCloud.SDK.Bailian20231229.Models.RetrieveResponse RetrieveIndex(
    AlibabaCloud.SDK.Bailian20231229.Client client,
    string workspaceId,
    string indexId,
    string query)
{
    var headers = new Dictionary<string, string>() { };
    var retrieveRequest = new AlibabaCloud.SDK.Bailian20231229.Models.RetrieveRequest
    {
        IndexId = indexId,
        Query = query
    };
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.RetrieveWithOptions(workspaceId, retrieveRequest, headers, runtime);
}
```

## Go

```
// retrieveIndex 在指定的知识库中检索信息。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - indexId（string）: 知识库ID。
//   - query（string）: 检索查询语句
//
// 返回:
//   - *bailian20231229.RetrieveResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func retrieveIndex(client *bailian20231229.Client, workspaceId, indexId, query string) (*bailian20231229.RetrieveResponse, error) {
	headers := make(map[string]*string)
	request := &bailian20231229.RetrieveRequest{
		IndexId: tea.String(indexId),
		Query:   tea.String(query),
	}
	runtime := &util.RuntimeOptions{}
	return client.RetrieveWithOptions(tea.String(workspaceId), request, headers, runtime)
}
```

**请求示例**

```
{
  "IndexId": "mymxbdxxxx",
  "WorkspaceId": "llm-4u5xpd1xdjqpxxxx",
  "Query": "请介绍一下阿里云百炼手机X1。"
}
```

**响应示例**

```
{
  "Status": "200",
  "Message": "success",
  "RequestId": "17316EA2-1F4D-55AC-8872-53F6F1XXXXXX",
  "Data": {
    "Nodes": [
      {
        "Score": 0.6294550895690918,
        "Metadata": {
          "file_path": "https://bailian-datahub-data-prod.oss-cn-beijing.aliyuncs.com/10285263/multimodal/docJson/%E7%99%BE%E7%82%BC%E7%B3%BB%E5%88%97%E6%89%8B%E6%9C%BA%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D_1742197778230.json?Expires=1742457465&OSSAccessKeyId=TestID&Signature=ptFkSObdnBrbJNEw8CnlOSP%2FTeI%3D",
          "is_displayed_chunk_content": "true",
          "_rc_v_score": 0.7449869735535081,
          "image_url": [],
          "nid": "9ad347d9e4d7465d2c1e693a08b0077c|d6f7fbf8403e0df796258e5ada1ee1c1|4772257e93ed64ea087ff4be0d5e4620|7ce1370e4a1958842c9268144a452cc7",
          "_q_score": 1,
          "source": "0",
          "_score": 0.6294550895690918,
          "title": "阿里云百炼手机产品介绍",
          "doc_id": "file_0b21e0a852cd40cd9741c54fefbb61cd_10xxxxxx",
          "content": "阿里云百炼手机产品介绍阿里云百炼 X1 ——畅享极致视界：搭载 6.7英寸 1440 x 3200像素超清屏幕，搭配 120Hz刷新率，流畅视觉体验跃然眼前。256GB海量存储空间与 12GB RAM强强联合，无论是大型游戏还是多任务处理，都能轻松应对。5000mAh电池长续航，加上超感光四摄系统，记录生活每一刻精彩。参考售价：4599- 4999千问 Vivid 7 ——智能摄影新体验：拥有 6.5英寸 1080 x 2400像素全面屏，AI智能摄影功能让每一张照片都能展现专业级色彩与细节。8GB RAM与 128GB存储空间确保流畅操作，4500mAh电池满足日常所需。侧面指纹解锁，便捷又安全。参考售价：2999- 3299星尘 S9 Pro ——创新视觉盛宴：突破性 6.9英寸 1440 x 3088像素屏下摄像头设计，带来无界视觉享受。512GB存储与 16GB RAM的顶级配置，配合 6000mAh电池与 100W快充技术，让性能与续航并驾齐驱，引领科技潮流。参考售价：5999- 6499。",
          "_rc_score": 0,
          "workspace_id": "llm-4u5xpd1xdjqpxxxx",
          "hier_title": "阿里云百炼手机产品介绍",
          "_rc_t_score": 0.05215025693178177,
          "doc_name": "阿里云百炼系列手机产品介绍",
          "pipeline_id": "mymxbdxxxx",
          "_id": "llm-4u5xpd1xdjqp8itj_mymxbd6172_file_0b21e0a852cd40cd9741c54fefbb61cd_10285263_0_0"
        },
        "Text": "阿里云百炼手机产品介绍阿里云百炼 X1 ——畅享极致视界：搭载 6.7英寸 1440 x 3200像素超清屏幕，搭配 120Hz刷新率，流畅视觉体验跃然眼前。256GB海量存储空间与 12GB RAM强强联合，无论是大型游戏还是多任务处理，都能轻松应对。5000mAh电池长续航，加上超感光四摄系统，记录生活每一刻精彩。参考售价：4599- 4999千问 Vivid 7 ——智能摄影新体验：拥有 6.5英寸 1080 x 2400像素全面屏，AI智能摄影功能让每一张照片都能展现专业级色彩与细节。8GB RAM与 128GB存储空间确保流畅操作，4500mAh电池满足日常所需。侧面指纹解锁，便捷又安全。参考售价：2999- 3299星尘 S9 Pro ——创新视觉盛宴：突破性 6.9英寸 1440 x 3088像素屏下摄像头设计，带来无界视觉享受。512GB存储与 16GB RAM的顶级配置，配合 6000mAh电池与 100W快充技术，让性能与续航并驾齐驱，引领科技潮流。参考售价：5999- 6499。"
      },
      {
        "Score": 0.5322970747947693,
        "Metadata": {
          "file_path": "https://bailian-datahub-data-prod.oss-cn-beijing.aliyuncs.com/10285263/multimodal/docJson/%E7%99%BE%E7%82%BC%E7%B3%BB%E5%88%97%E6%89%8B%E6%9C%BA%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D_1742197778230.json?Expires=1742457465&OSSAccessKeyId=TestID&Signature=ptFkSObdnBrbJNEw8CnlOSP%2FTeI%3D",
          "is_displayed_chunk_content": "true",
          "_rc_v_score": 0.641660213470459,
          "image_url": [],
          "nid": "00be1864c18b4c39c59f83713af80092|4f2bfb02cc9fc4e85597b2e717699207",
          "_q_score": 0.9948930557644994,
          "source": "0",
          "_score": 0.5322970747947693,
          "title": "阿里云百炼手机产品介绍",
          "doc_id": "file_0b21e0a852cd40cd9741c54fefbb61cd_10xxxxxx",
          "content": "阿里云百炼 Flex Fold+ ——折叠屏新纪元：集创新与奢华于一身，主屏 7.6英寸 1800 x 2400像素与外屏 4.7英寸 1080 x 2400像素，多角度自由悬停设计，满足不同场景需求。阿里云百炼 Flex Fold+ ——折叠屏新纪元：集创新与奢华于一身，主屏 7.6英寸 1800 x 2400像素与外屏 4.7英寸 1080 x 2400像素，多角度自由悬停设计，满足不同场景需求。512GB存储、12GB RAM，加之 4700mAh电池与 UTG超薄柔性玻璃，开启折叠屏时代新篇章。此外，这款手机还支持双卡双待、卫星通话，帮助您在世界各地都能畅联通话。参考零售价：9999- 10999。每一款手机都是匠心独运，只为成就您手中的科技艺术品。选择属于您的智能伙伴，开启未来科技生活的新篇章。",
          "_rc_score": 0,
          "workspace_id": "llm-4u5xpd1xdjqpxxxx",
          "hier_title": "阿里云百炼手机产品介绍",
          "_rc_t_score": 0.05188392847776413,
          "doc_name": "阿里云百炼系列手机产品介绍",
          "pipeline_id": "mymxbdxxxx",
          "_id": "llm-4u5xpd1xdjqp8itj_mymxbd6172_file_0b21e0a852cd40cd9741c54fefbb61cd_10285263_0_2"
        },
        "Text": "阿里云百炼 Flex Fold+ ——折叠屏新纪元：集创新与奢华于一身，主屏 7.6英寸 1800 x 2400像素与外屏 4.7英寸 1080 x 2400像素，多角度自由悬停设计，满足不同场景需求。阿里云百炼 Flex Fold+ ——折叠屏新纪元：集创新与奢华于一身，主屏 7.6英寸 1800 x 2400像素与外屏 4.7英寸 1080 x 2400像素，多角度自由悬停设计，满足不同场景需求。512GB存储、12GB RAM，加之 4700mAh电池与 UTG超薄柔性玻璃，开启折叠屏时代新篇章。此外，这款手机还支持双卡双待、卫星通话，帮助您在世界各地都能畅联通话。参考零售价：9999- 10999。每一款手机都是匠心独运，只为成就您手中的科技艺术品。选择属于您的智能伙伴，开启未来科技生活的新篇章。"
      },
      {
        "Score": 0.5050643086433411,
        "Metadata": {
          "file_path": "https://bailian-datahub-data-prod.oss-cn-beijing.aliyuncs.com/10285263/multimodal/docJson/%E7%99%BE%E7%82%BC%E7%B3%BB%E5%88%97%E6%89%8B%E6%9C%BA%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D_1742197778230.json?Expires=1742457465&OSSAccessKeyId=TestID&Signature=ptFkSObdnBrbJNEw8CnlOSP%2FTeI%3D",
          "is_displayed_chunk_content": "true",
          "_rc_v_score": 0.6757396459579468,
          "image_url": [],
          "nid": "f05d1b51eb6b033b32a162d90a9da71b|5cb6b848be8d11eb168c031025415cc5|4f2bfb02cc9fc4e85597b2e717699207",
          "_q_score": 0.9890713450653327,
          "source": "0",
          "_score": 0.5050643086433411,
          "title": "阿里云百炼手机产品介绍",
          "doc_id": "file_0b21e0a852cd40cd9741c54fefbb61cd_10xxxxxx",
          "content": "512GB存储与 16GB RAM的顶级配置，配合 6000mAh电池与 100W快充技术，让性能与续航并驾齐驱，引领科技潮流。参考售价：5999- 6499。阿里云百炼 Ace Ultra ——游戏玩家之选：配备 6.67英寸 1080 x 2400像素屏幕，内置 10GB RAM与 256GB存储，确保游戏运行丝滑无阻。5500mAh电池搭配液冷散热系统，长时间游戏也能保持冷静。高动态双扬声器，沉浸式音效升级游戏体验。参考售价：3999- 4299。阿里云百炼 Zephyr Z9 ——轻薄便携的艺术：轻巧的 6.4英寸 1080 x 2340像素设计，搭配 128GB存储与 6GB RAM，日常使用游刃有余。4000mAh电池确保一天无忧，30倍数字变焦镜头捕捉远处细节，轻薄而不失强大。参考售价：2499- 2799。阿里云百炼 Flex Fold+ ——折叠屏新纪元：集创新与奢华于一身，主屏 7.6英寸 1800 x 2400像素与外屏 4.7英寸 1080 x 2400像素，多角度自由悬停设计，满足不同场景需求。",
          "_rc_score": 0,
          "workspace_id": "llm-4u5xpd1xdjqpxxxx",
          "hier_title": "阿里云百炼手机产品介绍",
          "_rc_t_score": 0.05158032476902008,
          "doc_name": "阿里云百炼系列手机产品介绍",
          "pipeline_id": "mymxbdxxxx",
          "_id": "llm-4u5xpd1xdjqp8itj_mymxbd6172_file_0b21e0a852cd40cd9741c54fefbb61cd_10285263_0_1"
        },
        "Text": "512GB存储与 16GB RAM的顶级配置，配合 6000mAh电池与 100W快充技术，让性能与续航并驾齐驱，引领科技潮流。参考售价：5999- 6499。阿里云百炼 Ace Ultra ——游戏玩家之选：配备 6.67英寸 1080 x 2400像素屏幕，内置 10GB RAM与 256GB存储，确保游戏运行丝滑无阻。5500mAh电池搭配液冷散热系统，长时间游戏也能保持冷静。高动态双扬声器，沉浸式音效升级游戏体验。参考售价：3999- 4299。阿里云百炼 Zephyr Z9 ——轻薄便携的艺术：轻巧的 6.4英寸 1080 x 2340像素设计，搭配 128GB存储与 6GB RAM，日常使用游刃有余。4000mAh电池确保一天无忧，30倍数字变焦镜头捕捉远处细节，轻薄而不失强大。参考售价：2499- 2799。阿里云百炼 Flex Fold+ ——折叠屏新纪元：集创新与奢华于一身，主屏 7.6英寸 1800 x 2400像素与外屏 4.7英寸 1080 x 2400像素，多角度自由悬停设计，满足不同场景需求。"
      }
    ]
  },
  "Code": "Success",
  "Success": "true"
}
```

## **更新知识库**

接下来通过示例，引导您更新文档搜索类知识库。所有引用该知识库的应用会实时生效您本次的更新（新增内容可用于检索和召回，而已删除内容将不再可用）。

> 数据查询、图片问答类知识库不支持通过API更新。如何更新请参见[知识库：更新知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base#b2f92e9d2car8)。

-   **如何增量更新知识库：**请您按照以下三步（先上传更新后的文件，再追加文件至知识库，最后删除旧文件）操作。此外暂无其他实现方式。
    
-   **如何全量更新知识库：**对知识库中的所有文件，请您逐一执行以下三步完成更新。
    
-   **如何实现知识库的自动更新/同步：**请详见[如何实现知识库的自动更新/同步](#827f8c570a9ni)。
    
-   **单次更新对文件数量是否有限制：**建议不超过10万个，否则可能导致知识库无法正常更新。
    

### **1\. 上传更新后的文件**

按照[创建知识库：第二步](#4b4a1236aalno)操作，将更新后的文件上传至该知识库所在的业务空间。

> 您需要重新申请文件上传租约，为更新后的文件生成一组新的上传参数。

### **2\. 追加文件至知识库**

#### **2.1. 提交追加文件任务**

上传文件解析完成后，请调用[SubmitIndexAddDocumentsJob接口](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-submitindexadddocumentsjob)将新文件追加至知识库，并重新构建知识库索引。

-   **client：**[如何获取client](#52ff2774f0pq9)
    
-   **workspace\_id：**[如何获取业务空间ID](https://help.aliyun.com/zh/model-studio/use-workspace#c5222ec081sbo)
    
-   **file\_id：**请传入[添加文件到类目中](#494345d4b1hx2)时接口返回的`FileId`。
    
-   **source\_type：**在本示例中，请传入`DATA_CENTER_FILE`。
    

完成提交后，阿里云百炼将以异步任务方式开始重新构建知识库。本接口返回的`Data.Id`为对应的任务ID（job\_id）。下一步中，您将用到此ID查询任务的最新状态。

**重要**

-   SubmitIndexAddDocumentsJob接口调用成功后，将执行一段时间，您可通过`job_id`查询任务的最新状态。**在任务完成前，请勿重复提交。**
    

**重要**

-   子账号调用本示例前需获取[API权限](https://help.aliyun.com/zh/model-studio/member-management#a2e8c1d6246s2)（AliyunBailianDataFullAccess策略）。
    
-   本示例支持[在线调试](https://api.aliyun.com/api/bailian/2023-12-29/SubmitIndexAddDocumentsJob)及多语言[代码示例生成](https://api.aliyun.com/api/bailian/2023-12-29/SubmitIndexAddDocumentsJob?lang=JAVA&tab=DEMO)。
    

## Python

```
def submit_index_add_documents_job(client, workspace_id, index_id, file_id, source_type):
    """
    向一个文档搜索类知识库追加导入已解析的文件。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        file_id (str): 文件ID。
        source_type(str): 数据类型。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    submit_index_add_documents_job_request = bailian_20231229_models.SubmitIndexAddDocumentsJobRequest(
        index_id=index_id,
        document_ids=[file_id],
        source_type=source_type
    )
    runtime = util_models.RuntimeOptions()
    return client.submit_index_add_documents_job_with_options(workspace_id, submit_index_add_documents_job_request, headers, runtime)
```

## Java

```
/**
 * 向一个文档搜索类知识库追加导入已解析的文件
 *
 * @param client      客户端（Client）
 * @param workspaceId 业务空间ID
 * @param indexId     知识库ID
 * @param fileId      文件ID
 * @param sourceType  数据类型
 * @return 阿里云百炼服务的响应
 */
public SubmitIndexAddDocumentsJobResponse submitIndexAddDocumentsJob(com.aliyun.bailian20231229.Client client, String workspaceId, String indexId, String fileId, String sourceType) throws Exception {
    Map<String, String> headers = new HashMap<>();
    SubmitIndexAddDocumentsJobRequest submitIndexAddDocumentsJobRequest = new SubmitIndexAddDocumentsJobRequest();
    submitIndexAddDocumentsJobRequest.setIndexId(indexId);
    submitIndexAddDocumentsJobRequest.setDocumentIds(Collections.singletonList(fileId));
    submitIndexAddDocumentsJobRequest.setSourceType(sourceType);
    RuntimeOptions runtime = new RuntimeOptions();
    return client.submitIndexAddDocumentsJobWithOptions(workspaceId, submitIndexAddDocumentsJobRequest, headers, runtime);
}
```

## PHP

```
/**
 * 向一个文档搜索类知识库追加导入已解析的文件
 *
 * @param Bailian $client 客户端对象
 * @param string $workspaceId 业务空间ID
 * @param string $indexId 知识库ID
 * @param string $fileId 文件ID
 * @param string $sourceType 数据类型
 * @return SubmitIndexAddDocumentsJobResponse 阿里云百炼服务的响应
 * @throws Exception
 */
public function submitIndexAddDocumentsJob($client, $workspaceId, $indexId, $fileId, $sourceType) {
    $headers = [];
    $submitIndexAddDocumentsJobRequest = new SubmitIndexAddDocumentsJobRequest([
        "indexId" =>$indexId,
        "sourceType" => $sourceType,
        "documentIds" => [
            $fileId
        ]
    ]);
    $runtime = new RuntimeOptions([]);
    return $client->submitIndexAddDocumentsJobWithOptions($workspaceId, $submitIndexAddDocumentsJobRequest, $headers, $runtime);
}
```

## Node.js

```
/**
 * 提交追加文件任务
 * @param {Bailian20231229Client} client - 客户端（Client）
 * @param {string} workspaceId - 业务空间ID
 * @param {string} indexId - 知识库ID
 * @param {string} fileId - 文件ID
 * @param {string} sourceType - 数据类型
 * @returns {Promise<bailian20231229.SubmitIndexAddDocumentsJobResponse>} - 阿里云百炼服务的响应
 */
async function submitIndexAddDocumentsJob(client, workspaceId, indexId, fileId, sourceType) {
    const headers = {};
    const req = new bailian20231229.SubmitIndexAddDocumentsJobRequest({
        indexId,
        documentIds: [fileId],
        sourceType,
    });
    const runtime = new Util.RuntimeOptions({});
    return await client.submitIndexAddDocumentsJobWithOptions(workspaceId, req, headers, runtime);
}
```

## C#

```
/// <summary>
/// 向一个文档搜索类知识库追加导入已解析的文件
/// </summary>
/// <param name="client">客户端（Client）</param>
/// <param name="workspaceId">业务空间ID</param>
/// <param name="indexId">知识库ID</param>
/// <param name="fileId">文件ID</param>
/// <param name="sourceType">数据类型</param>
/// <returns>阿里云百炼服务的响应</returns>
public AlibabaCloud.SDK.Bailian20231229.Models.SubmitIndexAddDocumentsJobResponse SubmitIndexAddDocumentsJob(
    AlibabaCloud.SDK.Bailian20231229.Client client,
    string workspaceId,
    string indexId,
    string fileId,
    string sourceType)
{
    var headers = new Dictionary<string, string>() { };
    var submitIndexAddDocumentsJobRequest = new AlibabaCloud.SDK.Bailian20231229.Models.SubmitIndexAddDocumentsJobRequest
    {
        IndexId = indexId,
        DocumentIds = new List<string> { fileId },
        SourceType = sourceType
    };
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.SubmitIndexAddDocumentsJobWithOptions(workspaceId, submitIndexAddDocumentsJobRequest, headers, runtime);
}
```

## Go

```
// SubmitIndexAddDocumentsJob 向一个文档搜索类知识库追加导入已解析的文件。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - indexId（string）: 知识库ID。
//   - fileId(string): 文件ID。
//   - sourceType(string): 数据类型。
//
// 返回:
//   - *bailian20231229.SubmitIndexAddDocumentsJobResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func SubmitIndexAddDocumentsJob(client *bailian20231229.Client, workspaceId, indexId, fileId, sourceType string) (_result *bailian20231229.SubmitIndexAddDocumentsJobResponse, _err error) {
	headers := make(map[string]*string)
	submitIndexAddDocumentsJobRequest := &bailian20231229.SubmitIndexAddDocumentsJobRequest{
		IndexId:     tea.String(indexId),
		SourceType:  tea.String(sourceType),
		DocumentIds: []*string{tea.String(fileId)},
	}
	runtime := &util.RuntimeOptions{}
	return client.SubmitIndexAddDocumentsJobWithOptions(tea.String(workspaceId), submitIndexAddDocumentsJobRequest, headers, runtime)
}
```

**请求示例**

```
{
  "IndexId": "mymxbdxxxx",
  "SourceType": "DATA_CENTER_FILE",
  "WorkspaceId": "llm-4u5xpd1xdjqpxxxx",
  "DocumentIds": [
    "file_247a2fd456a349ee87d071404840109b_10xxxxxx"
  ]
}
```

**响应示例**

```
{
  "Status": "200",
  "RequestId": "F693EB60-FEFC-559A-BF56-A41F52XXXXXX",
  "Message": "success",
  "Data": {
    "Id": "d8d189a36a3248438dca23c078xxxxxx"
  },
  "Code": "Success",
  "Success": "true"
}
```

#### **2.2. 等待追加任务完成**

索引任务的执行需要一定时间，在请求高峰时段，该过程可能需要数小时。查询其执行状态可以调用[GetIndexJobStatus接口](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-getindexjobstatus)。

-   **job\_id：**请传入[提交追加文件任务](#b2f19a956bcsl)时接口返回的`Data.Id`。
    

当本接口返回的`Data.Status`字段值为`COMPLETED`，表示本次更新的文件已全部成功追加至知识库。

> 本接口返回的文件列表`Documents`为本次追加（由您提供的`job_id`唯一确定）的所有文件。

**重要**

-   子账号调用本示例前需获取[API权限](https://help.aliyun.com/zh/model-studio/member-management#a2e8c1d6246s2)（AliyunBailianDataFullAccess策略）。
    
-   本示例支持[在线调试](https://api.aliyun.com/api/bailian/2023-12-29/GetIndexJobStatus)及多语言[代码示例生成](https://api.aliyun.com/api/bailian/2023-12-29/GetIndexJobStatus?lang=JAVA&tab=DEMO)。
    

## Python

```
def get_index_job_status(client, workspace_id, index_id, job_id):
    """
    查询索引任务状态。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        job_id (str): 任务ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    get_index_job_status_request = bailian_20231229_models.GetIndexJobStatusRequest(
        index_id=index_id,
        job_id=job_id
    )
    runtime = util_models.RuntimeOptions()
    return client.get_index_job_status_with_options(workspace_id, get_index_job_status_request, headers, runtime)
```

## Java

```
/**
 * 查询索引任务状态。
 *
 * @param client      客户端对象
 * @param workspaceId 业务空间ID
 * @param jobId       任务ID
 * @param indexId     知识库ID
 * @return 阿里云百炼服务的响应对象
 */
public GetIndexJobStatusResponse getIndexJobStatus(com.aliyun.bailian20231229.Client client, String workspaceId, String jobId, String indexId) throws Exception {
    Map<String, String> headers = new HashMap<>();
    com.aliyun.bailian20231229.models.GetIndexJobStatusRequest getIndexJobStatusRequest = new com.aliyun.bailian20231229.models.GetIndexJobStatusRequest();
    getIndexJobStatusRequest.setIndexId(indexId);
    getIndexJobStatusRequest.setJobId(jobId);
    com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
    GetIndexJobStatusResponse getIndexJobStatusResponse = null;
    getIndexJobStatusResponse = client.getIndexJobStatusWithOptions(workspaceId, getIndexJobStatusRequest, headers, runtime);
    return getIndexJobStatusResponse;
}
```

## PHP

```
/**
 * 查询索引任务状态。
 *
 * @param Bailian $client 客户端（Client）。
 * @param string $workspaceId 业务空间ID。
 * @param string $indexId 知识库ID。
 * @param string $jobId 任务ID。
 * @return GetIndexJobStatusResponse 阿里云百炼服务的响应。
 */
public function getIndexJobStatus($client, $workspaceId, $jobId, $indexId) {
    $headers = [];
    $getIndexJobStatusRequest = new GetIndexJobStatusRequest([
        'indexId' => $indexId,
        'jobId' => $jobId
    ]);
    $runtime = new RuntimeOptions([]);
    return $client->getIndexJobStatusWithOptions($workspaceId, $getIndexJobStatusRequest, $headers, $runtime);
}
```

## Node.js

```
/**
 * 查询索引任务状态
 * @param {Bailian20231229Client} client - 客户端（Client）
 * @param {string} workspaceId - 业务空间ID
 * @param {string} jobId - 任务ID
 * @param {string} indexId - 知识库ID
 * @returns {Promise<bailian20231229.GetIndexJobStatusResponse>} - 阿里云百炼服务的响应
 */
static getIndexJobStatus(client, workspaceId, jobId, indexId) {
    const headers = {};
    const req = new bailian20231229.GetIndexJobStatusRequest({ jobId, indexId });
    const runtime = new Util.RuntimeOptions({});
    return await client.getIndexJobStatusWithOptions(workspaceId, req, headers, runtime);
}
```

## C#

```
/// <summary>
/// 查询索引任务状态。
/// </summary>
/// <param name="client">客户端对象</param>
/// <param name="workspaceId">业务空间ID</param>
/// <param name="jobId">任务ID</param>
/// <param name="indexId">知识库ID</param>
/// <returns>阿里云百炼服务的响应对象</returns>
/// <exception cref="Exception">调用过程中发生错误时抛出异常</exception>
public AlibabaCloud.SDK.Bailian20231229.Models.GetIndexJobStatusResponse GetIndexJobStatus(
    AlibabaCloud.SDK.Bailian20231229.Client client,
    string workspaceId,
    string jobId,
    string indexId)
{
    var headers = new Dictionary<string, string>() { };
    var getIndexJobStatusRequest = new AlibabaCloud.SDK.Bailian20231229.Models.GetIndexJobStatusRequest
    {
        IndexId = indexId,
        JobId = jobId
    };
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.GetIndexJobStatusWithOptions(workspaceId, getIndexJobStatusRequest, headers, runtime);
}
```

## Go

```
// GetIndexJobStatus 查询索引任务状态。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - jobId (string): 任务ID。
//   - indexId (string): 知识库ID。
//
// 返回:
//   - *bailian20231229.GetIndexJobStatusResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func GetIndexJobStatus(client *bailian20231229.Client, workspaceId, jobId, indexId string) (_result *bailian20231229.GetIndexJobStatusResponse, _err error) {
	headers := make(map[string]*string)
	getIndexJobStatusRequest := &bailian20231229.GetIndexJobStatusRequest{
		JobId:   tea.String(jobId),
		IndexId: tea.String(indexId),
	}
	runtime := &util.RuntimeOptions{}
	return client.GetIndexJobStatusWithOptions(tea.String(workspaceId), getIndexJobStatusRequest, headers, runtime)
}
```

**请求示例**

```
{
  "IndexId": "mymxbdxxxx",
  "JobId": "76f243b9ee534d59a61f156ff0xxxxxx",
  "WorkspaceId": "llm-4u5xpd1xdjqpxxxx"
}
```

**响应示例**

```
{
  "Status": 200,
  "Message": "success",
  "RequestId": "7F727D58-D90E-51E7-B56E-985A42XXXXXX",
  "Data": {
    "Status": "COMPLETED",
    "Documents": [
      {
        "Status": "FINISH",
        "DocId": "file_247a2fd456a349ee87d071404840109b_10xxxxxx",
        "Message": "导入成功",
        "DocName": "阿里云百炼系列手机产品介绍",
        "Code": "FINISH"
      }
    ],
    "JobId": "76f243b9ee534d59a61f156ff0xxxxxx"
  },
  "Code": "Success",
  "Success": true
}
```

### **3\. 删除旧文件**

最后，从指定知识库中永久删除旧版本的文件（避免旧的知识被错误检索），可以调用[DeleteIndexDocument接口](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-deleteindexdocument)。

-   **file\_id：**请传入旧版本文件的`FileId`。
    

**说明**

仅能删除知识库中状态为导入失败（INSERT\_ERROR）或导入成功（FINISH）的文件。如需查询知识库中的文件状态，可调用[ListIndexDocuments接口](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-listindexdocuments)。

**重要**

-   子账号调用本示例前需获取[API权限](https://help.aliyun.com/zh/model-studio/member-management#a2e8c1d6246s2)（AliyunBailianDataFullAccess策略）。
    
-   本示例支持[在线调试](https://api.aliyun.com/api/bailian/2023-12-29/DeleteIndexDocument)及多语言[代码示例生成](https://api.aliyun.com/api/bailian/2023-12-29/DeleteIndexDocument?lang=JAVA&tab=DEMO)。
    

## Python

```
def delete_index_document(client, workspace_id, index_id, file_id):
    """
    从指定的文档搜索类知识库中永久删除一个或多个文件。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        file_id (str): 文件ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    delete_index_document_request = bailian_20231229_models.DeleteIndexDocumentRequest(
        index_id=index_id,
        document_ids=[file_id]
    )
    runtime = util_models.RuntimeOptions()
    return client.delete_index_document_with_options(workspace_id, delete_index_document_request, headers, runtime)
```

## Java

```
/**
 * 从指定的文档搜索类知识库中永久删除一个或多个文件
 *
 * @param client      客户端（Client）
 * @param workspaceId 业务空间ID
 * @param indexId     知识库ID
 * @param fileId      文件ID
 * @return 阿里云百炼服务的响应
 */
public DeleteIndexDocumentResponse deleteIndexDocument(com.aliyun.bailian20231229.Client client, String workspaceId, String indexId, String fileId) throws Exception {
    Map<String, String> headers = new HashMap<>();
    DeleteIndexDocumentRequest deleteIndexDocumentRequest = new DeleteIndexDocumentRequest();
    deleteIndexDocumentRequest.setIndexId(indexId);
    deleteIndexDocumentRequest.setDocumentIds(Collections.singletonList(fileId));
    com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
    return client.deleteIndexDocumentWithOptions(workspaceId, deleteIndexDocumentRequest, headers, runtime);
}
```

## PHP

```
/**
 * 从指定的文档搜索类知识库中永久删除文件
 *
 * @param Bailian $client 客户端对象
 * @param string $workspaceId 业务空间ID
 * @param string $indexId 知识库ID
 * @param string $fileId 文件ID
 * @return mixed 阿里云百炼服务的响应
 * @throws Exception
 */
public function deleteIndexDocument($client, $workspaceId, $indexId, $fileId) {
    $headers = [];
    $deleteIndexDocumentRequest = new DeleteIndexDocumentRequest([
        "indexId" => $indexId,
        "documentIds" => [
            $fileId
        ]
    ]);
    $runtime = new RuntimeOptions([]);
    return $client->deleteIndexDocumentWithOptions($workspaceId, $deleteIndexDocumentRequest, $headers, $runtime);
}
```

## Node.js

```
/**
 * 删除旧文件
 * @param {Bailian20231229Client} client - 客户端（Client）
 * @param {string} workspaceId - 业务空间ID
 * @param {string} indexId - 知识库ID
 * @param {string} fileId - 文件ID
 * @returns {Promise<bailian20231229.DeleteIndexDocumentResponse>} - 阿里云百炼服务的响应
 */
async function deleteIndexDocument(client, workspaceId, indexId, fileId) {
    const headers = {};
    const req = new bailian20231229.DeleteIndexDocumentRequest({
        indexId,
        documentIds: [fileId],
    });
    const runtime = new Util.RuntimeOptions({});
    return await client.deleteIndexDocumentWithOptions(workspaceId, req, headers, runtime);
}
```

## C#

```
/// <summary>
/// 从指定的文档搜索类知识库中永久删除一个或多个文件
/// </summary>
/// <param name="client">客户端（Client）</param>
/// <param name="workspaceId">业务空间ID</param>
/// <param name="indexId">知识库ID</param>
/// <param name="fileId">文件ID</param>
/// <returns>阿里云百炼服务的响应</returns>
public AlibabaCloud.SDK.Bailian20231229.Models.DeleteIndexDocumentResponse DeleteIndexDocument(
    AlibabaCloud.SDK.Bailian20231229.Client client,
    string workspaceId,
    string indexId,
    string fileId)
{
    var headers = new Dictionary<string, string>() { };
    var deleteIndexDocumentRequest = new AlibabaCloud.SDK.Bailian20231229.Models.DeleteIndexDocumentRequest
    {
        IndexId = indexId,
        DocumentIds = new List<string> { fileId }
    };
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.DeleteIndexDocumentWithOptions(workspaceId, deleteIndexDocumentRequest, headers, runtime);
}
```

## Go

```
// DeleteIndexDocument 从指定的文档搜索类知识库中永久删除一个或多个文件。
//
// 参数:
//   - client (bailian20231229.Client): 客户端（Client）。
//   - workspaceId (string): 业务空间ID。
//   - indexId (string): 知识库ID。
//   - fileId (string): 文件ID。
//
// 返回:
//   - *bailian20231229.DeleteIndexDocumentResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func DeleteIndexDocument(client *bailian20231229.Client, workspaceId, indexId, fileId string) (*bailian20231229.DeleteIndexDocumentResponse, error) {
	headers := make(map[string]*string)
	deleteIndexDocumentRequest := &bailian20231229.DeleteIndexDocumentRequest{
		IndexId:     tea.String(indexId),
		DocumentIds: []*string{tea.String(fileId)},
	}
	runtime := &util.RuntimeOptions{}
	return client.DeleteIndexDocumentWithOptions(tea.String(workspaceId), deleteIndexDocumentRequest, headers, runtime)
}
```

**请求示例**

```
{
  "DocumentIds": [
    "file_0b21e0a852cd40cd9741c54fefbb61cd_10xxxxxx"
  ],
  "IndexId": "mymxbdxxxx",
  "WorkspaceId": "llm-4u5xpd1xdjqpxxxx"
}
```

**响应示例**

```
{
  "Status": "200",
  "RequestId": "2D8505EC-C667-5102-9154-00B6FEXXXXXX",
  "Message": "success",
  "Data": {
    "DeletedDocument": [
      "file_0b21e0a852cd40cd9741c54fefbb61cd_10xxxxxx"
    ]
  },
  "Code": "Success",
  "Success": "true"
}
```

## **管理知识库**

> [创建和使用知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base#81f57beb71zs1)不支持通过API操作，请使用[阿里云百炼控制台](https://bailian.console.aliyun.com/?&tab=app#/knowledge-base)操作。

### **查看知识库**

要查看给定业务空间下的一个或多个知识库的信息，可以调用[ListIndices接口](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-listindices)。

-   **client：**[如何获取client](#52ff2774f0pq9)
    
-   **workspace\_id：**[如何获取业务空间ID](https://help.aliyun.com/zh/model-studio/use-workspace#c5222ec081sbo)
    
    > 子账号只能查看自己[已加入的业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)中的知识库。
    

**重要**

-   子账号调用本示例前需获取[API权限](https://help.aliyun.com/zh/model-studio/member-management#a2e8c1d6246s2)（AliyunBailianDataFullAccess策略）。
    
-   本示例支持[在线调试](https://api.aliyun.com/api/bailian/2023-12-29/ListIndices)及多语言[代码示例生成](https://api.aliyun.com/api/bailian/2023-12-29/ListIndices?lang=JAVA&tab=DEMO)。
    

## Python

```
def list_indices(client, workspace_id):
    """
    获取指定业务空间下一个或多个知识库的详细信息。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    list_indices_request = bailian_20231229_models.ListIndicesRequest()
    runtime = util_models.RuntimeOptions()
    return client.list_indices_with_options(workspace_id, list_indices_request, headers, runtime)
```

## Java

```
/**
 * 获取指定业务空间下一个或多个知识库的详细信息
 *
 * @param client      客户端（Client）
 * @param workspaceId 业务空间ID
 * @return 阿里云百炼服务的响应
 */
public ListIndicesResponse listIndices(com.aliyun.bailian20231229.Client client, String workspaceId) throws Exception {
    Map<String, String> headers = new HashMap<>();
    com.aliyun.bailian20231229.models.ListIndicesRequest listIndicesRequest = new com.aliyun.bailian20231229.models.ListIndicesRequest();
    com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
    return client.listIndicesWithOptions(workspaceId, listIndicesRequest, headers, runtime);
}
```

## PHP

```
/**
 * 获取指定业务空间下一个或多个知识库的详细信息
 *
 * @param Bailian $client 客户端对象（Client）
 * @param string $workspaceId 业务空间ID
 * @return ListIndicesResponse 阿里云百炼服务的响应
 * @throws Exception
 */
public function listIndices($client, $workspaceId) {
    $headers = [];
    $listIndexDocumentsRequest = new ListIndexDocumentsRequest([]);
    $runtime = new RuntimeOptions([]);
    return $client->listIndicesWithOptions($workspaceId, $listIndexDocumentsRequest, $headers, $runtime);
}
```

## Node.js

```
/**
 * 获取指定业务空间下一个或多个知识库的详细信息
 * @param {bailian20231229.Client} client 客户端（Client）
 * @param {string} workspaceId 业务空间ID
 * @returns {Promise<bailian20231229.ListIndicesResponse>} 阿里云百炼服务的响应
 */
async function listIndices(client, workspaceId) {
    const headers = {};
    const listIndicesRequest = new bailian20231229.ListIndicesRequest();
    const runtime = new Util.RuntimeOptions({});
    return await client.listIndicesWithOptions(workspaceId, listIndicesRequest, headers, runtime);
}
```

## C#

```
/// <summary>
/// 获取指定业务空间下一个或多个知识库的详细信息。
/// </summary>
/// <param name="client">客户端（Client）</param>
/// <param name="workspaceId">业务空间ID</param>
/// <returns>阿里云百炼服务的响应</returns>
public AlibabaCloud.SDK.Bailian20231229.Models.ListIndicesResponse ListIndices(AlibabaCloud.SDK.Bailian20231229.Client client, string workspaceId)
{
    var headers = new Dictionary<string, string>() { };
    var listIndicesRequest = new Bailian20231229.Models.ListIndicesRequest();
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.ListIndicesWithOptions(workspaceId, listIndicesRequest, headers, runtime);
}
```

## Go

```
// listIndices 获取指定业务空间下一个或多个知识库的详细信息。
//
// 参数:
//   - client      *bailian20231229.Client: 客户端（Client）。
//   - workspaceId string: 业务空间ID。
//
// 返回:
//   - *bailian20231229.ListIndicesResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func listIndices(client *bailian20231229.Client, workspaceId string) (_result *bailian20231229.ListIndicesResponse, _err error) {
	headers := make(map[string]*string)
	listIndicesRequest := &bailian20231229.ListIndicesRequest{}
	runtime := &util.RuntimeOptions{}
	return client.ListIndicesWithOptions(tea.String(workspaceId), listIndicesRequest, headers, runtime)
}
```

**请求示例**

```
{
  "WorkspaceId": "llm-4u5xpd1xdjqpxxxx"
}
```

**响应示例**

```
{
  "Status": "200",
  "RequestId": "5ACB2EB3-6C9A-5B0F-8E60-3FBE7EXXXXXX",
  "Message": "success",
  "Data": {
    "TotalCount": "1",
    "PageSize": "10",
    "PageNumber": "1",
    "Indices": [
      {
        "DocumentIds": [
          "file_0b21e0a852cd40cd9741c54fefbb61cd_10xxxxxx"
        ],
        "Description": "",
        "OverlapSize": 100,
        "SinkInstanceId": "gp-2zegk3i6ca4xxxxxx",
        "SourceType": "DATA_CENTER_FILE",
        "RerankModelName": "gte-rerank-hybrid",
        "SinkRegion": "cn-beijing",
        "Name": "百炼手机知识库",
        "ChunkSize": 500,
        "EmbeddingModelName": "text-embedding-v2",
        "RerankMinScore": 0.01,
        "Id": "mymxbdxxxx",
        "SinkType": "BUILT_IN",
        "Separator": " |,|，|。|？|！|\n|\\?|\\!"
      }
    ]
  },
  "Code": "Success",
  "Success": "true"
}
```

### **删除知识库**

要永久性删除某个知识库，可以调用[DeleteIndex接口](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-deleteindex)。删除前，请[解除该知识库关联的所有阿里云百炼应用](https://help.aliyun.com/zh/model-studio/rag-knowledge-base#a78dc244578vx)（仅可通过阿里云百炼控制台操作），否则会删除失败。

-   **client：**[如何获取client](#52ff2774f0pq9)
    
-   **workspace\_id：**[如何获取业务空间ID](https://help.aliyun.com/zh/model-studio/use-workspace#c5222ec081sbo)
    
    > 子账号只能删除自己[已加入的业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)中的知识库。
    
-   **index\_id：**请传入[初始化知识库](#00ded5ee90ffx)时接口返回的`Data.Id`。
    

请注意：本操作不会删除您已[添加至类目中](#494345d4b1hx2)的文件。

**重要**

-   子账号调用本示例前需获取[API权限](https://help.aliyun.com/zh/model-studio/member-management#a2e8c1d6246s2)（AliyunBailianDataFullAccess策略）。
    
-   本示例支持[在线调试](https://api.aliyun.com/api/bailian/2023-12-29/DeleteIndex)及多语言[代码示例生成](https://api.aliyun.com/api/bailian/2023-12-29/DeleteIndex?lang=JAVA&tab=DEMO)。
    

## Python

```
def delete_index(client, workspace_id, index_id):
    """
    永久性删除指定的知识库。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    delete_index_request = bailian_20231229_models.DeleteIndexRequest(
        index_id=index_id
    )
    runtime = util_models.RuntimeOptions()
    return client.delete_index_with_options(workspace_id, delete_index_request, headers, runtime)
```

## Java

```
/**
 * 永久性删除指定的知识库
 *
 * @param client      客户端（Client）
 * @param workspaceId 业务空间ID
 * @param indexId     知识库ID
 * @return 阿里云百炼服务的响应
 */
public DeleteIndexResponse deleteIndex(com.aliyun.bailian20231229.Client client, String workspaceId, String indexId) throws Exception {
    Map<String, String> headers = new HashMap<>();
    com.aliyun.bailian20231229.models.DeleteIndexRequest deleteIndexRequest = new com.aliyun.bailian20231229.models.DeleteIndexRequest();
    deleteIndexRequest.setIndexId(indexId);
    com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
    return client.deleteIndexWithOptions(workspaceId, deleteIndexRequest, headers, runtime);
}
```

## PHP

```
/**
 * 永久性删除指定的知识库
 *
 * @param Bailian $client 客户端对象（Client）
 * @param string $workspaceId 业务空间ID
 * @param string $indexId 知识库ID
 * @return mixed 阿里云百炼服务的响应
 * @throws Exception
 */
public function deleteIndex($client, $workspaceId, $indexId) {
    $headers = [];
    $deleteIndexRequest = new DeleteIndexRequest([
        "indexId" => $indexId
    ]);
    $runtime = new RuntimeOptions([]);
    return $client->deleteIndexWithOptions($workspaceId, $deleteIndexRequest, $headers, $runtime);
}
```

## Node.js

```
/**
 * 永久性删除指定的知识库
 * @param {bailian20231229.Client} client 客户端（Client）
 * @param {string} workspaceId 业务空间ID
 * @param {string} indexId 知识库ID
 * @returns {Promise<bailian20231229.DeleteIndexResponse>} 阿里云百炼服务的响应
 */
async function deleteIndex(client, workspaceId, indexId) {
    const headers = {};
    const deleteIndexRequest = new bailian20231229.DeleteIndexRequest({
        indexId
    });
    const runtime = new Util.RuntimeOptions({});
    return await client.deleteIndexWithOptions(workspaceId, deleteIndexRequest, headers, runtime);
}
```

## C#

```
/// <summary>
/// 永久性删除指定的知识库。
/// </summary>
/// <param name="client">客户端（Client）</param>
/// <param name="workspaceId">业务空间ID</param>
/// <param name="indexId">知识库ID</param>
/// <returns>阿里云百炼服务的响应</returns>
public AlibabaCloud.SDK.Bailian20231229.Models.DeleteIndexResponse DeleteIndex(AlibabaCloud.SDK.Bailian20231229.Client client, string workspaceId, string indexId)
{
    var headers = new Dictionary<string, string>() { };
    var deleteIndexRequest = new Bailian20231229.Models.DeleteIndexRequest
    {
        IndexId = indexId
    };
    var runtime = new AlibabaCloud.TeaUtil.Models.RuntimeOptions();
    return client.DeleteIndexWithOptions(workspaceId, deleteIndexRequest, headers, runtime);
}
```

## Go

```
// deleteIndex 永久性删除指定的知识库。
//
// 参数:
//   - client      *bailian20231229.Client: 客户端（Client）。
//   - workspaceId string: 业务空间ID。
//   - indexId     string: 知识库ID。
//
// 返回:
//   - *bailian20231229.DeleteIndexResponse: 阿里云百炼服务的响应。
//   - error: 错误信息。
func deleteIndex(client *bailian20231229.Client, workspaceId, indexId string) (_result *bailian20231229.DeleteIndexResponse, _err error) {
	headers := make(map[string]*string)
	deleteIndexRequest := &bailian20231229.DeleteIndexRequest{
		IndexId: tea.String(indexId),
	}
	runtime := &util.RuntimeOptions{}
	return client.DeleteIndexWithOptions(tea.String(workspaceId), deleteIndexRequest, headers, runtime)

}
```

**请求示例**

```
{
  "IndexId": "mymxbdxxxx",
  "WorkspaceId": "llm-4u5xpd1xdjqpxxxx"
}
```

**响应示例**

```
{
  "Status": "200",
  "Message": "success",
  "RequestId": "118CB681-75AA-583B-8D84-25440CXXXXXX",
  "Code": "Success",
  "Success": "true"
}
```

## API参考

请参阅[API目录（知识库）](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-dir-knowledge-base/)获取最新完整的知识库API列表及输入输出参数。

## 常见问题

1.  **如何实现知识库的自动更新/同步？**
    
    ## 文档搜索类知识库
    
    使用对象存储OSS管理文件，通过函数计算FC监听文件变更事件，自动同步更新至知识库，实现知识的实时更新。详见[告别手动操作，让AI知识库自动更新](https://www.aliyun.com/solution/tech-solution/auto-updated-knowledge-base)。
    
    ## 数据查询/图片问答类知识库
    
    若要实现数据查询/图片问答类知识库的自动更新，可基于RDS数据表构建知识库。具体操作请参见[创建知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base#6028cfefaauhu)。
    
    ## 音视频搜索类知识库
    
    不支持。
    

2.  **为什么我新建的知识库里没有内容？**
    
    一般是由于没有执行或未能成功执行[提交索引任务](#bf14fb34a58vy)这一步导致。若调用[CreateIndex](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-createindex)接口后未成功调用[SubmitIndexJob](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-submitindexjob)接口，您将得到一个空知识库。此时，您只需重新执行[提交索引任务](#bf14fb34a58vy)并[等待索引任务完成](#402c6d08c3k71)即可。
    

3.  **遇到报错Access your uploaded file failed. Please check if your upload action was successful，应该如何处理？**
    
    一般是由于没有执行或未能成功执行[上传文件到临时存储](#a275d1cdd2gph)这一步导致。请在确认该步骤成功执行后，再调用[AddFile](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-addfile)接口。
    

4.  **遇到报错Access denied: Either you are not authorized to access this workspace, or the workspace does not exist，应该如何处理？**
    
    一般是由于：
    
    -   **您请求的服务地址（**[服务接入点](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-endpoint)**）有误：**以公网接入为例，如果您是中国站用户，应访问北京（公有云用户）地域的接入地址；如果您是国际站用户，应访问新加坡地域的接入地址。如果您正在使用[在线调试](https://api.aliyun.com/api/bailian/2023-12-29/CreateIndex)功能，请确认您选择的服务地址正确无误（如下图所示）。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2181138471/p952092.png)
        
    -   **您传入的WorkspaceId值不正确，或者您还不是该业务空间的成员导致：**请确认`WorkspaceId`值无误且您是该业务空间的成员后，再调用接口。[如何被添加为指定业务空间的成员](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)
        

5.  **遇到报错Specified access key is not found or invalid，应该如何处理？**
    
    一般是由于您传入的`access_key_id`或`access_key_secret`值不正确，或者该`access_key_id`已被[禁用](https://help.aliyun.com/zh/ram/user-guide/disable-an-accesskey-pair-of-a-ram-user)导致。请确认`access_key_id`值无误且未被禁用后，再调用接口。
    

6.  **遇到报错Category is mismatched，应该如何处理？**
    
    一般是由于在调用`ApplyFileUploadLease`接口申请文件上传租约时使用的`CategoryId`，与后续调用`AddFile`接口时传入的`CategoryId`不一致导致。
    
    请确保在整个文件上传流程中（从`ApplyFileUploadLease`到`AddFile`），使用同一个`CategoryId`。您可以通过`ListCategory`接口获取当前业务空间下的类目列表，确认所使用的`CategoryId`正确无误。
    

## 计费说明

知识库采用**按量付费（后付费）**，按**小时**统计下方计费项的用量，并从您的阿里云账户自动扣费。请确保账户余额充足（可前往[费用与成本](https://usercenter2.aliyun.com/home)充值），以免因[欠费](https://help.aliyun.com/zh/model-studio/billing-for-knowledge-base#ece89cd5852lm)导致服务中断。

**计费项**

**说明**

**规格费用**

`标准版` 或 `旗舰版` 知识库的实际运行时长费用，价格详见[知识库计费说明](https://help.aliyun.com/zh/model-studio/billing-for-knowledge-base)。变更配置按变更时间点[分段计费](https://help.aliyun.com/zh/model-studio/billing-for-knowledge-base#d90304901atdb)。

**向量、排序模型调用费用**

创建、更新或检索知识库时会调用向量（embedding）、排序（rerank）模型，会产生费用。按输入 Token 用量计费，价格以[模型调用计费](https://help.aliyun.com/zh/model-studio/model-pricing)页为准。

**账单查询：**[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)

## 错误码

如果调用本文中的API失败并收到错误信息，请参见[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)进行解决。
