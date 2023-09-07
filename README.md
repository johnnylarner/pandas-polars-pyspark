# ppp

This project contains the code for the pandas-polars-pyspark (PPP) experiment.

## Prerequisites
This project uses terraform to manage some aspects of its AWS resources.
Please follow the [Terraform install instructions](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli).

Validate your installation by running:

    terraform -help


In addition you'll also need AWS CLI installed locally. You can find the install docs [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

Validate your installation by running:

    aws --version

## Getting Started

To set up your local development environment, please run:

    poetry install

Behind the scenes, this creates a virtual environment and installs `ppp` along with its dependencies into a new virtualenv. Whenever you run `poetry run <command>`, that `<command>` is actually run inside the virtualenv managed by poetry.

You can now import functions and classes from the module with `import ppp`.


### Authenticating with AWS
To request credentials for our AWS user, please contact @johnnylarner. Once you have these, you can configure your credentials by running:

    aws configure


### Building the terraform stack
To update or build the terraform stack, run:

    terraform init && terraform apply

This will prompt you for use input

### Destroying the stack
To destory the stack, run:

    terraform destroy


### Running CLI scripts
We have several UNIX shell scripts in the `cli_scripts` folder.

Please make sure you `cd` into the directory before running any scripts:

    cd cli_scripts
    source deploy_image.sh
    source delete_images.sh

These scripts extract variables from our `terraform` stack. Any changes to the scripts should follow the same approach.

### Testing

We use `pytest` as test framework. To execute the tests, please run

    pytest tests

To run the tests with coverage information, please use

    pytest tests --cov=src --cov-report=html --cov-report=term

and have a look at the `htmlcov` folder, after the tests are done.

### Distribution Package

To build a distribution package (wheel), please use

    python setup.py bdist_wheel

this will clean up the build folder and then run the `bdist_wheel` command.

### Contributions

Before contributing, please set up the pre-commit hooks to reduce errors and ensure consistency

    pip install -U pre-commit
    pre-commit install

If you run into any issues, you can remove the hooks again with `pre-commit uninstall`.

## Contact

James Richardson (james.richardson.2556@gmail.com)

## License

© James Richardson
