"""Load profile analysis calculations."""
import pandas as pd
import numpy as np


def calculate_load_statistics(load_kw: pd.Series) -> dict:
    """Calculate key load profile statistics."""
    return {
        "peak_kw": float(load_kw.max()),
        "average_kw": float(load_kw.mean()),
        "daily_energy_kwh": float(load_kw.sum() / 4),  # 15-min intervals, 96 per day
        "min_kw": float(load_kw.min()),
        "std_dev_kw": float(load_kw.std()),
    }


def calculate_peak_demand(load_kw: pd.Series) -> float:
    """Return peak demand in kW."""
    return float(load_kw.max())


def calculate_average_load(load_kw: pd.Series) -> float:
    """Return average load in kW."""
    return float(load_kw.mean())


def calculate_daily_energy(load_kw: pd.Series) -> float:
    """Calculate daily energy consumption in kWh (assuming 15-min intervals)."""
    # Sum load * time interval (0.25 hours for 15-min intervals)
    return float((load_kw.sum() * 0.25))


def calculate_peak_duration(load_kw: pd.Series, peak_percentage: float = 0.9) -> float:
    """Calculate how long load stays above 90% of peak (in hours)."""
    peak = load_kw.max()
    threshold = peak * peak_percentage
    above_threshold = load_kw[load_kw >= threshold]
    # Each entry is 0.25 hours (15 minutes)
    return float(len(above_threshold) * 0.25)


def get_peak_window(load_kw: pd.Series, timestamps: pd.Series = None) -> dict:
    """Find the peak load period and return info."""
    peak_idx = load_kw.idxmax()
    peak_value = load_kw[peak_idx]

    if timestamps is not None:
        peak_time = timestamps.iloc[peak_idx]
    else:
        peak_time = f"Index {peak_idx}"

    return {
        "peak_kw": float(peak_value),
        "peak_time": str(peak_time),
        "peak_index": int(peak_idx),
    }


def analyze_load_profile(load_kw: pd.Series) -> dict:
    """Comprehensive load analysis."""
    stats = calculate_load_statistics(load_kw)
    peak_duration = calculate_peak_duration(load_kw)

    return {
        "peak_demand_kw": stats["peak_kw"],
        "average_demand_kw": stats["average_kw"],
        "daily_energy_kwh": stats["daily_energy_kwh"],
        "peak_duration_hours": peak_duration,
        "load_range_kw": (stats["min_kw"], stats["peak_kw"]),
        "findings": [
            f"Peak demand: {stats['peak_kw']:.1f} kW",
            f"Average demand: {stats['average_kw']:.1f} kW",
            f"Daily energy: {stats['daily_energy_kwh']:.1f} kWh",
            f"Peak lasts approximately {peak_duration:.2f} hours at ≥90% of peak",
            f"Load range: {stats['min_kw']:.1f}–{stats['peak_kw']:.1f} kW",
        ],
    }
