#!/usr/bin/env python
"""
An example of a step using MLflow and Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    logger.info("Creating wandb run")
    run = wandb.init(project='nyc_airbnb', job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################

    logger.info(f"Load data {args.input_artifact}")
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    sample = pd.read_csv(artifact_local_path)

    logger.info(f"Cleaning data using price column")
    clean_sample = sample[sample["price"].between(args.min_price, args.max_price)]
    
    logger.info("Cleaning data using lat and long columns") 
    
    idx = clean_sample['longitude'].between(-74.25, -73.50) & clean_sample['latitude'].between(40.5, 41.2)
    clean_sample = clean_sample[idx].copy()

    logger.info(f"Save cleaning data in {args.output_artifact}")
    clean_sample.to_csv(args.output_artifact, index=False)

    logger.info("Creating artifact")
    artifact = wandb.Artifact(
        name=args.output_artifact,
        type=args.output_type,
        description=args.output_description
    )

    logger.info(f"Add {args.output_artifact}")
    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Add parameters basic_cleaning")


    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Name of the input data file.",
        required=True
    )

    parser.add_argument(
            "--output_artifact",
            type=str,
            help="Name of the output data file.",
            required=True
        )

    parser.add_argument(
        "--output_type",
        type=str,
        help="Type of the output data file.",
        required=True
    )

    parser.add_argument(
            "--output_description",
            type=str,
            help="Description of the output data file.",
            required=True
        )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Min of price acceptable",
        required=True
    )

    parser.add_argument(
         "--max_price",
          type=float,
          help="Max of price acceptable",
          required=True
        )

    args = parser.parse_args()

    go(args)
