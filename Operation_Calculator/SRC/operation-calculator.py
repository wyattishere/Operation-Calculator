"""Operation cost calculator; PDF export dependencies: reportlab, pdf417gen, Pillow.

Install PDF export dependencies with: python -m pip install reportlab pdf417gen Pillow
"""

import csv
import json
import os
import tkinter as tk
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from tkinter import filedialog, messagebox, ttk


def consumable(name, category, unit, price):
    return {
        "name": name,
        "category": category,
        "kind": "consumable",
        "unit": unit,
        "price": price,
        "operating_rate": "",
        "operating_unit": "",
        "fuel_burn": "",
        "fuel_basis": "",
        "fuel_item": "",
    }


def capital(
    name,
    category,
    kind,
    unit,
    price,
    operating_rate="",
    operating_unit="",
    fuel_burn="",
    fuel_basis="",
    fuel_item="",
):
    return {
        "name": name,
        "category": category,
        "kind": kind,
        "unit": unit,
        "price": price,
        "operating_rate": operating_rate,
        "operating_unit": operating_unit,
        "fuel_burn": fuel_burn,
        "fuel_basis": fuel_basis,
        "fuel_item": fuel_item,
    }


DEFAULT_CATALOG = [
    consumable("9×19mm NATO Ball (C22 Pistol)", "Handgun Ammo", "Round", "0.38"),
    consumable("5.56×45mm C79 Blank", "Rifle Ammo", "Round", "0.45"),
    consumable("5.56×45mm C77 Ball (C7A2 / C8A3 / CMAR)", "Rifle Ammo", "Round", "0.55"),
    consumable("5.56×45mm Linked (C9A2 LMG)", "Rifle Ammo", "Round", "0.65"),
    consumable("7.62×51mm Ball (C19 / C20)", "Rifle Ammo", "Round", "1.15"),
    consumable("7.62×51mm Linked (C6A1 FLEX GPMG)", "Rifle Ammo", "Round", "1.35"),
    consumable(".50 BMG / 12.7×99mm API (M2HB HMG)", "Rifle Ammo", "Round", "5.50"),
    consumable("40mm Low-Velocity HE Grenade (M203A1)", "Grenades/Underbarrel Grenades", "Grenade", "45.00"),
    consumable("C8 Smoke Grenade", "Grenades/Underbarrel Grenades", "Grenade", "55.00"),
    consumable("C13 Fragmentation Grenade", "Grenades/Underbarrel Grenades", "Grenade", "65.00"),
    consumable("84mm Carl Gustaf HEAT Round", "Grenade Launchers / Rocket Launchers (Karl Gustaf)", "Round", "1800.00"),
    consumable("155mm M795 High-Explosive (Shell + Charge + Fuze)", "Shells", "Complete Round", "3200.00"),
    consumable("TOW-2B Anti-Tank Guided Missile", "Rockets", "Missile", "85000.00"),
    consumable("155mm M982 Excalibur GPS-Guided Shell", "Shells", "Guided Shell", "125000.00"),
    consumable("JP-8 Aviation Fuel", "Fuel", "Litre", "1.45"),
    consumable("F-54 Bulk Diesel Fuel", "Fuel", "Litre", "1.65"),
    consumable("Bottled Water (24-Pack Case)", "Provisions", "Case", "8.00"),
    consumable("Individual Meal Pack (IMP) Combat Ration", "Provisions", "Meal Pack (3/day)", "9.50"),
    consumable("Fresh Field Rations", "Provisions", "Person-Day", "22.50"),
    consumable("Field Operations / Deployment Allowance", "Provisions", "Person-Day", "48.00"),
    consumable("CADPAT Rank / Unit Slip-On Patch", "Uniform", "Pair", "14.00"),
    consumable("CADPAT MT Combat Shirt & Trousers", "Uniform", "Set", "210.00"),
    consumable("Combat Boots (Temperate or Cold/Wet)", "Uniform", "Pair", "275.00"),
    consumable("CG634 Combat Helmet", "Uniform", "Unit", "750.00"),
    consumable("Fragmentation Vest & Ballistic Plates", "Uniform", "Set", "2400.00"),
    consumable("Monocular Night Vision Device (MNVD)", "Tactical Devices", "Unit", "6500.00"),
    capital("C22 Pistol (Sig P320)", "Snipers/Marksman Rifles/Rifles/Handguns", "weapon", "Unit", "525.00", "45.00", "year"),
    capital("C7A2 Assault Rifle (Bare)", "Snipers/Marksman Rifles/Rifles/Handguns", "weapon", "Unit", "2500.00", "180.00", "year"),
    capital("C9A2 Light Machine Gun", "Snipers/Marksman Rifles/Rifles/Handguns", "weapon", "Unit", "7200.00", "450.00", "year"),
    capital("CMAR Modular Rifle Kit (w/ Optic & Suppressor)", "Snipers/Marksman Rifles/Rifles/Handguns", "weapon", "Unit", "10240.00", "350.00", "year"),
    capital("C6A1 FLEX General-Purpose Machine Gun", "Snipers/Marksman Rifles/Rifles/Handguns", "weapon", "Unit", "13500.00", "750.00", "year"),
    capital("C14 Timberwolf Sniper Rifle (.338 Lapua)", "Snipers/Marksman Rifles/Rifles/Handguns", "weapon", "Unit", "14000.00", "600.00", "year"),
    capital("M2HB-QCB .50 Cal Heavy Machine Gun", "Snipers/Marksman Rifles/Rifles/Handguns", "weapon", "Unit", "24000.00", "1100.00", "year"),
    capital("M777 155mm Towed Howitzer", "Artillery", "weapon", "Unit", "4000000.00", "450.00", "full-charge shot"),
    capital("MSVS Mack Logistics Truck", "Ground Vehicles", "vehicle", "Vehicle", "550000.00", "3.20", "km", "42", "100 km", "F-54 Bulk Diesel Fuel"),
    capital("Tactical Armoured Patrol Vehicle (TAPV)", "Ground Vehicles", "vehicle", "Vehicle", "1200000.00", "8.50", "km", "55", "100 km", "F-54 Bulk Diesel Fuel"),
    capital("LAV 6.0 Infantry Fighting Vehicle", "Ground Vehicles", "vehicle", "Vehicle", "3500000.00", "24.00", "km", "85", "100 km", "F-54 Bulk Diesel Fuel"),
    capital("LAV 6.0 ACSV (Ambulance / Command / Repair)", "Ground Vehicles", "vehicle", "Vehicle", "8500000.00", "26.00", "km", "85", "100 km", "F-54 Bulk Diesel Fuel"),
    capital("Leopard 2A6M Main Battle Tank", "Ground Vehicles", "vehicle", "Vehicle", "9500000.00", "68.00", "km", "400", "100 km", "F-54 Bulk Diesel Fuel"),
    capital("CH-146 Griffon Utility Helicopter", "Air Vehicles", "aircraft", "Aircraft", "14000000.00", "5800.00", "flight hour", "380", "flight hour", "JP-8 Aviation Fuel"),
    capital("CH-147F Chinook Heavy-Lift Helicopter", "Air Vehicles", "aircraft", "Aircraft", "65000000.00", "14500.00", "flight hour", "1400", "flight hour", "JP-8 Aviation Fuel"),
    capital("CF-188 Hornet Fighter Jet", "Air Vehicles", "aircraft", "Aircraft", "65000000.00", "28000.00", "flight hour", "4500", "flight hour", "JP-8 Aviation Fuel"),
    capital("CC-130J Hercules Transport", "Air Vehicles", "aircraft", "Aircraft", "115000000.00", "16000.00", "flight hour", "2900", "flight hour", "JP-8 Aviation Fuel"),
]

LEGACY_DEFAULT_NAMES = {
    "5.56mm Round",
    "Body Armor Plate",
    "Service Rifle",
    "MRE Ration",
    "155mm Artillery Shell",
    "JP-8 Fuel per Liter",
    "JP-8 Fuel per Gallon",
}

SELECTION_CATEGORIES = (
    "Rifle Ammo",
    "Handgun Ammo",
    "Grenades/Underbarrel Grenades",
    "Shells",
    "Rockets",
    "Provisions",
    "Uniform",
    "Fuel",
    "Tactical Devices",
    "Snipers/Marksman Rifles/Rifles/Handguns",
    "Grenade Launchers / Rocket Launchers (Karl Gustaf)",
    "Artillery",
    "Air Vehicles",
    "Ground Vehicles",
)

SELECTION_FIELDS = SELECTION_CATEGORIES + ("Other / Custom",)
CATEGORIES = SELECTION_CATEGORIES + ("Other",)
DEFAULT_LOGGING_MODEL = "1.0.01"


def money(value):
    """Format a Decimal value consistently as Canadian dollars."""
    rounded = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return "CAD ${:,.2f}".format(rounded)


def number(value):
    """Format a quantity without unnecessary trailing zeroes."""
    if isinstance(value, Decimal):
        formatted = format(value, ",f")
        if "." in formatted:
            formatted = formatted.rstrip("0").rstrip(".")
        return formatted
    return "{:,}".format(value)


class OperationCostCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Operation Cost Calculator")
        self.root.minsize(1000, 800)

        self.icon_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "moneycalc.ico"
        )
        self.icon_image_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "moneycalc.png"
        )
        self.icon_image = tk.PhotoImage(
            master=self.root, file=self.icon_image_path
        )
        self.root.iconphoto(True, self.icon_image)
        self.root.iconbitmap(self.icon_path)
        self.root.iconbitmap(default=self.icon_path)
        self.catalog_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "prices.json"
        )
        self.settings_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "settings.json"
        )
        self.logo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "canadian_army_logo.png"
        )
        self.catalog = self._load_catalog()
        self.logging_model = self._load_settings()
        self.operation_items = []
        self.next_item_id = 0
        self.manager_window = None

        self._configure_style()
        self._build_main_window()
        self._refresh_item_choices()

    def _load_settings(self):
        if not os.path.exists(self.settings_path):
            return DEFAULT_LOGGING_MODEL
        try:
            with open(self.settings_path, "r", encoding="utf-8") as settings_file:
                data = json.load(settings_file)
            model = str(data.get("logging_model", "")).strip()
            if (
                not model
                or len(model) > 32
                or not model.isascii()
                or not model.isprintable()
            ):
                raise ValueError(
                    "The logging model must be 1-32 printable ASCII characters."
                )
            return model
        except (OSError, json.JSONDecodeError, AttributeError, ValueError) as exc:
            messagebox.showerror(
                "Settings Error",
                "Could not load settings.json. The default logging model will be used.\n\n"
                "{}".format(exc),
            )
            return DEFAULT_LOGGING_MODEL

    def save_logging_model(self):
        model = self.logging_model_var.get().strip()
        if (
            not model
            or len(model) > 32
            or not model.isascii()
            or not model.isprintable()
        ):
            messagebox.showerror(
                "Invalid Logging Model",
                "Enter a logging model from 1 to 32 printable ASCII characters.",
                parent=self.manager_window,
            )
            return

        temporary_path = self.settings_path + ".tmp"
        try:
            with open(temporary_path, "w", encoding="utf-8") as settings_file:
                json.dump({"logging_model": model}, settings_file, indent=2)
                settings_file.write("\n")
            os.replace(temporary_path, self.settings_path)
        except OSError as exc:
            if os.path.exists(temporary_path):
                try:
                    os.remove(temporary_path)
                except OSError:
                    pass
            messagebox.showerror(
                "Settings Save Error",
                "Could not save settings.json:\n{}".format(exc),
                parent=self.manager_window,
            )
            return

        self.logging_model = model
        messagebox.showinfo(
            "Settings Saved",
            "Logging model set to {}.".format(model),
            parent=self.manager_window,
        )

    def _configure_style(self):
        style = ttk.Style(self.root)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=("", 9, "bold"))
        style.configure("Total.TLabel", font=("", 11, "bold"))

    def _load_catalog(self):
        if not os.path.exists(self.catalog_path):
            catalog = [dict(item) for item in DEFAULT_CATALOG]
            try:
                self._write_catalog(catalog)
            except OSError as exc:
                messagebox.showerror(
                    "Catalog Error",
                    "Could not create prices.json:\n{}".format(exc),
                )
            return catalog

        try:
            with open(self.catalog_path, "r", encoding="utf-8") as catalog_file:
                data = json.load(catalog_file)
            if not isinstance(data, list):
                raise ValueError("The catalog must contain a list of items.")

            catalog = []
            seen_names = set()
            catalog_changed = False
            for entry in data:
                if not isinstance(entry, dict):
                    raise ValueError("Every catalog entry must be an object.")
                name = str(entry.get("name", "")).strip()
                category = str(entry.get("category", "")).strip()
                if name in LEGACY_DEFAULT_NAMES:
                    catalog_changed = True
                    continue
                if not name or not category:
                    raise ValueError(
                        "Catalog item names and categories cannot be empty."
                    )
                key = name.casefold()
                if key in seen_names:
                    raise ValueError("Catalog item names must be unique.")
                seen_names.add(key)
                kind = str(entry.get("kind", "consumable")).strip().lower()
                if kind not in ("consumable", "weapon", "vehicle", "aircraft"):
                    raise ValueError("Unknown catalog item type: {}.".format(kind))
                unit = str(entry.get("unit", "Unit")).strip()
                if not unit:
                    raise ValueError("Catalog billing units cannot be empty.")
                price = self._parse_nonnegative_decimal(
                    entry.get("price"), "replacement / unit cost"
                )
                operating_rate = entry.get("operating_rate", "")
                if operating_rate not in (None, ""):
                    operating_rate = str(
                        self._parse_nonnegative_decimal(
                            operating_rate, "operating rate"
                        )
                    )
                else:
                    operating_rate = ""
                operating_unit = str(entry.get("operating_unit", "")).strip()
                fuel_burn = entry.get("fuel_burn", "")
                if fuel_burn not in (None, ""):
                    fuel_burn = str(
                        self._parse_nonnegative_decimal(fuel_burn, "fuel burn rate")
                    )
                else:
                    fuel_burn = ""
                fuel_basis = str(entry.get("fuel_basis", "")).strip()
                fuel_item = str(entry.get("fuel_item", "")).strip()
                if bool(operating_rate) != bool(operating_unit):
                    raise ValueError(
                        "Catalog operating rates must include a billing unit."
                    )
                if operating_unit not in (
                    "",
                    "year",
                    "full-charge shot",
                    "km",
                    "flight hour",
                ):
                    raise ValueError(
                        "Unsupported operating rate unit: {}.".format(operating_unit)
                    )
                valid_operating_units = {
                    "weapon": ("year", "full-charge shot"),
                    "vehicle": ("km",),
                    "aircraft": ("flight hour",),
                    "consumable": (),
                }
                if operating_unit and operating_unit not in valid_operating_units[kind]:
                    raise ValueError(
                        "Operating rate unit '{}' does not match item type '{}'.".format(
                            operating_unit, kind
                        )
                    )
                if (
                    bool(fuel_burn) != bool(fuel_basis and fuel_item)
                    or (not fuel_burn and (fuel_basis or fuel_item))
                ):
                    raise ValueError(
                        "Catalog fuel burn entries require a basis and fuel item."
                    )
                if fuel_burn and Decimal(fuel_burn) == 0:
                    raise ValueError("Catalog fuel burn rates must be greater than zero.")
                if fuel_burn and (
                    (fuel_basis == "100 km" and kind != "vehicle")
                    or (fuel_basis == "flight hour" and kind != "aircraft")
                    or fuel_basis not in ("100 km", "flight hour")
                ):
                    raise ValueError(
                        "Fuel burn basis does not match the catalog item type."
                    )
                if kind == "consumable" and (
                    operating_rate or fuel_burn
                ):
                    raise ValueError(
                        "Consumables cannot have operating or fuel-burn rates."
                    )
                normalized = {
                    "name": name,
                    "category": category,
                    "kind": kind,
                    "unit": unit,
                    "price": str(price),
                    "operating_rate": operating_rate,
                    "operating_unit": operating_unit,
                    "fuel_burn": fuel_burn,
                    "fuel_basis": fuel_basis,
                    "fuel_item": fuel_item,
                }
                if normalized != entry:
                    catalog_changed = True
                catalog.append(normalized)

            catalog_indexes = {
                item["name"].casefold(): index
                for index, item in enumerate(catalog)
            }
            for preset in DEFAULT_CATALOG:
                preset_key = preset["name"].casefold()
                existing_index = catalog_indexes.get(preset_key)
                if existing_index is None:
                    catalog_indexes[preset_key] = len(catalog)
                    catalog.append(dict(preset))
                    seen_names.add(preset_key)
                    catalog_changed = True
                    continue
                migrated_preset = dict(preset)
                migrated_preset["price"] = catalog[existing_index]["price"]
                if migrated_preset != catalog[existing_index]:
                    catalog[existing_index] = migrated_preset
                    catalog_changed = True

            catalog_by_name = {
                item["name"]: item for item in catalog
            }
            for item in catalog:
                if item["fuel_item"]:
                    fuel = catalog_by_name.get(item["fuel_item"])
                    if (
                        fuel is None
                        or fuel["kind"] != "consumable"
                        or fuel["unit"].casefold() != "litre"
                    ):
                        raise ValueError(
                            "Fuel price item '{}' must exist as a consumable billed "
                            "per litre.".format(item["fuel_item"])
                        )

            if catalog_changed:
                try:
                    self._write_catalog(catalog)
                except OSError as exc:
                    messagebox.showerror(
                        "Catalog Error",
                        "Could not save the updated prices.json catalog:\n{}".format(
                            exc
                        ),
                    )
            return catalog
        except (OSError, json.JSONDecodeError, ValueError, InvalidOperation) as exc:
            messagebox.showerror(
                "Catalog Error",
                "Could not load prices.json. The built-in catalog will be used "
                "for this session.\n\n{}".format(exc),
            )
            return [dict(item) for item in DEFAULT_CATALOG]

    def _write_catalog(self, catalog):
        temporary_path = self.catalog_path + ".tmp"
        try:
            with open(temporary_path, "w", encoding="utf-8") as catalog_file:
                json.dump(catalog, catalog_file, indent=2)
                catalog_file.write("\n")
            os.replace(temporary_path, self.catalog_path)
        except OSError:
            if os.path.exists(temporary_path):
                try:
                    os.remove(temporary_path)
                except OSError:
                    pass
            raise

    @staticmethod
    def _parse_nonnegative_decimal(value, label):
        try:
            number = Decimal(str(value).strip())
        except (InvalidOperation, ValueError):
            raise ValueError("{} must be a valid number.".format(label))
        if not number.is_finite():
            raise ValueError("{} must be a finite number.".format(label))
        if number < 0:
            raise ValueError("{} cannot be negative.".format(label))
        return number

    @staticmethod
    def _parse_nonnegative_integer(value, label):
        try:
            number = int(str(value).strip())
        except (ValueError, TypeError):
            raise ValueError("{} must be a whole number.".format(label))
        if number < 0:
            raise ValueError("{} cannot be negative.".format(label))
        return number

    @staticmethod
    def _parse_operation_number(value):
        operation_number = str(value).strip()
        if not operation_number or not operation_number.isascii() or not operation_number.isdigit():
            raise ValueError("Operation Number must contain digits only.")
        return operation_number

    def _build_main_window(self):
        container = ttk.Frame(self.root, padding=12)
        container.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(3, weight=0)
        container.rowconfigure(5, weight=1)

        header = ttk.Frame(container)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        header.columnconfigure(0, weight=1)
        ttk.Label(
            header,
            text="Operation Cost Calculator",
            font=("TkDefaultFont", 16, "bold"),
        ).grid(row=0, column=0, sticky="w")
        self.logo_image = tk.PhotoImage(
            master=self.root, file=self.logo_path
        ).subsample(4, 4)
        ttk.Label(header, image=self.logo_image).grid(
            row=0, column=1, sticky="e"
        )

        details = ttk.LabelFrame(container, text="Operation Details", padding=10)
        details.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        details.columnconfigure(1, weight=1)
        ttk.Label(details, text="Operation Name:").grid(
            row=0, column=0, sticky="w", padx=(0, 8), pady=3
        )
        self.operation_name = tk.StringVar()
        ttk.Entry(details, textvariable=self.operation_name).grid(
            row=0, column=1, sticky="ew", pady=3
        )
        ttk.Label(details, text="Duration (days):").grid(
            row=0, column=2, sticky="w", padx=(18, 8), pady=3
        )
        self.duration = tk.StringVar(value="0")
        ttk.Entry(details, textvariable=self.duration, width=12).grid(
            row=0, column=3, sticky="w", padx=(0, 12), pady=3
        )
        ttk.Label(details, text="Operation Number:").grid(
            row=0, column=4, sticky="w", padx=(6, 8), pady=3
        )
        self.operation_number = tk.StringVar()
        ttk.Entry(details, textvariable=self.operation_number, width=12).grid(
            row=0, column=5, sticky="w", pady=3
        )

        personnel = ttk.LabelFrame(container, text="Personnel", padding=10)
        personnel.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        for column in range(4):
            personnel.columnconfigure(column, weight=1 if column in (1, 3) else 0)
        ttk.Label(personnel, text="Number of Troops:").grid(
            row=0, column=0, sticky="w", padx=(0, 8), pady=3
        )
        self.troop_count = tk.StringVar(value="0")
        ttk.Entry(personnel, textvariable=self.troop_count, width=14).grid(
            row=0, column=1, sticky="ew", pady=3
        )
        ttk.Label(personnel, text="Daily Pay / Allowance per Troop (CAD $):").grid(
            row=0, column=2, sticky="w", padx=(18, 8), pady=3
        )
        self.daily_pay = tk.StringVar(value="0")
        ttk.Entry(personnel, textvariable=self.daily_pay, width=16).grid(
            row=0, column=3, sticky="ew", pady=3
        )

        selection = ttk.LabelFrame(
            container, text="Catalog Selection by Category", padding=10
        )
        selection.grid(row=3, column=0, sticky="ew", pady=(0, 8))
        for column in (1, 3):
            selection.columnconfigure(column, weight=1)
        self.category_selection_vars = {}
        self.category_combos = {}
        for index, category in enumerate(SELECTION_FIELDS):
            row = index // 2
            label_column = 0 if index % 2 == 0 else 2
            combo_column = label_column + 1
            label_text = category
            ttk.Label(
                selection,
                text=label_text,
                wraplength=250,
                justify="left",
            ).grid(row=row, column=label_column, sticky="w", padx=(4, 8), pady=3)
            category_var = tk.StringVar()
            category_combo = ttk.Combobox(
                selection,
                textvariable=category_var,
                state="readonly",
            )
            category_combo.grid(
                row=row,
                column=combo_column,
                sticky="ew",
                padx=(0, 12),
                pady=3,
            )
            category_combo.bind(
                "<<ComboboxSelected>>",
                lambda _event, selected_category=category: self._on_category_selected(
                    selected_category
                ),
            )
            self.category_selection_vars[category] = category_var
            self.category_combos[category] = category_combo

        entry_frame = ttk.LabelFrame(container, text="Selected Item Details", padding=8)
        entry_frame.grid(row=4, column=0, sticky="ew", pady=(0, 8))
        entry_frame.columnconfigure(0, weight=1)
        self.selected_item = tk.StringVar()
        self.selected_asset = tk.StringVar()
        self.selection_detail = tk.StringVar(
            value="Select an item from one of the category fields above."
        )
        ttk.Label(
            entry_frame,
            textvariable=self.selection_detail,
            wraplength=950,
            justify="left",
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        consumable_controls = ttk.Frame(entry_frame)
        consumable_controls.grid(row=1, column=0, sticky="ew")
        consumable_controls.columnconfigure(0, weight=1)
        ttk.Label(consumable_controls, text="Quantity:").grid(
            row=0, column=1, sticky="w", padx=(0, 6)
        )
        self.item_quantity = tk.StringVar(value="1")
        ttk.Entry(
            consumable_controls, textvariable=self.item_quantity, width=12
        ).grid(row=0, column=2, padx=(0, 8))
        ttk.Button(
            consumable_controls, text="Add Item", command=self.add_operation_item
        ).grid(row=0, column=3)
        self.consumable_controls = consumable_controls
        self.consumable_controls.grid_remove()

        asset_controls = ttk.Frame(entry_frame)
        asset_controls.grid(row=2, column=0, sticky="ew")
        ttk.Label(asset_controls, text="Qty to Acquire / Replace:").grid(
            row=0, column=0, padx=(0, 5)
        )
        self.asset_quantity = tk.StringVar(value="0")
        ttk.Entry(asset_controls, textvariable=self.asset_quantity, width=8).grid(
            row=0, column=1, padx=(0, 10)
        )
        ttk.Label(asset_controls, text="Assets in Service:").grid(
            row=0, column=2, padx=(0, 5)
        )
        self.asset_service_count = tk.StringVar(value="0")
        self.asset_service_entry = ttk.Entry(
            asset_controls, textvariable=self.asset_service_count, width=8
        )
        self.asset_service_entry.grid(row=0, column=3, padx=(0, 10))
        self.activity_label = tk.StringVar(value="Usage:")
        ttk.Label(asset_controls, textvariable=self.activity_label).grid(
            row=0, column=4, padx=(0, 5)
        )
        self.asset_activity = tk.StringVar(value="0")
        self.asset_activity_entry = ttk.Entry(
            asset_controls, textvariable=self.asset_activity, width=10
        )
        self.asset_activity_entry.grid(row=0, column=5, padx=(0, 10))
        ttk.Button(asset_controls, text="Add Asset", command=self.add_asset).grid(
            row=0, column=6
        )
        self.asset_detail = tk.StringVar(
            value=(
                "Acquisition costs use Qty to Acquire / Replace. Annual firearm "
                "rates use Assets in Service prorated by operation days; vehicle "
                "and aircraft usage is total fleet activity, with fuel added separately."
            )
        )
        self.asset_detail_label = ttk.Label(
            entry_frame,
            textvariable=self.asset_detail,
            wraplength=950,
            justify="left",
        )
        self.asset_detail_label.grid(row=3, column=0, sticky="w", pady=(6, 0))
        self.asset_controls = asset_controls
        self.asset_controls.grid_remove()
        self.asset_detail_label.grid_remove()

        breakdown = ttk.LabelFrame(
            container, text="Itemized Cost Breakdown", padding=10
        )
        breakdown.grid(row=5, column=0, sticky="nsew", pady=(0, 8))
        breakdown.columnconfigure(0, weight=1)
        breakdown.rowconfigure(0, weight=1)
        item_columns = (
            "name",
            "category",
            "unit",
            "quantity",
            "unit_cost",
            "replacement",
            "operating",
            "fuel",
            "line_total",
        )
        self.items_tree = ttk.Treeview(
            breakdown, columns=item_columns, show="headings", selectmode="extended"
        )
        headings = (
            ("name", "Item Name", 280, "w"),
            ("category", "Category", 190, "w"),
            ("unit", "Billing Unit", 125, "w"),
            ("quantity", "Qty / Assets", 110, "e"),
            ("unit_cost", "Unit / Replacement Cost", 155, "e"),
            ("replacement", "Acquisition Total", 145, "e"),
            ("operating", "Operating Cost", 145, "e"),
            ("fuel", "Fuel Cost", 130, "e"),
            ("line_total", "Line Total", 150, "e"),
        )
        for column, title, width, anchor in headings:
            self.items_tree.heading(column, text=title)
            self.items_tree.column(column, width=width, minwidth=90, anchor=anchor)
        item_scroll = ttk.Scrollbar(
            breakdown, orient="vertical", command=self.items_tree.yview
        )
        horizontal_scroll = ttk.Scrollbar(
            breakdown, orient="horizontal", command=self.items_tree.xview
        )
        self.items_tree.configure(
            yscrollcommand=item_scroll.set, xscrollcommand=horizontal_scroll.set
        )
        self.items_tree.grid(row=0, column=0, sticky="nsew")
        item_scroll.grid(row=0, column=1, sticky="ns")
        horizontal_scroll.grid(row=1, column=0, sticky="ew")
        ttk.Button(
            breakdown,
            text="Remove Selected",
            command=self.remove_operation_items,
        ).grid(row=2, column=0, sticky="e", pady=(8, 0))

        results = ttk.LabelFrame(container, text="Cost Summary", padding=10)
        results.grid(row=6, column=0, sticky="ew", pady=(0, 8))
        results.columnconfigure(0, weight=1)
        self.summary_text = tk.StringVar(value="Select Calculate to view the breakdown.")
        ttk.Label(
            results, textvariable=self.summary_text, justify="left", anchor="nw"
        ).grid(row=0, column=0, sticky="nsew")

        actions = ttk.Frame(container)
        actions.grid(row=7, column=0, sticky="ew")
        ttk.Button(actions, text="Calculate", command=self.calculate).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(actions, text="Clear / Reset", command=self.reset).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(actions, text="Export", command=self.export).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(actions, text="[>_]", command=self.open_catalog_manager).pack(
            side="right"
        )

    def _refresh_item_choices(self):
        for category, combo in self.category_combos.items():
            if category == "Other / Custom":
                items = [
                    item
                    for item in self.catalog
                    if item["category"] not in SELECTION_CATEGORIES
                ]
            else:
                items = [
                    item for item in self.catalog if item["category"] == category
                ]
            names = sorted((item["name"] for item in items), key=str.casefold)
            combo["values"] = names
            if self.category_selection_vars[category].get() not in names:
                self.category_selection_vars[category].set("")

        selected_name = self.selected_item.get() or self.selected_asset.get()
        selected = self._find_catalog_item(selected_name) if selected_name else None
        if selected is None:
            self.selected_item.set("")
            self.selected_asset.set("")
            self.selection_detail.set(
                "Select an item from one of the category fields above."
            )
            self.consumable_controls.grid_remove()
            self.asset_controls.grid_remove()
            self.asset_detail_label.grid_remove()
            return

        category = (
            selected["category"]
            if selected["category"] in SELECTION_CATEGORIES
            else "Other / Custom"
        )
        for field, variable in self.category_selection_vars.items():
            variable.set(selected_name if field == category else "")
        self._on_category_selected(category)

    def _on_category_selected(self, category):
        selected_name = self.category_selection_vars[category].get().strip()
        if not selected_name:
            return
        item = self._find_catalog_item(selected_name)
        if item is None:
            self._refresh_item_choices()
            return

        for field, variable in self.category_selection_vars.items():
            if field != category:
                variable.set("")
        if item["kind"] == "consumable":
            self.selected_item.set(item["name"])
            self.selected_asset.set("")
            self.selection_detail.set(
                "{} — {} per {}".format(
                    item["name"], money(Decimal(item["price"])), item["unit"]
                )
            )
            self.asset_controls.grid_remove()
            self.asset_detail_label.grid_remove()
            self.consumable_controls.grid()
        else:
            self.selected_asset.set(item["name"])
            self.selected_item.set("")
            self.selection_detail.set(
                "{} — {} replacement cost per {}".format(
                    item["name"], money(Decimal(item["price"])), item["unit"]
                )
            )
            self.consumable_controls.grid_remove()
            self.asset_controls.grid()
            self.asset_detail_label.grid()
            self._update_asset_form()

    def add_operation_item(self):
        name = self.selected_item.get().strip()
        if not name:
            messagebox.showerror("Invalid Item", "Select an item from the catalog.")
            return
        catalog_item = next(
            (item for item in self.catalog if item["name"] == name), None
        )
        if catalog_item is None:
            messagebox.showerror(
                "Item Unavailable", "That item is no longer in the price catalog."
            )
            self._refresh_item_choices()
            return

        try:
            if catalog_item["unit"].casefold() == "litre":
                quantity = self._parse_nonnegative_decimal(
                    self.item_quantity.get(), "Quantity expended"
                )
            else:
                quantity = self._parse_nonnegative_integer(
                    self.item_quantity.get(), "Quantity expended"
                )
            if quantity == 0:
                raise ValueError("Quantity expended must be greater than zero.")
        except ValueError as exc:
            messagebox.showerror("Invalid Quantity", str(exc))
            return

        entry = {
            "name": catalog_item["name"],
            "category": catalog_item["category"],
            "kind": catalog_item["kind"],
            "unit": catalog_item["unit"],
            "unit_price": Decimal(catalog_item["price"]),
            "quantity": quantity,
            "service_count": 0,
            "activity": Decimal("0"),
            "operating_rate": Decimal("0"),
            "operating_unit": "",
            "fuel_burn": Decimal("0"),
            "fuel_basis": "",
            "fuel_item": "",
            "fuel_price": Decimal("0"),
            "row_id": str(self.next_item_id),
        }
        self.next_item_id += 1
        self.operation_items.append(entry)
        self._insert_operation_item(entry)
        self.summary_text.set("Select Calculate to view the breakdown.")

    def _insert_operation_item(self, item):
        try:
            duration = self._parse_nonnegative_integer(
                self.duration.get(), "Duration in days"
            )
        except ValueError:
            duration = 0
        costs = self._calculate_item_costs(item, duration)
        if item["kind"] == "consumable":
            quantity_label = "{} {}".format(
                number(item["quantity"]), item["unit"]
            )
        else:
            quantity_label = "{} acquired; {} in service".format(
                number(item["quantity"]),
                number(item["service_count"]),
            )
            if item["activity"]:
                quantity_label += "; {} {}".format(
                    number(item["activity"]), item["operating_unit"]
                )
        self.items_tree.insert(
            "",
            "end",
            iid=item["row_id"],
            values=(
                item["name"],
                item["category"],
                item["unit"],
                quantity_label,
                money(item["unit_price"]),
                money(costs["replacement"]),
                money(costs["operating"]),
                money(costs["fuel"]),
                money(costs["total"]),
            ),
        )

    def _find_catalog_item(self, name):
        return next((item for item in self.catalog if item["name"] == name), None)

    def _update_asset_form(self, _event=None):
        item = self._find_catalog_item(self.selected_asset.get().strip())
        if item is None:
            self.activity_label.set("Usage:")
            self.asset_detail.set(
                "Acquisition costs use Qty to Acquire / Replace. Annual firearm "
                "rates use Assets in Service prorated by operation days; vehicle "
                "and aircraft usage is total fleet activity, with fuel added separately."
            )
            self.asset_activity_entry.configure(state="normal")
            self.asset_service_entry.configure(state="normal")
            return

        if item["operating_unit"] == "year":
            self.activity_label.set("Usage (duration-based):")
            self.asset_activity.set("0")
            self.asset_activity_entry.configure(state="disabled")
            self.asset_service_entry.configure(state="normal")
        else:
            self.asset_service_count.set("0")
            self.asset_service_entry.configure(state="disabled")
            if not item["operating_rate"] and not item["fuel_burn"]:
                self.activity_label.set("Usage (not applicable):")
                self.asset_activity.set("0")
                self.asset_activity_entry.configure(state="disabled")
            elif item["operating_unit"] == "full-charge shot":
                self.asset_activity_entry.configure(state="normal")
                self.activity_label.set("Full-charge shots:")
            elif item["kind"] == "vehicle":
                self.asset_activity_entry.configure(state="normal")
                self.activity_label.set("Total fleet km:")
            elif item["kind"] == "aircraft":
                self.asset_activity_entry.configure(state="normal")
                self.activity_label.set("Total fleet flight hours:")
            else:
                self.asset_activity_entry.configure(state="normal")
                self.activity_label.set("Usage:")

        details = "Replacement cost: {} per {}.".format(
            money(Decimal(item["price"])), item["unit"]
        )
        if item["operating_rate"]:
            details += " Operating: {} per {}.".format(
                money(Decimal(item["operating_rate"])), item["operating_unit"]
            )
        if item["fuel_burn"]:
            details += " Fuel burn: {} L per {}; fuel price from {}.".format(
                item["fuel_burn"], item["fuel_basis"], item["fuel_item"]
            )
        details += (
            " Acquisition costs use the acquire/replace quantity; annual rates "
            "are prorated by operation duration. Vehicle/aircraft usage is total "
            "fleet activity; fuel is added separately."
        )
        self.asset_detail.set(details)

    def add_asset(self):
        catalog_item = self._find_catalog_item(self.selected_asset.get().strip())
        if catalog_item is None or catalog_item["kind"] == "consumable":
            messagebox.showerror("Invalid Asset", "Select a capital asset from the catalog.")
            return
        try:
            quantity = self._parse_nonnegative_integer(
                self.asset_quantity.get(), "Quantity to acquire / replace"
            )
            service_count = self._parse_nonnegative_integer(
                self.asset_service_count.get(), "Assets in service"
            )
            activity = self._parse_nonnegative_decimal(
                self.asset_activity.get(), "Asset operating usage"
            )
            duration = self._parse_nonnegative_integer(
                self.duration.get(), "Duration in days"
            )
        except ValueError as exc:
            messagebox.showerror("Invalid Asset Input", str(exc))
            return

        if quantity == 0 and service_count == 0 and activity == 0:
            messagebox.showerror(
                "Invalid Asset Input",
                "Enter an acquisition quantity, assets in service, or positive usage.",
            )
            return
        if (
            catalog_item["operating_unit"] == "year"
            and service_count == 0
            and quantity == 0
        ):
            messagebox.showerror(
                "Invalid Asset Input",
                "Enter the number of assets in service for annual maintenance costs.",
            )
            return
        if catalog_item["operating_unit"] not in ("", "year") and activity == 0 and quantity == 0:
            messagebox.showerror(
                "Invalid Asset Input",
                "Enter positive usage for this asset, or a quantity to acquire / replace.",
            )
            return

        fuel_price = Decimal("0")
        if catalog_item["fuel_item"]:
            fuel = self._find_catalog_item(catalog_item["fuel_item"])
            if fuel is None:
                messagebox.showerror(
                    "Fuel Price Missing",
                    "The catalog fuel item '{}' is missing.".format(
                        catalog_item["fuel_item"]
                    ),
                )
                return
            fuel_price = Decimal(fuel["price"])

        entry = {
            "name": catalog_item["name"],
            "category": catalog_item["category"],
            "kind": catalog_item["kind"],
            "unit": catalog_item["unit"],
            "unit_price": Decimal(catalog_item["price"]),
            "quantity": quantity,
            "service_count": service_count,
            "activity": activity,
            "operating_rate": Decimal(catalog_item["operating_rate"] or "0"),
            "operating_unit": catalog_item["operating_unit"],
            "fuel_burn": Decimal(catalog_item["fuel_burn"] or "0"),
            "fuel_basis": catalog_item["fuel_basis"],
            "fuel_item": catalog_item["fuel_item"],
            "fuel_price": fuel_price,
            "row_id": str(self.next_item_id),
        }
        self.next_item_id += 1
        self.operation_items.append(entry)
        self._insert_operation_item(entry)
        self.summary_text.set("Select Calculate to view the breakdown.")

    @staticmethod
    def _calculate_item_costs(item, duration):
        replacement = item["unit_price"] * item["quantity"]
        operating = Decimal("0")
        fuel = Decimal("0")

        if item["kind"] == "weapon":
            if item["operating_unit"] == "year":
                operating = (
                    item["operating_rate"]
                    * item["service_count"]
                    * Decimal(duration)
                    / Decimal("365")
                )
            elif item["operating_unit"] == "full-charge shot":
                operating = item["operating_rate"] * item["activity"]
        elif item["kind"] in ("vehicle", "aircraft"):
            operating = item["operating_rate"] * item["activity"]
            if item["fuel_burn"] and item["fuel_basis"]:
                burn_quantity = item["fuel_burn"] * item["activity"]
                if item["fuel_basis"] == "100 km":
                    burn_quantity /= Decimal("100")
                fuel = burn_quantity * item["fuel_price"]

        if item["kind"] == "consumable":
            replacement = item["unit_price"] * item["quantity"]
        return {
            "replacement": replacement,
            "operating": operating,
            "fuel": fuel,
            "total": replacement + operating + fuel,
        }

    def remove_operation_items(self):
        selected = self.items_tree.selection()
        if not selected:
            return
        selected_ids = set(selected)
        self.operation_items = [
            item
            for item in self.operation_items
            if item["row_id"] not in selected_ids
        ]
        self.items_tree.delete(*selected)
        self.summary_text.set("Select Calculate to view the breakdown.")

    def calculate(self):
        try:
            operation_number = self._parse_operation_number(
                self.operation_number.get()
            )
            duration = self._parse_nonnegative_integer(
                self.duration.get(), "Duration in days"
            )
            troops = self._parse_nonnegative_integer(
                self.troop_count.get(), "Number of troops"
            )
            daily_pay = self._parse_nonnegative_decimal(
                self.daily_pay.get(), "Daily pay / allowance"
            )
        except ValueError as exc:
            messagebox.showerror("Invalid Input", str(exc))
            return

        personnel_total = Decimal(troops) * daily_pay * duration
        totals = {
            "consumables": Decimal("0"),
            "replacement": Decimal("0"),
            "operating": Decimal("0"),
            "fuel": Decimal("0"),
        }
        for item in self.operation_items:
            costs = self._calculate_item_costs(item, duration)
            if item["kind"] == "consumable":
                totals["consumables"] += costs["total"]
            else:
                totals["replacement"] += costs["replacement"]
                totals["operating"] += costs["operating"]
                totals["fuel"] += costs["fuel"]
            self._update_operation_row(item, duration, costs)

        grand_total = personnel_total + sum(totals.values(), Decimal("0"))
        self.last_summary = {
            "personnel": personnel_total,
            **totals,
            "grand_total": grand_total,
        }
        self.summary_text.set(
            "Operation #{}\n"
            "Personnel ({} troops x {} days): {}\n"
            "Consumables & gear: {}\n"
            "Capital replacement / acquisition: {}\n"
            "Asset operating costs: {}\n"
            "Fuel: {}\n"
            "Grand Total: {}".format(
                operation_number,
                "{:,}".format(troops),
                "{:,}".format(duration),
                money(personnel_total),
                money(totals["consumables"]),
                money(totals["replacement"]),
                money(totals["operating"]),
                money(totals["fuel"]),
                money(grand_total),
            )
        )

    def _update_operation_row(self, item, duration, costs=None):
        if costs is None:
            costs = self._calculate_item_costs(item, duration)
        if item["kind"] == "consumable":
            quantity_label = "{} {}".format(
                number(item["quantity"]), item["unit"]
            )
        else:
            quantity_label = "{} acquired; {} in service".format(
                number(item["quantity"]),
                number(item["service_count"]),
            )
            if item["activity"]:
                usage_unit = {
                    "km": "km fleet",
                    "flight hour": "flight hours",
                    "full-charge shot": "full-charge shots",
                }.get(item["operating_unit"], item["operating_unit"])
                quantity_label += "; {} {}".format(number(item["activity"]), usage_unit)
        self.items_tree.item(
            item["row_id"],
            values=(
                item["name"],
                item["category"],
                item["unit"],
                quantity_label,
                money(item["unit_price"]),
                money(costs["replacement"]),
                money(costs["operating"]),
                money(costs["fuel"]),
                money(costs["total"]),
            ),
        )

    def reset(self):
        self.operation_name.set("")
        self.operation_number.set("")
        self.duration.set("0")
        self.troop_count.set("0")
        self.daily_pay.set("0")
        self.selected_item.set("")
        self.selected_asset.set("")
        for variable in self.category_selection_vars.values():
            variable.set("")
        self.item_quantity.set("1")
        self.asset_quantity.set("0")
        self.asset_service_count.set("0")
        self.asset_activity.set("0")
        self.selection_detail.set(
            "Select an item from one of the category fields above."
        )
        self.consumable_controls.grid_remove()
        self.asset_controls.grid_remove()
        self.asset_detail_label.grid_remove()
        self._update_asset_form()
        self.operation_items.clear()
        self.items_tree.delete(*self.items_tree.get_children())
        self.summary_text.set("Select Calculate to view the breakdown.")
        self.last_summary = None

    def export(self):
        try:
            self._get_calculation_data()
        except ValueError as exc:
            messagebox.showerror("Invalid Input", str(exc))
            return

        path = filedialog.asksaveasfilename(
            title="Export Operation Cost Report",
            defaultextension=".pdf",
            filetypes=(
                ("PDF report with barcodes", "*.pdf"),
                ("CSV files", "*.csv"),
                ("Text files", "*.txt"),
            ),
        )
        if not path:
            return
        try:
            if path.lower().endswith(".pdf"):
                self._export_pdf(path)
            elif path.lower().endswith(".txt"):
                self._export_text(path)
            elif path.lower().endswith(".csv"):
                self._export_csv(path)
            else:
                raise ValueError("Choose a PDF, CSV, or TXT file extension.")
        except (OSError, ValueError, RuntimeError) as exc:
            messagebox.showerror("Export Error", "Could not save the export:\n{}".format(exc))
            return
        messagebox.showinfo("Export Complete", "Breakdown saved to:\n{}".format(path))

    def _get_calculation_data(self):
        operation_name = self.operation_name.get().strip()
        if not operation_name:
            raise ValueError("Operation Name cannot be empty.")
        operation_number = self._parse_operation_number(
            self.operation_number.get()
        )
        duration = self._parse_nonnegative_integer(
            self.duration.get(), "Duration in days"
        )
        troops = self._parse_nonnegative_integer(
            self.troop_count.get(), "Number of troops"
        )
        daily_pay = self._parse_nonnegative_decimal(
            self.daily_pay.get(), "Daily pay / allowance"
        )
        totals = {
            "personnel": Decimal(troops) * daily_pay * duration,
            "consumables": Decimal("0"),
            "replacement": Decimal("0"),
            "operating": Decimal("0"),
            "fuel": Decimal("0"),
        }
        line_costs = {}
        for item in self.operation_items:
            costs = self._calculate_item_costs(item, duration)
            line_costs[item["row_id"]] = costs
            if item["kind"] == "consumable":
                totals["consumables"] += costs["total"]
            else:
                totals["replacement"] += costs["replacement"]
                totals["operating"] += costs["operating"]
                totals["fuel"] += costs["fuel"]
        totals["grand_total"] = sum(totals.values(), Decimal("0"))
        return operation_name, operation_number, duration, troops, totals, line_costs

    def _export_text(self, path):
        operation_name, operation_number, duration, troops, totals, line_costs = (
            self._get_calculation_data()
        )
        with open(path, "w", encoding="utf-8") as output:
            output.write("Operation Cost Breakdown (CAD)\n")
            output.write("Operation: {}\n".format(operation_name))
            output.write("Operation Number: {}\n".format(operation_number))
            output.write("Logging Model: {}\n".format(self.logging_model))
            output.write("Duration: {} days\n\n".format(duration))
            output.write(
                "Personnel: {} troops - {}\n\n".format(
                    "{:,}".format(troops), money(totals["personnel"])
                )
            )
            writer = csv.writer(output, delimiter="\t", lineterminator="\n")
            writer.writerow(
                (
                    "Item",
                    "Category",
                    "Billing Unit",
                    "Acquired / Quantity",
                    "In Service",
                    "Usage",
                    "Acquisition",
                    "Operating",
                    "Fuel",
                    "Line Total",
                )
            )
            if self.operation_items:
                for item in self.operation_items:
                    costs = line_costs[item["row_id"]]
                    writer.writerow(
                        (
                            item["name"],
                            item["category"],
                            item["unit"],
                            item["quantity"],
                            item["service_count"],
                            item["activity"],
                            money(costs["replacement"]),
                            money(costs["operating"]),
                            money(costs["fuel"]),
                            money(costs["total"]),
                        )
                    )
            else:
                output.write("No equipment or capital asset entries.\n")
            output.write("\nPersonnel subtotal: {}\n".format(money(totals["personnel"])))
            output.write("Consumables & gear: {}\n".format(money(totals["consumables"])))
            output.write("Capital replacement / acquisition: {}\n".format(
                money(totals["replacement"])
            ))
            output.write("Asset operating costs: {}\n".format(money(totals["operating"])))
            output.write("Fuel: {}\n".format(money(totals["fuel"])))
            output.write("Grand Total: {}\n".format(money(totals["grand_total"])))

    def _export_csv(self, path):
        operation_name, operation_number, duration, troops, totals, line_costs = (
            self._get_calculation_data()
        )
        with open(path, "w", newline="", encoding="utf-8") as output:
            writer = csv.writer(output)
            writer.writerow(("Operation Cost Breakdown",))
            writer.writerow(("Currency", "CAD"))
            writer.writerow(("Operation", operation_name))
            writer.writerow(("Operation Number", operation_number))
            writer.writerow(("Logging Model", self.logging_model))
            writer.writerow(("Duration (days)", duration))
            writer.writerow(())
            writer.writerow(
                (
                    "Item Name",
                    "Category",
                    "Billing Unit",
                    "Quantity / Assets Acquired",
                    "Assets in Service",
                    "Usage",
                    "Unit / Replacement Cost",
                    "Acquisition Total",
                    "Operating Cost",
                    "Fuel Cost",
                    "Line Total",
                )
            )
            writer.writerow(
                (
                    "Personnel",
                    "Personnel",
                    "Person-Day",
                    "",
                    "",
                    "{} troops x {} days".format(
                        "{:,}".format(troops), "{:,}".format(duration)
                    ),
                    "",
                    "",
                    "",
                    "",
                    "",
                    money(totals["personnel"]),
                )
            )
            for item in self.operation_items:
                costs = line_costs[item["row_id"]]
                writer.writerow(
                    (
                        item["name"],
                        item["category"],
                        item["unit"],
                        item["quantity"],
                        item["service_count"],
                        "{} {}".format(item["activity"], item["operating_unit"]),
                        money(item["unit_price"]),
                        money(costs["replacement"]),
                        money(costs["operating"]),
                        money(costs["fuel"]),
                        money(costs["total"]),
                    )
                )
            writer.writerow(())
            writer.writerow(("Personnel subtotal", money(totals["personnel"])))
            writer.writerow(("Consumables & gear", money(totals["consumables"])))
            writer.writerow(
                ("Capital replacement / acquisition", money(totals["replacement"]))
            )
            writer.writerow(("Asset operating costs", money(totals["operating"])))
            writer.writerow(("Fuel", money(totals["fuel"])))
            writer.writerow(("Grand Total", money(totals["grand_total"])))

    def _export_pdf(self, path):
        try:
            import pdf417gen
            from reportlab.graphics.barcode.code128 import Code128
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import landscape, letter
            from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
            from reportlab.lib.utils import ImageReader
            from reportlab.pdfgen.canvas import Canvas
            from reportlab.platypus import (
                LongTable,
                Paragraph,
                SimpleDocTemplate,
                Spacer,
                Table,
                TableStyle,
            )
        except ImportError as exc:
            raise RuntimeError(
                "PDF barcode export requires reportlab, pdf417gen, and Pillow. "
                "Install them with: python -m pip install reportlab pdf417gen Pillow"
            ) from exc

        operation_name, operation_number, duration, troops, totals, line_costs = (
            self._get_calculation_data()
        )
        barcode_text = "OPERATION #{} {}".format(
            operation_number, operation_name.upper()
        )
        if not barcode_text.isascii() or any(
            ord(character) < 32 or ord(character) > 126
            for character in barcode_text
        ):
            raise ValueError(
                "Code 128 requires an operation name using standard ASCII characters."
            )
        pdf417_text = "OPERATION_NUMBER={};LOGGING_MODEL={}".format(
            operation_number, self.logging_model
        )

        try:
            pdf417_codes = pdf417gen.encode(
                pdf417_text, columns=6, security_level=2
            )
            pdf417_image = pdf417gen.render_image(
                pdf417_codes, scale=4, ratio=3, padding=8
            )
        except ImportError as exc:
            raise RuntimeError(
                "PDF417 image rendering requires Pillow. "
                "Install dependencies with: python -m pip install Pillow"
            ) from exc
        except ValueError as exc:
            raise RuntimeError("Could not encode the PDF417 barcode: {}".format(exc)) from exc

        page_size = landscape(letter)
        page_width, page_height = page_size
        margin = 36
        logo_reader = ImageReader(self.logo_path)
        logo_pixel_width, logo_pixel_height = logo_reader.getSize()
        pdf_logo_width = 160
        pdf_logo_height = pdf_logo_width * logo_pixel_height / logo_pixel_width
        pdf_logo_x = page_width - margin - pdf_logo_width
        pdf_logo_y = page_height - 20 - pdf_logo_height
        styles = getSampleStyleSheet()
        item_style = ParagraphStyle(
            "BarcodeReportCell",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=7,
            leading=8.5,
            spaceAfter=0,
        )
        header_style = ParagraphStyle(
            "BarcodeReportHeader",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=7,
            leading=8,
            textColor=colors.white,
        )

        def cell(value, style=item_style):
            from html import escape

            return Paragraph(escape(str(value)), style)

        detail_data = [
            [cell("Operation"), cell(operation_name)],
            [cell("Operation Number"), cell(operation_number)],
            [cell("Duration"), cell("{} days".format(number(duration)))],
            [cell("Logging Model"), cell(self.logging_model)],
            [cell("Personnel"), cell(money(totals["personnel"]))],
            [cell("Consumables & Gear"), cell(money(totals["consumables"]))],
            [
                cell("Capital Replacement / Acquisition"),
                cell(money(totals["replacement"])),
            ],
            [cell("Asset Operating Costs"), cell(money(totals["operating"]))],
            [cell("Fuel"), cell(money(totals["fuel"]))],
            [cell("Grand Total"), cell(money(totals["grand_total"]))],
        ]
        detail_table = Table(
            detail_data,
            colWidths=(page_width - 2 * margin - 150, 150),
            hAlign="LEFT",
        )
        detail_table.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (0, 0), (-1, -2), 0.25, colors.lightgrey),
                    ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#e7edf5")),
                    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )

        item_headers = (
            "Item",
            "Category",
            "Unit",
            "Qty / Usage",
            "Unit Cost",
            "Acquisition",
            "Operating",
            "Fuel",
            "Line Total",
        )
        table_data = [[cell(value, header_style) for value in item_headers]]
        for item in self.operation_items:
            costs = line_costs[item["row_id"]]
            if item["kind"] == "consumable":
                quantity_text = "{} {}".format(number(item["quantity"]), item["unit"])
            else:
                quantity_text = "{} acquired; {} in service".format(
                    number(item["quantity"]), number(item["service_count"])
                )
                if item["activity"]:
                    quantity_text += "; {} {}".format(
                        number(item["activity"]), item["operating_unit"]
                    )
            table_data.append(
                [
                    cell(item["name"]),
                    cell(item["category"]),
                    cell(item["unit"]),
                    cell(quantity_text),
                    cell(money(item["unit_price"])),
                    cell(money(costs["replacement"])),
                    cell(money(costs["operating"])),
                    cell(money(costs["fuel"])),
                    cell(money(costs["total"])),
                ]
            )
        if not self.operation_items:
            table_data.append([cell("No items recorded.")] + [""] * 8)

        item_table = LongTable(
            table_data,
            colWidths=(105, 105, 60, 110, 75, 70, 70, 55, 70),
            repeatRows=1,
            hAlign="LEFT",
        )
        item_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#334b68")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("ALIGN", (4, 1), (-1, -1), "RIGHT"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), (colors.white, colors.HexColor("#f4f6f8"))),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )

        def draw_pdf417(canvas):
            canvas.saveState()
            image_width, image_height = pdf417_image.size
            image_scale = min(205 / image_width, 55 / image_height)
            rendered_width = image_width * image_scale
            rendered_height = image_height * image_scale
            canvas.setFont("Helvetica", 7)
            canvas.drawString(
                margin,
                82,
                "Operation #{} | Logging Model {}".format(
                    operation_number, self.logging_model
                ),
            )
            canvas.drawImage(
                ImageReader(pdf417_image),
                margin,
                22,
                width=rendered_width,
                height=rendered_height,
                preserveAspectRatio=True,
                mask="auto",
            )
            canvas.restoreState()

        class LastPageBarcodeCanvas(Canvas):
            def __init__(self, *args, **kwargs):
                self._saved_page_states = []
                super().__init__(*args, **kwargs)

            def showPage(self):
                self._saved_page_states.append(dict(self.__dict__))
                self._startPage()

            def save(self):
                last_page = len(self._saved_page_states)
                for page_number, page_state in enumerate(
                    self._saved_page_states, start=1
                ):
                    self.__dict__.update(page_state)
                    if page_number == last_page:
                        draw_pdf417(self)
                    Canvas.showPage(self)
                Canvas.save(self)

        def draw_page(canvas, document, include_code128):
            canvas.saveState()
            canvas.setTitle(
                "Operation #{} - {}".format(operation_number, operation_name)
            )
            canvas.setFont("Helvetica-Bold", 12)
            canvas.drawString(margin, page_height - 25, "Operation Cost Report (CAD)")
            canvas.setFont("Helvetica", 8)
            canvas.drawString(
                margin,
                page_height - 40,
                "OPERATION #{} {}".format(operation_number, operation_name),
            )
            if include_code128:
                code128 = Code128(
                    barcode_text, barHeight=27, barWidth=0.55, humanReadable=True
                )
                max_barcode_width = pdf_logo_x - margin - 12
                barcode_scale = min(1.0, max_barcode_width / code128.width)
                canvas.saveState()
                canvas.translate(margin, page_height - 82)
                canvas.scale(barcode_scale, 1)
                code128.drawOn(canvas, 0, 0)
                canvas.restoreState()
                canvas.drawImage(
                    logo_reader,
                    pdf_logo_x,
                    pdf_logo_y,
                    width=pdf_logo_width,
                    height=pdf_logo_height,
                    preserveAspectRatio=True,
                    mask="auto",
                )
            canvas.setFont("Helvetica", 8)
            canvas.drawRightString(
                page_width - margin, 28, "Page {}".format(document.page)
            )
            canvas.restoreState()

        def draw_first_page(canvas, document):
            draw_page(canvas, document, include_code128=True)

        def draw_later_pages(canvas, document):
            draw_page(canvas, document, include_code128=False)

        document = SimpleDocTemplate(
            path,
            pagesize=page_size,
            leftMargin=margin,
            rightMargin=margin,
            topMargin=100,
            bottomMargin=95,
            title="Operation #{} {}".format(operation_number, operation_name),
            author="Operation Cost Calculator",
        )
        story = [
            Paragraph("Operation Cost Summary", styles["Heading1"]),
            detail_table,
            Spacer(1, 12),
            Paragraph("Itemized Cost Breakdown", styles["Heading2"]),
            item_table,
        ]
        document.build(
            story,
            onFirstPage=draw_first_page,
            onLaterPages=draw_later_pages,
            canvasmaker=LastPageBarcodeCanvas,
        )

    def open_catalog_manager(self):
        if self.manager_window is not None and self.manager_window.winfo_exists():
            self.manager_window.lift()
            self.manager_window.focus_set()
            return

        window = tk.Toplevel(self.root)
        self.manager_window = window
        window.title("Price Database & Item Manager")
        window.geometry("1120x760")
        window.minsize(850, 620)
        window.transient(self.root)

        frame = ttk.Frame(window, padding=12)
        frame.grid(row=0, column=0, sticky="nsew")
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        columns = (
            "name",
            "category",
            "kind",
            "unit",
            "price",
            "operating_rate",
            "operating_unit",
            "fuel_burn",
            "fuel_basis",
            "fuel_item",
        )
        self.catalog_tree = ttk.Treeview(frame, columns=columns, show="headings")
        for column, heading, width, anchor in (
            ("name", "Item Name", 270, "w"),
            ("category", "Category", 190, "w"),
            ("kind", "Type", 95, "w"),
            ("unit", "Billing Unit", 125, "w"),
            ("price", "Unit / Replacement Cost", 160, "e"),
            ("operating_rate", "Operating Rate", 145, "e"),
            ("operating_unit", "Rate Unit", 130, "w"),
            ("fuel_burn", "Fuel Burn (L)", 100, "e"),
            ("fuel_basis", "Fuel Basis", 110, "w"),
            ("fuel_item", "Fuel Price Item", 200, "w"),
        ):
            self.catalog_tree.heading(column, text=heading)
            self.catalog_tree.column(column, width=width, minwidth=90, anchor=anchor)
        vertical_scroll = ttk.Scrollbar(
            frame, orient="vertical", command=self.catalog_tree.yview
        )
        horizontal_scroll = ttk.Scrollbar(
            frame, orient="horizontal", command=self.catalog_tree.xview
        )
        self.catalog_tree.configure(
            yscrollcommand=vertical_scroll.set, xscrollcommand=horizontal_scroll.set
        )
        self.catalog_tree.grid(row=0, column=0, columnspan=2, sticky="nsew")
        vertical_scroll.grid(row=0, column=2, sticky="ns")
        horizontal_scroll.grid(row=1, column=0, columnspan=2, sticky="ew")

        editor = ttk.LabelFrame(frame, text="Item Details", padding=8)
        editor.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(10, 0))
        for column in (1, 3, 5):
            editor.columnconfigure(column, weight=1)

        ttk.Label(editor, text="Item Name:").grid(row=0, column=0, sticky="w", padx=4)
        self.catalog_name = tk.StringVar()
        ttk.Entry(editor, textvariable=self.catalog_name).grid(
            row=0, column=1, sticky="ew", padx=4, pady=4
        )
        ttk.Label(editor, text="Category:").grid(row=0, column=2, sticky="w", padx=4)
        self.catalog_category = tk.StringVar()
        ttk.Combobox(
            editor,
            textvariable=self.catalog_category,
            values=CATEGORIES,
        ).grid(row=0, column=3, sticky="ew", padx=4, pady=4)
        ttk.Label(editor, text="Item Type:").grid(row=0, column=4, sticky="w", padx=4)
        self.catalog_kind = tk.StringVar(value="consumable")
        ttk.Combobox(
            editor,
            textvariable=self.catalog_kind,
            values=("consumable", "weapon", "vehicle", "aircraft"),
            state="readonly",
        ).grid(row=0, column=5, sticky="ew", padx=4, pady=4)

        ttk.Label(editor, text="Billing Unit:").grid(row=1, column=0, sticky="w", padx=4)
        self.catalog_unit = tk.StringVar(value="Unit")
        ttk.Entry(editor, textvariable=self.catalog_unit).grid(
            row=1, column=1, sticky="ew", padx=4, pady=4
        )
        ttk.Label(editor, text="Unit / Replacement Cost (CAD $):").grid(
            row=1, column=2, sticky="w", padx=4
        )
        self.catalog_price = tk.StringVar()
        ttk.Entry(editor, textvariable=self.catalog_price).grid(
            row=1, column=3, sticky="ew", padx=4, pady=4
        )
        ttk.Label(editor, text="Operating Rate (CAD $):").grid(
            row=1, column=4, sticky="w", padx=4
        )
        self.catalog_operating_rate = tk.StringVar()
        ttk.Entry(editor, textvariable=self.catalog_operating_rate).grid(
            row=1, column=5, sticky="ew", padx=4, pady=4
        )

        ttk.Label(editor, text="Operating Rate Unit:").grid(
            row=2, column=0, sticky="w", padx=4
        )
        self.catalog_operating_unit = tk.StringVar()
        ttk.Combobox(
            editor,
            textvariable=self.catalog_operating_unit,
            values=("year", "full-charge shot", "km", "flight hour"),
            state="readonly",
        ).grid(row=2, column=1, sticky="ew", padx=4, pady=4)
        ttk.Label(editor, text="Fuel Burn (litres):").grid(
            row=2, column=2, sticky="w", padx=4
        )
        self.catalog_fuel_burn = tk.StringVar()
        ttk.Entry(editor, textvariable=self.catalog_fuel_burn).grid(
            row=2, column=3, sticky="ew", padx=4, pady=4
        )
        ttk.Label(editor, text="Fuel Burn Basis:").grid(
            row=2, column=4, sticky="w", padx=4
        )
        self.catalog_fuel_basis = tk.StringVar()
        ttk.Combobox(
            editor,
            textvariable=self.catalog_fuel_basis,
            values=("100 km", "flight hour"),
            state="readonly",
        ).grid(row=2, column=5, sticky="ew", padx=4, pady=4)

        ttk.Label(editor, text="Fuel Price Catalog Item:").grid(
            row=3, column=0, sticky="w", padx=4
        )
        self.catalog_fuel_item = tk.StringVar()
        self.catalog_fuel_combo = ttk.Combobox(
            editor, textvariable=self.catalog_fuel_item, state="readonly"
        )
        self.catalog_fuel_combo.grid(
            row=3, column=1, columnspan=3, sticky="ew", padx=4, pady=4
        )
        ttk.Label(
            editor,
            text="Fuel costs use the selected item's CAD price per litre.",
        ).grid(row=3, column=4, columnspan=2, sticky="w", padx=4)

        self._refresh_catalog_fuel_choices()
        controls = ttk.Frame(frame)
        controls.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(10, 0))
        ttk.Button(
            controls, text="Add to Catalog", command=self.add_catalog_item
        ).pack(side="left", padx=(0, 6))
        ttk.Button(
            controls, text="Update Selected", command=self.update_catalog_item
        ).pack(side="left", padx=(0, 6))
        ttk.Button(
            controls, text="Delete Selected", command=self.delete_catalog_item
        ).pack(side="left", padx=(0, 6))
        ttk.Button(controls, text="Clear Fields", command=self._clear_catalog_fields).pack(
            side="left"
        )

        report_settings = ttk.LabelFrame(
            frame, text="Report Settings", padding=8
        )
        report_settings.grid(
            row=4, column=0, columnspan=3, sticky="ew", pady=(10, 0)
        )
        ttk.Label(report_settings, text="Logging Model:").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        self.logging_model_var = tk.StringVar(value=self.logging_model)
        ttk.Entry(
            report_settings, textvariable=self.logging_model_var, width=20
        ).grid(row=0, column=1, sticky="w", padx=(0, 8))
        ttk.Label(
            report_settings,
            text="Stored in settings.json and encoded in the PDF417 barcode.",
        ).grid(row=0, column=2, sticky="w", padx=(4, 12))
        ttk.Button(
            report_settings, text="Save Settings", command=self.save_logging_model
        ).grid(row=0, column=3, sticky="e")

        self.catalog_tree.bind("<<TreeviewSelect>>", self._catalog_selection_changed)
        self._refresh_catalog_tree()
        window.protocol("WM_DELETE_WINDOW", self._close_catalog_manager)

    def _refresh_catalog_fuel_choices(self):
        fuel_names = sorted(
            (
                item["name"]
                for item in self.catalog
                if item["kind"] == "consumable" and item["unit"].casefold() == "litre"
            ),
            key=str.casefold,
        )
        if self.manager_window is not None and self.manager_window.winfo_exists():
            self.catalog_fuel_combo["values"] = fuel_names

    def _refresh_catalog_tree(self):
        if self.manager_window is None or not self.manager_window.winfo_exists():
            return
        self.catalog_tree.delete(*self.catalog_tree.get_children())
        for index, item in enumerate(
            sorted(self.catalog, key=lambda value: value["name"].casefold())
        ):
            self.catalog_tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    item["name"],
                    item["category"],
                    item["kind"],
                    item["unit"],
                    money(Decimal(item["price"])),
                    (
                        money(Decimal(item["operating_rate"]))
                        if item["operating_rate"]
                        else ""
                    ),
                    item["operating_unit"],
                    item["fuel_burn"],
                    item["fuel_basis"],
                    item["fuel_item"],
                ),
            )

    def _catalog_selection_changed(self, _event=None):
        selection = self.catalog_tree.selection()
        if not selection:
            return
        item = self._selected_catalog_item()
        if item is not None:
            self.catalog_name.set(item["name"])
            self.catalog_category.set(item["category"])
            self.catalog_kind.set(item["kind"])
            self.catalog_unit.set(item["unit"])
            self.catalog_price.set(item["price"])
            self.catalog_operating_rate.set(item["operating_rate"])
            self.catalog_operating_unit.set(item["operating_unit"])
            self.catalog_fuel_burn.set(item["fuel_burn"])
            self.catalog_fuel_basis.set(item["fuel_basis"])
            self.catalog_fuel_item.set(item["fuel_item"])

    def _selected_catalog_item(self):
        selection = self.catalog_tree.selection()
        if not selection:
            return None
        try:
            index = int(selection[0])
            ordered = sorted(self.catalog, key=lambda value: value["name"].casefold())
            return ordered[index]
        except (ValueError, IndexError):
            return None

    def _catalog_form_values(self):
        name = self.catalog_name.get().strip()
        category = self.catalog_category.get().strip()
        kind = self.catalog_kind.get().strip()
        unit = self.catalog_unit.get().strip()
        if not name:
            raise ValueError("Item Name cannot be empty.")
        if not category:
            raise ValueError("Category cannot be empty.")
        if not unit:
            raise ValueError("Billing Unit cannot be empty.")
        if kind not in ("consumable", "weapon", "vehicle", "aircraft"):
            raise ValueError("Select a valid item type.")
        price = self._parse_nonnegative_decimal(
            self.catalog_price.get(), "Unit / Replacement Cost"
        )
        operating_rate_text = self.catalog_operating_rate.get().strip()
        operating_rate = ""
        if operating_rate_text:
            operating_rate = str(
                self._parse_nonnegative_decimal(
                    operating_rate_text, "Operating Rate"
                )
            )
        operating_unit = self.catalog_operating_unit.get().strip()
        if bool(operating_rate) != bool(operating_unit):
            raise ValueError(
                "Enter both an Operating Rate and its unit, or leave both blank."
            )
        valid_operating_units = {
            "weapon": ("year", "full-charge shot"),
            "vehicle": ("km",),
            "aircraft": ("flight hour",),
            "consumable": (),
        }
        if operating_unit and operating_unit not in valid_operating_units[kind]:
            raise ValueError(
                "Operating rate unit does not match the selected item type."
            )

        fuel_burn_text = self.catalog_fuel_burn.get().strip()
        fuel_burn = ""
        if fuel_burn_text:
            fuel_burn = str(
                self._parse_nonnegative_decimal(fuel_burn_text, "Fuel Burn")
            )
            if Decimal(fuel_burn) == 0:
                raise ValueError("Fuel Burn must be greater than zero.")
        fuel_basis = self.catalog_fuel_basis.get().strip()
        fuel_item = self.catalog_fuel_item.get().strip()
        if fuel_burn:
            if not fuel_basis or not fuel_item:
                raise ValueError(
                    "Fuel Burn requires both a burn basis and a fuel price item."
                )
            if (
                (fuel_basis == "100 km" and kind != "vehicle")
                or (fuel_basis == "flight hour" and kind != "aircraft")
            ):
                raise ValueError(
                    "Fuel burn basis does not match the selected item type."
                )
            fuel_record = self._find_catalog_item(fuel_item)
            if (
                fuel_record is None
                or fuel_record["kind"] != "consumable"
                or fuel_record["unit"].casefold() != "litre"
            ):
                raise ValueError(
                    "Select a catalog consumable billed per litre for fuel pricing."
                )
        elif fuel_basis or fuel_item:
            raise ValueError(
                "Clear the fuel basis and fuel item when no fuel burn is set."
            )
        if kind == "consumable" and (operating_rate or fuel_burn):
            raise ValueError(
                "Consumables use a unit price only; choose a capital asset type "
                "for operating or fuel rates."
            )
        return {
            "name": name,
            "category": category,
            "kind": kind,
            "unit": unit,
            "price": str(price),
            "operating_rate": operating_rate,
            "operating_unit": operating_unit,
            "fuel_burn": fuel_burn,
            "fuel_basis": fuel_basis,
            "fuel_item": fuel_item,
        }

    def add_catalog_item(self):
        try:
            item = self._catalog_form_values()
        except ValueError as exc:
            messagebox.showerror("Invalid Catalog Item", str(exc), parent=self.manager_window)
            return
        if any(
            existing["name"].casefold() == item["name"].casefold()
            for existing in self.catalog
        ):
            messagebox.showerror(
                "Duplicate Item",
                "An item with that name already exists. Select it to update it.",
                parent=self.manager_window,
            )
            return
        updated_catalog = self.catalog + [item]
        self._save_catalog_changes(updated_catalog)

    def update_catalog_item(self):
        selected = self._selected_catalog_item()
        if selected is None:
            messagebox.showerror(
                "No Selection", "Select an item to update.", parent=self.manager_window
            )
            return
        try:
            updated_item = self._catalog_form_values()
        except ValueError as exc:
            messagebox.showerror("Invalid Catalog Item", str(exc), parent=self.manager_window)
            return
        if any(
            item is not selected
            and item["name"].casefold() == updated_item["name"].casefold()
            for item in self.catalog
        ):
            messagebox.showerror(
                "Duplicate Item",
                "Another catalog item already uses that name.",
                parent=self.manager_window,
            )
            return
        updated_catalog = []
        for item in self.catalog:
            if item is selected:
                updated_catalog.append(updated_item)
            else:
                copied_item = dict(item)
                if (
                    selected["name"] != updated_item["name"]
                    and copied_item["fuel_item"] == selected["name"]
                ):
                    copied_item["fuel_item"] = updated_item["name"]
                updated_catalog.append(copied_item)
        self._save_catalog_changes(updated_catalog)

    def delete_catalog_item(self):
        selected = self._selected_catalog_item()
        if selected is None:
            messagebox.showerror(
                "No Selection", "Select an item to delete.", parent=self.manager_window
            )
            return
        if any(item["fuel_item"] == selected["name"] for item in self.catalog):
            messagebox.showerror(
                "Fuel Item In Use",
                "Update or remove the linked asset fuel rates before deleting "
                "this fuel item.",
                parent=self.manager_window,
            )
            return
        if not messagebox.askyesno(
            "Delete Catalog Item",
            "Delete '{}' from the catalog?".format(selected["name"]),
            parent=self.manager_window,
        ):
            return
        updated_catalog = [item for item in self.catalog if item is not selected]
        self._save_catalog_changes(updated_catalog)
        self._clear_catalog_fields()

    def _save_catalog_changes(self, updated_catalog):
        try:
            self._write_catalog(updated_catalog)
        except OSError as exc:
            messagebox.showerror(
                "Catalog Save Error",
                "Could not save prices.json:\n{}".format(exc),
                parent=self.manager_window,
            )
            return
        self.catalog = updated_catalog
        self._refresh_catalog_tree()
        self._refresh_item_choices()
        self._refresh_catalog_fuel_choices()
        self._update_asset_form()

    def _clear_catalog_fields(self):
        self.catalog_name.set("")
        self.catalog_category.set("")
        self.catalog_kind.set("consumable")
        self.catalog_unit.set("Unit")
        self.catalog_price.set("")
        self.catalog_operating_rate.set("")
        self.catalog_operating_unit.set("")
        self.catalog_fuel_burn.set("")
        self.catalog_fuel_basis.set("")
        self.catalog_fuel_item.set("")
        if self.catalog_tree.selection():
            self.catalog_tree.selection_remove(*self.catalog_tree.selection())

    def _close_catalog_manager(self):
        self.manager_window.destroy()
        self.manager_window = None


def main():
    root = tk.Tk()
    OperationCostCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
