#!/bin/bash
cd /home/kavia/workspace/code-generation/wordcharcountapi-69997-02e6a7e1/astro_frontend_workspace/astro_frontend
npm run lint 
$ESLINT_EXIT_CODE
npm run build
BUILD_EXIT_CODE=$?
if [ $ESLINT_EXIT_CODE -ne 0 ] || [ $BUILD_EXIT_CODE -ne 0 ]; then
  exit 1
fi

