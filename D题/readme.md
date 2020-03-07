# 说明

## 传球事件分析

执行:  

``` python
python pass_event_analyse.py [可选]
可选项中有：  
--cp 获取 cooperation&pass_count.txt

--pass_memberwise 获取 pass_dest.txt pass_origin.txt

--attractive 获取 attractive_force_item.txt

--coordinate 获取 coordinate_origin_dest_avg.txt
```

获得 build/[team_name]/result 路径下的文件，目前可获得的文件有：  

+ cooperation&pass_count.txt 用来存储，整队的合作和传球情况。  
+ pass_dest.txt 存储 Husky 队伍队员的接球情况。
+ pass_origin.txt 存储 Husky 队伍队员的传球情况。  
+ attractive_force_item.txt 存储计算球员吸引力系数的各参数。
+ coordinate_origin_dest_avg.txt 存储球员传接球平均坐标。


## 绘图

修改你要检索的队伍，例如 "Opponent1_" 这里加 '_' 的原因是因为可能会与 "Opponent11" 重叠，这是个很恶心的问题。   

绘图的时候顺便会计算：结点吸引力，质心坐标，离散程度，加权平均路径，聚类系数，二元聚类系数，  
存储文件都放置在 build/[team_name]/result，其中离散程度、加权平均路径，聚类系数，二元聚类系数放置在  
 S_and_path_avg_c_ff_index.txt 文件，而结点吸引力放置在 Matchwise_attrct_cal.txt ,质心坐标放置在  
 Matchwise_weight_point.txt 文件中。

执行以下命令生成所有文件：

``` python
python all.py
```