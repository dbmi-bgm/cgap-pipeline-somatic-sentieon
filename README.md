<img src="https://github.com/dbmi-bgm/cgap-pipeline/blob/master/docs/images/cgap_logo.png" width="200" align="right">

# CGAP Somatic Pipeline - Sentieon

This repository contains components for the CGAP Somatic Pipeline for SNVs, INDELs, and SVs using Sentieon:

  * CWL workflows
  * CGAP Portal Workflows and MetaWorkflows objects
  * ECR (Docker) source files, which allow for creation of public Docker images (using `docker build`) or private dynamically-generated ECR images (using [*cgap pipeline utils*](https://github.com/dbmi-bgm/cgap-pipeline-utils/) `deploy_pipeline`)

The pipeline can process analysis ready ``bam`` files for a tumor/normal comparison and produces a `vcf` file as output.
For more details check the [*documentation*](https://cgap-pipeline-main.readthedocs.io/en/latest/Pipelines/Downstream/Downstream_pipelines.html#somatic).

### Version Updates

#### v1.0.0

Coming soon...
