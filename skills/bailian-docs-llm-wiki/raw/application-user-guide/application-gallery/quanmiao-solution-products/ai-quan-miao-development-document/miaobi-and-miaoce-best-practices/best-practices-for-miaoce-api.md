# 妙策API最佳实践

本文提供妙策链路 API的最佳示例，帮助您快速入门并开发您自己的业务应用。

## 前提要求

-   阿里云账号已开通产品；
    
-   获得AgentKey、AccessKeyId、AcccessKeySecret：[获取 AccessKey 与 AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)；
    
-   获取WorkSpaceId [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)；
    
-   引入妙笔SDK [注意获取最新SDK版本](https://api.aliyun.com/api-tools/sdk/AiMiaoBi?version=2023-08-01&language=java-async-tea&tab=primer-doc)；
    

```
<dependency>
  <groupId>com.aliyun</groupId>
  <artifactId>alibabacloud-aimiaobi20230801</artifactId>
  <version>1.0.81</version>
</dependency>
```

-   引入其他三方依赖。
    

```
<dependency>
      <groupId>org.projectlombok</groupId>
      <artifactId>lombok</artifactId>
      <version>1.18.30</version>
  </dependency>

  <dependency>
      <groupId>com.alibaba.fastjson2</groupId>
      <artifactId>fastjson2</artifactId>
      <version>2.0.21</version>
  </dependency>

  <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <version>5.8.1</version>
  </dependency>
```

## 新闻话题聚合

> 给定一批内容，按照语义聚合成不同的主题。

```
package org.example.miaoce;

import com.alibaba.fastjson2.JSONObject;
import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.AsyncClient;
import com.aliyun.sdk.service.aimiaobi20230801.models.*;
import darabonba.core.client.ClientOverrideConfiguration;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.stream.Collectors;

@Slf4j
public class MiaoCeSubmitDocClusterTaskTest {

    public static AsyncClient asyncClient() {

        //accessKeyId
        String accessKeyId = System.getenv("accessKeyId");

        //accessKeySecret
        String accessKeySecret = System.getenv("accessKeySecret");

        //域名:aimiaobi.cn-beijing.aliyuncs.com
        String domain = System.getenv("domain");

        return AsyncClient.builder().credentialsProvider(StaticCredentialProvider.create(Credential.builder()
                .accessKeyId(accessKeyId).accessKeySecret(accessKeySecret).build())).serviceConfiguration(Configuration.create().setSignatureVersion(SignatureVersion.V3)).overrideConfiguration(ClientOverrideConfiguration.create().setProtocol("HTTPS")
                .setEndpointOverride(domain)).build();
    }

    /**
     * 提交文档聚类任务
     */
    @Test
    public void testDocClusterTaskTest() throws ExecutionException, InterruptedException, IOException {
        String agentKey = System.getenv("AgentKey");

        List<SubmitDocClusterTaskRequest.Documents> documentList = buildDocuments();

        //构建请求对象
        AsyncClient asyncClient = asyncClient();

        //提文档聚合任务
        SubmitDocClusterTaskResponse response = asyncClient.submitDocClusterTask(SubmitDocClusterTaskRequest.builder().agentKey(agentKey).documents(documentList).build()).get();

        SubmitDocClusterTaskResponseBody.Data data = response.getBody().getData();

        log.info("response: {}", JSONObject.toJSONString(response));

        //获取TaskId
        String taskId = data.getTaskId();

        //轮询任务状态，直到状态不为 RUNNING 或者 PENDING
        GetDocClusterTaskResponse response1;
        while (true) {
            response1 = asyncClient.getDocClusterTask(GetDocClusterTaskRequest.builder().agentKey(agentKey).taskId(taskId).build()).get();

            log.info("response1: {}", JSONObject.toJSONString(response1));

            //RUNNING PENDING 时继续轮询
            if ("RUNNING".equals(response1.getBody().getData().getStatus()) || "PENDING".equals(response1.getBody().getData().getStatus())) {
                Thread.sleep(1000);
            } else {
                break;
            }
        }

        if (response1.getStatusCode() == 200) {
            //获取聚类结果
            for (GetDocClusterTaskResponseBody.Topics topic : response1.getBody().getData().getTopics()) {
                log.info("topic: {}", JSONObject.toJSONString(topic));
            }
        }
    }

    private static List<SubmitDocClusterTaskRequest.Documents> buildDocuments() throws IOException {

        List<String> contents = new ArrayList<>();

        contents.add("作为全球顶级展会之一，柏林国际电子消费展（IFA）不仅仅是厂商秀实力、消费者了解新产品的窗口，更是整个行业发展的风向标。\\n雷科技报道团已飞赴德国·柏林，发掘各家厂商的最新动向。雷科技发现，在本届IFA大会上，中国、德国、日本、土耳其等不同国家的家电企业，都在强调产品和智能家居解决方案的节能属性，几乎将电子消费展变成了“节能产品展览会”。琳琅满目的展品、各大企业秀肌肉的节能方案，将IFA2024推向了高潮。\\n100年前，IFA刚诞生之时，以电力为能源的设备正在逐渐普及。100年后，电力支撑起了现代社会，但我们却开始思考如何节能减排，减少电力能源的使用。本届IFA上，来自全球各地的企业各显神通，向广大消费者展示了他们在节能减排方面的研究成果。\\n1、长虹、美的们AllForAI，用AI助力节能减排。\\n从AIIInAI到AllForAI，人工智能正以迅雷不及掩耳之势席卷全球，渗透到生活的方方面面，而AI俨然已成为节能减排的强大助力。\\n美的于IFA2024首次展出了AIECO智慧节能解决方案，该方案可以通过千亿级设备运行数据库和云端实时天气、电费数据等信息，结合搭载全新大数据预学习模型的AI算法，对环境、材质等信息实时分析，实现智能决策和精准控制设备能耗，能够有效降低30%的家电能耗。\\n（图源：雷科技摄制）\\n长虹则推出了“长虹美菱智汇家AI大模型”，基于80亿级参数，为长虹旗下的冰箱、洗衣机、空调等设备加入了“思考”能力。以洗衣机为例，长虹的产品可以根据衣服材质与状态，提供不同的洗涤和烘护方案，一方面可以确保衣服干净卫生不受损，另一方面也能有效降低能耗。\\n（图源：雷科技摄制）\\n其他TCL、海信、海尔、三星等企业，也纷纷以AI技术为核心，搭配感知和决策系统，定制智能能耗方案，推出了多款能耗低于A级标准的产品。国内家电企业在IFA2024上展示的绿色家电不但做到了节能减排，而且更符合欧洲消费者的需求，也展现出了中国企业的技术实力，或将成为国内家电企业引领全球家电行业发展的开端。\\n2、VESTEL们的新理念：全屋节能才是真节能。\\n自从家电行业进入智能化时代，家电设备之间就不再是孤立状态，顺应消费者的需求，在研发节能技术的同时，家电企业也开始布局全屋节能解决方案。\\nIFA2024上，美的展出了冰箱、洗衣机、热水器等多种支持AIECO智慧节能解决方案的家电产品，TCL、海信、海尔等企业同样如此。这些企业的节能减排方案不局限于“省电”，还在尽量使用可回收物，尤其是塑料材质，进而减少对化石燃料的依赖。\\n（图源：雷科技摄制）\\n欧洲三大电视制造商之一的土耳其品牌VESTEL，除了发布在能耗不变的前提下，亮度可以提升60%的新款65英寸电视RevolutionaryEnergy-SavingTV之外，也公布了全屋节能方案。包含电池、空调、洗衣机等各类设备在内，均做到了静音、低功耗。\\n（图源：雷科技摄制）\\n现阶段大多数全屋节能方案依赖AI技术，是因为设备之间缺少联动，利用热泵技术实现的三联供，是降低能耗、提升能量利用效率的有效方案。本次IFA大会上，TCL展出的R290三联供空调就集供暖、制冷、生活热水等功能于一体，将空调制冷时“搬运”的热量用于加热生活用水，把烧热水的成本省去了。\\n（图源：雷科技摄制）\\n从三联供到AI节能，国内外企业都在发力“绿色家电”，将IFA2024视为“节能技术展”也不为过。IFA2024上企业关注节能减排的关键原因之一或许在于，无论是欧洲本地家电企业，还是来自全球其他地区的企业，想要在欧洲市场发展，节能是必须面对的问题。\\n节能减排是全球性问题，但欧洲无疑是节能减排的主要推动者，瑞典00后环保少女格蕾塔·桑伯格甚至被选入《时代》周刊“影响世界的一百位名人”。实地探访欧洲后，小雷认为欧洲人重视节能减排主要有三大原因。\\n首先，欧洲绿色消费观念深入人心。IFA展台熙熙攘攘的外国人，对家电企业展出的产品表现出了浓厚的兴趣，这种对待节能减排的态度，为绿色家电在欧洲发展提供了土壤。\\n（图源：雷科技摄制）\\n面对新事物电动汽车，欧洲多个国家率先公布了禁售燃油车时间表，部分车企也陆续宣布了停产停售燃油车时间。为进一步确保新能源汽车的环保，欧洲还要求车企加强电池回收管理。\\n欧盟早已于20世纪90年代实现了碳达峰，如今碳排放量已呈现下滑趋势。今年第一季度欧盟温室气体排放量大约8.94亿吨，同比下滑4%。\\n其次，欧洲存在能源危机。目前欧洲消费者使用的石油、天然气等能源依赖进口，一旦进口渠道出现问题，就可能面临能源储备不足的情况。2022年9月北溪管道发生断裂事件后，欧洲立刻爆发了天然气危机。\\n能源危机爆发后，欧盟多个国家推出了限电措施，给当地居民生活带去了诸多不便，冬季一些欧洲居民为取暖不得不砍树烧柴。\\n最后，欧洲电费太贵了。身处德国柏林，小雷切身感受到了空调有多么重要。欧洲许多酒店压根没有空调，还有一些酒店虽然有空调，但舍不得把档位开高，就连地铁也给人一种闷热的感觉。尽管德国属于温带海洋气候，气温相对没那么高，但夏季依然会感到闷热。\\n（图源：雷科技摄制）\\n问过当地居民才知道，原来是因为当地电费太高，不仅仅是个人不舍得用电，一些企业用电都有些“抠抠搜搜”。\\n2023年德国平均电费大约0.45欧元/kWh（约合人民币3.54元/kWh），而月收入中位数仅3796欧元。再加上房租、饮食等其他生活成本，也难怪许多欧洲人不愿意装空调，不舍得用空调。\\n前段时间法国巴黎奥运会，因奥运村没有安装空调还曾登上过热搜。电费过于昂贵的问题还影响到了欧洲新能源汽车行业的发展，我们购买新能源汽车是因为家用电就0.5元/kWh左右，充电站一般也就1.5元/kWh左右，比燃油车出行成本低不少。当前德国油价也就1.75欧元/L（约合人民币13.76元/L）左右，电动车没有任何出行成本优势。\\n（图源：雷科技摄制）\\n以上因素导致，欧洲消费者对于低能耗家电的需求高于国内。IFA2024上各大企业纷纷拿出节能减排方案，奔向绿色生活方式的同时，也在深度布局欧洲市场，用技术实力征服当地消费者。\\n家电产品关于节能方向的探索早已有之，AI技术的加入将家电节能解决方案带上了新高度，但IFA2024只是家电企业探索节能方案新阶段的开始，节能减排的征程还将在更多新技术的加持下迈向更高的山峰。\\n通过AI感知+决策，智能调整设备工作状态，从而降低家电功耗，是本届IFA大会家电企业的一致选择。但对于整个家电企业节能减排大方向而言，AI只能起到部分作用，如何提高能量利用效率同样重要。\\n一位TCL空调工程师告诉小雷，国内消费者不太在意的“三联供”系统，在欧洲十分受欢迎，不少人购买空调时会优先选择三联供空调，将空调废热预热用于加热生活用水，可以节省不少电费。小雷认为，其中的原因或许在于国内电费便宜，对于热泵的需求度没有那么高。\\n（图源：雷科技摄制）\\n不过国内各类热泵技术也在飞速发展，除了三联供空调外，其他如热水器、洗衣机等，都加入了热泵技术，可以利用电器产生的废热和空气中的热量加热水源或烘干衣物。\\n另外，国内厂商也在尝试通过光伏技术解决家庭用电难题，如TCL中环与TCL光伏科技联合打造的智慧家庭解决方案，将光伏发电设备、储能系统、热泵、电动汽车充电桩、家用电器等设备相融合，打造出了一套一体化管理系统，可以将光伏发电存储起来，以达到节能减排效果。\\n中国是全球光伏产业第一大国，TCL、格力等企业都在将家电与光伏设备结合，缓解电网压力的同时，也能减少用户电费支出，甚至在房屋无人居住的状态下，光伏设备还能发电后卖给电网，帮助用户“赚外快”。\\n能量不是无穷无尽的，节能减排可能是未来人类社会永恒的话题，国内外企业正一步步探索节能减排路线。发达国家云集的欧洲地区，经济水平较高，再加上基础电力价格昂贵，当前对于节能家电的接受程度较高。\\nIFA2024上，各大家电企业展出的产品，指明了发展与节能减排技术的发展趋势与路线，AI、三联供、光伏等技术，将成为目前降低用户使用成本、降低电网压力的三大主流方案。相信接下来其他尚未加入节能减排阵营的企业，也会加紧研发AI与三联供技术，致力于提高绿色家电的渗透率，为全球节能减排作出贡献。");

        contents.add("　　文 丨 新浪科技 周文猛　　“今年的IFA展会现场，一半企业来自中国。”这是一位德籍华人参观2024德国柏林消费电子展后的感慨。　　这样的一番感慨，并没有夸大其词。此时远在德国，2024柏林消费电子展（简称“IFA2024”）正式举办，来自中国、欧美、日韩等国家的家电及消费电子企业，共同出席有着百年历史的展会。　　作为同样走进IFA展会现场的媒体，新浪科技走遍整个IFA展馆发现，2024年现场，除美的、海尔、TCL、创维、长虹、海信等老牌家电企业外，包括追觅、石头科技、徕芬、SKG等在内的新锐家电品牌，以及大疆、荣耀、极米等消费硬件品牌，均出席了展览，且占据了主要展馆接近一半的展位。　　在国内家电及消费电子行业增速放缓，同质竞争越来越激烈的当下，出海正成为国内企业共同的选择。这一过程中，由供应链和人工智能等新兴技术发展所带来的竞争优势，帮助越来越多的国内企业走向全球。　　中国厂商们“秀肌肉”　　今年是IFA展会100周年，也是TCL首次包馆展示自身及上下游协同创新成果的一年。从IFA展会北门入场，右转跨过由多家中小型外企组成的20号馆，紧接着便是TCL包下的21号展馆。　　今年IFA展会，TCL通过TCL实业和TCL科技两大主体，围绕智能终端、半导体显示、新能源光伏三大产业进行展示。带来万级分区QD-Mini LED电视X11H，和号称全球最大的115吋QD-Mini LED电视X955 Max等终端产品。同时还发布了105“高刷曲面电竞显示屏，展出了57”8K曲面MLED电竞显示屏等。　　据TCL工作人员介绍，目前TCL已在全球建立46个研发中心、33个制造基地，业务范围超过160个国家和地区，过去5年海外营收从590亿元增长至1252.8亿元。　　穿越TCL展馆进入22号馆，首先进入视野的是长虹电器。今年，长虹携全屋AI家电参展，同时发布了沧海智能体AI TV和长虹美菱智汇家AI大模型。据悉，沧海智能体AI TV能交流、能思考、会成长，长虹美菱智汇家AI大模型则拥有80亿级参数规模，可将大模型嵌入到冰箱、洗衣机、烘护机和空调等家电中。　　进入由海信和创维共同承包的23号馆，海信展出的《黑神话：悟空》官方定制电视，展示了大型国产3A游戏的高画质，让悟空的衣服褶皱、金箍棒花纹等细节生动显现。　　穿过23号馆后的微型展馆，紧接着便到了美的集团承包的5-1号展馆。今年IFA，美的携旗下家用空调、厨房电器、洗护产品等参展，并且首次展示了AI ECO智慧节能解决方案，该方案搭载大数据预学习模型的AI节能算法，能对环境、材质等各类条件进行智能分析、预测并综合智能决策与节能精控，使家电能耗平均降低30%。　　“欧洲四季分明同时电气化程度较高，用电需求量大，现在欧洲能源价格上涨，当地居民用电成本极高，用技术手段提升能源效率，是市场需求，也是我们响应全球绿色低碳可持续发展的承诺。”美的国际业务智能产品人员对新浪科技表示。　　此外，在3-1号馆和6-2号馆，由海尔、荣耀为代表的国内参展企业，也占据了半数过半场馆。　　在9号展馆，由科沃斯、石头科技、追觅科技、徕芬等为代表的新锐家电企业，占据了绝大部分展馆，几乎联合承包了整个展馆。　　此外，大疆创新、极米科技、SKG等新锐科技企业，也在展馆不同位置出现，不断扩大着IFA展会上的中国企业阵营。　　“被动布局，为了不被拉开距离”　　近半展馆被中企承包背后，到全球市场寻找新的业绩增长点，正在成为越来越多中国家电及消费电子企业的必答题。　　在与新浪科技沟通中，TCL实业欧洲营销本部总经理李永平直言，“近几年国内市场竞争非常，所以很多品牌或者企业都想在海外寻找新的增长点，欧洲虽然过去几年整个市场是承压的，新增需求更新速度相对来讲也没有其他市场快，但整个欧洲消费体量大，而且消费结构高，在品牌、在产品服务上能够做到更好的增值或者差异化，能获取的价值空间会比较高，所以在欧洲做到比较大规模的同时，也会带来更好的利润价值。”　　美的国际业务智能系统相关负责人同样对新浪科技表示，“美的布局全球化多年，全球化早已是不可分割的一部分，欧洲等海外市场份额足够大，空间足，在这些市场结合公司长期技术积累和供应链优势，研发出符合当地市场的产品，便能取得快速的增长。”　　随着中企全球化步伐的开展，国内不断被提及的人工智能技术等智能产品理念，随着企业的不断实践，通过IFA向外展示。在美的、海尔、TCL、海信、荣耀等展馆，有关人工智能技术相关的词汇不断闪现。但对于数据隐私保护严密，绝大多数餐厅点菜仍处于人工点菜模式的欧洲市场而言，消费者们对于这项技术的拥抱程度，并没有想象中高。　　“这个市场需要高投入、长期坚持，要烧很多的钱去做产品，同时要投入很多的钱做品牌，大家对固有品牌的信任度非常高，不太容易接受新的产品，对于人工智能这些技术的接受度也不太高，目前企业在这个布局AI，更多的是出于战略布局的目的，被动布局，为了不被轻易拉开距离。”某家电巨头业务负责人对新浪科技表示。　　大举出海的背后，国内企业在全球市场的布局，也正因区域文化和消费者需求的不同，面临着新的挑战。责任编辑：江钰涵 ");

        contents.add("九月初的小雷，工作日程显得格外忙碌。\\n这柏林的天气虽好，但我却没有多少欣赏的闲暇时间，简单洗漱过后，草草品尝一下我并不怎么习惯的酒店早餐，然后便该看准时间朝德国柏林会展中心出发了。\\n早啊各位，欢迎来到IFA2024（2024年德国柏林国际消费电子展）的第二天。\\n诞生于1924年的IFA（柏林国际电子消费品展览会，前身为柏林国际广播展），迄今已有100年的历史，作为全球三大消费电子展会之一，更重要的是下半年唯一一个大型消费电子展会，自然吸引了全世界的高度关注。\\n（图源：雷科技摄制）\\n与CES上展示的炫目技术不同，也有别于MWC面向运营商和ISP的技术发布，IFA展出的许多技术和产品真的可以在不久的将来买到并使用。这种「务实」的特点，在我看来，正是IFA能够从1924年一路延续至今的重要原因之一。\\n那么今天，也是时候把目光放回到IFA的主角——白色家电身上了。\\n中国白电，闪耀IFA\\n不得不说，出现在IFA展会上的中国品牌数量远超我的预期。\\n与CES、MWC展会需要从大量初创企业中挖掘中国品牌不同，IFA几乎随处可见中国品牌的身影。\\n海尔：从产品到场景\\n在海尔智家展区入口，最醒目的位置，是海尔参展的冰箱、洗衣机产品。\\n步入海尔智家展区，不少欧洲采购商、零售商都是奔着Cube90系列冰箱而来。这款搭载「全空间保鲜科技」的智能冰箱刚刚在米兰国际厨房展上大放异彩，通过干湿独立分区，将果蔬与干货的储藏区域，以不同的适宜湿度分隔开来，可将湿区抽屉内果蔬保存时间延长2倍。\\n诸如此类的创新科技，在海尔智家展区之中并不罕见，例如海尔朗境X11展示了其独创的风巡航科技，可实现2分钟全面置换筒内空气；搭载自然风循环系统的海尔WineBank60Series7，则通过自然风循环系统，再现了真实的葡萄酒地下室条件，可以同时存储红葡萄酒、白葡萄酒和香槟，非常有意思。\\n（图源：雷科技摄制）\\n以海尔为代表的中国品牌，让世界看到了「中国创造」的魅力。\\n而这样的魅力，不仅体现在出色的单品上，更体现在海尔智家一直致力于实现的智能生态场景中。\\n海尔智家在欧洲推出的生态系统——hOn，可同时管理海尔、Candy、Hoover三大品牌互联产品和智慧场景，更是集AI、机器学习技术、智能传感器于一体，为用户打造符合个性需求的多样化家居场景。\\n（图源：雷科技摄制）\\n在智慧厨房场景下，每一件厨电都是整个厨房生态中不可或缺的一环。冰箱可以联动烤箱一键烤制；烟机可以感知灶具功率自动调节风量；烤箱通过仿生智能科技智慧互联后可以向用户推荐食谱。立足智能化发展方向，基于最先进的仿生智能技术，为用户打造符合个性需求的智能场景方案，或许就是海尔智家想要实现的未来。\\n三星：带来进阶节能体验\\n对三星电子这种国际大厂来说，IFA2024确实是个不错的展示机会。\\n所以他们不仅包下了一整个展馆，还特地展出面向欧洲生活方式打造的全新节能家电系列——拥有A-55%额外能效的三星BespokeAI™洗衣机、达到洗烘全程A级能效的BespokeAI™洗烘一体机以及拥有A-10%能效的Bespoke洗碗机。\\n（图源：三星）\\n没错，这次三星主打的是节能牌。\\n在这三款产品中，最夸张的就是三星BespokeAI™洗衣机，借助全新的BubbleShot技术，通过循环泵将洗涤剂和水抽出并喷洒到滚筒内的衣物上，这款产品的理论能耗要比欧洲A级能效等级的最低要求低55%，同时洗涤效果也获得了不错的提升。\\n不过该型号计划在明年发布，今年欧洲用户看来是用不上了。\\n还有全新的三星BespokeAIHybrid冰箱，其采用了压缩机和珀尔帖混合式制冷技术，可使冰箱在能耗超出日常使用量时做出智能调整进而实现节能，例如在冰箱门打开的时间较长时，能耗较低的珀尔帖制冷技术就能够作为额外的冷却源以提高整体能效。\\n从某种意义上来说，这或许也是一种「混动式」家电了吧。\\n（图源：雷科技摄制）\\n按照官方的说法，三星在其产品中继续优先考虑能源效率，并致力于借助AI技术实现这一目标，比如在冰箱、洗衣机等电器中内置AI功能，或是利用AI功能释放其SmartThings生态系统的潜力，从而节省更多能源。\\n在不知不觉中，AI已经深入我们生活中的方方面面。\\n美的：体验AIECO智慧节能\\n要说美的这次展出的重点是什么，那一定是首次展示的AIECO智慧节能解决方案。\\n按照官方说法，该方案基于千亿级的设备运行数据库及通过云端连接获取的实况天气、电费等第三方数据，运用了搭载全新大数据预学习模型的AI节能算法，有效对环境、材质等各类条件进行智能分析、预测并综合智能决策与节能精控，使家电能耗平均大幅度降低30%。\\n（图源：雷科技摄制）\\n以空调为例，随着户外环境温湿度的变化，传统空调即便设定在相同的温度，也难以维持用户感受上的恒温，人们的体感往往会因忽冷忽热而感到不适。尤其在夜晚，空调的持续运行有时可能导致室内温度过低，影响睡眠质量；与此同时，频繁反复的温度调节也会增加空调的耗电。\\n而搭载该方案的空调，就可以预判室内热负荷变化，并提前做出精准控温，实现能源使用效率的重大飞跃。\\n此外，美的展台中央还展示了支持美的AIECO智慧节能解决方案的多款家电产品，包含冰箱、洗衣机、热水器等。\\n（图源：雷科技摄制）\\n根据不同产品在使用过程中可能出现异常耗电的情况，美的采用全面定制化的AIECO算法，就像是一个隐形的智能能源管家，为日常家庭生活中的多种场景提供全面的节能解决方案。\\n通过多元的绿色家电产品解决方案，美的展示出积极投身并引领行业的可持续发展理念与绿色转型决心。\\n这和目前能源紧缺的欧洲市场，确实是很搭的组合。\\n长虹：首发白电垂域大模型\\n要在大半年前，有人和你说以后冰洗产品也会用上AI，我想大多数人肯定不信。\\n但在IFA2024展会上，长虹真的发布了行业首个白电垂域大模型——长虹美菱智汇家AI大模型。\\n（图源：雷科技摄制）\\n根据官方介绍，长虹美菱智汇家AI大模型则拥有80亿级参数规模，能够嵌入到冰箱、洗衣机、烘护机和空调等家电中，使它们具备“思考”能力。\\n放在现实场景中，这一大模型能够理解用户需求，预见用户喜好，提供更加精准的服务。例如衣物材质与状态，为用户提供最佳的洗涤和烘护方案的AI净衣技术；根据食材特性，为用户提供最佳的保存环境，以及专属的健康食谱建议的AI鲜冻技术；以此来打造适合每名用户自己生活习惯的AI家电。\\n在我看来，此次长虹发布的AI大模型技术，将推动长虹在智能技术的深度探索，其不仅仅带来了技术的进步，也将在未来将进一步改变智能家居生态。\\nTCL：当AI与实用主义交融\\n既然来都来了，那肯定要去看一下TCL实业的展区。\\n该说不说，虽然TCL以其出色的电视产品闻名，但他们的空冰洗产品同样令人印象深刻。\\n先说我看到的这台TCLFreshIN3.0空调吧，这款采用了可升降式新鲜空气入口“FreshIN”的专利设计，可在新鲜空气进入房间时对用户进行通知，搭配上行业领先的TVOC检测系统，让用户能够一目了然地监测空气质量，搭配上超省电的AI大数据模型算法，能够智能感知环境温度变化，精准调控运行频率，节能率高达40%。\\n（图源：雷科技摄制）\\nTCL还展出了自家引以为傲的超薄平嵌系列冰箱，1mm的无缝式嵌入设计，可完美匹配传统600mm橱柜；冷藏室T-Fresh系统能在48小时内灭杀99.99%的细菌，延长食物保鲜期；第四代微孔发泡技术和真空绝缘材料的使用，让冰箱存储空间更大。\\n不难看出，在积极拥抱AI技术的同时，TCL对家电本身的核心功能与设计也很看重，力求为用户解决实际问题，带来更便捷的生活体验。\\n照目前势头发展下去，TCL白电业务正在迅速跻身头部阵营。\\n海信：加快场景化升级\\n在去年IFA展上，海信首次公布了未来的技术战略：以场景致未来。\\n在今年IFA展上，海信更进一步，启动实施场景化升级，从提供单一产品转变到提供场景解决方案，为白电产品提供了智能洗衣、智能厨房和智能空气护理三个主要场景。\\n海信Series7i洗衣机系列通过远程监控和自动调整功能简化了衣物护理过程；海信智能大屏冰箱允许用户应用远程调节温度设置，并通过AIEco功能一键激活节能模式；海信的EnergyProX空调系列则提供实时监控室内空气质量，让用户远程根据需要进行调整。\\n（图源：雷科技摄制）\\n这些产品不仅提升了家电的智能化水平，也为用户提供了更加直观和便捷的智能生活体验。\\n除了产品外，海信还展示了可再生材料、非石油基材料、咖啡渣材料在家电整机上应用的环保材料。\\n按照现场人员介绍，海信冰箱研发团队经过长期的技术攻关，开创生物基材料产品应用的行业先例，冰箱产品再生材料使用占比可达到40%以上，可回收利用率超过80%。\\n不难看出，海信正在构思着一个智慧、绿色、健康的未来生活空间。\\n要高端智能，更要绿色节能\\n不得不说，这股囊括了整个消费市场的AI之风，还真有种吹向白电市场的趋势。\\n美的运用了搭载大数据预学习模型的AI节能算法，打造出符合自身核心理念的AIECO智慧节能解决方案；长虹则更具突破性一些，带来了行业首个白电垂域大模型——长虹美菱智汇家AI大模型，希望借此理解用户需求，预见用户喜好，提供更加精准的服务。\\n（图源：雷科技摄制）\\n至于「AllinAI」的三星，也在展会上推出了具备升级Bixby语音助手功能的Bespoke缤色铂格套系智能家电，升级后的Bixby可以理解用户对话中的多个指令，同时结合之前的情境执行连续指令，比如，用户可以通过语音指令启动洗衣机、调节空调温度或查询冰箱内的食物库存，并获得推荐更健康的食谱。\\n这些智能家电不仅提高了用户的生活质量，还展示了AI技术在家电领域的广泛应用前景。\\n不过在AI技术的表面下，其实各家厂商追求的还是更基础的实用主义。\\n就这么说吧，因为白电是更加贴近于日常生活的产品，你很难在白电上，看到类似于手机、电脑、电视上所强调的AIGC功能。\\n取而代之的，则是一系列比较明确的实用性功能，例如「借助AI识别面料智能匹配洗涤算法」或者是「借助AI识别当前场景控制空调出风」之类的，都是在产品的核心功能上做强化。\\n（图源：雷科技摄制）\\n具体到卖点上，在类似于冰箱这样的产品上，薄嵌设计和保鲜技术显然更加受欢迎；放在洗衣机与烘干机上，解决的则是「如何才能把衣服彻底洗干净」这个问题；而在空调上，问题的关键就变成了是否省电、新风系统体验如何以及「能不能让我进入精致睡眠」。\\n有趣的是，在今年的展台里，出现了几乎每家厂商都在强调自身借助AI能力达到节能效果的场景。\\n（图源：雷科技摄制）\\n而出现这种情况的深层原因，则是欧洲地区积年累月形成的能源危机问题。\\n近年来，突发的地缘政治事件，对整个欧洲能源市场产生了重大影响，曾经最大的天然气和石油供应国的断供，再加上由于白左抗议而导致维护和关闭的大批核电站，导致欧洲目前处于严重的能源危机中。\\n为了应对这一挑战，欧洲各国与欧盟采取了一系列措施，从2021年3月1日起，欧盟的能效标签等级有所调整，在旧能效等级标准下的A+++级产品，转换为新能效等级后基本在A级到C级区间，新能效等级划分显然更为严格。\\n但是在此基础上，海尔、美的、TCL、长虹等国内厂商均在IFA上推出了多款比欧洲A级能源标准更节能的产品。\\n这些节能家电不仅有助于降低能源消耗，还能帮助消费者节省电费，符合欧洲市场对可持续发展的需求，最重要的是向世界展示了中国在节能领域的卓越成就，「绿色节能」或将成为国产家电引领海外市场的又一大关键。\\n说在最后\\n在IFA2024上，我看到了白色家电市场的最新趋势，AI技术的应用、实用主义的回归以及对节能环保的重视，俨然成为未来全球市场的主要发展方向。\\n在我看来，作为国内企业接触欧洲市场的第一站，IFA不仅是展示新产品和技术的机会，更是深入了解欧洲消费者需求和市场动态的关键渠道。\\n（图源：雷科技摄制）\\n随着中国品牌在全球影响力的提升，越来越多的企业向世界展现出强大的创新力，凸显了中国品牌在全球市场中的引领地位，进一步提升了国际市场对中国品牌的认知与信赖。\\n如果说IFA的百年历程，是中国品牌走向世界、影响世界的生动写照。\\n那么在下一个百年，希望国内企业能够继续在全球科技浪潮中扮演重要角色，推动技术进步和市场发展，持续创新产品和技术应用，为全球消费者带来更多高品质的产品与服务，为更多全球用户打造美好生活。");

        contents.add("九月初的小雷，工作日程显得格外忙碌。\\n这柏林的天气虽好，但我却没有多少欣赏的闲暇时间，简单洗漱过后，草草品尝一下我并不怎么习惯的酒店早餐，然后便该看准时间朝德国柏林会展中心出发了。\\n早啊各位，欢迎来到IFA 2024（2024年德国柏林国际消费电子展）的第二天。\\n诞生于1924年的IFA（柏林国际电子消费品展览会，前身为柏林国际广播展），迄今已有100 年的历史，作为全球三大消费电子展会之一，更重要的是下半年唯一一个大型消费电子展会，自然吸引了全世界的高度关注。\\n\\n（图源：雷科技摄制）\\n与CES上展示的炫目技术不同，也有别于MWC面向运营商和ISP的技术发布，IFA展出的许多技术和产品真的可以在不久的将来买到并使用。这种「务实」的特点，在我看来，正是IFA能够从1924年一路延续至今的重要原因之一。\\n那么今天，也是时候把目光放回到IFA的主角——白色家电身上了。\\n中国白电，闪耀IFA\\n不得不说，出现在IFA展会上的中国品牌数量远超我的预期。\\n与CES、MWC展会需要从大量初创企业中挖掘中国品牌不同，IFA几乎随处可见中国品牌的身影。\\n海尔：从产品到场景\\n在海尔智家展区入口，最醒目的位置，是海尔参展的冰箱、洗衣机产品。\\n步入海尔智家展区，不少欧洲采购商、零售商都是奔着Cube 90系列冰箱而来。这款搭载「全空间保鲜科技」的智能冰箱刚刚在米兰国际厨房展上大放异彩，通过干湿独立分区，将果蔬与干货的储藏区域，以不同的适宜湿度分隔开来，可将湿区抽屉内果蔬保存时间延长2倍。\\n诸如此类的创新科技，在海尔智家展区之中并不罕见，例如海尔朗境X11展示了其独创的风巡航科技，可实现2分钟全面置换筒内空气；搭载自然风循环系统的海尔Wine Bank 60 Series 7，则通过自然风循环系统，再现了真实的葡萄酒地下室条件，可以同时存储红葡萄酒、白葡萄酒和香槟，非常有意思。\\n\\n（图源：雷科技摄制）\\n以海尔为代表的中国品牌，让世界看到了「中国创造」的魅力。\\n而这样的魅力，不仅体现在出色的单品上，更体现在海尔智家一直致力于实现的智能生态场景中。\\n海尔智家在欧洲推出的生态系统——hOn，可同时管理海尔、Candy、Hoover三大品牌互联产品和智慧场景，更是集AI、机器学习技术、智能传感器于一体，为用户打造符合个性需求的多样化家居场景。\\n\\n（图源：雷科技摄制）\\n在智慧厨房场景下，每一件厨电都是整个厨房生态中不可或缺的一环。冰箱可以联动烤箱一键烤制；烟机可以感知灶具功率自动调节风量；烤箱通过仿生智能科技智慧互联后可以向用户推荐食谱。\\n立足智能化发展方向，基于最先进的仿生智能技术，为用户打造符合个性需求的智能场景方案，或许就是海尔智家想要实现的未来。\\n三星：带来进阶节能体验\\n对三星电子这种国际大厂来说，IFA 2024确实是个不错的展示机会。\\n所以他们不仅包下了一整个展馆，还特地展出面向欧洲生活方式打造的全新节能家电系列——拥有A-55%额外能效的三星BespokeAI™洗衣机 、达到洗烘全程A级能效的Bespoke AI™洗烘一体机以及拥有A-10%能效的Bespoke洗碗机。\\n\\n（图源：三星）\\n没错，这次三星主打的是节能牌。\\n在这三款产品中，最夸张的就是三星Bespoke AI™洗衣机，借助全新的Bubble Shot技术，通过循环泵将洗涤剂和水抽出并喷洒到滚筒内的衣物上，这款产品的理论能耗要比欧洲A级能效等级的最低要求低55%，同时洗涤效果也获得了不错的提升。\\n不过该型号计划在明年发布，今年欧洲用户看来是用不上了。\\n还有全新的三星Bespoke AI Hybrid冰箱，其采用了压缩机和珀尔帖混合式制冷技术，可使冰箱在能耗超出日常使用量时做出智能调整进而实现节能，例如在冰箱门打开的时间较长时，能耗较低的珀尔帖制冷技术就能够作为额外的冷却源以提高整体能效。\\n从某种意义上来说，这或许也是一种「混动式」家电了吧。\\n\\n（图源：雷科技摄制）\\n按照官方的说法，三星在其产品中继续优先考虑能源效率，并致力于借助AI技术实现这一目标，比如在冰箱、洗衣机等电器中内置AI功能，或是利用AI功能释放其SmartThings生态系统的潜力，从而节省更多能源。\\n在不知不觉中，AI已经深入我们生活中的方方面面。\\n美的：体验AI ECO智慧节能\\n要说美的这次展出的重点是什么，那一定是首次展示的AI ECO智慧节能解决方案。\\n按照官方说法，该方案基于千亿级的设备运行数据库及通过云端连接获取的实况天气、电费等第三方数据，运用了搭载全新大数据预学习模型的AI节能算法，有效对环境、材质等各类条件进行智能分析、预测并综合智能决策与节能精控，使家电能耗平均大幅度降低30%。\\n\\n（图源：雷科技摄制）\\n以空调为例，随着户外环境温湿度的变化，传统空调即便设定在相同的温度，也难以维持用户感受上的恒温，人们的体感往往会因忽冷忽热而感到不适。尤其在夜晚，空调的持续运行有时可能导致室内温度过低，影响睡眠质量；与此同时，频繁反复的温度调节也会增加空调的耗电。\\n而搭载该方案的空调，就可以预判室内热负荷变化，并提前做出精准控温，实现能源使用效率的重大飞跃。\\n此外，美的展台中央还展示了支持美的AI ECO智慧节能解决方案的多款家电产品，包含冰箱、洗衣机、热水器等。\\n\\n（图源：雷科技摄制）\\n根据不同产品在使用过程中可能出现异常耗电的情况，美的采用全面定制化的AI ECO算法，就像是一个隐形的智能能源管家，为日常家庭生活中的多种场景提供全面的节能解决方案。\\n通过多元的绿色家电产品解决方案，美的展示出积极投身并引领行业的可持续发展理念与绿色转型决心。\\n这和目前能源紧缺的欧洲市场，确实是很搭的组合。\\n长虹：首发白电垂域大模型\\n要在大半年前，有人和你说以后冰洗产品也会用上AI，我想大多数人肯定不信。\\n但在IFA 2024展会上，长虹真的发布了行业首个白电垂域大模型——长虹美菱智汇家AI大模型。\\n\\n（图源：雷科技摄制）\\n根据官方介绍，长虹美菱智汇家AI大模型则拥有80亿级参数规模，能够嵌入到冰箱、洗衣机、烘护机和空调等家电中，使它们具备“思考”能力。\\n放在现实场景中，这一大模型能够理解用户需求，预见用户喜好，提供更加精准的服务。例如衣物材质与状态，为用户提供最佳的洗涤和烘护方案的AI净衣技术；根据食材特性，为用户提供最佳的保存环境，以及专属的健康食谱建议的AI鲜冻技术；以此来打造适合每名用户自己生活习惯的AI家电。\\n在我看来，此次长虹发布的AI大模型技术，将推动长虹在智能技术的深度探索，其不仅仅带来了技术的进步，也将在未来将进一步改变智能家居生态。\\nTCL：当AI与实用主义交融\\n既然来都来了，那肯定要去看一下TCL实业的展区。\\n该说不说，虽然TCL以其出色的电视产品闻名，但他们的空冰洗产品同样令人印象深刻。\\n先说我看到的这台TCL FreshIN 3.0 空调吧，这款采用了可升降式新鲜空气入口“FreshIN”的专利设计，可在新鲜空气进入房间时对用户进行通知，搭配上行业领先的TVOC 检测系统，让用户能够一目了然地监测空气质量，搭配上超省电的AI大数据模型算法，能够智能感知环境温度变化，精准调控运行频率，节能率高达40%。\\n\\n（图源：雷科技摄制）\\nTCL还展出了自家引以为傲的超薄平嵌系列冰箱，1mm的无缝式嵌入设计，可完美匹配传统600mm橱柜；冷藏室T-Fresh系统能在48小时内灭杀99.99%的细菌，延长食物保鲜期；第四代微孔发泡技术和真空绝缘材料的使用，让冰箱存储空间更大。\\n不难看出，在积极拥抱AI技术的同时，TCL对家电本身的核心功能与设计也很看重，力求为用户解决实际问题，带来更便捷的生活体验。\\n照目前势头发展下去，TCL白电业务正在迅速跻身头部阵营。\\n海信：加快场景化升级\\n在去年IFA展上，海信首次公布了未来的技术战略：以场景致未来。\\n在今年IFA展上，海信更进一步，启动实施场景化升级，从提供单一产品转变到提供场景解决方案，为白电产品提供了智能洗衣、智能厨房和智能空气护理三个主要场景。\\n海信Series 7i洗衣机系列通过远程监控和自动调整功能简化了衣物护理过程；海信智能大屏冰箱允许用户应用远程调节温度设置，并通过AI Eco功能一键激活节能模式；海信的Energy Pro X空调系列则提供实时监控室内空气质量，让用户远程根据需要进行调整。\\n\\n（图源：雷科技摄制）\\n这些产品不仅提升了家电的智能化水平，也为用户提供了更加直观和便捷的智能生活体验。\\n除了产品外，海信还展示了可再生材料、非石油基材料、咖啡渣材料在家电整机上应用的环保材料。\\n按照现场人员介绍，海信冰箱研发团队经过长期的技术攻关，开创生物基材料产品应用的行业先例，冰箱产品再生材料使用占比可达到40%以上，可回收利用率超过80%。\\n不难看出，海信正在构思着一个智慧、绿色、健康的未来生活空间。\\n要高端智能，更要绿色节能\\n不得不说，这股囊括了整个消费市场的AI之风，还真有种吹向白电市场的趋势。\\n美的运用了搭载大数据预学习模型的AI节能算法，打造出符合自身核心理念的AI ECO智慧节能解决方案；长虹则更具突破性一些，带来了行业首个白电垂域大模型——长虹美菱智汇家AI大模型，希望借此理解用户需求，预见用户喜好，提供更加精准的服务。\\n\\n（图源：雷科技摄制）\\n至于「All in AI」的三星，也在展会上推出了具备升级Bixby语音助手功能的Bespoke缤色铂格套系智能家电，升级后的Bixby可以理解用户对话中的多个指令，同时结合之前的情境执行连续指令，比如，用户可以通过语音指令启动洗衣机、调节空调温度或查询冰箱内的食物库存，并获得推荐更健康的食谱。\\n这些智能家电不仅提高了用户的生活质量，还展示了AI技术在家电领域的广泛应用前景。\\n不过在AI技术的表面下，其实各家厂商追求的还是更基础的实用主义。\\n就这么说吧，因为白电是更加贴近于日常生活的产品，你很难在白电上，看到类似于手机、电脑、电视上所强调的AIGC功能。\\n取而代之的，则是一系列比较明确的实用性功能，例如「借助AI识别面料智能匹配洗涤算法」或者是「借助AI识别当前场景控制空调出风」之类的，都是在产品的核心功能上做强化。\\n\\n（图源：雷科技摄制）\\n具体到卖点上，在类似于冰箱这样的产品上，薄嵌设计和保鲜技术显然更加受欢迎；放在洗衣机与烘干机上，解决的则是「如何才能把衣服彻底洗干净」这个问题；而在空调上，问题的关键就变成了是否省电、新风系统体验如何以及「能不能让我进入精致睡眠」。\\n有趣的是，在今年的展台里，出现了几乎每家厂商都在强调自身借助AI能力达到节能效果的场景。\\n\\n（图源：雷科技摄制）\\n而出现这种情况的深层原因，则是欧洲地区积年累月形成的能源危机问题。\\n近年来，突发的地缘政治事件，对整个欧洲能源市场产生了重大影响，曾经最大的天然气和石油供应国的断供，再加上由于白左抗议而导致维护和关闭的大批核电站，导致欧洲目前处于严重的能源危机中。\\n为了应对这一挑战，欧洲各国与欧盟采取了一系列措施，从2021年3月1日起，欧盟的能效标签等级有所调整，在旧能效等级标准下的A+++级产品，转换为新能效等级后基本在A级到C级区间，新能效等级划分显然更为严格。\\n但是在此基础上，海尔、美的、TCL、长虹等国内厂商均在IFA上推出了多款比欧洲A级能源标准更节能的产品。\\n这些节能家电不仅有助于降低能源消耗，还能帮助消费者节省电费，符合欧洲市场对可持续发展的需求，最重要的是向世界展示了中国在节能领域的卓越成就，「绿色节能」或将成为国产家电引领海外市场的又一大关键。\\n说在最后\\n在IFA 2024上，我看到了白色家电市场的最新趋势，AI技术的应用、实用主义的回归以及对节能环保的重视，俨然成为未来全球市场的主要发展方向。\\n在我看来，作为国内企业接触欧洲市场的第一站，IFA不仅是展示新产品和技术的机会，更是深入了解欧洲消费者需求和市场动态的关键渠道。\\n\\n（图源：雷科技摄制）\\n随着中国品牌在全球影响力的提升，越来越多的企业向世界展现出强大的创新力，凸显了中国品牌在全球市场中的引领地位，进一步提升了国际市场对中国品牌的认知与信赖。\\n如果说IFA的百年历程，是中国品牌走向世界、影响世界的生动写照。\\n那么在下一个百年，希望国内企业能够继续在全球科技浪潮中扮演重要角色，推动技术进步和市场发展，持续创新产品和技术应用，为全球消费者带来更多高品质的产品与服务，为更多全球用户打造美好生活。\\n责任编辑：");

        contents.add("北京时间9月6日16:00，作为下半年仅有的消费电子展会，柏林国际电子消费品展览会（IFA2024）在德国柏林会展中心正式开幕，为期5天（9月6日-10日）。\\n为了及时给大家带来下半年科技产业的最新动态，雷科技报道团已飞赴德国·柏林，发掘各家厂商的最新动向。\\n在IFA展会100年的历史中，经历过无数次的革新，也推动了许多关键性技术的普及，但其核心主题一直未曾改变，那就是家电。德系家电在家电行业一直是与中系、日系并列的存在，其中不乏西门子、博世、嘉格纳等著名品牌。如今随着展会规模的不断扩大，IFA已成为全球家电品牌的绝佳展示平台。\\n今年除了TCL带来MiniLED大屏方案外，海信、长虹、三星、海尔等品牌也展示了各自的最新技术和电视产品，小雷这几天在柏林已暴走4万步，现在就跟我一起来看看这次IFA2024有哪些电视技术与产品展示吧。\\n重磅新品扎堆，电视巨头狂秀肌肉\\n1、长虹：死磕AI发布首款“智能体AITV”\\n在众多电视品牌中，长虹无疑是最突出AI概念的那位，不仅带来了最新的全屋AI家电，还向大伙展示了长虹全球首款沧海智能体AITV。\\n据了解，全新沧海智能体AITV能交流、能思考、会成长，相比起“云帆”大模型，它的技术和功能更加强大。例如，长虹通过自研自适应唤醒技术，引入多通道算法，让语音唤醒、语音识别更准确，沟通起来就像和家庭成员在聊天一般，同时，沧海智能体更善于思考，且能自我学习成长。\\n图源：雷科技现场摄制\\n不仅如此，长虹在本次展会执行“ALLINAI”战略，将人工智能技术深度融入多款OLED、QD-MiniLED电视产品中。比如一款在AI加持下的115英寸UMaxAITV，画质、影像、全景声等方面均得到显著提升，配合上UMAX超画质引擎，让用户时刻感受到AI科技带来的声画双重享受以及全方位的沉浸式观影体验。\\n换言之，智能体+AI产品的组合让全新一代的CHiQ产品，成为行业首款真正意义上的智能体AITV。\\n2、TCL：大屏、画质两手抓\\n作为MiniLED技术的推动者，TCL这次带来了号称最强万级分区的QD-MiniLED电视X11H，以及全球最大的115英寸QD-MiniLED电视X955Max。\\n图源：雷科技现场摄制\\n展会现场，这两款产品备受瞩目，雷科技等了许久才找到合适的拍照角度。虽说这些产品我们在其他展会见过了，但并不妨碍它们依旧是出色的好产品。\\n其中QD-MiniLED电视拥有万级背光分区，X11H搭载TCL华星HVAA++蝶翼星曜屏，配合高达6500nits的峰值亮度，让画面的明暗层次与细腻细节得到提升，通过搭载全域光晕控制技术，可在MiniLED成像的全链路上实现精准调控，有效解决行业光晕难题。\\n此外，163英寸的MicroLED巨幕电视X11HMax也是TCL展区的明星产品之一。今年3月，这款产品在国内正式发布，但无论看多少遍，我依旧感到震撼。X11HMax拥有10000nits的XDR亮度，内置超过2488万颗无机自发光芯片，且拥有22bit+色深，响应速度号称达到纳秒级，整机硬件水平堪称超顶配。\\n图源：雷科技现场摄制\\n3、海信：面向场景做更好的大屏\\n基于芯、屏、光三大核心技术，面向场景做产品深度优化，是海信电视的核心打法。\\n海信电视作为《黑神话：悟空》的全球合作伙伴，直接将无数玩家梦想中的电竞场景搬到了现场。数名电竞选手使用海信100英寸《黑神话：悟空》定制电视E8N系列畅玩游戏，现场显示效果就是最好的宣传。\\n图源：雷科技现场摄制\\n据了解，E8N系列，在芯片、屏幕、音响上都有独家核心技术，拥有“百吋+信芯AI画质芯片+黑曜屏+MiniLED”的超强组合，在大屏MiniLED领域有很不错的竞争力。\\n除了游戏场景，家庭影院也是海信主推的电视场景之一。升降卷曲激光电视是行业首台菲涅尔卷曲隐藏式电视，卷曲屏幕环境光遮敝率高达90%。用户可一键实现屏幕高精准度升降或隐藏，高清高亮画面跟随屏幕升降，可以让家庭观影更具仪式感。主机与屏幕采用模块化分离设计，可通过自由组合搬动，使客厅/卧室随时随地变身为电影院。\\n图源：雷科技现场摄制\\n说到显示技术，那就不得不提8K屏幕发声激光电视了。该产品拥有8K画质，精控3000万个像素点。同时搭载屏幕发声技术，10万级发声单元让整个屏幕都能发声，声音无衰减不失真，色彩和护眼方面的表现也相当不错。\\n4、三星：多屏齐聚持续AllForAI\\n在IFA展会上，三星直接搞了一个三星馆，牌面直接拉满。据雷科技观察，MiniLED、OLED、MicroLED等不同显示技术的电视产品均有展示，特别是那块MicroLED超级大屏，更是吸睛无数。\\n图源：雷科技现场摄制\\n其中，三星NeoQLED8KAI电视内置NQ8AIGen3处理器，拥有512个神经元网络（相较上一代提升8倍）。为了带给用户高品质音效与视觉画面的个性化定制体验，该技术在AI加持下可提升视觉显示效果和听觉体验，带给用户高品质音效与视觉画面。\\n图源：雷科技现场摄制\\n从今年开始，新款三星AI电视以及部分2023年款产品可享有Tizen操作系统升级服务，以增强所有三星设备之间的互联体验，而持续扩展的SmartThings生态系统是关键的核心要素。\\n图源：雷科技现场摄制\\n目前SmartThings生态系统已经连接了全球5亿多台三星设备，能够为三星旗下所有支持AI功能的产品提供无缝远程操控体验，用户可实时操控管理所有家电。例如，用户可远程浏览三星电视内容。\\n看来三星是要将“ALLFORAI”贯彻到底了。\\n电视走向何方？AI、大屏、场景与显示技术\\n雷科技认为，在这批IFA首日展出的电视产品里，有四个趋势还是非常明显的。\\n1、AI，AI，还是AI！\\n在宣传层面，TCL、海信等品牌尽管都将AI融入到产品技术中，但在展会现场并没有特别强调自己的产品是AITV。与之相反的是，三星、长虹把AI放在了更显眼的位置，两家都表示要ALLINAI。\\n图源：雷科技现场摄制\\n从技术角度来看，四个品牌的电视产品其实都已经融入了AI，例如AI对硬件的调校，对画面和声音的优化，还有运用生成式AI的艺术电视等等，这些AI功能正在变得越来越寻常。\\n目前行业对AITV还没有一个明确的标准，如果你问我，我认为是不是AITV并没有那么重要，关键是带给用户实际提升的AI技术，就像能海信针对游戏场景大模型算法那样。\\n2、比大更大，屏幕从Plus到MAX！\\n163英寸、136英寸、115英寸、100英寸......\\n在本次IFA2024上，几乎每家品牌都有展出大屏电视产品。回看近些年国内市场逐渐增大的电视尺寸，其实行业早已有共识：大屏化是电视行业确定的增长趋势。\\n洛图科技(RUNTO)的零售数据分析显示，今年618期间，电视销量整体下降约30%，但大屏电视则表现出了非常惊人的爆发力，85寸及以上尺寸的电视产品表现相对亮眼，特别是100寸电视在618电商零售活动中销量同比增长达到惊人的60%。\\n图源：雷科技现场摄制\\n其他数据方面，电视的平均尺寸比去年增加了9寸，达到69寸。而在超大尺寸段，即85寸以上的市场份额同比显著增长，表现远胜于65寸及75寸的电视。\\n雷科技认为大屏化趋势适用于全球市场，电视行业的大尺寸化进程或许会领先于其它方向的增速。\\n3、从游戏到体育再到户外，面向场景深度优化。\\n海信相关工作人员向雷科技介绍，场景化是目前电视发展的重大趋势。\\n与《黑神话：悟空》联名的电视E8N系列围绕游戏这一场景，与游戏科学开展了深度合作，就这一游戏而言，市面上或许没有任何一家品牌能在画面上超过海信。\\n同样的经验可以放到任何一款游戏身上，如果某个电视品牌能与市面大多数主流达成合作，那么他必将成为玩家们的首选。当然背后付出的成本也是巨大的，但场景化的魅力还远不止于此。\\n图源：雷科技现场摄制\\n在过去，人们对电视的印象应该只存在于客厅或房间，但随着模组化设计的普及，电视也可以和投影仪一样，出现在家中任何一个地方。例如主机与屏幕采取模块化分离设计的海信升降卷曲激光电视，可以自由行走的TCL第三代艺术电视。\\n4、“*LED”多线进化，显示技术百花齐放\\nULED、QLED、MiniLED、OLED、MicroLED是本届IFA电视产品的5大主流显示技术，说是五大，其实严格来说是三大，因为ULED和QLED主要是海信和三星在用。\\n而在MiniLED、OLED、MicroLED三种显示技术之间，虽然品牌都有布局，但战略具有明显差异。TCL、海信、长虹、创维等国产品牌更倾向于MiniLED，三星倾向于OLED，而MicroLED则是大家拿来“秀肌肉”的香饽饽。\\n前段时间，MiniLED电视凭借低成本、高对比度、高亮度等优势，成功在2024年第二季度的高端电视中超过OLED电视，押注MiniLED技术的国产品牌们也尝到了甜头，TCL实现了对三星的超越，登顶MiniLED电视全球出货量第一；海信在MiniLED产品线的助理下收获了17%的高端电视市场份额。\\n图源：雷科技现场摄制\\n从中长期来看，MiniLED电视具备的巨大市场潜力毋庸置疑。另一边，OLED阵营也在不断地提升效能，通过串联架构、Oxide背板等技术革新，让显示方案日趋完善。\\n比如三星正通过扩大OLED产品线来巩固其在高端电视市场的地位，继去年推出83英寸机型之后，三星最近又推出了采用LGDisplayWOLED面板的42英寸和48英寸OLED电视。\\n目前我们很难评判两种显示技术，因为它们是完全不同的技术路线，最终结果得让市场下结论。\\nIFA展会内容确实有点过于丰富了，雷科技暴走了几天，只看到冰山一角，光是电视产品就让人看得眼花缭乱，其实只用一天根本看不够、看不完。\\n这对消费者来说是好事，因为创新意味着选择，选择越多，我们就能从中挑选体验最佳的产品。就像MicroLED那样，目前还没有量产产品，即便量产了，价格肯定也贵的离谱，但谁知道未来会不会像LED电视一样走进寻常百姓家呢？\\n带给人们希望，这或许正是科技的魅力所在。\\nIFA2024将从当地时间6日持续到10日，敬请继续与雷科技一起在柏林发现科技带来的更多惊喜~");

        return contents.stream().map(content -> {
            return SubmitDocClusterTaskRequest.Documents.builder().content(content).build();
        }).collect(Collectors.toList());
    }
}
```

## 自定义话题聚合

> 给定一批内容，或者一个热点事件，针对这个事件从热门视角、网友观点、时效性、新颖性角度进行

> 分析，并生成选题策划。

```
package org.example.miaoce;

import com.alibaba.fastjson2.JSONObject;
import com.aliyun.aimiaobi20230801.Client;
import com.aliyun.aimiaobi20230801.models.*;
import com.aliyun.teaopenapi.models.Config;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.util.concurrent.ExecutionException;

@Slf4j
public class MiaoCeSubmitTopicSelectionPerspectiveAnalysisTaskTest {

    public static Client createClient() throws Exception {
        //accessKeyId
        String accessKeyId = System.getenv("accessKeyId");

        //accessKeySecret
        String accessKeySecret = System.getenv("accessKeySecret");

        //域名:aimiaobi.cn-hangzhou.aliyuncs.com
        String endpoint = System.getenv("domain");
        if (endpoint == null || endpoint.isEmpty()) {
            endpoint = "aimiaobi.cn-hangzhou.aliyuncs.com";
        }

        Config config = new Config()
                .setAccessKeyId(accessKeyId)
                .setAccessKeySecret(accessKeySecret)
                .setEndpoint(endpoint);
        return new Client(config);
    }

    /**
     * 选题视角分析
     */
    @Test
    public void testSubmitTopicSelectionPerspectiveAnalysisTask() throws Exception {
        String agentKey = System.getenv("AgentKey");

        //构建请求Client
        Client client = createClient();

        SubmitTopicSelectionPerspectiveAnalysisTaskRequest request = new SubmitTopicSelectionPerspectiveAnalysisTaskRequest()
                .setAgentKey(agentKey)
                .setTopic("杭州亚运会");

        //流式提交 自定
        SubmitTopicSelectionPerspectiveAnalysisTaskResponse taskResponse = client.submitTopicSelectionPerspectiveAnalysisTask(request);

        if (taskResponse.getStatusCode() != 200) {
            log.error("提交热点选题视角分析任务失败，response：{}", JSONObject.toJSONString(taskResponse));
            return;
        }

        log.info("提交热点选题视角分析任务成功，任务ID为：{}", taskResponse.getBody().getData().getTaskId());

        //轮询任务ID
        GetTopicSelectionPerspectiveAnalysisTaskRequest queryRequest = GetTopicSelectionPerspectiveAnalysisTaskRequest.builder()
                .agentKey(agentKey)
                .taskId(taskResponse.getBody().getData().getTaskId()).build();

        //每秒钟轮询结果
        GetTopicSelectionPerspectiveAnalysisTaskResponse queryResponse;
        while (true) {
            queryResponse = client.getTopicSelectionPerspectiveAnalysisTask(queryRequest);

            log.info("queryResponse:{}", JSONObject.toJSONString(queryResponse));
            //任务状态为RUNNING或者PENDING时，等待1秒钟
            if ("RUNNING".equals(queryResponse.getBody().getData().getStatus()) || "PENDING".equals(queryResponse.getBody().getData().getStatus())) {
                Thread.sleep(1000);
            } else {
                break;
            }
        }
        if (queryResponse.getStatusCode() == 200 && queryResponse.getBody().getSuccess() && queryResponse.getBody().getData().getStatus().equals("SUCCESSED")) {
            GetTopicSelectionPerspectiveAnalysisTaskResponseBody.Data data = queryResponse.getBody().getData();

            log.info("获取热点选题视角分析任务成功，任务结果为：{}", JSONObject.toJSONString(data));

            log.info("主题事件:{},", data.getTopic());

            //热点摘要
            for (GetTopicSelectionPerspectiveAnalysisTaskResponseBody.Summaries summary : data.getTopicSummaryResult().getSummaries()) {
                System.out.printf("标题：%s%n", summary.getTitle());
                System.out.printf("摘要：%s%n", summary.getSummary());
                System.out.printf("摘要引用新闻来源：%n");
                for (GetTopicSelectionPerspectiveAnalysisTaskResponseBody.DocList source : summary.getDocList()) {
                    System.out.printf("\t新闻标题：%s%n", source.getTitle());
                    System.out.printf("\t新闻来源：%s%n", source.getSource());
                    System.out.printf("\t新闻链接：%s%n%n", source.getUrl());
                }
            }

            log.info("热点摘要分析：{}", JSONObject.toJSONString(data.getTopicSummaryResult()));

            //热门选题视角列表
            for (GetTopicSelectionPerspectiveAnalysisTaskResponseBody.HotViewPointsResultAttitudes attitude : data.getHotViewPointsResult().getAttitudes()) {
                System.out.printf("热门观点：【%s%n", attitude.getAttitude());
                System.out.printf("观点占比：%s%n", attitude.getRatio());
                System.out.printf("热门选题视角列表：%n");
                for (GetTopicSelectionPerspectiveAnalysisTaskResponseBody.AttitudesViewPoints viewPoint : attitude.getViewPoints()) {
                    System.out.printf("\t视角名称：%s%n", viewPoint.getPoint());
                    System.out.printf("\t视角摘要：%s%n", viewPoint.getSummary());
                    System.out.printf("\t选题策划：%n");
                    for (GetTopicSelectionPerspectiveAnalysisTaskResponseBody.ViewPointsOutlines outline : viewPoint.getOutlines()) {
                        System.out.printf("\t\t大纲：%s%n", outline.getOutline());
                        System.out.printf("\t\t摘要：%s%n%n", outline.getSummary());
                    }
                }
                System.out.println();
            }

            //网友选题视角分析
            for (GetTopicSelectionPerspectiveAnalysisTaskResponseBody.WebReviewPointsResultAttitudes attitude : data.getWebReviewPointsResult().getAttitudes()) {
                System.out.printf("网友观点：【%s%n", attitude.getAttitude());
                System.out.printf("观点占比：%s%n", attitude.getRatio());
                System.out.printf("网友观点视角列表：%n");
                for (GetTopicSelectionPerspectiveAnalysisTaskResponseBody.WebReviewPointsResultAttitudesViewPoints viewPoint : attitude.getViewPoints()) {
                    System.out.printf("\t视角名称：%s%n", viewPoint.getPoint());
                    System.out.printf("\t视角摘要：%s%n", viewPoint.getSummary());
                    System.out.printf("\t选题策划：%n");
                    for (GetTopicSelectionPerspectiveAnalysisTaskResponseBody.WebReviewPointsResultAttitudesViewPointsOutlines outline : viewPoint.getOutlines()) {
                        System.out.printf("\t\t大纲：%s%n", outline.getOutline());
                        System.out.printf("\t\t摘要：%s%n%n", outline.getSummary());
                    }
                }
                System.out.println();
            }

            //时效性选题视角分析
            for (GetTopicSelectionPerspectiveAnalysisTaskResponseBody.TimedViewPointsResultAttitudes attitude : data.getTimedViewPointsResult().getAttitudes()) {
                System.out.printf("时效性观点：【%s%n", attitude.getAttitude());
                System.out.printf("新闻源：%s【%s】", attitude.getUrl(), attitude.getSource());
                System.out.printf("时效性观点视角列表：%n");
                for (GetTopicSelectionPerspectiveAnalysisTaskResponseBody.TimedViewPointsResultAttitudesViewPoints viewPoint : attitude.getViewPoints()) {
                    System.out.printf("\t视角名称：%s%n", viewPoint.getPoint());
                    System.out.printf("\t视角摘要：%s%n", viewPoint.getSummary());
                    System.out.printf("\t选题策划：%n");
                    for (GetTopicSelectionPerspectiveAnalysisTaskResponseBody.AttitudesViewPointsOutlines outline : viewPoint.getOutlines()) {
                        System.out.printf("\t\t大纲：%s%n", outline.getOutline());
                        System.out.printf("\t\t摘要：%s%n%n", outline.getSummary());
                    }
                }
                System.out.println();
            }

            //新颖视角默认只有一个观点
            for (GetTopicSelectionPerspectiveAnalysisTaskResponseBody.Attitudes attitude : data.getFreshViewPointsResult().getAttitudes()) {
                System.out.printf("新颖观点：【%s%n", attitude.getAttitude());
                System.out.printf("新颖视角列表：%n");
                for (GetTopicSelectionPerspectiveAnalysisTaskResponseBody.ViewPoints viewPoint : attitude.getViewPoints()) {
                    System.out.printf("\t视角名称：%s%n", viewPoint.getPoint());
                    System.out.printf("\t视角摘要：%s%n", viewPoint.getSummary());
                    System.out.printf("\t选题策划：%n");
                    for (GetTopicSelectionPerspectiveAnalysisTaskResponseBody.Outlines outline : viewPoint.getOutlines()) {
                        System.out.printf("\t\t大纲：%s%n", outline.getOutline());
                        System.out.printf("\t\t摘要：%s%n%n", outline.getSummary());
                    }
                }
                System.out.println();
            }
        } else {
            log.error("获取热点选题视角分析任务失败，response：{}", JSONObject.toJSONString(queryResponse));
        }

    }

}
```

## 自定义视角分析

> 给定一批内容，或者一个热点事件，按照用户指定的视角进行热点分析并生成选题策划的大纲。

```
package org.example.miaoce;

import com.alibaba.fastjson2.JSONObject;
import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.AsyncClient;
import com.aliyun.sdk.service.aimiaobi20230801.models.*;
import darabonba.core.client.ClientOverrideConfiguration;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

@Slf4j
public class MiaoCeSubmitCustomTopicSelectionPerspectiveAnalysisTaskTest {

    public static AsyncClient asyncClient() {

        //accessKeyId
        String accessKeyId = System.getenv("accessKeyId");

        //accessKeySecret
        String accessKeySecret = System.getenv("accessKeySecret");

        //域名:aimiaobi.cn-hangzhou.aliyuncs.com
        String domain = System.getenv("domain");

        return AsyncClient.builder().credentialsProvider(StaticCredentialProvider.create(Credential.builder()
                .accessKeyId(accessKeyId).accessKeySecret(accessKeySecret).build())).serviceConfiguration(Configuration.create().setSignatureVersion(SignatureVersion.V3)).overrideConfiguration(ClientOverrideConfiguration.create().setProtocol("HTTPS")
                .setEndpointOverride(domain)).build();
    }

    /**
     * 选题视角分析
     */
    @Test
    public void testSubmitCustomTopicSelectionPerspectiveAnalysisTask() throws ExecutionException, InterruptedException, IOException {
        String agentKey = System.getenv("AgentKey");

        //构建请求Client
        AsyncClient asyncClient = asyncClient();

        SubmitCustomTopicSelectionPerspectiveAnalysisTaskRequest request = SubmitCustomTopicSelectionPerspectiveAnalysisTaskRequest.builder().agentKey(agentKey)
                .prompt("请从 经济影响方面分析  杭州亚运会 对 杭州的影响").build();

        //流式提交 自定
        SubmitCustomTopicSelectionPerspectiveAnalysisTaskResponse taskResponse = asyncClient.submitCustomTopicSelectionPerspectiveAnalysisTask(request).get();

        if (taskResponse.getStatusCode() != 200) {
            log.error("提交自定义热点选题视角分析任务失败，response：{}", JSONObject.toJSONString(taskResponse));
            return;
        }

        log.info("提交自定义热点选题视角分析任务成功，任务ID为：{}", taskResponse.getBody().getData().getTaskId());

        //轮询任务ID
        GetCustomTopicSelectionPerspectiveAnalysisTaskRequest queryRequest = GetCustomTopicSelectionPerspectiveAnalysisTaskRequest.builder()
                .agentKey(agentKey)
                .taskId(taskResponse.getBody().getData().getTaskId()).build();

        //每秒钟轮询结果
        GetCustomTopicSelectionPerspectiveAnalysisTaskResponse queryResponse;
        while (true) {
            CompletableFuture<GetCustomTopicSelectionPerspectiveAnalysisTaskResponse> getTaskResponse = asyncClient.getCustomTopicSelectionPerspectiveAnalysisTask(queryRequest);
            queryResponse = getTaskResponse.get();

            log.info("queryResponse:{}", JSONObject.toJSONString(queryResponse));

            //任务状态为RUNNING或者PENDING时，等待1秒钟
            if ("RUNNING".equals(queryResponse.getBody().getData().getStatus()) || "PENDING".equals(queryResponse.getBody().getData().getStatus())) {
                Thread.sleep(1000);
            } else {
                break;
            }
        }
        if (queryResponse.getStatusCode() == 200 && queryResponse.getBody().getSuccess() && queryResponse.getBody().getData().getStatus().equals("SUCCESSED")) {
            GetCustomTopicSelectionPerspectiveAnalysisTaskResponseBody.Data data = queryResponse.getBody().getData();

            //自定义结果
            GetCustomTopicSelectionPerspectiveAnalysisTaskResponseBody.CustomViewPointsResult viewPointsResult = data.getCustomViewPointsResult();

            log.info("主题事件:{},", viewPointsResult.getTopic());

            //自定义观点列表
            for (GetCustomTopicSelectionPerspectiveAnalysisTaskResponseBody.Attitudes attitude : data.getCustomViewPointsResult().getAttitudes()) {
                System.out.printf("自定义观点：%s%n", attitude.getAttitude());
                System.out.printf("自定义视角列表：%n");
                for (GetCustomTopicSelectionPerspectiveAnalysisTaskResponseBody.ViewPoints viewPoint : attitude.getViewPoints()) {
                    System.out.printf("\t视角名称：%s%n", viewPoint.getPoint());
                    System.out.printf("\t视角摘要：%s%n", viewPoint.getSummary());
                    System.out.printf("\t选题策划：%n");
                    for (GetCustomTopicSelectionPerspectiveAnalysisTaskResponseBody.Outlines outline : viewPoint.getOutlines()) {
                        System.out.printf("\t\t大纲：%s%n", outline.getOutline());
                        System.out.printf("\t\t摘要：%s%n%n", outline.getSummary());
                    }
                }
                System.out.println();
            }
        } else {
            log.error("获取自定义热点选题视角分析任务失败，response：{}", JSONObject.toJSONString(queryResponse));
        }

    }

}
```

## SASS页面查询类接口

涉及接口：[ListHotSources - 获取三方热榜源列表](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listhotsources)、[ListHotTopics - 获取热点话题列表](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listhottopics)、[ListHotViewPoints - 获取热门视角列表](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listhotviewpoints)、[ListWebReviewPoints - 获取网友视角列表](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listwebreviewpoints)、[ListFreshViewPoints - 获取新颖视角列表](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listfreshviewpoints)、[ListTimedViewAttitude - 获取时效性视角列表](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-listtimedviewattitude)。

```
package org.example.miaoce;

import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.AsyncClient;
import com.aliyun.sdk.service.aimiaobi20230801.models.*;
import darabonba.core.client.ClientOverrideConfiguration;
import lombok.extern.slf4j.Slf4j;
import org.jetbrains.annotations.NotNull;
import org.junit.jupiter.api.Test;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.stream.Collectors;

@Slf4j
public class MiaoCePortalQueryDemoTest {

    public static AsyncClient asyncClient() {

        //accessKeyId
        String accessKeyId = System.getenv("accessKeyId");

        //accessKeySecret
        String accessKeySecret = System.getenv("accessKeySecret");

        //域名:aimiaobi.cn-hangzhou.aliyuncs.com
        String domain = System.getenv("domain");

        return AsyncClient.builder().credentialsProvider(StaticCredentialProvider.create(Credential.builder()
                .accessKeyId(accessKeyId).accessKeySecret(accessKeySecret).build())).serviceConfiguration(Configuration.create().setSignatureVersion(SignatureVersion.V3)).overrideConfiguration(ClientOverrideConfiguration.create().setProtocol("HTTPS")
                .setEndpointOverride(domain)).build();
    }

    /**
     * SASS页面 妙策 查询类接口 DEMO
     */
    @Test
    public void testPortalApiDemo() throws ExecutionException, InterruptedException {

        AsyncClient asyncClient = asyncClient();

        String agentKey = System.getenv("AgentKey");

        CompletableFuture<ListHotSourcesResponse> hotSources = asyncClient.listHotSources(ListHotSourcesRequest.builder().agentKey(agentKey).build());

        ListHotSourcesResponse response = hotSources.get();

        //获取所有的三方源
        for (ListHotSourcesResponseBody.Data datum : response.getBody().getData()) {
            log.info("三方源名称：{}", datum.getSource());
        }

        ListHotSourcesResponseBody.Data source = response.getBody().getData().get(0);

        //取第一个三方源的数据
        ListHotTopicsResponse listHotTopics =
                asyncClient.listHotTopics(ListHotTopicsRequest.builder().agentKey(agentKey)
                        .topicSource(source.getSource()).build()).get();

        //获取该热点源下所有的热点
        for (ListHotTopicsResponseBody.Data datum : listHotTopics.getBody().getData()) {

            String summary = datum.getStructureSummary().stream().map(x -> {
                return String.format("【%s】%s", x.getTitle(), x.getSummary());
            }).collect(Collectors.joining("\n"));

            log.info("热点名称：{},摘要：{}", datum.getTopic(), summary);
        }

        //获取全国热点话题榜
        listHotTopics = listHotTopicResponseAggregation(asyncClient, agentKey);
        //获取某个话题的热门视角选题热点
        ListHotTopicsResponseBody.Data topicObj = listHotTopics.getBody().getData().get(0);

        String topic = topicObj.getTopic();
        String topicSource = topicObj.getTopicSource();

        //获取热门选题观点列表
        log.info("获取热门选题观点列表");
        listHotViewPoints(asyncClient, agentKey, topic, topicSource);

        //获取时效性选题视角列表
        log.info("获取时效性选题视角列表");
        listTimedAttitude(asyncClient, agentKey, topic, topicSource);

        //获取网友选题视角列表
        log.info("获取网友选题观点列表");
        listWebReviewPoints(asyncClient, agentKey, topicSource, topic);

        //新颖选题视角列表
        log.info("获取新颖选题视角列表");
        listFreshViewPoint(asyncClient, agentKey, topic, topicSource);
    }

    private static void listFreshViewPoint(AsyncClient asyncClient, String agentKey, String topic, String topicSource) throws InterruptedException, ExecutionException {
        ListFreshViewPointsResponse freshViewPointsResponse = asyncClient.listFreshViewPoints(
                ListFreshViewPointsRequest.builder().agentKey(agentKey).topic(topic).topicSource(topicSource).build()).get();

        for (ListFreshViewPointsResponseBody.Data item : freshViewPointsResponse.getBody().getData()) {
            System.out.printf("\t视角名称：%s%n", item.getPoint());
            System.out.printf("\t视角摘要：%s%n", item.getSummary());
            System.out.printf("\t选题策划：%n");
            for (ListFreshViewPointsResponseBody.Outlines outline : item.getOutlines()) {
                System.out.printf("\t\t大纲：%s%n", outline.getOutline());
                System.out.printf("\t\t摘要：%s%n%n", outline.getSummary());
            }
        }
    }

    private static void listWebReviewPoints(AsyncClient asyncClient, String agentKey, String topicSource, String topic) throws InterruptedException, ExecutionException {
        ListWebReviewPointsResponse webReviewPointsResponse = asyncClient.listWebReviewPoints(ListWebReviewPointsRequest.builder()
                .agentKey(agentKey).topicSource(topicSource).topic(topic).build()).get();

        //热门选题观点列表
        for (ListWebReviewPointsResponseBody.Data item : webReviewPointsResponse.getBody().getData()) {
            System.out.printf("网友观点：【%s%n", item.getAttitude());
            System.out.printf("观点占比：%s%n", item.getRatio());
            System.out.printf("网友观点视角列表：%n");
            for (ListWebReviewPointsResponseBody.ViewPoints viewPoint : item.getViewPoints()) {
                System.out.printf("\t视角名称：%s%n", viewPoint.getPoint());
                System.out.printf("\t视角摘要：%s%n", viewPoint.getSummary());
                System.out.printf("\t选题策划：%n");
                for (ListWebReviewPointsResponseBody.Outlines outline : viewPoint.getOutlines()) {
                    System.out.printf("\t\t大纲：%s%n", outline.getOutline());
                    System.out.printf("\t\t摘要：%s%n%n", outline.getSummary());
                }
            }
            System.out.println();
        }
    }

    private static void listTimedAttitude(AsyncClient asyncClient, String agentKey, String topic, String topicSource) throws InterruptedException, ExecutionException {
        ListTimedViewAttitudeResponse timedViewAttitudeResponse = asyncClient.listTimedViewAttitude(
                ListTimedViewAttitudeRequest.builder().agentKey(agentKey).topic(topic).topicSource(topicSource).build()).get();
        for (ListTimedViewAttitudeResponseBody.Data item : timedViewAttitudeResponse.getBody().getData()) {
            System.out.printf("新闻标题：%s%n", item.getAttitude());
            System.out.printf("新闻源：%s【%s】%n", item.getUrl(), item.getSource());
            System.out.printf("时效性视角列表：%n");
            for (ListTimedViewAttitudeResponseBody.ViewPoints viewPoint : item.getViewPoints()) {
                System.out.printf("\t视角名称：%s%n", viewPoint.getPoint());
                System.out.printf("\t视角摘要：%s%n", viewPoint.getSummary());
                System.out.printf("\t选题策划：%n");
                for (ListTimedViewAttitudeResponseBody.Outlines outline : viewPoint.getOutlines()) {
                    System.out.printf("\t\t大纲：%s%n", outline.getOutline());
                    System.out.printf("\t\t摘要：%s%n%n", outline.getSummary());
                }
            }
            System.out.println();
        }
    }

    private static void listHotViewPoints(AsyncClient asyncClient, String agentKey, String topic, String topicSource) throws InterruptedException, ExecutionException {
        ListHotViewPointsResponse hotViewPointsResponse = asyncClient.listHotViewPoints(ListHotViewPointsRequest.builder().agentKey(
                agentKey).topic(topic).topicSource(topicSource).build()).get();
        //热门选题观点列表
        for (ListHotViewPointsResponseBody.Data item : hotViewPointsResponse.getBody().getData()) {
            System.out.printf("热门观点：【%s%n", item.getAttitude());
            System.out.printf("观点占比：%s%n", item.getRatio());
            System.out.printf("热门选题视角列表：%n");
            for (ListHotViewPointsResponseBody.ViewPoints viewPoint : item.getViewPoints()) {
                System.out.printf("\t视角名称：%s%n", viewPoint.getPoint());
                System.out.printf("\t视角摘要：%s%n", viewPoint.getSummary());
                System.out.printf("\t选题策划：%n");
                for (ListHotViewPointsResponseBody.Outlines outline : viewPoint.getOutlines()) {
                    System.out.printf("\t\t大纲：%s%n", outline.getOutline());
                    System.out.printf("\t\t摘要：%s%n%n", outline.getSummary());
                }
            }
            System.out.println();
        }
    }

    private static @NotNull ListHotTopicsResponse listHotTopicResponseAggregation(AsyncClient asyncClient, String agentKey) throws InterruptedException, ExecutionException {
        ListHotTopicsResponse listHotTopics;
        listHotTopics =
                asyncClient.listHotTopics(ListHotTopicsRequest.builder().agentKey(agentKey)
                        .topicSource("Aggregation").build()).get();
        //获取该热点源下所有的热点
        for (ListHotTopicsResponseBody.Data datum : listHotTopics.getBody().getData()) {
            String summary = datum.getStructureSummary().stream().map(x -> {
                return String.format("【%s】%s", x.getTitle(), x.getSummary());
            }).collect(Collectors.joining("\n"));
            log.info("全国热点名称：{},摘要：{}", datum.getTopic(), summary);
        }
        return listHotTopics;
    }

}
```

## **自定义数据源**

> 请参照以下demo示例进行调用。

**说明**

-   调用自定义数据源的前提：请点击[全妙智能检索生成应用后付费API](https://common-buy.aliyun.com/?commodityCode=sfm_quanmiaoAPI_public_cn)进行开通。
    
-   自定义数据源的计费说明：自定义数据源是按照token消耗计费，妙策其他接口即购买妙笔和妙策公有云预付费版本即可调用，自定义数据源计费详见：《[计费说明（妙策-自定义数据源）](https://help.aliyun.com/zh/model-studio/billing-document-miaoce-custom-data-source)》。
    

```
package org.example.miaoce;

import com.alibaba.fastjson2.JSONObject;
import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.AsyncClient;
import com.aliyun.sdk.service.aimiaobi20230801.models.*;
import darabonba.core.client.ClientOverrideConfiguration;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

/**
 * * 前置依赖
 * * <dependency>
 * * <groupId>com.aliyun</groupId>
 * * <artifactId>alibabacloud-aimiaobi20230801</artifactId>
 * * <version>取最新版本，详见：https://api.aliyun.com/api-tools/sdk/AiMiaoBi?version=2023-08-01&language=java-async-tea&tab=primer-doc</version>
 * * </dependency>
 * *
 * * <dependency>
 * * <groupId>org.projectlombok</groupId>
 * * <artifactId>lombok</artifactId>
 * * <version>1.18.30</version>
 * * </dependency>
 * *
 * * <dependency>
 * * <groupId>com.alibaba.fastjson2</groupId>
 * * <artifactId>fastjson2</artifactId>
 * * <version>2.0.21</version>
 * * </dependency>
 * * <dependency>
 * * <groupId>org.junit.jupiter</groupId>
 * * <artifactId>junit-jupiter</artifactId>
 * * <version>5.8.1</version>
 * * </dependency>
 * <p>
 *
 * 参考API文档：
 *      https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-dir-tips-custom-data-source/?spm=a2c4g.11186623.help-menu-2400256.d_1_7_4_2_0_3_9.411d7544s0dRMp
 */
@Slf4j
public class SubmitCustomSourceTopicAnalysisTest {
    private static String accessKeyId = System.getenv("accessKeyId");

    private static String accessKeySecret = System.getenv("accessKeySecret");

    private static String workspaceId = System.getenv("WorkspaceId");

    private static String agentKey = System.getenv("AgentKey");

    private static String endpoint = "aimiaobi.cn-beijing.aliyuncs.com";

    public static AsyncClient asyncClient() {
        return AsyncClient.builder().credentialsProvider(
                StaticCredentialProvider.create(Credential.builder().accessKeyId(accessKeyId).accessKeySecret(accessKeySecret).build())
        ).serviceConfiguration(Configuration.create().setSignatureVersion(SignatureVersion.V3)).overrideConfiguration(
                ClientOverrideConfiguration.create().setProtocol("HTTPS").setEndpointOverride(endpoint)
        ).build();
    }

    @Test
    public void testSubmitCustomSourceTopicAnalysis() throws InterruptedException, IOException, ExecutionException {

        AsyncClient asyncClient = asyncClient();

        String fileUrl = "https://aimiaobi-service-prod.oss-cn-beijing.aliyuncs.com/temp/input_news_list_20.json";

        SubmitCustomSourceTopicAnalysisRequest.Builder builder = SubmitCustomSourceTopicAnalysisRequest.builder().workspaceId(workspaceId);

        //文件URL以及文件对应的格式。支持 json（json数组、每个item为一篇新闻对象json） jsonLine格式（每行为一篇新闻对象json）。数据结构同news字段
        builder.fileType("json").fileUrl(fileUrl);

        //同样支持直接传对象列表
        //builder.news(Arrays.asList(SubmitCustomSourceTopicAnalysisRequest.News.builder().url("<url>").title("<标题>").content("<正文>").build()));

        //最大分析的话题数量
        builder.maxTopicSize(2);

        CompletableFuture<SubmitCustomSourceTopicAnalysisResponse> submitFuture = asyncClient.submitCustomSourceTopicAnalysis(builder.build());

        SubmitCustomSourceTopicAnalysisResponse response = submitFuture.get();

        //异步任务ID
        String taskId = response.getBody().getData().getTaskId();

        while (true) {
            CompletableFuture<GetCustomSourceTopicAnalysisTaskResponse> taskFuture = asyncClient.getCustomSourceTopicAnalysisTask(GetCustomSourceTopicAnalysisTaskRequest.builder().workspaceId(workspaceId).taskId(taskId).build());
            GetCustomSourceTopicAnalysisTaskResponseBody body = taskFuture.get().getBody();
            if (!body.getSuccess()) {
                System.out.printf("查询任务失败，错误码：%s，错误信息：%s\n", body.getCode(), body.getMessage());
                return;
            }

            //只有 PENDING、RUNNING才轮询
            GetCustomSourceTopicAnalysisTaskResponseBody.Data data = body.getData();

            System.out.printf("解析新闻的数量：%d，聚类后的新闻数量：%d，最大聚类文档数量：%d\n", data.getParsedNewsSize(), data.getClusterCount(), data.getMaxClusteredTopicNewsSize());

            if (data.getStatus().equals("PENDING") || data.getStatus().equals("RUNNING")) {
                System.out.printf("任务执行中，TaskId:%s,TaskStatus:%s\n", taskId, data.getStatus());
                Thread.sleep(1000);
                continue;
            }

            if (!data.getStatus().equals("SUCCESSED")) {
                System.out.printf("任务执行失败，错误信息：%s\n", data.getErrorMessage());
                break;
            }
            System.out.printf("Response:%s\n", JSONObject.toJSONString(data));

            List<GetCustomSourceTopicAnalysisTaskResponseBody.ClusterResults> clusterResults = data.getClusterResults();

            System.out.println("新闻聚合结果：" + JSONObject.toJSONString(clusterResults));

            System.out.println("消耗时间（毫秒）：" + data.getRt());

            System.out.println("token消耗情况：" + JSONObject.toJSONString(data.getUsages()));

            //查询明细列表
            //doListDetails(taskId, asyncClient);

            //导出全量文件
            exportFullResults(taskId, asyncClient);
            break;
        }
    }

    private static void exportFullResults(String taskId, AsyncClient asyncClient) throws InterruptedException, ExecutionException, IOException {
        ExportCustomSourceAnalysisTaskRequest.Builder exportBuilder = ExportCustomSourceAnalysisTaskRequest.builder();
        exportBuilder.workspaceId(workspaceId);
        exportBuilder.taskId(taskId);
        CompletableFuture<ExportCustomSourceAnalysisTaskResponse> responseFuture = asyncClient.exportCustomSourceAnalysisTask(exportBuilder.build());
        //下载URL为文件
        String url = responseFuture.get().getBody().getData();
        //下载文件
        String s = downResultFile(url);
        System.out.println(s);
    }

    private static String downResultFile(String url) throws IOException {
        URL url1 = new URL(url);
        HttpURLConnection urlConnection = (HttpURLConnection) url1.openConnection();
        // 设置请求方法
        urlConnection.setRequestMethod("GET");
        String fileName = null;
        String contentDisposition = urlConnection.getHeaderField("Content-Disposition");
        if (contentDisposition != null && contentDisposition.contains("filename=")) {
            int startIndex = contentDisposition.indexOf("filename=") + 9;
            int endIndex = contentDisposition.indexOf(";", startIndex);
            if (endIndex == -1) {
                endIndex = contentDisposition.length();
            }
            String extractedFileName = contentDisposition.substring(startIndex, endIndex).replace("\"", "");
            if (!extractedFileName.isEmpty()) {
                fileName = extractedFileName;
            }
        }

        // 创建临时目录
        String tmpDir = System.getProperty("java.io.tmpdir");
        java.io.File tempDir = new java.io.File(tmpDir);
        if (!tempDir.exists()) {
            tempDir.mkdirs();
        }

        if (fileName == null) {
            //random uuid
            fileName = UUID.randomUUID().toString();
        }

        // 在临时目录中创建文件
        java.io.File outputFile = new java.io.File(tempDir, fileName);

        // 获取输入流
        try (java.io.InputStream inputStream = urlConnection.getInputStream();
             java.io.FileOutputStream outputStream = new java.io.FileOutputStream(outputFile)) {
            byte[] buffer = new byte[4096];
            int bytesRead;

            // 读取数据并写入文件
            while ((bytesRead = inputStream.read(buffer)) != -1) {
                outputStream.write(buffer, 0, bytesRead);
            }

            String absolutePath = outputFile.getAbsolutePath();
            System.out.println("文件已成功下载到临时目录: " + absolutePath);
            return absolutePath;
        } catch (IOException e) {
            System.err.println("下载文件时发生错误: " + e.getMessage());
        }
        return null;
    }

    private static void doListDetails(String taskId, AsyncClient asyncClient) throws InterruptedException, ExecutionException {
        //获取话题分析详情。taskId传版本号。Custom表示自定义数据源。 取top10的数据
        ListHotTopicsRequest.Builder queryBuilder = ListHotTopicsRequest.builder();
        //历史原因需要填写 agentKey
        queryBuilder.agentKey(agentKey);
        queryBuilder.topicSource("Custom");
        queryBuilder.topicVersion(taskId);
        queryBuilder.maxResults(10);
        //获取所有聚合话题
        ListHotTopicsResponse listHotTopics = asyncClient.listHotTopics(queryBuilder.build()).get();
        List<ListHotTopicsResponseBody.Data> data = listHotTopics.getBody().getData();
        for (ListHotTopicsResponseBody.Data datum : data) {
            String topic = datum.getTopic();
            //话题摘要
            List<ListHotTopicsResponseBody.StructureSummary> structureSummary = datum.getStructureSummary();
            System.out.printf("聚合话题：%s，话题摘要：%s", topic, JSONObject.toJSONString(structureSummary));
        }
        //查询第一个的话题选题详情
        ListHotTopicsResponseBody.Data data1 = data.get(0);
        String topic = data1.getTopic();
        queryTopicSelectionDetail(asyncClient, topic);
    }

    /**
     * 话题选题详情
     */
    private static void queryTopicSelectionDetail(AsyncClient asyncClient, String topic) throws InterruptedException, ExecutionException {
        String topicSource = "Custom";
        //获取热门选题观点列表
        log.info("获取热门选题观点列表");
        listHotViewPoints(asyncClient, agentKey, topic, topicSource);

        //获取时效性选题视角列表
        log.info("获取时效性选题视角列表");
        listTimedAttitude(asyncClient, agentKey, topic, topicSource);

        //获取网友选题视角列表
        log.info("获取网友选题观点列表");
        listWebReviewPoints(asyncClient, agentKey, topicSource, topic);

        //新颖选题视角列表
        log.info("获取新颖选题视角列表");
        listFreshViewPoint(asyncClient, agentKey, topic, topicSource);
    }

    private static void listFreshViewPoint(AsyncClient asyncClient, String agentKey, String topic, String topicSource) throws InterruptedException, ExecutionException {
        ListFreshViewPointsResponse freshViewPointsResponse = asyncClient.listFreshViewPoints(
                ListFreshViewPointsRequest.builder().agentKey(agentKey).topic(topic).topicSource(topicSource).build()).get();

        for (ListFreshViewPointsResponseBody.Data item : freshViewPointsResponse.getBody().getData()) {
            System.out.printf("\t视角名称：%s%n", item.getPoint());
            System.out.printf("\t视角摘要：%s%n", item.getSummary());
            System.out.printf("\t选题策划：%n");
            for (ListFreshViewPointsResponseBody.Outlines outline : item.getOutlines()) {
                System.out.printf("\t\t大纲：%s%n", outline.getOutline());
                System.out.printf("\t\t摘要：%s%n%n", outline.getSummary());
            }
        }
    }

    private static void listWebReviewPoints(AsyncClient asyncClient, String agentKey, String topicSource, String topic) throws InterruptedException, ExecutionException {
        ListWebReviewPointsResponse webReviewPointsResponse = asyncClient.listWebReviewPoints(ListWebReviewPointsRequest.builder()
                .agentKey(agentKey).topicSource(topicSource).topic(topic).build()).get();

        //热门选题观点列表
        for (ListWebReviewPointsResponseBody.Data item : webReviewPointsResponse.getBody().getData()) {
            System.out.printf("网友观点：【%s%n", item.getAttitude());
            System.out.printf("观点占比：%s%n", item.getRatio());
            System.out.printf("网友观点视角列表：%n");
            for (ListWebReviewPointsResponseBody.ViewPoints viewPoint : item.getViewPoints()) {
                System.out.printf("\t视角名称：%s%n", viewPoint.getPoint());
                System.out.printf("\t视角摘要：%s%n", viewPoint.getSummary());
                System.out.printf("\t选题策划：%n");
                for (ListWebReviewPointsResponseBody.Outlines outline : viewPoint.getOutlines()) {
                    System.out.printf("\t\t大纲：%s%n", outline.getOutline());
                    System.out.printf("\t\t摘要：%s%n%n", outline.getSummary());
                }
            }
            System.out.println();
        }
    }

    private static void listTimedAttitude(AsyncClient asyncClient, String agentKey, String topic, String topicSource) throws InterruptedException, ExecutionException {
        ListTimedViewAttitudeResponse timedViewAttitudeResponse = asyncClient.listTimedViewAttitude(
                ListTimedViewAttitudeRequest.builder().agentKey(agentKey).topic(topic).topicSource(topicSource).build()).get();
        for (ListTimedViewAttitudeResponseBody.Data item : timedViewAttitudeResponse.getBody().getData()) {
            System.out.printf("新闻标题：%s%n", item.getAttitude());
            System.out.printf("新闻源：%s【%s】%n", item.getUrl(), item.getSource());
            System.out.printf("时效性视角列表：%n");
            for (ListTimedViewAttitudeResponseBody.ViewPoints viewPoint : item.getViewPoints()) {
                System.out.printf("\t视角名称：%s%n", viewPoint.getPoint());
                System.out.printf("\t视角摘要：%s%n", viewPoint.getSummary());
                System.out.printf("\t选题策划：%n");
                for (ListTimedViewAttitudeResponseBody.Outlines outline : viewPoint.getOutlines()) {
                    System.out.printf("\t\t大纲：%s%n", outline.getOutline());
                    System.out.printf("\t\t摘要：%s%n%n", outline.getSummary());
                }
            }
            System.out.println();
        }
    }

    private static void listHotViewPoints(AsyncClient asyncClient, String agentKey, String topic, String topicSource) throws InterruptedException, ExecutionException {
        ListHotViewPointsResponse hotViewPointsResponse = asyncClient.listHotViewPoints(ListHotViewPointsRequest.builder().agentKey(
                agentKey).topic(topic).topicSource(topicSource).build()).get();
        //热门选题观点列表
        for (ListHotViewPointsResponseBody.Data item : hotViewPointsResponse.getBody().getData()) {
            System.out.printf("热门观点：【%s%n", item.getAttitude());
            System.out.printf("观点占比：%s%n", item.getRatio());
            System.out.printf("热门选题视角列表：%n");
            for (ListHotViewPointsResponseBody.ViewPoints viewPoint : item.getViewPoints()) {
                System.out.printf("\t视角名称：%s%n", viewPoint.getPoint());
                System.out.printf("\t视角摘要：%s%n", viewPoint.getSummary());
                System.out.printf("\t选题策划：%n");
                for (ListHotViewPointsResponseBody.Outlines outline : viewPoint.getOutlines()) {
                    System.out.printf("\t\t大纲：%s%n", outline.getOutline());
                    System.out.printf("\t\t摘要：%s%n%n", outline.getSummary());
                }
            }
            System.out.println();
        }
    }

}
```
