from flask import Flask, render_template, request
import pandas as pd
import numpy as np

popular_df = pd.read_pickle('popular.pkl')
pt = pd.read_pickle('pt.pkl')
books = pd.read_pickle('books.pkl')
similarity_score = pd.read_pickle('similarity_score.pkl')
app = Flask(__name__)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        if form_type == 'form1':
            # Process the form data here
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            email = request.form.get('email')
            message = request.form.get('message')
            # Print form details to the console
            print(f"Received form data - Name: {fname} {lname}, Email: {email}, Message: {message}")
            # You can add further processing or store the data in a database here
            return 'Form submitted successfully!'
        elif form_type == 'form2':
            email = request.form.get('email')
            print(f"Received form data - Email: {email} ")
            return 'Form submitted successfully!'

    else:
        # Render the contact page template for GET requests
        return render_template('contact.html')

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Process the form data here
        email = request.form.get('email')
        # Print form details to the console
        print(f"Received form data - Email: {email}")
        # You can add further processing or store the data in a database here
        return 'Form submitted successfully!'
    else :
        return render_template('index.html',
                                book_name=list(popular_df['Book-Title'].values),
                                author=list(popular_df['Book-Author'].values),
                                image=list(popular_df['Image-URL-M'].values)

                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/About_Us', methods=['GET', 'POST'])
def about_us():
    if request.method == 'POST':
        # Process the form data here
        Name = request.form.get('Name')
        Email = request.form.get('Email')
        Message = request.form.get('Message')
        # Print form details to the console
        print(f"Received form data - Name: {Name}, Email: {Email}, Message: {Message}")
        # You can add further processing or store the data in a database here
        return 'Form submitted successfully!'
    else:
        return render_template('About.html')


@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))
        data.append(item)

    print(data)

    return render_template('recommend.html', data=data)



    return str(user_input)

if __name__== '__main__':
    app.run(debug=True)
