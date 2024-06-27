import os
import grp

group_ids = os.getgroups()
group_names = [grp.getgrgid(gid).gr_name for gid in group_ids]

print(group_names)