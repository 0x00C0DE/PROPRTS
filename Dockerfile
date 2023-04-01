FROM public.ecr.aws/lambda/python:3.8

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .
RUN  pip install --target "${LAMBDA_TASK_ROOT}" -r requirements.txt

# Copy function code
COPY src/* ${LAMBDA_TASK_ROOT}
COPY python_aws/* ${LAMBDA_TASK_ROOT}
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

ENTRYPOINT [ "python3" ]

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.lambda_handler" ] 