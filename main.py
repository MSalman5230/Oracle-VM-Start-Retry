import oci
import time

# Path to your custom OCI config file
config_path = "C:\MegaSync\Projects\SSHKeys\OCI-Config\config.txt"

# OCI Configuration
config = oci.config.from_file(config_path)  # Make sure you have the OCI config file set up

# Instance OCID (replace with your actual VM OCID)
instance_id = "ocid1.instance.oc1.ap-singapore-1.anzwsljra5grx2iclv4zs6rwap4zjvxxzdtyidykng7sg2omsauhizwfe65a"

# Create the compute client
compute_client = oci.core.ComputeClient(config)


def start_vm():
    try:
        # Get the instance details
        instance = compute_client.get_instance(instance_id).data
        if instance.lifecycle_state == "STOPPED":
            print("Starting VM...")
            compute_client.instance_action(instance_id, "START")
            print("VM start request sent.")
        elif instance.lifecycle_state == "RUNNING":
            print("VM is already running.")
        else:
            print(f"VM is in {instance.lifecycle_state} state.")
    except oci.exceptions.ServiceError as e:
        if "Out of host capacity" in str(e):
            print("Out of host capacity, retrying in 60 seconds...")
        else:
            print(f"Failed to start VM: {e}")


if __name__ == "__main__":
    while True:
        try:
            start_vm()
        except Exception as e:
            print(e)
        time.sleep(60)
