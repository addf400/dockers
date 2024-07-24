FROM singularitybase.azurecr.io/validations/base/singularity-tests:20240722T152227637 as validator 
FROM hangbo/pytorch-2.23dev:xformers
COPY --from=validator /validations /opt/microsoft/_singularity/validations/ 
RUN /opt/microsoft/_singularity/validations/validator.sh 
