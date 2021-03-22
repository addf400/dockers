
FROM pytorch/pytorch:1.3-cuda10.1-cudnn7-devel

RUN apt-get update && apt-get install vim screen -y
RUN pip install --user methodtools py-rouge pyrouge nltk
RUN python -c "import nltk; nltk.download('punkt')"

RUN if [ -d apex ]; then rm -Rf apex; fi
RUN git clone https://github.com/NVIDIA/apex.git && cd apex && git reset --hard 453eefa56454142f8fc788478ad511973cc0fe1b && python setup.py install --cuda_ext --cpp_ext

# pip install botocore==1.18.18 --user
# echo "install botocore 1.18.18 done!"
RUN pip install boto3==1.14.11 --user
RUN echo "**** install boto3==1.14.11 done!"
RUN pip install sentencepiece==0.1.91 --user
RUN echo "**** sentencepiece==0.1.91 done!"

RUN pip install transformers==2.3.0 tensorboardX==1.8 scikit-learn==0.20.3


RUN apt-get update && apt-get install expat libexpat-dev -y
RUN cpan install XML::Parser
RUN cpan install XML::Parser::PerlSAX
RUN cpan install XML::DOM


