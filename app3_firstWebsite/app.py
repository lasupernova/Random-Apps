from flask import Flask, render_template

#initiate Flask-object
app =Flask(__name__)

#decorator mapping '/'-route to subsequent function
@app.route('/')
def home():
    return render_template('home.html') #html-files need to be stored in folder named "templates"

@app.route('/about')
def about():
    return render_template('about.html')

#run app if this file is executed directly
if __name__ == "__main__":
    app.run(debug=True)



