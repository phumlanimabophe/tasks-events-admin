class SampleData():

    def get_task_data( **kwargs):
        tasks = [
            {
                "title": "Fix website bug",
                "due_date": "2025-02-15",
                "description": "Fix the bug in the homepage slider.",
                "priority": "High",
                "status": "Pending",
                "assigned_to": "johndoe",
                "created_by": "johndoe",
                "updated_by": "janedoe",
                "created_at": "2025-01-01T10:00:00",
                "updated_at": "2025-01-05T12:00:00"
            },
            {
                "title": "Prepare for meeting",
                "due_date": "2025-01-30",
                "description": "Prepare the presentation for the client meeting.",
                "priority": "Low",
                "status": "Completed",
                "assigned_to": "janedoe",
                "created_by": "janedoe",
                "updated_by": "janedoe",
                "created_at": "2025-01-01T11:00:00",
                "updated_at": "2025-01-02T14:00:00"
            },
            {
                "title": "Update software",
                "due_date": "2025-03-10",
                "description": "Update the software to the latest version.",
                "priority": "High",
                "status": "Pending",
                "assigned_to": "johndoe",
                "created_by": "janedoe",
                "updated_by": "janedoe",
                "created_at": "2025-01-05T15:00:00",
                "updated_at": "2025-01-06T16:00:00"
            }
        ]
        return tasks
