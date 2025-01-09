import requests
import json
import csv

# HH API base URL
BASE_URL = "https://api.hh.ru/vacancies"

# Function to get vacancies from HH API
def get_vacancies(keyword, pages=1):
    vacancies = []
    for page in range(pages):
        params = {
            'text': keyword,
            'area': 113,  # Russia
            'per_page': 20,
            'page': page
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            vacancies.extend(data['items'])
        else:
            print(f"Error: {response.status_code}")
            break
    return vacancies

# Function to save vacancies to a CSV file
def save_to_csv(vacancies, filename="vacancies.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(["ID", "Name", "Employer", "Salary From", "Salary To", "City", "URL"])
        
        for vacancy in vacancies:
            salary_from = vacancy.get('salary', {}).get('from') if vacancy.get('salary') else None
            salary_to = vacancy.get('salary', {}).get('to') if vacancy.get('salary') else None
            writer.writerow([
                vacancy.get('id'),
                vacancy.get('name'),
                vacancy.get('employer', {}).get('name'),
                salary_from,
                salary_to,
                vacancy.get('area', {}).get('name'),
                vacancy.get('alternate_url')
            ])

# Main function
def main():
    keyword = input("Enter keyword for search (e.g., 'Python Developer'): ")
    pages = int(input("Enter number of pages to parse: "))
    vacancies = get_vacancies(keyword, pages)
    if vacancies:
        save_to_csv(vacancies)
        print(f"Successfully saved {len(vacancies)} vacancies to vacancies.csv")
    else:
        print("No vacancies found.")

if __name__ == "__main__":
    main()
