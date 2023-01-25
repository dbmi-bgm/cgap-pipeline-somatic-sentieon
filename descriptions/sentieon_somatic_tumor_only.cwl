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

baseCommand: [somatic_sentieon_tumor_only.sh]

inputs:
  - id: input_bam
    type: File
    inputBinding:
      position: 1
    secondaryFiles:
      - .bai
    doc: input bam file, must have read groups

  - id: samplename
    type: string
    inputBinding:
      position: 2
    doc: expect string for sample name from bam

  - id: reference_fa
    type: File
    inputBinding:
      position: 3
    secondaryFiles:
      - .fai
    doc: expect the path to the fa file

  - id: known-sites-snp
    type: File
    inputBinding:
      position: 4
    secondaryFiles:
      - .tbi
    doc: expect the path to the dbsnp vcf gz file

outputs:
  - id: output_vcf_gz
    type: File
    outputBinding:
      glob: output.vcf.gz
    secondaryFiles:
        - .tbi

doc: |
  run somatic Sentieon for tumor sample only
