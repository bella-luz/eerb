"""Battery and energy storage calculations."""
import pandas as pd
import numpy as np


def calculate_battery_duration(energy_kwh: float, power_kw: float) -> float:
    """Calculate discharge duration at rated power."""
    if power_kw <= 0:
        return 0.0
    return float(energy_kwh / power_kw)


def calculate_peak_shaving(peak_before_kw: float, peak_after_kw: float) -> float:
    """Calculate peak reduction percentage."""
    if peak_before_kw <= 0:
        return 0.0
    reduction = (peak_before_kw - peak_after_kw) / peak_before_kw
    return float(max(0, min(1, reduction)))  # Clamp to 0-1


def simulate_battery_soc(
    load_kw: pd.Series,
    pv_generation_kw: pd.Series,
    battery_capacity_kwh: float,
    discharge_power_kw: float,
    charge_power_kw: float,
    efficiency: float = 0.90,
    min_soc_percent: float = 0.10,
    max_soc_percent: float = 0.95,
    initial_soc_percent: float = 0.50,
) -> dict:
    """
    Simplified battery SOC simulation.

    Strategy:
    1. PV serves load first
    2. Excess PV charges battery (if below max SOC)
    3. If load > PV, discharge battery (during defined hours or when beneficial)
    4. Respect power limits, SOC limits, efficiency

    Returns: SOC timeseries, peak reduction, charging/discharging energy
    """
    n = len(load_kw)
    soc = np.zeros(n)
    soc[0] = initial_soc_percent * battery_capacity_kwh

    charge_energy = 0.0
    discharge_energy = 0.0

    load_after_battery = load_kw.copy()

    for i in range(1, n):
        current_soc_kwh = soc[i - 1]
        current_load = load_kw.iloc[i]
        current_pv = pv_generation_kw.iloc[i]

        # Net energy needed (load - PV)
        net_load = current_load - current_pv

        if net_load > 0:
            # Load exceeds PV: try to discharge battery
            discharge_available = min(
                discharge_power_kw * 0.25,  # 15-min interval = 0.25 hours
                current_soc_kwh - (min_soc_percent * battery_capacity_kwh)
            )
            discharge_amount = min(net_load, discharge_available)

            # Apply efficiency loss during discharge
            soc_deduction = discharge_amount / efficiency
            new_soc = current_soc_kwh - soc_deduction
            discharge_energy += discharge_amount

            # Remaining load after battery
            load_after_battery.iloc[i] = current_load - discharge_amount
        else:
            # PV exceeds load: try to charge battery
            excess_pv = abs(net_load)
            charge_available = min(
                charge_power_kw * 0.25,
                (max_soc_percent * battery_capacity_kwh) - current_soc_kwh
            )
            charge_amount = min(excess_pv, charge_available)

            # Apply efficiency loss during charge
            soc_addition = charge_amount * efficiency
            new_soc = current_soc_kwh + soc_addition
            charge_energy += charge_amount

            # No remaining load
            load_after_battery.iloc[i] = 0

        # Clamp SOC to min/max
        min_soc_kwh = min_soc_percent * battery_capacity_kwh
        max_soc_kwh = max_soc_percent * battery_capacity_kwh
        soc[i] = np.clip(new_soc, min_soc_kwh, max_soc_kwh)

    peak_before = load_kw.max()
    peak_after = load_after_battery.max()
    peak_reduction = calculate_peak_shaving(peak_before, peak_after)

    return {
        "soc_timeseries": soc.tolist(),
        "load_after_battery": load_after_battery.values.tolist(),
        "peak_before_battery_kw": float(peak_before),
        "peak_after_battery_kw": float(peak_after),
        "peak_reduction_percent": float(peak_reduction * 100),
        "total_charged_kwh": float(charge_energy),
        "total_discharged_kwh": float(discharge_energy),
    }


def analyze_bess(
    energy_capacity_kwh: float,
    discharge_power_kw: float,
    peak_load_kw: float,
    peak_duration_hours: float,
    efficiency: float = 0.90,
) -> dict:
    """Comprehensive BESS analysis."""
    battery_duration = calculate_battery_duration(energy_capacity_kwh, discharge_power_kw)

    findings = [
        f"BESS energy capacity: {energy_capacity_kwh:.0f} kWh",
        f"BESS discharge power: {discharge_power_kw:.0f} kW",
        f"Battery duration at rated power: {battery_duration:.2f} hours",
        f"Round-trip efficiency: {efficiency * 100:.0f}%",
    ]

    concerns = []
    if battery_duration < peak_duration_hours * 0.8:
        concerns.append(
            f"Battery duration ({battery_duration:.2f}h) is shorter than peak period "
            f"({peak_duration_hours:.2f}h). Cannot fully support peak shaving for entire period."
        )

    if discharge_power_kw < peak_load_kw * 0.3:
        concerns.append(
            f"Discharge power ({discharge_power_kw:.0f} kW) is significantly less than peak load "
            f"({peak_load_kw:.0f} kW). Peak reduction may be limited."
        )

    return {
        "energy_capacity_kwh": energy_capacity_kwh,
        "discharge_power_kw": discharge_power_kw,
        "battery_duration_hours": battery_duration,
        "efficiency_percent": efficiency * 100,
        "findings": findings,
        "concerns": concerns,
    }
