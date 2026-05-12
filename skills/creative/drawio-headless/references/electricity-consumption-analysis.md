# Electricity Consumption Analysis Pattern

Pattern for analyzing household/office electricity usage from meter token readings, with focus on AC (air conditioning) as primary consumer.

## Use Case

User provides token meter readings at different timestamps. Goal: calculate consumption, identify major consumers, project costs, recommend savings.

## Input Data Format

```
Tanggal 1: Token = X kWh at HH:MM
Tanggal 2: Token = Y kWh at HH:MM
Tanggal 3: Token = Z kWh at HH:MM
```

## Calculation Steps

### 1. Consumption Per Period

```python
consumption_kwh = previous_token - current_token
duration_hours = (current_datetime - previous_datetime).total_seconds() / 3600
average_power_watt = (consumption_kwh / duration_hours) * 1000
```

### 2. Daily/Monthly Projection

```python
daily_consumption = total_consumption / (total_duration / 24)
monthly_consumption = daily_consumption * 30
```

### 3. Cost Calculation

```python
# PLN tariff (Indonesia) — adjust per region
tariff_per_kwh = 1444.70  # Rp/kWh for R1/900VA

daily_cost = daily_consumption * tariff_per_kwh
monthly_cost = monthly_consumption * tariff_per_kwh
```

### 4. Token Remaining Projection

```python
current_token = latest_reading
days_remaining = current_token / daily_consumption
estimated_empty_date = last_date + timedelta(days=days_remaining)
```

## Device Breakdown

### Typical Power Consumption (Indonesia)

| Device | Idle | Load | Average | Runtime |
|---|---|---|---|---|
| **AC 1 PK (non-inverter)** | 900W | 900W | 900W | 21-22h/day |
| **AC 1 PK (inverter)** | 300W | 600W | 450W | 21-22h/day |
| PC (Ryzen 7 + RX 7700 XT) | 150W | 450W | 250W | 24h/day |
| Monitor (24") | 30W | 30W | 30W | 12h/day |
| Router/Modem | 10W | 10W | 10W | 24h/day |
| LED Lamp (10W x3) | 30W | 30W | 30W | 8h/day |
| Kipas angin | 50W | 50W | 50W | Variable |

### AC Dominance Pattern

**Key insight:** AC 1 PK non-inverter running 21h/day = **~80% of total consumption**.

```python
ac_power = 900  # Watt
ac_hours = 21.5  # hours/day
ac_daily_kwh = (ac_power / 1000) * ac_hours  # 19.4 kWh/day

# If total consumption = 24.4 kWh/day
ac_percentage = (19.4 / 24.4) * 100  # 79.5%
```

## Savings Scenarios

### 1. Upgrade AC to Inverter

```python
non_inverter_consumption = 900 * 21.5 / 1000  # 19.4 kWh/day
inverter_consumption = 450 * 21.5 / 1000      # 9.7 kWh/day
saving_per_day = 9.7  # kWh
saving_per_month = 9.7 * 30 * tariff  # Rp 419,324
```

**ROI:** AC inverter costs ~Rp 3-5 juta. Payback period: 7-12 months.

### 2. Reduce Runtime

```python
# 21h → 12h
current_consumption = 900 * 21.5 / 1000  # 19.4 kWh/day
reduced_consumption = 900 * 12 / 1000    # 10.8 kWh/day
saving_per_day = 8.6  # kWh
saving_per_month = 8.6 * 30 * tariff  # Rp 372,690
```

### 3. AC Only at Night (8h)

```python
night_only_consumption = 900 * 8 / 1000  # 7.2 kWh/day
saving_per_day = 12.2  # kWh
saving_per_month = 12.2 * 30 * tariff  # Rp 528,594
```

## Visualization Pattern

### Pie Chart (Consumption Breakdown)

- AC slice: 80% (red/orange)
- PC + Others: 20% (green)

### Bar Chart (Cost Breakdown)

- AC cost bar: 80% width
- Other devices: 20% width

### Timeline (Token Depletion)

```
[Start] → [Period 1] → [Period 2] → [Current] → [Projected Empty]
  843      -14.3 kWh    -24.0 kWh     804.7      0 kWh (~33 days)
```

### Savings Comparison

Three scenarios side-by-side:
1. Upgrade inverter (50% AC saving)
2. Reduce runtime (47% AC saving)
3. Night-only (70% AC saving)

## Recommendations Template

### Immediate Actions (No Cost)

1. Set AC temperature 25-26°C (not 18-20°C)
2. Close doors/windows when AC running
3. Use timer/smart plug for auto-off
4. Service AC coil (clean = efficient)

### Short-term (Low Cost)

1. Install power meter (Rp 100-300k)
2. Smart plug with scheduling (Rp 150-400k)
3. Kipas angin for daytime (Rp 200-500k)

### Long-term (Investment)

1. Upgrade to inverter AC (Rp 3-5 juta, ROI 1-2 years)
2. Solar panels (if feasible)

## Common Pitfalls

### 1. Ignoring AC Runtime

**Mistake:** Focusing on PC/monitor optimization when AC is 80% of consumption.

**Fix:** Always calculate AC contribution first. If AC >70%, that's the primary target.

### 2. Assuming Linear Consumption

**Mistake:** Extrapolating from short periods without considering usage patterns.

**Fix:** Collect data across multiple days, including weekday/weekend variations.

### 3. Forgetting Standby Power

**Mistake:** Only counting active usage, ignoring standby/idle devices.

**Fix:** Account for 24/7 devices (router, modem, standby appliances).

## Python Implementation

```python
from datetime import datetime, timedelta

def analyze_electricity(readings, tariff=1444.70):
    \"\"\"
    readings: list of {'date': 'YYYY-MM-DD', 'time': 'HH:MM', 'token': float}
    tariff: Rp per kWh
    \"\"\"
    # Parse datetimes
    for r in readings:
        r['datetime'] = datetime.strptime(f"{r['date']} {r['time']}", '%Y-%m-%d %H:%M')
    
    # Calculate periods
    periods = []
    for i in range(1, len(readings)):
        prev, curr = readings[i-1], readings[i]
        consumption = prev['token'] - curr['token']
        duration = (curr['datetime'] - prev['datetime']).total_seconds() / 3600
        avg_power = (consumption / duration) * 1000
        
        periods.append({
            'consumption_kwh': consumption,
            'duration_hours': duration,
            'avg_power_watt': avg_power
        })
    
    # Summary
    total_consumption = sum(p['consumption_kwh'] for p in periods)
    total_duration = sum(p['duration_hours'] for p in periods)
    overall_avg_power = (total_consumption / total_duration) * 1000
    
    daily_consumption = total_consumption / (total_duration / 24)
    monthly_consumption = daily_consumption * 30
    
    current_token = readings[-1]['token']
    days_remaining = current_token / daily_consumption
    
    return {
        'total_consumption_kwh': total_consumption,
        'daily_consumption_kwh': daily_consumption,
        'monthly_consumption_kwh': monthly_consumption,
        'avg_power_watt': overall_avg_power,
        'daily_cost': daily_consumption * tariff,
        'monthly_cost': monthly_consumption * tariff,
        'token_remaining': current_token,
        'days_remaining': days_remaining,
        'periods': periods
    }
```

## See Also

- VPS resource analysis pattern (similar breakdown approach)
- System services diagram pattern (visual breakdown)
