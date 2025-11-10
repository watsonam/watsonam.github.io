| **bmUnitType** | **Description**                                                                                                                                                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **G**          | **Generating BM Unit** — A generation unit that exports electricity to the grid. This includes power stations or smaller embedded generators that are registered in the Balancing Mechanism.                                    |
| **D**          | **Demand BM Unit** — A unit that primarily consumes electricity. This can include large industrial consumers or demand-side response units.                                                                                     |
| **E**          | **Externally Interconnected System (EIS) BM Unit** — Used for interconnectors between Great Britain and other markets (e.g., France, Netherlands, Belgium, Norway). Represents import/export capability.                        |
| **X**          | **Embedded BM Unit (Supplier BM Unit)** — Typically associated with suppliers for their customers’ consumption and generation (i.e., embedded within distribution networks, not directly connected to the transmission system). |
| **T**          | **Trading Unit BM Unit** — Used for aggregations of BM Units across different sites or companies under specific trading arrangements.                                                                                           |


  For Physical Notifications (PN dataset):
  - level_from: Starting power level (MW)
  - level_to: Ending power level (MW)
  - Positive values = Generation/Export to grid
  - Negative values = Consumption/Import from grid


If level_from = level_to, the unit maintains 
  constant output/consumption for the full
  30-minute period.

  If they're different, the unit is ramping up/down
   during that settlement period.

## Primary vs Secondary BM Units

| **BMU Category** | **Description** |
| ---------------- | --------------- |
| **Primary BMU** | Fundamental accounting units under BSC for ALL energy flows. Handle mandatory settlement obligations. Required for all market participants. |
| **Secondary BMU** | Optional units for specialized trading/balancing services. Registered by Virtual Lead Parties (VLPs) in addition to Primary BMUs. Enable commercial flexibility. |