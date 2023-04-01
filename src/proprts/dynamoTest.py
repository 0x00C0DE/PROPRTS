from models.function_stats import FunctionStatsModel


class DynamoTest:
    def run(self):
        model = FunctionStatsModel()
        model.message = "Hello World"
        model.save()
