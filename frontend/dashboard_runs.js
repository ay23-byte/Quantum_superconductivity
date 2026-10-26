window.QUANTUM_RUNS = [
  {
    "id": "quick_20261023",
    "scan": [
      {
        "t_prime": 0.0,
        "W_uniform": 0.0,
        "mean_pairing": 0.35870478040558434,
        "sample_sd_pairing": "0.0",
        "mean_spatial_std": 2.3894167330183194e-16,
        "sample_sd_spatial_std": "0.0",
        "converged_samples": 3,
        "samples": 3,
        "sem_pairing": 0.0,
        "sem_spatial_std": "0.0"
      },
      {
        "t_prime": 0.0,
        "W_uniform": 0.6,
        "mean_pairing": 0.36828666258340803,
        "sample_sd_pairing": "0.030726902187517564",
        "mean_spatial_std": 0.02644166437645121,
        "sample_sd_spatial_std": "0.004675278105009129",
        "converged_samples": 3,
        "samples": 3,
        "sem_pairing": 0.01774018524932657,
        "sem_spatial_std": "0.002699273072463384"
      },
      {
        "t_prime": 0.0,
        "W_uniform": 1.2,
        "mean_pairing": 0.4018939756646398,
        "sample_sd_pairing": "0.02937166381274525",
        "mean_spatial_std": 0.04828313986853746,
        "sample_sd_spatial_std": "0.00757179752026303",
        "converged_samples": 3,
        "samples": 3,
        "sem_pairing": 0.01695773800883566,
        "sem_spatial_std": "0.004371579336573201"
      },
      {
        "t_prime": 0.2,
        "W_uniform": 0.0,
        "mean_pairing": 0.32002547828420436,
        "sample_sd_pairing": "0.0",
        "mean_spatial_std": 2.532036096237387e-16,
        "sample_sd_spatial_std": "0.0",
        "converged_samples": 3,
        "samples": 3,
        "sem_pairing": 0.0,
        "sem_spatial_std": "0.0"
      },
      {
        "t_prime": 0.2,
        "W_uniform": 0.6,
        "mean_pairing": 0.31669322236516856,
        "sample_sd_pairing": "0.01139521246844502",
        "mean_spatial_std": 0.027131524232872767,
        "sample_sd_spatial_std": "0.0035782799913658837",
        "converged_samples": 3,
        "samples": 3,
        "sem_pairing": 0.006579028986129713,
        "sem_spatial_std": "0.0020659209162509446"
      },
      {
        "t_prime": 0.2,
        "W_uniform": 1.2,
        "mean_pairing": 0.3329042970577723,
        "sample_sd_pairing": "0.01855389540918802",
        "mean_spatial_std": 0.052134771491379135,
        "sample_sd_spatial_std": "0.0068728852514987355",
        "converged_samples": 3,
        "samples": 3,
        "sem_pairing": 0.010712096509010866,
        "sem_spatial_std": "0.003968062150062204"
      }
    ],
    "metadata": {
      "run_id": "quick_20261023",
      "timestamp_local": "2026-10-23",
      "python": "3.13.5 | packaged by Anaconda, Inc. | (main, Jun 12 2025, 16:37:03) [MSC v.1929 64 bit (AMD64)]",
      "platform": "Windows-11-10.0.26300-SP0",
      "numpy": "2.1.3",
      "scipy": "1.15.2",
      "matplotlib": "3.10.6",
      "pandas": "2.2.3",
      "parameters": {
        "L": 6,
        "t": 1.0,
        "mu": -0.5,
        "U": 2.2,
        "T": 0.08,
        "uniform_W_values": [
          0.0,
          0.6,
          1.2
        ],
        "tprime_values": [
          0.0,
          0.2
        ],
        "disorder_distribution": "uniform[-W/2,W/2]",
        "seed_base": 94721,
        "realizations_per_pair": 3,
        "tolerance": 2e-06,
        "mixing": 0.55
      },
      "clean_validation": {
        "reference_gap": 0.34616927167295836,
        "bdg_mean_gap": 0.3461692716729582,
        "spatial_std": 2.618455766672135e-16,
        "absolute_difference": 1.6653345369377348e-16,
        "converged": true,
        "iterations": 1
      },
      "finite_size": [
        {
          "L": 4,
          "N_sites": 16,
          "reference_gap": 0.34616927167295836,
          "bdg_mean_gap": 0.3461692716729582,
          "spatial_std": 2.618455766672135e-16,
          "converged": true
        },
        {
          "L": 6,
          "N_sites": 36,
          "reference_gap": 0.35871055826850656,
          "bdg_mean_gap": 0.3587105582685066,
          "spatial_std": 2.2850404966761176e-16,
          "converged": true
        },
        {
          "L": 8,
          "N_sites": 64,
          "reference_gap": 0.3760504819590624,
          "bdg_mean_gap": 0.3760504819590622,
          "spatial_std": 2.0572386961145153e-16,
          "converged": true
        }
      ],
      "all_scan_samples_converged": true,
      "sample_count": 18,
      "dos_broadening_eta": 0.06,
      "dos_convention": "spin-resolved electron DOS; Gaussian broadening"
    },
    "figures": [
      "bdg_spectrum",
      "convergence_residual",
      "disorder_map",
      "dispersion",
      "dos_clean_disordered",
      "finite_size_comparison",
      "gap_map",
      "gap_vs_interaction",
      "gap_vs_temperature",
      "hopping_disorder_heatmap",
      "inhomogeneity_vs_disorder_tp0",
      "inhomogeneity_vs_disorder_tp0.2",
      "mean_gap_vs_disorder_tp0",
      "mean_gap_vs_disorder_tp0.2"
    ]
  },
  {
    "id": "research_20261023",
    "scan": [
      {
        "t_prime": 0.0,
        "W_uniform": 0.0,
        "mean_pairing": 0.3587047804055844,
        "sample_sd_pairing": "0.0",
        "mean_spatial_std": 2.6272439147327565e-16,
        "sample_sd_spatial_std": "9.792589172893483e-18",
        "converged_samples": 20,
        "samples": 20,
        "sem_pairing": 0.0,
        "sem_spatial_std": "2.189689506631827e-18"
      },
      {
        "t_prime": 0.0,
        "W_uniform": 0.6,
        "mean_pairing": 0.3696044346724472,
        "sample_sd_pairing": "0.018133509161681716",
        "mean_spatial_std": 0.02538451318591462,
        "sample_sd_spatial_std": "0.0032303013342222676",
        "converged_samples": 20,
        "samples": 20,
        "sem_pairing": 0.004054775915613554,
        "sem_spatial_std": "0.0007223173371129258"
      },
      {
        "t_prime": 0.0,
        "W_uniform": 1.2,
        "mean_pairing": 0.3779619884064517,
        "sample_sd_pairing": "0.02190807096029743",
        "mean_spatial_std": 0.04751571241952159,
        "sample_sd_spatial_std": "0.005613680964321822",
        "converged_samples": 20,
        "samples": 20,
        "sem_pairing": 0.004898793592311415,
        "sem_spatial_std": "0.0012552572240220165"
      },
      {
        "t_prime": 0.2,
        "W_uniform": 0.0,
        "mean_pairing": 0.32002547828420436,
        "sample_sd_pairing": "0.0",
        "mean_spatial_std": 3.2473891677161724e-16,
        "sample_sd_spatial_std": "0.0",
        "converged_samples": 20,
        "samples": 20,
        "sem_pairing": 0.0,
        "sem_spatial_std": "0.0"
      },
      {
        "t_prime": 0.2,
        "W_uniform": 0.6,
        "mean_pairing": 0.3199091050287172,
        "sample_sd_pairing": "0.005668051217026425",
        "mean_spatial_std": 0.027238432573014854,
        "sample_sd_spatial_std": "0.003375386857021205",
        "converged_samples": 20,
        "samples": 20,
        "sem_pairing": 0.00126741478212215,
        "sem_spatial_std": "0.0007547594462658778"
      },
      {
        "t_prime": 0.2,
        "W_uniform": 1.2,
        "mean_pairing": 0.31854840194216294,
        "sample_sd_pairing": "0.011783768112216536",
        "mean_spatial_std": 0.054477809621852044,
        "sample_sd_spatial_std": "0.004395607853862547",
        "converged_samples": 20,
        "samples": 20,
        "sem_pairing": 0.0026349306530010544,
        "sem_spatial_std": "0.0009828877963668616"
      }
    ],
    "metadata": {
      "run_id": "research_20261023",
      "timestamp_local": "2026-10-23",
      "python": "3.11.17 | packaged by Anaconda, Inc. | (main, Oct  1 2026, 20:16:54) [MSC v.1942 64 bit (AMD64)]",
      "platform": "Windows-10-10.0.26300-SP0",
      "numpy": "2.4.6",
      "scipy": "1.17.1",
      "matplotlib": "3.11.2",
      "pandas": "3.1.0",
      "parameters": {
        "L": 6,
        "t": 1.0,
        "mu": -0.5,
        "U": 2.2,
        "T": 0.08,
        "uniform_W_values": [
          0.0,
          0.6,
          1.2
        ],
        "tprime_values": [
          0.0,
          0.2
        ],
        "disorder_distribution": "uniform[-W/2,W/2]",
        "disorder_seed_formula": "seed_base + round(100*W) + realization_index",
        "seed_base": 94721,
        "realizations_per_pair": 20,
        "finite_size_disorder_realizations": 10,
        "tolerance": 2e-06,
        "mixing": 0.55
      },
      "clean_validation": {
        "reference_gap": 0.34616927167295836,
        "bdg_mean_gap": 0.34616927167295847,
        "spatial_std": 2.3263411494723067e-16,
        "absolute_difference": 1.1102230246251565e-16,
        "converged": true,
        "iterations": 1
      },
      "clean_limit_crosschecks": [
        {
          "L": 4,
          "U_over_t": 1.5,
          "T_over_t": 0.05,
          "reference_gap": 0.0,
          "bdg_mean_gap": 0.0,
          "absolute_difference": 0.0,
          "converged": true
        },
        {
          "L": 4,
          "U_over_t": 1.5,
          "T_over_t": 0.12,
          "reference_gap": 0.0,
          "bdg_mean_gap": 0.0,
          "absolute_difference": 0.0,
          "converged": true
        },
        {
          "L": 4,
          "U_over_t": 2.2,
          "T_over_t": 0.05,
          "reference_gap": 0.34717318604465536,
          "bdg_mean_gap": 0.34717318604465575,
          "absolute_difference": 3.885780586188048e-16,
          "converged": true
        },
        {
          "L": 4,
          "U_over_t": 2.2,
          "T_over_t": 0.12,
          "reference_gap": 0.33352063677524585,
          "bdg_mean_gap": 0.3335206367752458,
          "absolute_difference": 5.551115123125783e-17,
          "converged": true
        },
        {
          "L": 4,
          "U_over_t": 3.0,
          "T_over_t": 0.05,
          "reference_gap": 0.8103302630611481,
          "bdg_mean_gap": 0.8103302630611482,
          "absolute_difference": 1.1102230246251565e-16,
          "converged": true
        },
        {
          "L": 4,
          "U_over_t": 3.0,
          "T_over_t": 0.12,
          "reference_gap": 0.8096311764150765,
          "bdg_mean_gap": 0.8096311764150768,
          "absolute_difference": 2.220446049250313e-16,
          "converged": true
        }
      ],
      "finite_size_clean": [
        {
          "L": 4,
          "N_sites": 16,
          "reference_gap": 0.34616927167295836,
          "bdg_mean_gap": 0.34616927167295847,
          "spatial_std": 2.3263411494723067e-16,
          "converged": true
        },
        {
          "L": 6,
          "N_sites": 36,
          "reference_gap": 0.35871055826850656,
          "bdg_mean_gap": 0.3587105582685067,
          "spatial_std": 2.6894119993512124e-16,
          "converged": true
        },
        {
          "L": 8,
          "N_sites": 64,
          "reference_gap": 0.3760504819590624,
          "bdg_mean_gap": 0.3760504819590623,
          "spatial_std": 2.128555894067847e-16,
          "converged": true
        }
      ],
      "finite_size_disorder": [
        {
          "L": 4,
          "mean_pairing": 0.3689800230463649,
          "sample_sd_pairing": 0.07015026827768743,
          "mean_spatial_std": 0.06974132940376908,
          "sample_sd_spatial_std": 0.018533097121100826,
          "samples": 10,
          "converged_samples": 10,
          "sem_pairing": 0.022183462622934948,
          "sem_spatial_std": 0.005860679899978804
        },
        {
          "L": 6,
          "mean_pairing": 0.3868718323955611,
          "sample_sd_pairing": 0.02147983173145277,
          "mean_spatial_std": 0.04931196806079603,
          "sample_sd_spatial_std": 0.005016136443842122,
          "samples": 10,
          "converged_samples": 10,
          "sem_pairing": 0.006792519202854897,
          "sem_spatial_std": 0.00158624162167184
        },
        {
          "L": 8,
          "mean_pairing": 0.3786774455134115,
          "sample_sd_pairing": 0.014064681930703784,
          "mean_spatial_std": 0.04281805189834191,
          "sample_sd_spatial_std": 0.003363546720349941,
          "samples": 10,
          "converged_samples": 10,
          "sem_pairing": 0.004447642946683844,
          "sem_spatial_std": 0.0010636468652695237
        }
      ],
      "all_scan_samples_converged": true,
      "all_finite_size_disorder_converged": true,
      "all_clean_crosschecks_converged": true,
      "sample_count": 120,
      "unique_solver_runs": 140,
      "all_unique_runs_converged": true,
      "dos_broadening_eta": 0.06,
      "dos_convention": "spin-resolved electron DOS; Gaussian broadening"
    },
    "figures": [
      "bdg_spectrum",
      "convergence_residual",
      "disorder_map",
      "dispersion",
      "dos_clean_disordered",
      "finite_size_comparison",
      "finite_size_disorder_comparison",
      "gap_map",
      "gap_vs_interaction",
      "gap_vs_temperature",
      "hopping_disorder_heatmap",
      "inhomogeneity_vs_disorder_tp0",
      "inhomogeneity_vs_disorder_tp0.2",
      "mean_gap_vs_disorder_tp0",
      "mean_gap_vs_disorder_tp0.2"
    ]
  },
  {
    "id": "user_simulation_20261023",
    "scan": [
      {
        "t_prime": 0.0,
        "W_uniform": 0.0,
        "mean_pairing": 0.3587047804055844,
        "sample_sd_pairing": "0.0",
        "mean_spatial_std": 2.6272439147327565e-16,
        "sample_sd_spatial_std": "9.792589172893483e-18",
        "converged_samples": 20,
        "samples": 20,
        "sem_pairing": 0.0,
        "sem_spatial_std": "2.189689506631827e-18"
      },
      {
        "t_prime": 0.0,
        "W_uniform": 0.6,
        "mean_pairing": 0.3696044346724472,
        "sample_sd_pairing": "0.018133509161681716",
        "mean_spatial_std": 0.02538451318591462,
        "sample_sd_spatial_std": "0.0032303013342222676",
        "converged_samples": 20,
        "samples": 20,
        "sem_pairing": 0.004054775915613554,
        "sem_spatial_std": "0.0007223173371129258"
      },
      {
        "t_prime": 0.0,
        "W_uniform": 1.2,
        "mean_pairing": 0.3779619884064517,
        "sample_sd_pairing": "0.02190807096029743",
        "mean_spatial_std": 0.04751571241952159,
        "sample_sd_spatial_std": "0.005613680964321822",
        "converged_samples": 20,
        "samples": 20,
        "sem_pairing": 0.004898793592311415,
        "sem_spatial_std": "0.0012552572240220165"
      },
      {
        "t_prime": 0.2,
        "W_uniform": 0.0,
        "mean_pairing": 0.32002547828420436,
        "sample_sd_pairing": "0.0",
        "mean_spatial_std": 3.2473891677161724e-16,
        "sample_sd_spatial_std": "0.0",
        "converged_samples": 20,
        "samples": 20,
        "sem_pairing": 0.0,
        "sem_spatial_std": "0.0"
      },
      {
        "t_prime": 0.2,
        "W_uniform": 0.6,
        "mean_pairing": 0.3199091050287172,
        "sample_sd_pairing": "0.005668051217026425",
        "mean_spatial_std": 0.027238432573014854,
        "sample_sd_spatial_std": "0.003375386857021205",
        "converged_samples": 20,
        "samples": 20,
        "sem_pairing": 0.00126741478212215,
        "sem_spatial_std": "0.0007547594462658778"
      },
      {
        "t_prime": 0.2,
        "W_uniform": 1.2,
        "mean_pairing": 0.31854840194216294,
        "sample_sd_pairing": "0.011783768112216536",
        "mean_spatial_std": 0.054477809621852044,
        "sample_sd_spatial_std": "0.004395607853862547",
        "converged_samples": 20,
        "samples": 20,
        "sem_pairing": 0.0026349306530010544,
        "sem_spatial_std": "0.0009828877963668616"
      }
    ],
    "metadata": {
      "run_id": "user_simulation_20261023",
      "timestamp_local": "2026-10-23",
      "python": "3.11.17 | packaged by Anaconda, Inc. | (main, Oct  1 2026, 20:16:54) [MSC v.1942 64 bit (AMD64)]",
      "platform": "Windows-10-10.0.26300-SP0",
      "numpy": "2.4.6",
      "scipy": "1.17.1",
      "matplotlib": "3.11.2",
      "pandas": "3.1.0",
      "parameters": {
        "L": 6,
        "t": 1.0,
        "mu": -0.5,
        "U": 2.2,
        "T": 0.08,
        "uniform_W_values": [
          0.0,
          0.6,
          1.2
        ],
        "tprime_values": [
          0.0,
          0.2
        ],
        "disorder_distribution": "uniform[-W/2,W/2]",
        "disorder_seed_formula": "seed_base + round(100*W) + realization_index",
        "seed_base": 94721,
        "realizations_per_pair": 20,
        "finite_size_disorder_realizations": 10,
        "tolerance": 2e-06,
        "mixing": 0.55
      },
      "clean_validation": {
        "reference_gap": 0.34616927167295836,
        "bdg_mean_gap": 0.34616927167295847,
        "spatial_std": 2.3263411494723067e-16,
        "absolute_difference": 1.1102230246251565e-16,
        "converged": true,
        "iterations": 1
      },
      "clean_limit_crosschecks": [
        {
          "L": 4,
          "U_over_t": 1.5,
          "T_over_t": 0.05,
          "reference_gap": 0.0,
          "bdg_mean_gap": 0.0,
          "absolute_difference": 0.0,
          "converged": true
        },
        {
          "L": 4,
          "U_over_t": 1.5,
          "T_over_t": 0.12,
          "reference_gap": 0.0,
          "bdg_mean_gap": 0.0,
          "absolute_difference": 0.0,
          "converged": true
        },
        {
          "L": 4,
          "U_over_t": 2.2,
          "T_over_t": 0.05,
          "reference_gap": 0.34717318604465536,
          "bdg_mean_gap": 0.34717318604465575,
          "absolute_difference": 3.885780586188048e-16,
          "converged": true
        },
        {
          "L": 4,
          "U_over_t": 2.2,
          "T_over_t": 0.12,
          "reference_gap": 0.33352063677524585,
          "bdg_mean_gap": 0.3335206367752458,
          "absolute_difference": 5.551115123125783e-17,
          "converged": true
        },
        {
          "L": 4,
          "U_over_t": 3.0,
          "T_over_t": 0.05,
          "reference_gap": 0.8103302630611481,
          "bdg_mean_gap": 0.8103302630611482,
          "absolute_difference": 1.1102230246251565e-16,
          "converged": true
        },
        {
          "L": 4,
          "U_over_t": 3.0,
          "T_over_t": 0.12,
          "reference_gap": 0.8096311764150765,
          "bdg_mean_gap": 0.8096311764150768,
          "absolute_difference": 2.220446049250313e-16,
          "converged": true
        }
      ],
      "finite_size_clean": [
        {
          "L": 4,
          "N_sites": 16,
          "reference_gap": 0.34616927167295836,
          "bdg_mean_gap": 0.34616927167295847,
          "spatial_std": 2.3263411494723067e-16,
          "converged": true
        },
        {
          "L": 6,
          "N_sites": 36,
          "reference_gap": 0.35871055826850656,
          "bdg_mean_gap": 0.3587105582685066,
          "spatial_std": 2.0248681091331313e-16,
          "converged": true
        },
        {
          "L": 8,
          "N_sites": 64,
          "reference_gap": 0.3760504819590624,
          "bdg_mean_gap": 0.3760504819590623,
          "spatial_std": 2.128555894067847e-16,
          "converged": true
        }
      ],
      "finite_size_disorder": [
        {
          "L": 4,
          "mean_pairing": 0.3689800230463649,
          "sample_sd_pairing": 0.07015026827768743,
          "mean_spatial_std": 0.06974132940376908,
          "sample_sd_spatial_std": 0.018533097121100826,
          "samples": 10,
          "converged_samples": 10,
          "sem_pairing": 0.022183462622934948,
          "sem_spatial_std": 0.005860679899978804
        },
        {
          "L": 6,
          "mean_pairing": 0.3868718323955611,
          "sample_sd_pairing": 0.02147983173145277,
          "mean_spatial_std": 0.04931196806079603,
          "sample_sd_spatial_std": 0.005016136443842122,
          "samples": 10,
          "converged_samples": 10,
          "sem_pairing": 0.006792519202854897,
          "sem_spatial_std": 0.00158624162167184
        },
        {
          "L": 8,
          "mean_pairing": 0.37867744551341154,
          "sample_sd_pairing": 0.014064681930703801,
          "mean_spatial_std": 0.04281805189834192,
          "sample_sd_spatial_std": 0.003363546720349938,
          "samples": 10,
          "converged_samples": 10,
          "sem_pairing": 0.00444764294668385,
          "sem_spatial_std": 0.0010636468652695228
        }
      ],
      "all_scan_samples_converged": true,
      "all_finite_size_disorder_converged": true,
      "all_clean_crosschecks_converged": true,
      "sample_count": 120,
      "unique_solver_runs": 140,
      "all_unique_runs_converged": true,
      "dos_broadening_eta": 0.06,
      "dos_convention": "spin-resolved electron DOS; Gaussian broadening"
    },
    "figures": [
      "bdg_spectrum",
      "convergence_residual",
      "disorder_map",
      "dispersion",
      "dos_clean_disordered",
      "finite_size_comparison",
      "finite_size_disorder_comparison",
      "gap_map",
      "gap_vs_interaction",
      "gap_vs_temperature",
      "hopping_disorder_heatmap",
      "inhomogeneity_vs_disorder_tp0",
      "inhomogeneity_vs_disorder_tp0.2",
      "mean_gap_vs_disorder_tp0",
      "mean_gap_vs_disorder_tp0.2"
    ]
  }
];
