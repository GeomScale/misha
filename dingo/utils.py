# dingo : a python library for metabolic networks sampling and analysis
# dingo is part of GeomScale project

# Copyright (c) 2021 Apostolos Chalkis

# Licensed under GNU LGPL.3, see LICENCE file

import numpy as np
import math
import scipy.sparse as sp
import matplotlib.pyplot as plt
from scipy.sparse import diags
from dingo.scaling import gmscale
from dingo.nullspace import nullspace_dense, nullspace_sparse


def apply_scaling(A, b, cs, rs):
    """A Python function to apply the scaling computed by the function `gmscale` to a convex polytope

    Keyword arguments:
    A -- an mxn matrix that contains the normal vectors of the facets of the polytope row-wise
    b -- a m-dimensional vector
    cs -- a scaling vector for the matrix A
    rs -- a scaling vector for the vector b
    """

    m = rs.shape[0]
    n = cs.shape[0]
    r_diagonal_matrix = diags(1 / rs, shape=(m, m)).toarray()
    c_diagonal_matrix = diags(1 / cs, shape=(n, n)).toarray()

    new_A = np.dot(r_diagonal_matrix, np.dot(A, c_diagonal_matrix))
    new_b = np.dot(r_diagonal_matrix, b)

    return new_A, new_b, c_diagonal_matrix


def remove_almost_redundant_facets(A, b):
    """A Python function to remove the facets of a polytope with norm smaller than 1e-06

    Keyword arguments:
    A -- an mxn matrix that contains the normal vectors of the facets of the polytope row-wise
    b -- a m-dimensional vector
    """

    new_A = []
    new_b = []

    for i in range(A.shape[0]):
        entry = np.linalg.norm(
            A[
                i,
            ]
        )
        if entry < 1e-06:
            continue
        else:
            new_A.append(A[i, :])
            new_b.append(b[i])

    new_A = np.array(new_A)
    new_b = np.array(new_b)

    return new_A, new_b


# Map the points samples on the (rounded) full dimensional polytope, back to the initial one to obtain the steady states of the metabolic network
def map_samples_to_steady_states(samples, N, N_shift, T=None, T_shift=None):
    """A Python function to map back to the initial space the sampled points from a full dimensional polytope derived by two
    linear transformation of a low dimensional polytope, to obtain the steady states of the metabolic network

    Keyword arguments:
    samples -- an nxN matrix that contains sample points column-wise
    N, N_shift -- the matrix and the vector of the linear transformation applied on the low dimensional polytope to derive the full dimensional polytope
    T, T_shift -- the matrix and the vector of the linear transformation applied on the full dimensional polytope
    """

    extra_2 = np.full((samples.shape[1], N.shape[0]), N_shift)
    if T is None or T_shift is None:
        steady_states = N.dot(samples) + extra_2.T
    else:
        extra_1 = np.full((samples.shape[1], samples.shape[0]), T_shift)
        steady_states = N.dot(T.dot(samples) + extra_1.T) + extra_2.T

    return steady_states


def get_matrices_of_low_dim_polytope(S, lb, ub, min_fluxes, max_fluxes):
    """A Python function to derive the matrices A, Aeq and the vectors b, beq of the low dimensional polytope,
    such that A*x <= b and Aeq*x = beq.

    Keyword arguments:
    samples -- an nxN matrix that contains sample points column-wise
    S -- the stoichiometric matrix
    lb -- lower bounds for the fluxes, i.e., a n-dimensional vector
    ub -- upper bounds for the fluxes, i.e., a n-dimensional vector
    min_fluxes -- minimum values of the fluxes, i.e., a n-dimensional vector
    max_fluxes -- maximum values for the fluxes, i.e., a n-dimensional vector
    """

    n = S.shape[1]
    m = S.shape[0]
    beq = np.zeros(m)
    Aeq = S

    A = np.zeros((2 * n, n), dtype="float")
    A[0:n] = np.eye(n)
    A[n:] -= np.eye(n, n, dtype="float")

    b = np.concatenate((ub, -lb), axis=0)
    b = np.asarray(b, dtype="float")
    b = np.ascontiguousarray(b, dtype="float")

    for i in range(n):

        width = abs(max_fluxes[i] - min_fluxes[i])

        # Check whether we keep or not the equality
        if width < 1e-07:
            Aeq = np.vstack(
                (
                    Aeq,
                    A[
                        i,
                    ],
                )
            )
            beq = np.append(beq, min(max_fluxes[i], min_fluxes[i]))

    return A, b, Aeq, beq


def get_matrices_of_full_dim_polytope(A, b, Aeq, beq):
    """A Python function to derive the matrix A and the vector b of the full dimensional polytope,
    such that Ax <= b given a low dimensional polytope.

    Keyword arguments:
    A -- an mxn matrix that contains the normal vectors of the facets of the polytope row-wise
    b -- a m-dimensional vector, s.t. A*x <= b
    Aeq -- an kxn matrix that contains the normal vectors of hyperplanes row-wise
    beq -- a k-dimensional vector, s.t. Aeq*x = beq
    """

    nullspace_res = nullspace_sparse(Aeq, beq)
    N = nullspace_res[0]
    N_shift = nullspace_res[1]

    if A.shape[1] != N.shape[0] or N.shape[0] != N_shift.size or N.shape[1] <= 1:
        raise Exception(
            "The computation of the matrix of the right nullspace of the stoichiometric matrix failed."
        )

    product = np.dot(A, N_shift)
    b = np.subtract(b, product)
    A = np.dot(A, N)

    res = remove_almost_redundant_facets(A, b)
    A = res[0]
    b = res[1]

    try:
        res = gmscale(A, 0.99)
        res = apply_scaling(A, b, res[0], res[1])
        A = res[0]
        b = res[1]
        N = np.dot(N, res[2])

        res = remove_almost_redundant_facets(A, b)
        A = res[0]
        b = res[1]
    except:
        print("gmscale failed to compute a good scaling.")

    return A, b, N, N_shift


def plot_histogram(reaction_fluxes, reaction, n_bins=40):
    """A Python function to plot the histogram of a certain reaction flux.

    Keyword arguments:
    reaction_fluxes -- a vector that contains sampled fluxes of a reaction
    reaction -- a string with the name of the reacion
    n_bins -- the number of bins for the histogram
    """

    plt.figure(figsize=(7, 7))

    n, bins, patches = plt.hist(
        reaction_fluxes, bins=n_bins, density=False, facecolor="red", ec="black"
    )

    plt.xlabel("Flux (mmol/gDW/h)", fontsize=16)
    plt.ylabel("Frequency (#samples: " + str(reaction_fluxes.size) + ")", fontsize=14)
    plt.grid(True)
    plt.title("Reaction: " + reaction, fontweight="bold", fontsize=18)
    plt.axis([np.amin(reaction_fluxes), np.amax(reaction_fluxes), 0, np.amax(n) * 1.2])

    plt.show()
