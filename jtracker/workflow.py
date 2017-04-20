import yaml

class Workflow(object):
    def __init__(self, workflow_yaml_file=None):
        with open(workflow_yaml_file, 'r') as stream:
            self._workflow_dict = yaml.load(stream)

        self._name = self.workflow_dict.get('workflow').get('name')
        self._version = self.workflow_dict.get('workflow').get('version')

        self._get_workflow_calls()
        self._add_default_runtime_to_tasks()


    @property
    def name(self):
        return self._name


    @property
    def version(self):
        return self._version


    @property
    def workflow_dict(self):
        return self._workflow_dict


    @property
    def workflow_calls(self):
        return self._workflow_calls


    def _get_workflow_calls(self):
        calls = self.workflow_dict.get('workflow', {}).get('calls', {})

        for c in calls:
            task_called = calls[c].get('task')
            if not task_called:
                calls[c]['task'] = c

        self._workflow_calls = calls


    def _add_default_runtime_to_tasks(self):
        for t in self.workflow_dict.get('tasks', {}):
            if not 'runtime' in t:  # no runtime defined in the task, add the default one
                self.workflow_dict['tasks'][t]['runtime'] = self.workflow_dict.get('workflow', {}).get('runtime')
