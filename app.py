import json
import streamlit as st
from errors import ParseError, BuildError, ExecutionError
from parser import parse
from builder import build
from executor import execute
import db

st.set_page_config(page_title="mini-nl2sql", layout="centered")

db.init_db()

st.title("mini-nl2sql")
st.caption(
    "A mini deterministic NL-to-SQL tool — rule-based parser, "
    "sqlglot AST builder, full audit trail. No LLM in the "
    "calculation path."
)

st.write('Try: "How many orders did customer 5 place?" or "What is the total amount of all orders?"')

question = st.text_input(
    "Question:",
    placeholder="How many orders did customer 5 place?",
)

if st.button("Ask", type="primary") and question:
    try:
        intent = parse(question)
        sql = build(intent)
        result = execute(sql)

        st.subheader("Parsed Intent")
        st.code(json.dumps(intent, indent=2), language="json")

        st.subheader("Generated SQL (via sqlglot AST)")
        st.code(sql, language="sql")

        st.subheader("Result")
        if result["rows"] and result["rows"][0][0] is not None:
            st.code(f"{result['columns'][0]} = {result['rows'][0][0]}", language="text")
        else:
            st.warning("No data (or NULL result — e.g. customer has 0 orders)")

        st.subheader("Audit Trail")
        audit_data = {
            "method": "rule-based (no LLM in calculation path)",
            "tables used": [intent["table"]],
            "columns used": (
                ["customer_id", "amount"]
                if intent["filter_column"]
                else ["amount"]
            ),
            "execution_ms": result["time_ms"],
            "rows_returned": len(result["rows"]),
        }
        st.code(json.dumps(audit_data, indent=2), language="json")
    except ParseError as e:
        st.error(str(e))
    except (BuildError, ExecutionError) as e:
        st.error(str(e))
