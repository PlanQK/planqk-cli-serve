planqk-cli-serve
==========

The "serve" command is used in the PlanQK Command Line Interface (CLI). Its purpose is to help users to test their services locally.

Once the project has been built, the container can be started with the docker run command. For a proper start, the directory of the project you want to run should be mounted under the path `/user_code`.

The following code snippet is an example of using the `docker run` command after navigating to the root directory of the project you want to execute:

```bash
docker run -p 8001:8001 -v "$(pwd):/user_code" <tag>
```

## License

Apache-2.0 | Copyright 2023 Anaqor AG
