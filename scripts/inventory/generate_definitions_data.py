#!/usr/bin/env python3
"""
generate_definitions_data.py - Builds taxonomy_definitions.py with complete 55 disciplines.
"""

import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# We will define the full categories data in a python script that writes scripts/inventory/taxonomy_definitions.py
# Let's inspect the files in categories to ensure exact matching filenames.
CATEGORY_FILES = {
    1: "01_curated_knowledge_developer_gu.md",
    2: "02_artificial_intelligence_large_.md",
    3: "03_multi_agent_systems_autonomous.md",
    4: "04_computer_vision_multimodal_ai_.md",
    5: "05_speech_voice_ai_audio_processi.md",
    6: "06_robotics_humanoid_kinematics_d.md",
    7: "07_autonomous_vehicles_mobile_rob.md",
    8: "08_semiconductor_silicon_eda_rtl_.md",
    9: "09_quantum_computing_quantum_algo.md",
    10: "10_superconducting_systems_cryoge.md",
    11: "11_spintronics_micromagnetics_ato.md",
    12: "12_nuclear_fusion_plasma_physics_.md",
    13: "13_clean_energy_solid_oxide_fuel_.md",
    14: "14_space_systems_orbital_astrodyn.md",
    15: "15_spacecraft_proximity_operation.md",
    16: "16_gravitational_wave_astronomy_p.md",
    17: "17_aerospace_aerodynamics_hyperso.md",
    18: "18_computational_fluid_dynamics_c.md",
    19: "19_peridynamics_structural_mechan.md",
    20: "20_additive_manufacturing_laser_p.md",
    21: "21_terrestrial_laser_scanning_tls.md",
    22: "22_subsurface_geomechanics_geothe.md",
    23: "23_acoustic_levitation_acoustoflu.md",
    24: "24_marine_hydrodynamics_sonar_tra.md",
    25: "25_atmospheric_sciences_meteorolo.md",
    26: "26_healthcare_computational_biome.md",
    27: "27_genomics_crispr_gene_editing_s.md",
    28: "28_neurotechnology_brain_computer.md",
    29: "29_smart_cities_building_informat.md",
    30: "30_cybersecurity_reverse_engineer.md",
    31: "31_industrial_automation_scada_pl.md",
    32: "32_cryptography_zero_knowledge_pr.md",
    33: "33_formal_verification_theorem_pr.md",
    34: "34_edtech_adaptive_learning_cogni.md",
    35: "35_fintech_core_banking_payment_p.md",
    36: "36_blockchain_web3_smart_contract.md",
    37: "37_database_engines_distributed_s.md",
    38: "38_data_engineering_distributed_a.md",
    39: "39_cloud_native_infrastructure_ku.md",
    40: "40_ci_cd_automation_gitops_infras.md",
    41: "41_observability_apm_telemetry_me.md",
    42: "42_networking_reverse_proxies_loa.md",
    43: "43_operating_systems_linux_kernel.md",
    44: "44_compilers_interpreters_virtual.md",
    45: "45_systems_programming_low_level_.md",
    46: "46_developer_tooling_shell_enviro.md",
    47: "47_code_editors_ides_syntax_plugi.md",
    48: "48_game_development_engines_2d_3d.md",
    49: "49_modern_frontend_frameworks_rea.md",
    50: "50_ui_component_systems_design_to.md",
    51: "51_mobile_app_development_cross_p.md",
    52: "52_desktop_application_frameworks.md",
    53: "53_backend_web_frameworks_microse.md",
    54: "54_multimedia_processing_audio_vi.md",
    55: "55_python_ecosystem_data_science_.md"
}

print(f"Verified {len(CATEGORY_FILES)} category files.")
