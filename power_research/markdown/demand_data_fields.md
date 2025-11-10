# NESO Historic Demand Data Field Definitions

## Time & Settlement

| **Field** | **Description** |
|-----------|-----------------|
| `SETTLEMENT_DATE` | Date of historic electricity data (ISO 8601 format, follows UK clock changes) |
| `SETTLEMENT_PERIOD` | Half-hourly time period (1-48). Period 1 = 00:00-00:30, Period 48 = 23:30-24:00 |

## Core Demand Metrics

| **Field** | **Description** |
|-----------|-----------------|
| `ND` | **National Demand** - GB generation requirement. Excludes station load, pumping, interconnector exports (MW) |
| `TSD` | **Transmission System Demand** - ND plus estimated station load and other generation requirements (MW) |
| `ENGLAND_WALES_DEMAND` | Demand specifically for England & Wales region (MW) |

## Embedded Generation

| **Field** | **Description** |
|-----------|-----------------|
| `EMBEDDED_WIND_GENERATION` | Estimated wind generation from distribution networks (MW) |
| `EMBEDDED_WIND_CAPACITY` | Total embedded wind capacity available (MW) |
| `EMBEDDED_SOLAR_GENERATION` | Estimated solar generation from distribution networks (MW) |
| `EMBEDDED_SOLAR_CAPACITY` | Total embedded solar capacity available (MW) |

## Storage & System Services

| **Field** | **Description** |
|-----------|-----------------|
| `NON_BM_STOR` | Non-Balancing Mechanism Short Term Operating Reserve (MW) |
| `PUMP_STORAGE_PUMPING` | Electricity used for pumping water to storage (MW) |

## Interconnector Flows

**Note: Negative values = GB exports power, Positive values = GB imports power**

| **Field** | **Description** |
|-----------|-----------------|
| `SCOTTISH_TRANSFER` | Power transfer between Scotland and England/Wales (MW) |
| `IFA_FLOW` | Interconnector to France (MW) |
| `IFA2_FLOW` | Second interconnector to France (MW) |
| `BRITNED_FLOW` | Interconnector to Netherlands (MW) |
| `MOYLE_FLOW` | Interconnector to Northern Ireland (MW) |
| `EAST_WEST_FLOW` | Interconnector to Republic of Ireland (MW) |
| `NEMO_FLOW` | Interconnector to Belgium (MW) |
| `NSL_FLOW` | North Sea Link to Norway (MW) |
| `ELECLINK_FLOW` | ElecLink to France (MW) |
| `VIKING_FLOW` | Viking Link to Denmark (MW) |
| `GREENLINK_FLOW` | Greenlink to Republic of Ireland (MW) |

## Key Notes

- All power values in Megawatts (MW)
- Embedded generation represents renewables connected to distribution networks (not transmission-connected)
- Settlement periods follow UK daylight saving time changes
- Interconnector flows show the complete picture of GB's electricity trade with neighboring countries