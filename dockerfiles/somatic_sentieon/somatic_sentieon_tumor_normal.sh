#!/bin/bash

# *******************************************
# Script to run somatic Sentieon (TNscope)
# on tumor / normal sample
# *******************************************

## Command line arguments
tumor_bam=$1
tumor_name=$2

normal_bam=$3
normal_name=$4

# reference data files
reference_fa=$5
dbsnp=$6
pon=$7

## Other settings
nt=$(nproc) #number of threads to use in computation, set to number of cores in the server

# ******************************************
# 1. Check readgroups
# ******************************************

# need to have unique readgroups for the tumor and somatic samples

samtools view -H $tumor_bam | grep "@RG" | awk '{print $2}' | awk 'BEGIN { FS = ":" } ; { print $2 }' > tumor_read_groups.txt
samtools view -H $normal_bam | grep "@RG" | awk '{print $2}' | awk 'BEGIN { FS = ":" } ; { print $2 }' > normal_read_groups.txt

#possible that read groups match between tumor and normal, and for TNscope they need to be unique. in the case that they do match (then statement) we replace everything with something generic ()
if [ $(grep -f tumor_read_groups.txt normal_read_groups.txt | wc -l) -gt 0 ]
then
  declare -i n=0; for i in $(cat tumor_read_groups.txt); do n+=1; tumor_replace+=" --replace_rg ${i}=ID:T_${n}\tSM:TUMOR\tPL:PLATFORM"; done
  declare -i n=0; for i in $(cat normal_read_groups.txt); do n+=1; normal_replace+=" --replace_rg ${i}=ID:N_${n}\tSM:NORMAL\tPL:PLATFORM"; done
  command="sentieon driver -t ${nt} -r ${reference_fa} ${tumor_replace} -i ${tumor_bam} ${normal_replace} -i ${normal_bam} --algo TNscope --tumor_sample TUMOR --normal_sample NORMAL --dbsnp ${dbsnp} --pon ${pon} output.vcf"
  echo $command
  $command
else
  command="sentieon driver -t ${nt} -r ${reference_fa} -i ${tumor_bam} -i ${normal_bam} --algo TNscope --tumor_sample ${tumor_name} --normal_sample ${normal_name} --dbsnp ${dbsnp} --pon ${pon} output.vcf"
  echo $command
  $command
fi




# ******************************************
# 2. Run TNscope
# ******************************************

sentieon driver -t $nt -r $reference_fa -i $tumor_bam --algo TNscope --tumor_sample $tumor_name output.vcf || exit 1

sentieon driver -t 16 -r ../GAPFIXRDPDK5.fa --replace_rg A00169_41_H2WM5DMXX_2='ID:T_1\tSM:TUMOR\tPL:PLATFORM' -i ../GAPFI2USVS21.bam --replace_rg A00169_41_H2WM5DMXX_2='ID:N\tSM:NORMAL\tPL:PLATFORM' -i ../GAPFI14IJOX2.bam --algo TNscope --tumor_sample TUMOR --normal_sample NORMAL --dbsnp ../GAPFI4LJRN98.vcf.gz --pon panel_of_normals.vcf.gz test_tumor_normal_with_panel.vcf

# ******************************************
# 3. Compress and index output
# ******************************************

bgzip output.vcf || exit 1
tabix output.vcf.gz || exit 1
