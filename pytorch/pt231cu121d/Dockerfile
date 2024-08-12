FROM hangbo/pytorch:pt231cu121

RUN pip install datasets
RUN python -m pip install flash-attn --no-build-isolation
RUN pip install fire nltk
RUN pip install jsonlines
RUN pip install llm-blender
RUN pip install transformers==4.43.3
RUN pip install vllm==0.5.3.post1
