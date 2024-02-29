#!/usr/bin/env python

import argparse
import boto3
import logging
import os


class AwsEbsVolumes:
    def __init__(self, logger=None, verbose=False):
        self.logger = logger or logging.getLogger(__name__)
        self.ec2_resource = self.__get_ec2_resource()
        self.ec2_client = self.__get_ec2_client()
        self.verbose = verbose

        if self.verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

    def __get_region(self):
        try:
            return os.environ["AWS_DEFAULT_REGION"]
        except KeyError:
            self.logger.warning(
                "Error: AWS_DEFAULT_REGION environment variable is not set. "
                "Using default region 'eu-west-1'."
            )
            return "eu-west-1"

    def __get_ec2_client(self):
        try:
            return boto3.client("ec2", region_name=self.__get_region())
        except Exception as e:
            self.logger.error(f"Error creating EC2 client: {e}")
            return None

    def __get_ec2_resource(self):
        try:
            return boto3.resource("ec2", region_name=self.__get_region())
        except Exception as e:
            self.logger.error(f"Error creating EC2 resource: {e}")
            return None

    def __format_volume_info(self, volume):
        return (
            f"\nVolume ID: {volume['VolumeId']}\n"
            f"Size: {volume['Size']} GB\n"
            f"Availability Zone: {volume['AvailabilityZone']}\n"
            "------"
        )

    def delete_ebs_volume_by_id(self, volume_id):
        try:
            self.ec2_resource.Volume(volume_id).delete()
            self.logger.info(f"Volume {volume_id} deleted successfully.")
            return 1
        except Exception as e:
            self.logger.error(f"Error deleting volume {volume_id}: {e}")
            return 0

    def delete_all_unattached_ebs_volumes(self):
        all_volumes = self.list_all_unattached_ebs_volumes(print_output=False)

        if not all_volumes:
            self.logger.warning("No volumes found.")
            self.logger.warning("Aborting deletion.")
            return 0

        num_volumes_to_delete = 0

        for volume in all_volumes:
            volume_id = volume.get("VolumeId")
            self.logger.info(f"Deleting volume: {volume_id}")
            try:
                self.ec2_resource.Volume(volume_id).delete()
                self.logger.info(f"Volume {volume_id} deleted successfully.")
                num_volumes_to_delete += 1
            except Exception as e:
                self.logger.error(f"Error deleting volume {volume_id}: {e}")

        self.logger.info("All volumes deletion complete.")
        self.logger.info(f" {num_volumes_to_delete} volumes deleted.")

        return num_volumes_to_delete

    def list_all_unattached_ebs_volumes(self, print_output=True):
        volume_list = []

        try:
            volumes = self.ec2_client.describe_volumes()["Volumes"]
            for volume in volumes:
                log_message = self.__format_volume_info(volume)
                if print_output:
                    self.logger.info(log_message)
                else:
                    volume_list.append(volume)
        except Exception as e:
            self.logger.error(f"Error listing volumes: {e}")

        return volume_list

    def main(self):
        parser = argparse.ArgumentParser(description="AWS EBS Volumes Management")
        parser.add_argument(
            "--list-all-unattached-ebs-volumes",
            action="store_true",
            help="List all EBS volumes",
        )

        parser.add_argument(
            "--delete-all-unattached-ebs-volumes",
            action="store_true",
            help="Delete all EBS volumes",
        )

        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Enable verbose mode",
        )

        args = parser.parse_args()

        if args.list_all_unattached_ebs_volumes:
            self.list_all_unattached_ebs_volumes(print_output=True)
        elif args.delete_all_unattached_ebs_volumes:
            self.delete_all_unattached_ebs_volumes()
        else:
            self.logger.warning(
                "No valid command provided. Use --list-all-ebs-volumes or --delete-all-ebs-volumes."
            )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    aws_ebs_volumes = AwsEbsVolumes()
    aws_ebs_volumes.main()
