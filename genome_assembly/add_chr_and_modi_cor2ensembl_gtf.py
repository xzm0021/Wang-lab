# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 17:21:44 2019

@author: Y.H. Zhou

Contact: yihangjoe@foxmail.com
         https://github.com/Y-H-Joe/

####============================ discription ==============================####
add addin (set as "chr" as default), and replace names containing special key
to special value.
if change_gtf_coordinates_via_agp==1, then do as it says
=================================== input =====================================

=================================== output ====================================

================================= parameters ==================================
dp="catequ.1.gtf"
output_gtf="catequ.2.new.gtf"

addin="chr"
gtf_sep='\t'
#if some row begin with(containing) these markers, then we specially modify them
#into special values
#the position must be 1vs1
special_key_value=[["MT","chrM"],["NKLS","chrUn"]] 

#if need to change gtf coordinates via agp coordinates
#explanation:
#PJAA1001 locates 10001-10010 in ensembl_gtf, but locates 501-510 in self-format
#apg file, which means there're 500 nts ahead of PJAA101, so we need to change
#10001-10010 to 10501-10510
#in math, we add agp_start_minus_one to gtf_coordinates
change_gtf_coordinates_via_agp=1
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

original ensembl gtf:
PJAA01004199.1	ensembl	exon	21	788	.	-	.	gene_id "ENSECAG00000041954"; g\
ene_version "1"; transcript_id "ENSECAT00000072187"; transcript_version "1"; ex\
on_number "2"; gene_source "ensembl"; gene_biotype "lncRNA"; transcript_source "\
ensembl"; transcript_biotype "lncRNA"; exon_id "ENSECAE00000334958"; exon_vers\
ion "1";
=================================== warning ===================================
directly read whole gtf file, will demand at least 1G memory.
####=======================================================================####
"""
import pandas as pd
import csv 

dp="Bos_taurus.ARS-UCD1.2.98.gtf"
output_gtf="Bos_taurus.ARS-UCD1.2.98.chr.cor.unchecked.gtf"

change_gtf_coordinates_via_agp=True
input_agp="bosTau9_chrUn.agp"

addin="chr"
gtf_sep='\t'
#if some row begin with(containing) these markers, then we specially modify them
#into special values
#the position must be 1vs1
special_key_value=[["MT","chrM"],["NKLS","chrUn"]] 

#if need to change gtf coordinates via agp coordinates
#explanation:
#PJAA1001 locates 10001-10010 in ensembl_gtf, but locates 501-510 in self-format
#apg file, which means there're 500 nts ahead of PJAA101, so we need to change
#10001-10010 to 10501-10510
#in math, we add agp_start_minus_one to gtf_coordinates
if change_gtf_coordinates_via_agp:
    input_agp=input_agp
    #in final agp version, the PJAAxxx is the 7th column
    agp_df=pd.read_csv(input_agp,sep='\t',index_col=6,header=None)

gtf_new=[]

print("Loading ",dp,"...")
with open(dp,'r') as f:
    lines=f.readlines()
    for line in lines:
        if "#!" in line: ##get rid of #!genome-build EquCab3.0
            gtf_new.append([line.strip()])
        else:
            line_list=line.strip().split("\t")
            check_whether_some_key_hits=0
            for key_value in special_key_value:
                if key_value[0] in line_list[0]: #modify special key values
                
                    #print(key_value[0])    
                    print(line_list[0]," processed!")
                    #print([key_value[1]]+line_list[1:])
                    
                    #need to change coordinates
                    """
                    line_list:
                    ['PJAA01000649.1','ensembl','exon','146','1159','.','-'...]
                    """
                    if change_gtf_coordinates_via_agp:
                        try:
                            coordinate_difference=int(agp_df.loc[line_list[0]][1])-1
                            line_list[3]=str(int(line_list[3])+coordinate_difference)
                            line_list[4]=str(int(line_list[4])+coordinate_difference)
                            print(line_list[0]," success!")
                        except:
                            print(line_list[0]," not in the agp, skip.")
                    gtf_new.append([key_value[1]]+line_list[1:])
                    check_whether_some_key_hits=1
                    continue
                else:##modify normal chrs, like 1,2,3...
                    pass
            if check_whether_some_key_hits==0:
                gtf_new.append([str(addin+str(line_list[0]))]+line_list[1:])
            
gtf_df=pd.DataFrame(gtf_new)
# quoting=csv.QUOTE_NONE is for removing quotes
# https://stackoverflow.com/questions/21147058/pandas-to-csv-output-quoting-issue
gtf_df.to_csv(output_gtf,header=None,index=None,sep=gtf_sep,quoting=csv.QUOTE_NONE)


