#!/usr/bin/env python
import unittest
from botocore.exceptions import ClientError
from unittest.mock import MagicMock, patch
from unattached_volumes.unattached_volumes import AwsEbsVolumes

VOLUME_ID = "vol-04298f2566bc60403"


class TestAwsEbsVolumes(unittest.TestCase):

    @staticmethod
    def __create_mock_volume():
        """
        Creates a mock Volume without a simulated delete error.
        """
        mock_volume = MagicMock()
        mock_volume.delete.side_effect = None
        return mock_volume

    @patch("unattached_volumes.unattached_volumes.boto3")
    def test_delete_ebs_volume_by_id_success(self, mock_boto3):
        aws_ebs_volumes = AwsEbsVolumes()

        # Mock the EC2 resource and its Volume
        mock_ec2_resource = mock_boto3.resource.return_value
        mock_ec2_volume = mock_ec2_resource.Volume.return_value

        # Mock the Volume for a successful deletion
        mock_volume = self.__create_mock_volume()

        # Attach the mock_volume to the Volume
        mock_ec2_volume.attach_mock(mock_volume, "Volume")

        # Act
        result = aws_ebs_volumes.delete_ebs_volume_by_id(VOLUME_ID)

        # Assert
        self.assertEqual(result, 1)
        mock_boto3.resource.assert_called_once_with(
            "ec2", region_name=aws_ebs_volumes._AwsEbsVolumes__get_region()
        )
        mock_ec2_resource.Volume.assert_called_once_with(VOLUME_ID)
        mock_ec2_volume.delete.assert_called_once()

    @patch("unattached_volumes.unattached_volumes.boto3")
    def test_delete_ebs_volume_by_id_volume_not_exists(self, mock_boto3):
        aws_ebs_volumes = AwsEbsVolumes()

        mock_ec2_resource = mock_boto3.resource.return_value

        mock_ec2_resource.Volume.side_effect = ClientError(
            {
                "Error": {
                    "Code": "InvalidVolume.NotFound",
                    "Message": "Volume not found",
                }
            },
            "operation_name",
        )

        result = aws_ebs_volumes.delete_ebs_volume_by_id(VOLUME_ID)

        self.assertEqual(result, 0)
        mock_boto3.resource.assert_called_once_with(
            "ec2", region_name=aws_ebs_volumes._AwsEbsVolumes__get_region()
        )
        mock_ec2_resource.Volume.assert_called_once_with(VOLUME_ID)
        mock_ec2_resource.Volume.return_value.delete.assert_not_called()


if __name__ == "__main__":
    unittest.main()
