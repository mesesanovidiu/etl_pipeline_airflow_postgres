import unittest
from datetime import datetime
import pendulum
from jsonschema import validate
from user_processing import json_std_schema

from airflow.models import DagBag
from airflow.models import TaskInstance
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.email import EmailOperator

from user_processing import (validate_user_schema, check_data, process_user, store_user)


class TestUserProcessing(unittest.TestCase):
        
    def setUp(self):
        self.dagbag = DagBag()
        self.dag_id = 'user_processing'
        self.dag = self.dagbag.get_dag(dag_id=self.dag_id)

    def test_dag_loaded(self):
        """Test that the DAG is loaded successfully"""
        self.assertIsNotNone(self.dag)

    def test_task_count(self):
        """Test that the DAG contains the expected number of tasks"""
        expected_task_count = 7
        self.assertEqual(len(self.dag.tasks), expected_task_count)

    def test_contain_tasks(self):
        """Test that the DAG contains the expected tasks"""
        expected_task_ids = [
            'create_table',
            'is_api_available',
            'extract_user',
            'validate_user_schema',
            'process_user',
            'store_user',
            'check_data'
        ]
        task_ids = [task.task_id for task in self.dag.tasks]
        self.assertListEqual(expected_task_ids, task_ids)

    def test_default_args(self):
        """Test that the DAG's default arguments are set correctly"""
        expected_default_args = {
            'catchup': False,
            'email': ['mesesan_ovidiu@yahoo.com'],
            'email_on_retry': False,
            'email_on_failure': False
        }
        self.assertDictEqual(expected_default_args, self.dag.default_args)

    def test_schedule_interval(self):
        """Test that the DAG's schedule interval is set correctly"""
        expected_schedule_interval = '* * * * *'
        self.assertEqual(expected_schedule_interval, self.dag.schedule_interval)

    def test_start_date(self):
        """Test that the DAG's start date is set correctly"""
        expected_start_date = pendulum.datetime(2021, 1, 1, tz="UTC")
        self.assertEqual(expected_start_date, self.dag.start_date)


if __name__ == '__main__':
    unittest.main()