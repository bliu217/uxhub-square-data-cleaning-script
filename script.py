import numpy as np
import pandas as pd

df = pd.read_csv('data/orders.csv')
sel = df[["Recipient Name", "Recipient Email", "Fulfillment Notes", "Recipient Phone", "Order Date", "Item Name"]].copy()
sel["student_number"] = sel["Fulfillment Notes"].str.extract(r"Student Number:\s*(\d+)")
sel["membership_type"] = sel["Item Name"].str.extract(r"\[([^\s\]]+)")


sel.columns = sel.columns.str.lower().str.replace(" ", "_")

sel = sel.rename(columns={
    "recipient_name": "name",
    "recipient_email": "email",
    "fulfillment_notes": "notes",
    "recipient_phone": "phone"
})

sel["phone"] = sel["phone"].str.replace(r"^\+1\s*", "", regex=True).str.replace("-","")
sel["phone"] = sel["phone"].str[:3] + "-" + sel["phone"].str[3:6] + "-" + sel["phone"].str[6:]
sel["newsletter"] = sel["notes"].str.extract(r"Email for Newsletter \(n/a if no\):\s*(\S+)").replace("n/a", np.nan)

sel.drop(["notes", "item_name"], axis=1, inplace=True)
sel = sel[sel["name"].str.strip().astype(bool)]

# random purchase idk what it is
sel.drop(index=63, inplace=True)

sel.to_csv("uxhub_members/clean_member_data.csv", index=False)
