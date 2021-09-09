
"""
server file to run the assignment file
"""

from assignment import app

app.add_api('assignment_swagger.yaml')

if __name__ == '__main__':
    app.run(debug=True)
