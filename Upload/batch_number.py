import pandas as pd

def latest_batch_number():
    csv_path = 'Database/Mapping.csv'

    try:
        # Load the CSV file into a DataFrame
        dataframe = pd.read_csv(csv_path)
        
        # Ensure 'date' column is in datetime format for accurate sorting
        dataframe['date'] = pd.to_datetime(dataframe['date'])
        
        # Sort the DataFrame by 'date' column in descending order
        sorted_df = dataframe.sort_values(by='date', ascending=False)
        
        # Get the latest value of 'batch_no'
        latest_batch_name = sorted_df.iloc[0]['batch_no']
        
        # Extract batch number from the latest batch name
        try:
            batch_number = int(latest_batch_name.split('Batch')[1].strip())
        except Exception as e:
            print(f"Error extracting batch number: {e}")
            batch_number = 0  # Return 0 in case of extraction error
        
        return batch_number
    
    except Exception as e:
        print(f"Error loading or processing CSV file: {e}")
        return 0  # Return 0 if there's any error loading or processing the CSV file

    
    except Exception as e:
        print(f"Error loading or processing CSV file: {e}")
        return 0  # Return 0 if there's any error loading or processing the CSV file


if __name__=="__main__":
    latest_batch_number = latest_batch_number()
    print("Latest Batch Number:", latest_batch_number)

