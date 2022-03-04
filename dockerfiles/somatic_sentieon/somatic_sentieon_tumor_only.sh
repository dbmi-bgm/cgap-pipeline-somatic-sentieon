#!/bin/sh

# *******************************************
# Script to run somatic Sentieon (TNscope)
# on tumor only (e.g., for creation of
# panel of normals)
# *******************************************

## Command line arguments
# input bam
raw_bam=$1
sample_name=$2

# reference data files
reference_fa=$3
dbsnp=$4

## Other settings
nt=$(nproc) #number of threads to use in computation, set to number of cores in the server

# ******************************************
# 1. Run TNscope
# ******************************************

sentieon driver --algo TNscope -t $nt -r $reference_fa -i $raw_bam --tumor_sample $sample_name output.vcf || exit 1

# ******************************************
# 2. Compress and index output
# ******************************************

bgzip output.vcf || exit 1
tabix output.vcf.gz || exit 1
