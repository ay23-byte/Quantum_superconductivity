window.HARTREE_PHASE_SIZE = {
  "summary": [
    {
      "L": 4,
      "phase_seeds": 1,
      "twist_step": 0.05,
      "mean_pairing": 0.3095288300861895,
      "sem_pairing": 0.036707751629409924,
      "mean_twist_curvature": 0.06203238800921439,
      "sem_twist_curvature": 0.1069140620203711,
      "max_density_residual": 4.890056773954043e-07,
      "samples": 4
    },
    {
      "L": 4,
      "phase_seeds": 4,
      "twist_step": 0.05,
      "mean_pairing": 0.3094418214911715,
      "sem_pairing": 0.0367460399326239,
      "mean_twist_curvature": 0.06203240414848209,
      "sem_twist_curvature": 0.10691405751084064,
      "max_density_residual": 4.4024975698331303e-07,
      "samples": 4
    },
    {
      "L": 6,
      "phase_seeds": 1,
      "twist_step": 0.05,
      "mean_pairing": 0.3495383592364871,
      "sem_pairing": 0.006381849783234849,
      "mean_twist_curvature": 0.30491765955673594,
      "sem_twist_curvature": 0.022779440559868306,
      "max_density_residual": 3.277333729956311e-07,
      "samples": 4
    },
    {
      "L": 6,
      "phase_seeds": 4,
      "twist_step": 0.05,
      "mean_pairing": 0.3494898823471141,
      "sem_pairing": 0.0063866563406392825,
      "mean_twist_curvature": 0.30491758940343056,
      "sem_twist_curvature": 0.0227794460779981,
      "max_density_residual": 2.148457654005398e-07,
      "samples": 4
    },
    {
      "L": 8,
      "phase_seeds": 1,
      "twist_step": 0.05,
      "mean_pairing": 0.3652345169467545,
      "sem_pairing": 0.0068338321858492776,
      "mean_twist_curvature": 0.4308991727668853,
      "sem_twist_curvature": 0.025771718458772467,
      "max_density_residual": 1.516574258397796e-07,
      "samples": 4
    },
    {
      "L": 8,
      "phase_seeds": 4,
      "twist_step": 0.05,
      "mean_pairing": 0.3652193563007955,
      "sem_pairing": 0.006833657480946287,
      "mean_twist_curvature": 0.4308990752463159,
      "sem_twist_curvature": 0.02577169405935446,
      "max_density_residual": 1.516574258397796e-07,
      "samples": 4
    },
    {
      "L": 10,
      "phase_seeds": 1,
      "twist_step": 0.05,
      "mean_pairing": 0.3497160332819637,
      "sem_pairing": 0.014736889111313026,
      "mean_twist_curvature": 0.4274929189193698,
      "sem_twist_curvature": 0.03379066000818975,
      "max_density_residual": 2.429282970339841e-07,
      "samples": 4
    }
  ],
  "phase_effects": [
    {
      "L": 4,
      "phase_seed_counts": [
        1,
        4
      ],
      "mean_curvature_change": 1.6139267700054916e-08,
      "sem_curvature_change": 1.1985985691854927e-08,
      "samples": 4
    },
    {
      "L": 6,
      "phase_seed_counts": [
        1,
        4
      ],
      "mean_curvature_change": -7.015330538706621e-08,
      "sem_curvature_change": 7.437166332975208e-09,
      "samples": 4
    },
    {
      "L": 8,
      "phase_seed_counts": [
        1,
        4
      ],
      "mean_curvature_change": -9.752056939760223e-08,
      "sem_curvature_change": 5.632942696469689e-08,
      "samples": 4
    }
  ],
  "metadata": {
    "run_id": "phase_size_validation_20261023",
    "python": "3.13.5 | packaged by Anaconda, Inc. | (main, Jun 12 2025, 16:37:03) [MSC v.1929 64 bit (AMD64)]",
    "platform": "Windows-11-10.0.26300-SP0",
    "numpy": "2.1.3",
    "scipy": "1.15.2",
    "parameters": {
      "L_values": [
        4,
        6,
        8,
        10
      ],
      "comparison_sizes": [
        4,
        6,
        8
      ],
      "extended_size_phase_seeds": 1,
      "realizations": 4,
      "phase_seed_counts": [
        1,
        4
      ],
      "twist_step": 0.05,
      "t": 1.0,
      "U": 2.2,
      "T": 0.08,
      "target_density": 0.87,
      "t_prime": 0.0,
      "W_uniform": 1.2,
      "disorder_distribution": "uniform[-W/2,W/2]",
      "seed_formula": "seed_base + 1000*L + realization_index",
      "seed_base": 826103,
      "pairing_tolerance": 2e-05,
      "density_tolerance": 0.0001,
      "mixing": 0.1,
      "Hartree_convention": "K_eff = K0 - mu*I - diag(U*n_i/2)"
    },
    "planned_calculations": 28,
    "successful_calculations": 28,
    "failed_calculations": 0,
    "complete": true,
    "max_density_residual": 4.890056773954043e-07,
    "caveats": [
      "Phase-start comparison is limited to four seeded disorder realizations and the selected point W/t=1.2, t'/t=0.",
      "The L=10 extension uses the one-start baseline and four realizations; it is an additional finite-size check, not an extrapolation.",
      "A finite set of starts does not prove the global mean-field free-energy minimum.",
      "Twist curvature is a finite-size mean-field response, not a BKT temperature or experimental transition temperature."
    ]
  }
};
