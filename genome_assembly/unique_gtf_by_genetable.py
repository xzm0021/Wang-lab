# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 15:02:41 2019

@author: Y.H. Zhou

Contact: yihangjoe@foxmail.com
         https://github.com/Y-H-Joe/

####============================ discription ==============================####
given a gtf and an unique genetable, you can unique this gtf using the unique
gene id & trans id from genetable. You can also extract coding_unique gtf by
via gene futures annotated in gtf, like "protein_coding", etc.
=================================== input =====================================

=================================== output ====================================

================================= parameters ==================================
gtf="Equus_caballus.EquCab3.0.98.ensembl.chr.cor.unchecked.gtf"
gt="horse_genetable_coding.csv"

gtf_df=yh.read_table(gtf,sep="\t",skiprows=5)
gtf_df_head=yh.read_table(gtf,sep='\t',nrows=5)
gt_df=yh.read_table(gt,header=0)

##== unique_mark ==##
# Index(['gene_id', 'trans_id'], dtype='object')
gt_gene_id_col=0
gt_trans_id_col=1
gt_df.index=gt_df['gene_id']

##== unique gtf via matching gtf_features with gt_marks ==##
gtf_gene_id_col=1
gtf_trans_id_col=5

##== change dtype ==##
unique_gtf_df=pd.DataFrame(unique_gtf[5:])
dtype_col1=unique_gtf_df.columns[3]
dtype_col2=unique_gtf_df.columns[4]
unique_gtf_df.astype({dtype_col1:'int'})
unique_gtf_df.astype({dtype_col2:'int'})

##== output ==##
unique_gtf_df.to_csv("Equus_caballus.EquCab3.0.98.ensembl.chr.cor.unchecked.unique.gtf"
=================================== example =================================== 

=================================== warning ===================================

####=======================================================================####
"""
import yh_fun as yh
import pandas as pd
import sys
import csv

gtf="Equus_caballus.EquCab3.0.98.chr.cor.unchecked.gtf"
output_gtf="Equus_caballus.EquCab3.0.98.chr.cor.unchecked.unique.gtf"
gt="horse_genetable.csv"

gtf_df=yh.read_table(gtf,sep="\t",skiprows=5)
gtf_df_head=yh.read_table(gtf,sep='\t',nrows=5)
gt_df=yh.read_table(gt,header=0)

# whether to extract coding transcript out
coding=True

##== check gene table is unique ==##
print("##== check gene table is unique ==##")
if len(set(gt_df['gene_id'])) != gt_df.shape[0]:
    print("The gene table is not unique!")
    sys.exit()

##== unique_mark ==##
# Index(['gene_id', 'trans_id'], dtype='object')
gt_gene_id_col=0
gt_trans_id_col=1
gt_df.index=gt_df['gene_id']

##== prepare gtf features for further matching with genetable marks ==##
print("##== prepare gtf features for further matching with genetable marks ==##")
gtf_features=list(gtf_df.loc[:,gtf_df.columns[-1]])
gtf_features=[x.split() for x in gtf_features]
gtf_features1=[[y.strip(";").strip('\"') for y in x] for x in gtf_features]
gtf_features2=[]
for i in range(gtf_df.shape[0]):
    gtf_features2.append(gtf_features1[i]+[gtf_df.loc[i,gtf_df.columns[2]]])
#==============================================================================
# gtf_features1[0]
# ['gene_id',
#  'ENSECAG00000012421',
#  'gene_version',
#  '3',
#  'gene_name',
#  'SYCE1',
#  'gene_source',
#  'ensembl',
#  'gene_biotype',
#  'protein_coding']
#
# gtf_features2[0]
# ['gene_id',
#   'ENSECAG00000012421',
#   'gene_version',
#   '3',
#   'gene_name',
#   'SYCE1',
#   'gene_source',
#   'ensembl',
#   'gene_biotype',
#   'protein_coding',
#   'gene']
#==============================================================================


##== unique gtf via matching gtf_features with gt_marks ==##
print("##== unique gtf via matching gtf_features with gt_marks ==##")
gtf_gene_id_col=1
gtf_trans_id_col=5

unique_gtf=gtf_df_head.values.tolist()
for i in range(gtf_df.shape[0]):
    if gtf_features2[i][-1] == 'gene':
        if gtf_features2[i][gtf_gene_id_col] in gt_df.index:
            unique_gtf.append(list(gtf_df.loc[i]))
    elif (gtf_features2[i][gtf_gene_id_col] in gt_df.index) and \
    (gtf_features2[i][gtf_trans_id_col] == gt_df.loc[gtf_features2[i][gtf_gene_id_col]\
                   ,gt_df.columns[gt_trans_id_col]]):
        unique_gtf.append(list(gtf_df.loc[i]))

##== change dtype ==##
# unique_gtf_df=unique_gtf_df.loc[[dtype_col1,dtype_col2]].astype('int')
# the number are set to be float as default, the output will be like 111.0,
# we need to dtype it to int, to be 111
#==============================================================================
print("##== change dtype ==##")
unique_gtf_df=pd.DataFrame(unique_gtf[5:])
dtype_col1=unique_gtf_df.columns[3]
dtype_col2=unique_gtf_df.columns[4]
unique_gtf_df.astype({dtype_col1:'int'})
unique_gtf_df.astype({dtype_col2:'int'})

unique_gtf_df_head=pd.DataFrame(unique_gtf[:5])
#unique_gtf_df_whole=pd.concat([unique_gtf_df_head,unique_gtf_df])

#unique_gtf_df[[dtype_col1,dtype_col2]]=unique_gtf_df[[dtype_col1,dtype_col2]].astype('Int32')
#true_index=unique_gtf_df.index[unique_gtf_df[dtype_col1].notnull()]
#unique_gtf_df.loc[true_index, [dtype_col1,dtype_col2]] = unique_gtf_df.loc[true_index, [dtype_col1,dtype_col2]].astype('Int64')
unique_gtf_df_head=[x[0]+'\n' for x in unique_gtf[:5]]
unique_gtf_df_head_text="".join(unique_gtf_df_head)

unique_gtf_df.to_csv(output_gtf,index=None,sep='\t',header=None,quoting=csv.QUOTE_NONE)

##== output ==##
print("##== output ==##")
with open(output_gtf,'r+') as f:
    content=f.read()
    f.seek(0,0)
    f.write(unique_gtf_df_head_text+content)


