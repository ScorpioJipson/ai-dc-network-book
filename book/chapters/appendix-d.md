---
title: 附录 D　术语中英对照表
appendix: D
word_count: 137
figures: 0
tables: 9
status: review
word_count_full: 1334
---
# 附录 D　术语中英对照表

> **用途**：术语首次出现给中英对照（写作规范第三节），本表汇总全书用词，便于查译与统一口径。
> 排序按主题分组，组内按中文拼音/英文首字母大致排布。

---

## D.1 GPU 与芯片级互联

| 中文 | 英文 / 缩写 | 简注 |
|---|---|---|
| 图形处理器 / 加速卡 | GPU（Graphics Processing Unit） | 本书"卡"= 一块 GPU；"节点"= 一台服务器，全文不混用 |
| 硬件互联 | NVLink | GPU 间高速互联；本书统一写 NVLink 4 / NVLink 5，不写 NVLink4 |
| 交换芯片 | NVSwitch | 机内全互联交换，构成 NVLink 域 |
| 互联域 | NVLink Domain | 8 卡 SXM 域内 900 GB/s 双向（H100 SXM） |
| 超节点 / 参考架构 | HGX / DGX SuperPOD | 整机与集群参考架构 |
| 加速器抽象层 | CUDA | |
| GPU 管理库 | DCGM（Data Center GPU Manager） | GPU 遥测与诊断 |

## D.2 拓扑与架构

| 中文 | 英文 / 缩写 | 简注 |
|---|---|---|
| 无阻塞 | Non-blocking | 1:1 收敛 |
| 收敛比 / 超配比 | Oversubscription Ratio | 下行带宽 : 上行带宽 |
| 两层 / 三层 CLOS | Two-tier / Three-tier CLOS | 胖树 |
| 脊 / 叶 | Spine / Leaf | 层级固定：服务器在下、Leaf 居中、Spine 在上 |
| 同轨组网 | Rail-optimized Topology | 第 k 号网卡固定接入第 k 轨 |
| 轨 | Rail | 由网卡序号唯一决定的逻辑分组 |
| 端点 | Endpoint | 一个网卡口 = 一个端点 |
| 五平面 | Five-plane Architecture | 算力 / 带外 / 带内 / 业务 / 存储 |
| 纯加法扩容 | Pure-additive Scaling | 新增 Leaf 只增邻居与链路，现网零改动 |

## D.3 网络协议与拥塞控制

| 中文 | 英文 / 缩写 | 简注 |
|---|---|---|
| 远程直接内存访问 | RDMA（Remote Direct Memory Access） | 绕过内核，零拷贝 |
| 基于融合以太网的 RDMA | RoCEv2（RDMA over Converged Ethernet v2） | 本书主线 |
| 无限带宽 | IB（InfiniBand） | 封闭生态，直连网卡（含 HCA 全称 Host Channel Adapter） |
| 无损网络 | Lossless Network | 靠 PFC 反压，不是靠"不丢包" |
| 优先级流控 | PFC（Priority Flow Control） | 逐跳反压；缓冲区余量见 headroom |
| 显式拥塞通知 | ECN（Explicit Congestion Notification） | 端到端标记，先于 PFC 触发 |
| 数据中心量化拥塞通知 | DCQCN（Data Center Quantized Congestion Notification） | ECN 的端侧算法 |
| 缓冲余量 | Headroom | 防止 PFC 反压到达前的在途报文被丢 |
| 死锁 / 风暴 | Deadlock / Storm | PFC 的两种失效模式 |
| 服务质量 | QoS（Quality of Service） | DSCP / 优先级映射 |
| 区分服务码点 | DSCP（Differentiated Services Code Point） | |
| 等价多路径 | ECMP（Equal-Cost Multi-Path） | multipath ≥ 16 |
| 双向转发检测 | BFD（Bidirectional Forwarding Detection） | 100 ms × 3 |
| 边界网关协议 | BGP（Border Gateway Protocol） | Underlay，逐链路 /31 |
| 自主系统号 | AS（Autonomous System） | Spine 65001；Leaf 每台独立 |
| 网内集合通信 | SHARP（Scalable Hierarchical Aggregation and Reduction Protocol） | IB 侧网内计算 |

## D.4 光模块与物理层

