# 说明

执行:  

``` python
python statistics.py [可选]
可选项中有：  
--coop_pass 获取 [team_name]_cooperation&pass_count.txt

--pass_ori_dst_pm 获取 [team_name]_pass_dest.txt [team_name]_pass_origin.txt

--attrc_force_item_pm 获取 [team_name]_attractive_force_item.txt

--coordinate_per_op 获取 [team_name]_coordinate_origin_dest_avg.txt
```

获得 result 路径下的文件，目前可获得的文件有：  

+ [team_name]cooperation&pass_count.txt 用来存储，整队的合作和传球情况。  
+ [team_name]Husk_pass_dest.txt 存储 Husky 队伍队员的接球情况。
+ [team_name]_Husk_pass_origin.txt 存储 Husky 队伍队员的传球情况。  
+ [team_name]_attractive_force_item.txt 存储计算球员吸引力系数的各参数。
+ [team_name]_coordinate_origin_dest_avg.txt 存储球员传接球平均坐标。
