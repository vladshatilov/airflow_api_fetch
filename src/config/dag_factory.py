import inspect
from datetime import timedelta
from typing import List, Union

from airflow import DAG

from config.config import DAGS_FOLDER, DEFAULT_START_DATE, PROJECT_SYSTEM, SYSTEM_PRIORITY_WEIGHT, TASK_TIMEOUT


class MyDAG(DAG):
    _project_name: str = None
    _name: str = None
    _file: str = None
    _owner: str = None
    _reviewers: List[str] = None
    # is_debug: bool = False

    def __init__(self, owner: str, schedule_interval: Union[str, timedelta] = '@once',
                 # is_debug: bool = False,
                 # project_name: str = None,
                 default_args: dict = None,
                 **kwargs):
        if not default_args:
            default_args = {}

        default_args['owner'] = owner
        self._owner = owner
        self._name = self._get_dag_id()

        kwargs['start_date'] = kwargs.get('start_date', DEFAULT_START_DATE)
        default_args['start_date'] = kwargs['start_date']

        if 'execution_timeout' not in default_args:
            default_args['execution_timeout'] = TASK_TIMEOUT

        # if self.is_debug:
        #     schedule_interval = '@once'

        if 'pool' not in default_args:
            default_args['pool'] = 'default_pool'

        # if project_name == PROJECT_SYSTEM:
        #     default_args['priority_weight'] = SYSTEM_PRIORITY_WEIGHT

        default_args['depends_on_past'] = False

        super().__init__(
            # f'{project_name}.{self._name}',
            schedule_interval=schedule_interval,
            default_args=default_args, catchup=False,
            **kwargs)

    @staticmethod
    def _get_dag_id() -> str:
        stack = inspect.stack()
        for i in range(len(stack)):
            if f'{DAGS_FOLDER}/dags/' in stack[i].filename:
                return stack[i].filename.replace(f'{DAGS_FOLDER}/dags/', '').split('/')[-1][:-3]

    def run(self, **kwargs):
        super().run(**kwargs)
