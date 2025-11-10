import matplotlib.pyplot as plt
from scrapers.nordpool import scrape_nordpool, scrape_nordpool_volumes

# Get data for a recent date
nord_pool_df = scrape_nordpool('2025-10-20')
nord_pool_volumes_df = scrape_nordpool_volumes('2025-10-20')

fig, ax1 = plt.subplots(figsize=(15, 8))

# Plot price on left y-axis
color = 'tab:red'
ax1.set_xlabel('Hour')
ax1.set_ylabel('Price (GBP/MWh)', color=color)
ax1.plot(range(len(nord_pool_df)), nord_pool_df['price'], marker='o', color=color, label='Price', linewidth=2)
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, alpha=0.3)

# Create second y-axis for volumes
ax2 = ax1.twinx()
color_buy = 'tab:blue'
color_sell = 'tab:green'
ax2.set_ylabel('Volume (MWh)', color='black')
ax2.plot(range(len(nord_pool_volumes_df)), nord_pool_volumes_df['buy_volume'], marker='x', color=color_buy, label='Buy Volume', linewidth=2, alpha=0.7)
ax2.plot(range(len(nord_pool_volumes_df)), nord_pool_volumes_df['sell_volume'], marker='s', color=color_sell, label='Sell Volume', linewidth=2, alpha=0.7)
ax2.tick_params(axis='y', labelcolor='black')

# Set x-axis labels
ax1.set_xticks(range(len(nord_pool_df)))
ax1.set_xticklabels(nord_pool_df['period'], rotation=45, ha='right')

# Add title and legends
plt.title('UK Electricity Day-Ahead Prices and Trading Volumes (2025-10-20)', fontsize=14, pad=20)
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.tight_layout()
plt.show()