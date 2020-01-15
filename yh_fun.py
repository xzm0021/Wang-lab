# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:35:29 2019

@author: Y.H. Zhou

Contact: yihangjoe@foxmail.com
         https://github.com/Y-H-Joe/

####============================ discription ==============================####
yihang's functions.
usage:
    import yh_fun as yh
=================================== input =====================================

=================================== output ====================================

================================= parameters ==================================

=================================== example =================================== 

=================================== warning ===================================

####=======================================================================####
"""
##== return value is iterator, use list() for vision ==##
def list_duplicates(seq):
    from collections import defaultdict
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items() 
                            if len(locs)>1)

def read_table(input_table,sep="",skiprows=None,header=None,index_col=None,nrows=None):
    import pandas as pd
    if len(sep)==0:
        if input_table.strip().split(".")[-1]=="csv":
            sep=","
            return(pd.read_csv(input_table,sep=sep,skiprows=skiprows,header=header,index_col=index_col,nrows=nrows))
        elif input_table.strip().split(".")[-1]=="tsv":
            sep="\t"
            return(pd.read_csv(input_table,sep=sep,skiprows=skiprows,header=header,index_col=index_col,nrows=nrows))
        elif input_table.strip().split(".")[-1]=="xls":
            return(pd.read_excel(input_table,skiprows=skiprows,header=header,index_col=index_col,nrows=nrows))
        else:
            print(input_table.strip().split(".")[-1]," is unknown format. Use , to seperate by default.")
    else:
        return(pd.read_csv(input_table,sep=sep,skiprows=skiprows,header=header,index_col=index_col,nrows=nrows))


##== according to lookup value, filter search_area and output part of search_area ==##
def VLOOKUP(lookup_value_dir='',search_area_dir='',l_col=1,s_col=1,output_name='',output_index=None,output_header=True,output_sep='\t',concat=False):
    import pandas as pd   
    import traceback
    ## input table
    lookup_value=read_table(lookup_value_dir,header=0)
    search_area=read_table(search_area_dir,header=0)
    
    ## start from 0
    ## tell which column is for index
    l_col=l_col
    s_col=s_col
    
    lookup_value_list=list(pd.Series(lookup_value.loc[:,lookup_value.columns[l_col]]).dropna())
    lookup_value.index=list(lookup_value.loc[:,lookup_value.columns[l_col]])
    search_area.index=search_area.loc[:,search_area.columns[s_col]]
    
    if concat==False:
        output=search_area.loc[lookup_value_list,:]
        output.to_csv(output_name,index=output_index,header=output_header,sep=output_sep)
    else:
        try:
            lookup_value_dropna=lookup_value.loc[lookup_value_list,:]
            lookup_value_dropna.index=lookup_value_list
        except Exception as e:
            traceback.print_exc()
            print(e)
            print("Check whether duplicates in lookup_value.")
        search_area_concated=pd.concat([search_area,lookup_value_dropna],axis=1,join_axes=[search_area.index])
        search_area_concated.to_csv(output_name,index=output_index,header=output_header,sep=output_sep)
        
## VLOOKUP(lookup_value_dir='D:/CurrentProjects/Cattle_WGS/cattle_transtable_ucsc.unique.tsv',search_area_dir='D:/CurrentProjects/Cattle_WGS/cattle_transtable_ensembl.unique.tsv',l_col=12,s_col=11,output_name='D:/CurrentProjects/Cattle_WGS/cattle_genetable_ensembl_ucsc.tsv',concat=True)




