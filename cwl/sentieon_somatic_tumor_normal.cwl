#!/usr/bin/env cwl-runner

cwlVersion: v1.0

class: CommandLineTool

requirements:
  - class: InlineJavascriptRequirement

  - class: EnvVarRequirement
    envDef:
      -
        envName: SENTIEON_LICENSE
        envValue: LICENSEID

hints:
  - class: DockerRequirement
    dockerPull: ACCOUNT/somatic_sentieon:VERSION

baseCommand: [somatic_sentieon_tumor_normal.sh]

inputs:
  - id: input_bam_tumor
    type: File
    inputBinding:
      position: 1
    secondaryFiles:
      - .bai
    doc: input bam file, must have read groups

  - id: tumorname
    type: string
    inputBinding:
      position: 2
    doc: expect string for sample name from tumor bam

  - id: input_bam_normal
    type: File
    inputBinding:
      position: 3
    secondaryFiles:
      - .bai
    doc: input bam file, must have read groups

  - id: normalname
    type: string
    inputBinding:
      position: 4
    doc: expect string for sample name from tumor bam

  - id: reference_fa
    type: File
    inputBinding:
      position: 5
    secondaryFiles:
      - .fai
    doc: expect the path to the fa file

  - id: known-sites-snp
    type: File
    inputBinding:
      position: 6
    secondaryFiles:
      - .tbi
    doc: expect the path to the dbsnp vcf gz file

  - id: pon
    type: File
    inputBinding:
      position: 7
    secondaryFiles:
      - .tbi
    doc: expect the path to the panel of normals vcf gz file

outputs:
  - id: output_vcf_gz
    type: File
    outputBinding:
      glob: output.vcf.gz
    secondaryFiles:
        - .tbi

doc: |
  run somatic Sentieon for tumor-normal 
