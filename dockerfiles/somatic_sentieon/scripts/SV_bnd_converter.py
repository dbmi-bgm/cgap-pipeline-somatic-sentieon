#!/usr/bin/env python3

################################################
#
#  Script to convert Sentieon SVs to BEDPE
#
################################################

################################################
#   Libraries
################################################
import sys, argparse, subprocess
from granite.lib import vcf_parser
import re


class sample_entry:
    def __init__(self, CHROM1, START1, CHROM2, START2, NAME, SCORE, STRAND1, STRAND2):
        self.CHROM1 = CHROM1
        self.START1 = str(int(START1-1))
        self.END1 = str(START1)
        self.CHROM2 = CHROM2
        self.START2 = str(int(START2-1))
        self.END2 = str(START2)
        self.NAME = self
        self.STRAND1 = STRAND1
        self.STRAND2 = STRAND2

################################################
#   Functions
################################################

def mate_matcher(vnt_obj, mate_dict):
    if vnt_obj.ID not in mate_dict:
        try:
            mate_dict[vnt_obj.ID] = {vnt_obj.get_tag_value("MATEID"):vnt_obj}
        except Exception:
            print('no mate')
    else:
        print("duplicate?")

def vcf_scanner():#(args['inputvcf']):
    #vcf = vcf_parser.Vcf(args['inputvcf'])
    vcf = vcf_parser.Vcf('/Users/phil_hms/Desktop/somatic/SV_test_tumor_normal_with_panel.vcf')
    mate_dict = {}

    for vnt_obj in vcf.parse_variants():
        if vnt_obj.get_tag_value("SVTYPE") == "BND":
            mate_matcher(vnt_obj,mate_dict)
        else:
            #so far, I have only seen SVTYPE=INS in tumor only analyses
            #we will only support paired breakpoints at this point with BEDPE
            if vnt_obj.get_tag_value("SVTYPE") == "INS":
                pass

    return mate_dict

def mate_checker(mateID, mate_dict):
    # mate_dict has {bnd1: {bnd2: <granite.lib.vcf_parser.Vcf.Variant for bnd1>}}
    # want to check that bnd1's mate (bnd2) has bnd1 as its mate in its entry in the dictionary
    # only want to do this once for each pair, so finished_list is imporant there
    mate_match = list(mate_dict[mateID].keys())[0]
    #print(mate_match)
    #print(finished_list)
    if mateID not in finished_list:
        if mateID == list(mate_dict[mate_match].keys())[0]:
            # if they do match reciprocally, we want to store each of their vnt_objs from the original vcf file
            pair1 = list(mate_dict[mateID].values())[0]
            pair2 = list(mate_dict[mate_match].values())[0]

            # add the second mate to the finished_dict so that we only do the work once
            finished_list.append(mate_match)

            #then return the pair of vnt_objs
            return pair1, pair2

        else:
            print(mateID, mate_dict[list(mate_dict[mateID].keys())[0]])
            raise Exception('bnd mates not reciprocal for '+mateID+' and '+list(mate_dict[mateID].keys())[0])

x = '[chr22:20272153[C'
'[' in x

first_alt = re.findall(r'([])([])', x)

def strand_finder(first_bnd):
    first_alt = re.findall(r'([])([])', first_bnd.ALT)
    first_strand = second_strand = '+'

    # bnd square brackets must be in the same orientation
    if first_alt[0] == first_alt[1]:
        if first_bnd.ALT.startswith(first_alt[0]):
            first_strand = '-'
        if first_alt[0] == '[':
            second_strand = '-'

        return first_strand, second_strand
    else:
        raise Exception('bnd square brackets not matching for '+first_bnd.ID+' at '+first_bnd.CHROM+' '+first_bnd.POS)
    # bnd square brackets must be in the same orientation

    # upstream bnd has ]]N, downstream bnd has N[[, that's a - +
    # upstream bnd has N[[, downstream bnd has ]]N, that's a + -
    # upstream bnd has [[N, downstream bnd has [[N, that's a - -
    # upstream bnd has N]], downstream bnd has N]], that's a + +

def create_bedpe(pair1, pair2):
    chromsome_order =  {
                    "chr1" : 1,
                    "chr2" : 2,
                    "chr3" : 3,
                    "chr4" : 4,
                    "chr5" : 5,
                    "chr6" : 6,
                    "chr7" : 7,
                    "chr8" : 8,
                    "chr9" : 9,
                    "chr10" : 10,
                    "chr11" : 11,
                    "chr12" : 12,
                    "chr13" : 13,
                    "chr14" : 14,
                    "chr15" : 15,
                    "chr16" : 16,
                    "chr17" : 17,
                    "chr18" : 18,
                    "chr19" : 19,
                    "chr20" : 20,
                    "chr21" : 21,
                    "chr22" : 22,
                    "chrX" : 23,
                    "chrY" : 24
                    }
    #only want the main chromosomes
    if pair1.CHROM not in chromsome_order or pair2.CHROM not in chromsome_order:
        pass
    else:
        # need to determine which bnd will be #1 and which will be #2. this depends on the first one to appear in the genome
        if pair1.CHROM == pair2.CHROM:
            if pair1.POS < pair2.POS:
                first_bnd = pair1
                second_bnd = pair2
            else:
                #might not happen
                first_bnd = pair2
                second_bnd = pair1
        else:
            if chromsome_order[pair1.CHROM] < chromsome_order[pair2.CHROM]:
                first_bnd = pair1
                second_bnd = pair2
            else:
                #might not happen
                first_bnd = pair2
                second_bnd = pair1

        CHROM1 = first_bnd.CHROM
        START1 = str(int(first_bnd.POS)-1)
        END1 = str(first_bnd.POS)
        CHROM2 = second_bnd.CHROM
        START2 = str(int(second_bnd.POS)-1)
        END2 = str(second_bnd.POS)
        NAME = first_bnd.ID
        SCORE = str(first_bnd.QUAL)
        STRAND1, STRAND2 = strand_finder(first_bnd)


        bedpe_variant = [CHROM1, START1, END1, CHROM2, START2, END2, NAME, SCORE, STRAND1, STRAND2]
        return bedpe_variant



def main():

    # fill the mate_dict with pairs
    mate_dict = vcf_scanner()

    # get matched pairs from mate_dict
    global finished_list
    finished_list = []

    #with open(out_file_name, 'w') as fo:
    with open('/Users/phil_hms/Desktop/somatic/SV_test_tumor_normal_with_panel.bedpe', 'w') as fo:
        for variant in mate_dict:
            try:
                #as we move down the list we will have variants that have been moved to finished_list
                pair1, pair2 = mate_checker(variant, mate_dict)
                print(pair1.CHROM, pair2.CHROM)
                bedpe_variant = create_bedpe(pair1, pair2)
                fo.write('\t'.join(bedpe_variant)+'\n')

            except:
                pass

main()


################################################
#   MAIN
################################################
# if __name__ == '__main__':
#
#     parser = argparse.ArgumentParser(description='')
#
#     parser.add_argument('-i', '--inputvcf',  help='input sample vcf', required=True)
#     parser.add_argument('-f', '--full', help='output VCF file for all variant types', required=True)
#     parser.add_argument('-s', '--snv', help='output VCF file for SNVs', required=True)
#     parser.add_argument('-d', '--indel', help='output VCF file for INDELs', required=True)
#     parser.add_argument('-v', '--sv', help='output VCF file for SVs', required=True)
#
#     args = vars(parser.parse_args())
#
#     main(args)
