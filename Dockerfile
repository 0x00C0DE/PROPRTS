FROM public.ecr.aws/lambda/python:3.8

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .
RUN  pip install --target "${LAMBDA_TASK_ROOT}" -r requirements.txt

# Copy function code
COPY ./src ${LAMBDA_TASK_ROOT}
COPY ./python-aws ${LAMBDA_TASK_ROOT}
COPY ./lambda_function.py ${LAMBDA_TASK_ROOT}

ENTRYPOINT [ "python3", "lambda_function.py" ]