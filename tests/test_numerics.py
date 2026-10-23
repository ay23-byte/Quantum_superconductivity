import numpy as np
from src.lattice import square_lattice_hamiltonian, momentum_grid, square_lattice_dispersion
from src.hamiltonian import bdg_hamiltonian
from src.solver import solve_bdg, density_from_result
from src.hamiltonian import electron_ldos
from src.gap_equation import uniform_gap
from src.validation import particle_hole_error
from src.disorder import onsite_disorder
from src.observables import phase_stiffness_fixed_density_hartree

def test_lattice_hermitian_and_dispersion_matches():
    L=4; t=1.; tp=.17; mu=-.31
    K=square_lattice_hamiltonian(L,t,tp,mu)
    kx,ky=momentum_grid(L)
    vals=np.linalg.eigvalsh(K)
    expected=np.sort(square_lattice_dispersion(kx,ky,t,tp,mu).ravel())
    assert np.allclose(K,K.T)
    assert np.allclose(vals,expected,atol=1e-12)

def test_small_lattice_bond_multiplicity_matches_dispersion():
    for L in (1,2,3):
        K=square_lattice_hamiltonian(L,t=1,t_prime=.2,mu=.4)
        kx,ky=momentum_grid(L)
        assert np.allclose(np.linalg.eigvalsh(K),np.sort(square_lattice_dispersion(kx,ky,1,.2,.4).ravel()))

def test_bdg_is_hermitian_and_particle_hole_symmetric():
    K=square_lattice_hamiltonian(3,1,.1,-.3,np.arange(9)/20)
    H=bdg_hamiltonian(K,np.linspace(.1,.4,9))
    e=np.linalg.eigvalsh(H)
    assert np.allclose(H,H.T.conj())
    assert particle_hole_error(e)<1e-11

def test_clean_uniform_bdg_matches_independent_bcs():
    L=4; U=2.2; T=.08; mu=-.6
    ref=uniform_gap(L,U,T,mu=mu)
    result=solve_bdg(square_lattice_hamiltonian(L,mu=mu),U,T,initial_gap=ref,tolerance=2e-9)
    assert result.converged
    assert np.allclose(result.gap,ref,atol=2e-7)

def test_seeded_disorder_is_reproducible_and_has_defined_support():
    a=onsite_disorder(100,2,seed=17); b=onsite_disorder(100,2,seed=17)
    assert np.array_equal(a,b)
    assert np.all((a>=-1)&(a<=1))

def test_normal_state_density_and_ldos_are_well_formed():
    K=square_lattice_hamiltonian(2,t=1,t_prime=0,mu=.37)
    result=solve_bdg(K,U=.2,T=.2,initial_gap=0.)
    density=density_from_result(K,result,.2)
    spectrum=electron_ldos(K,result.gap,np.linspace(-5,5,301),.08)
    assert result.converged and np.all((density>=0)&(density<=2))
    assert spectrum.shape==(4,301) and np.all(spectrum>=0)

def test_twisted_lattice_is_hermitian_and_zero_twist_is_unchanged():
    clean=square_lattice_hamiltonian(4,t=1,t_prime=.2,mu=0)
    twisted=square_lattice_hamiltonian(4,t=1,t_prime=.2,mu=0,twist_x=.1)
    assert np.allclose(clean,clean.T.conj())
    assert np.allclose(twisted,twisted.T.conj())
    assert np.allclose(clean,square_lattice_hamiltonian(4,t=1,t_prime=.2,mu=0,twist_x=0))

def test_fixed_density_hartree_solver_and_phase_stiffness():
    result=phase_stiffness_fixed_density_hartree(
        2,2.2,.08,1.0,delta=.08,phase_seeds=1,tolerance=2e-5,
        density_tolerance=1e-4,max_iterations=1200,mixing=.1)
    center=result["twists"]["0.0"]
    assert result["paired_state"] and result["rho_s"] is not None
    assert result["rho_s"] > 0
    assert abs(center["mean_density"]-1.0)<1e-4
    assert center["mean_gap"]>0

