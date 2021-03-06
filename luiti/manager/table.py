# -*-coding:utf-8-*-

import os
from .dep import Dep
import luigi


class Table(object):
    """
    print task and package info.
    """

    @staticmethod
    def puts(task_body, task_headers, **opts):
        from tabulate import tabulate
        result = tabulate(task_body, task_headers, **opts)
        print
        print result
        print
        return result

    @staticmethod
    def print_all_tasks(result):
        """ input from Loader.load_all_tasks """

        def task_inspect(task_cls, order):
            return [
                order,
                task_cls.__name__,
                task_cls.__module__.split(".")[0]
            ]

        task_headers = ["", "All Tasks", "luiti_package"]
        task_body = [task_inspect(item1['task_cls'], idx1 + 1)
                     for idx1, item1 in enumerate(sorted(result['success']))]
        task_body.extend([["total", len(result['success']), ""]])

        Table.puts(task_body, task_headers, tablefmt="grid")

        if result['failure']:
            print
            print "[warn] failure parsed files"
            print
            for failure1 in result['failure']:
                print "[task_file] ", failure1['task_clsname']
                print "[err] ", failure1['err']
                print
        return (task_body, task_headers)

    @staticmethod
    def print_files_by_task_cls_and_date_range(curr_task, args, opts=None):
        opts = opts or dict()
        # 打印 依赖类 和 执行配置 信息
        task_headers = ["Current Env Key", "Current Env Value"]
        task_body = [
            ["task name", args.task_name],
            ["task date range", args.date_range],
            ["task execute mode", "DRY=" + str(args.dry)],
            ["task dep mode", "DEP=" + str(args.dep)],
            ["related task classes total count", opts['task_classes_count']],
        ]
        print
        print "Tasks related infos"
        Table.puts(task_body, task_headers, tablefmt="grid")

        # 打印 要删除的文件列表
        file_headers = ["Generated from task", "Storage",
                        "Date value", "Filename"]

        dep_file_to_task_instances = opts['dep_file_to_task_instances']
        file_table = [
            [dep_file_to_task_instances[f1].__class__.__name__,
             'HDFS', dep_file_to_task_instances[f1].date_str,
             os.path.basename(f1), ]
            for f1 in sorted(dep_file_to_task_instances.keys())]
        file_table.append(
            ['', '', '', "Total count %s" % len(dep_file_to_task_instances)])
        file_table.append(['', '', '', ''])
        file_uniq_root_dir = set(
            [t1.root_dir for t1 in opts['dep_tasks_on_curr_task']])
        file_table.append(
            ['All root dirs', '', '',
             'Total count %s' % len(file_uniq_root_dir)])
        for dir1 in file_uniq_root_dir:
            file_table.append(['', '', '', dir1])

        print
        print "Files related infos"
        Table.puts(file_table, file_headers, tablefmt="grid")
        print "\n" * 3
        return (file_table, file_headers)

    @staticmethod
    def print_task_info(curr_task):
        assert issubclass(curr_task, luigi.Task)

        dep_tasks_on_curr_task = Dep.find_dep_on_tasks(
            curr_task, Table.ld.all_task_classes)

        task_headers = ["Task name", curr_task.__name__]
        task_content = [
            ["Tasks self dep on", str(list(curr_task._ref_tasks))],
            ["Tasks dep on self",
             str(sorted([t2.__name__ for t2 in dep_tasks_on_curr_task]))],
        ]
        Table.puts(task_content, task_headers, tablefmt="grid")
        return (task_content, task_headers)
