# Boundaries Setup for MCMC initial conditions

# LB = Lower Bounds. | UB = Upper Bounds.
gamma_Young_LB, e_cut_Young_LB, eta_Young_LB = [1.1, 400, 0.001]
gamma_Young_UB, e_cut_Young_UB, eta_Young_UB = [2.6, 10000, 1.0]

## inital bounds. for Middle PWN
gamma_Middle_LB, e_cut_Middle_LB, eta_Middle_LB = [1.1, 10, 0.001]
gamma_Middle_UB, e_cut_Middle_UB, eta_Middle_UB = [2.6, 5000, 1.0]

## inital bounds. for Old PWN
gamma_Old_LB, e_cut_Old_LB, eta_Old_LB = [1.1, 1.0, 0.001]
gamma_Old_UB, e_cut_Old_UB, eta_Old_UB = [2.6, 1000, 1.0]
