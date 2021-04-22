# Put your app in here.
from flask import Flask, request
from operations import add, sub, mult, div

app = Flask(__name__) 

@app.route('/add')
def add_plus():
    """Add a and b."""    
    a = int(request.args.get("a"))
    b = int(request.args.get("b"))
    total = add(a, b)
    return str(total)

@app.route('/sub')
def sub_minus():
    """Substract b from a."""
    a = int(request.args.get("a"))
    b = int(request.args.get("b"))
    total = sub(a, b)
    return str(total)

@app.route('/mult')
def multi_ply():
    """Multiply a and b."""
    a = int(request.args.get("a"))
    b = int(request.args.get("b"))
    total = mult(a, b)
    return str(total)

@app.route('/div')
def div_ide():
    """Divide a by b."""  
    a = int(request.args.get("a"))
    b = int(request.args.get("b"))
    total = div(a, b)
    return str(total)


mathematics = {
        "add": add,
        "sub": sub,
        "mult": mult,
        "div": div,
        }

@app.route("/math/<math>")
def see_math(math):
    """Do math on a and b."""
    a = int(request.args.get("a"))
    b = int(request.args.get("b"))
    total = mathematics[math](a, b)
    return str(total)