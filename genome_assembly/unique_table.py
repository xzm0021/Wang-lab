# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 21:25:07 2019

@author: Y.H. Zhou

Contact: yihangjoe@foxmail.com
         https://github.com/Y-H-Joe/

####============================ discription ==============================####
given a table, unique it via sort columns, and get the largest (ascending=False)
or smallest (ascending = True) piece of repeat items.
=================================== input =====================================

=================================== output ====================================

================================= parameters ==================================
table_dir=r"D:\CurrentProjects\Equid\horse_transtable_ensembl.tsv"
output_dir="horse_transtable_ensembl.unique.tsv"

## here're the number 1st and number 12th columns that matter, and 1st is primary
## you can add more columns if you like
## but make sure the first col is the one that really repeative
## cause " if table_sorted_df.loc[index,sort_cols[0]) " the "0" here
sort_cols=[0,11]
ascending=(True,False)
=================================== example =================================== 

=================================== warning ===================================

####=======================================================================####
"""
import yh_fun as yh

table_dir=r"D:\CurrentProjects\Cattle_WGS\cattle_transtable_ensembl.tsv"
output_dir=r"D:\CurrentProjects\Cattle_WGS\cattle_transtable_ensembl.unique.tsv"

## here're the number 1st and number 12th columns that matter, and 1st is primary
## you can add more columns if you like
## but make sure the first col is the one that really repeative
## cause " if table_sorted_df.loc[index,sort_cols[0]) " the "0" here
sort_cols=[0,11]
ascending=(True,False)


table_df=yh.read_table(table_dir,header=0)
## sort table
real_sort_cols=list(table_df.columns[sort_cols])
table_sorted_df=table_df.sort_values(by=real_sort_cols,ascending=ascending)

## drop_duplicates
## not sure how the pandas drop_duplicates works, so just write my own
index_list=list(table_sorted_df.index)
index_filtered=[index_list[0]]
for index in index_list[1:]:
    if table_sorted_df.loc[index,real_sort_cols[0]]==table_sorted_df.loc[index_filtered[-1],real_sort_cols[0]]:
        pass
    else:
        index_filtered.append(index)

## output
table_sorted_unique_df=table_sorted_df.loc[index_filtered]
table_sorted_unique_df.to_csv(output_dir,sep='\t',index=None)