| 中文 | 英文 / 缩写 | 简注 |
|---|---|---|
| 可插拔模块封装 | OSFP / QSFP112 / QSFP-DD / QSFP28 / SFP28 / SFP+ | 服务器侧 OSFP、交换机侧 QSFP112（本案例） |
| 短距 / 单模并行 / 单模波分 / 长距 | SR / DR / FR / LR | 见附录 A |
| 四通道脉冲幅度调制 | PAM4 | 每符号 2 bit |
| 垂直腔面发射激光器 | VCSEL | 多模光源 |
| 电吸收调制激光器 / 直接调制激光器 | EML / DML | 单模光源 |
| 数字信号处理 | DSP | 模块内均衡 |
| 多芯连接器 | MPO / MTP | 12/16/24 芯 |
| 端面研磨 | PC / UPC / APC | 平面 / 超精平面 / 8° 斜面（见附录 A） |
| 极性 | Polarity Type A / B / C | 见附录 A |
| 光链路诊断 | OTDR / DDM | 插损定位 / 光功率监测 |
| 前向纠错 | FEC（Forward Error Correction） | `rx_uncorrectable = 0` 为硬判据 |
| 共封装光学 | CPO（Co-Packaged Optics） | 第 18 章 |

## D.5 服务器与主机

| 中文 | 英文 / 缩写 | 简注 |
|---|---|---|
| 高速外设互联总线 | PCIe（Peripheral Component Interconnect Express） | Gen4/5/6 |
| 非统一内存访问 | NUMA（Non-Uniform Memory Access） | GPU–NIC 亲和性 |
| 亲和性 | Affinity（PIX / PXB / PHB / NODE / SYS） | 见第 5 章 |
| 智能网卡 | SmartNIC / DPU | ConnectX-7 / ConnectX-6 Dx |
| 主机总线适配器 | HCA（Host Channel Adapter） | IB 侧网卡 |
| 单根 I/O 虚拟化 | SR-IOV | |

## D.6 存储

| 中文 | 英文 / 缩写 | 简注 |
|---|---|---|
| 网络附加存储协议 | NVMe-oF（NVMe over Fabrics） | 走 RoCEv2 |
| 并行文件系统 | Lustre / GPFS | OST / MDS 配比 |
| 全闪 / 混闪 | All-flash / Hybrid-flash | |
| 纠删码 | EC（Erasure Coding） | 本案例 EC 8+4 |
| 叠瓦式 / 传统磁记录 | SMR / CMR | 写放大差异 |
| 检查点 | Checkpoint | 全局同步落盘，瞬时冲击 |
| 对象存储 | Object Storage | 冷数据 |

## D.7 集合通信与调优

| 中文 | 英文 / 缩写 | 简注 |
|---|---|---|
| 集合通信库 | NCCL（NVIDIA Collective Communications Library） | 国产对应 HCCL |
| 全规约 / 全收集 / 规约散射 / 全交换 | AllReduce / AllGather / ReduceScatter / AllToAll | |
| 数据并行 / 张量并行 / 流水并行 / 专家并行 | DP / TP / PP / EP | |
| 算法带宽 / 总线带宽 | algbw / busbw | `busbw = algbw × 2(n−1)/n` |
| 通信与计算重叠 | Overlap | L0 / L1 / L2 分层 |
| 算力利用率 | MFU（Model FLOPs Utilization） | 调优的端到端判据 |
| 单跳 / 两跳 | Single-hop / Two-hop | 轨内跨 Leaf 需经 Spine **两跳** |

## D.8 运维、可观测与时间同步

| 中文 | 英文 / 缩写 | 简注 |
|---|---|---|
| 带内 / 带外管理 | In-band / Out-of-band Management | |
| 基板管理控制器 | BMC（Baseboard Management Controller） | |
| 智能平台管理接口 | IPMI（Intelligent Platform Management Interface） | |
| 网络管理协议 | SNMP / gNMI / Streaming Telemetry | 低频 / 高频 |
| 精确时间协议 | PTP（Precision Time Protocol, IEEE 1588v2） | 边界时钟 / 主时钟 |
| 网络时间协议 | NTP（Network Time Protocol） | |
| 亚健康 | Gray Failure | |
| 故障演练 | Chaos / Failure Drill | |

## D.9 商务与交付

| 中文 | 英文 / 缩写 | 简注 |
|---|---|---|
| 物料清单 | BOM（Bill of Materials） | 本案例最易漏项见第 16 章 |
| 概念验证 | POC（Proof of Concept） | |
| 资本性 / 运营性支出 | CAPEX / OPEX | 5 年模型 |
| 服务等级协议 | SLA（Service Level Agreement） | |
| 生命周期终止 | EOL / EOS（End of Life / End of Support） | 备件链风险 |
| 交付界面 | Interface / Scope Boundary | 逐条书面确认 |
