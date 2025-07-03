#!/bin/bash
set -e  # Exit on any error

echo "Starting MinIO bucket initialization..."

# Wait for MinIO to be ready
echo "Waiting for MinIO to be ready..."
for i in {1..30}; do
    if /usr/bin/mc alias set myminio http://s3-artifact-storage:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD" 2>/dev/null; then
        echo "MinIO connection successful!"
        break
    else
        echo "Attempt $i/30: MinIO not ready yet, waiting 2 seconds..."
        sleep 2
    fi
    if [ $i -eq 30 ]; then
        echo "ERROR: MinIO failed to become ready after 60 seconds"
        exit 1
    fi
done

# Create bucket (ignore error if it already exists)
echo "Creating bucket 'data'..."
if /usr/bin/mc mb myminio/data 2>/dev/null; then
    echo "Bucket 'data' created successfully"
elif /usr/bin/mc ls myminio/data >/dev/null 2>&1; then
    echo "Bucket 'data' already exists"
else
    echo "ERROR: Failed to create or verify bucket 'data'"
    exit 1
fi

# Set bucket policy
echo "Setting bucket policy..."
if /usr/bin/mc anonymous set download myminio/data; then
    echo "Bucket policy set successfully"
else
    echo "ERROR: Failed to set bucket policy"
    exit 1
fi

# Verify setup
echo "Verifying setup..."
if /usr/bin/mc ls myminio/data >/dev/null 2>&1; then
    echo "SUCCESS: MinIO bucket setup completed successfully!"
else
    echo "ERROR: Bucket verification failed"
    exit 1
fi
