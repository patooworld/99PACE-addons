# Copyright 2023 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""
Tests for tfx_addons.copy_example_gen.component.
"""
from unittest import mock

import tensorflow as tf

from tfx_addons.copy_example_gen import component


class TestCopyExampleGen(tf.test.TestCase):
  """Test module for CopyExampleGen."""
  def setUp(self):
    self.input_json_str = """
    {
      "label1": "fakeuri",
      "label2": "fakeuri2",
    }
    """

  def test_empty_input(self) -> None:
    empty_input_json_str = ""
    expected_error = (
        "Input string is not provided. Expected format is Split label (key) "
        "and Split URI (value).")

    with self.assertRaises(ValueError, msg=expected_error):
      # pylint: disable=protected-access
      component._create_input_dictionary(input_json_str=empty_input_json_str)

  def test_non_dictionary_input(self) -> None:
    non_dictionary_input = "'a', 'b', 'c'"
    expected_error = (
        f"Input string {non_dictionary_input} is not provided as a dictionary. "
        "Expected format is Split label (key) and Split URI (value).")

    with self.assertRaises(ValueError, msg=expected_error):
      # pylint: disable=protected-access
      component._create_input_dictionary(input_json_str=non_dictionary_input)

  def test_empty_dictionary(self) -> None:
    empty_input_json_str = "{}"
    expected_error = (
        "Input dictionary is empty. Expected format is Split label (key) "
        "and Split URI (value).")

    with self.assertRaises(ValueError, msg=expected_error):
      # pylint: disable=protected-access
      component._create_input_dictionary(input_json_str=empty_input_json_str)

  def test_valid_input(self) -> None:
    with mock.patch('tfx_addons.copy_example_gen.component.fileio'):
      # pylint: disable=protected-access
      component.CopyExampleGen(input_json_str=self.input_json_str)

  def test_empty_gcs_directory(self) -> None:
    with mock.patch(
        'tfx_addons.copy_example_gen.component.fileio') as mock_fileio:
      # Returns an empty list indicating no matching files in that location.
      mock_fileio.glob.return_value = []
      with self.assertLogs() as warning_msg:
        # pylint: disable=protected-access
        component._copy_examples(split_tfrecords_uri="mock_uri",
                                 split_value_uri="mock_uri_2")
        expected_msg = (
            "WARNING:root:Directory mock_uri does not contain files with .gz "
            "suffix.")
        self.assertEqual(warning_msg.output, [expected_msg])
