import os
import requests
import math
import csv
from datetime import datetime
from Professor import Professor


# Endpoint Constants
RMP_BASE_URL = "https://www.ratemyprofessors.com/filter/professor/"
RMP_PAGE_URL = "https://www.ratemyprofessors.com/paginate/professors/ratings"

class RateMyProfScraper:
    def __init__(self, school_id):
        self.school_id = school_id
        self.professor_list = self._create_professor_list()
        self.index_number = None
        self._ensure_directory_exists(f"SchoolID_{self.school_id}")

    def _ensure_directory_exists(self, directory_path):
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)

    def _create_professor_list(self):
        professor_list = []
        total_professors = self._get_number_of_professors()
        total_pages = math.ceil(total_professors / 20)
        for page_number in range(1, total_pages + 1):
            professors_data = self._fetch_professors_by_page(page_number)
            professor_list.extend(Professor(professor) for professor in professors_data)
        return professor_list

    def _fetch_professors_by_page(self, page_number):
        response = requests.get(
            f"{RMP_BASE_URL}?page={page_number}&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid={self.school_id}")
        response_data = response.json()
        return response_data.get('professors', [])

    def _get_number_of_professors(self):
        response = requests.get(
            f"{RMP_BASE_URL}?page=1&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid={self.school_id}")
        response_data = response.json()
        return response_data.get('remaining', 0) + 20

    def search_professor(self, professor_name):
        self.index_number = self._get_professor_index(professor_name.title())
        self._print_professor_info()

    def _get_professor_index(self, professor_name):
        for index, professor in enumerate(self.professor_list):
            if professor_name == professor.get_full_name():
                return index

        return None

    def _print_professor_info(self):
        if self.index_number is None:
            print("Professor not found.")
        else:
            self.professor_list[self.index_number].display_info()

    def write_professors_to_csv(self):
        csv_columns = [
            'tDept', 'tFname', 'tLname', 'tid',
            'tNumRatings', 'overall_rating'
        ]
        directory_path = f"SchoolID_{self.school_id}"
        self._ensure_directory_exists(directory_path)

        date_timestamp = datetime.now().strftime("%m_%d_%Y-%H_%M")
        csv_file_path = os.path.join(directory_path, f'SchoolID_{self.school_id} {date_timestamp}.csv')

        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for professor in self.professor_list:
                writer.writerow(professor.get_dict())

school_id = 4466  # Replace with actual school ID
scraper = RateMyProfScraper(school_id)
# Perform operations
scraper.write_professors_to_csv()