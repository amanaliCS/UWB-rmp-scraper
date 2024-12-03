class Professor:
    def __init__(self, data):
        self.department = data.get('tDept')
        self.first_name = data.get('tFname').strip()
        self.last_name = data.get('tLname').strip()
        self.tid = data.get('tid')
        self.num_ratings = data.get('tNumRatings')
        self.overall_rating = data.get('overall_rating')

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_dict(self):
        return {
            'tDept': self.department,
            'tFname': self.first_name,
            'tLname': self.last_name,
            'tid': self.tid,
            'tNumRatings': self.num_ratings,
            'overall_rating': self.overall_rating,
        }

    def display_info(self):
        print(f"Department: {self.department} SID: {self.sid} Name: {self.first_name} {self.last_name} Num ratings: {self.num_ratings} Overall Rating: {self.overall_rating}")

