#!/bin/bash
cd /home/kavia/workspace/code-generation/wordcharcountapi-69997-02e6a7e1/django_backend_workspace/django_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

