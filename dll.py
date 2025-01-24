from collections import deque

# 1. Application Submission and Storage
class ApplicationStorage:
    def __init__(self):
        self.applications = []  # List to store application data

    def submit_application(self, name, job_id, resume_link, status="Submitted"):
        application = {
            "name": name,
            "job_id": job_id,
            "resume_link": resume_link,
            "status": status
        }
        self.applications.append(application)
        print(f"Application submitted for {name} (Job ID: {job_id})")

    def get_applications(self):
        return self.applications

# 2. Application Queue for Review
class ApplicationQueue:
    def __init__(self):
        self.queue = deque()  # Queue for FIFO processing

    def add_to_queue(self, application):
        self.queue.append(application)
        print(f"Application added to review queue: {application['name']} (Job ID: {application['job_id']})")

    def process_next_application(self):
        if self.queue:
            application = self.queue.popleft()
            print(f"Processing application: {application['name']} (Job ID: {application['job_id']})")
            return application
        else:
            print("No applications in the review queue.")
            return None

# 3. Shortlisting and Filtering Applications
class ApplicationShortlist:
    def __init__(self):
        self.stack = []  # Stack to track recent shortlisting/rejections

    def shortlist(self, application):
        application["status"] = "Shortlisted"
        self.stack.append((application, "Shortlisted"))
        print(f"Application shortlisted: {application['name']} (Job ID: {application['job_id']})")

    def reject(self, application):
        application["status"] = "Rejected"
        self.stack.append((application, "Rejected"))
        print(f"Application rejected: {application['name']} (Job ID: {application['job_id']})")

    def filter_applications(self, applications, criteria):
        filtered = [app for app in applications if all(app.get(k) == v for k, v in criteria.items())]
        return filtered

# 4. Search Applications
class ApplicationSearch:
    @staticmethod
    def search(applications, key, value):
        results = [app for app in applications if app.get(key) == value]
        if results:
            print(f"Found {len(results)} application(s) matching {key} = {value}")
        else:
            print(f"No applications found matching {key} = {value}")
        return results

# 5. Application Tracking System
class ApplicationTracking:
    class Node:
        def __init__(self, application):
            self.application = application
            self.next = None

    def __init__(self):
        self.head = None

    def add_stage(self, application, stage):
        application["status"] = stage
        new_node = self.Node(application)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        print(f"Application {application['name']} moved to stage: {stage}")

    def display_tracking(self):
        stages = []
        current = self.head
        while current:
            stages.append((current.application['name'], current.application['status']))
            current = current.next
        return stages

# 6. Report Generation
class ReportGenerator:
    @staticmethod
    def generate_report(applications):
        total_applications = len(applications)
        status_count = {"Submitted": 0, "Shortlisted": 0, "Rejected": 0}
        job_count = {}

        for app in applications:
            status_count[app["status"]] += 1
            job_count[app["job_id"]] = job_count.get(app["job_id"], 0) + 1

        report = {
            "Total Applications": total_applications,
            "Status Count": status_count,
            "Applications per Job": job_count
        }
        return report

# 7. Main Program
if __name__ == "__main__":
    # Initialize modules
    storage = ApplicationStorage()
    queue = ApplicationQueue()
    shortlist = ApplicationShortlist()
    tracking = ApplicationTracking()

    while True:
        print("\n--- Application Management System ---")
        print("1. Submit Application")
        print("2. View All Applications")
        print("3. Add Applications to Review Queue")
        print("4. Process Next Application")
        print("5. Shortlist/Reject Applications")
        print("6. Search Applications")
        print("7. Track Application Stages")
        print("8. Generate Report")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter applicant name: ")
            job_id = input("Enter job ID: ")
            resume_link = input("Enter resume link: ")
            storage.submit_application(name, job_id, resume_link)

        elif choice == "2":
            applications = storage.get_applications()
            print("\n--- All Applications ---")
            for app in applications:
                print(app)

        elif choice == "3":
            applications = storage.get_applications()
            for app in applications:
                queue.add_to_queue(app)

        elif choice == "4":
            queue.process_next_application()

        elif choice == "5":
            applications = storage.get_applications()
            name = input("Enter applicant name to shortlist/reject: ")
            action = input("Enter 'shortlist' or 'reject': ").lower()
            app = next((app for app in applications if app["name"] == name), None)
            if app:
                if action == "shortlist":
                    shortlist.shortlist(app)
                elif action == "reject":
                    shortlist.reject(app)
                else:
                    print("Invalid action.")
            else:
                print("Application not found.")

        elif choice == "6":
            key = input("Enter search key (name/job_id/status): ")
            value = input(f"Enter value for {key}: ")
            ApplicationSearch.search(storage.get_applications(), key, value)

        elif choice == "7":
            applications = storage.get_applications()
            for app in applications:
                tracking.add_stage(app, app["status"])

            print("\n--- Application Tracking ---")
            for name, stage in tracking.display_tracking():
                print(f"{name}: {stage}")

        elif choice == "8":
            report = ReportGenerator.generate_report(storage.get_applications())
            print("\n--- Report ---")
            for key, value in report.items():
                print(f"{key}: {value}")

        elif choice == "9":
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")
