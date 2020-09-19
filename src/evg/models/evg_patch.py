from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class VariantTasks(BaseModel):

    name: str
    tasks: List[str]


class GithubPatchData(BaseModel):

    pr_number: int
    base_owner: str
    base_repo: str
    head_owner: str
    head_repo: str
    head_hash: str
    author: str


class FileDiff(BaseModel):
    file_name: str
    additions: int
    deletions: int
    diff_link: str


class ModuleCodeChange(BaseModel):
    branch_name: str
    html_link: str
    raw_link: str
    file_diffs: List[FileDiff]


class EvgPatch(BaseModel):

    patch_id: str
    description: str
    project_id: str
    branch: str
    git_hash: str
    patch_number: int
    author: str
    version: str
    status: str
    create_time: datetime
    start_time: Optional[datetime]
    finish_time: Optional[datetime]
    builds: List[str]
    tasks: List[str]
    variants_tasks: List[VariantTasks]
    activated: bool
    alias: str
    github_patch_data: GithubPatchData
    module_code_changes: List[ModuleCodeChange]
    # parameters: List[]
    patched_config: str
    project: str
    can_enqueue_to_commit_queue: bool


# patch_id: "5f63a4675623433a436d1a2e",
# description: "'10gen/build-baron-tools' commit queue merge (PR #297) by david.bradford: DAG-422: Update to use python-service-tools (https://github.com/10gen/build-baron-tools/pull/297)",
# project_id: "build-baron-tools",
# branch: "build-baron-tools",
# git_hash: "1295dea9d737dac932d149c2a2b415f879be6513",
# patch_number: 1997,
# author: "david.bradford",
# version: "5f63a4675623433a436d1a2e",
# status: "succeeded",
# create_time: "2020-09-17T18:01:11.235Z",
# start_time: "2020-09-17T18:02:21.006Z",
# finish_time: "2020-09-17T18:07:14.087Z",
# builds: [
# "ubuntu1604"
# ],
# tasks: [
# "test_ui",
# "lint_ui",
# "check_formatting_ui",
# "build_ui",
# "unit_tests"
# ],
# variants_tasks: [
# {
# name: "ubuntu1604",
# tasks: [
# "unit_tests",
# "test_ui",
# "lint_ui",
# "check_formatting_ui",
# "build_ui"
# ]
# }
# ],
# activated: true,
# alias: "__commit_queue",
# github_patch_data: {
# pr_number: 297,
# base_owner: "10gen",
# base_repo: "build-baron-tools",
# head_owner: "",
# head_repo: "",
# head_hash: "0c541e0694e60846b7c86be27b74b8b09c0d4525",
# author: ""
# },
# module_code_changes: [
# {
# branch_name: "build-baron-tools",
# html_link: "https://evergreen.mongodb.com/filediff/5f63a4675623433a436d1a2e?patch_number=0",
# raw_link: "https://evergreen.mongodb.com/rawdiff/5f63a4675623433a436d1a2e?patch_number=0",
# file_diffs: [
# {
# file_name: "poetry.lock",
# additions: 21,
# deletions: 4,
# diff_link: "https://evergreen.mongodb.com/filediff/5f63a4675623433a436d1a2e?file_name=poetry.lock&patch_number=0"
# },
# {
# file_name: "pyproject.toml",
# additions: 1,
# deletions: 1,
# diff_link: "https://evergreen.mongodb.com/filediff/5f63a4675623433a436d1a2e?file_name=pyproject.toml&patch_number=0"
# },
# {
# file_name: "src/bb/bb_process_failure_queue_cli.py",
# additions: 1,
# deletions: 1,
# diff_link: "https://evergreen.mongodb.com/filediff/5f63a4675623433a436d1a2e?file_name=src%2Fbb%2Fbb_process_failure_queue_cli.py&patch_number=0"
# },
# {
# file_name: "src/bb/config/logging_config.py",
# additions: 1,
# deletions: 1,
# diff_link: "https://evergreen.mongodb.com/filediff/5f63a4675623433a436d1a2e?file_name=src%2Fbb%2Fconfig%2Flogging_config.py&patch_number=0"
# },
# {
# file_name: "src/bb/db/bf_collection.py",
# additions: 1,
# deletions: 1,
# diff_link: "https://evergreen.mongodb.com/filediff/5f63a4675623433a436d1a2e?file_name=src%2Fbb%2Fdb%2Fbf_collection.py&patch_number=0"
# },
# {
# file_name: "src/bb/db/task_failure_collection.py",
# additions: 1,
# deletions: 1,
# diff_link: "https://evergreen.mongodb.com/filediff/5f63a4675623433a436d1a2e?file_name=src%2Fbb%2Fdb%2Ftask_failure_collection.py&patch_number=0"
# },
# {
# file_name: "src/bbserver/app.py",
# additions: 2,
# deletions: 2,
# diff_link: "https://evergreen.mongodb.com/filediff/5f63a4675623433a436d1a2e?file_name=src%2Fbbserver%2Fapp.py&patch_number=0"
# }
# ]
# }
# ],
# parameters: [ ],
# patched_config: "buildvariants: - display_name: Ubuntu 16.04 name: ubuntu1604 run_on: - ubuntu1604-test tasks: - name: unit_tests - name: test_ui - name: lint_ui - name: check_formatting_ui - name: build_ui functions: create virtualenv: - command: shell.exec params: working_dir: src script: | set -o errexit /opt/mongodbtoolchain/v3/bin/python3 -m venv venv . venv/bin/activate pip install poetry poetry install pre: - command: git.get_project params: directory: src - func: create virtualenv post: - command: attach.xunit_results params: file: src/*_junit.xml tasks: - name: unit_tests commands: - command: shell.exec params: working_dir: src script: | set -o errexit . venv/bin/activate export LD_LIBRARY_PATH=/opt/mongodbtoolchain/v3/lib poetry run pytest src tests - name: test_ui commands: - command: shell.exec params: working_dir: src/bb-ui script: | set -o errexit set -o verbose PATH=$PATH:/opt/node/bin npm install CI=true npm run test:ci - name: lint_ui commands: - command: shell.exec params: working_dir: src/bb-ui script: | set -o errexit set -o verbose PATH=$PATH:/opt/node/bin npm install npm run lint:ci - name: check_formatting_ui commands: - command: shell.exec params: working_dir: src/bb-ui script: | set -o errexit set -o verbose PATH=$PATH:/opt/node/bin npm install npm run format:ci - name: build_ui commands: - command: shell.exec params: working_dir: src/bb-ui script: | set -o errexit set -o verbose PATH=$PATH:/opt/node/bin npm install npm run build ",
# project: "build-baron-tools",
# can_enqueue_to_commit_queue: false