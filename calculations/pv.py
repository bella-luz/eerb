"""PV analysis calculations."""
import pandas as pd


def calculate_pv_energy(pv_capacity_kw: float, irradiance_profile: pd.Series) -> dict:
    """
    Calculate PV energy generation given capacity and irradiance.

    Assumes irradiance_profile is normalized (0-1) or actual kW output.
    If values > 1, assumes they are actual kW values.
    """
    if irradiance_profile.max() > 1:
        # Already in kW
        daily_energy_kwh = irradiance_profile.sum() * 0.25  # 15-min intervals
        peak_kw = irradiance_profile.max()
    else:
        # Normalized irradiance, multiply by capacity
        daily_energy_kwh = (irradiance_profile * pv_capacity_kw).sum() * 0.25
        peak_kw = irradiance_profile.max() * pv_capacity_kw

    return {
        "daily_energy_kwh": float(daily_energy_kwh),
        "peak_generation_kw": float(peak_kw),
    }


def compare_pv_to_load(pv_capacity_kw: float, peak_load_kw: float, avg_load_kw: float,
                       daily_pv_kwh: float, daily_load_kwh: float) -> dict:
    """Compare PV capacity and generation to load."""
    pv_to_peak_ratio = pv_capacity_kw / peak_load_kw if peak_load_kw > 0 else 0
    pv_to_avg_ratio = pv_capacity_kw / avg_load_kw if avg_load_kw > 0 else 0
    coverage_ratio = daily_pv_kwh / daily_load_kwh if daily_load_kwh > 0 else 0

    findings = [
        f"PV capacity: {pv_capacity_kw:.0f} kW",
        f"PV-to-peak ratio: {pv_to_peak_ratio:.2f}",
        f"Estimated daily PV generation: {daily_pv_kwh:.0f} kWh",
        f"Estimated daily load: {daily_load_kwh:.0f} kWh",
        f"PV covers approximately {coverage_ratio * 100:.0f}% of daily load",
    ]

    concerns = []
    if pv_to_peak_ratio < 0.5:
        concerns.append("PV capacity is significantly smaller than peak load (typically expected)")
    if coverage_ratio < 0.3:
        concerns.append("PV generation may not significantly offset load without BESS")

    return {
        "pv_capacity_kw": pv_capacity_kw,
        "pv_to_peak_ratio": float(pv_to_peak_ratio),
        "pv_to_avg_ratio": float(pv_to_avg_ratio),
        "daily_pv_kwh": float(daily_pv_kwh),
        "daily_load_kwh": float(daily_load_kwh),
        "coverage_ratio": float(coverage_ratio),
        "findings": findings,
        "concerns": concerns,
    }


def analyze_pv(pv_capacity_kw: float, daily_pv_kwh: float, peak_load_kw: float,
               avg_load_kw: float, daily_load_kwh: float) -> dict:
    """Comprehensive PV analysis."""
    comparison = compare_pv_to_load(pv_capacity_kw, peak_load_kw, avg_load_kw,
                                    daily_pv_kwh, daily_load_kwh)

    return {
        "pv_capacity_kw": pv_capacity_kw,
        "daily_generation_kwh": daily_pv_kwh,
        "pv_to_peak_ratio": comparison["pv_to_peak_ratio"],
        "load_coverage_percent": comparison["coverage_ratio"] * 100,
        "findings": comparison["findings"],
        "concerns": comparison["concerns"],
    }
