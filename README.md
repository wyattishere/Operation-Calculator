Operation Calculator---

Made By: Hodgins W. wyattishere6940@gmail.com

Installation: 
Open installer_output
Double Click OperationCostCalculator_Setup.exe
 **Note on Windows SmartScreen:** Because this is an independent, non-profit project without a paid Microsoft code-signing certificate, Windows may display a *"Windows protected your PC"* popup when running the installer. To proceed, click **More info** → **Run anyway**.

-- This may pop up; here is a copyable command: python -m pip install reportlab pdf417gen Pillow


Un-Installation:
Select the whole Operation_Calculator folder and press delete
You can also go right click the Windows icon on the taskbar > Installed Apps > Operation Calculator > Uninstall

Features

• Comprehensive Equipment & Asset Catalog: Pre-loaded with 40+ items across 14 categories—including small arms, ammunition, grenades, artillery, ground vehicles, aircraft, fuel, provisions, uniforms, and tactical gear.
• Quick Catalog Search: Filter across all 40+ items and categories instantly using the search bar at the top of the catalog selection panel.
• Save & Load Operation Presets (.json): Save your configured operation details, troop counts, and equipment loadouts to a preset file and reload them anytime.
• Smart Cost Calculation Engine (CAD):
	• Personnel Costs: Automatically calculates troop deployment pay/allowances based on headcount and operation duration.
	• Consumables & Gear: Tracks per-round, per-litre, per-ration, and per-unit expenditures.
	• Capital Assets (Weapons, Vehicles & Aircraft): Separates one-time acquisition/replacement costs from active operating expenses—prorating annual weapon maintenance by operation days and calculating vehicle/aircraft wear by kilometres or flight hours.
	• Automated Fuel Burn: Dynamically calculates JP-8 aviation fuel and F-54 diesel consumption based on vehicle distance (L/100 km) or aircraft flight hours (L/hr) using live catalog fuel prices.
• Built-In Price Database & Item Manager ([>_]): Add custom items, edit unit prices, adjust fuel burn rates, or configure custom categories directly inside the app—changes save automatically to prices.json.
• Dark Mode & Classic Theme Toggle: Switch between classic light mode and dark mode inside the [>_] settings menu.
• Multi-Format Report Exporting:
	• PDF Reports with Barcodes: Generates a landscape operation summary complete with a Code 128 linear barcode (encoding the operation number and name) and a PDF417 2D barcode (encoding the operation number and logging model).
	• CSV & TXT Exports: Exports clean, itemized spreadsheets and plain-text breakdowns for easy sharing or archival.


How to Use


1. Set Up Operation Details & Personnel

1. Enter an Operation Name, Duration (days), and numeric Operation Number at the top of the window. (Note: Use standard ASCII characters in the Operation Name if you plan to export a PDF barcode).
2. Under Personnel, enter the Number of Troops and the Daily Pay / Allowance per Troop (CAD $).

2. Add Consumables, Equipment & Vehicles

1. Use the Quick Search bar or any dropdown under Catalog Selection by Category to pick an item.
2. Depending on what you selected, fill in the details that appear below:
	• For Consumables (Ammo, Rations, Fuel, Gear): Enter the Quantity expended and click Add Item.
	• For Weapons, Vehicles & Aircraft:
		• Qty to Acquire / Replace: Number of new/destroyed units to charge at full replacement cost.
		• Assets in Service: Number of firearms deployed (used to prorate annual maintenance over the operation's duration).
		• Usage (Fleet km / Flight Hours / Shots): Total combined distance, flight time, or full-charge shots across the fleet. Fuel costs are added automatically.
3. Click Add Asset to add the line item to the breakdown table. (To remove a mistake, highlight the row(s) in the table and click Remove Selected).

3. Save, Load, Calculate & Export

1. Click Calculate at the bottom-left to compute subtotals and the Grand Total in the Cost Summary box.
2. Click Export and choose .pdf, .csv, or .txt to save your report.
3. Click Save Operation to save your current operation and item list to a .json preset file, or Load Operation to restore a saved setup later.

4. Customize Prices & Settings ([>_])

• Click the [>_] button in the bottom-right corner to open the Price Database & Item Manager.
• Select any existing item to update its price, operating rate, or fuel burn—or fill out the fields and click Add to Catalog to create your own equipment.
• At the bottom of the manager window, you can switch the Theme between light and dark mode, or change the Logging Model version (saved in settings.json and embedded into exported PDF417 barcodes).


Disclaimer & Legal Notice

Operation Cost Calculator is a free, non-profit, community-oriented software project created strictly for educational, simulation, milsim, and game-prop purposes.

Non-Affiliation & Official Status

This project is in no way, shape, or form affiliated with, endorsed by, sponsored by, authorized by, or connected to the Canadian Armed Forces (CAF), the Canadian Army, the Department of National Defence (DND), or the Government of Canada. All trademarks, service marks, emblems, and logos referenced or displayed within this software remain the property of their respective owners and are used strictly for non-commercial, illustrative, and simulation purposes.

Usage, Modification & Distribution Terms

• Free & Non-Profit: This software is provided entirely free of charge for personal, educational, and non-commercial community use. It may not be sold, monetized, or bundled into commercial products.
• Right to Modify: Users are free to inspect, fork, and modify the source code and price catalog (prices.json) for their own personal or private community/milsim use.
• No Unauthorized Publication: You may not publicly redistribute, re-upload, mirror, or publish this software or any derivative/modified versions of it (in whole or in part) without the explicit prior written consent of the original author.

Accuracy & Simulation Data

• Estimated & Fictional Figures: All equipment prices, ammunition costs, fuel burn rates, operating expenses, and personnel allowance figures included in the default catalog are rough estimates, approximations, or fictionalized placeholders compiled from open-source information. They do not represent actual, classified, or official Department of National Defence procurement, logistics, or operational budgets.
• Generated Reports & Barcodes: Any exported reports, serial numbers, or barcodes (Code 128 / PDF417) are generated solely for immersion and organizational tracking within fictional or simulated scenarios and do not constitute official government or military records.

Limitation of Liability & No Warranty

THIS SOFTWARE IS PROVIDED "AS IS" AND "AS AVAILABLE," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, ACCURACY, OR NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE FOR ANY CLAIM, DIRECT, INDIRECT, INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES, OR ANY LOSS OF DATA OR PROFITS ARISING OUT OF OR IN CONNECTION WITH THE USE, MISUSE, OR INABILITY TO USE THIS SOFTWARE.
