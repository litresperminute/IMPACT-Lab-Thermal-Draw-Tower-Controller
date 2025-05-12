#!/bin/bash

echo "--------------------------------------"
echo "Thesis Experiment Logger Menu"
echo "--------------------------------------"
echo
echo "Do you want to install required Python packages?"
echo "(Recommended if this is your first time running the tool)"
echo "[Y] Yes, install dependencies now"
echo "[S] Skip and go to menu"
echo
read -p "Install dependencies? (Y/S): " depchoice

if [[ "$depchoice" == "Y" || "$depchoice" == "y" ]]; then
    if [[ -f "requirements.txt" ]]; then
        echo "Installing dependencies from requirements.txt..."
        pip3 install -r requirements.txt
        if [[ $? -ne 0 ]]; then
            echo "Failed to install packages. Please ensure Python and pip are installed."
            exit 1
        fi
    else
        echo "requirements.txt not found. Skipping installation."
    fi
fi

while true; do
    echo
    echo "--------------------------------------"
    echo "Thesis Experiment Logger Menu"
    echo "--------------------------------------"
    echo "1) Run drawlogger (start a new experiment)"
    echo "2) View experiment summary table"
    echo "3) Generate metadata for legacy files"
    echo "4) Plot a single experiment"
    echo "5) Compare multiple draw trials"
    echo "Q) Quit"
    echo
    read -p "Choose an option (1-5 or Q): " choice

    case $choice in
        1) python3 drawlogger.py ;;
        2) python3 summarize_metadata.py ;;
        3) python3 generate_metadata_for_legacy_logs.py ;;
        4) python3 plot_single_experiment.py ;;
        5) python3 compare_draw_trials.py ;;
        [Qq]) echo "Goodbye!"; exit ;;
        *) echo "Invalid option." ;;
    esac
done