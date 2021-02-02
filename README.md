# aio-evergreen.py

An async experimental Evergreen API client.

## Table of contents

1. [Description](#description)
2. [Dependencies](#dependencies)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Documentation](#documentation)
6. [Contributor's Guide](#contributors-guide)
    - [High Level Architecture](#high-level-architecture)
    - [Setting up a local development environment](#setting-up-a-local-development-environment)
    - [linting/formatting](#lintingformatting)
    - [Running tests](#running-tests)
    - [Automatically running checks on commit](#automatically-running-checks-on-commit)
    - [Versioning](#versioning)
    - [Code Review](#code-review)
    - [Deployment](#deployment)
    - [Additional Documentation](#additional-documentation)
7. [Resources](#resources)

## Description

An async python client for the [Evergreen](https://github.com/evergreen-ci/evergreen/wiki/REST-V2-Usage) API. 

**Note**: This is currently experimental and under development.

## Dependencies

* Python 3.6 or later

## Installation

Installation is done via pip.

```bash
$ pip install aio-evergreen.py
```

## Usage

In order to make API calls, you will need an api object. This will create a shared session
that will need to be cleaned up when done. To handle the creation and cleanup, you can use
an `EvgApiFactory`.

Here is an example of using the API to stream a task log:

```python
import asyncio
from evg import EvgApiFactory


async def stream_log(api_factory: EvgApiFactory, task_id: str) -> None:
    async with api_factory.evergreen_api() as evg_api:
        task = await evg_api.task_by_id(task_id)
        task_log = task.log.get("task_log")
        async for line in evg_api.stream_log(task_log):
            print(line)

            
api_factory = EvgApiFactory.from_default_config()
asyncio.run(stream_log(api_factory, "task_1234"))
```

## Documentation

_Links to any additional documentation for the project. This refers to documentation meant
for end users of the project. For APIs, this should include a link to the swagger docs._

## Contributor's Guide

_This section should contain details on how to make contributions to the project. It can be
embedded here in the README or be a link to other documentations, but should include the 
following._

### High Level Architecture

TBD

### Setting up a local development environment

This project uses poetry to manage the python project.

```bash
$ poetry install
```

### linting/formatting

```bash
$ poetry run black src tests
```

### Running tests

```bash
$ poetry run pytest
```

### Automatically running checks on commit

_For projects with pre-commit support, explain how to enable it._

This project has [pre-commit](https://pre-commit.com/) configured. Pre-commit will run 
configured checks at git commit time. To enable pre-commit on your local repository run:

```bash
$ poetry run pre-commit install
```

### Versioning

This project uses [semver](https://semver.org/) for versioning.

Please include a description what is added for each new version in `CHANGELOG.md`.

### Code Review

_Explain the code review process. Call out any details that are unique to the project._

This project uses the [Evergreen Commit Queue](https://github.com/evergreen-ci/evergreen/wiki/Commit-Queue#pr). 
Add a PR comment with `evergreen merge` to trigger a merge.

### Deployment

Deployment to production is automatically triggered on merges to master.

### Additional Documentation

_Links to more documentation for details not covered above. This refers to documentation
meant for contributors to the project._

## Resources

* [Evergreen REST Documentation](https://github.com/evergreen-ci/evergreen/wiki/REST-V2-Usage)
* [Synchronous evergreen client](https://github.com/evergreen-ci/evergreen.py)
