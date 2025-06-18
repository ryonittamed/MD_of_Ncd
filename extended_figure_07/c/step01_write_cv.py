#!/usr/bin/env python

import argparse
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
warnings.warn = lambda *args, **kwargs: None

import numpy as np
import polars as pl
import pandas as pd
import MDAnalysis as mda
from msm_utils.plot_angle_vs_native_contacts import angle_vs_contacts
from tqdm import tqdm


def calculate_spherical_angles_rotated(vector, x_prime, y_prime, z_prime):
    """
    Calculate the spherical angles (theta and phi) for a vector in a rotated coordinate system.

    Parameters:
    vector (array-like): A 3D vector [vx, vy, vz].
    x_prime (array-like): Unit vector representing x_prime in the global coordinate system.
    y_prime (array-like): Unit vector representing y_prime in the global coordinate system.
    z_prime (array-like): Unit vector representing z_prime in the global coordinate system.

    Returns:
    tuple: (theta, phi) where
        - theta is the polar angle in radians [0, pi].
        - phi is the azimuthal angle in radians [-pi, pi].
    """
    # Ensure inputs are NumPy arrays
    vector = np.array(vector)
    x_prime = np.array(x_prime)
    y_prime = np.array(y_prime)
    z_prime = np.array(z_prime)

    # Ensure the basis vectors are orthonormal
    if not (np.isclose(np.linalg.norm(x_prime), 1.0) and
            np.isclose(np.linalg.norm(y_prime), 1.0) and
            np.isclose(np.linalg.norm(z_prime), 1.0)):
        raise ValueError("Basis vectors must be unit vectors.")
    if not (np.isclose(np.dot(x_prime, y_prime), 0) and
            np.isclose(np.dot(y_prime, z_prime), 0) and
            np.isclose(np.dot(z_prime, x_prime), 0)):
        raise ValueError("Basis vectors must be orthogonal.")

    # Construct the rotation matrix
    R = np.column_stack((x_prime, y_prime, z_prime))

    # Transform the vector into the rotated coordinate system
    vector_rotated = np.dot(R.T, vector)

    # Extract components of the transformed vector
    vx_prime, vy_prime, vz_prime = vector_rotated

    # Calculate spherical angles
    theta = np.arccos(vz_prime)
    phi = np.arctan2(vy_prime, vx_prime)

    return theta, phi


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sel-stalk1", type=str, required=True, help="Selection string for the stalk 1")
    parser.add_argument("--sel-stalk2", type=str, required=True, help="Selection string for the stalk 2")
    parser.add_argument("--sel-msu1", type=str, required=True, help="Selection for the microtubule subunit C")
    parser.add_argument("--sel-msu2", type=str, required=True, help="Selection for the microtubule subunit G")
    parser.add_argument("--sel-msu3", type=str, required=True, help="Selection for the microtubule subunit L")
    parser.add_argument("--pdb", type=str, required=True, help="PDB file for topology")
    parser.add_argument("--dcd", type=str, required=True, help="DCD file for trajectory")
    parser.add_argument("--itp", type=str, required=True, help="ITP file for trajectory")
    parser.add_argument("--out", type=str, required=True, help="Output file name")
    args = parser.parse_args()

    # Load data
    print(f"{args.dcd=}")
    uni = mda.Universe(args.pdb, args.dcd)

    # Define selections
    stalk1 = uni.select_atoms(args.sel_stalk1)
    stalk2 = uni.select_atoms(args.sel_stalk2)
    msu1 = uni.select_atoms(args.sel_msu1)
    msu2 = uni.select_atoms(args.sel_msu2)
    msu3 = uni.select_atoms(args.sel_msu3)

    # Define point selections
    sel1 = stalk1[10:15] + stalk2[10:15]
    sel2 = stalk1[-5:]

    # Calculate points for defining the vector
    p1 = np.zeros((uni.trajectory.n_frames, 3))  # Top
    p2 = np.zeros((uni.trajectory.n_frames, 3))  # Bottom
    for ts in tqdm(uni.trajectory):
        p1[ts.frame] = sel1.center_of_geometry()
        p2[ts.frame] = sel2.center_of_geometry()

    # Calculate direction vector
    vectors = p2 - p1
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    vectors /= norms

    # Define plane selections
    sel1 = msu1
    sel2 = msu2
    sel3 = msu3

    # Calculate points for defining the plane
    p1 = np.zeros((uni.trajectory.n_frames, 3))
    p2 = np.zeros((uni.trajectory.n_frames, 3))
    p3 = np.zeros((uni.trajectory.n_frames, 3))
    for ts in tqdm(uni.trajectory):
        p1[ts.frame] = sel1.center_of_geometry()
        p2[ts.frame] = sel2.center_of_geometry()
        p3[ts.frame] = sel3.center_of_geometry()

    # Calculate axes
    p21 = p1 - p2
    p23 = p3 - p2

    z_axes = np.cross(p23, p21)
    x_axes = np.cross(p21, z_axes)
    y_axes = np.cross(z_axes, x_axes)

    x_axes /= np.linalg.norm(x_axes, axis=1, keepdims=True)
    y_axes /= np.linalg.norm(y_axes, axis=1, keepdims=True)
    z_axes /= np.linalg.norm(z_axes, axis=1, keepdims=True)

    # Calculate angles
    theta_list = []
    phi_list = []
    # for vector in vectors:
    for vector, x_axis, y_axis, z_axis in zip(vectors, x_axes, y_axes, z_axes):
        theta, phi = calculate_spherical_angles_rotated(vector, x_axis, y_axis, z_axis)
        theta_list.append(theta)
        phi_list.append(phi)

    # Calculate contact count ratio and rmsd
    ret = angle_vs_contacts(Path(args.dcd), Path(args.itp), Path(args.pdb), neckmimic=True if Path(args.dcd).parent.parent.name != 'kinesin-no-neckmimic' else False)

    # Create dataframe
    df = pd.DataFrame({
        "theta": theta_list,
        "phi": phi_list,
        "contact_count_ratio": ret['contact_count_ratio'],
        "rmsd": ret['rmsd'],
        "contact_resids_in_neckmimic": ret['contact_resids_in_neckmimic'],
        "docks": ret['docks'],
    })
    print(df)


    # Save dataframe
    df.to_csv(args.out)


if __name__ == "__main__":
    main()
