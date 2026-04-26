import pandas as pd
from io import StringIO
import re
import glob
import os

# Automatically find the Excel file in the current directory
excel_files = glob.glob('*.xlsx')
print(f"Found Excel files: {excel_files}")

# Pick the climate file (not the cleaned one)
source_file = None
for f in excel_files:
    if 'cleaned' not in f.lower():
        source_file = f
        break

if source_file is None:
    print("❌ No Excel file found! Make sure your Excel file is in the same folder as this script.")
    exit()

print(f"✅ Using file: {source_file}")

# Load the raw Excel file
df_raw = pd.read_excel(source_file, header=None)

# Combine all columns into one string per row (fixes the splitting issue)
df_raw['combined'] = df_raw.apply(lambda row: ''.join(str(x) for x in row if str(x) != 'nan'), axis=1)

# Convert to proper CSV format
csv_data = '\n'.join(df_raw['combined'].tolist())
df = pd.read_csv(StringIO(csv_data))

# Rename columns
df.columns = ['Country Name', 'Country ISO3', 'Year', 'Indicator Name', 'Indicator Code', 'Value']

# Fix Country Name
df['Country Name'] = 'Sri Lanka'

# Fix spacing issues in Indicator Names
def fix_spaces(text):
    text = re.sub(r'([a-zA-Z0-9])\(', r'\1 (', text)
    text = re.sub(r'\)([a-zA-Z])', r') \1', text)
    text = text.replace('Agriculturalland', 'Agricultural land')
    text = text.replace('oflandarea', 'of land area')
    text = text.replace('ofland area', 'of land area')
    text = text.replace('Forest area(sq.km)', 'Forest area (sq. km)')
    text = text.replace('Forest area(% oflandarea)', 'Forest area (% of land area)')
    text = text.replace('precipitationin', 'precipitation in')
    text = text.replace('yield(kg', 'yield (kg')
    text = text.replace('kgper', 'kg per')
    text = text.replace('Electricityproduction', 'Electricity production')
    text = text.replace('electricityoutput', 'electricity output')
    text = text.replace('energyconsumption', 'energy consumption')
    text = text.replace('Energy use(kg', 'Energy use (kg')
    text = text.replace('oilequivalent', 'oil equivalent')
    text = text.replace('Terrestrialprotectedareas', 'Terrestrial protected areas')
    text = text.replace('protectedareas', 'protected areas')
    text = text.replace('marineprotected', 'marine protected')
    text = text.replace('Terrestrialand', 'Terrestrial and')
    text = text.replace('publicsector', 'public sector')
    text = text.replace('Mortality rate,under-5', 'Mortality rate, under-5')
    text = text.replace('Prevalenceof', 'Prevalence of')
    text = text.replace('headcountratio', 'headcount ratio')
    text = text.replace('Population growth(annual', 'Population growth (annual')
    text = text.replace('Population,total', 'Population, total')
    text = text.replace('populationgrowth', 'population growth')
    text = text.replace('populationliving', 'population living')
    text = text.replace('Renewable electricityoutput', 'Renewable electricity output')
    text = text.replace('Renewable energyconsumption', 'Renewable energy consumption')
    text = text.replace('whereelevation', 'where elevation')
    text = text.replace('livingin', 'living in')
    text = text.replace('productionfrom', 'production from')
    text = text.replace('k Wh', 'kWh')
    text = text.replace('ofoil', 'of oil')
    text = text.replace('% oftotal', '% of total')
    text = text.replace('population(% of', 'population (% of')
    text = re.sub(r' +', ' ', text).strip()
    return text

df['Indicator Name'] = df['Indicator Name'].apply(fix_spaces)

# Save cleaned file
df.to_excel('sri_lanka_climate_cleaned.xlsx', index=False)
print("✅ Cleaned file saved as 'sri_lanka_climate_cleaned.xlsx'")
print(f"✅ Total rows: {len(df)}")
print(f"✅ Total indicators: {df['Indicator Name'].nunique()}")
print(f"✅ Year range: {df['Year'].min()} - {df['Year'].max()}")
