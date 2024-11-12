# %% create a bucket called f1_data 
# create a new api token with read and write permissions to f1_data
import os
from influxdb_client import InfluxDBClient, BucketsApi, Permission, PermissionResource, Organization

# %% Configuration
url = "http://localhost:64093"
token = os.getenv("INFLUXDB_ADMIN_TOKEN")
org = "influxdata"
bucket_name = "f1_data"

# Initialize the InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)

# Create a bucket
buckets_api = client.buckets_api()
bucket = buckets_api.create_bucket(bucket_name=bucket_name, org=org)
print(f"Bucket '{bucket_name}' created.")

# Create read and write permissions for the bucket
bucket_id = bucket.id
read_permission = Permission(
    action="read",
    resource=PermissionResource(type="buckets", id=bucket_id, org_id=bucket.org_id)
)
write_permission = Permission(
    action="write",
    resource=PermissionResource(type="buckets", id=bucket_id, org_id=bucket.org_id)
)

# Create a new API token with the permissions
authorization_api = client.authorizations_api()
token = authorization_api.create_authorization(org_id=bucket.org_id, permissions=[read_permission, write_permission])
print(f"API token created with ID: {token.id}")

# Output the token
print(f"API token: {token.token}")

# Close the client
client.close()
# %%
