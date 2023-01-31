<img src="https://github.com/dbmi-bgm/cgap-pipeline/blob/master/docs/images/cgap_logo.png" width="200" align="right">

# CGAP Somatic Pipeline - Sentieon

This repository contains components for the CGAP pipeline for Single Nucleotide Variants (SNVs), small insertions/delitions (INDELs), and Structural Variants (SVs) in somatic data using Sentieon:

  * CWL workflow descriptions
  * CGAP Portal *Workflow* and *MetaWorkflow* objects
  * CGAP Portal *Software*, *FileFormat*, and *FileReference* objects
  * ECR (Docker) source files, which allow for creation of public Docker images (using `docker build`) or private dynamically-generated ECR images (using [*cgap pipeline utils*](https://github.com/dbmi-bgm/cgap-pipeline-utils/) `pipeline_deploy`)

The pipeline can process analysis ready `bam` files for a tumor/normal comparison and produces a `vcf` file as output.
Documentation for all CGAP Pipelines can now be found here:
https://cgap-pipeline-main.readthedocs.io/en/latest/
