import unittest
from src.rule_engine import create_rule, evaluate_rule, combine_rules

class TestRuleEngine(unittest.TestCase):
    
    def test_create_rule(self):
        rule_string = "(age > 30 AND department == 'Sales')"
        ast = create_rule(rule_string)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.value, 'and')

    def test_evaluate_rule(self):
        rule_string = "(age > 30 AND department == 'Sales')"
        ast = create_rule(rule_string)
        user_data = {"age": 32, "department": "Sales"}
        result = evaluate_rule(ast, user_data)
        self.assertTrue(result)

    def test_combine_rules(self):
        rule1 = "(age > 30 AND department == 'Sales')"
        rule2 = "(age < 25 AND department == 'Marketing')"
        combined_ast = combine_rules([rule1, rule2])
        self.assertIsNotNone(combined_ast)

if __name__ == "__main__":
    unittest.main()
