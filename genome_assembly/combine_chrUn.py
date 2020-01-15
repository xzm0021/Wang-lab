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
output_agp='chrY.agp'
output_fq='chrY_new.fa'
fq_width=50 #every 60 nts one line
dp="combine_chrY"
head="chrY"
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
import textwrap #for wrap text
import time

output_agp='chrY.agp'
output_fq='chrY_new.fa'
fq_width=50 #every 60 nts one line

##get each insterested file and their absolut datapath
def findfile(start, name,filenames):
    for relpath, dirs, files in os.walk(start):
        for file in files:
            if name in file:
                full_path = os.path.join(relpath, file)
                filenames.append(os.path.normpath(os.path.abspath(full_path)))

dp="combine_chrY"
filenames=[]
findfile(dp,"chrY",filenames)

#count time
time_start=time.time()

##parse input chrUn files
##to get the ID and length return in nesting list
##and add fragment to tail
##also, prepare combined chrUn
ID_and_length=[]
combined_chrUn=['>chrUn']
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
        
        combined_chrUn.append(line_others+"N"*1000)
        print(ID," success!")

##rm last N tail
del(ID_and_length[-1])
combined_chrUn_last=combined_chrUn[-1][:-1000]
del(combined_chrUn[-1])
combined_chrUn.append(combined_chrUn_last)


##format agp file
head="chrY"
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
#combined_chrUn: [['>chrUn'],['act..NNN']...]
#method1---too slow
"""
combined_chrUn_oneline="".join([x.strip() for x in combined_chrUn[1:]])
combined_chrUn_fq=str(combined_chrUn[0]+'\n'+textwrap.fill(combined_chrUn_oneline,width=fq_width))
with open(output_fq,'w') as f:
    f.write(combined_chrUn_fq)

"""
#method2
# reduce the complexity to linear
with open(output_fq,'w') as f:
    chrUn_wrap_without_tail=[]
    chrUn_wrap_tail=""
    f.write(combined_chrUn[0]) #separately process >chrUn
    f.write('\n')
    for chrUn in combined_chrUn[1:]:
        last_tail_and_this_chrUn=chrUn_wrap_tail+chrUn
        chrUn_wrap=textwrap.wrap(last_tail_and_this_chrUn,width=fq_width)
        if len(chrUn_wrap[-1])!=fq_width: #the last one, which is the tail
            chrUn_wrap_without_tail=chrUn_wrap[:-1]
            chrUn_wrap_tail=chrUn_wrap[-1]
        else:
            chrUn_wrap_without_tail=chrUn_wrap
            chrUn_wrap_tail=""      
        for line in chrUn_wrap_without_tail:
            f.write(line)
            f.write('\n')
    f.write(chrUn_wrap_tail)
    f.write('\n')
        
#remove last /n of output
#using wheel from stackoverflow
#https://stackoverflow.com/questions/18857352/python-remove-very-last-character-in-file      
def truncate_utf8_chars(filename, count, ignore_newlines=False):

    #Truncates last `count` characters of a text file encoded in UTF-8.
    #:param filename: The path to the text file to read
    #:param count: Number of UTF-8 characters to remove from the end of the file
    #:param ignore_newlines: Set to true, if the newline character at the end of the file should be ignored

    with open(filename, 'rb+') as f:
        last_char = None

        size = os.fstat(f.fileno()).st_size

        offset = 1
        chars = 0
        while offset <= size:
            f.seek(-offset, os.SEEK_END)
            b = ord(f.read(1))

            if ignore_newlines:
                if b == 0x0D or b == 0x0A:
                    offset += 1
                    continue

            if b & 0b10000000 == 0 or b & 0b11000000 == 0b11000000:
                # This is the first byte of a UTF8 character
                chars += 1
                if chars == count:
                    # When `count` number of characters have been found, move current position back
                    # with one byte (to include the byte just checked) and truncate the file
                    f.seek(-1, os.SEEK_CUR)
                    f.truncate()
                    return
            offset += 1        
    

#truncate_utf8_chars(output_fq,1)

print("time2 consumed: ",time.time()-time_start)
