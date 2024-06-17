# PROJECT MOVED TO GITLAB

**NOTICE:** This project is no longer maintained on GitHub. It has been moved to GitLab for continued updates and development. You can find the latest version of this project at [https://gitlab.com/planqk-foss/planqk-cli-serve](https://gitlab.com/planqk-foss/planqk-cli-serve).

---

# planqk-cli-serve

This project is the baseline for the PlanQK CLI command `serve`.

It runs a PlanQK project directory in a containerized environment to expose it through a local web server, similarly to how the PlanQK Platform would run the code.
The local web server exposes the same RESTful HTTP endpoints to start a service execution, to check the status of running executions, to cancel executions, and to retrieve execution results.

## Usage

The container expects the project directory to be used mounted under the path `/user_code`.

Build the container image:

```bash
docker build -t planqk-cli-serve .
```

Once the container image has been built, start it with the following command:

```bash
docker run -it -e PORT=8000 -p 8000:8000 -v "$(pwd):/user_code" planqk-cli-serve standalone
```

## Development

We use FastAPI, to run the service locally, you can use the following command:

```bash
uvicorn src.app:app --reload
```

By default, the `user_code_runner` tries to execute the supplied test directory `user_code`.
The implementation therein is the bare minimum a service needs to provide.
In this case, the logic simply prints/logs the input data and params and returns it as is wrapped in a dictionary.

## License

Apache-2.0 | Copyright 2023-2024 Anaqor AG
