#!/usr/bin/env bash
set -e

ports=(5000 27017)

for port in "${ports[@]}"; do
    lsof -i:"$port" -t | xargs kill || true
done
