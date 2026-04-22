from pymongo import MongoClient

class StudentResults:
    def __init__(self, db_name='school', collection_name='students'):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def calculate_sgpa(self, student):
        total_weighted_score = sum(sub['grade'] * sub['credits'] for sub in student['subjects'])
        total_credits = sum(sub['credits'] for sub in student['subjects'])
        return round(total_weighted_score / total_credits, 2) if total_credits > 0 else 0

    def calculate_all_sgpas(self):
        students = self.collection.find()
        results = []
        for student in students:
            sgpa = self.calculate_sgpa(student)
            results.append({
                "name": student['name'],
                "roll_no": student['roll_no'],
                "sgpa": sgpa
            })
        return results

    def top_scorer(self):
        sgpa_list = self.calculate_all_sgpas()
        if not sgpa_list:
            return None
        top_student = max(sgpa_list, key=lambda x: x['sgpa'])
        return top_student

    def total_students(self):
        return self.collection.count_documents({})

    def add_student(self, name, roll_no, subjects):
        student_data = {
            "name": name,
            "roll_no": roll_no,
            "subjects": subjects
        }
        self.collection.insert_one(student_data)
        print(f"Student {name} added.")

# Example Usage
if __name__ == "__main__":
    sr = StudentResults()
    
    # Add a new student
    sr.add_student("Bob", "002", [
        {"name": "Math", "grade": 9, "credits": 4},
        {"name": "Biology", "grade": 8, "credits": 3},
        {"name": "Chemistry", "grade": 10, "credits": 3}
    ])

    # Calculate SGPA for all students
    all_results = sr.calculate_all_sgpas()
    print("All Results:", all_results)

    # Top scorer
    print("Top Scorer:", sr.top_scorer())

    # Total students
    print("Total Students:", sr.total_students())
