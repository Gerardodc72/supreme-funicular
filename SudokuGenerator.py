import random
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Sudoku Generator</title>
<style>
body { font-family: Arial; margin: 40px;}
table { border-collapse: collapse; }
td { width: 36px; height: 36px; text-align: center; border: 1px solid #333; font-size: 1.3em;}
input { width: 32px; height: 32px; font-size: 1.2em; text-align: center;}
</style>
</head>
<body>
<h1>Sudoku Generator</h1>
<form method="post">
    <button>Generate New Puzzle</button>
</form>
<table>
{% for row in puzzle %}
<tr>
    {% for val in row %}
        <td>
        {% if val != 0 %}
            <b>{{val}}</b>
        {% else %}
            <input maxlength="1">
        {% endif %}
        </td>
    {% endfor %}
</tr>
{% endfor %}
</table>
<p><small>Filled cells are the clues. Try to solve!</small></p>
</body>
</html>
"""

def pattern(r,c): return (3*(r%3)+r//3+c)%9
def shuffle(s): return random.sample(s,len(s))
def generate_sudoku():
    base  = range(3)
    rows  = [g*3 + r for g in shuffle(base) for r in shuffle(base)]
    cols  = [g*3 + c for g in shuffle(base) for c in shuffle(base)]
    nums  = shuffle(range(1,10))
    board = [[nums[pattern(r,c)] for c in cols] for r in rows]
    squares = 81
    empties = random.randint(35,55)
    for p in random.sample(range(squares), empties):
        board[p//9][p%9] = 0
    return board

@app.route("/", methods=["GET","POST"])
def index():
    puzzle = generate_sudoku() if request.method=="POST" else generate_sudoku()
    return render_template_string(HTML, puzzle=puzzle)

if __name__ == "__main__":
    app.run(debug=True)