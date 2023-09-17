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


This project relies on the OS NYC city taxi data set. As downloading the data is a one time step, we don't have a way of automating it.

Below are the specifications for which files need to be downloaded manually. Please save them in the `data` folder of your repository.

#### Yearly yellow cab data
For the years 2011-2013, [please download](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) the __Yellow Taxi Trip Records__ for each month.

#### Zone lookup table
Here the download link for the [zone lookup table](https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv).

## Getting Started

To set up your local development environment, please run:

    poetry install

Behind the scenes, this creates a virtual environment and installs `ppp` along with its dependencies into a new virtualenv. Whenever you run `poetry run <command>`, that `<command>` is actually run inside the virtualenv managed by poetry.

You can now import functions and classes from the module with `import ppp`.


### Partition your local data
Once you've downloaded the taxi data, you can partition by running:

    python scripts/partition_data.py

### Locally running scripts
You can test out the feature engineering script by running:

    python scripts/feature_engineering.py

By default this will run the script using local data. If you want to be explicit, you can run the script with the `local` argument:

    python scripts/feature_engineering.py local


### Running scripts with S3 data
You can also run the script using the the s3 argument to use the data on s3:

    python scripts/feature_engineering.py s3


### Authenticating with AWS
To request credentials for our AWS user, please contact @johnnylarner. Once you have these, you can configure your credentials by running:

    aws configure

### Building the terraform stack
To update or build the terraform stack, run:

    terraform init && terraform apply

This will prompt you for use input

### Destroying the stack
Terraform doesn't manage objects stored in S3 buckets or ECR repos. This means that these resources will only be destroyed if you empty them first. This is actually quite useful as we don't want to reupload everything each time we want to destory all our expensive ECS instances. If you _do_ want to delete _everything_, run the `delete_**.sh` scripts from the `cli_scripts` folder first.

To destory the stack, run:

    terraform destroy

### Running CLI scripts
We have several UNIX shell scripts in the `cli_scripts` folder. These scripts extract variables from our `terraform` stack. Any changes to the scripts should follow the same approach.

Please make sure you `cd` into the directory before running any scripts, as the terraform paths are hard coded.

Copy your locally downloaded data to the terraform bucket by running `update_data_folder.sh`.

You can push our app image via the `deploy_image.sh` script. You can then submit a batch job - defined in our terraform stack - via the `submit_batch.sh` script.


### Docker
When building our image, docker will default to the system build platform. This means that images built on MacOS M series devices will have an incompatible build for cloud environments. To address this, we parameterize the build using the build arg `BUILD_PLATFORM`.

There are two shell scripts that set this for the `local` and `cloud` builds.

When running `docker build` you can pass the argument `--build-arg PLATFORM=$BUILD_PLATFORM` to declare the build platform. For example:


    docker build -t ppp:latest --build-arg PLATFORM=$BUILD_PLATFORM  .


To run the container locally, mounting your AWS credentials as read-only, run:

    docker run -v $HOME/.aws/credentials:/app/.aws/credentials:ro  ppp


### Testing

We use `pytest` as test framework. To execute the tests, please run

    pytest tests

To run the tests with coverage information, please use

    pytest tests --cov=src --cov-report=html --cov-report=term

and have a look at the `htmlcov` folder, after the tests are done.

We use the `Moto` package to mock our `boto3` services. You can find the configuration of our mock s3 bucket in the `conftest.py` file. If you have IO dependent tests, you can try using the data made available over the `s3_data_uri` fixture.

If you need to create more data, you can either do it inline via the boto3 client from the `s3` fixture or create another fixutre similar to the `s3_data` fixture.

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
