import sys
from errors import ParseError, BuildError, ExecutionError
from parser import parse
from builder import build
from executor import execute
from reporter import report


def run(question: str) -> int:
    try:
        intent = parse(question)
        sql = build(intent)
        result = execute(sql)
        report(question, intent, sql, result)
        return 0
    except ParseError as e:
        print(f"ParseError: {e}")
        return 1
    except BuildError as e:
        print(f"BuildError: {e}")
        return 1
    except ExecutionError as e:
        print(f"ExecutionError: {e}")
        return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python main.py "<your question>"')
        print()
        print("Examples:")
        print('  python main.py "How many orders did customer 5 place?"')
        print('  python main.py "What is the total amount of all orders?"')
        print('  python main.py "What is the average amount for customer 3?"')
        sys.exit(1)
    question = sys.argv[1]
    sys.exit(run(question))
