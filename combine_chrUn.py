# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 09:41:13 2019

@author: Y.H. Zhou

Contact: yihangjoe@foxmail.com
         https://github.com/Y-H-Joe/

####============================ discription ==============================####
given the datapath of the folder containing chrUns, combine them together and
output agp file.
=================================== input =====================================

=================================== output ====================================

================================= parameters ==================================

=================================== example =================================== 
agp file:
    
chrUn	1	291010	1	W	chrUn_NW_019645229v1	1	291010	+
chrUn	291011	292010	2	N	fragment	1	1000	+
chrUn	292011	296614	3	W	chrUn_NW_019642425v1	1	4604	+

but we need to use excel to mannually link ensemble ID to the output agp file,
the final version looks:
    
chrUn	1	291010	1	W	chrUn_NW_019645229v1	PJAA01004061.1	1	291010	+
chrUn	291011	292010	2	N	fragment	fragment	1	1000	+
chrUn	292011	296614	3	W	chrUn_NW_019642425v1	PJAA01000297.1	1	4604	+

=================================== warning ===================================
this script is to use in linux, for windows, you may need to modify the way to 
get file name list.
####=======================================================================####
"""
import os
import pandas as pd

output_agp='equCab3_chrUn.agp'
output_fq='equCab3_chrUn.fa'

##get each insterested file and their absolut datapath
def findfile(start, name,filenames):
    for relpath, dirs, files in os.walk(start):
        for file in files:
            if name in file:
                full_path = os.path.join(relpath, file)
                filenames.append(os.path.normpath(os.path.abspath(full_path)))

dp="unknown"
filenames=[]
findfile(dp,"chrUn",filenames)

##parse input chrUn files
##to get the ID and length return in nesting list
##and add fragment to tail
##also, prepare combined chrUn
ID_and_length=[]
combined_chrUn=[['>chrUn']]
for file in filenames:
    with open(file,'r') as f:
        lines=f.readlines()
        ID=lines[0].strip()
        ##string join with strip
        line_others="".join([x.strip() for x in lines[1:]])
        length=int(len(line_others))
        ID_and_length.append([ID,length])
        ##add fragment
        ID_and_length.append(['fragment',1000])
        
        combined_chrUn.append([line_others+"N"*1000])
        print(ID," success!")

##rm last N tail
del(ID_and_length[-1])
combined_chrUn_last=combined_chrUn[-1][0][:-1000]
del(combined_chrUn[-1])
combined_chrUn.append([combined_chrUn_last])


##format agp file
head="chrUn"
start=1
end=0
index=0
index2=""
ID=""
unit_start=1
unit_end=0
index3="+"

agp_lines=[]

for ial in ID_and_length:
    
    end=end+ial[1] #end=end+length
    index=index+1
    index2=["N","W"][index%2] ##even odd
    ID=ial[0].strip(">")
    unit_end=ial[1]

    agp_line=[head,start,end,index,index2,ID,unit_start,unit_end,index3]
    
    start=start+ial[1]
    
    agp_lines.append(agp_line)
    
##output agp file
agp_df=pd.DataFrame(agp_lines)
agp_df.to_csv(output_agp,index=None,header=None,sep='\t')

##output combined chrUn
with open(output_fq,'w') as f:
    for chrUn in combined_chrUn:
        f.write(chrUn[0])
        f.write('\n')


