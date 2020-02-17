# 说明

## 传球事件分析

执行:  

``` python
python pass_event_analyse.py [可选]
可选项中有：  
--cp 获取 [team_name]_cooperation&pass_count.txt

--pass_memberwise 获取 [team_name]_pass_dest.txt [team_name]_pass_origin.txt

--attractive 获取 [team_name]_attractive_force_item.txt

--coordinate 获取 [team_name]_coordinate_origin_dest_avg.txt
```

获得 result 路径下的文件，目前可获得的文件有：  

+ [team_name]cooperation&pass_count.txt 用来存储，整队的合作和传球情况。  
+ [team_name]Husk_pass_dest.txt 存储 Husky 队伍队员的接球情况。
+ [team_name]_Husk_pass_origin.txt 存储 Husky 队伍队员的传球情况。  
+ [team_name]_attractive_force_item.txt 存储计算球员吸引力系数的各参数。
+ [team_name]_coordinate_origin_dest_avg.txt 存储球员传接球平均坐标。

## 绘图

修改你要检索的队伍，例如 "Opponent1_" 这里加 '_' 的原因是因为可能会与 "Opponent11" 重叠，这是个很恶心的问题。   

首先执行：  

``` python
python pass_event_analyse.py --cp --pass_memberwise --attractive --coordinate
python Matchwise_graph.py
```