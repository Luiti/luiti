# -*-coding:utf-8-*-

__all__ = ["PTM"]


import sys
from etl_utils import singleton, cached_property
import importlib
import inspect
from copy import deepcopy

from ... import manager
from ..utils import stringify

from .params import Params
from .query import Query


@singleton()
class PackageTaskManagementClass(Params, Query):
    """
    Manage packages and tasks.
    """

    @cached_property
    def current_package_name(self):
        return manager.luiti_config.get_curr_project_name()

    @cached_property
    def current_init_luiti(self):
        self.current_package_path  # insert pacakge into sys.path
        __init_luiti = self.current_package_name + ".luiti_tasks.__init_luiti"
        return importlib.import_module(__init_luiti)

    @cached_property
    def current_package_path(self):
        p1 = manager.luiti_config.get_curr_project_path()
        sys.path.insert(0, p1)
        return p1

    @cached_property
    def current_luiti_visualiser_env(self):
        # TODO assert must setup `luiti_visualiser_env`
        return getattr(self.current_init_luiti, "luiti_visualiser_env")

    @cached_property
    def load_all_tasks_result(self):
        return manager.load_all_tasks()

    @cached_property
    def task_classes(self):
        return [i1["task_cls"] for i1 in self.load_all_tasks_result["success"]]

    @cached_property
    def task_class_names(self):
        return [i1.__name__ for i1 in self.task_classes]

    @cached_property
    def task_clsname_to_package(self):
        return manager.PackageMap.task_clsname_to_package

    @cached_property
    def task_clsname_to_source_file(self):
        def get_pyfile(task_cls):
            f1 = inspect.getfile(task_cls)
            return f1.replace(".pyc", ".py")

        return {task_cls.__name__: get_pyfile(task_cls) for task_cls in self.task_classes}

    @cached_property
    def task_clsname_to_package_name(self):
        return {t1: p1.__name__ for t1, p1 in self.task_clsname_to_package.iteritems()}

    @cached_property
    def task_package_names(self):
        return sorted([p1.__name__ for p1 in set(self.task_clsname_to_package.values())])

    @cached_property
    def package_to_task_clsnames(self):
        return {package.__name__: list(task_clsnames) for package, task_clsnames
                in manager.PackageMap.package_to_task_clsnames.iteritems()}

    def generate_task_instance_repr_to_info(self, task_instances):
        result = dict()
        for ti in task_instances:
            param_kwargs = deepcopy(ti.param_kwargs)
            if "pool" in param_kwargs:
                del param_kwargs["pool"]
            result[str(ti)] = {"task_cls": ti.task_clsname, "param_kwargs": stringify(param_kwargs)}
        return result

PTM = PackageTaskManagementClass()