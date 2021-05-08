#!/bin/bash
#set -v
echo start
kubectl apply -f 0_namespace.yaml
sleep 5
helm install postgres bitnami/postgresql -f helm/pg_values.yaml -n testing3
sleep 30
kubectl get pods -n testing3
sleep 30
kubectl apply -f . 
echo stop