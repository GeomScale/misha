# dingo : a python library for metabolic networks sampling and analysis
# dingo is part of GeomScale project

# Copyright (c) 2021 Apostolos Chalkis
# Copyright (c) 2021 Haris Zafeiropoulos

# Licensed under GNU LGPL.3, see LICENCE file

import argparse


def dingo_args():
    parser = argparse.ArgumentParser()

    parser = argparse.ArgumentParser(
        description="a parser to read the inputs of dingo package \
         dingo is a Python library for the analysis of \
         metabolic networks developed by the \
         GeomScale group - https://geomscale.github.io/ ",
        usage="%(prog)s [--help | -h] : help \n\n \
         The default method is to generate uniformly distributed steady states of the given model:\n\
            1. provide just your metabolic model: \n \
           python -m dingo -i path_to_my_model \n\n \
           2. or ask for more: \n \
           python -m dingo -i path_to_my_model -n 2000 -s gurobi \n \
         \n\n\
         You could give a full dimensional polytope derived from a model by dingo and saved to a `pickle` file:\n\
            python -m dingo -poly path_to_pickle_file -n 1000 \n \
         \n\n \
         You could ask for FVA or FBA methods:\n \
           python -m dingo -i path_to_my_model -fva True\n \
         \n\n\
         We recommend to use gurobi library for more stable and fast computations.",
    )

    parser._action_groups.pop()

    required = parser.add_argument_group("required arguments")

    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "--metabolic_network",
        "-i",
        help="the path to a metabolic network as a .json or a .mat file.",
        required=False,
        default=None,
        metavar="",
    )

    optional.add_argument(
        "--unbiased_analysis",
        "-unbiased",
        help="a boolean flag to ignore the objective function in preprocessing. Multiphase Monte Carlo Sampling algorithm will sample steady states but not restricted to optimal solutions. The default value is False.",
        required=False,
        default=False,
        metavar="",
    )

    optional.add_argument(
        "--polytope",
        "-poly",
        help="the path to a pickle file generated by dingo that contains a full dimensional polytope derived from a model. This file could be used to sample more steady states of a preprocessed metabolic network.",
        required=False,
        default=None,
        metavar="",
    )

    optional.add_argument(
        "--model_name",
        "-name",
        help="The name of the input model.",
        required=False,
        default=None,
        metavar="",
    )

    optional.add_argument(
        "--histogram",
        "-hist",
        help="A boolean flag to request a histogram for a certain reaction flux.",
        required=False,
        default=False,
        metavar="",
    )

    optional.add_argument(
        "--steady_states",
        "-st",
        help="A path to a pickle file tha was generated by dingo and contains steady states of a model.",
        required=False,
        default=None,
        metavar="",
    )

    optional.add_argument(
        "--metabolites_reactions",
        "-mr",
        help="A path to a pickle file tha was generated by dingo and contains the names of the metabolites and the reactions of a model.",
        required=False,
        default=None,
        metavar="",
    )

    optional.add_argument(
        "--n_bins",
        "-bins",
        help="The number of bins if a histogram is requested. The default value is 40.",
        required=False,
        default=40,
        metavar="",
    )

    optional.add_argument(
        "--reaction_index",
        "-reaction_id",
        help="The index of the reaction to plot the histogram of its fluxes. The default value is 1.",
        required=False,
        default=1,
        metavar="",
    )

    optional.add_argument(
        "--fva",
        "-fva",
        help="a boolean flag to request FVA method. The default value is False.",
        required=False,
        default=False,
        metavar="",
    )

    optional.add_argument(
        "--opt_percentage",
        "-opt",
        help="consider solutions that give you at least a certain percentage of the optimal solution in FVA method. The default is to consider optimal solutions only.",
        required=False,
        default=100,
        metavar="",
    )

    optional.add_argument(
        "--fba",
        "-fba",
        help="a boolean flag to request FBA method. The default value is False.",
        required=False,
        default=False,
        metavar="",
    )

    optional.add_argument(
        "--preprocess_only",
        "-preprocess",
        help="perform only preprocess to compute the full dimensional polytope from a model.",
        required=False,
        default=False,
        metavar="",
    )

    optional.add_argument(
        "--effective_sample_size",
        "-n",
        help="the minimum effective sample size per marginal of the sample that the Multiphase Monte Carlo Sampling algorithm will return. The default value is 1000.",
        required=False,
        default=1000,
        metavar="",
    )

    optional.add_argument(
        "--output_directory",
        "-o",
        help="the output directory for the dingo output",
        required=False,
        metavar="",
    )

    optional.add_argument(
        "--nullspace",
        "-null",
        help="the method to compute the right nullspace of the stoichiometric matrix. Choose between `sparseQR` and `scipy`. The default method is `sparseQR`.",
        required=False,
        default="sparseQR",
        metavar="",
    )

    optional.add_argument(
        "--psrf_check",
        "-psrf",
        help="a boolean flag to request psrf < 1.1 for each marginal of the sample that the Multiphase Monte Carlo Sampling algorithm will return. The default value is `False`.",
        required=False,
        default=False,
        metavar="",
    )

    optional.add_argument(
        "--parallel_mmcs",
        "-pmmcs",
        help="a boolean flag to request sampling with parallel Multiphase Monte Carlo Sampling algorithm. The default value is `false`.",
        required=False,
        default=False,
        metavar="",
    )

    optional.add_argument(
        "--num_threads",
        "-nt",
        help="the number of threads to be used in parallel Multiphase Monte Carlo Sampling algorithm. The default number is 2.",
        required=False,
        default=2,
        metavar="",
    )

    optional.add_argument(
        "--distribution",
        "-d",
        help="the distribution to sample from the flux space of the metabolic network. Choose among `uniform`, `gaussian` and `exponential` distribution. The default value is `uniform`.",
        required=False,
        default="uniform",
        metavar="",
    )

    optional.add_argument(
        "--solver",
        "-s",
        help="the solver to use for the linear programs. Choose between `scipy` and `gurobi` (faster computations --- it needs a licence). The default value is `scipy`.",
        required=False,
        default="scipy",
        metavar="",
    )

    args = parser.parse_args()
    return args
