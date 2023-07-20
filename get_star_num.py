import os
import pandas as pd
import argparse

def calculate_counts_and_save_to_csv(input_names, base_input_dir, base_output_dir):
    for name in input_names:
        # Construct the input file path
        input_filename = os.path.join(base_input_dir, name, "Commit", "CSV", "total.csv")

        # Load the CSV file
        df = pd.read_csv(input_filename)

        # Convert the "committedDate" column to datetime
        df['committedDate'] = pd.to_datetime(df['committedDate'])

        # Extract the year and month from "committedDate"
        df['year_month'] = df['committedDate'].dt.to_period('M')

        # Group by year-month and count
        df_counts = df['year_month'].value_counts().reset_index()
        df_counts.columns = ['year_month', 'count']

        # Sort by year_month
        df_counts = df_counts.sort_values('year_month')

        # Construct the output directory and file path
        output_dir = os.path.join(base_output_dir, name)
        output_filename = "N_Commit.csv"

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Write the DataFrame to a CSV file
        df_counts.to_csv(os.path.join(output_dir, output_filename), index=False)

def main():
    parser = argparse.ArgumentParser(description='Calculate counts by year-month and save to CSV.')
    parser.add_argument('input', nargs='+', help='Input names')
    parser.add_argument('--base_input_dir', default="cache", help='Base input directory')
    parser.add_argument('--base_output_dir', default="date_data", help='Base output directory')
    args = parser.parse_args()

    calculate_counts_and_save_to_csv(args.input, args.base_input_dir, args.base_output_dir)

if __name__ == "__main__":
    main()
