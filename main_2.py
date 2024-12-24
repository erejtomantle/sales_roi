import json
from flask import Flask, render_template, request, jsonify
import os

# Initialize Flask app with updated template and static folder paths
app = Flask(
    __name__,
    template_folder='static',  # Relative path to the templates folder
    static_folder='static'     # Relative path to the static folder
)


# Path to the config file
config_path = "static/config_costs.json"

# Load configuration data
with open(config_path, "r") as f:
    config = json.load(f)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Retrieve user inputs
        option1_inserts = int(request.form.get("option1_inserts") or 0)
        option1_cost = float(request.form.get("option1_cost") or 0.0)
        option1_time = float(request.form.get("option1_time") or 0.0)  # User's estimated lead time for 2x2x2 inserts

        option2_inserts = int(request.form.get("option2_inserts") or 0)
        option2_cost = float(request.form.get("option2_cost") or 0.0)
        option2_time = float(request.form.get("option2_time") or 0.0)  # User's estimated lead time for 3x3x3 inserts

        option3_inserts = int(request.form.get("option3_inserts") or 0)
        option3_cost = float(request.form.get("option3_cost") or 0.0)
        option3_time = float(request.form.get("option3_time") or 0.0)  # User's estimated lead time for 4x4x4 inserts

        # Access Mantle's configuration costs and times
        mantle_2x2x2_cost = config["mantle_costs"]["2x2x2"]["cost"]
        mantle_2x2x2_time = config["mantle_costs"]["2x2x2"]["time"]

        mantle_3x3x3_cost = config["mantle_costs"]["3x3x3"]["cost"]
        mantle_3x3x3_time = config["mantle_costs"]["3x3x3"]["time"]

        mantle_4x4x4_cost = config["mantle_costs"]["4x4x4"]["cost"]
        mantle_4x4x4_time = config["mantle_costs"]["4x4x4"]["time"]

        # Calculate savings or loss for each insert size
        savings_2x2x2 = (option1_inserts * option1_cost) - (option1_inserts * mantle_2x2x2_cost)
        savings_3x3x3 = (option2_inserts * option2_cost) - (option2_inserts * mantle_3x3x3_cost)
        savings_4x4x4 = (option3_inserts * option3_cost) - (option3_inserts * mantle_4x4x4_cost)

        # Calculate time saved for each insert size (subtract the user's time from the Mantle time)
        time_saved_2x2x2 = (option1_time - mantle_2x2x2_time) * option1_inserts
        time_saved_3x3x3 = (option2_time - mantle_3x3x3_time) * option2_inserts
        time_saved_4x4x4 = (option3_time - mantle_4x4x4_time) * option3_inserts

        # Calculate total savings and total time saved
        total_savings = savings_2x2x2 + savings_3x3x3 + savings_4x4x4
        total_time_saved = time_saved_2x2x2 + time_saved_3x3x3 + time_saved_4x4x4

        # Cost of the Mantle machine
        mantle_machine_cost = 400000  # $400k

        # Calculate breakeven in months
        if total_savings > 0:
            breakeven_months = (mantle_machine_cost / total_savings) * 12
        else:
            breakeven_months = None  # Cannot calculate breakeven if savings <= 0

        # Format the results correctly
        formatted_savings_2x2x2 = "${:,.0f}".format(savings_2x2x2)
        formatted_savings_3x3x3 = "${:,.0f}".format(savings_3x3x3)
        formatted_savings_4x4x4 = "${:,.0f}".format(savings_4x4x4)
        formatted_total_savings = "${:,.0f}".format(total_savings)
        formatted_total_time_saved = f"{total_time_saved} days"

        return jsonify({
            "savings_2x2x2": formatted_savings_2x2x2,
            "savings_3x3x3": formatted_savings_3x3x3,
            "savings_4x4x4": formatted_savings_4x4x4,
            "total_savings": formatted_total_savings,
            "total_time_saved": formatted_total_time_saved,
            "breakeven_time": f"{round(breakeven_months, 2)} months" if breakeven_months else "Not applicable",
            "time_saved_2x2x2": time_saved_2x2x2,
            "time_saved_3x3x3": time_saved_3x3x3,
            "time_saved_4x4x4": time_saved_4x4x4,
        })

    return render_template("index2.html")  # Ensure this is pointing to the correct file


if __name__ == "__main__":
    app.run(debug=True)
