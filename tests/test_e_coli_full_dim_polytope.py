#!/usr/bin/env python3
import os
import json
import numpy as np
from dingo.loading_models import read_json_file
from dingo.scaling import gmscale, apply_scaling, remove_almost_redundant_facets
from dingo.fva import slow_fva, fast_fva
from dingo.inner_ball import slow_inner_ball, fast_inner_ball
from dingo.nullspace import nullspace_sparse, nullspace_dense


current_directory = os.getcwd()
input_file_json = current_directory +  '/ext_data/e_coli_core.json'

e_coli_network = read_json_file(input_file_json)

lb = e_coli_network[0]
ub = e_coli_network[1]
S = e_coli_network[2]

fva_res = fast_fva(lb, ub, S)

A = fva_res[0]
b = fva_res[1]
Aeq = fva_res[2]
beq = fva_res[3]
min_fluxes = fva_res[4]
max_fluxes = fva_res[5]

print(A.shape[0], A.shape[1])
print(b.size)
print(Aeq.shape[0], Aeq.shape[1])
print(beq.size)
print(min_fluxes.size)
print(max_fluxes.size)

nullspace_res_sparse = nullspace_sparse(Aeq, beq)

N = nullspace_res_sparse[0]
N_shift = nullspace_res_sparse[1]

print(N.shape[0], N.shape[1])
print(N_shift.size)

product = np.dot(A, N_shift)
b = np.subtract(b, product)
A = np.dot(A, N)

print(A.shape[0], A.shape[1])
print(b.size)

res = remove_almost_redundant_facets(A, b)
A = res[0]
b = res[1]

print(A.shape[0], A.shape[1])
print(b.size)

res = gmscale(A, 0, 0.99)
res = apply_scaling(A, b, res[0], res[1])
A = res[0]
b = res[1]

res = remove_almost_redundant_facets(A, b)
A = res[0]
b = res[1]

print("shape of the matrix of the full dimensional polytope, A: \n", A.shape)
print("shape of the vector of the full dimensional polytope, b: \n", b.shape)

max_ball = slow_inner_ball(A, b)
print("The center point of the maximum inscribed ball:")
print(max_ball[0])
print("The radius of the maximum inscribed ball:")
print(max_ball[1])

