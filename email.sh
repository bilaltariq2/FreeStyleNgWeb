#!/bin/bash

email1="btariq@stellatechnology.com"
echo "Hi, Please find the attach Amazon ECR Image vulnerabilities report. Thanks"| mail -s "ECR Image Scan Report" -A `ls -t /var/lib/jenkins/workspace/nginx-ecr/scan_report* | head -1` $email1
