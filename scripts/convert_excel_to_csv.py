import pandas as pd

# Load both sheets
sheet1 = pd.read_excel('./dataset/online_retail_II.xlsx', sheet_name='Year 2009-2010')
sheet2 = pd.read_excel('./dataset/online_retail_II.xlsx', sheet_name='Year 2010-2011')

# Combine into one DataFrame
df_combined = pd.concat([sheet1, sheet2], ignore_index=True)

# Save as a unified CSV
df_combined.to_csv('./dataset/online_retail_II.csv', index=False)

print("✅ Combined both sheets and saved as 'online_retail_II.csv'")
