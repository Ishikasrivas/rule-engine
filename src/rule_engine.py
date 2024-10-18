class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        """
        node_type: Can be 'operator' for AND/OR, or 'operand' for conditions.
        left: Reference to another Node (left child).
        right: Reference to another Node (right child).
        value: The condition or operator value (like "age > 30" or 'AND').
        """
        self.node_type = node_type  # 'operator' or 'operand'
        self.left = left  # Left child node (for binary operations)
        self.right = right  # Right child node (for binary operations)
        self.value = value  # The condition or operator

    def __repr__(self):
        return f"Node({self.node_type}, {self.value})"
import re

def create_rule(rule_string):
    try:
        # Check for empty rules
        if not rule_string.strip():
            raise ValueError("Rule string cannot be empty.")

        tokens = re.split(r'(\band\b|\bor\b|\(|\))', rule_string, flags=re.IGNORECASE)
        tokens = [token.strip().lower() for token in tokens if token.strip()]

        def parse_tokens(tokens):
            stack = []
            current_node = None

            for token in tokens:
                if token == '(':
                    stack.append(current_node)
                    current_node = None
                elif token == ')':
                    if not stack:
                        raise ValueError("Unbalanced parentheses")
                    previous_node = stack.pop()
                    if previous_node is not None:
                        if previous_node.left is None:
                            previous_node.left = current_node
                        else:
                            previous_node.right = current_node
                        current_node = previous_node
                elif token in ['and', 'or']:
                    new_node = Node('operator', value=token)
                    new_node.left = current_node
                    current_node = new_node
                else:
                    condition_node = Node('operand', value=token)
                    if current_node is None:
                        current_node = condition_node
                    else:
                        current_node.right = condition_node

            if stack:
                raise ValueError("Unbalanced parentheses")
            return current_node

        return parse_tokens(tokens)
    
    except Exception as e:
        print(f"Error parsing rule: {e}")
        return None


def evaluate_rule(node, data):
    """
    Recursively evaluates the AST (starting from the root node) against the user data.
    node: The root node of the AST (operator or operand).
    data: A dictionary containing user data (e.g., {"age": 35, "salary": 60000}).
    """
    if node.node_type == 'operand':
        # The node is a condition like "age > 30", we need to evaluate this condition
        condition = node.value
        result = eval_condition(condition, data)
        print(f"Evaluating operand: {condition} -> {result}")
        return result

    elif node.node_type == 'operator':
        # Evaluate the left side of the operator
        left_result = evaluate_rule(node.left, data)
        print(f"Evaluating left side of {node.value}: {left_result}")

        if node.value == 'and':
            # If it's AND, we must evaluate both sides
            right_result = evaluate_rule(node.right, data)
            print(f"Evaluating right side of {node.value}: {right_result}")
            return left_result and right_result

        elif node.value == 'or':
            # If it's OR, return True if the left side is True, otherwise check the right side
            if left_result:
                return True
            else:
                right_result = evaluate_rule(node.right, data)
                print(f"Evaluating right side of {node.value}: {right_result}")
                return right_result


VALID_ATTRIBUTES = ['age', 'department', 'salary', 'experience']

def eval_condition(condition, data):
    match = re.match(r"(\w+)\s*(==|!=|>|<|>=|<=|in)\s*(\d+|'[^']+'|\"[^\"]+\")", condition)
    if not match:
        raise ValueError(f"Invalid condition: {condition}")

    field, operator, value = match.groups()

    # Validate the field
    if field not in VALID_ATTRIBUTES:
        raise ValueError(f"Invalid attribute: {field}")

    # Process the value
    if operator == 'in':
        value = value.strip("'\"")  # Remove quotes if it's a string
        value_list = [v.strip() for v in value.split(',')]
        data_value = data.get(field)
        return data_value in value_list

    if value.startswith("'") or value.startswith('"'):
        value = value.strip("'\"")
    else:
        value = int(value)

    data_value = data.get(field)

    # Evaluate based on the operator
    if operator == '>':
        return data_value > value
    elif operator == '<':
        return data_value < value
    elif operator == '>=':
        return data_value >= value
    elif operator == '<=':
        return data_value <= value
    elif operator == '==':
        return data_value == value
    elif operator == '!=':
        return data_value != value



def combine_rules(rules):
    if not rules:
        return None

    # Start with the first rule's AST
    combined_ast = create_rule(rules[0])

    for rule in rules[1:]:
        # Create the AST for the new rule
        new_ast = create_rule(rule)

        # Combine using OR for simplicity
        combined_ast = Node('operator', left=combined_ast, right=new_ast, value='or')

    return combined_ast


if __name__ == "__main__":
    # Define your rules
    rule1 = "(age > 30 AND department == 'Sales')"
    rule2 = "(experience > 5 AND salary > 40000)"
    
    # Combine the rules
    combined_ast = combine_rules([rule1, rule2])
    
    print(f"Combined AST: {combined_ast}")
    
    # Example user data
    user_data = {"age": 32, "department": "Sales", "salary": 45000, "experience": 3}
    
    # Evaluate the combined rule
    result = evaluate_rule(combined_ast, user_data)
    print(f"User data matches combined rule: {result}")