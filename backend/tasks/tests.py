from django.test import TestCase
from datetime import date, timedelta
from .scoring import calculate_scores

class ScoringTests(TestCase):

    def setUp(self):
        self.tasks = [
            {
                "id": 1,
                "title": "Task A",
                "due_date": str(date.today()),
                "estimated_hours": 5,
                "importance": 7,
                "dependencies": []
            },
            {
                "id": 2,
                "title": "Task B",
                "due_date": str(date.today() - timedelta(days=2)),  # overdue
                "estimated_hours": 3,
                "importance": 9,
                "dependencies": []
            },
            {
                "id": 3,
                "title": "Task C",
                "due_date": str(date.today() + timedelta(days=5)),  # future
                "estimated_hours": 10,
                "importance": 6,
                "dependencies": [2]
            },
        ]

    def test_scores_between_0_and_100(self):
        """Each task should get a priority_score in [0, 100]."""
        scored = calculate_scores(self.tasks, 'balanced')
        for t in scored:
            self.assertGreaterEqual(t['priority_score'], 0)
            self.assertLessEqual(t['priority_score'], 100)

    def test_overdue_has_higher_priority_than_future(self):
        """Overdue task (id=2) should be ranked first."""
        scored = calculate_scores(self.tasks, 'balanced')
        self.assertEqual(scored[0]['id'], 2)

    def test_circular_dependency_penalty(self):
        """Circular dependencies should result in zero dependency contribution."""
        tasks = self.tasks.copy()
        tasks[0]['dependencies'] = [3]  # 1 depends on 3
        tasks[2]['dependencies'] = [1]  # 3 depends on 1 -> circular

        scored = calculate_scores(tasks, 'balanced')

        # Find the circular task (id=3) in scored and check its dependency_contribution
        circular_task = next(t for t in scored if t['id'] == 3)
        self.assertEqual(circular_task['dependency_contribution'], 0)

    def test_high_impact_mode_prioritizes_importance(self):
        """High impact profile should still put the most important task at the top."""
        scored_balanced = calculate_scores(self.tasks, 'balanced')
        scored_impact = calculate_scores(self.tasks, 'high_impact')

        top_balanced = scored_balanced[0]['id']
        top_impact = scored_impact[0]['id']

        # In both cases, the most important + overdue task (id=2) should be first
        self.assertEqual(top_impact, 2)
